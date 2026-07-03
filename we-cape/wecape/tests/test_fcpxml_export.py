"""
FCPXML export bridge (scripts/fcpxml_export.py).

Validates the emitted FCPXML *structure* with a mocked ffprobe (no real media):
one <mc-clip> per group, one <mc-angle> per camera, asset-clip offsets normalized
to the group's earliest clip, original+proxy media-reps, resource-ref integrity,
frame-conformed time tokens, and XML well-formedness. Frame-accurate behaviour and
FCP acceptance are validated by importing into FCP — out of scope for a unit test.
"""

import calendar
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


def test_mc_clip_has_no_format_or_tcformat_attr():
    # FCPXML DTD: <mc-clip> does NOT declare 'format' or 'tcFormat' — FCP rejects them
    # ("No declaration for attribute format of element mc-clip"). They live on <multicam>.
    xml, _ = _build()
    root = _root(xml)
    mcs = root.findall(".//mc-clip")
    assert mcs
    for mc in mcs:
        assert mc.get("format") is None, "mc-clip must not carry 'format'"
        assert mc.get("tcFormat") is None, "mc-clip must not carry 'tcFormat'"
    for m in root.findall(".//multicam"):       # multicam SHOULD still carry format
        assert m.get("format") is not None


def test_assets_deduped_by_sha():
    # 5 distinct SHAs across the two groups -> 5 assets, no duplicates.
    xml, stats = _build()
    root = _root(xml)
    assert stats["assets"] == 5
    assert len(root.findall(".//asset")) == 5


# ── ungrouped single-camera clips ───────────────────────────────────────────
UNGROUPED = [
    {"original": "/src/Insta360 X5/VID_solo1.mp4", "proxy": "/out/VID_solo1_proxy.mov",
     "sha": "u1", "camera": "Insta360 X5", "resolution": "3840x2160", "duration_sec": 8.0},
    {"original": "/src/DJI ACTION 6/DJI_solo2.MP4", "proxy": None,
     "sha": "u2", "camera": "DJI Osmo Action 6", "resolution": "3840x2160", "duration_sec": 6.0},
]


def _build_ung(ungrouped, media_mode="both"):
    return fx.build_fcpxml("O-SIX", make_groups(), make_index(),
                           probe=fake_probe(), media_mode=media_mode, ungrouped=ungrouped)


def test_ungrouped_emitted_as_event_asset_clips():
    xml, stats = _build_ung(UNGROUPED)
    ev = _root(xml).find("library").find("event")
    assert len(ev.findall("asset-clip")) == 2      # event-level (direct children)
    assert len(ev.findall("mc-clip")) == 2         # multicam clips still present
    assert stats["ungrouped"] == 2


def test_ungrouped_clips_are_not_inside_multicam():
    root = _root(_build_ung(UNGROUPED)[0])
    assert len(root.findall(".//multicam//asset-clip")) == 5   # grouped placements
    event_clips = root.find("library").find("event").findall("asset-clip")
    names = {c.get("name") for c in event_clips}
    assert names == {"VID_solo1", "DJI_solo2"}


def test_groups_only_omits_ungrouped():
    xml, stats = fx.build_fcpxml("O-SIX", make_groups(), make_index(),
                                 probe=fake_probe(), ungrouped=None)
    assert _root(xml).find("library").find("event").findall("asset-clip") == []
    assert stats["ungrouped"] == 0


def test_ungrouped_assets_resolve_refs_and_carry_proxy():
    xml, _ = _build_ung(UNGROUPED)
    root = _root(xml)
    ids = {e.get("id") for e in root.iter() if e.get("id")}
    for c in root.find("library").find("event").findall("asset-clip"):
        assert c.get("ref") in ids
    assert "/out/VID_solo1_proxy.mov" in xml          # u1 proxy linked
    assert "file:///src/DJI%20ACTION%206/DJI_solo2.MP4" in xml   # u2 original (no proxy)


# ── chronological order + timestamp-prefixed names ──────────────────────────
def _groups_ts():
    g = make_groups()
    g[0]["timestamp_start"] = calendar.timegm((2026, 3, 14, 6, 0, 0, 0, 0, 0))    # 06:00 UTC
    g[1]["timestamp_start"] = calendar.timegm((2026, 3, 14, 12, 0, 0, 0, 0, 0))   # 12:00 UTC
    return g


