"""
Tests for the registry schema migration (CODEBASE_AUDIT_2026-06-23 finding #6):
rebrand of runs.we_forge_version -> runs.we_cape_version, applied idempotently
and without data loss, so an existing live registry upgrades safely on next open.
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.registry.schema import (
    initialize_registry, get_schema_version, migrate, _table_columns,
)


def test_fresh_db_is_v2_with_rebranded_column(tmp_path):
    conn = initialize_registry(tmp_path / "fresh.db")
    cols = _table_columns(conn, "runs")
    assert "we_cape_version" in cols
    assert "we_forge_version" not in cols
    assert get_schema_version(conn) == 2
    conn.close()


def test_legacy_v1_db_migrates_without_data_loss(tmp_path):
    db = tmp_path / "legacy.db"
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE runs (id TEXT PRIMARY KEY, timestamp TEXT, "
        "we_forge_version TEXT, source_path TEXT, output_path TEXT, "
        "file_count INTEGER DEFAULT 0)"
    )
    conn.execute(
        "CREATE TABLE schema_version (version INTEGER PRIMARY KEY, "
        "applied_at TEXT, description TEXT)"
    )
    conn.execute("INSERT INTO schema_version VALUES (1, datetime('now'), 'v1')")
    conn.execute(
        "INSERT INTO runs (id, timestamp, we_forge_version, source_path, "
        "output_path, file_count) VALUES ('OLD', '2026-06-01', '0.9', '/s', '/o', 42)"
    )
    conn.commit()

    result_version = migrate(conn)

    cols = _table_columns(conn, "runs")
    assert "we_cape_version" in cols and "we_forge_version" not in cols
    assert result_version == 2
    row = conn.execute("SELECT * FROM runs WHERE id='OLD'").fetchone()
    assert row["we_cape_version"] == "0.9", "renamed column must keep its data"
    assert row["file_count"] == 42, "other columns untouched"
    conn.close()


def test_migrate_is_idempotent(tmp_path):
    conn = initialize_registry(tmp_path / "x.db")
    assert migrate(conn) == 2
    assert migrate(conn) == 2  # second call must be a safe no-op
    conn.close()
