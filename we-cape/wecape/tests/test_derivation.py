"""
Tests for derivation lineage (select -> source clip), schema v3.

Lineage is a SEPARATE concept from §8 variant detection: it records that a
curated select derives from a source clip, without duplicate/redundancy
semantics, and is captured in content.source_clip / source_clip_sha.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.capture.derivation import DerivationResolver
from wecape.registry.writer import RegistryWriter
from wecape.registry.reader import RegistryReader


def test_select_resolves_to_source_stem():
    r = DerivationResolver()
    assert r.source_stem("VID_20260314_093040_00_006_sel01.mp4") == "VID_20260314_093040_00_006"
    # case-insensitive
    assert r.source_stem("VID_20260314_093040_00_006_SEL12.MP4") == "VID_20260314_093040_00_006"


def test_non_select_returns_none():
    r = DerivationResolver()
    assert r.source_stem("VID_20260314_093040_00_006.mp4") is None
    assert r.source_stem("DJI_0001.MP4") is None
    # a variant indexed name is NOT a select (different concept)
    assert r.source_stem("clip(1).mp4") is None


def test_resolve_pins_source_hash_when_source_in_run():
    r = DerivationResolver()
    r.index_sources([("VID_006", "SHA_SOURCE"), ("OTHER", "x")])
    stem, sha = r.resolve("VID_006_sel01.mp4")
    assert stem == "VID_006"
    assert sha == "SHA_SOURCE"


def test_resolve_returns_stem_without_hash_when_source_absent():
    r = DerivationResolver()
    stem, sha = r.resolve("VID_006_sel03.mp4")
    assert stem == "VID_006"
    assert sha is None


def test_disabled_resolver_is_noop():
    r = DerivationResolver(enabled=False)
    assert r.resolve("VID_006_sel01.mp4") == (None, None)


def test_source_clip_round_trips_through_registry(tmp_path):
    db = tmp_path / "wecape.db"
    w = RegistryWriter(db_path=db)
    w.write_run("R1", we_cape_version="1.0.0", source_path="/s", output_path="/o")
    w.write_content("R1", "HASH_SEL", "VID_006_sel01.mp4", "/s/VID_006_sel01.mp4",
                    source_clip="VID_006", source_clip_sha="HASH_SRC")
    w.close()
    rec = RegistryReader(db_path=db).get_content("HASH_SEL")
    assert rec["source_clip"] == "VID_006"
    assert rec["source_clip_sha"] == "HASH_SRC"


def test_lineage_preserved_on_sparse_rewrite(tmp_path):
    """Lineage must survive a later AI-free re-ingest (P5 field preservation)."""
    db = tmp_path / "wecape.db"
    w = RegistryWriter(db_path=db)
    w.write_run("R1", we_cape_version="1.0.0", source_path="/s", output_path="/o")
    w.write_content("R1", "H", "VID_006_sel01.mp4", "/s/VID_006_sel01.mp4",
                    source_clip="VID_006", source_clip_sha="SRCSHA")
    # later run re-ingests with only basics
    w.write_content("R1", "H", "VID_006_sel01.mp4", "/s/VID_006_sel01.mp4")
    w.close()
    rec = RegistryReader(db_path=db).get_content("H")
    assert rec["source_clip"] == "VID_006", "lineage must not be wiped on re-ingest"
    assert rec["source_clip_sha"] == "SRCSHA"