UNGROUPED_TS = [
    {"original": "/src/Insta360 X5/VID_a.mp4", "proxy": "/out/VID_a_proxy.mov", "sha": "u1",
     "camera": "Insta360 X5", "resolution": "3840x2160", "duration_sec": 8.0,
     "corrected_timestamp": "2026-03-14T09:00:00"},
    {"original": "/src/DJI ACTION 6/DJI_b.MP4", "proxy": None, "sha": "u2",
     "camera": "DJI Osmo Action 6", "resolution": "3840x2160", "duration_sec": 6.0,
     "corrected_timestamp": "2026-03-14T18:00:00"},
]


def _build_ts(timestamp_names=True):
    return fx.build_fcpxml("O-SIX", _groups_ts(), make_index(), probe=fake_probe(),
                           ungrouped=UNGROUPED_TS, timestamp_names=timestamp_names)


def test_event_items_sorted_chronologically():
    ev = _root(_build_ts()[0]).find("library").find("event")
    names = [c.get("name") for c in list(ev)]     # mc-clips + asset-clips, document order
    assert names == sorted(names)                 # timestamp-prefixed -> lexical == chronological
    assert names[0].startswith("2026-03-14 06:00:00")    # earliest group first
    assert names[-1].startswith("2026-03-14 18:00:00")   # latest ungrouped last


def test_names_are_timestamp_prefixed():
    ev = _root(_build_ts()[0]).find("library").find("event")
    for c in list(ev):
        assert re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} · ", c.get("name")), c.get("name")


def test_no_timestamp_prefix_still_chronological():
    ev = _root(_build_ts(timestamp_names=False)[0]).find("library").find("event")
    names = [c.get("name") for c in list(ev)]
    assert not any("·" in n for n in names)              # prefix suppressed
    assert names.index("Multicam 01") < names.index("Multicam 02")   # still capture-ordered


def test_ungrouped_timestamp_from_filename_when_no_corrected_ts():
    ung = [{"original": "/src/DJI ACTION 6/DJI_20260314072347_0001_D.MP4", "proxy": None,
            "sha": "uf", "camera": "DJI Osmo Action 6", "resolution": "3840x2160",
            "duration_sec": 5.0, "corrected_timestamp": None}]
    ev = _root(fx.build_fcpxml("O-SIX", [], make_index(), probe=fake_probe(), ungrouped=ung)[0])\
        .find("library").find("event")
    names = [c.get("name") for c in list(ev)]
    assert names and names[0].startswith("2026-03-14 07:23:47")   # parsed from the filename


# ── angle labels, per-clip numbering, multicam names, metadata ──────────────
def test_angle_labels_are_camera_plus_clip_number():
    root = _root(_build()[0])
    labels = [a.get("name") for a in root.findall(".//mc-angle")]
    assert labels and all(re.search(r" - \d{2}$", n) for n in labels), labels
    assert any(n.startswith("Insta360 X5 - ") for n in labels)


def test_multiple_clips_same_camera_get_distinct_numbered_angles():
    g = [{"group_id": "G", "timestamp_start": 100, "files": [
        {"file_hash_sha256": "s1", "path": "/src/DJI ACTION 6/DJI_1.MP4",
         "camera_source": "DJI Osmo Action 6", "timestamp_delta_seconds": 0.0},
        {"file_hash_sha256": "s2", "path": "/src/DJI ACTION 6/DJI_2.MP4",
         "camera_source": "DJI Osmo Action 6", "timestamp_delta_seconds": 3.0},
        {"file_hash_sha256": "s3", "path": "/src/Insta360 X5/VID_1.mp4",
         "camera_source": "Insta360 X5", "timestamp_delta_seconds": 1.0}]}]
    idx = {s: {"proxy_path": None, "resolution": "3840x2160", "duration_sec": 5.0}
           for s in ("s1", "s2", "s3")}
    labels = [a.get("name") for a in _root(fx.build_fcpxml("O", g, idx, probe=fake_probe())[0]).findall(".//mc-angle")]
    # numbered chronologically by delta; the two DJI clips stay distinct
    assert labels == ["DJI Osmo Action 6 - 01", "Insta360 X5 - 02", "DJI Osmo Action 6 - 03"]


def test_multicam_named_sequentially():
    names = [c.get("name") for c in _root(_build_ts()[0]).findall(".//mc-clip")]
    assert any("Multicam 01" in n for n in names)
    assert any("Multicam 02" in n for n in names)


