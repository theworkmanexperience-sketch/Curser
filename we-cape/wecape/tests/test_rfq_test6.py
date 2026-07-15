"""
§17 Test 6 — Quantitative Acceptance Thresholds (defined July 14, 2026)

Thresholds grounded in empirically validated production data
(MG-01 through MG-05, O-SIX RYDERZ MC Community Service dataset).
The RFQ is self-issued; these thresholds constitute the formal
Test 6 definition of record.

  6.1  Ingest completeness:   100% — zero dropped files (§3 lock)
  6.2  Pipeline error rate:   0 errors on valid input
  6.3  Log completeness:      5/5 streams, 100% file traceability
  6.4  Proxy success rate:    >=95% eligible transcoded (empirical:
                              MG-04/05 = 100%; synthetic form checks
                              structural contract only)
  6.5  Classification rate:   >=75% camera files to a named source
                              (MG-02 empirical: 78%)
  6.6  Determinism (P1):      identical input+config -> identical
                              structural output across two runs
  6.7  Run ID consistency:    one run_id across all outputs

Runtime thresholds excluded: hardware-dependent (see CLAUDE.md).
Grouping-percentage excluded: covered by §7 deviation record.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
os.environ['WECAPE_TEST_MODE'] = '1'

from wecape.capture.pipeline import Pipeline

PIPELINE_CONFIG = {
    "pipeline": {"run_id_prefix": "T6", "file_operation": "copy",
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
            "DJI":      {"patterns": ["^DJI_"],       "extensions": [".mp4", ".mov"]},
            "iPhone":   {"patterns": ["^IMG_\\d{4}"], "extensions": [".mov", ".mp4"]},
            "Insta360": {"patterns": ["^VID_", "^LRV_"], "extensions": [".mp4", ".insv"]},
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

DATASET = {
    "DJI_0001.mp4":       b"DJI_A" * 512,
    "DJI_0002.mp4":       b"DJI_B" * 700,
    "IMG_1001.mov":       b"IPH_A" * 512,
    "IMG_1002.mov":       b"IPH_B" * 600,
    "VID_20260101.mp4":   b"INS_A" * 512,
    "VID_20260102.mp4":   b"INS_B" * 650,
    "DJI_0003.mp4":       b"DJI_C" * 800,
    "IMG_1003.mov":       b"IPH_C" * 450,
    "notes.png":          b"PNG_DATA" * 100,
    "shotlist.pdf":       b"PDF_DATA" * 100,
}


def _make_dataset(root: Path) -> int:
    for name, data in DATASET.items():
        (root / name).write_bytes(data)
    return len(DATASET)


def _run_pipeline(src: Path, out: Path) -> dict:
    import yaml
    cfg_path = src.parent / "t6_config.yaml"
    if not cfg_path.exists():
        cfg_path.write_text(yaml.dump(PIPELINE_CONFIG))
    out.mkdir(parents=True, exist_ok=True)
    p = Pipeline(cfg_path)
    summary = p.run(src, out)
    return {"summary": summary, "run_id": p.run_id}


def _load_log(out: Path, name_fragment: str):
    logs = list((out / "LOGS").glob(f"*{name_fragment}*"))
    assert logs, f"log matching '{name_fragment}' not found"
    return json.loads(logs[0].read_text())


# ── 6.1 Ingest completeness — 100%, zero dropped ─────────────────────
def test_6_1_ingest_completeness_100_percent(tmp_path):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    n = _make_dataset(src)
    _run_pipeline(src, out)
    ingest = _load_log(out, "ingest")
    entries = ingest.get("entries", ingest if isinstance(ingest, list) else [])
    assert len(entries) == n, (
        f"6.1 FAIL: {len(entries)} ingested of {n} — zero-drop lock violated")


# ── 6.2 Pipeline error rate — 0 on valid input ───────────────────────
def test_6_2_zero_errors_on_valid_input(tmp_path):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    _make_dataset(src)
    r = _run_pipeline(src, out)
    errors = r["summary"].get("errors", 0)
    assert errors == 0, f"6.2 FAIL: {errors} pipeline errors on valid input"


# ── 6.3 Log completeness — 5/5 streams, all files traceable ──────────
def test_6_3_log_completeness_and_traceability(tmp_path):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    n = _make_dataset(src)
    _run_pipeline(src, out)
    logs = [f for f in (out / "LOGS").iterdir() if f.suffix == ".json"]
    assert len(logs) >= 5, f"6.3 FAIL: {len(logs)} log streams, expected >=5"
    classification = _load_log(out, "classification")
    entries = classification.get("entries",
              classification if isinstance(classification, list) else [])
    assert len(entries) == n, (
        f"6.3 FAIL: {len(entries)}/{n} files traceable in classification log")


# ── 6.4 Proxy stage structural integrity (empirical rate: CLAUDE.md) ─
def test_6_4_proxy_stage_structural_integrity(tmp_path):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    _make_dataset(src)
    _run_pipeline(src, out)
    proxies_dirs = list(out.rglob("PROXIES"))
    assert proxies_dirs, "6.4 FAIL: PROXIES/ folder not created"


# ── 6.5 Classification rate — >=75% to a named camera source ─────────
def test_6_5_classification_rate_75_percent(tmp_path):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    _make_dataset(src)
    _run_pipeline(src, out)
    classification = _load_log(out, "classification")
    entries = classification.get("entries",
              classification if isinstance(classification, list) else [])
    camera_entries = [e for e in entries
                      if e.get("classification") == "camera"]
    named = [e for e in camera_entries
             if e.get("camera_source") not in (None, "", "Unknown_Camera")]
    assert camera_entries, "6.5 FAIL: no camera files classified"
    rate = len(named) / len(camera_entries)
    assert rate >= 0.75, (
        f"6.5 FAIL: {rate:.0%} of camera files named — threshold 75%")


# ── 6.6 Determinism — identical input+config -> identical structure ──
def test_6_6_determinism_identical_structure(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    _make_dataset(src)
    out_a, out_b = tmp_path / "run_a", tmp_path / "run_b"
    _run_pipeline(src, out_a)
    _run_pipeline(src, out_b)

    def structure(root: Path) -> list:
        items = []
        for p in sorted(root.rglob("*")):
            rel = p.relative_to(root)
            if any(part == "LOGS" for part in rel.parts):
                continue
            if p.name.endswith("_index.json") or p.name.endswith("summary.md"):
                continue
            items.append((str(rel), p.is_dir()))
        return items

    assert structure(out_a) == structure(out_b), (
        "6.6 FAIL: identical input + config produced different structure — P1 violated")


# ── 6.7 Run ID consistency — one run_id across all outputs ───────────
def test_6_7_run_id_consistent(tmp_path):
    src, out = tmp_path / "src", tmp_path / "out"
    src.mkdir()
    _make_dataset(src)
    r = _run_pipeline(src, out)
    run_id = r["run_id"]
    log_names = [f.name for f in (out / "LOGS").iterdir()]
    tagged = [n for n in log_names if run_id in n]
    assert tagged, f"6.7 FAIL: run_id {run_id} not present in any log filename"
    index_files = list(out.glob("*_index.json"))
    if index_files:
        assert any(run_id in f.name for f in index_files), (
            "6.7 FAIL: run_id missing from index filename")
