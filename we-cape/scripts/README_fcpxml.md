# FCPXML Export Bridge — CAPTURE multicam groups → Final Cut Pro

Turns a CAPTURE run's multicam **groups** into a Final Cut Pro **multicam clip** per
group: each camera (DJI Osmo Action 5/6, Insta360 X5, …) becomes an **angle**, and each
clip is placed on its angle by the corrected-timestamp delta CAPTURE already computed.
One Event per shoot: one `<mc-clip>` per group, **plus every ungrouped single-camera clip as an
ordinary clip** so the *whole* shoot lands in FCP (not just the multicam moments; use `--groups-only`
to omit them). Reads the registry **read-only**; stdlib + `ffprobe`; zero network.

## The honest scope (read this first)

v1 aligns angles by **timestamp** — drift-corrected from filenames, accurate to within the
grouping window (±seconds) — **not by audio waveform**. So FCP receives the *right cameras
grouped together and roughly aligned*, then you run **Clip ▸ Synchronize Clips** (or future
J3) to lock audio to the frame.

This is the deliberate division of labor, not a shortcut:

> **CAPTURE decides *what belongs together*** (the expensive cross-camera grouping call).
> **FCP / J3 does the *frame-accurate* part** (waveform sync within each group).

It is not "we already do PluralEyes-grade sync." It's "here are your camera groups,
pre-aligned to within seconds — finish the lock in one click." That's the PluralEyes-killer
*surfacing*, honestly scoped.

## Run it
```bash
cd ~/Curser/we-cape
python3 scripts/fcpxml_export.py --run WEF_20260630_125435_06980D
# -> ./<shoot>_multicam.fcpxml
```
Options:
```bash
--db PATH        registry (default ~/.wecape/registry/wecape.db)
--out PATH       output .fcpxml (default ./<shoot>_multicam.fcpxml)
--media MODE     both | proxies | originals   (default both)
--fps N/D        force the sequence timebase, e.g. 30000/1001 or 30
--event NAME     override the Event name (default: shoot folder name)
--groups-only    export only the multicam groups (omit ungrouped single-camera clips)
--no-timestamp-prefix   keep clean clip names (no capture-time prefix; order stays chronological)
```
By default the Event holds **both** the multicam clips (the grouped moments) and the ungrouped
single-camera clips, so the full shoot is editable in FCP. The ungrouped list comes from the run's
`<run_id>_index.json`; each clip is matched to its proxy by SHA, same as the grouped ones.

**Chronological order.** Event items are emitted in **capture-time order**, and each clip's name is
prefixed with its corrected capture timestamp (e.g. `2026-03-14 07:23:47 · DJI_0001`) — so sorting the
FCP browser by **Name** gives true chronological order across *all* cameras, using CAPTURE's *corrected*
times, not the camera clock or FCP's metadata guess. Multicam clips slot in at their group's start
time, interleaved with the ungrouped clips. Times come from the group anchor (multicam) or the
registry's `corrected_timestamp`, falling back to the timestamp embedded in the filename. Use
`--no-timestamp-prefix` if you'd rather keep clean names (the XML order stays chronological either way).

**Keyword Collections (organize without scrolling).** Every clip is tagged with `<keyword>` values,
which FCP turns into clickable **Keyword Collections** in the browser sidebar — click one to see just
those clips:
- `Camera: <model>` (e.g. `Camera: Insta360 X5`) — per-camera grouping. Multicam clips are tagged with
  every camera they contain.
- `Shoot: <YYYY-MM-DD>` — per-capture-date grouping.

Camera keywords are always correct. **Date keywords are only as accurate as the camera clocks** — a
camera set to the wrong year (e.g. an Insta360 stuck at 2018) lands its clips under a wrong `Shoot:`
date. CAPTURE now persists its resolved timestamp (`corrected_timestamp`) so the export prefers it over
re-reading raw filenames, but nothing can override a genuinely wrong camera clock — set the clock.

**Naming & metadata.**
- **Angles** in a multicam clip are labeled `<camera> - NN` (e.g. `DJI Osmo Action 6 - 03`), numbered
  chronologically within the group — so multiple clips from the same camera stay distinct in the Angle Viewer.
- **Multicam clips** are named `Multicam NN` in capture order (behind the timestamp prefix).
- **Every clip** (angles + standalone) carries a **Notes** field, visible and searchable in FCP's Info
  inspector: `cam=<model> · shot=<corrected time> · file=<original> · run=<run_id> · shoot=<name>` —
  full provenance back to the source file and the CAPTURE run that produced it.
Then in Final Cut Pro: **File ▸ Import ▸ XML…**, pick the `.fcpxml`. Each group lands as a
multicam clip; open one and run **Clip ▸ Synchronize Clips** to refine audio sync.
(Full import walkthrough + troubleshooting: `SOP_fcpxml_import.md`.)

## One-command handoff

`capture_to_fcp.sh` chains it end to end — run CAPTURE on a source, auto-export the new run's
FCPXML, and open it on FCP's import sheet (one confirming click; it never UI-scripts the import,
since FCP has no import API and that step is the editor's call):
```bash
bash scripts/capture_to_fcp.sh "/Volumes/10TB/O-SIX RYDERZ MC Community Service" \
    "/Volumes/WE_CAPE_OUTPUT/O-SIX_v2" --proxy
```
Anything after the output path passes straight to `python -m wecape` (e.g. `--proxy`, `--profile
ryderz`). For an `--fps` tweak on the export, run `fcpxml_export.py` directly afterward.

## Media references (the FCP proxy workflow)

Default `--media both` writes, per asset, an `original-media` rep **and** a `proxy-media` rep
(your CAPTURE proxy). In FCP, the **View ▸ Proxy/Optimized** toggle then lets you cut offline
on proxies and conform to full-res originals when the 10TB is mounted.

- **Proxies are linked by SHA-256** (`content.id`). Because the registry uses a field-preserving
  upsert (P5), proxy paths from your earlier proxy run are **preserved on the same SHAs** — so a
  no-proxy re-CAPTURE (like the camera-identity run) still links its proxies. You don't have to
  re-transcode to export.
- `--media proxies` references only the always-available proxies (a clip with no proxy falls back
  to its original). `--media originals` references only full-res (needs the originals' drive mounted).

## Formats & timing

`ffprobe` reads each source's real resolution, frame rate, and duration so the FCPXML formats and
times are correct. If `ffprobe` is unavailable or a file is offline, it **falls back to registry
metadata** (resolution + duration) and *assumes* the sequence fps — the run warns, and you should
verify timing in FCP. All times are emitted as frame-conformed rational values (`N/Ds`).

## Compatibility

Targets **FCPXML 1.9** — imported by Final Cut Pro and (with more limited multicam handling) by
DaVinci Resolve. Premiere does not import FCPXML well; use FCP or Resolve. The version is a single
constant (`FCPXML_VERSION`) if you need to bump it.

## Honest caveats

- **FCP import is the real validator.** FCPXML is finicky about formats/timing; this is a first
  version. The very first import may surface a tweak (a frame-rate edge case, a path that needs
  relinking). Bring back whatever FCP says and we iterate.
- **Timestamp alignment is coarse** (±seconds), by design — see *honest scope* above.
- **Mixed frame rates** are conformed to one sequence timebase (the most common among the clips, or
  `--fps`); expect sub-frame rounding across cameras until per-angle sync in FCP.
- It **reads** the registry and your output folders; it never writes to them (the shoot's output
  drive must be mounted so `MULTICAM/*.json` is readable).
