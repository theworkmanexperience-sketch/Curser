"""
Footage-first camera identity (scripts/camera_identity.py).

Pins the whole point of the module: identity comes from the FOOTAGE, the volume
label is only a weak hint, and a label that CONTRADICTS the footage is a hard
conflict (never a silent mislabel). Uses the real kit's verified serials.
"""

import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import camera_identity as ci        # scripts/camera_identity.py

A6 = "9KRXNC800BGX5N"               # DJI Osmo Action 6
A5 = "82JXN4500BW1VE"               # DJI Osmo Action 5 Pro
X5 = "IAHEA2503SK8FE"               # Insta360 X5


# ── registry ────────────────────────────────────────────────────────────────
def test_registry_seeded_with_three_bodies():
    reg = ci.load_registry(path="/no/such/file")
    serials = {r["serial"] for r in reg}
    assert {A6, A5, X5} <= serials


def test_registry_merges_cameras_yaml():
    with tempfile.TemporaryDirectory() as t:
        y = Path(t) / "cameras.yaml"
        y.write_text("cameras:\n  - label: GoPro Hero 13\n    brand: GoPro\n    serial: GP12345\n")
        labels = {r["label"] for r in ci.load_registry(path=y)}
        assert "GoPro Hero 13" in labels and "Insta360 X5" in labels     # merged, not replaced


def test_registry_match_by_serial_and_by_model():
    reg = ci.load_registry(path="/no/such/file")
    assert ci.registry_match({"serial": A5}, reg)["label"] == "DJI Osmo Action 5 Pro"
    # device_name / model containment also matches (probe-tolerant)
    assert ci.registry_match({"model": "OsmoAction6-84CB"}, reg)["label"] == "DJI Osmo Action 6"


# ── signal extractors ─────────────────────────────────────────────────────────
def test_brand_from_files():
    assert ci.brand_from_files(["DJI_0007.MP4"]) == "DJI"                 # brand, not body
    assert ci.brand_from_files(["VID_20260101_00_001.insv"]) == "Insta360 X5"
    assert ci.brand_from_files(["P7030001.MOV"]) == "OM System OM-1"
    assert ci.brand_from_files(["random.txt"]) is None


def test_serial_from_metadata_parses_injected_exiftool():
    text = "Serial Number                   : 82JXN4500BW1VE\nModel : OsmoAction5ProA715\nMake : DJI\n"
    meta = ci.serial_from_metadata("x.mp4", runner=lambda p: text)
    assert meta["serial"] == A5 and "OsmoAction5Pro" in meta["model"] and meta["make"] == "DJI"


def test_serial_from_metadata_graceful_when_no_exiftool():
    assert ci.serial_from_metadata("x.mp4", runner=lambda p: "") == {}


def test_dji_model_code_extracted_from_category_tag():
    # Real DJI shape: the model lives in the Category tag's model_name token.
    text = ("Category  : pb_file:dvtm_ac206.proto;model_name:AC006;pb_version:2.0.1;\n")
    meta = ci.serial_from_metadata("x.mp4", runner=lambda p: text)
    assert meta["model_code"] == "AC006"


def test_model_code_identifies_action_6_from_footage():
    # WEDDING card reality: files report AC006 -> Action 6, authoritatively.
    idn = ci.identify("WEDDING", ["DJI_0001.MP4"], meta={"model_code": "AC006"})
    assert idn["label"] == "DJI Osmo Action 6" and idn["confidence"] == "verified"


def test_action5pro_code_catches_the_label_trap():
    # RESOLVED: AC004 = Action 5 Pro. The "DJIAction6" card's footage is AC004, so it
    # resolves to the 5 Pro AND flags a conflict against its misleading volume name.
    idn = ci.identify("DJIAction6", ["DJI_0001.MP4"], meta={"model_code": "AC004"})
    assert idn["label"] == "DJI Osmo Action 5 Pro" and idn["confidence"] == "verified"
    assert idn["conflict"] is True and "DJI Osmo Action 6" in idn["label_hint"]


