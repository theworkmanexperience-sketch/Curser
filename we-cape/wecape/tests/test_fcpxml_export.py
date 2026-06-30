"""
FCPXML export bridge (scripts/fcpxml_export.py).

Validates the emitted FCPXML *structure* with a mocked ffprobe (no real media):
one <mc-clip> per group, one <mc-angle> per camera, asset-clip offsets normalized
to the group's earliest clip, original+proxy media-reps, resource-ref integrity,
frame-conformed time tokens, and XML well-formedness. Frame-accurate behaviour and
FCP acceptance are validated by importing into FCP — out of scope for a unit test.
"""

import re
import sys
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import fcpxml_export as fx          # scripts/fcpxml_export.py

TIME_RE = re.compile(r"^(-?\d+/\d+s|-?\d+s|0s)$")


def fake_probe(fps=(30, 1), w=3840, h=2160, dur=10.0, audio=True):
    def p(_path):
        return {"width": w, "height": h, "fps_num": fps[0], "fps_den": fps[1],
                "duration_s": dur, "has_video": True, "has_audio": audio,
                "audio_channels": 2, "audio_rate": 48000}
    return p


def make_groups():
    return [
        {"group_id": "G001", "files": [
            {"file_hash_sha256": "sha_a", "path": "/src/DJI ACTION 6/DJI_0001.MP4",
             "camera_source": "DJI Osmo Action 6", "timestamp_delta_seconds": 5.0},
            {"file_hash_sha256": "sha_b", "path": "/src/DJI ACTION 5/DJI_0002.MP4",
             "camera_source": "DJI Osmo Action 5", "timestamp_delta_seconds": 0.0},
            {"file_hash_sha256": "sha_c", "path": "/src/Insta360 X5/VID_0003.mp4",
             "camera_source": "Insta360 X5", "timestamp_delta_seconds": 2.0}]},
        {"group_id": "G002", "files": [
            {"file_hash_sha256": "sha_d", "path": "/src/DJI ACTION 6/DJI_0009.MP4",
             "camera_source": "DJI Osmo Action 6", "timestamp_delta_seconds": 0.0},
            {"file_hash_sha256": "sha_e", "path": "/src/Insta360 X5/VID_0010.mp4",
             "camera_source": "Insta360 X5", "timestamp_delta_seconds": 1.0}]},
    ]


def make_index():
    # sha_c deliberately has NO proxy -> tests original-only fallback in "both" mode.
    return {
        "sha_a": {"proxy_path": "/out/DJI_0001_proxy.mov", "original_path": "/src/DJI ACTION 6/DJI_0001.MP4",
                  "resolution": "3840x2160", "duration_sec": 10.0},
        "sha_b": {"proxy_path": "/out/DJI_0002_proxy.mov", "original_path": "/src/DJI ACTION 5/DJI_0002.MP4",
                  "resolution": "3840x2160", "duration_sec": 10.0},
        "sha_c": {"proxy_path": None, "original_path": "/src/Insta360 X5/VID_0003.mp4",
                  "resolution": "3840x2160", "duration_sec": 10.0},
        "sha_d": {"proxy_path": "/out/DJI_0009_proxy.mov", "original_path": "/src/DJI ACTION 6/DJI_0009.MP4",
                  "resolution": "3840x2160", "duration_sec": 10.0},
        "sha_e": {"proxy_path": "/out/VID_0010_proxy.mov", "original_path": "/src/Insta360 X5/VID_0010.mp4",
                  "resolution": "3840x2160", "duration_sec": 10.0},
    }


def _root(xml):
    """Parse for structural queries (strip prolog + DOCTYPE for ElementTree)."""
    body = "\n".join(l for l in xml.splitlines()
                     if not l.lstrip().startswith(("<?xml", "<!DOCTYPE")))
    return ET.fromstring(body)


def _build(media_mode="both", **kw):
    return fx.build_fcpxml("O-SIX Community Service", make_groups(), make_index(),
                           probe=fake_probe(**kw), media_mode=media_mode)


# ── well-formedness ─────────────────────────────────────────────────────────
def test_xml_is_well_formed_including_doctype():
    xml, _ = _build()
    minidom.parseString(xml)              # raises if malformed
    assert xml.startswith("<?xml")
    assert "<!DOCTYPE fcpxml>" in xml
    assert 'version="1.9"' in xml


# ── multicam structure ──────────────────────────────────────────────────────
def test_one_mc_clip_per_group():
    xml, stats = _build()
    root = _root(xml)
    assert len(root.findall(".//mc-clip")) == 2
    assert stats["groups"] == 2


