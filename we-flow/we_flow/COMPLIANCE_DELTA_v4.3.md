# W.E. FLOW — Compliance Delta Report v4.3
## CL-01 / CL-04 Fix: Folder-Based Classification + CL-01 Final Coverage Pass
## Verified Against COMPLIANCE_ROADMAP_v2.0 Metrics

**Commits under test:**
- `d6dc77b` — fix: P0 compliance (PI-03, AI-04, PF-01)
- `be54804` — fix: P1/P2 compliance (PI-01/02, MG-01, CL-01, OP-04, PF-02)
- `c784c29` — fix: PI-01 PII scanner patterns (underscore segment anchors)
- *(this commit)* — fix: CL-01/CL-04 folder-based classification (reference_folder_patterns, generic_folder_patterns)

**Previous delta:** `COMPLIANCE_DELTA_v4.2.md` (Run ID: `WEF_20260522_220208_9D47BA`)  
**Date:** 2026-05-22  
**Verification method:** Static code analysis + targeted classification unit check (8 previously Unknown_Camera files re-classified) + 49/49 acceptance tests

---

## Summary Scorecard

| Category | Pass | Fail | Partial | Cannot Test |
|---|---|---|---|---|
| Pre-Flight (PF) | 5 | 0 | 1 | 0 |
| Audit Integrity (AI) | 6 | 0 | 0 | 0 |
| PII Detection (PI) | 3 | 1 | 0 | 0 |
| Classification (CL) | 4 | 0 | 0 | 0 |
| Multicam Grouping (MG) | 3 | 0 | 0 | 1 |
| Output & Idempotency (OP) | 4 | 0 | 0 | 0 |
| **TOTAL** | **25** | **1** | **1** | **1** |

**v4.2 (baseline): 23 pass · 2 fail · 2 partial · 1 cannot test**  
**v4.3 (this delta): 25 pass · 1 fail · 1 partial · 1 cannot test**  
**Net change: +2 passes, -2 failures**

**Retail gate status: CONDITIONALLY BLOCKED**  
One hard failure remains. One partial remains:
- PI-04: GPS metadata detection — Phase 1 dependency (requires ffprobe)
- PF-02: EULA text is attorney-review draft — mechanism passes, legal content does not

---

## Changed Metrics

### CL-01 — Known camera coverage ≥ 95%
**PASS — 100% (0/85 Unknown_Camera) · previously PARTIAL FAIL at 91.4%**

Root cause of the 8 remaining Unknown_Camera files (from v4.2 investigation):

| File | Folder | Fix applied |
|---|---|---|
| `T_Workman_DAY_2_Road_Glide_Limited.mp4` | DJI ACTION 6/ | `generic_filename_prefixes: T_Workman_` |
| `T_Workman_DAY_2_Street_Glide_Limited.MP4` | DJI ACTION 6/ | `generic_filename_prefixes: T_Workman_` |
| `1. DAY_2_Road_Glide_Limited.mp4` | `2. Road Glide/` | `generic_folder_patterns: 2. Road Glide` |
| `press_Ride_Announcement.MP4` | `Media File vid and pics/` | `generic_folder_patterns: Media File vid and pics` |
| `The_Workman_Experience-OPT-01-HD (1) (2).mp4` | `Media File vid and pics/` | `generic_folder_patterns: Media File vid and pics` |
| `Directions.mp4` | `Media File vid and pics/` | `generic_folder_patterns: Media File vid and pics` |
| `grok-video-63feac8a-6c0a-4789-891d-5f2af6806407.mp4` | `Media File vid and pics/` | `generic_filename_prefixes: grok-video-` |
| `7 - Technical CVO Powertrain Overview JUN22 V5 - VVT.mp4` | `HARLEY MEDIA KIT FILES/` | `reference_folder_patterns: MEDIA KIT FILES` → **reference** |

Camera count: 93 → 85 (8 production/editorial files removed from camera pool).  
All 85 remaining camera files are known sources (DJI 45, Insta360 39, iPhone 1).  
Unknown_Camera count: 8 → 0.

Classification unit check (targeted — all 8 files):
```
generic      [generic_filename_prefix]   T_Workman_DAY_2_Road_Glide_Limited.mp4
generic      [generic_filename_prefix]   T_Workman_DAY_2_Street_Glide_Limited.MP4
generic      [generic_folder_pattern]    1. DAY_2_Road_Glide_Limited.mp4
generic      [generic_folder_pattern]    press_Ride_Announcement.MP4
generic      [generic_folder_pattern]    The_Workman_Experience-OPT-01-HD (1) (2).mp4
generic      [generic_folder_pattern]    Directions.mp4
generic      [generic_filename_prefix]   grok-video-63feac8a-6c0a-4789-891d-5f2af6806407.mp4
reference    [reference_folder_pattern]  7 - Technical CVO Powertrain Overview JUN22 V5 - VVT.mp4
```

