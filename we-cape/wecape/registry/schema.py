"""
wecape.registry.schema
=======================
SQLite schema for the W.E. C.A.P.E. production registry.

Location: ~/.wecape/registry/wecape.db

Design principles:
  - Append-only by default (records never overwritten)
  - JSON columns for extensible metadata
  - Sync-ready (designed for eventual cloud sync without requiring it)
  - Creator-controlled (full export and deletion always available)
"""

import sqlite3
from pathlib import Path

REGISTRY_DIR = Path.home() / ".wecape" / "registry"
REGISTRY_PATH = REGISTRY_DIR / "wecape.db"
SCHEMA_VERSION = 1

RUNS_TABLE = """
CREATE TABLE IF NOT EXISTS runs (
    id                  TEXT PRIMARY KEY,
    timestamp           TEXT NOT NULL,
    we_forge_version    TEXT NOT NULL,
    profile_id          TEXT,
    source_path         TEXT NOT NULL,
    output_path         TEXT NOT NULL,
    file_count          INTEGER DEFAULT 0,
    total_duration_sec  REAL DEFAULT 0.0,
    runtime_sec         REAL DEFAULT 0.0,
    stage_results       TEXT,
    errors              TEXT,
    diagnostics         TEXT,
    sync_status         TEXT DEFAULT 'local',
    metadata            TEXT
);"""

CONTENT_TABLE = """
CREATE TABLE IF NOT EXISTS content (
    id                      TEXT PRIMARY KEY,
    run_id                  TEXT REFERENCES runs(id),
    filename                TEXT NOT NULL,
    original_path           TEXT NOT NULL,
    scaffold_path           TEXT,
    proxy_path              TEXT,
    camera_id               TEXT,
    camera_family           TEXT,
    corrected_timestamp     TEXT,
    shoot_date              TEXT,
    duration_sec            REAL,
    codec                   TEXT,
    resolution              TEXT,
    file_size_bytes         INTEGER,
    quality_score           REAL,
    content_tags            TEXT,
    alignment_offset_ms     REAL,
    highlight_score         REAL,
    model_version           TEXT,
    embedding_model_version TEXT,
    embedding_vector_dims   INTEGER,
    content_type            TEXT DEFAULT 'original',
    first_seen              TEXT NOT NULL,
    last_seen               TEXT NOT NULL,
    metadata                TEXT
);"""

PREFERENCES_TABLE = """
CREATE TABLE IF NOT EXISTS preferences (
    key         TEXT PRIMARY KEY,
    value       TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);"""

SCHEMA_VERSION_TABLE = """
CREATE TABLE IF NOT EXISTS schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL,
    description TEXT
);"""


def get_connection(db_path: Path = REGISTRY_PATH) -> sqlite3.Connection:
    """Return a connection to the registry database, creating it if needed."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def initialize_registry(db_path: Path = REGISTRY_PATH) -> sqlite3.Connection:
    """
    Create all tables and seed schema version.
    Safe to call on existing registry — CREATE IF NOT EXISTS.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.executescript(
        RUNS_TABLE + CONTENT_TABLE + PREFERENCES_TABLE + SCHEMA_VERSION_TABLE
    )
    cursor.execute(
        "INSERT OR IGNORE INTO schema_version (version, applied_at, description) VALUES (?, datetime('now'), ?)",
        (SCHEMA_VERSION, "Initial schema — W.E. C.A.P.E. v1.0")
    )
    conn.commit()
    return conn


def get_schema_version(conn: sqlite3.Connection) -> int:
    """Return current schema version from registry."""
    try:
        row = conn.execute(
            "SELECT MAX(version) as v FROM schema_version"
        ).fetchone()
        return row["v"] if row and row["v"] else 0
    except sqlite3.OperationalError:
        return 0
