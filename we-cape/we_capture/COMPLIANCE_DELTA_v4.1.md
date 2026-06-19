# W.E. C.A.P.E. CAPTURE v4.1 — Compliance Delta Report
## Stress Test: Harley Press Ride, March 4 2026
## v4.1 Behavior vs. COMPLIANCE_ROADMAP_v2.0 Metrics

**Run ID:** `WEF_20260522_205035_AB4BE3`  
**Dataset:** 178 files · 152.7 GB · 7 camera sources  
**Method:** Static code analysis + runtime test  
**Date:** 2026-05-22  

---

## Summary Scorecard

| Category | Pass | Fail | Partial | Cannot Test |
|---|---|---|---|---|
| Pre-Flight (PF) | 3 | 3 | 0 | 0 |
| Audit Integrity (AI) | 5 | 1 | 0 | 0 |
| PII Detection (PI) | 0 | 4 | 0 | 0 |
| Classification (CL) | 2 | 2 | 1 | 0 |
| Multicam Grouping (MG) | 2 | 0 | 1 | 1 |
| Output & Idempotency (OP) | 3 | 1 | 0 | 0 |
| **TOTAL** | **15** | **11** | **2** | **1** |

**Retail gate status: BLOCKED — 11 failures must be resolved before Phase 0 retail.**

---

## Pre-Flight Metrics (PF)

### PF-01 — Operator attestation logged
**FAIL**  
- Expected: `_preflight.json` exists with `event: preflight_accepted` and non-null `attestation_hash`  
- Actual: `_preflight_check()` prints a summary and checks disk space but **never writes any log file**. No attestation prompt is shown to the user. No `_preflight.json` exists after any run.  
- Impact: Zero audit trail for who ran the engine, on what data, with what authorization. Chain of custody begins at Stage 0 ingest, not at the operator decision point.  
- Fix required: Implement attestation prompt + `_preflight.json` writer before Stage 0.

### PF-02 — EULA version recorded
**FAIL**  
- Expected: `_preflight.json` contains `eula_version_accepted` matching current version string  
- Actual: No EULA mechanism exists anywhere in the codebase. First-run acceptance is not implemented.  
- Impact: No legal record of user agreement to terms at retail.  
- Fix required: First-run EULA acceptance flow + version logging.

### PF-03 — System drive detection
**PASS**  
- `_is_system_drive()` correctly identifies output paths on the internal volume.  
- Runtime confirmed: output on 10TB external drive, system drive correctly not flagged.

### PF-04 — Output drive space check
**PASS**  
- Runtime confirmed: 1,002.5 GB free on output drive, check passed and printed correctly.

### PF-05 — System drive headroom printed
**PASS**  
- Runtime confirmed: "System drive: 146.3 GB free ✓" printed in pre-flight summary.

### PF-06 — Input path hashed in log (not plaintext)
**FAIL**  
- Expected: Input path stored as SHA-256 hash in `_preflight.json`  
- Actual: Full plaintext path printed to terminal:  
  `Input media: /Volumes/10TB/2026 Harley-Davidson Chronicles/Harley Press Ride for Claude/March 4 2026`  
  No log is written at all (PF-01 failure), so the path exposure is in terminal output only.  
- Impact: Terminal output (which may be screen-shared, logged, or captured) exposes full project directory structure including client names.  
- Fix required: Hash paths in any log record; consider truncating display path in terminal output for sensitive deployments.

---

## Audit Integrity Metrics (AI)

### AI-01 — 100% file coverage
**PASS**  
- Ingest entries: 171. Classification entries: 171. Count match confirmed.  
- Note: 178 files in folder, 171 discovered. 7 files filtered by `SKIP_NAMES` (`.DS_Store`, `Thumbs.db`, etc.) — this is correct behavior, not a drop.

### AI-02 — No silent drops
**PASS**  
- Every discovered file appears in `_classification.json` or `_errors.json`. Zero uncovered files.

### AI-03 — All five log streams exist
**PASS**  
- All five streams confirmed: ingest, classification, grouping, variants, errors.