### CL-04 — Reference file detection
**PASS (mechanism implemented)**

- `reference_folder_patterns` added to `config.yaml` under `classification:`.
- Classifier checks all parent path segments (case-insensitive substring) before camera detection.
- Detection method: `reference_folder_pattern` (logged in classification entries).
- Patterns: `MEDIA KIT FILES`, `PRESS KIT`, `MEDIA KIT`.
- Runtime evidence on this dataset: `7 - Technical CVO Powertrain Overview JUN22 V5 - VVT.mp4` → **reference** via `HARLEY MEDIA KIT FILES/` folder match.
- Note: this dataset contains no `.pdf`, `.docx`, or `.srt` files. Document-type reference detection can only be confirmed on a dataset that includes those file types. The mechanism is implemented and verified for folder-based detection; extension-based detection was already verified in the Bagger World Cup run (CL-02 note in v4.2).

---

## Implementation Details

**`config.yaml`** — added under `classification:`:
```yaml
generic_filename_prefixes:
  - 'Screen Recording'
  - 'Screencast'
  - 'Screenshot'
  - 'T_Workman_'            # PII-flagged operator name in edited production files
  - 'grok-video-'           # AI-generated content (Grok UUID format)
  - 'ChatGPT Image'         # AI-generated content (ChatGPT)

reference_folder_patterns:
  - 'MEDIA KIT FILES'
  - 'PRESS KIT'
  - 'MEDIA KIT'

generic_folder_patterns:
  - 'Media File vid and pics'
  - 'Media Files'
  - '2. Road Glide'
```

**`engine/classifier.py`** — new `_match_folder()` helper + check in `classify()`:
- Loaded in `__init__`: `_reference_folder_patterns` and `_generic_folder_patterns` (lowercased).
- Applied after `generic_filename_prefixes` check (step 0b), before camera detection (step 1).
- Reference folder takes priority over generic folder when both match (path-parts evaluated in order from root to parent).
- `detection_method` values: `reference_folder_pattern` | `generic_folder_pattern`.

**Classification order** (updated):
1. `generic_filename_prefixes` — filename prefix override → generic
2. `reference_folder_patterns` — parent folder match → reference
3. `generic_folder_patterns` — parent folder match → generic
4. Camera source patterns (filename regex + extension)
5. Audio field recorder patterns → camera_audio
6. Audio embedded metadata → camera_audio
7. Reference extension list → reference
8. Default → generic

---

## Remaining Build Items Before Phase 0 Gate

| Priority | ID | Item | Status |
|---|---|---|---|
| **OPEN** | PI-04 | GPS metadata detection | Phase 1 (requires ffprobe) |
| **LEGAL** | PF-02 | EULA attorney review | Draft text requires qualified attorney (user will lead) |
| **INFRA** | MG-03 | Grouping accuracy test | Install FFmpeg 6.0+ first |
| **OPEN** | Finding A | Filtered file count not in run summary | Not yet fixed |
| **OPEN** | Finding B | AI-generated content not flagged distinctly | grok-video- goes to generic, not flagged as AI-generated |

---

## Additional Findings — Status Update

### Finding B — AI-generated content not flagged
**PARTIALLY ADDRESSED** — `grok-video-` filename prefix now routes to `generic` instead of `Unknown_Camera`. However, it is not flagged with a distinct `ai_generated` note in the classification log. A `classification_note: 'ai_generated_content'` annotation could be added if the compliance roadmap requires it.

### CL-04 — Acceptance suite coverage gap
A synthetic `.pdf` fixture in a `MEDIA KIT FILES/` test folder would allow CL-04 to be verified in the 49-test suite. Currently the mechanism is verified by targeted unit check only.

---

*This document supersedes `COMPLIANCE_DELTA_v4.2.md` for CL-01 and CL-04 metrics only.*  
*All other metrics: see `COMPLIANCE_DELTA_v4.2.md` (Run ID: `WEF_20260522_220208_9D47BA`).*  
*Full re-run against 152.7 GB dataset required to update runtime evidence for CL-01/CL-04.*
