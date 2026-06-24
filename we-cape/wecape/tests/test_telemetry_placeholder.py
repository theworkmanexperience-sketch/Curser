"""
Locks the DJI telemetry placeholder contract (deferred future enhancement).

_extract_dji_telemetry must stay a safe no-op until real .SRT parsing lands, and
must not perturb the validated timestamp fallback chain / grouping.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.capture.timestamp import TimestampExtractor


def test_dji_telemetry_is_noop_placeholder(tmp_path):
    f = tmp_path / "DJI_0001.MP4"
    f.write_bytes(b"\x00")
    ts, method = TimestampExtractor()._extract_dji_telemetry(f)
    assert ts is None and method is None


def test_extract_chain_still_uses_filename(tmp_path):
    f = tmp_path / "20260519_120000_clip.MP4"
    f.write_bytes(b"\x00")
    r = TimestampExtractor().extract(f, "DJI")
    assert r.method == "filename"
    assert r.fallback_level == 0