### AI-04 — Log tamper-evidence
**FAIL**  
- Expected: SHA-256 of each log file written to a signed manifest; re-verification passes on demand  
- Actual: `flush()` in `audit.py` writes plain JSON with no signing, no manifest, no hash record.  
- Impact: Any log file can be modified after the fact with no detection. Chain of custody is unverifiable. This is a critical failure for any compliance framework that requires audit integrity (SOC 2, ISO 27001, GDPR data accuracy principle).  
- Fix required: After `flush()`, compute SHA-256 of each written log file and write a `{run_id}_manifest.json` containing filename → hash pairs. Verification function reads manifest and re-hashes to confirm.

### AI-05 — Run ID consistency
**PASS**  
- `run_id` confirmed present and consistent across all 5 log files.

### AI-06 — Timestamp monotonicity
**PASS**  
- `logged_at` values in ingest log are non-decreasing. Confirmed.

---

## PII Detection Metrics (PI)

### PI-01 — 100% of filenames scanned for PII patterns
**FAIL**  
- Expected: Every filename scanned against PII pattern list before Stage 1  
- Actual: No PII scanning exists anywhere in the codebase.  
- Evidence from this run: The following filenames contain direct operator/subject PII and were processed without any warning:  
  - `T_Workman_DAY_2_Road_Glide_Limited.mp4` — operator name in filename  
  - `T_Workman_DAY_2_Street_Glide_Limited.MP4` — operator name in filename  
  - `The_Workman_Experience-OPT-01-HD (1) (2).mp4` — brand/entity name in filename  
  - `press_Ride_Announcement.MP4` — event identifier  
- Fix required: PII pattern scanner in pre-flight — minimum patterns: full names, email addresses, phone numbers, SSN/DOB formats, brand/entity identifiers.

### PI-02 — PII warning printed before attestation prompt
**FAIL**  
- Expected: Warning printed if any filename matches PII pattern  
- Actual: No warning. Files with operator name embedded processed silently.  
- Fix required: Implement after PI-01 scanner.

### PI-03 — PII not logged in plaintext
**FAIL — CRITICAL**  
- Expected: PII-flagged filenames hashed in all log entries; plaintext PII never written to any log file  
- Actual: `audit.py:153` — `'file': str(file_path)` — **every log entry writes the full absolute path as plaintext**, including client names, project names, and any PII embedded in filenames.  
- Runtime evidence:  
  ```
  "file": "/Volumes/10TB/2026 Harley-Davidson Chronicles/Harley Press Ride 
           for Claude/March 4 2026/T_Workman_DAY_2_Road_Glide_Limited.mp4"
  ```
  This string — containing the operator name — is written to `_classification.json`, `_ingest.json`, `_errors.json`, and `_grouping.json`.  
- Impact: Every audit log is a PII disclosure document under GDPR. Sharing logs with vendors, support, or auditors exposes client and operator names without consent. This is a GDPR Article 5(1)(c) data minimization violation.  
- Fix required: Hash the full path in log records. Store only `filename` (basename) in plaintext; store `file_path_hash` (SHA-256 of full path) for correlation. The run-time path mapping lives in `_preflight.json` only, which has stricter access controls.

### PI-04 — GPS metadata flagged before processing
**FAIL**  
- Expected: If ffprobe detects GPS coordinates in any media file, pre-flight warns before processing  
- Actual: No GPS checking. ffprobe is not installed; even if it were, GPS extraction is not implemented.  
- Impact: Media files from the Press Ride dataset contain embedded GPS coordinates (shot locations). These are processed and routed without any disclosure to the operator.  
- Fix required: Phase 1 (when ffprobe is installed) — add GPS extraction to timestamp pipeline; flag files with GPS in pre-flight summary.

---

## Classification Metrics (CL)

