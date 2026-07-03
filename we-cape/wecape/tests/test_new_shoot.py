"""
New Shoot orchestration core (scripts/new_shoot.py).

Pins the headless spine: camera guessing, card detection, pre-flight space,
manifest sidecar round-trip, and the orchestrator's sequencing / guards
(idempotent dry-run, offload-fail abort, preflight abort, no-label skip) —
all with the impure edges (offload/CAPTURE/export/open) injected as fakes.
"""

import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import new_shoot as ns          # scripts/new_shoot.py


# ── camera guessing ──────────────────────────────────────────────────────────
def test_guess_camera_high_on_name():
    pats = [("DJI ACTION 6", "DJI Osmo Action 6"), ("Insta360 X5", "Insta360 X5")]
    label, conf = ns.guess_camera("DJI ACTION 6", [], pats)
    assert label == "DJI Osmo Action 6" and conf == "high"


def test_guess_camera_medium_on_filenames():
    label, conf = ns.guess_camera("UNTITLED", ["DJI_0007.MP4"], [])
    assert label == "DJI" and conf == "medium"


def test_om_system_guessed_from_filename():
    for fn in ("P7030001.MOV", "PA030001.ORF"):        # OM System / Olympus DCF naming
        label, conf = ns.guess_camera("NO NAME", [fn], [])
        assert label == "OM System OM-1" and conf == "medium"


def test_om_system_is_a_selectable_camera():
    models = [m for _, m in ns.load_camera_patterns()]   # what the dropdown lists
    assert "OM System OM-1" in models


def test_guess_camera_low_when_unknown():
    label, conf = ns.guess_camera("SOMECARD", ["random.txt"], [])
    assert label is None and conf == "low"


def test_longest_pattern_wins():
    pats = ns.load_camera_patterns()          # DJI ACTION 6 must beat any shorter DJI substring
    label, _ = ns.guess_camera("DJI ACTION 6", [], pats)
    assert label == "DJI Osmo Action 6"


# ── media scan + card detection ──────────────────────────────────────────────
def test_scan_media_counts_and_skips_cruft():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        (d / "A.MP4").write_bytes(b"x" * 10)
        (d / "B.mov").write_bytes(b"y" * 20)
        (d / ".DS_Store").write_bytes(b"z")
        (d / "._A.MP4").write_bytes(b"z")
        files, total, vids = ns.scan_media(d, ns.MEDIA_EXTS)
        assert vids == 2 and total == 30 and len(files) == 2


def test_loose_videos_without_structure_is_not_a_card():
    """The FreeAgent-GoFlex case: a drive full of scattered videos but NO card
    structure at root must NOT be treated as a card."""
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / "FreeAgent GoFlex Drive"
        (d / "MOVIES").mkdir(parents=True)
        (d / "MOVIES" / "IMG_0001.MOV").write_bytes(b"v" * 10)   # video, but no DCIM
        assert not ns.is_camera_card(d)


def test_dcim_or_camera_folder_counts_as_card():
    with tempfile.TemporaryDirectory() as t:
        a = Path(t) / "A"; (a / "DCIM").mkdir(parents=True)
        b = Path(t) / "B"; (b / "DJI ACTION 6").mkdir(parents=True)
        assert ns.is_camera_card(a) and ns.is_camera_card(b)


def test_detect_ignores_loose_video_drive():
    with tempfile.TemporaryDirectory() as t:
        vols = Path(t)
        real = vols / "CARD"; (real / "DCIM").mkdir(parents=True)
        (real / "DCIM" / "DJI_0001.MP4").write_bytes(b"v" * 10)
        junk = vols / "FreeAgent"; (junk / "stuff").mkdir(parents=True)
        (junk / "stuff" / "MOV_1.MOV").write_bytes(b"v" * 10)      # loose videos, no DCIM
        names = [Path(c["mount"]).name for c in ns.detect_cards(str(vols))]
        assert names == ["CARD"]


def test_detect_skips_oversized_volumes():
    """A 10 TB archive drive must be skipped WITHOUT being walked — only real cards."""
    with tempfile.TemporaryDirectory() as t:
        vols = Path(t)
        card = vols / "CARD"; (card / "DCIM").mkdir(parents=True)
        (card / "DCIM" / "DJI_0001.MP4").write_bytes(b"v" * 10)
        big = vols / "10TB"; (big / "DCIM").mkdir(parents=True)
        (big / "DCIM" / "VID.MP4").write_bytes(b"v" * 10)
        caps = {str(card): 256 * 1024 ** 3, str(big): 10 * 1024 ** 4}   # 256 GB card, 10 TB drive
        cards = ns.detect_cards(str(vols), capacity_fn=lambda m: caps.get(str(m)))
        names = [Path(c["mount"]).name for c in cards]
        assert "CARD" in names and "10TB" not in names


def test_detect_cards_finds_dcim_and_guesses():
    with tempfile.TemporaryDirectory() as t:
        vols = Path(t)
        card = vols / "DJIcard"; (card / "DCIM").mkdir(parents=True)
        (card / "DCIM" / "DJI_0001.MP4").write_bytes(b"v" * 100)
        (vols / "Macintosh HD").mkdir()          # system volume must be ignored
        cards = ns.detect_cards(str(vols))
        assert len(cards) == 1
        c = cards[0]
        assert c["camera"] == "DJI" and c["video_count"] == 1 and c["bytes"] == 100


