"""
Regression tests for P5 — append-only / non-destructive content writes.

Guards the write_content fix: re-ingesting a file (same content hash) must
never wipe enrichment columns (quality_score, tags, embeddings, etc.) that an
earlier run populated. See CODEBASE_AUDIT_2026-06-23.md finding #2.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.registry.writer import RegistryWriter
from wecape.registry.reader import RegistryReader


def _new_writer(tmp_path):
    db = tmp_path / "wecape.db"
    w = RegistryWriter(db_path=db)
    w.write_run(run_id="R1", we_forge_version="1.0.0",
                source_path="/src", output_path="/out")
    return w, db


def test_enrichment_preserved_on_sparse_rewrite(tmp_path):
    """A later, AI-free re-ingest must not null prior enrichment."""
    w, db = _new_writer(tmp_path)
    w.write_content(run_id="R1", content_id="HASH1", filename="a.mp4",
                    original_path="/src/a.mp4", quality_score=0.91,
                    content_tags="ride,sunset", highlight_score=0.7,
                    camera_family="DJI")
    w.write_run(run_id="R2", we_forge_version="1.0.0",
                source_path="/src", output_path="/out2")
    # Re-ingest with only the basic fields a non-AI run would supply.
    w.write_content(run_id="R2", content_id="HASH1", filename="a.mp4",
                    original_path="/src2/a.mp4")
    w.close()

    r = RegistryReader(db_path=db)
    rec = r.get_content("HASH1")
    r.close()
    assert rec["quality_score"] == 0.91, "quality_score was wiped"
    assert rec["content_tags"] == "ride,sunset", "content_tags were wiped"
    assert rec["highlight_score"] == 0.7, "highlight_score was wiped"
    assert rec["camera_family"] == "DJI", "camera_family was wiped"
    assert rec["run_id"] == "R2", "run_id should track latest sighting"
    assert rec["original_path"] == "/src2/a.mp4", "path should update to latest"


def test_first_seen_preserved_last_seen_refreshed(tmp_path):
    w, db = _new_writer(tmp_path)
    w.write_content(run_id="R1", content_id="H", filename="a.mp4", original_path="/a")
    r = RegistryReader(db_path=db)
    first = r.get_content("H")
    r.close()

    time.sleep(0.01)
    w.write_content(run_id="R1", content_id="H", filename="a.mp4", original_path="/a")
    w.close()

    r = RegistryReader(db_path=db)
    rec = r.get_content("H")
    r.close()
    assert rec["first_seen"] == first["first_seen"], "first_seen must never change"
    assert rec["last_seen"] >= first["last_seen"], "last_seen must refresh"


def test_explicit_value_overwrites(tmp_path):
    """Supplying a new non-null enrichment value should win (not COALESCE-stuck)."""
    w, db = _new_writer(tmp_path)
    w.write_content(run_id="R1", content_id="H", filename="a.mp4",
                    original_path="/a", quality_score=0.5)
    w.write_content(run_id="R1", content_id="H", filename="a.mp4",
                    original_path="/a", quality_score=0.95)
    w.close()
    r = RegistryReader(db_path=db)
    rec = r.get_content("H")
    r.close()
    assert rec["quality_score"] == 0.95, "explicit new value should overwrite"
