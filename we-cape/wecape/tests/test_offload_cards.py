"""
Verified card offload (scripts/offload_cards.py).

Pins the safety-critical bits: SHA-256 correctness, copy+verify, resume-skip, and —
most important — that a copy whose bytes DON'T match the source is reported as a
failure (never a silent pass), plus cruft/ext filtering of the source listing.
"""

import hashlib
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import offload_cards as oc          # scripts/offload_cards.py


def test_sha256_matches_hashlib():
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "x.bin"
        p.write_bytes(b"the workman experience" * 1000)
        assert oc.sha256(p) == hashlib.sha256(p.read_bytes()).hexdigest()


def test_copy_verify_happy_path():
    with tempfile.TemporaryDirectory() as t:
        src = Path(t) / "s.bin"; src.write_bytes(b"hello world")
        h = oc.sha256(src)
        ok, dh, skipped = oc.copy_verify(src, Path(t) / "sub" / "d.bin", h)
        assert ok is True and dh == h and skipped is False
        assert (Path(t) / "sub" / "d.bin").read_bytes() == b"hello world"


def test_copy_verify_resume_skips_when_already_verified():
    with tempfile.TemporaryDirectory() as t:
        src = Path(t) / "s.bin"; src.write_bytes(b"data" * 500)
        h = oc.sha256(src)
        dst = Path(t) / "d.bin"
        ok1, _, sk1 = oc.copy_verify(src, dst, h)
        ok2, _, sk2 = oc.copy_verify(src, dst, h)
        assert ok1 and not sk1          # first: real copy
        assert ok2 and sk2              # second: resume-skip (already verified)


def test_copy_verify_detects_mismatch():
    # A copy whose hash != the source's must come back ok=False (never silent pass).
    with tempfile.TemporaryDirectory() as t:
        src = Path(t) / "s.bin"; src.write_bytes(b"real bytes")
        ok, dh, skipped = oc.copy_verify(src, Path(t) / "d.bin", "deadbeef_not_the_real_hash")
        assert ok is False and skipped is False
        assert dh == oc.sha256(src)     # it reports the actual hash it computed


def test_is_cruft():
    assert oc.is_cruft(Path(".DS_Store"))
    assert oc.is_cruft(Path("DCIM/._DJI_0001.MP4"))
    assert oc.is_cruft(Path("x/.Trashes/y.bin"))
    assert not oc.is_cruft(Path("DCIM/100MEDIA/DJI_0001.MP4"))


def test_list_source_filters_cruft_and_ext():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        (root / "DCIM").mkdir()
        (root / "DCIM" / "DJI_0001.MP4").write_bytes(b"v")
        (root / "DCIM" / "DJI_0001.SRT").write_bytes(b"s")
        (root / ".DS_Store").write_bytes(b"x")
        (root / "DCIM" / "._DJI_0001.MP4").write_bytes(b"x")
        # no ext filter -> 2 real files, cruft excluded
        _, files = oc.list_source(root, None)
        names = sorted(f.name for f in files)
        assert names == ["DJI_0001.MP4", "DJI_0001.SRT"]
        # ext filter -> only the MP4
        _, only_mp4 = oc.list_source(root, {"mp4"})
        assert [f.name for f in only_mp4] == ["DJI_0001.MP4"]


# ── shoot manifest (shoot.yaml) writing at offload ───────────────────────────
def test_render_manifest_shape_matches_health_parser():
    # The rendered trusted_clock line must be parseable by health_report's reader.
    text = oc.render_manifest({"shoot_name": "O-SIX", "trusted_clock": "DJI Osmo Action 6",
                               "cameras": ["DJI ACTION 6", "Insta360 X5"]})
    assert "trusted_clock: DJI Osmo Action 6" in text
    assert "cameras: [DJI ACTION 6, Insta360 X5]" in text
    import health_report as hr
    assert hr.load_trusted_clock  # sanity: importable
    parsed = oc.parse_manifest(text)
    assert parsed["trusted_clock"] == "DJI Osmo Action 6"
    assert parsed["cameras"] == ["DJI ACTION 6", "Insta360 X5"]


def test_merge_manifest_appends_cameras_and_overwrites_scalars():
    first = oc.merge_manifest("", {"shoot_name": "O-SIX", "trusted_clock": "DJI Osmo Action 6",
                                   "_camera": "DJI ACTION 6"})
    # second card offload: same shoot, new camera, and a corrected note
    second = oc.merge_manifest(first, {"notes": "Insta360 clock not reset", "_camera": "Insta360 X5"})
    d = oc.parse_manifest(second)
    assert d["cameras"] == ["DJI ACTION 6", "Insta360 X5"]     # accumulated, no dupes
    assert d["trusted_clock"] == "DJI Osmo Action 6"           # preserved across merge
    assert d["notes"] == "Insta360 clock not reset"
    # re-offloading the same camera must not duplicate it
    third = oc.merge_manifest(second, {"_camera": "Insta360 X5"})
    assert oc.parse_manifest(third)["cameras"] == ["DJI ACTION 6", "Insta360 X5"]


def test_write_shoot_manifest_roundtrip(tmp_path=None):
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        p = oc.write_shoot_manifest(root, "DJI ACTION 6",
                                    {"shoot_name": "O-SIX", "trusted_clock": "DJI Osmo Action 6"})
        assert p == root / oc.MANIFEST_NAME and p.exists()
        # a real Health-Report read of the written file yields the trusted clock
        import health_report as hr
        assert hr.load_trusted_clock(str(p)) == "DJI Osmo Action 6"


def test_empty_manifest_only_written_when_fields_given():
    # parse of an empty string is empty; render of empty data has no field lines
    assert oc.parse_manifest("") == {}
    body = oc.render_manifest({})
    assert "trusted_clock" not in body and "cameras" not in body