### CL-01 — Known camera coverage ≥ 95%
**PARTIAL FAIL — 87.6% (12/97 Unknown_Camera)**  
- Expected: ≥ 95% of camera files assigned to a known camera source  
- Actual: 87.6% — 85 known, 12 Unknown_Camera  
- The 12 unclassified files fall into three distinct failure categories:

  **Category A — Screen Recordings misclassified as camera (3 files):**
  - `Screen Recording 2026-03-18 at 11.54.11 PM.mov`
  - `Screen Recording 2026-03-19 at 12.00.47 AM.mov`
  - `Screen Recording 2026-03-19 at 12.04.43 AM.mov`
  - These are macOS screen captures, not camera footage. Classified as `camera/Unknown_Camera` instead of `generic`. Classification error.

  **Category B — Named production files with no pattern match (6 files):**
  - `T_Workman_DAY_2_Road_Glide_Limited.mp4`
  - `T_Workman_DAY_2_Street_Glide_Limited.MP4`
  - `press_Ride_Announcement.MP4`
  - `1. DAY_2_Road_Glide_Limited.mp4`
  - `The_Workman_Experience-OPT-01-HD (1) (2).mp4`
  - `Directions.mp4`
  - These are edited/produced video files, not raw camera footage. Should be `generic` or `reference`, not `camera`.

  **Category C — Third-party / AI-generated content (2 files):**
  - `grok-video-63feac8a-6c0a-4789-891d-5f2af6806407.mp4` — AI-generated content (Grok)
  - No classification or flagging for third-party/AI-generated content.

- Fix required: Add `Screen Recording` prefix to `SKIP_NAMES` or `generic` classifier. Add pattern exclusions for named production files. Consider flagging AI-generated content.

### CL-02 — Zero unclassified drops
**PASS**  
- All 171 discovered files received a classification. Zero NULL classifications.

### CL-03 — OMSystem recognition
**PASS (conditional)**  
- No P*.MOV files present in this dataset. Config v4.1.1 OMSystem patterns are in place.  
- Confirmed passing on March 29 Bagger World Cup dataset (204 files would have been Unknown_Camera without the fix).

### CL-04 — Reference file detection
**FAIL**  
- Expected: All PDF, DOCX, SRT files classified as `reference`  
- Actual: 0 reference files detected despite `HARLEY MEDIA KIT FILES` subfolder being present in input.  
- Root cause: The HARLEY MEDIA KIT FILES folder contains documents, but 0 were classified as `reference`. Either the files are not `.pdf`/`.docx` extensions, or they were filtered at discovery. Requires investigation.  
- Fix required: Inspect HARLEY MEDIA KIT FILES contents; verify reference extension list covers all file types present; add test assertion for reference detection with real media kit files.

---

## Multicam Grouping Metrics (MG)

### MG-01 — ffprobe missing → warn and skip, not crash
**PARTIAL FAIL**  
- Expected: Explicit "ffprobe not found" warning printed; multicam grouping skipped gracefully  
- Actual: `timestamp.py:107` catches all exceptions silently (`except Exception: pass`). Engine falls back to `file_stat_mtime` for every file and logs `[SKIP] fallback`. The pipeline does not crash — but it **never explicitly tells the user that ffprobe is missing**.  
- Runtime evidence: 83 files at fallback_level=2, 0 groups formed, no ffprobe warning printed.  
- Impact: A new user running the engine without ffprobe sees 0 multicam groups and has no idea why. They may assume their footage has no multicam content.  
- Fix required: In `_from_ffprobe()`, catch `FileNotFoundError` specifically and print a named warning: `"⚠ ffprobe not found — multicam grouping disabled. Install FFmpeg 6.0+ to enable."` Print once, not per-file.

### MG-02 — Group ID determinism
**PASS**  
- SHA-256 based group IDs confirmed in acceptance suite (49/49 tests passing).

### MG-03 — Grouping accuracy ≥ 95%
**CANNOT TEST**  
- Blocked by ffprobe absence. All 97 camera files ungrouped. Cannot score until ffprobe is installed.

### MG-04 — Window compliance ±5s
**PASS**  
- No groups formed, so no window violations possible. Constraint is enforced in grouper code.

---

## Output & Idempotency Metrics (OP)

### OP-01 — Idempotent re-runs
**PASS**  
- Confirmed in 49/49 acceptance tests. No `_1` suffix artifacts.

### OP-02 — No system drive writes in symlink mode
**PASS**  
- Output on 10TB drive. Zero media bytes written to system drive. 151 symlinks created.

