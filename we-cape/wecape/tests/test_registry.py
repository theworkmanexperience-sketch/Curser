"""Tests for wecape.registry — schema, writer, reader."""

import json
import pathlib
import tempfile
import pytest

from wecape.registry.schema import initialize_registry, get_schema_version, SCHEMA_VERSION
from wecape.registry.writer import RegistryWriter
from wecape.registry.reader import RegistryReader


@pytest.fixture
def tmp_db():
    """Temporary database for each test."""
    tmp = pathlib.Path(tempfile.mktemp(suffix=".db"))
    yield tmp
    if tmp.exists():
        tmp.unlink()


@pytest.fixture
def writer(tmp_db):
    w = RegistryWriter(tmp_db)
    yield w
    w.close()


@pytest.fixture
def writer_reader(tmp_db):
    w = RegistryWriter(tmp_db)
    r = RegistryReader(tmp_db)
    yield w, r
    w.close()
    r.close()


# --- Schema tests ---

def test_initialize_creates_all_tables(tmp_db):
    conn = initialize_registry(tmp_db)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()]
    assert "runs" in tables
    assert "content" in tables
    assert "preferences" in tables
    assert "schema_version" in tables
    conn.close()


def test_schema_version_is_current(tmp_db):
    conn = initialize_registry(tmp_db)
    version = get_schema_version(conn)
    assert version == SCHEMA_VERSION
    conn.close()


def test_initialize_is_idempotent(tmp_db):
    initialize_registry(tmp_db)
    conn = initialize_registry(tmp_db)  # second call must not raise
    version = get_schema_version(conn)
    assert version == SCHEMA_VERSION
    conn.close()


# --- Writer tests ---

def test_write_run_creates_record(writer):
    writer.write_run("run-001", "weforge-1.0", "/src", "/out", "ryderz")
    row = writer.conn.execute(
        "SELECT * FROM runs WHERE id = ?", ("run-001",)
    ).fetchone()
    assert row is not None
    assert row["source_path"] == "/src"
    assert row["sync_status"] == "local"


def test_write_run_is_idempotent(writer):
    writer.write_run("run-001", "weforge-1.0", "/src", "/out")
    writer.write_run("run-001", "weforge-1.0", "/src", "/out")  # should not raise
    count = writer.conn.execute(
        "SELECT COUNT(*) FROM runs WHERE id = ?", ("run-001",)
    ).fetchone()[0]
    assert count == 1


def test_write_content_creates_record(writer):
    writer.write_run("run-001", "weforge-1.0", "/src", "/out")
    writer.write_content(
        "run-001", "hash-abc", "GX011863.MP4", "/src/GX011863.MP4",
        camera_family="GoPro", shoot_date="2026-06-01"
    )
    row = writer.conn.execute(
        "SELECT * FROM content WHERE id = ?", ("hash-abc",)
    ).fetchone()
    assert row is not None
    assert row["filename"] == "GX011863.MP4"
    assert row["camera_family"] == "GoPro"
    assert row["content_type"] == "original"


def test_write_content_preserves_first_seen(writer):
    writer.write_run("run-001", "weforge-1.0", "/src", "/out")
    writer.write_content("run-001", "hash-abc", "GX011863.MP4", "/src/GX011863.MP4")
    first_seen = writer.conn.execute(
        "SELECT first_seen FROM content WHERE id = ?", ("hash-abc",)
    ).fetchone()["first_seen"]

    writer.write_run("run-002", "weforge-1.0", "/src", "/out")
    writer.write_content("run-002", "hash-abc", "GX011863.MP4", "/src/GX011863.MP4")
    still_first = writer.conn.execute(
        "SELECT first_seen FROM content WHERE id = ?", ("hash-abc",)
    ).fetchone()["first_seen"]

    assert first_seen == still_first


def test_finalize_run_updates_stats(writer):
    writer.write_run("run-001", "weforge-1.0", "/src", "/out")
    writer.finalize_run("run-001", 103, 3200.0, 540.0, errors=[], diagnostics=[])
    row = writer.conn.execute(
        "SELECT * FROM runs WHERE id = ?", ("run-001",)
    ).fetchone()
    assert row["file_count"] == 103
    assert row["runtime_sec"] == 540.0


# --- Reader tests ---

def test_get_run_returns_record(writer_reader):
    w, r = writer_reader
    w.write_run("run-001", "weforge-1.0", "/src", "/out", "ryderz")
    run = r.get_run("run-001")
    assert run is not None
    assert run["id"] == "run-001"
    assert run["profile_id"] == "ryderz"


def test_get_run_returns_none_for_missing(writer_reader):
    _, r = writer_reader
    assert r.get_run("nonexistent") is None


def test_list_content_for_run(writer_reader):
    w, r = writer_reader
    w.write_run("run-001", "weforge-1.0", "/src", "/out")
    w.write_content("run-001", "hash-a", "file_a.MP4", "/src/file_a.MP4")
    w.write_content("run-001", "hash-b", "file_b.MP4", "/src/file_b.MP4")
    content = r.list_content_for_run("run-001")
    assert len(content) == 2


def test_search_content_by_camera_family(writer_reader):
    w, r = writer_reader
    w.write_run("run-001", "weforge-1.0", "/src", "/out")
    w.write_content("run-001", "hash-a", "GX01.MP4", "/src/GX01.MP4", camera_family="GoPro")
    w.write_content("run-001", "hash-b", "VID.mp4", "/src/VID.mp4", camera_family="Insta360")
    gopro = r.search_content(camera_family="GoPro")
    assert len(gopro) == 1
    assert gopro[0]["camera_family"] == "GoPro"


def test_get_run_summary(writer_reader):
    w, r = writer_reader
    w.write_run("run-001", "weforge-1.0", "/src", "/out")
    w.write_content("run-001", "hash-a", "file_a.MP4", "/src/file_a.MP4",
                    camera_family="GoPro", shoot_date="2026-06-01")
    w.finalize_run("run-001", 1, 60.0, 10.0)
    summary = r.get_run_summary("run-001")
    assert summary["content_summary"]["total"] == 1
    assert summary["content_summary"]["camera_families"] == 1
