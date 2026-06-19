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
        we_forge_version: str,
        source_path: str,
        output_path: str,
        profile_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        """Write a new run record at the start of a pipeline run."""
        self.conn.execute(
            """
            INSERT OR IGNORE INTO runs
                (id, timestamp, we_forge_version, profile_id,
                 source_path, output_path, sync_status, metadata)
            VALUES (?, datetime('now'), ?, ?, ?, ?, 'local', ?)
            """,
            (
                run_id,
                we_forge_version,
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

    def write_content(
        self,
        run_id: str,
        content_id: str,
        filename: str,
        original_path: str,
        **kwargs,
    ) -> None:
        """
        Write or update a content record.
        Uses INSERT OR REPLACE — content_id (hash) is the primary key.
        Preserves first_seen on subsequent appearances.
        """
        now = datetime.now(timezone.utc).isoformat()

        # Preserve first_seen if content was seen in a previous run
        existing = self.conn.execute(
            "SELECT first_seen FROM content WHERE id = ?",
            (content_id,)
        ).fetchone()

        values = {
            "id": content_id,
            "run_id": run_id,
            "filename": filename,
            "original_path": original_path,
            "first_seen": existing["first_seen"] if existing else now,
            "last_seen": now,
            "content_type": kwargs.get("content_type", "original"),
            **{k: v for k, v in kwargs.items() if k != "content_type"},
        }

        columns = ", ".join(values.keys())
        placeholders = ", ".join("?" for _ in values)

        self.conn.execute(
            f"INSERT OR REPLACE INTO content ({columns}) VALUES ({placeholders})",
            list(values.values()),
        )
        self.conn.commit()

    def finalize_run(
        self,
        run_id: str,
        file_count: int,
        total_duration_sec: float,
        runtime_sec: float,
        errors: Optional[list] = None,
        diagnostics: Optional[list] = None,
    ) -> None:
        """Update run record with final statistics at pipeline completion."""
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

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
