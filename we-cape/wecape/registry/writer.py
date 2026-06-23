"""
wecape.registry.writer
=======================
RegistryWriter — persists stage results to the local SQLite registry.

Injected into StageContext at run start.
Stages call context.registry_writer.write_stage_result() only.
Stages never import this module directly.
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from wecape.registry.schema import initialize_registry, REGISTRY_PATH


class RegistryWriter:
    """
    Writes run and content records to the local registry.
    One instance per pipeline run.
    """

    def __init__(self, db_path: Path = REGISTRY_PATH):
        self.db_path = db_path
        self.conn: sqlite3.Connection = initialize_registry(db_path)

    def write_run(
        self,
        run_id: str,
        we_cape_version: Optional[str] = None,
        source_path: str = "",
        output_path: str = "",
        profile_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        **legacy,
    ) -> None:
        """
        Write a new run record at the start of a pipeline run.

        Accepts the legacy keyword ``we_forge_version`` as an alias for
        ``we_cape_version`` (pre-rebrand callers).
        """
        if we_cape_version is None:
            we_cape_version = legacy.get("we_forge_version", "")
        self.conn.execute(
            """
            INSERT OR IGNORE INTO runs
                (id, timestamp, we_cape_version, profile_id,
                 source_path, output_path, sync_status, metadata)
            VALUES (?, datetime('now'), ?, ?, ?, ?, 'local', ?)
            """,
            (
                run_id,
                we_cape_version,
                profile_id,
                source_path,
                output_path,
                json.dumps(metadata or {}),
            ),
        )
        self.conn.commit()

    def write_stage_result(
        self,
        run_id: str,
        stage_id: str,
        result: object,
    ) -> None:
        """Append stage result metadata to the run record."""
        row = self.conn.execute(
            "SELECT stage_results FROM runs WHERE id = ?", (run_id,)
        ).fetchone()

        existing = json.loads(row["stage_results"] or "[]") if row else []
        existing.append({
            "stage_id": stage_id,
            "success": result.success,
            "files_processed": result.files_processed,
            "files_skipped": result.files_skipped,
            "files_failed": result.files_failed,
            "duration_sec": result.duration_sec,
            "errors": result.errors,
            "diagnostics": result.diagnostics,
            "metadata": result.metadata,
        })

        self.conn.execute(
            "UPDATE runs SET stage_results = ? WHERE id = ?",
            (json.dumps(existing), run_id),
        )
        self.conn.commit()

    # Bookkeeping columns that always reflect the most recent sighting.
    # Everything else is enrichment and is preserved (never nulled) across runs.
    _ALWAYS_UPDATE = frozenset({"run_id", "filename", "original_path", "last_seen"})
    _NEVER_UPDATE = frozenset({"id", "first_seen"})

    def write_content(
        self,
        run_id: str,
        content_id: str,
        filename: str,
        original_path: str,
        **kwargs,
    ) -> None:
        """
        Write or enrich a content record (P5: append-only / never destructive).

        Uses INSERT ... ON CONFLICT(id) DO UPDATE so that re-ingesting a file
        (same content hash) NEVER wipes enrichment columns supplied by an
        earlier run. A column is updated only when this write supplies a
        non-NULL value for it; otherwise the prior value is kept via COALESCE.

        - first_seen  : set on first insert, preserved forever.
        - last_seen   : always refreshed to now.
        - run_id/paths: always reflect the most recent run that saw the file.
        - quality_score, content_tags, alignment_offset_ms, highlight_score,
          embeddings, etc.: preserved if not re-supplied (no silent loss).

        Only columns explicitly provided are touched on conflict; columns
        omitted entirely are left exactly as they were.
        """
        now = datetime.now(timezone.utc).isoformat()

        values = {
            "id": content_id,
            "run_id": run_id,
            "filename": filename,
            "original_path": original_path,
            "first_seen": now,   # insert-only; ON CONFLICT never overwrites this
            "last_seen": now,
        }
        # content_type and any enrichment fields only when explicitly provided,
        # so unspecified columns keep their schema default on insert and their
        # prior value on conflict.
        values.update(kwargs)

        cols = list(values.keys())
        placeholders = ", ".join("?" for _ in cols)

        set_parts = []
        for c in cols:
            if c in self._NEVER_UPDATE:
                continue
            if c in self._ALWAYS_UPDATE:
                set_parts.append(f"{c} = excluded.{c}")
            else:
                # Enrichment: keep existing value when the new value is NULL.
                set_parts.append(f"{c} = COALESCE(excluded.{c}, content.{c})")

        sql = (
            f"INSERT INTO content ({', '.join(cols)}) "
            f"VALUES ({placeholders}) "
            f"ON CONFLICT(id) DO UPDATE SET {', '.join(set_parts)}"
        )
        self.conn.execute(sql, list(values.values()))
        self.conn.commit()

    def finalize_run(
        self,
        run_id: str,
        file_count: int,
        total_duration_sec: float,
        runtime_sec: float,
        errors: Optional[list] = None,
        diagnostics: Optional[list] = None,
        prune_if_empty: bool = True,
    ) -> bool:
        """
        Update run record with final statistics at pipeline completion.

        If the run processed no files (file_count <= 0 — e.g. it ran against a
        source still being copied) and prune_if_empty is True, the run row is
        removed instead of persisted, so empty no-op runs never enter the
        registry. Returns True if the run was pruned, False if it was updated.
        See "Known Registry Anomaly" in CLAUDE.md.
        """
        if prune_if_empty and (file_count is None or file_count <= 0):
            self.conn.execute("DELETE FROM content WHERE run_id = ?", (run_id,))
            self.conn.execute("DELETE FROM runs WHERE id = ?", (run_id,))
            self.conn.commit()
            return True

        self.conn.execute(
            """
            UPDATE runs SET
                file_count = ?,
                total_duration_sec = ?,
                runtime_sec = ?,
                errors = ?,
                diagnostics = ?
            WHERE id = ?
            """,
            (
                file_count,
                total_duration_sec,
                runtime_sec,
                json.dumps(errors or []),
                json.dumps(diagnostics or []),
                run_id,
            ),
        )
        self.conn.commit()
        return False

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
