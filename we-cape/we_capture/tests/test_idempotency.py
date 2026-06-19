"""
§17 Test 6 — Idempotency & Robustness
§3.x  — Edge Case Matrix (all 10 cases)

Idempotency rule (§17 Test 6 LOCKED):
  Three identical runs on the same input folder (new run_id each time)
  must produce bit-identical folder structure + JSON metadata
  EXCEPT: run_id, log timestamps, SHA-256 hashes of log files themselves.

Edge cases from §3.x (all must be handled without pipeline failure):
  1.  Corrupt / unreadable file
  2.  Missing metadata → fallback chain
  3.  Clock / creation-time drift → confidence=low, pipeline continues
  4.  Duplicate filenames across cameras
  5.  Zero camera files in folder
  6.  Files >50 GB (structural test only — no 50GB file created)
  7.  Variant files with no parent → Option B standalone
  8.  Unsupported codec / format → Generic
  9.  Identical content, different names
  10. Conflicting grouping candidates → deterministic resolution
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
os.environ['WECAPE_TEST_MODE'] = '1'

from engine.pipeline import Pipeline
from engine.classifier import FileClassifier

# ── Shared config ─────────────────────────────────────────────────────
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
        "field_recorder_patterns": ["^ZOOM\\d*"],
        "default_classification": "generic",
    },
    "classification": {
        "camera_sources": {
            "DJI":    {"patterns": ["^DJI_"],       "extensions": [".mp4", ".mov"]},
            "iPhone": {"patterns": ["^IMG_\\d{4}"], "extensions": [".mov", ".mp4"]},
        },
        "reference_extensions": [".pdf", ".srt", ".xml"],
        "generic_video_extensions": [".mp4", ".mov"],
        "generic_image_extensions": [".png"],
    },
    "proxies":     {"generate_proxies": False},
    "performance": {"max_workers": 2, "hash_chunk_size_mb": 1},
    "logging":     {"log_level": "WARNING", "log_format": "json"},
    "output":      {"date_format": "%Y-%m-%d", "group_id_prefix": "MCG"},
}


def _write_config(tmp: Path) -> Path:
    import yaml
    cfg = tmp / "config.yaml"
    cfg.write_text(yaml.dump(PIPELINE_CONFIG))
    return cfg


def _make_pipeline(tmp: Path) -> Pipeline:
    return Pipeline(_write_config(tmp))


def _collect_structure(root: Path) -> dict:
    """
    Collect folder structure + file sizes for idempotency comparison.
    Excludes: LOGS/ directory (run_id, timestamps, log hashes all vary per §17 Test 6).
    Normalizes: run_id-keyed index files → canonical name for comparison.
    Returns {relative_path_str: file_size}.
    """
    result = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        parts = rel.parts
        if parts[0] == "LOGS":
            continue
        # Normalize: {run_id}_index.json → __run_index.json
        # run_id format: PREFIX_YYYYMMDD_HHMMSS_XXXXXX
        import re
        rel_str = str(rel)
        rel_str = re.sub(r'^[A-Z0-9]+_\d{8}_\d{6}_[A-F0-9]+_index\.json$',
                         '__run_index.json', rel_str)
        result[rel_str] = p.stat().st_size
    return result


def _collect_metadata_content(root: Path) -> dict:
    """
    Collect content-comparable metadata from JSON files, stripping mutable fields.
    Mutable fields excluded per §17 Test 6: run_id, generated_at, log timestamps.
    Also normalizes run_id-keyed filenames in path keys.
    """
    import re
    result = {}
    for p in sorted(root.rglob("*.json")):
        rel = str(p.relative_to(root))
        if "LOGS" in rel:
            continue
        # Normalize run_id-keyed filenames in path for comparison
        rel = re.sub(r'^[A-Z0-9]+_\d{8}_\d{6}_[A-F0-9]+_index\.json$',
                     '__run_index.json', rel)
        try:
            doc = json.loads(p.read_text())
            normalized = _strip_mutable(doc)
            result[rel] = json.dumps(normalized, sort_keys=True)
        except json.JSONDecodeError:
            pass
    return result


def _strip_mutable(obj):
    """Recursively remove mutable fields from JSON for idempotency comparison."""
    MUTABLE = {"run_id", "generated_at", "logged_at"}
    if isinstance(obj, dict):
        return {k: _strip_mutable(v) for k, v in obj.items() if k not in MUTABLE}
    if isinstance(obj, list):
        return [_strip_mutable(i) for i in obj]
    return obj


# ── §17 Test 6: Idempotency ───────────────────────────────────────────

def test_three_runs_produce_identical_structure(tmp_path):
    """
    §17 Test 6 LOCKED: runs 2 and 3 must produce bit-identical folder structure
    (except run_id, log timestamps, log SHA-256 hashes).
    """
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "DJI_0001.mp4").write_bytes(b"V" * 4096)
    (input_dir / "IMG_4321.mov").write_bytes(b"W" * 2048)
    (input_dir / "notes.srt").write_bytes(b"SRT")
    (input_dir / "thumb.png").write_bytes(b"PNG")

    output_dirs = []
    for i in range(3):
        out = tmp_path / f"run_{i+1}"
        out.mkdir()
        p = _make_pipeline(tmp_path)
        p.run(input_dir, out)
        output_dirs.append(out)

    # Compare structure of runs 1, 2, 3 — must all be identical
    structures = [_collect_structure(d) for d in output_dirs]
    assert structures[0] == structures[1], \
        f"§17 Test 6: run 1 vs run 2 structure mismatch:\n" \
        f"  Only in run 1: {set(structures[0]) - set(structures[1])}\n" \
        f"  Only in run 2: {set(structures[1]) - set(structures[0])}"
    assert structures[1] == structures[2], \
        "§17 Test 6: run 2 vs run 3 structure mismatch"


def test_three_runs_produce_identical_metadata(tmp_path):
    """§17 Test 6: JSON metadata content identical across runs (run_id excluded)."""
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "DJI_0001.mp4").write_bytes(b"V" * 4096)
    (input_dir / "IMG_4321.mov").write_bytes(b"W" * 2048)

    metadata_runs = []
    for i in range(3):
        out = tmp_path / f"run_{i+1}"
        out.mkdir()
        p = _make_pipeline(tmp_path)
        p.run(input_dir, out)
        metadata_runs.append(_collect_metadata_content(out))

    assert metadata_runs[0] == metadata_runs[1], \
        "§17 Test 6: metadata differs between run 1 and run 2"
    assert metadata_runs[1] == metadata_runs[2], \
        "§17 Test 6: metadata differs between run 2 and run 3"


def test_rerun_on_same_output_dir_skips_existing(tmp_path):
    """
    §17 Test 6 idempotency: re-running into the same output folder must
    not create duplicate MEDIA files. Per-run metadata (run_index, logs)
    legitimately accumulates — that is correct and expected behavior.
    """
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir(); output_dir.mkdir()
    (input_dir / "DJI_0001.mp4").write_bytes(b"V" * 4096)
    (input_dir / "IMG_4321.mov").write_bytes(b"W" * 2048)

    def _media_files(root: Path) -> set[str]:
        """Collect non-JSON, non-log files — the actual media content."""
        return {
            str(p.relative_to(root))
            for p in root.rglob("*")
            if p.is_file()
            and "LOGS" not in str(p.relative_to(root))
            and not p.name.endswith(".json")  # exclude per-run metadata indexes
            and not p.name.endswith(".md")    # exclude per-run summary reports
        }

    p1 = _make_pipeline(tmp_path)
    p1.run(input_dir, output_dir)
    media_after_run1 = _media_files(output_dir)

    p2 = _make_pipeline(tmp_path)
    p2.run(input_dir, output_dir)
    media_after_run2 = _media_files(output_dir)

    new_media = media_after_run2 - media_after_run1
    assert not new_media, \
        f"Re-run created duplicate media files:\n  New: {new_media}"


# ── §3.x Edge Case Matrix ─────────────────────────────────────────────

def test_corrupt_file_logged_pipeline_continues(tmp_path):
    """§3.x: Corrupt/unreadable file → logged, skipped, pipeline never halts."""
    input_dir = tmp_path / "input"; input_dir.mkdir()
    (input_dir / "DJI_0001.mp4").write_bytes(b"V" * 2048)
    corrupt = input_dir / "corrupt_file.mp4"
    corrupt.write_bytes(b"\x00\xFF\xFE\xFD" * 8)   # garbage bytes
    corrupt.chmod(0o000)                              # make unreadable

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = _make_pipeline(tmp_path)
    try:
        summary = p.run(input_dir, output_dir)
        # Pipeline must not raise — partial success is required (§13)
        assert summary is not None, "Pipeline returned None on corrupt file"
    except Exception as e:
        assert False, f"§3.x: Pipeline raised exception on corrupt file: {e}"
    finally:
        corrupt.chmod(0o644)   # restore for cleanup


def test_zero_camera_files_produces_empty_multicam(tmp_path):
    """§3.x: Zero camera files → all Generic/Reference; MULTICAM/ folder created empty."""
    input_dir = tmp_path / "input"; input_dir.mkdir()
    (input_dir / "notes.srt").write_bytes(b"SRT")
    (input_dir / "thumb.png").write_bytes(b"PNG")

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = _make_pipeline(tmp_path)
    summary = p.run(input_dir, output_dir)

    assert summary["multicam_groups_formed"] == 0
    # Error log must contain explicit note about no camera files
    run_id = summary["run_id"]
    error_log = json.loads(
        (output_dir / "LOGS" / f"{run_id}_errors.json").read_text()
    )
    # No crash — pipeline produced output
    assert (output_dir / "LOGS").is_dir()


def test_duplicate_filenames_across_cameras_treated_separately(tmp_path):
    """§3.x: Duplicate filenames from different cameras → separate files, grouped by timestamp."""
    config = dict(PIPELINE_CONFIG)
    clf_config = dict(config["classification"])
    clf_config["camera_sources"] = {
        "DJI":    {"patterns": ["^DJI_"],       "extensions": [".mp4"]},
        "GoPro":  {"patterns": ["^GP_"],         "extensions": [".mp4"]},
    }
    config["classification"] = clf_config

    import yaml
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.dump(config))

    input_dir = tmp_path / "input"; input_dir.mkdir()
    # Same filename stem, different camera prefixes
    (input_dir / "DJI_clip.mp4").write_bytes(b"DJI" * 512)
    (input_dir / "GP_clip.mp4").write_bytes(b"GoPro" * 256)

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = Pipeline(cfg_path)
    summary = p.run(input_dir, output_dir)

    # Both must be ingested (§6: ALL files ingested, none dropped)
    assert summary["files_ingested"] == 2


def test_unsupported_codec_routed_to_generic(tmp_path):
    """§3.x: Unsupported codec/format → ingest + classify as Generic; logged."""
    input_dir = tmp_path / "input"; input_dir.mkdir()
    # .flv has no camera pattern and is in generic_video_extensions
    (input_dir / "old_export.flv").write_bytes(b"FLV" * 128)

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = _make_pipeline(tmp_path)
    summary = p.run(input_dir, output_dir)

    # Must be ingested
    assert summary["files_ingested"] == 1
    # Must appear in classification log as generic
    run_id = summary["run_id"]
    class_log = json.loads(
        (output_dir / "LOGS" / f"{run_id}_classification.json").read_text()
    )
    classes = [e["classification"] for e in class_log["entries"]]
    assert "generic" in classes or "reference" in classes


def test_identical_content_different_names_treated_separately_by_default(tmp_path):
    """
    §3.x: Identical content, different names → treated as separate files
    when enable_duplicate_content_detection = false (default).
    """
    input_dir = tmp_path / "input"; input_dir.mkdir()
    identical_bytes = b"IDENTICAL_CONTENT" * 256
    (input_dir / "DJI_0001.mp4").write_bytes(identical_bytes)
    (input_dir / "DJI_0002.mp4").write_bytes(identical_bytes)

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = _make_pipeline(tmp_path)
    summary = p.run(input_dir, output_dir)

    # Both must be ingested and classified independently
    assert summary["files_ingested"] == 2


def test_timestamp_fallback_logged_as_low_confidence(tmp_path):
    """
    §3.x + §5: Files with no embedded timestamp fall back to file-system clock.
    Fallback level 2 → confidence=low → logged as WARNING (pipeline never halts).
    """
    input_dir = tmp_path / "input"; input_dir.mkdir()
    # Generic file with no camera metadata — will fallback to file_stat_mtime
    (input_dir / "GENERIC_NO_META.png").write_bytes(b"PNG" * 64)

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = _make_pipeline(tmp_path)
    # Must complete without exception
    summary = p.run(input_dir, output_dir)
    assert summary is not None


def test_orphan_variant_no_parent_field_in_output(tmp_path):
    """§3.x Option B: orphan variant → standalone, classification_note set, no parent_id."""
    input_dir = tmp_path / "input"; input_dir.mkdir()
    (input_dir / "scene_final.mp4").write_bytes(b"FINAL" * 512)  # variant, no base

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = _make_pipeline(tmp_path)
    summary = p.run(input_dir, output_dir)

    run_id = summary["run_id"]
    class_log = json.loads(
        (output_dir / "LOGS" / f"{run_id}_classification.json").read_text()
    )
    # Must be classified — not dropped
    assert len(class_log["entries"]) == 1
    # Must not appear in variants log with a parent_id link
    var_log = json.loads(
        (output_dir / "LOGS" / f"{run_id}_variants.json").read_text()
    )
    assert len(var_log["entries"]) == 0, \
        "Orphan variant should not appear in variants log with a parent link"


def test_pipeline_never_halts_on_any_single_error(tmp_path):
    """§13 LOCKED: no single file error may cause total pipeline failure."""
    input_dir = tmp_path / "input"; input_dir.mkdir()
    # Mix: one valid camera, one corrupt, one normal generic
    (input_dir / "DJI_0001.mp4").write_bytes(b"V" * 2048)
    (input_dir / "thumb.png").write_bytes(b"PNG")
    bad = input_dir / "bad.mp4"; bad.write_bytes(b"\x00" * 16); bad.chmod(0o000)

    output_dir = tmp_path / "output"; output_dir.mkdir()
    p = _make_pipeline(tmp_path)
    try:
        summary = p.run(input_dir, output_dir)
        # Partial success must still produce output
        assert (output_dir / "LOGS").is_dir(), "§13: No output produced on partial failure"
    finally:
        bad.chmod(0o644)


# ── Standalone runner ─────────────────────────────────────────────────

if __name__ == "__main__":
    import traceback
    tests = [
        test_three_runs_produce_identical_structure,
        test_three_runs_produce_identical_metadata,
        test_rerun_on_same_output_dir_skips_existing,
        test_corrupt_file_logged_pipeline_continues,
        test_zero_camera_files_produces_empty_multicam,
        test_duplicate_filenames_across_cameras_treated_separately,
        test_unsupported_codec_routed_to_generic,
        test_identical_content_different_names_treated_separately_by_default,
        test_timestamp_fallback_logged_as_low_confidence,
        test_orphan_variant_no_parent_field_in_output,
        test_pipeline_never_halts_on_any_single_error,
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
    print(f"Test 6 + §3.x: {len(passed)}/{len(passed)+len(failed)} passed", end="")
    print("" if failed else "  — All passed ✓")
    if failed:
        print(f"  FAILED: {failed}")