def test_one_angle_per_camera():
    xml, _ = _build()
    root = _root(xml)
    medias = root.findall(".//media")
    # G001 has 3 cameras, G002 has 2.
    angle_counts = sorted(len(m.findall(".//mc-angle")) for m in medias)
    assert angle_counts == [2, 3]


def test_offsets_normalized_to_earliest_clip():
    xml, _ = _build()
    root = _root(xml)
    # Find G001's media; its earliest clip (delta 0 -> "0s") must exist, and the
    # Insta360 clip (delta 2) must be offset 2s (60 frames @30 -> reduced "2s").
    offsets = [ac.get("offset") for ac in root.findall(".//asset-clip")]
    assert "0s" in offsets
    assert "2s" in offsets and "5s" in offsets        # G001 deltas 0,2,5 normalized


def test_all_times_are_conformed_tokens():
    xml, _ = _build(fps=(30000, 1001))                # 29.97 -> rational times
    root = _root(xml)
    for ac in root.findall(".//asset-clip"):
        assert TIME_RE.match(ac.get("offset")), ac.get("offset")
        assert TIME_RE.match(ac.get("duration")), ac.get("duration")


# ── media references (FCP proxy workflow) ───────────────────────────────────
def test_both_mode_emits_original_and_proxy_reps():
    xml, _ = _build(media_mode="both") if False else _build()
    root = _root(xml)
    kinds = [mr.get("kind") for mr in root.findall(".//media-rep")]
    # 5 assets all have originals; 4 have proxies (sha_c has none).
    assert kinds.count("original-media") == 5
    assert kinds.count("proxy-media") == 4


def test_proxies_mode_falls_back_to_original_when_no_proxy():
    xml, _ = fx.build_fcpxml("S", make_groups(), make_index(),
                             probe=fake_probe(), media_mode="proxies")
    root = _root(xml)
    kinds = [mr.get("kind") for mr in root.findall(".//media-rep")]
    assert kinds.count("proxy-media") == 4
    assert kinds.count("original-media") == 1         # sha_c fallback


def test_proxy_src_is_file_uri_with_encoded_spaces():
    xml, _ = _build()
    assert "file:///out/DJI_0001_proxy.mov" in xml
    assert "%20" in xml                               # "/src/DJI ACTION 6/..." encoded


# ── resource integrity ──────────────────────────────────────────────────────
def test_every_ref_resolves_to_a_resource_id():
    xml, _ = _build()
    root = _root(xml)
    ids = {e.get("id") for e in root.iter() if e.get("id")}
    refs = {e.get("ref") for e in root.iter() if e.get("ref")}
    fmts = {e.get("format") for e in root.iter() if e.get("format")}
    assert refs and refs <= ids, (refs - ids)
    assert fmts and fmts <= ids, (fmts - ids)


def test_assets_deduped_by_sha():
    # 5 distinct SHAs across the two groups -> 5 assets, no duplicates.
    xml, stats = _build()
    root = _root(xml)
    assert stats["assets"] == 5
    assert len(root.findall(".//asset")) == 5


# ── robustness ──────────────────────────────────────────────────────────────
def test_fallback_to_registry_metadata_when_probe_fails():
    xml, stats = fx.build_fcpxml("S", make_groups(), make_index(),
                                 probe=lambda p: None)   # ffprobe unavailable
    assert stats["fallback"] == 5
    root = _root(xml)
    assert len(root.findall(".//mc-clip")) == 2          # still builds
    # registry resolution 3840x2160 used for the format
    assert any(f.get("width") == "3840" for f in root.findall(".//format"))


def test_xml_escaping_in_camera_names():
    groups = [{"group_id": "G&1", "files": [
        {"file_hash_sha256": "s1", "path": "/src/A/x.mp4", "camera_source": "A & B <cam>",
         "timestamp_delta_seconds": 0.0},
        {"file_hash_sha256": "s2", "path": "/src/B/y.mp4", "camera_source": "C",
         "timestamp_delta_seconds": 0.0}]}]
    idx = {"s1": {"proxy_path": None, "resolution": "1920x1080", "duration_sec": 5.0},
           "s2": {"proxy_path": None, "resolution": "1920x1080", "duration_sec": 5.0}}
    xml, _ = fx.build_fcpxml("Ev", groups, idx, probe=fake_probe())
    assert "A &amp; B &lt;cam&gt;" in xml
    assert "A & B <cam>" not in xml
    minidom.parseString(xml)                              # still well-formed


def test_empty_groups_still_valid_xml():
    xml, stats = fx.build_fcpxml("Ev", [], {}, probe=fake_probe())
    minidom.parseString(xml)
    assert stats["groups"] == 0
