#!/usr/bin/env python3
"""
W.E. C.A.P.E. — New Shoot GUI  (PyWebView skin over the new_shoot core)

A native window that renders local HTML/JS (new_shoot_gui.html) and drives the
SAME headless core as the CLI — `new_shoot.py`. The GUI holds ZERO orchestration
logic: it only collects input, calls the core, and shows progress. Everything it
does is also doable from the CLI, so the skin is never the only path.

Why PyWebView: BSD-licensed (unlike PySimpleGUI, now paid), one dependency, and
it reuses the design language of the dashboard + Next-Steps card. macOS uses the
system WKWebView — nothing bundled.

Install once:   pip3 install pywebview
Run:            python3 scripts/new_shoot_gui.py   (or double-click new_shoot_gui.command)

stdlib + pywebview only · zero network · read-only on cards.
"""

import json
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import new_shoot as ns                      # the core — single source of truth

try:
    import webview                          # pip3 install pywebview
except Exception:                           # keep the module importable for tests
    webview = None

HTML = Path(__file__).resolve().parent / "new_shoot_gui.html"


# ─────────────────────────────────────────────────────────────────────────────
# Testable, window-free logic (unit-tested without launching a GUI)
# ─────────────────────────────────────────────────────────────────────────────
def _manifest_from(payload):
    return ns.ShootManifest(name=payload.get("name") or "shoot",
                            date=payload.get("date", ""),
                            location=payload.get("location", ""),
                            trusted_clock=payload.get("trusted_clock", "unknown"))


def build_preview(payload, volumes="/Volumes"):
    """What WILL happen: plan steps, pre-flight space, and any unlabeled cards.
    Pure read-only — writes nothing."""
    cards = payload.get("cards") or []
    m = _manifest_from(payload)
    plan = ns.build_plan(m, cards, payload.get("dest", ""), payload.get("output", ""),
                         payload.get("dest2"), payload.get("proxy", True),
                         payload.get("stills"))
    total = sum(int(c.get("bytes", 0)) for c in cards)
    dests = [payload.get("dest", "")] + ([payload["dest2"]] if payload.get("dest2") else [])
    pf = ns.preflight_space(total, dests)
    unlabeled = [c["mount"] for c in cards if not c.get("camera")]
    return {"plan": plan, "preflight": pf, "unlabeled": unlabeled, "total_bytes": total}


def do_run(payload, emit, runners=None):
    """Execute the shoot, forwarding each step to `emit(stage, detail)`.
    `runners` lets tests inject fakes for the offload/CAPTURE/export/open edges."""
    m = _manifest_from(payload)
    return ns.run_new_shoot(
        m, payload.get("cards") or [], payload.get("dest", ""), payload.get("output", ""),
        dest2=payload.get("dest2"), stills=payload.get("stills"),
        proxy=payload.get("proxy", True), db=payload.get("db"),
        runners=runners, progress=emit)


# ─────────────────────────────────────────────────────────────────────────────
# The JS bridge — pywebview exposes these as window.pywebview.api.*
# ─────────────────────────────────────────────────────────────────────────────
class Api:
    def __init__(self, volumes="/Volumes"):
        self.volumes = volumes
        self._window = None

    # fast, synchronous calls -------------------------------------------------
    def detect(self):
        return {"cards": ns.detect_cards(self.volumes),
                "cameras": [model for _, model in ns.load_camera_patterns()]}

    def preview(self, payload):
        try:
            return build_preview(payload, self.volumes)
        except Exception as e:                       # never crash the window
            return {"error": str(e)}

    # long-running: run on a worker thread, stream events back to the page ----
    def run(self, payload):
        threading.Thread(target=self._run_thread, args=(payload,), daemon=True).start()
        return {"started": True}

    def _run_thread(self, payload):
        def emit(stage, detail):
            self._push({"stage": stage, "detail": detail})
        try:
            res = do_run(payload, emit)
            self._push({"stage": "result", "detail": res})
        except Exception as e:
            self._push({"stage": "error", "detail": {"message": str(e)}})

    def _push(self, obj):
        if self._window is not None:
            # double-encode so the JS receives a string it JSON.parses (safe quoting)
            self._window.evaluate_js(f"window.onWecapeEvent({json.dumps(json.dumps(obj))})")


def main(argv=None):
    if webview is None:
        print("PyWebView isn't installed. Run:  pip3 install pywebview\n"
              "(The CLI works without it:  python3 scripts/new_shoot.py detect)")
        return 1
    if not HTML.exists():
        print(f"missing UI file: {HTML}")
        return 1
    api = Api()
    win = webview.create_window("W.E. C.A.P.E. — New Shoot", url=HTML.as_uri(),
                                js_api=api, width=980, height=760, min_size=(820, 640))
    api._window = win
    webview.start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
