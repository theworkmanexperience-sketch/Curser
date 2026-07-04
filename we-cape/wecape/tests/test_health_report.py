"""
Production Health Report (scripts/health_report.py).

Pins the pure metrics (relative vs trusted skew, outlier discipline, projection)
and — critically — the honesty guardrails: no culprit named without a material
outlier, "likely" (not definitive) when relative, definitive only with a trusted
reference, and never a "% sync accuracy" number.
"""

import sqlite3
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import health_report as hr          # scripts/health_report.py

_MAR14 = "2026-03-14 09:30:%02d"      # base time template


def _clip(cam, sec, day="2026-03-14"):
    return {"camera": cam, "epoch": hr._epoch(f"{day} 09:30:{sec:02d}")}


def test_humanize_skew_scales():
    assert "year" in hr.humanize_skew(-8 * 31557600)
    assert hr.humanize_skew(0) == "in sync"
    assert hr.humanize_skew(3).endswith("ahead")


def _gross_outlier_clips():
    # Realistic: TWO cameras agree at 2026 and one camera's clock is stuck in 2018.
    # (With only two cameras disagreeing it's symmetric — no culprit can be named.)
    return [_clip("DJI Osmo 5", 10), _clip("DJI Osmo 6", 12),
            {"camera": "Insta360", "epoch": hr._epoch("2018-03-14 09:30:11")},
            {"camera": "Insta360", "epoch": hr._epoch("2018-03-14 09:30:14")}]


def test_relative_skew_flags_gross_outlier():
    r = hr.camera_skews(_gross_outlier_clips(), window=15)
    assert r["outlier"] == "Insta360"
    assert any(c["is_outlier"] for c in r["cameras"])


def test_two_cameras_disagreeing_names_no_culprit():
    # Honesty guardrail: two cameras, can't tell which is wrong → no accusation.
    clips = [{"camera": "DJI", "epoch": hr._epoch("2026-03-14 09:30:10")},
             {"camera": "Insta360", "epoch": hr._epoch("2018-03-14 09:30:10")}]
    assert hr.camera_skews(clips, window=15)["outlier"] is None


def test_small_drift_within_window_is_not_an_outlier():
    clips = [_clip("DJI", 10), _clip("Insta360", 13), _clip("iPhone", 11)]   # a few seconds
    r = hr.camera_skews(clips, window=15)
    assert r["outlier"] is None


def test_trusted_clock_sets_consensus():
    clips = [{"camera": "DJI", "epoch": hr._epoch("2026-03-14 09:30:10")},
             {"camera": "Insta360", "epoch": hr._epoch("2018-03-14 09:30:10")}]
    r = hr.camera_skews(clips, trusted_camera="DJI", window=15)
    dji = next(c for c in r["cameras"] if c["camera"] == "DJI")
    assert abs(dji["skew_s"]) < 1          # trusted camera is the zero point


def test_no_timestamps_is_handled():
    r = hr.camera_skews([{"camera": "DJI", "epoch": None}], window=15)
    assert r["no_timestamps"] and r["outlier"] is None


def test_projection_only_when_outlier():
    with_out = hr.camera_skews(_gross_outlier_clips(), window=15)
    assert hr.projected_improvement(with_out, 15) is not None
    healthy = hr.camera_skews([_clip("DJI", 10), _clip("Insta360", 12), _clip("iPhone", 11)], window=15)
    assert hr.projected_improvement(healthy, 15) is None


def test_render_never_prints_sync_accuracy():
    data = _synth_data(gross_outlier=True, trusted=None)
    md = hr.render_markdown(data)
    assert "sync accuracy" not in md.lower() and "% sync" not in md.lower()
    assert "0 files lost" in md.lower()


def test_render_relative_says_likely_not_definitive():
    md = hr.render_markdown(_synth_data(gross_outlier=True, trusted=None))
    assert "likely culprit" in md.lower()          # hedged
    assert "reference: **relative" in md.lower()


def test_render_with_trusted_names_culprit_definitively():
    md = hr.render_markdown(_synth_data(gross_outlier=True, trusted="DJI Osmo 6"))
    assert "culprit:" in md.lower() and "likely culprit" not in md.lower()


# ── helper: build report data without a registry, via the pure path ──────────
def _synth_data(gross_outlier, trusted):
    clips = _gross_outlier_clips() if gross_outlier else \
        [_clip("DJI Osmo 5", 10), _clip("DJI Osmo 6", 12), _clip("Insta360", 11)]
    skew = hr.camera_skews(clips, trusted_camera=trusted, window=15)
    return {"run_id": "WEF_TEST", "run": {},
            "summary": hr.grouping_health(4, 3, 1, 0),
            "skew": skew, "window_used": 15,
            "ground_truth": ("manifest" if trusted else None), "trusted": trusted,
            "projection": hr.projected_improvement(skew, 15), "have_times": 4, "total_clips": 4}


def test_build_report_data_from_registry():
    with tempfile.TemporaryDirectory() as t:
        db = Path(t) / "reg.db"
        con = sqlite3.connect(str(db))
        con.execute("CREATE TABLE runs(id TEXT, output_path TEXT)")
        con.execute("CREATE TABLE content(id TEXT, run_id TEXT, camera_family TEXT, "
                    "corrected_timestamp TEXT, content_type TEXT)")
        con.execute("INSERT INTO runs VALUES('WEF_X', ?)", (t,))
        rows = [("s1", "WEF_X", "DJI Osmo 6", "2026-03-14 09:30:10", "original"),
                ("s2", "WEF_X", "iPhone", "2026-03-14 09:30:12", "original"),
                ("s3", "WEF_X", "Insta360", "2018-03-14 09:30:11", "original"),
                ("s4", "WEF_X", "Insta360", "2018-03-14 09:30:13", "original")]
        con.executemany("INSERT INTO content VALUES(?,?,?,?,?)", rows)
        con.commit(); con.close()

        data = hr.build_report_data(str(db), "WEF_X", telemetry="/no/telemetry")
        assert data is not None and data["skew"]["outlier"] == "Insta360"
        md = hr.render_markdown(data)
        assert "Insta360" in md and "0 files lost" in md.lower()
