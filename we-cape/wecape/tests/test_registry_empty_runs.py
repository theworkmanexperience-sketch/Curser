"""
Regression tests for the empty-run guard (CODEBASE_AUDIT_2026-06-23 finding #3).

A run started against an empty source (e.g. rsync still in progress) must not
pollute listings or aggregates. Two layers:
  1. reader.list_runs / get_aggregate_stats exclude file_count == 0 by default.
  2. writer.finalize_run prunes a run row that finalizes with zero files.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.registry.writer import RegistryWriter
from wecape.registry.reader import RegistryReader


def test_finalize_prunes_empty_run(tmp_path):
    db = tmp_path / "wecape.db"
    w = RegistryWriter(db_path=db)
    w.write_run("EMPTY", "1.0.0", "/src", "/out")
    pruned = w.finalize_run("EMPTY", file_count=0, total_duration_sec=0.0, runtime_sec=0.0)
    w.close()
    assert pruned is True
    r = RegistryReader(db_path=db)
    assert r.get_run("EMPTY") is None, "empty run should be pruned, not persisted"
    r.close()


def test_finalize_keeps_nonempty_run(tmp_path):
    db = tmp_path / "wecape.db"
    w = RegistryWriter(db_path=db)
    w.write_run("REAL", "1.0.0", "/src", "/out")
    pruned = w.finalize_run("REAL", file_count=103, total_duration_sec=3200.0, runtime_sec=540.0)
    w.close()
    assert pruned is False
    r = RegistryReader(db_path=db)
    assert r.get_run("REAL")["file_count"] == 103
    r.close()


def test_list_runs_excludes_empty_by_default(tmp_path):
    db = tmp_path / "wecape.db"
    w = RegistryWriter(db_path=db)
    # A run that was opened but never finalized stays at file_count default 0.
    w.write_run("UNFINISHED", "1.0.0", "/src", "/out")
    w.write_run("GOOD", "1.0.0", "/src", "/out")
    w.finalize_run("GOOD", file_count=5, total_duration_sec=10.0, runtime_sec=2.0)
    w.close()

    r = RegistryReader(db_path=db)
    ids = {x["id"] for x in r.list_runs()}
    assert ids == {"GOOD"}, "empty/unfinished runs must be hidden by default"
    ids_all = {x["id"] for x in r.list_runs(include_empty=True)}
    assert {"GOOD", "UNFINISHED"} <= ids_all, "include_empty=True must show raw history"
    r.close()


def test_aggregate_stats_excludes_empty(tmp_path):
    db = tmp_path / "wecape.db"
    w = RegistryWriter(db_path=db)
    w.write_run("A", "1.0.0", "/src", "/out")
    w.finalize_run("A", file_count=10, total_duration_sec=100.0, runtime_sec=30.0)
    w.write_run("EMPTY", "1.0.0", "/src", "/out")  # never finalized -> file_count 0
    w.close()

    r = RegistryReader(db_path=db)
    stats = r.get_aggregate_stats()
    r.close()
    assert stats["run_count"] == 1, "empty run must not be counted"
    assert stats["total_files"] == 10
    assert stats["total_runtime_sec"] == 30.0