def test_unmapped_dji_code_falls_through_to_confirm_not_mislabel():
    # A code we don't own (AC003 = Action 4) must NOT be guessed; brand is still DJI,
    # so we ask which body rather than trusting the card name.
    idn = ci.identify("SomeCard", ["DJI_0001.MP4"], meta={"model_code": "AC003"})
    assert idn["label"] is None and idn["confidence"] == "brand"
    assert idn["must_confirm"] is True


# ── the decision ──────────────────────────────────────────────────────────────
def test_metadata_serial_is_authoritative_and_catches_the_label_trap():
    # THE case: card NAMED "DJIAction6" but its footage serial is the Action 5 Pro.
    idn = ci.identify("DJIAction6", ["DJI_20260625_0001.MP4"], meta={"serial": A5})
    assert idn["label"] == "DJI Osmo Action 5 Pro"
    assert idn["confidence"] == "verified"
    assert idn["conflict"] is True and idn["must_confirm"] is True
    assert "DJI Osmo Action 6" in idn["label_hint"]          # what the name wrongly suggested


def test_verified_and_consistent_needs_no_confirm():
    idn = ci.identify("WEDDING", ["DJI_0001.MP4"], meta={"serial": A6})
    assert idn["label"] == "DJI Osmo Action 6"
    assert idn["confidence"] == "verified" and idn["conflict"] is False
    assert idn["must_confirm"] is False


def test_ambiguous_dji_brand_defers_to_confirm_not_the_label():
    idn = ci.identify("Untitled", ["DJI_0001.MP4"], meta=None)
    assert idn["label"] is None and idn["brand"] == "DJI"
    assert idn["confidence"] == "brand" and idn["must_confirm"] is True
    assert set(idn["options"]) == {"DJI Osmo Action 6", "DJI Osmo Action 5 Pro"}


def test_single_body_brand_identifies_outright():
    idn = ci.identify("card", ["VID_20260101_00_001.insv"], meta=None)
    assert idn["label"] == "Insta360 X5" and idn["confidence"] == "file"


def test_label_only_is_weak_and_must_confirm():
    # A name-only match is NOT high confidence anymore (the inversion).
    idn = ci.identify("DJI ACTION 6", [], meta=None)
    assert idn["label"] == "DJI Osmo Action 6"
    assert idn["confidence"] == "label" and idn["must_confirm"] is True


def test_brand_beats_a_contradicting_label():
    # Files say Insta360, card is named "DJI ACTION 6" → footage wins, conflict flagged.
    idn = ci.identify("DJI ACTION 6", ["VID_00_001.insv"], meta=None)
    assert idn["label"] == "Insta360 X5" and idn["conflict"] is True


def test_nothing_known_asks_to_choose():
    idn = ci.identify("SOMECARD", ["random.txt"], meta=None)
    assert idn["label"] is None and idn["confidence"] == "none" and idn["must_confirm"] is True


# ── labels + prompts ──────────────────────────────────────────────────────────
def test_labels_compatible_distinguishes_action_5_and_6():
    assert ci._labels_compatible("DJI Osmo Action 6", "DJI Osmo Action 6")
    assert not ci._labels_compatible("DJI Osmo Action 6", "DJI Osmo Action 5 Pro")


def test_status_taxonomy():
    # every outcome carries exactly one named status (error taxonomy / audit provenance)
    assert ci.identify("WEDDING", ["DJI_1.MP4"], meta={"model_code": "AC006"})["status"] == "verified"
    assert ci.identify("DJIAction6", ["DJI_1.MP4"], meta={"model_code": "AC004"})["status"] == "conflict"
    assert ci.identify("Untitled", ["DJI_1.MP4"], meta=None)["status"] == "ambiguous"
    assert ci.identify("DJI ACTION 6", [], meta=None)["status"] == "label_only"
    assert ci.identify("X", ["random.txt"], meta=None)["status"] == "unknown"


def test_confirm_prompt_wording():
    conflict = ci.identify("DJIAction6", ["DJI_1.MP4"], meta={"serial": A5})
    assert "CONFLICT" in ci.confirm_prompt(conflict)
    verified = ci.identify("WEDDING", ["DJI_1.MP4"], meta={"serial": A6})
    assert "verified" in ci.confirm_prompt(verified).lower()
    ambiguous = ci.identify("Untitled", ["DJI_1.MP4"], meta=None)
    assert "Which camera" in ci.confirm_prompt(ambiguous)