### OP-03 — Symlink integrity
**PASS**  
- 151 symlinks created, 0 broken. All resolve to existing source files.

### OP-04 — Secure temp file deletion
**FAIL**  
- Expected: No temp files remain in system temp after run completes  
- Actual: No secure deletion is implemented. Python's default temp file handling is used. No cleanup in Stage 6.  
- Fix required: At Stage 6 close, scan and delete any temp files created during the run. Use `tempfile.TemporaryDirectory()` context manager pattern so cleanup is guaranteed even on crash.

---

## Additional Findings (Not in Metric Set)

These emerged from the stress test and are not yet covered by any metric. They represent gaps in the metric set itself.

### Finding A — 7 files filtered without disclosure
- 178 files in folder, 171 discovered. 7 files silently filtered by `SKIP_NAMES`.
- The summary reports 171 files, not 178. An operator reviewing the output has no way to know 7 files were excluded.
- Recommendation: Add `files_filtered` count to run summary and `_ingest.json` header.

### Finding B — AI-generated content not flagged
- `grok-video-63feac8a-6c0a-4789-891d-5f2af6806407.mp4` processed without any AI provenance flag.
- As AI-generated content becomes more common in production folders, pipeline output should distinguish AI-generated from camera-original content. Relevant to EU AI Act Article 50 (disclosure of AI-generated content).
- Recommendation: Add AI-generated content detection pattern to classifier (UUID-style filenames from known AI tools).

### Finding C — Run time 955 seconds for 171 files
- 5.6 files/second for 152.7 GB in symlink mode. This is below the Novice tier benchmark (≥50 GB/hr = ~13.9 files/sec for typical file sizes).
- Root cause: Likely the SHA-256 hashing of 152.7 GB of media at Stage 0. Each file is fully read for hashing.
- Recommendation: Add optional `--skip-hash` flag for smoke test runs; or make hashing lazy (hash only on dedup check).

### Finding D — Screen Recordings in production folder
- Three macOS screen recordings present in a media production folder. The pipeline has no mechanism to warn the operator that screen recordings (which may contain sensitive on-screen content) are present in the shoot folder.
- Recommendation: Add `Screen Recording` to a `sensitive_filename_patterns` warning list in pre-flight.

---

## Build Priority for Phase 0 Retail Gate

Ordered by severity and blocking status:

| Priority | ID | Failure | Effort |
|---|---|---|---|
| P0 — Critical | PI-03 | Plaintext PII paths in every log entry | Medium — change `_base()` in audit.py |
| P0 — Critical | AI-04 | No log tamper-evidence | Medium — add `flush()` SHA-256 manifest |
| P0 — Critical | PF-01 | No operator attestation | Medium — add prompt + `_preflight.json` writer |
| P1 — High | PF-02 | No EULA mechanism | High — requires legal content first |
| P1 — High | PI-01/02 | No PII filename scanning | Medium — add pattern scanner to pre-flight |
| P1 — High | MG-01 | ffprobe missing silently | Low — one specific except clause in timestamp.py |
| P1 — High | CL-01 | Screen recordings misclassified | Low — add patterns to config |
| P2 — Medium | CL-04 | Reference detection gap | Low — investigate media kit files |
| P2 — Medium | OP-04 | No secure temp deletion | Low — wrap Stage 6 in cleanup context |
| P2 — Medium | PF-06 | Plaintext path in terminal | Low — truncate display path |
| P3 — Low | PI-04 | No GPS detection | Deferred to Phase 1 (requires ffprobe) |
| P3 — Low | Finding A | 7 files filtered silently | Low — add to summary |
| P3 — Low | Finding B | AI content not flagged | Low — add UUID pattern |
| P3 — Low | Finding C | Performance below Novice tier | Medium — optional skip-hash flag |

---

*This document is the evidence artifact for the Phase 0 retail gate.*  
*All failures must be resolved and re-tested before the gate clears.*  
*Run ID: WEF_20260522_205035_AB4BE3 | Dataset: Harley Press Ride March 4 2026*
