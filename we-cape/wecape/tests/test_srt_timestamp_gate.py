"""
.SRT sidecar timestamp source — gate + parsing tests.

Covers the four required cases:
  1. Gate ON  + sidecar present   -> SRT timestamp used (level 0, high)
  2. Gate ON  + sidecar absent    -> falls through to existing chain
  3. Gate ON  + sidecar malformed -> falls through, never raises
  4. Gate OFF + sidecar present   -> SRT ignored (baseline preserved)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import os
os.environ['WECAPE_TEST_MODE'] = '1'

from wecape.capture.timestamp import TimestampExtractor

SRT_CONTENT = """1
00:00:00,000 --> 00:00:01,000
2026-03-14 07:23:47
latitude: 30.123456 longitude: -97.654321

2
00:00:01,000 --> 00:00:02,000
2026-03-14 07:23:48
"""


def _clip_with_sidecar(tmp_path, srt_text=SRT_CONTENT):
    clip = tmp_path / "DJI_20260314072347_0001_D.mp4"
    clip.write_bytes(b"FAKE_VIDEO" * 100)
    sidecar = tmp_path / "DJI_20260314072347_0001_D.SRT"
    sidecar.write_text(srt_text)
    return clip


def test_gate_on_sidecar_present_uses_srt(tmp_path):
    clip = _clip_with_sidecar(tmp_path)
    ext = TimestampExtractor(enable_srt_telemetry=True)
    result = ext.extract(clip)
    assert result.method == 'dji_srt_sidecar'
    assert result.fallback_level == 0
    assert result.confidence == 'high'
    # 2026-03-14 07:23:47 local -> verify components round-trip
    from datetime import datetime
    dt = datetime.fromtimestamp(result.unix_timestamp)
    assert (dt.year, dt.month, dt.day) == (2026, 3, 14)
    assert (dt.hour, dt.minute, dt.second) == (7, 23, 47)


def test_gate_on_sidecar_absent_falls_through(tmp_path):
    clip = tmp_path / "DJI_20260314072347_0001_D.mp4"
    clip.write_bytes(b"FAKE_VIDEO" * 100)
    ext = TimestampExtractor(enable_srt_telemetry=True)
    result = ext.extract(clip)
    # No sidecar -> existing chain: filename pattern wins here
    assert result.method != 'dji_srt_sidecar'
    assert result.unix_timestamp > 0


def test_gate_on_sidecar_malformed_falls_through(tmp_path):
    clip = _clip_with_sidecar(tmp_path, srt_text="garbage with no datetime here")
    ext = TimestampExtractor(enable_srt_telemetry=True)
    result = ext.extract(clip)
    assert result.method != 'dji_srt_sidecar'
    assert result.unix_timestamp > 0  # never raises, chain continues


def test_gate_off_sidecar_present_ignored(tmp_path):
    clip = _clip_with_sidecar(tmp_path)
    ext_off = TimestampExtractor(enable_srt_telemetry=False)
    ext_default = TimestampExtractor()
    r_off = ext_off.extract(clip)
    r_default = ext_default.extract(clip)
    # Baseline preserved: SRT never consulted
    assert r_off.method != 'dji_srt_sidecar'
    assert r_default.method != 'dji_srt_sidecar'
    assert r_off.method == r_default.method
