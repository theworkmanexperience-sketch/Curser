"""
.SRT sidecar telemetry (scripts/srt_telemetry.py).

Pins the tolerant parser (labeled GPS, time-only, malformed, multi-block,
out-of-range) and the scan→store→link path with a synthetic clip + sidecar.
"""

import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import srt_telemetry as st          # scripts/srt_telemetry.py

_GPS_BLOCK = """1
00:00:00,000 --> 00:00:00,033
<font size="28">FrameCnt: 1, DiffTime: 33ms
2026-03-14 09:30:40.123
[iso: 100] [shutter: 1/500] [latitude: 33.123456] [longitude: -84.123456] [rel_alt: 1.2 abs_alt: 250.5]</font>

2
00:00:00,033 --> 00:00:00,066
<font size="28">FrameCnt: 2, DiffTime: 33ms
2026-03-14 09:30:41.156
[iso: 100] [shutter: 1/500] [latitude: 33.123460] [longitude: -84.123450] [rel_alt: 1.2 abs_alt: 250.6]</font>
"""

_TIME_ONLY_BLOCK = """1
00:00:00,000 --> 00:00:00,033
2026-03-14 09:30:40
FrameCnt: 1
"""


def test_parse_gps_and_time():
    d = st.parse_srt(_GPS_BLOCK)
    assert d["start_time"] == "2026-03-14T09:30:40"
    assert d["end_time"] == "2026-03-14T09:30:41"      # last block
    assert round(d["gps_lat"], 4) == 33.1235 and round(d["gps_lon"], 4) == -84.1235
    assert d["gps_alt"] == 250.5 and d["sample_count"] == 2


def test_parse_time_only_no_gps():
    d = st.parse_srt(_TIME_ONLY_BLOCK)
    assert d["start_time"] == "2026-03-14T09:30:40"    # time survives
    assert d["gps_lat"] is None and d["gps_lon"] is None
    assert d["sample_count"] == 1


def test_parse_malformed_never_crashes():
    d = st.parse_srt("this is not an SRT at all\n[latitude: nope]")
    assert d["start_time"] is None and d["gps_lat"] is None and d["sample_count"] == 0


def test_parse_rejects_impossible_gps():
    d = st.parse_srt("2026-03-14 09:30:40\n[latitude: 999.0] [longitude: -84.1]")
    assert d["gps_lat"] is None and d["gps_lon"] is None    # 999° latitude rejected


def test_parse_paren_gps_order_lon_lat():
    # DJI paren form GPS(lon,lat,alt) — documented assumed order
    d = st.parse_srt("2026-03-14 09:30:40\nGPS(-84.5,33.5,120)")
    assert round(d["gps_lat"], 1) == 33.5 and round(d["gps_lon"], 1) == -84.5


def test_scan_links_to_clip_sha_and_stores():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        (d / "VID_0001.MP4").write_bytes(b"video-bytes-here")     # the clip
        (d / "VID_0001.SRT").write_text(_GPS_BLOCK)               # its sidecar
        db = d / "telemetry.db"
        r = st.scan([str(d)], db=str(db), registry="/no/registry", hash_video=True)
        assert r["srt_files"] == 1 and r["linked_to_clip"] == 1 and r["with_gps"] == 1

        expect_sha = st.sha256_file(d / "VID_0001.MP4")
        rows = st._fetch(str(db), "WHERE content_sha=?", (expect_sha,))
        assert len(rows) == 1
        assert rows[0]["gps_lat"] is not None and rows[0]["start_time"] == "2026-03-14T09:30:40"


def test_scan_time_only_sidecar_stores_without_gps():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        (d / "clip.mov").write_bytes(b"x")
        (d / "clip.srt").write_text(_TIME_ONLY_BLOCK)
        db = d / "telemetry.db"
        r = st.scan([str(d)], db=str(db), registry="/no/registry")
        assert r["srt_files"] == 1 and r["with_gps"] == 0
        rows = st._fetch(str(db), "", ())
        assert rows[0]["start_time"] == "2026-03-14T09:30:40" and rows[0]["gps_lat"] is None


_CAPTION_SRT = """1
00:00:00,900 --> 00:00:01,633
hey we bikers

2
00:00:01,633 --> 00:00:02,666
welcome to part three
"""


def test_scan_skips_caption_srt_not_telemetry():
    # Real-world case: a spoken-word caption .SRT has SRT timecodes but no
    # camera datetime — it MUST be skipped, not stored as an empty telemetry row.
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        (d / "0413.mp4").write_bytes(b"v")
        (d / "0413.srt").write_text(_CAPTION_SRT)
        db = d / "telemetry.db"
        r = st.scan([str(d)], db=str(db), registry="/no/registry")
        assert r["srt_files"] == 0 and r["skipped_non_telemetry"] == 1
        assert st._fetch(str(db), "", ()) == []          # nothing stored


def test_scan_is_idempotent():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        (d / "a.mp4").write_bytes(b"aa")
        (d / "a.srt").write_text(_GPS_BLOCK)
        db = d / "telemetry.db"
        st.scan([str(d)], db=str(db), registry="/no/registry")
        st.scan([str(d)], db=str(db), registry="/no/registry")     # re-scan
        rows = st._fetch(str(db), "", ())
        assert len(rows) == 1                                       # updated, not duplicated
