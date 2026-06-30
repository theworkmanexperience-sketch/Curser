# SOP — Importing a W.E. C.A.P.E. FCPXML into Final Cut Pro

Companion to `fcpxml_export.py` / `README_fcpxml.md`. Follow in order. FCPXML is picky;
**Section 6 (Troubleshooting)** covers the two issues most likely on the first import —
a frame-rate edge case (often the Insta360 X5) and an offline-media relink.

---

## 1. Before you import (pre-flight — prevents 90% of problems)

1. **Mount the drives the clips live on**, so nothing imports offline:
   - **10TB** — the camera originals.
   - **WE_CAPE_OUTPUT** — the CAPTURE proxies *and* the `MULTICAM/*.json` the export reads.
2. **Generate the FCPXML** (with the drives mounted so `ffprobe` reads true frame rates):
   ```bash
   cd ~/Curser/we-cape
   python3 scripts/fcpxml_export.py --run WEF_20260630_125435_06980D
   ```
   Note the summary line — it tells you how many multicam clips/angles, and **warns if any clip
   fell back to assumed fps** (that's your early signal for a Section 6.2 frame-rate check).
3. **In FCP, create or open the target Library first** (File ▸ New ▸ Library, e.g.
   `O-SIX_CAPE.fcpbundle`). The XML brings its own *Event*; it needs a Library to land in.

---

## 2. Import the XML

1. **File ▸ Import ▸ XML…**
2. Select `Community_Service_cameras_multicam.fcpxml` (in `~/Curser/we-cape/` unless you used `--out`).
3. In the import sheet, confirm the **target Library**. Leave media settings as-is — this XML
   **references files in place** (it does *not* copy media), so there's nothing to "copy to library."
4. Click **Import**. A new **Event** (named for the shoot) appears with one **multicam clip per
   group** (the 4-squares icon).

> If the import **fails outright** (red error, "not a valid fcpxml", DTD/version complaint),
> stop and jump to **6.3** — don't fight it.

---

## 3. Verify the multicam clips

1. Select the new Event. You should see **2 multicam clips** for the O-SIX camera run (your 2 groups).
2. **Double-click** a multicam clip → the **Angle Editor** opens.
3. Confirm each **angle = a camera**: *DJI Osmo Action 6*, *DJI Osmo Action 5*, *Insta360 X5*.
4. Scrub the angles. They should be aligned **to within a second or two** — that's the timestamp
   alignment, working as intended. Frame-accurate sync is Section 5.

---

## 4. Edit on proxies (optional, recommended offline)

The assets carry both original and proxy media. To cut on the lightweight CAPTURE proxies:

1. In the **Viewer**, click the **View** pop-up (top-right) → under **Media**, choose **Proxy**
   (or *Proxy Preferred*).
2. If proxies show offline, relink them (Section 6.1) — point FCP at **WE_CAPE_OUTPUT**.
3. Switch back to **Optimized/Original** for final export (needs the **10TB** mounted).

---

## 5. Lock audio to the frame (finish the sync)

The import gives you the right cameras **grouped and roughly aligned** — CAPTURE's job. FCP does
the frame-accurate part. Two honest paths:

- **Fastest — refine in place:** in the **Angle Editor**, nudge an angle while watching the audio
  **waveforms**; line up a transient (clap, beat, door). Timestamp alignment already put you within
  a second, so this is a small slip, not a hunt.
- **Frame-accurate — let FCP sync by audio:** select the grouped clips (the export already told you
  which clips belong together), then **Clip ▸ Synchronize Clips…** *(or New Multicam Clip…)* with
  **"Use audio for synchronization"** enabled. FCP rebuilds the sync from the waveforms. You're
  using CAPTURE for the expensive *grouping* decision and FCP for the *alignment* — the intended split.

---

## 6. Troubleshooting

| # | Symptom | Fix |
|---|---------|-----|
| **6.1** | Clips are **red / "Missing File" / offline** | Drive not mounted, or path moved. Mount **10TB** (originals) + **WE_CAPE_OUTPUT** (proxies). Then **File ▸ Relink Files…**, choose **Original Media** (and again for **Proxy Media**), **Locate** → point at the folder; FCP relinks by filename. |
| **6.2** | **Wrong speed / "conform frame rate" warning / jerky angle** — often the **Insta360 X5** | An angle's real rate differs from the sequence rate the export guessed (especially if `ffprobe` was offline → "assumed fps" warning). Find the real rate, then re-export forcing it. See below. |
| **6.3** | **Import fails entirely** (invalid fcpxml / version) | Capture the exact FCP error text and send it to me. Likely a one-line fix (FCPXML version bump, or an attribute FCP wants). The version is one constant in the script. |
| **6.4** | Angles **off by a few seconds** before syncing | Expected — that's timestamp alignment, not waveform. Do Section 5. |
| **6.5** | A camera's clips **missing** from a group | That clip wasn't in the CAPTURE group (check the dashboard's multicam membership / the run's `MULTICAM/*.json`), or it had no resolvable path (the export prints a "skipped" count). |

### Fixing a frame-rate mismatch (6.2)

1. **Find the real rate** of the off clip:
   ```bash
   ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "/Volumes/10TB/.../VID_xxxx.mp4"
   # e.g. prints 30000/1001  (=29.97)  or  30/1  or  60000/1001
   ```
   (Or in FCP: select the clip ▸ **Info** inspector ▸ *Frame Rate*.)
2. **Re-export forcing that timebase:**
   ```bash
   python3 scripts/fcpxml_export.py --run WEF_20260630_125435_06980D --fps 30000/1001
   ```
3. Delete the old Event in FCP and re-import the new `.fcpxml`.

> Mixed-rate shoots (Insta360 at one rate, DJI at another) are normal — `--fps` sets the multicam's
> base timebase; FCP conforms the off-rate angles to it. Pick the rate of the camera you'll cut to
> most (usually the DJI bodies).

---

## 7. What to report back

If anything in Section 6 fires, send me:
1. The **export summary line** (multicam/angle/clip counts + any fallback warning).
2. The **exact FCP message** (screenshot or text).
3. Which clips/cameras were affected (e.g., "only the Insta360 angle").

That's usually enough for a one-shot fix — most likely a `--fps` value or a small XML attribute tweak.
