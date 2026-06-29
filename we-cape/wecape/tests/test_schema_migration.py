"""
Tests for the registry schema migrations, applied idempotently and without data
loss so a live registry upgrades safely on next open.

  v1 -> v2: runs.we_forge_version -> runs.we_cape_version (rebrand)
  v2 -> v3: content.source_clip + source_clip_sha (derivation lineage)
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.registry.schema import (
    initialize_registry, get_schema_version, migrate, _table_columns,
    SCHEMA_VERSION,
)


def test_fresh_db_is_current_with_all_columns(tmp_path):
    conn = initialize_registry(tmp_path / "fresh.db")
    runs = _table_columns(conn, "runs")
    content = _table_columns(conn, "content")
    assert "we_cape_version" in runs and "we_forge_version" not in runs
    assert "source_clip" in content and "source_clip_sha" in content
    assert get_schema_version(conn) == SCHEMA_VERSION
    conn.close()


def test_legacy_db_migrates_rename_and_lineage_without_data_loss(tmp_path):
    db = tmp_path / "legacy.db"
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    # A realistic v1 DB: old runs column + a content table lacking source_clip.
    conn.execute(
        "CREATE TABLE runs (id TEXT PRIMARY KEY, timestamp TEXT, "
        "we_forge_version TEXT, source_path TEXT, output_path TEXT, "
        "file_count INTEGER DEFAULT 0)"
    )
    conn.execute(
        "CREATE TABLE content (id TEXT PRIMARY KEY, filename TEXT, "
        "first_seen TEXT, last_seen TEXT)"
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
    conn.execute(
        "INSERT INTO content (id, filename, first_seen, last_seen) "
        "VALUES ('H', 'a.mp4', '2026-06-01', '2026-06-01')"
    )
    conn.commit()

    result_version = migrate(conn)

    runs = _table_columns(conn, "runs")
    content = _table_columns(conn, "content")
    assert "we_cape_version" in runs and "we_forge_version" not in runs
    assert "source_clip" in content and "source_clip_sha" in content
    assert result_version == SCHEMA_VERSION
    # data preserved through both migrations
    assert conn.execute("SELECT we_cape_version FROM runs WHERE id='OLD'").fetchone()[0] == "0.9"
    assert conn.execute("SELECT file_count FROM runs WHERE id='OLD'").fetchone()[0] == 42
    assert conn.execute("SELECT filename FROM content WHERE id='H'").fetchone()[0] == "a.mp4"
    conn.close()


def test_migrate_is_idempotent(tmp_path):
    conn = initialize_registry(tmp_path / "x.db")
    assert migrate(conn) == SCHEMA_VERSION
    assert migrate(conn) == SCHEMA_VERSION  # second call must be a safe no-op
    conn.close()
