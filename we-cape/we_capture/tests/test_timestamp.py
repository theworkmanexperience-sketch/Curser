"""
§5 Timestamp Fallback Chain + §3.x Clock Drift
Tests the three-level fallback chain, confidence flags, and per-camera offsets.
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.timestamp import TimestampExtractor, TimestampResult


def _make_file(name: str, tmp: Path, content: bytes = b"data") -> Path:
    f = tmp / name
    f.write_bytes(content)
    return f


# ── §5 Priority 0: Filename ───────────────────────────────────────────

def test_filename_with_timestamp_parsed_as_level_0(tmp_path):
    """Filename containing YYYYMMDD_HHMMSS → fallback_level=0, confidence=high."""
    extractor = TimestampExtractor()
    f = _make_file("DJI_20230615_143022_001.mp4", tmp_path)
    result = extractor.extract(f)
    assert result.fallback_level == 0
    assert result.confidence == "high"
    assert result.method == "filename"


def test_filename_without_timestamp_falls_through(tmp_path):
    """DJI_0001.mp4 (no date) → fallback_level ≥ 1."""
    extractor = TimestampExtractor()
    f = _make_file("DJI_0001.mp4", tmp_path)
    # ffprobe not available in test env → falls to file_stat
    result = extractor.extract(f)
    assert result.fallback_level >= 1


# ── §5 Priority 2: File stat (fallback level 2) ───────────────────────

def test_file_stat_fallback_produces_low_confidence(tmp_path):
    """
    §3.x + §5: When filename and metadata both fail,
    file-stat mtime is used → fallback_level=2, confidence=low.
    Pipeline continues. §5 fallback chain is NEVER bypassed.
    """
    extractor = TimestampExtractor()
    f = _make_file("no_metadata_file.png", tmp_path)
    # Force fallback by patching ffprobe to fail
    with patch("subprocess.run", side_effect=FileNotFoundError("ffprobe not found")):
        result = extractor.extract(f)
    assert result.fallback_level == 2
    assert result.confidence == "low"
    assert result.method == "file_stat_mtime"
    assert result.unix_timestamp > 0   # still a valid timestamp


def test_file_stat_never_raises(tmp_path):
    """§13: timestamp extraction must never raise — even for unreadable metadata."""
    extractor = TimestampExtractor()
    f = _make_file("mystery.mp4", tmp_path)
    with patch("subprocess.run", side_effect=Exception("any error")):
        result = extractor.extract(f)
    assert isinstance(result, TimestampResult)
    assert result.unix_timestamp is not None


# ── §3.x Per-camera offset ────────────────────────────────────────────

def test_per_camera_offset_applied(tmp_path):
    """
    §3.x clock drift: configurable per-camera offset must be added to timestamp.
    Offset is applied regardless of fallback level.
    """
    offsets = {"DJI": 30.0}   # DJI clock runs 30s fast
    extractor = TimestampExtractor(camera_offsets=offsets)
    f = _make_file("no_metadata_file.mp4", tmp_path)
    with patch("subprocess.run", side_effect=FileNotFoundError):
        result_without_offset = TimestampExtractor().extract(f)
        result_with_offset = extractor.extract(f, camera_source="DJI")
    delta = result_with_offset.unix_timestamp - result_without_offset.unix_timestamp
    assert abs(delta - 30.0) < 0.1, f"Expected +30s offset, got {delta:.2f}s"


def test_zero_offset_does_not_change_timestamp(tmp_path):
    extractor_no_offset = TimestampExtractor(camera_offsets={"DJI": 0})
    extractor_default   = TimestampExtractor()
    f = _make_file("clip.mp4", tmp_path)
    with patch("subprocess.run", side_effect=FileNotFoundError):
        r1 = extractor_no_offset.extract(f, "DJI")
        r2 = extractor_default.extract(f, "DJI")
    assert abs(r1.unix_timestamp - r2.unix_timestamp) < 0.1


def test_negative_offset_applied_correctly(tmp_path):
    """Negative offset (camera clock runs slow) must subtract correctly."""
    offsets = {"iPhone": -15.0}
    extractor = TimestampExtractor(camera_offsets=offsets)
    extractor_base = TimestampExtractor()
    f = _make_file("clip.mov", tmp_path)
    with patch("subprocess.run", side_effect=FileNotFoundError):
        r_base = extractor_base.extract(f, "iPhone")
        r_offset = extractor.extract(f, "iPhone")
    delta = r_offset.unix_timestamp - r_base.unix_timestamp
    assert abs(delta - (-15.0)) < 0.1


# ── Standalone runner ─────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    tests = [
        test_filename_with_timestamp_parsed_as_level_0,
        test_filename_without_timestamp_falls_through,
        test_file_stat_fallback_produces_low_confidence,
        test_file_stat_never_raises,
        test_per_camera_offset_applied,
        test_zero_offset_does_not_change_timestamp,
        test_negative_offset_applied_correctly,
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
    print(f"§5 Timestamp: {len(passed)}/{len(passed)+len(failed)} passed", end="")
    print("" if failed else "  — All passed ✓")
    if failed:
        print(f"  FAILED: {failed}")
