"""
Camera Probe (scripts/probe_camera.py) — the discovery/onboarding tool.

Pins the pure fingerprint extractors (with injected exiftool/ffprobe text, no real
tools needed), the smarter label suggestion (canonical / brand+code / Unknown-brand),
the coverage verdict, and the paste-ready stubs. Boundaries: it FLAGS telemetry
streams, it does not decode them.
"""

import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import probe_camera as pc          # scripts/probe_camera.py
import camera_identity as ci


# ── structure ─────────────────────────────────────────────────────────────────
def test_sample_and_structure_from_card():
    with tempfile.TemporaryDirectory() as t:
        card = Path(t) / "CARD"
        (card / "DCIM").mkdir(parents=True)
        (card / "DCIM" / "DJI_20260625_0001.MP4").write_bytes(b"v")
        (card / "DCIM" / "DJI_20260625_0001.SRT").write_bytes(b"s")
        (card / "DCIM" / "._junk.MP4").write_bytes(b"x")
        files = pc.sample_files(card)
        assert [f.name for f in files] == ["DJI_20260625_0001.MP4", "DJI_20260625_0001.SRT"]
        s = pc.structure_signals(files, card)
        assert "mp4" in s["extensions"] and "DCIM" in s["card_markers"]
        assert "srt" in s["sidecars"]
        assert s["filename_regex"] == r"^DJI_\d+_\d+"


def test_time_signals_split_gps_vs_clock():
    text = "GPSDateTime : 2026:06:25 06:27:17Z\nCreateDate : 2026:06:25 06:27:17\n"
    t = pc.time_signals(text)
    assert t["drift_free"] == ["GPSDateTime"] and "CreateDate" in t["camera_clock"]


def test_stream_signals_flags_telemetry_not_decodes_it():
    ff = ("index=0\ncodec_type=video\ncodec_name=hevc\nwidth=3840\nheight=2160\navg_frame_rate=30/1\n"
          "index=1\ncodec_type=audio\ncodec_name=aac\n"
          "index=2\ncodec_type=data\ncodec_name=none\ntag:handler_name=DJI meta\n")
    st = pc.stream_signals(ff)
    assert st["video_codec"] == "hevc" and st["resolution"] == "3840x2160" and st["fps"] == 30.0
    assert st["telemetry"] and st["telemetry"][0]["hint"] in ("meta", "dvtm", "djmd")


# ── label suggestion (the three refinements) ─────────────────────────────────
def test_suggest_label_canonical_when_known():
    reg = ci.load_registry(path="/no/file")
    label, known = pc.suggest_label({"model_code": "AC006"}, "DJI", reg)
    assert label == "DJI Osmo Action 6" and known is True


def test_suggest_label_combines_brand_and_code_when_unknown():
    reg = ci.load_registry(path="/no/file")
    label, known = pc.suggest_label({"model_code": "AC999"}, "DJI", reg)
    assert label == "DJI AC999 - TODO confirm model" and known is False


def test_suggest_label_brand_only_defaults_to_unknown_brand():
    reg = ci.load_registry(path="/no/file")
    label, known = pc.suggest_label({}, "GoPro", reg)
    assert label == "Unknown GoPro - TODO confirm model" and known is False


def test_suggest_label_nothing_known():
    label, known = pc.suggest_label({}, None, ci.load_registry(path="/no/file"))
    assert label == "Unknown camera - TODO confirm make/model" and known is False


# ── end-to-end fingerprint (injected tools) ──────────────────────────────────
def _dji_exif(_p):
    return ("Category : pb_file:dvtm_ac206.proto;model_name:AC006;pb_version:2.0.1;\n"
            "CreateDate : 2026:06:25 06:27:17\n")


def _dji_ff(_p):
    return ("index=0\ncodec_type=video\ncodec_name=hevc\nwidth=3840\nheight=2160\navg_frame_rate=30/1\n"
            "index=2\ncodec_type=data\ncodec_name=none\ntag:handler_name=djmd\n")


def test_fingerprint_recognizes_known_camera():
    with tempfile.TemporaryDirectory() as t:
        card = Path(t) / "WEDDING"; (card / "DCIM").mkdir(parents=True)
        (card / "DCIM" / "DJI_20260625_0001.MP4").write_bytes(b"v")
        fp = pc.build_fingerprint(card, exif_runner=_dji_exif, ffprobe_runner=_dji_ff)
        assert fp["identity"]["model_code"] == "AC006"
        assert fp["suggested_label"] == "DJI Osmo Action 6" and fp["already_known"] is True
        assert fp["coverage"]["in_registry"] is True
        assert fp["streams"]["telemetry"]            # djmd flagged
        assert "Already recognized" in pc.render_report(fp)


def test_fingerprint_unknown_camera_yields_stub_and_gaps():
    with tempfile.TemporaryDirectory() as t:
        card = Path(t) / "NEWCAM"; (card / "DCIM").mkdir(parents=True)
        (card / "DCIM" / "ZED0001.MP4").write_bytes(b"v")
        exif = lambda p: "Serial Number : ZED-777\nModel : ZedCam Pro\nMake : ZedCorp\n"
        fp = pc.build_fingerprint(card, exif_runner=exif, ffprobe_runner=lambda p: "")
        assert fp["already_known"] is False
        assert fp["brand"] == "ZedCorp"                              # from Make tag fallback
        assert fp["suggested_label"] == "ZedCorp ZedCam Pro - TODO confirm model"
        stub = pc.cameras_yaml_stub(fp)
        assert "serial: ZED-777" in stub and "label: ZedCorp ZedCam Pro" in stub
        assert any("cameras.yaml" in g for g in fp["coverage"]["gaps"])
        assert pc.family_pattern_line(fp).startswith('(re.compile(r"^ZED')


def test_add_to_cameras_yaml_is_optin_and_skips_known():
    with tempfile.TemporaryDirectory() as t:
        yml = Path(t) / "cameras.yaml"; yml.write_text("cameras:\n")
        unknown_fp = {"already_known": False, "brand": "ZedCorp", "suggested_label": "ZedCorp X",
                      "identity": {"serial": "ZED-777"}}
        p = pc.add_to_cameras_yaml(unknown_fp, path=yml)
        assert p == yml and "ZED-777" in yml.read_text()
        known_fp = {"already_known": True, "brand": "DJI", "suggested_label": "DJI Osmo Action 6",
                    "identity": {}}
        assert pc.add_to_cameras_yaml(known_fp, path=yml) is None      # nothing to add
