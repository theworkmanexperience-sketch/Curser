"""
wecape.registry.reader
=======================
RegistryReader — read-only query interface for the local registry.

Used by W.E. ARCHIVE (J5) and the future W.E. API (J3).
Never writes — all writes go through RegistryWriter.
"""

import json
import sqlite3
from pathlib import Path
from typing import Optional

from wecape.registry.schema import get_connection, REGISTRY_PATH


class RegistryReader:
    """Read-only interface to the W.E. C.A.P.E. production registry."""

    def __init__(self, db_path: Path = REGISTRY_PATH):
        self.db_path = db_path
        self.conn: sqlite3.Connection = get_connection(db_path)

    def get_run(self, run_id: str) -> Optional[dict]:
        """Return a single run record by ID."""
        row = self.conn.execute(
            "SELECT * FROM runs WHERE id = ?", (run_id,)
        ).fetchone()
        return dict(row) if row else None

    def list_runs(self, limit: int = 50, include_empty: bool = False) -> list[dict]:
        """
        Return most recent runs, newest first.

        Empty/no-op runs (file_count == 0 — e.g. a run started against a source
        still being copied) are excluded by default so they never pollute
        listings or aggregates. Pass include_empty=True for raw history.
        See "Known Registry Anomaly" in CLAUDE.md.
        """
        where = "" if include_empty else "WHERE file_count > 0"
        rows = self.conn.execute(
            f"SELECT * FROM runs {where} ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_aggregate_stats(self) -> dict:
        """
        Roll-up across real runs only. Excludes empty runs by construction so
        the documented 'all aggregate queries must filter file_count > 0' rule
        is enforced in code, not just in docs.
        """
        row = self.conn.execute(
            """
            SELECT COUNT(*)                         AS run_count,
                   COALESCE(SUM(file_count), 0)     AS total_files,
                   COALESCE(SUM(runtime_sec), 0.0)  AS total_runtime_sec,
                   COALESCE(SUM(total_duration_sec), 0.0) AS total_media_sec
            FROM runs
            WHERE file_count > 0
            """
        ).fetchone()
        return dict(row) if row else {}

    def get_content(self, content_id: str) -> Optional[dict]:
        """Return a single content record by ID (hash)."""
        row = self.conn.execute(
            "SELECT * FROM content WHERE id = ?", (content_id,)
        ).fetchone()
        return dict(row) if row else None

    def list_content_for_run(self, run_id: str) -> list[dict]:
        """Return all content records for a given run."""
        rows = self.conn.execute(
            "SELECT * FROM content WHERE run_id = ? ORDER BY shoot_date, filename",
            (run_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def search_content(
        self,
        camera_family: Optional[str] = None,
        shoot_date: Optional[str] = None,
        content_type: Optional[str] = None,
        min_quality_score: Optional[float] = None,
        limit: int = 100,
    ) -> list[dict]:
        """
        Flexible content search — foundation for W.E. ARCHIVE (J5).
        All filters are optional and combined with AND.
        """
        conditions = []
        params = []

        if camera_family:
            conditions.append("camera_family = ?")
            params.append(camera_family)
        if shoot_date:
            conditions.append("shoot_date = ?")
            params.append(shoot_date)
        if content_type:
            conditions.append("content_type = ?")
            params.append(content_type)
        if min_quality_score is not None:
            conditions.append("quality_score >= ?")
            params.append(min_quality_score)

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        params.append(limit)

        rows = self.conn.execute(
            f"SELECT * FROM content {where} ORDER BY shoot_date DESC, filename LIMIT ?",
            params
        ).fetchall()
        return [dict(r) for r in rows]

    def get_run_summary(self, run_id: str) -> Optional[dict]:
        """Return a summary of a run including content counts."""
        run = self.get_run(run_id)
        if not run:
            return None

        counts = self.conn.execute(
            """
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN proxy_path IS NOT NULL THEN 1 ELSE 0 END) as proxied,
                COUNT(DISTINCT camera_family) as camera_families,
                COUNT(DISTINCT shoot_date) as shoot_dates
            FROM content WHERE run_id = ?
            """,
            (run_id,)
        ).fetchone()

        return {
            **run,
            "content_summary": dict(counts) if counts else {}
        }

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
