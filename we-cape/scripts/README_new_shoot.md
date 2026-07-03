# New Shoot — the Phase 0 → Final Cut front door

`scripts/new_shoot.py` is the **headless orchestration core** behind the "New Shoot"
wizard. It chains the tools you already have — **verified card offload → CAPTURE →
FCPXML export → Final Cut Pro** — behind one guided flow, and records the shoot
manifest (name / date / location / trusted-clock) as a sidecar that later feeds
export keywords and the Production Health report.

## Why a core, not a GUI (yet)

A wizard is a skin. If orchestration logic lived in button callbacks it would weld
the product to one UI framework and break the "thin wizard, tools stay independently
runnable" rule. So the logic lives here as plain, unit-tested functions with **no GUI
and no network**. A graphical skin (PyWebView is the planned choice — BSD-licensed,
reuses the dashboard/cheat-sheet HTML) can sit on top later without touching any of it.

> Note on GUI toolkits: **PySimpleGUI is no longer free** (paid commercial license
> since 2024). PyWebView / Tkinter stay license-clean, which is why they're the path.

## What it does, in order

1. **Write the manifest** → `shoot.yaml` in the output folder (one intake, many consumers).
2. **Pre-flight space** — checks each destination has room (+10% headroom) *before* any copy.
3. **Verified offload** — each card → `<dest>/<shoot>/<camera>/…`, every copy SHA-256
   checked, optional second destination (two copies before CAPTURE — Principle #1).
4. **CAPTURE** the offloaded shoot folder (`python -m wecape … --proxy`).
5. **Export FCPXML** for the new run.
6. **Open Final Cut** on the import sheet + the Next-Steps guide.

Every step writes a line to `_new_shoot_session.jsonl` in the output folder (audit
trail, P3). The flow is **idempotent**: offload resumes by hash, CAPTURE skips by SHA —
re-running a finished shoot is safe and fast.

## Card → camera mapping is a guess you confirm

`detect` scans `/Volumes` for cards (a `DCIM` folder or media files) and proposes a
camera per card:

- `✓ high`  — the card/volume name matches a per-body pattern (`DJI ACTION 6`, `Insta360 X5`).
- `~ medium` — filenames match a known family (`DJI_*`, `IMG_*`, `*_00_*.insv`).
- `? low`   — nothing matched; **you must choose** (`--card 'MOUNT=DJI ACTION 6'`).

An unlabeled card is **never silently offloaded** — it's skipped and reported.

## CLI (v1 front end)

```bash
# 1. See what's plugged in
python3 scripts/new_shoot.py detect

# 2. Preview the whole run — writes nothing
python3 scripts/new_shoot.py plan \
    --name "O-SIX_2026" --date 2026-03-14 --location "Clubhouse" \
    --trusted-clock "DJI Osmo Action 6" \
    --dest /Volumes/10TB --dest2 "/Volumes/Got My BackUP" \
    --output /Volumes/WE_CAPE_OUTPUT/O-SIX_2026

# 3. Run it (add --card MOUNT=CAMERA for any '?' cards; --no-proxy to skip transcode)
python3 scripts/new_shoot.py run  … same flags …  --stills "/Volumes/…/Photos"
```

Each step is also runnable standalone (`offload_cards.py`, `python -m wecape`,
`fcpxml_export.py`) — the wizard never becomes the only path.

## Privacy: paths hashed on the way out (SECURITY_RISK_ANALYSIS D1)

`shoot.yaml` and the session log keep **full paths readable locally** for troubleshooting.
Before anything leaves the machine (offsite backup, a shared manifest), run:

```bash
python3 scripts/new_shoot.py redact --output /Volumes/WE_CAPE_OUTPUT/O-SIX_2026
```

This writes `shoot.shared.yaml` + `_new_shoot_session.shared.jsonl` with every path-like
field **hashed** (`sha256:` — the same scheme the engine's audit uses), while keeping
shoot **name / date / location** readable, plus the note *"Paths hashed for privacy; full
paths available locally."* The local originals are untouched. `.gitignore` also blocks
committing manifests, session logs, and `*.db`.

## Graphical skin (PyWebView) — the same core, in a window

`new_shoot_gui.py` + `new_shoot_gui.html` are a thin **PyWebView** front end over this
exact core — it holds **zero orchestration logic**, only collects input and calls
`detect_cards` / `build_preview` / `run_new_shoot`. PyWebView is BSD-licensed (unlike
PySimpleGUI, now paid), needs one dependency, uses macOS's system WebView, and reuses the
dashboard/cheat-sheet design language.

```bash
pip3 install pywebview                 # one-time
python3 scripts/new_shoot_gui.py       # or double-click scripts/new_shoot_gui.command
```

The window: **Detect cards** (each card shows a confidence badge — green "name" / amber
"guess" / red "choose" — and a camera dropdown) → shoot details → destinations →
**Preview plan** (plan + pre-flight space, writes nothing) → **Start shoot** (runs on a
background thread, streaming a live log; opens Final Cut + the Next-Steps guide at the end).

The core emits a `progress(stage, detail)` callback the GUI listens to; the CLI ignores it.
Because the GUI is pure skin, everything it does is still doable from the CLI.

> **Honest caveat:** the window's logic (`build_preview`, `do_run`, the progress callback)
> is unit-tested, but a GUI can't be launched in a headless build — the **visual/interaction
> pass must be run on the Mac** (`python3 scripts/new_shoot_gui.py`). Treat the first live
> launch as the validation step.

## Out of scope for v1 (intentionally)

In-wizard video preview/thumbnails, any editing, cloud upload, multi-shoot batch queue.

Core: stdlib only · zero network · read-only on camera cards.  ·  GUI: + pywebview.
