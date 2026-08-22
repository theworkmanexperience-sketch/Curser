# EXECUTION_LOG.md
## Permanent audit log — Sprint 3A

| field | value |
|---|---|
| RUN_ID | `WECAPE-AR2-SPRINT3A-20260822-114028` |
| Sprint | G3-ESS-001 Rev A (Sprint 3A), governed production run |
| Start (UTC) | 2026-08-22T11:40:28Z |
| End (UTC) | 2026-08-22T12:14:00Z |
| Total runtime | ~33.5 minutes wall clock |
| Machine (compute) | `claude` — Linux aarch64, Ubuntu 22.04.5 LTS, 4 cores, 3 GB RAM |
| Machine (repo/media host) | `ts-mac-studio-3-local` — macOS (darwin/arm64) |
| ffmpeg | 4.4.2-0ubuntu0.22.04.1 |
| python | 3.10.12 (media host) / 3.11 (analysis) · numpy 2.2.6 · Pillow 12.3.0 |
| Repository | `~/Curser` (working tree `we-cape/`) |
| Branch at launch | `main` |
| Git commit at launch | `ff0c45f77b2fb612606e1d5b8ef86641822e5e4a` |
| Repo status at launch | clean (no modified or untracked files) |
| Specification | WET-SPEC-DIE-001 v0.2 (frozen, tag `wet-spec-die-001-v0.2-frozen`) |
| Architecture | ADR-009 (ACCEPTED, Chairman 2026-08-21) |
| Completion status | **COMPLETE — stopped at completion for Executive Review** |

## Input hashes (computed by this run, first act, before any processing)

| # | input | SHA-256 | bytes |
|---|---|---|---|
| 1 | `Filmage_Editor.mp4` | `a53655fc673945a0d99dde3d5b60c9a126d8b41e4e44a7c7eedeb058ba0f47e8` | 399,320,021 |
| 2 | `Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` | `2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7` | 4,479,627 |
| 3 | `Alpha RoudUp Part 2_SRT__SRT 2_English (United States).srt` | `89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b` | 140,526 |
| 4 | `P2_LOCK_timing.json` | `e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d` | 183,116 |

Working copies of inputs 2–4 were made to `AlphaRoundUp_2026/SPRINT3A_WORK/inputs/` and hash-verified
byte-identical to the originals before use. The originals were never modified.

`P2_LOCK_timing.json` declares `source_sha256` = input 2's hash. The chain is closed at the hash level.

## Phase log

| phase | start (UTC) | finish (UTC) | outcome |
|---|---|---|---|
| Access + reconnaissance | 11:36 | 11:40 | Repo and media volume located and granted; ffmpeg/python/git verified on the media host |
| Input hashing (first act) | 11:40 | 11:41 | 4/4 hashes computed |
| ETC + FCPXML parse | 11:41 | 11:46 | 1,025 elements resolved to absolute sequence time; resolver validated 191/191 against ETC spine |
| Step 0 — timing closure | 11:46 | 11:53 | Offset = 0.000 s by two independent methods; drift CI contains zero; ledger built |
| Step 1 — DIE-V extraction | 11:47 | 12:00 | Audio envelope, 2 fps observable series, 1,616 survey frames, 258 probe frames, 57 sheets; 3/3 probes PASS |
| Step 2–3 — ESS + Conductor | 12:00 | 12:09 | Synchronization model and Conductor's Score generated |
| Step 4–5 — Validation + seed | 12:09 | 12:11 | Validation report and production seed generated |
| YAML conformance + fixes | 12:11 | 12:13 | 5/5 artifacts parse; schema conformance verified |
| Commit + push | 12:13 | 12:14 | See commit hashes below |

## Warnings encountered

1. **`Filmage_Editor.mp4` is a 320×180 proxy, not the 3840×2160 master the FCPXML describes**, and it
   carries a "Filmage Editor" trial watermark. Recorded as delta **D-24**. Every visual observation is
   capped by this; nothing in VISUAL_EVENT_REGISTRY claims detail the proxy cannot resolve. The
   Executive Team should know that richer visual events in Sprint 4 require a better proxy, not a
   better method.
2. **`P2_LOCK_timing.json` carries `timeline_offset_s: null` for all 404 connected elements** and
   references parents by non-unique clip name. The 16 audio elements' and 40 titles' absolute in/outs
   could not be read from the ETC and had to be re-derived from FCPXML nesting. Recorded as **D-08**.
3. **FCPXML asset `r95` (`NOTOR1OUS_CARAVAN_2_`) resolves to `/Volumes/10TB/…`, a volume not mounted
   for this run.** Its content could not be inspected. Recorded as **D-22**; it is the reason **D-18**
   (an audio element inside SIL-01) is escalated rather than resolved.
4. **A single fully black sampled frame at 00:35:06.** Classified `OBSERVED_BLACK_FRAME` at MEDIUM
   confidence and flagged for human inspection; at a 3.000 s grid a dip-to-black and a defect are not
   distinguishable.
5. **Background processes do not survive a shell-call boundary on the media host.** The first DIE-V
   run was killed silently between passes. All subsequent media work was re-run in foreground,
   chunked to fit the per-call time budget. No data was lost; the run was repeated from the start of
   the affected pass.
6. **`rm` is not permitted on the mounted repository**, and a stale `.git/index.lock` left by a status
   call blocked all git operations. Cleared by moving the lock to `_to_delete/index.lock.stale` inside
   the mounted folder. **That file should be deleted by hand — this run could not delete it.**

## Exceptions / stop-conditions

None triggered. All three fixture probes passed on first run, so no diagnose-and-stop was required.
Two conditions were **escalated rather than resolved**, per the no-silent-recovery constraint:

- **D-18 / SLF-01** — audio-lane element inside a mandatory-silence window, content undetermined.
- **VCONF-01/02/03** — three registry-versus-observation conflicts, registry value retained in all three.

## Governance compliance

- Music generated: **0**. Biometric operations: **0**. Sentiment inferences: **0**.
- Frozen documents modified: **none**.
- Existing registries modified: **CAPTION_REGISTRY only** (0.1.0 → 0.2.0), with the enrichment noted
  in its header, exactly as the work order permits.
- Enrichment namespaces `nie` / `mie` / `pie`: written **empty** on all 39 DIE-V events.
- Deltas logged: **25**. Deltas uncategorized: **0**.

## Artifacts produced (all reference this RUN_ID)

`STEP0_TIMING_CLOSURE.md` · `VISUAL_EVENT_REGISTRY.yaml` · `EDITORIAL_SYNCHRONIZATION.yaml` ·
`CONDUCTOR_SCORE.yaml` · `ESS_VALIDATION_REPORT.md` · `PRODUCTION_INTELLIGENCE_SEED.yaml` ·
`EXECUTION_LOG.md` (this file) · `CAPTION_REGISTRY.yaml` (enriched, in `intelligence/p2/registries/`)

Intermediate working data (frames, contact sheets, observable series, input copies) is under
`WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/` on the media volume and is **not** committed to the
repository. It is retained so any observation in this run can be re-inspected at its cited timestamp.

## Commit

Recorded below after commit; see repository history for authoritative values.