# ── pre-flight space ─────────────────────────────────────────────────────────
def test_preflight_ok_on_real_dir():
    with tempfile.TemporaryDirectory() as t:
        pf = ns.preflight_space(1000, [t])
        assert pf["ok"] and pf["dests"][0]["known"]


def test_preflight_fails_when_needed_exceeds_free():
    with tempfile.TemporaryDirectory() as t:
        huge = ns.free_bytes(t) + 10 ** 15       # more than exists
        pf = ns.preflight_space(huge, [t])
        assert not pf["ok"]


# ── manifest sidecar round-trip ──────────────────────────────────────────────
def test_manifest_write_and_read_roundtrip():
    with tempfile.TemporaryDirectory() as t:
        m = ns.ShootManifest(name="O-SIX: Community", date="2026-03-14",
                             location="Gas station", trusted_clock="DJI Osmo Action 6",
                             cameras=[{"label": "Insta360 X5", "source": "/Volumes/CARD"}])
        p = m.write(t)
        got = ns.read_manifest(p)
        assert got["name"] == "O-SIX: Community"          # colon survives quoting
        assert got["trusted_clock"] == "DJI Osmo Action 6"
        assert got["cameras"] == [{"label": "Insta360 X5", "source": "/Volumes/CARD"}]


# ── plan ─────────────────────────────────────────────────────────────────────
def test_build_plan_lists_every_stage():
    m = ns.ShootManifest(name="S")
    cards = [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 1}]
    plan = ns.build_plan(m, cards, "/dest", "/out", proxy=True)
    joined = " ".join(plan).lower()
    assert "offload" in joined and "capture" in joined and "fcpxml" in joined and "final cut" in joined


# ── orchestrator (fakes injected) ────────────────────────────────────────────
def _fakes():
    calls = {"offload": [], "capture": [], "export": [], "open": []}
    runners = {
        "offload": lambda *a: (calls["offload"].append(a), 0)[1],
        "capture": lambda src, out, extra: (calls["capture"].append((src, out, tuple(extra))),
                                            "WEF_20260703_120000_ABCDEF")[1],
        "export": lambda rid, out, db, stills: (calls["export"].append((rid, stills)), 0)[1],
        "open": lambda p: (calls["open"].append(p), True)[1],
    }
    return runners, calls


def test_run_new_shoot_full_sequence():
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        cards = [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 100}]
        runners, calls = _fakes()
        m = ns.ShootManifest(name="Shoot")
        res = ns.run_new_shoot(m, cards, t, out, runners=runners)
        assert not res["errors"]
        assert res["run_id"] == "WEF_20260703_120000_ABCDEF" and res["exported"]
        assert len(calls["offload"]) == 1 and len(calls["capture"]) == 1 and len(calls["export"]) == 1
        assert (out / "shoot.yaml").exists()                       # manifest sidecar
        assert (out / "_new_shoot_session.jsonl").exists()         # audit trail (P3)


def test_dry_run_writes_manifest_but_no_capture():
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        cards = [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 100}]
        runners, calls = _fakes()
        res = ns.run_new_shoot(ns.ShootManifest(name="S"), cards, t, out, dry_run=True, runners=runners)
        assert calls["offload"] and not calls["capture"] and not calls["export"]
        assert (out / "shoot.yaml").exists() and res["run_id"] is None


def test_offload_failure_aborts_before_capture():
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        cards = [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 100}]
        runners, calls = _fakes()
        runners["offload"] = lambda *a: 1                          # verification MISMATCH
        res = ns.run_new_shoot(ns.ShootManifest(name="S"), cards, t, out, runners=runners)
        assert res["errors"] and not calls["capture"]             # never proceeds on a bad copy


# ── D1: paths hashed on the way out, names kept, local originals untouched ────
def test_path_hash_matches_engine_style():
    h = ns._path_hash("/Volumes/CARD/x.mp4")
    assert h.startswith("sha256:") and len(h) == len("sha256:") + 64


def test_redact_hashes_paths_but_keeps_names():
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        cards = [{"mount": "/Volumes/SECRET_LOCATION_CARD", "camera": "Insta360 X5", "bytes": 100}]
        runners, _ = _fakes()
        m = ns.ShootManifest(name="O-SIX", location="123 Private Rd")
        ns.run_new_shoot(m, cards, t, out, runners=runners)          # writes shoot.yaml + session log

        written = ns.redact_for_sharing(out)
        shared_yaml = (out / "shoot.shared.yaml").read_text()
        shared_log = (out / "_new_shoot_session.shared.jsonl").read_text()

        assert "O-SIX" in shared_yaml and "123 Private Rd" in shared_yaml     # names kept
        assert "SECRET_LOCATION_CARD" not in shared_yaml                       # path hashed away
        assert "sha256:" in shared_yaml and ns.SHARE_NOTE in shared_yaml
        assert "SECRET_LOCATION_CARD" not in shared_log and "sha256:" in shared_log
        # local originals must remain full-path for troubleshooting
        assert "SECRET_LOCATION_CARD" in (out / "shoot.yaml").read_text()
        assert len(written) == 2


def test_card_without_camera_label_is_skipped_not_guessed():
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        cards = [{"mount": "/Volumes/C", "camera": None, "bytes": 100}]
        runners, calls = _fakes()
        res = ns.run_new_shoot(ns.ShootManifest(name="S"), cards, t, out, runners=runners)
        assert not calls["offload"]                                # never silently offloads an unlabeled card
        assert any("no camera label" in e for e in res["errors"])
