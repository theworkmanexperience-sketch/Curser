"""Tests for weforge.core.manifest — RunManifest tri-format output."""

import json
import pytest
from datetime import datetime, timezone, timedelta
from weforge.core.manifest import RunManifest, ContentRecord, StageRecord


def make_manifest(with_content=True, with_errors=False):
    start = datetime.now(timezone.utc) - timedelta(seconds=540)
    m = RunManifest.create(
        run_id="run-test-001",
        source_path="/Volumes/10TB/O-SIX",
        output_path="/Volumes/10TB/WE_FLOW_OUTPUT",
        started_at=start,
        profile_id="ryderz",
    )
    if with_content:
        m.content = [
            ContentRecord(
                "GX011863.MP4", "/src/GX011863.MP4", "hash-abc",
                camera_family="GoPro", shoot_date="2026-06-01",
                proxy_path="/out/GX011863_proxy.mov",
                duration_sec=120.0,
            ),
            ContentRecord(
                "VID_001.mp4", "/src/VID_001.mp4", "hash-def",
                camera_family="Insta360", shoot_date="2026-06-01",
                duration_sec=90.0,
            ),
        ]
        m.stage_records = [
            StageRecord("ingest", "1.0.0", True, files_processed=2, duration_sec=12.3),
            StageRecord("proxy", "1.0.0", True, files_processed=1,
                        files_skipped=1, duration_sec=527.7),
        ]
    if with_errors:
        m.errors = [{"file": "bad.mp4", "reason": "corrupted"}]
    return m


# --- Factory ---

def test_create_sets_run_id():
    m = make_manifest()
    assert m.run_id == "run-test-001"


def test_create_sets_profile_id():
    m = make_manifest()
    assert m.profile_id == "ryderz"


def test_create_runtime_is_positive():
    m = make_manifest()
    assert m.runtime_sec > 0


# --- Computed properties ---

def test_total_files():
    m = make_manifest()
    assert m.total_files == 2


def test_proxied_files():
    m = make_manifest()
    assert m.proxied_files == 1


def test_total_duration_sec():
    m = make_manifest()
    assert m.total_duration_sec == 210.0


def test_camera_families_sorted():
    m = make_manifest()
    assert m.camera_families == ["GoPro", "Insta360"]


def test_shoot_dates():
    m = make_manifest()
    assert m.shoot_dates == ["2026-06-01"]


def test_has_errors_false_when_clean():
    m = make_manifest()
    assert m.has_errors is False


def test_has_errors_true_when_errors_present():
    m = make_manifest(with_errors=True)
    assert m.has_errors is True
    assert m.error_count == 1


def test_empty_manifest_properties():
    m = make_manifest(with_content=False)
    assert m.total_files == 0
    assert m.proxied_files == 0
    assert m.camera_families == []
    assert m.has_errors is False


# --- to_json ---

def test_to_json_schema_version():
    j = make_manifest().to_json()
    assert j["schema_version"] == "1.0"


def test_to_json_platform():
    j = make_manifest().to_json()
    assert j["platform"] == "W.E. FORGE"


def test_to_json_statistics():
    j = make_manifest().to_json()
    stats = j["statistics"]
    assert stats["total_files"] == 2
    assert stats["proxied_files"] == 1
    assert stats["error_count"] == 0
    assert "GoPro" in stats["camera_families"]


def test_to_json_content_count():
    j = make_manifest().to_json()
    assert len(j["content"]) == 2


def test_to_json_stages_count():
    j = make_manifest().to_json()
    assert len(j["stages"]) == 2


def test_to_json_is_serializable():
    j = make_manifest().to_json()
    dumped = json.dumps(j)
    assert isinstance(dumped, str)
    reloaded = json.loads(dumped)
    assert reloaded["run"]["id"] == "run-test-001"


def test_to_json_intelligence_keys_present():
    j = make_manifest().to_json()
    assert "intelligence" in j
    assert "quality" in j["intelligence"]
    assert "alignment" in j["intelligence"]
    assert "highlights" in j["intelligence"]


# --- to_html ---

def test_to_html_returns_string():
    h = make_manifest().to_html()
    assert isinstance(h, str)


def test_to_html_contains_run_id():
    h = make_manifest().to_html()
    assert "run-test-001" in h


def test_to_html_contains_status_completed():
    h = make_manifest().to_html()
    assert "COMPLETED" in h


def test_to_html_contains_file_count():
    h = make_manifest().to_html()
    assert "2" in h


def test_to_html_contains_camera_families():
    h = make_manifest().to_html()
    assert "GoPro" in h
    assert "Insta360" in h


def test_to_html_is_valid_html_structure():
    h = make_manifest().to_html()
    assert "<!DOCTYPE html>" in h
    assert "</html>" in h
    assert "<table>" in h


def test_to_html_shows_error_count_when_errors():
    h = make_manifest(with_errors=True).to_html()
    assert "1" in h


# --- to_fcpxml ---

def test_to_fcpxml_returns_string():
    fx = make_manifest().to_fcpxml()
    assert isinstance(fx, str)


def test_to_fcpxml_is_valid_xml_stub():
    fx = make_manifest().to_fcpxml()
    assert '<?xml version="1.0"' in fx
    assert "<fcpxml" in fx
    assert "</fcpxml>" in fx


def test_to_fcpxml_contains_run_id():
    fx = make_manifest().to_fcpxml()
    assert "run-test-001" in fx


def test_to_fcpxml_notes_j4_implementation():
    fx = make_manifest().to_fcpxml()
    assert "J4" in fx


# --- to_drxml ---

def test_to_drxml_returns_string():
    dr = make_manifest().to_drxml()
    assert isinstance(dr, str)


def test_to_drxml_is_valid_xml_stub():
    dr = make_manifest().to_drxml()
    assert '<?xml version="1.0"' in dr
    assert "<xmeml" in dr


def test_to_drxml_contains_run_id():
    dr = make_manifest().to_drxml()
    assert "run-test-001" in dr
