# SOP — Shoot → Final Cut Pro (per-shoot runbook)

End-to-end checklist tying together the W.E. C.A.P.E. tools: **offload → CAPTURE →
FCPXML → FCP**. Deeper FCP-import detail + troubleshooting tables live in
`SOP_fcpxml_import.md`.

> Replace every `<…>` with a real name. Run `ls /Volumes` first to get exact drive
> names — **watch for trailing spaces** (e.g. the O-SIX folder has one).

---

## 0. Pre-flight

- [ ] Mount the drives: **10TB** (originals), **WE_CAPE_OUTPUT** (proxies + output), **Got My BackUP** (2nd copy).
- [ ] `ls /Volumes` — confirm the exact names of the drives and the card.

## 1. Offload cards — verified, two copies (do this FIRST, before CAPTURE)

- [ ] Dry-run each camera card to preview:
  - `python3 scripts/offload_cards.py --source "/Volumes/<CARD>" --camera "DJI ACTION 6" --shoot "<SHOOT>" --dest "/Volumes/10TB" --dry-run`
- [ ] Run for real, with a second copy:
  - add `--dest2 "/Volumes/Got My BackUP/cards"` and drop `--dry-run`
- [ ] Use the right `--camera` label so CAPTURE IDs the body: **`DJI ACTION 5`**, **`DJI ACTION 6`**, **`Insta360 X5`**.
- [ ] Repeat for every card / camera.
- [ ] Confirm the summary says **"every file verified in every destination."**
- [ ] **Do NOT format any card** until you've seen that line. (The tool never touches the card.)

## 2. CAPTURE → FCPXML → FCP (one command)

- [ ] `bash scripts/capture_to_fcp.sh "/Volumes/10TB/<SHOOT>" "/Volumes/WE_CAPE_OUTPUT/<SHOOT>" --proxy`
  - runs CAPTURE, exports the new run's FCPXML, opens FCP's import sheet
  - extra args (`--proxy`, `--profile ryderz`) pass straight to CAPTURE
- [ ] *Manual alternative* (if you want each step separately):
  - `WECAPE_NONINTERACTIVE=1 python3 -m wecape --input "/Volumes/10TB/<SHOOT>" --output "/Volumes/WE_CAPE_OUTPUT/<SHOOT>" --proxy`
  - `python3 scripts/fcpxml_export.py --run <RUN_ID>`
  - `open "/Volumes/WE_CAPE_OUTPUT/<SHOOT>/<SHOOT>_multicam.fcpxml"`

## 3. Import into Final Cut Pro

- [ ] Create/open a target **Library** first (File ▸ New ▸ Library).
- [ ] **File ▸ Import ▸ XML…** → pick the `.fcpxml`.
- [ ] Confirm the import sheet (Library / Event). Media is **referenced, not copied** — nothing duplicates.
- [ ] A new **Event** appears with **one multicam clip per group**.

## 4. Verify + lock sync

- [ ] Double-click a multicam clip → **Angle Editor** → confirm each angle = a camera (Osmo 6 / Osmo 5 / Insta360 X5).
- [ ] To edit offline: **Viewer ▸ View pop-up ▸ Proxy**; switch to **Optimized/Original** for final export.
- [ ] Lock audio (timestamp alignment is ±seconds by design):
  - nudge angles against the **waveform** in the Angle Editor, **or**
  - select the grouped clips → **Clip ▸ Synchronize Clips** (uses audio).

## 5. Troubleshoot (quick — full tables in `SOP_fcpxml_import.md`)

- [ ] **Clips red / offline** → mount the drive → **File ▸ Relink Files** (Original → 10TB, Proxy → WE_CAPE_OUTPUT).
- [ ] **Wrong speed / jerky (often the Insta360)** → get the real rate, re-export with it:
  - `ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "<clip>"`
  - `python3 scripts/fcpxml_export.py --run <RUN_ID> --fps 30000/1001`
- [ ] **Import fails (DTD / version)** → copy the exact FCP error and send it over.
- [ ] **Angles off by seconds before syncing** → expected; do step 4.

## 6. After the edit

- [ ] Registry + notes back up daily on their own schedule; force one anytime:
  - `bash scripts/backup_holder_mac.sh --registry-only`
- [ ] Review the shoot in the dashboard: `python3 scripts/dashboard.py` → open `wecape_dashboard.html`.
- [ ] Add notes: `python3 scripts/annotations.py add --scope shoot --target <RUN_ID> --body "…"`
- [ ] **Format cards only now** — and only because Step 1 verified two copies.
