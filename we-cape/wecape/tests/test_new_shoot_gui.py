"""
New Shoot GUI bridge (scripts/new_shoot_gui.py) — window-free unit tests.

The window itself needs a display and pywebview, so it can't be tested here. But
the bridge's *logic* — build_preview() and do_run() — is plain and delegates to
the core, so it's fully testable with pywebview absent and the impure edges faked.
Also pins the core's new progress(stage, detail) callback.
"""

import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import new_shoot as ns
import new_shoot_gui as gui          # imports fine even without pywebview (guarded)


def test_module_imports_without_pywebview():
    # webview may be None in a headless/CI env — the module must still load.
    assert hasattr(gui, "build_preview") and hasattr(gui, "do_run")


def test_build_preview_reports_plan_and_preflight():
    with tempfile.TemporaryDirectory() as t:
        payload = {"name": "S", "dest": t, "output": str(Path(t) / "out"),
                   "cards": [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 100}]}
        r = gui.build_preview(payload)
        assert r["preflight"]["ok"] and r["plan"] and not r["unlabeled"]


def test_build_preview_flags_unlabeled_card():
    with tempfile.TemporaryDirectory() as t:
        payload = {"name": "S", "dest": t, "output": str(Path(t) / "out"),
                   "cards": [{"mount": "/Volumes/C", "camera": None, "bytes": 1}]}
        assert gui.build_preview(payload)["unlabeled"] == ["/Volumes/C"]


def _fake_runners(calls):
    return {
        "offload": lambda *a: (calls.append(("offload", a)), 0)[1],
        "capture": lambda src, out, extra: (calls.append(("capture", src)), "WEF_20260703_120000_ABCDEF")[1],
        "export": lambda rid, out, db, stills: (calls.append(("export", rid)), 0)[1],
        "open": lambda p: True,
    }


def test_do_run_streams_events_and_completes():
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        payload = {"name": "S", "dest": t, "output": str(out),
                   "cards": [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 100}]}
        events, calls = [], []
        res = gui.do_run(payload, lambda stage, detail: events.append(stage), runners=_fake_runners(calls))
        stages = [e for e in events]
        assert "manifest" in stages and "capture" in stages and stages[-1] == "done"
        assert res["run_id"] == "WEF_20260703_120000_ABCDEF" and not res["errors"]


def test_progress_callback_optional_in_core():
    # run_new_shoot must behave identically with no progress callback (headless).
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        cards = [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 100}]
        res = ns.run_new_shoot(ns.ShootManifest(name="S"), cards, t, out,
                               runners=_fake_runners([]))     # no progress=
        assert res["exported"] and not res["errors"]


def test_progress_receives_stage_and_detail():
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "out"
        cards = [{"mount": "/Volumes/C", "camera": "Insta360 X5", "bytes": 100}]
        seen = []
        ns.run_new_shoot(ns.ShootManifest(name="S"), cards, t, out,
                         runners=_fake_runners([]), progress=lambda s, d: seen.append((s, d)))
        stages = [s for s, _ in seen]
        assert "offload_start" in stages and "export" in stages
        # detail is always a dict
        assert all(isinstance(d, dict) for _, d in seen)
