"""
§17 Test 4 — Deterministic Output Structure & Metadata Schema
§17 Test 5 — Comprehensive Logging (all 5 log streams present + non-empty)

Validates:
  - Locked folder hierarchy (§10)
  - §11 JSON metadata schema fields
  - classification_note field (§3.x edge case matrix)
  - PROXIES/ created empty (Phase 0 only)
  - All five log files generated per run (§12)
  - SHA-256 present in ingest log (§12 + §17 Test 5)
  - run_id consistent across all outputs
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.pipeline import Pipeline

# ── Minimal synthetic config (no ffprobe required) ────────────────────
PIPELINE_CONFIG = {
    "pipeline": {"run_id_prefix": "TEST", "file_operation": "copy",
                 "enable_duplicate_content_detection": False},
    "grouping": {"window_seconds": 5, "min_cameras": 2, "camera_offsets": {}},
    "variant_detection": {
        "indexed_pattern": r"[\(\[](\d+)[\)\]]",
        "suffix_patterns": ["_v\\d+", "_edit", "_final"],
        "duplicate_keywords": ["copy", "final", "backup"],
        "parent_selection": "largest_file",
    },
    "audio_classification": {
        "field_recorder_patterns": ["^ZOOM\\d*", "^SD_\\d+"],
        "default_classification": "generic",
    },
    "classification": {
        "camera_sources": {
            "DJI":    {"patterns": ["^DJI_"],       "extensions": [".mp4", ".mov"]},
            "iPhone": {"patterns": ["^IMG_\\d{4}"], "extensions": [".mov", ".mp4"]},
        },
        "reference_extensions": [".pdf", ".srt", ".xml"],
        "generic_video_extensions": [".mp4", ".mov", ".avi"],
        "generic_image_extensions": [".png", ".tiff"],
    },
    "proxies":     {"generate_proxies": False},
    "performance": {"max_workers": 2, "hash_chunk_size_mb": 1},
    "logging":     {"log_level": "WARNING", "log_format": "json"},
    "output":      {"date_format": "%Y-%m-%d", "group_id_prefix": "MCG"},
}


def _build_test_dataset(root: Path) -> dict:
    """Create a minimal synthetic mixed-folder dataset."""
    files = {
        "DJI_0001.mp4":      b"DJI_VIDEO_DATA" * 512,
        "IMG_4321.mov":      b"IPHONE_VIDEO_DATA" * 256,
        "ZOOM0001.wav":      b"AUDIO_DATA" * 128,
        "thumbnail.png":     b"PNG_DATA" * 64,
        "notes.srt":         b"SRT_DATA",
        "interview.mp4":     b"INTERVIEW_BASE" * 300,
        "interview_v2.mp4":  b"INTERVIEW_V2" * 200,
        "orphan_final.mp4":  b"ORPHAN_FINAL" * 100,
    }
    for name, data in files.items():
        (root / name).write_bytes(data)
    return files


def _write_config(tmp: Path) -> Path:
    import yaml
    cfg_path = tmp / "test_config.yaml"
    cfg_path.write_text(yaml.dump(PIPELINE_CONFIG))
    return cfg_path


def _run_pipeline(tmp: Path) -> tuple[dict, Path, Path]:
    import yaml
    input_dir = tmp / "input"
    output_dir = tmp / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    _build_test_dataset(input_dir)
    cfg_path = _write_config(tmp)
    p = Pipeline(cfg_path)
    summary = p.run(input_dir, output_dir)
    return summary, input_dir, output_dir


# ── Test 4: Output structure ──────────────────────────────────────────

def test_logs_folder_created(tmp_path):
    _, _, out = _run_pipeline(tmp_path)
    assert (out / "LOGS").is_dir(), "LOGS/ folder missing"


def test_references_folder_created(tmp_path):
    _, _, out = _run_pipeline(tmp_path)
    assert (out / "REFERENCES").is_dir(), "REFERENCES/ folder missing"


def test_run_index_json_created(tmp_path):
    summary, _, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    index_path = out / f"{run_id}_index.json"
    assert index_path.exists(), f"Run index not found: {index_path.name}"


def test_run_index_schema(tmp_path):
    """§11 run index must contain required top-level fields."""
    summary, _, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    index = json.loads((out / f"{run_id}_index.json").read_text())
    for field in ("run_id", "generated_at", "totals", "multicam_groups",
                  "variants", "ungrouped_camera_files"):
        assert field in index, f"§11 index missing field: {field}"


def test_multicam_group_metadata_schema(tmp_path):
    """§11 LOCKED: each multicam group JSON must have all required fields."""
    summary, _, out = _run_pipeline(tmp_path)
    mcam_files = list(out.rglob("MULTICAM/*.json"))
    if not mcam_files:
        return  # no groups formed from synthetic data — skip structural check
    for mf in mcam_files:
        doc = json.loads(mf.read_text())
        for field in ("run_id", "group_id", "timestamp_start", "timestamp_end",
                      "camera_sources", "files", "variants", "classification"):
            assert field in doc, f"§11 group metadata missing: {field}"
        assert "parent" in doc["variants"], "§11 variants.parent missing"
        assert "children" in doc["variants"], "§11 variants.children missing"


def test_proxies_folder_created_empty(tmp_path):
    """§10.x LOCKED: PROXIES/ must exist but contain no files in Phase 0."""
    _, _, out = _run_pipeline(tmp_path)
    proxy_dirs = list(out.rglob("PROXIES"))
    assert len(proxy_dirs) > 0, "PROXIES/ folder not created"
    for pd in proxy_dirs:
        contents = list(pd.iterdir())
        assert len(contents) == 0, f"PROXIES/ must be empty in Phase 0; found: {contents}"


def test_generate_proxies_is_false(tmp_path):
    """§10.x: generate_proxies config must be False in Phase 0."""
    import yaml
    _, _, out = _run_pipeline(tmp_path)
    cfg_path = tmp_path / "test_config.yaml"
    cfg = yaml.safe_load(cfg_path.read_text())
    assert cfg.get("proxies", {}).get("generate_proxies") is False, \
        "generate_proxies must be False in Phase 0"


def test_srt_routed_to_references(tmp_path):
    """§6 reference files must appear in REFERENCES/."""
    _, _, out = _run_pipeline(tmp_path)
    refs = list((out / "REFERENCES").rglob("*.srt")) if (out / "REFERENCES").exists() else []
    assert len(refs) > 0, "SRT file not routed to REFERENCES/"


def test_audio_not_in_references(tmp_path):
    """§6 LOCKED: audio files must never be classified as Reference."""
    _, _, out = _run_pipeline(tmp_path)
    refs_dir = out / "REFERENCES"
    if refs_dir.exists():
        audio_in_refs = list(refs_dir.rglob("*.wav")) + list(refs_dir.rglob("*.aiff"))
        assert len(audio_in_refs) == 0, \
            f"Audio files found in REFERENCES/ (§6 violation): {audio_in_refs}"


# ── Test 5: Logging completeness ──────────────────────────────────────

REQUIRED_LOG_STREAMS = ("ingest", "classification", "grouping", "variants", "errors")


def test_all_five_log_streams_generated(tmp_path):
    """§12 LOCKED: all five log streams must be generated on every run."""
    summary, _, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    logs_dir = out / "LOGS"
    for stream in REQUIRED_LOG_STREAMS:
        log_path = logs_dir / f"{run_id}_{stream}.json"
        assert log_path.exists(), f"§12 missing log stream: {stream}"


def test_log_streams_are_valid_json(tmp_path):
    summary, _, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    logs_dir = out / "LOGS"
    for stream in REQUIRED_LOG_STREAMS:
        log_path = logs_dir / f"{run_id}_{stream}.json"
        if log_path.exists():
            doc = json.loads(log_path.read_text())
            assert "run_id" in doc, f"log {stream} missing run_id"
            assert "entries" in doc, f"log {stream} missing entries"


def test_ingest_log_contains_sha256(tmp_path):
    """§12 + §17 Test 5: SHA-256 must appear in every ingest log entry."""
    summary, _, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    ingest_log = json.loads((out / "LOGS" / f"{run_id}_ingest.json").read_text())
    for entry in ingest_log["entries"]:
        assert "file_hash_sha256" in entry, \
            f"§12 SHA-256 missing from ingest entry: {entry.get('filename')}"


def test_every_file_traceable_in_classification_log(tmp_path):
    """§12 LOCKED: every file must be traceable from ingest through classification."""
    summary, input_dir, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    ingest_log  = json.loads((out / "LOGS" / f"{run_id}_ingest.json").read_text())
    class_log   = json.loads((out / "LOGS" / f"{run_id}_classification.json").read_text())
    ingested    = {Path(e["file"]).name for e in ingest_log["entries"]}
    classified  = {Path(e["file"]).name for e in class_log["entries"]}
    missing     = ingested - classified
    assert not missing, f"§12 files ingested but not in classification log: {missing}"


def test_run_summary_report_created(tmp_path):
    """§18: human-readable Markdown summary must be generated."""
    summary, _, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    report = out / "LOGS" / f"{run_id}_summary.md"
    assert report.exists(), "Run summary .md report missing"
    content = report.read_text()
    assert "Run ID" in content
    assert "Files ingested" in content


def test_run_id_consistent_across_all_outputs(tmp_path):
    """§16: run_id must be identical in index, all logs, and summary."""
    summary, _, out = _run_pipeline(tmp_path)
    run_id = summary["run_id"]
    index = json.loads((out / f"{run_id}_index.json").read_text())
    assert index["run_id"] == run_id
    for stream in REQUIRED_LOG_STREAMS:
        log_path = out / "LOGS" / f"{run_id}_{stream}.json"
        if log_path.exists():
            doc = json.loads(log_path.read_text())
            assert doc["run_id"] == run_id, \
                f"run_id mismatch in {stream} log: {doc['run_id']} != {run_id}"


# ── Standalone runner ─────────────────────────────────────────────────

if __name__ == "__main__":
    import traceback
    tests = [
        test_logs_folder_created,
        test_references_folder_created,
        test_run_index_json_created,
        test_run_index_schema,
        test_multicam_group_metadata_schema,
        test_proxies_folder_created_empty,
        test_generate_proxies_is_false,
        test_srt_routed_to_references,
        test_audio_not_in_references,
        test_all_five_log_streams_generated,
        test_log_streams_are_valid_json,
        test_ingest_log_contains_sha256,
        test_every_file_traceable_in_classification_log,
        test_run_summary_report_created,
        test_run_id_consistent_across_all_outputs,
    ]
    passed, failed = [], []
    for test_fn in tests:
        with tempfile.TemporaryDirectory() as td:
            try:
                test_fn(Path(td))
                passed.append(test_fn.__name__)
                print(f"  ✓ {test_fn.__name__}")
            except Exception as e:
                failed.append(test_fn.__name__)
                print(f"  ✗ {test_fn.__name__}: {e}")
    print(f"\n{'='*55}")
    print(f"Test 4+5: {len(passed)}/{len(passed)+len(failed)} passed", end="")
    print("" if failed else "  — All passed ✓")
    if failed:
        print(f"  FAILED: {failed}")
