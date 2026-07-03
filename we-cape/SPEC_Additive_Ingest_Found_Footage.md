# SPEC — Additive Ingest / Found-Footage
## Draft v0.1 · 2026-07-01 · status: DESIGN (build starting on stills)

## 1. Purpose

Handle the real-world case: **after a shoot is processed, more files turn up** — a forgotten card,
a second disk, a collaborator's drive — often in **mixed / unknown formats**. They must be:

- **ingested into the intelligence** (registry: hashed, classified, lineage-tracked),
- **merged into the existing project** (registry + output + FCPXML), not a fresh silo,
- and handled by **format** (video, image, audio, unknown) — with unknowns surfaced, never dropped.

## 2. The core principle: additive, not parallel

This is **not a second pipeline.** CAPTURE's existing properties already make late-found footage a
first-class case:

- **Registry is SHA-keyed + non-destructive (P5).** Re-ingesting merges: new content added,
  existing preserved (COALESCE upsert), nothing overwritten or duplicated.
- **CAPTURE is idempotent.** Already-processed files skip on SHA match (proxy transcode skipped),
  so "add the new stuff" ≠ "redo everything" — the re-run is cheap.
- **`reconcile.py` detects** the unaccounted files (the gap) in the first place.

So the whole workflow is three existing steps:

> **reconcile (detect gap) → additive CAPTURE (ingest + merge into the same shoot) → re-export.**

## 3. The merge-vs-append rule

One decision, every time found footage arrives:

- **Merge-and-regroup (default):** add found files to the shoot's source and re-CAPTURE the
  **combined** set → new clips **group with the existing footage** (a found angle joins the
  multicams). Cheap because matched SHAs skip. **Recommended** for footage that belongs to the shoot.
- **Append-only:** process the found disk alone; its clips are added to the event as **standalone**
  (no regrouping). Faster; use when the footage is supplemental and needn't join multicam groups.

## 4. Format-coverage matrix

| Format | Handling | Status |
|--------|----------|--------|
| **Video** (camera) | classify → group → proxy → FCPXML angle / asset-clip | ✅ built |
| **iPhone video** | a camera source (`^IMG_` + `.mov/.mp4`, or an `iPhone` folder) → same as any camera | ✅ config added |
| **Image / stills** | FCPXML **image assets** in a `Stills` Keyword Collection; not in multicam/timeline logic | 🔨 building (`--stills`) |
| **Audio** (field/voice) | FCPXML audio assets (`Audio` collection); camera-audio grouping where applicable | ⏭ Phase 2 |
| **Unknown / unsupported** | **quarantine** (`_QUARANTINE/`) + **report**, never silently drop or mis-bucket | ⏭ Phase 2 (report exists via reconcile) |

## 5. Unknown / unsupported formats — the honesty rule

- **Quarantine, don't guess.** Move unrecognized files to `_QUARANTINE/` (the archive engine already
  quarantines partials/corrupts — extend it to "unrecognized extension").
- **Surface loudly.** Both `reconcile.py` and the Production Health Report state it plainly:
  > "6 files of unsupported type `.xyz` — not processed. Quarantined to `_QUARANTINE/`. Review manually."
- **Never** classify an unknown as `generic` by default in a way that hides it — the creator must be
  told the platform doesn't recognize it. (P3 auditability, honesty.)

## 6. Stills — the first build (this week)

- Export flag: **`--stills <folder>`** (repeatable) on `fcpxml_export.py`.
- Each image → a still `<format>` (dimensions from `ffprobe`, no `frameDuration`) + `<asset>`
  (`hasVideo=1 hasAudio=0 duration=0s`, original media-rep) + an event `<asset-clip>` with a chosen
  placement duration (default 4s).
- **Keyword Collection `Stills`** (and `Camera: iPhone (Stills)` when an `IMG_` iPhone photo).
- **Metadata**: `<note>` with original filename + capture time (from the filename's date, else file
  mtime) + shoot. Timestamp-prefixed name so stills sort chronologically with the video.
- Stills live in the **browser** (event + `Stills` collection), so they're organized and reachable
  **without cluttering the timeline** (never auto-placed).

## 7. Provenance & verification (free with additive ingest)

- Found files are **hashed** (verified) on ingest, **classified**, and **lineage-tracked** (which
  source, when). `reconcile.py` proves afterward the disk is fully accounted for.
- The offload tool (`offload_cards.py`) is the ideal front door for a found disk too: verified
  two-copy offload → per-camera folders → additive CAPTURE.

## 8. Phasing

- **v1 (now):** image-asset support (`--stills`) + iPhone-as-camera config. Merge-and-regroup
  workflow documented; reconcile already detects gaps.
- **v2:** audio-asset support; archive-engine quarantine of unknown extensions + Health-Report/reconcile
  surfacing; a one-command "found-footage" wrapper (reconcile → additive CAPTURE → re-export).

## 9. Open decisions (for review)

1. **Still placement duration** — fixed 4s, or configurable (`fcpxml.still_duration`)? (Lean: config, default 4s.)
2. **Stills source** — `--stills <folder>` (explicit, decoupled) vs. reading images from the registry.
   (Lean: `--stills` for v1 — simplest, works even if images aren't in the registry; registry-driven later.)
3. **`_QUARANTINE` scope** — only truly-unreadable, or also "recognized-but-unsupported"? (Lean: both,
   with distinct report lines so the creator knows which.)
4. **Merge-and-regroup default** — always re-CAPTURE the combined set, or make append-only an explicit
   opt-out? (Lean: merge-and-regroup default; `--append-only` opt-out.)