def test_clips_carry_metadata_note():
    # DTD: <note> is a first-child element (not an attribute). FCP shows it in Notes.
    xml, _ = fx.build_fcpxml("O-SIX Shoot", make_groups(), make_index(),
                             probe=fake_probe(), ungrouped=UNGROUPED, run_id="WEF_TESTRUN")
    root = _root(xml)

    def note_text(el):
        n = el.find("note")
        return n.text if n is not None else ""

    angle_clips = root.findall(".//mc-angle/asset-clip")
    assert angle_clips and all("cam=" in note_text(a) and "shoot=O-SIX Shoot" in note_text(a)
                               for a in angle_clips)
    assert any("run=WEF_TESTRUN" in note_text(a) for a in angle_clips)
    ev_clips = root.find("library").find("event").findall("asset-clip")
    assert all("file=" in note_text(c) for c in ev_clips)
    # a mc-clip's note is also a child element
    assert any("angles" in note_text(mc) for mc in root.findall(".//mc-clip"))


def test_clips_carry_camera_and_date_keywords():
    # <keyword> children -> FCP Keyword Collections ("Camera: …", "Shoot: …").
    xml, _ = fx.build_fcpxml("O-SIX", _groups_ts(), make_index(), probe=fake_probe(),
                             ungrouped=UNGROUPED_TS, run_id="R")
    ev = _root(xml).find("library").find("event")
    kws = [k.get("value") for k in ev.findall("asset-clip/keyword")]
    assert any("Camera: Insta360 X5" in v for v in kws)
    assert any("Shoot: 2026-03-14" in v for v in kws)
    mc_kw = [k.get("value") for mc in ev.findall("mc-clip") for k in mc.findall("keyword")]
    assert mc_kw and any("Camera:" in v and "Shoot: 2026-03-14" in v for v in mc_kw)


def test_keyword_is_after_note_and_well_formed():
    xml, _ = fx.build_fcpxml("O-SIX", [], make_index(), probe=fake_probe(),
                             ungrouped=UNGROUPED_TS)
    minidom.parseString(xml)                       # DTD-shaped: note then keyword
    for ac in _root(xml).find("library").find("event").findall("asset-clip"):
        kids = [c.tag for c in list(ac)]
        assert kids == ["note", "keyword"] or kids == ["keyword"], kids
        assert all(k.get("value") for k in ac.findall("keyword"))   # value required


# ── still images ────────────────────────────────────────────────────────────
STILLS = [
    {"original": "/photos/IMG_0001.HEIC", "ts": "2026-03-14T12:13:00", "camera": "iPhone"},
    {"original": "/photos/screenshot.png", "ts": "2026-03-14T09:00:00", "camera": None},
]


def test_stills_emitted_as_image_assets_with_keyword():
    xml, stats = fx.build_fcpxml("O-SIX", [], make_index(), probe=fake_probe(),
                                 stills=STILLS, run_id="R")
    minidom.parseString(xml)
    root = _root(xml)
    imgs = [a for a in root.findall(".//asset") if a.get("hasAudio") == "0"]   # image assets
    assert len(imgs) == 2 and all(a.get("duration") == "0s" for a in imgs)
    ev = root.find("library").find("event")
    kws = [k.get("value") for c in ev.findall("asset-clip") for k in c.findall("keyword")]
    assert any("Stills" in v for v in kws)
    assert any("Camera: iPhone (Stills)" in v for v in kws)     # IMG_ -> iPhone still
    assert stats["stills"] == 2


def test_still_format_has_no_frameduration():
    xml, _ = fx.build_fcpxml("O", [], make_index(), probe=fake_probe(), stills=STILLS)
    root = _root(xml)
    img_fmt_ids = {a.get("format") for a in root.findall(".//asset") if a.get("hasAudio") == "0"}
    for f in root.findall(".//format"):
        if f.get("id") in img_fmt_ids:
            assert f.get("frameDuration") is None            # stills carry no frameDuration


def test_still_capture_time_prefers_filename_source_moment():
    # A video screenshot's name carries the SOURCE clip's moment (3/14 09:30:40); that
    # beats the grab date (3/22, in the trailing timestamp / EXIF / mtime).
    name = "/x/VID_20260314_093040_00_007_2026-03-22_14-25-17_screenshot.jpg"
    assert fx._still_capture_time(Path(name)).startswith("2026-03-14T09:30:40")


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
