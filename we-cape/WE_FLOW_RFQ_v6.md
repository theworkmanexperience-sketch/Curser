# W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Request for Quotation v6.0
## Phase 0 Production Engine | Contract-Grade Specification
**The Workman Experience, LLC | May 22, 2026 | Confidential**

---

## §1. Executive Summary

The Workman Experience, LLC ("Client") seeks qualified software vendors to provide integration, deployment, and Phase 1 development services for the W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. media ingestion platform.

**Phase 0 (complete):** A production-grade deterministic media ingestion engine with 26/28 compliance metrics passing and a Phase 0 gate status of CONDITIONALLY GREEN. The reference implementation (`we_capture/`) is delivered with this RFQ. Vendors are expected to read, run, and extend this codebase — not replace it.

**Phase 1 scope (this RFQ):** Proxy generation, GPS metadata extraction, grouping accuracy validation, and run summary enhancements as defined in §14.

The engine and all associated documents are proprietary to The Workman Experience, LLC. Vendors must execute an NDA and data governance agreement before receiving benchmark datasets.

---

## §2. System Flow

```
Stage 0: Pre-flight
  → Disk space check (output drive + system drive)
  → EULA v1.0 first-run acceptance (attorney-reviewed, 15 sections)
  → PII filename scan (segment-boundary pattern matching)
  → Operator attestation (tty-guarded; CI-safe)
  → SHA-256 of input path stored in _preflight.json

Stage 1: Ingest
  → Parallel file discovery (configurable workers, default 8)
  → SHA-256 per-file (streaming, handles 50 GB+ files)
  → Optional duplicate content detection (SHA-256 comparison)

Stage 2: Timestamp Extraction
  → Level 0: filename parse (DJI, Insta360, GoPro, iPhone patterns)
  → Level 1: ffprobe creation_time (UTC from container metadata)
  → Level 2: file_stat_mtime (low confidence, flagged in logs)

Stage 3: Classification
  → Priority: generic prefixes → reference folders → generic folders
              → camera patterns → audio field recorder → reference extensions → default generic

Stage 4: Multicam Grouping
  → ±5s UTC window (§7 LOCKED default; configurable)
  → SHA-256 group IDs (deterministic across runs)
  → Per-camera UTC offset correction

Stage 5: Variant Detection
  → Indexed, suffix, and keyword patterns
  → Parent selection: largest_file | lowest_index | earliest_timestamp

Stage 6: Output
  → Locked directory structure (§10 LOCKED)
  → symlink | copy | move

Stage 7: Audit Close
  → Five log streams flushed
  → SHA-256 manifest written (_manifest.json)
```

---

## §3. System Locks

The following parameters are LOCKED and may not be changed by vendor implementation:

| Lock | Value | Section |
|---|---|---|
| Multicam grouping window | ±5 seconds (configurable, default 5) | §7 |
| Output directory structure | CAMERA/DATE/SOURCE, REFERENCES, LOGS, MULTICAM | §10 |
| Log stream count | Five streams (ingest, classification, grouping, variants, errors) | §12 |
| Group ID algorithm | SHA-256 of sorted member paths | §7 |
| `generate_proxies` default | `false` in Phase 0 | §10 |
| PII logging behavior | Hash only — plaintext PII never written to any log | §6 |
| Audit manifest | SHA-256 of all five log streams, written after every flush | §12 |

---

## §3.x Edge Case Matrix

| Case | Required Behavior |
|---|---|
| Zero-byte file | Ingested, classified by extension/pattern, logged without crash |
| Corrupt media file | Logged to errors stream with reason; pipeline continues |
| Filename with special characters (`#`, `&`, spaces, Unicode) | Processed correctly; no crash |
| File on read-only volume | Symlink created; copy/move logged as error |
| Duplicate content (SHA-256 collision) | Flagged in ingest log; second instance not re-processed |
| Output drive below minimum free space | Pre-flight blocks run with clear error message |
| System drive used as output (copy mode, input > 10 GB) | Pre-flight blocks with explicit warning |
| ffprobe not on PATH | Warning printed; multicam grouping skipped; pipeline continues |
| Re-run on same input+output | Identical index JSON; no `_1` artifact accumulation |
| Multi-day shoot spanning multiple calendar dates | Files separated by date in output structure |

---

## §4. Input Methodology

**Primary mode:** Single-folder recursive ingest. The engine traverses the input path recursively, discovers all files, and processes them as a single pipeline run.

**Excluded files:** `.DS_Store`, `Thumbs.db`, and files matching `generic_filename_prefixes` configuration entries are discovered (counted) but classified as generic. Filtered file count is logged.

**Multi-day shoots:** Files are separated by calendar date in the output structure based on their resolved timestamp (Level 0 > Level 1 > Level 2 priority).

---

## §5. Detection Priority (§5 LOCKED Fallback Chain)

Timestamp resolution order — Level 0 always attempted first:

```
Level 0 → filename parse          [confidence: high]
Level 1 → ffprobe creation_time   [confidence: high]
Level 2 → file_stat_mtime         [confidence: low — flagged in logs]
```

If Level 2 is used, the file's grouping eligibility is flagged as `low_confidence: true` in the grouping log.

---

## §6. File Classification (§6 LOCKED Priority Order)

**Camera sources (full list):**

| Source | Key Patterns | Extensions |
|---|---|---|
| DJI | `^DJI_`, `^DJI\d`, `DJI_\d{4}` | `.mp4`, `.mov`, `.jpg`, `.dng` |
| Insta360 | `^ISD_`, `^VID_`, `_00_\d+\.insv`, `^PRO_VID` | `.insv`, `.insp`, `.mp4`, `.jpg` |
| iPhone | `^IMG_\d{4}`, `^MOV_\d{4}`, `^RPReplay`, `^AAL` | `.mov`, `.mp4`, `.heic` |
| GoPro | `^GOPR\d+`, `^GP\d{6}`, `^GH\d{6}`, `^GX\d{6}`, `^GL\d{6}` | `.mp4`, `.lrv`, `.thm` |
| Sony | `^C\d{3}S\d{4}`, `^CLIP\d+`, `^M2U\d+` | `.mxf`, `.mp4`, `.mov` |
| Canon | `^MVI_\d+`, `^_MG_\d+` | `.mov`, `.mp4`, `.cr3` |
| Blackmagic | `^Blackmagic_`, `^BMPCC` | `.braw`, `.mp4`, `.mov` |
| OMSystem | `^P\d{7}`, `^PA\d{6}` | `.mov`, `.mp4`, `.orf` |

**Camera-Audio classification:** Files from field recorders (Zoom, Sound Devices MixPre, Tascam DR series) are classified as `camera_audio` — eligible for multicam association by timestamp.

**Performance SLA:** Classification throughput ≥ 50 GB/hr (novice tier), ≥ 120 GB/hr (pro tier).

---

## §7. Multicam Grouping (§7 LOCKED)

**Window:** ±5 seconds UTC (LOCKED default; operator-configurable in `config.yaml`)  
**Algorithm:** For each camera file, find all camera files from different sources within the window. Groups of ≥ 2 cameras from different sources form a multicam group.  
**Group ID:** SHA-256 of sorted member file path list — deterministic across re-runs.  
**Output:** `MULTICAM/MCG_{sha256_prefix}.json` per group.  
**Camera-Audio association:** Field recorder files within ±5s of a group are associated with the group; they do not trigger group creation on their own.

---

## §8. Variant Detection (§8 LOCKED)

**Pattern types:**
- Indexed: `filename(1).mp4`, `filename[2].mov`
- Suffix: `_v2`, `_edit`, `_final`, `_export`, `_rev1`
- Keyword: `copy`, `final`, `backup`, `duplicate` in filename

**Parent selection (configurable):** `largest_file` (default) | `lowest_index` | `earliest_timestamp`

**Option B orphan logic:** A variant file with no surviving group members is promoted to standalone, not discarded.

---

## §9. Audio Classification

Field recorder detection uses filename prefix patterns (configurable):

| Pattern | Device |
|---|---|
| `^ZOOM\d*`, `^ZH\d` | Zoom H4n, H5, H6, H8 |
| `^SD_\d+`, `^F\d+_\d+` | Sound Devices MixPre series |
| `^TASCAM_`, `^DR\d+_` | Tascam DR series |

Default audio files (no prefix match) are classified as `generic` unless ffprobe detects `codec_type=audio`, in which case they are classified as `camera_audio`.

---

## §10. Output Structure (§10 LOCKED)

See §2 Stage 6 and `WE_FLOW_IMPLEMENTATION_PACKAGE_v6.md §5` for full tree.

Key constraints:
- `PROXIES/` directory created empty in Phase 0 (reserved for Phase 1)
- `REFERENCES/` at project root (not inside date folders)
- All five log streams in `LOGS/`
- `{run_id}_index.json` at project root — single-file machine-readable summary

---

## §11. Metadata Schema

**Index JSON (`{run_id}_index.json`):**

```json
{
  "run_id": "WEF_20260304_143022_A1B2C3",
  "input_path_hash": "sha256:...",
  "started_at": "2026-03-04T14:30:22Z",
  "completed_at": "2026-03-04T14:42:51Z",
  "files_discovered": 178,
  "files_processed": 171,
  "files_filtered": 7,
  "camera_files": 80,
  "generic_files": 90,
  "reference_files": 1,
  "error_files": 4,
  "groups_formed": 0,
  "variant_groups": 4,
  "throughput_gb_hr": 712
}
```

**Multicam group JSON (`MCG_{sha256}.json`):**

```json
{
  "group_id": "MCG_4a7f2b1c",
  "formed_at": "...",
  "window_seconds": 5,
  "members": [
    {"path_hash": "sha256:...", "source": "DJI", "timestamp": "2026-03-04T15:04:04Z", "confidence": "high"},
    {"path_hash": "sha256:...", "source": "Insta360", "timestamp": "2026-03-04T15:04:07Z", "confidence": "high"}
  ]
}
```

---

## §12. Logging (§12 LOCKED — Five Mandatory Streams)

| Stream | Content |
|---|---|
| `_ingest.json` | Every file: path hash, size, mtime, SHA-256 content hash (if enabled) |
| `_classification.json` | Every file: classification, camera_source, detection_method, file_size |
| `_grouping.json` | Groups formed, members, confidence; ungrouped camera files with reason |
| `_variants.json` | Variant groups, parent selection rationale, orphan promotion events |
| `_errors.json` | Every error: path hash, stage, error_type, message |
| `_manifest.json` | SHA-256 of each of the five streams above (tamper evidence) |

All path fields contain SHA-256 hashes of the full path string, not plaintext paths.

---

## §13. Edge Case Handling

All edge cases from §3.x must be handled without crash. Full test coverage in `test_idempotency.py` (11 cases) and `test_classifier.py` (7 cases).

---

## §14. Phase 1 Scope (This RFQ)

| ID | Item | Specification |
|---|---|---|
| P1-1 | **Proxy generation** | H.264, 720p, 1–2 Mbps per `{basename}_proxy.mp4`. Output to `PROXIES/` within date folder. FFmpeg temp files securely deleted after transcode. Pre-flight checks output drive space before transcode begins. Controlled by `proxies.generate_proxies: true` in config. |
| P1-2 | **GPS metadata extraction** | Parse DJI `CAM meta` binary telemetry stream (stream 2 in MP4 container). Standard ffprobe format tags do not expose this data. Requires ExifTool, DJI SDK, or custom KLVE/DJI atom parser. On detection: pre-flight warning printed with filename hash (never plaintext); GPS coordinates stored in classification log as hashed value only. |
| P1-3 | **Grouping accuracy validation** | Validate MG-03 (≥ 95% grouping accuracy) using a simultaneous-recording dataset. Bagger World Cup dataset or controlled test shoot. Provide ground-truth manifest in `benchmark_manifest` format. |
| P1-4 | **Run summary enhancements** | (a) Surface `files_filtered` count in run summary and index JSON. (b) Add `classification_note: ai_generated_content` to classification log entries for `grok-video-*` and similar AI-generated file patterns. |

---

## §15. Technical Stack

| Component | Specification |
|---|---|
| Language | Python 3.9+ |
| Runtime dependencies | `pyyaml` (runtime); `ffprobe` (multicam grouping) |
| Media processing | FFmpeg ≥ 4.4.6 (MacPorts) or ≥ 6.0 (Homebrew) |
| Platform | macOS 14+ and Ubuntu 22.04 LTS |
| Concurrency | `concurrent.futures.ThreadPoolExecutor` |
| Hashing | `hashlib.sha256` (streaming, 64 MB chunks) |
| Configuration | YAML (`config.yaml`) — no database, no external service |

**No cloud dependencies in Phase 0 or Phase 1.** The engine is fully air-gap capable.

---

## §16. Security Requirements

- PII filenames hashed in all logs — plaintext never written
- GPS coordinates hashed in all logs — plaintext never written
- EULA acceptance stored locally (`~/.weflow/`) — not transmitted
- Temp files securely deleted after each stage
- No network calls in Phase 0 or Phase 1
- No telemetry, no analytics, no callbacks

---

## §17. Acceptance Criteria

### Test 1 — Classification Accuracy

**Pass condition:** All 49 acceptance tests pass (`python run_tests.py`).  
**Evidence:** `run_tests.py` output attached showing 49/49.  
**Additional:** CL-01 metric ≥ 95% on Client benchmark dataset (all known camera sources classified correctly).

### Test 2 — Variant Detection

**Pass condition:** All 4 variant test cases pass.  
**Evidence:** `test_variants.py` output.

### Test 3 — Multicam Grouping

**Pass condition:** All 5 grouping test cases pass. MG-03 ≥ 95% on simultaneous-recording dataset (Phase 1).  
**Evidence:** `test_grouper.py` output + grouping log from benchmark run.

### Test 4 — Output Structure

**Pass condition:** All 15 output test cases pass. Directory tree matches §10 LOCKED specification exactly.  
**Evidence:** `test_output.py` output + `tree` output from benchmark run.

### Test 5 — Comprehensive Logging

**Pass condition:** All five log streams exist after every run. SHA-256 manifest verifies on re-check.  
**Evidence:** `LOGS/` directory listing + manifest verification command output.

### Test 6 — Idempotency & Robustness

**Pass condition:** Re-running on same input + output produces byte-identical `{run_id}_index.json`. No `_1` suffix artifacts.  
**Evidence:** `diff` output of two consecutive index JSON files (must be empty).

### Test 7 — Performance

**Pass condition:** 
- Novice tier: ≥ 50 GB/hr on 100 GB dataset, ≤ 16 GB memory
- Pro tier: ≥ 120 GB/hr on 500 GB dataset, ≤ 32 GB memory
- Studio tier: ≥ 80 GB/hr on 1 TB dataset, ≤ 64 GB memory  
**Evidence:** Wall time and memory peak from benchmark run logs.

### Test 8 — Compliance Metrics (Phase 1)

**Pass condition:** All PF-01 through OP-04 metrics pass (28/28 with PI-04 and MG-03 resolved).  
**Evidence:** Compliance delta document in `COMPLIANCE_DELTA` format, run ID attached.

---

## §18. Deliverables

| Deliverable | Milestone | Format |
|---|---|---|
| Phase 1 engine code | Milestone 1 | Git branch against reference implementation |
| 49/49 acceptance tests passing (with Phase 1 additions) | Milestone 1 | `run_tests.py` output |
| Compliance delta document (28/28) | Milestone 1 | `COMPLIANCE_DELTA_vX.X.md` format |
| GPS extraction implementation + PIA | Milestone 2 | Code + completed PIA template |
| Proxy generation implementation + PIA | Milestone 2 | Code + completed PIA template |
| MG-03 validation dataset + ground-truth manifest | Milestone 2 | `benchmark_manifest_*.json` format |
| Full stress test on Client benchmark dataset | Final | Run logs + compliance delta |
| macOS code signing + Apple notarization | Final | Notarization ticket |
| Privacy Policy, ToS, DPA template | Final | Attorney-reviewed documents |

---

## §19. Payment Terms

| Milestone | Trigger | Amount |
|---|---|---|
| Milestone 1 | 49/49 tests passing; compliance delta showing 28/28; code delivered to Client repo | 30% |
| Milestone 2 | GPS extraction, proxy generation, MG-03 validation complete; PIAs submitted | 40% |
| Final | Full stress test pass; code signing; attorney-reviewed legal documents delivered | 30% |

Total contract value: per vendor quote.

---

## §20. Data Governance

All vendor personnel must execute the W.E. C.A.P.E. CAPTURE Data Governance Agreement before receiving access to benchmark datasets. Key obligations:

- Benchmark datasets are **Confidential** — delete within 30 days of contract close
- PII content in test datasets is authorized for compliance testing only (releases on file)
- No benchmark content may be used for model training, public demonstration, or any purpose outside this engagement
- Full obligations: `DATA_GOVERNANCE.md`

---

## Appendix A: Compliance Status at RFQ Issue

| Metric | Status | Notes |
|---|---|---|
| PF-01–06 Pre-Flight | **6/6 PASS** | Attestation, EULA, disk checks, path hashing |
| AI-01–06 Audit Integrity | **6/6 PASS** | Coverage, completeness, tamper-evidence |
| PI-01–03 PII Detection | **3/3 PASS** | Scan, warning, hash-only logging |
| PI-04 GPS Extraction | **FAIL** | Phase 1 item — CAM meta binary parser needed |
| CL-01–04 Classification | **4/4 PASS** | 100% known source coverage on benchmark |
| MG-01–02, MG-04 Grouping | **3/3 PASS** | Mechanism proven; determinism verified |
| MG-03 Grouping Accuracy | **CANNOT TEST** | Phase 1 dataset needed |
| OP-01–04 Output | **4/4 PASS** | Idempotency, no system writes, temp cleanup |
| **TOTAL** | **26/28** | Gate: CONDITIONALLY GREEN |

---

## Appendix B: Benchmark Datasets

| Dataset | Size | Files | Camera Sources | Status |
|---|---|---|---|---|
| Harley Press Ride, March 4, 2026 | 152.7 GB | 178 | 7 (DJI, Insta360, iPhone, + audio) | **Primary stress test dataset** |
| Bagger World Cup, March 29, 2026 | TBD | TBD | TBD | Phase 1 grouping accuracy candidate |

Ground-truth manifest format: `benchmark_manifest_example.json` (included in package).

Benchmark access requires executed Data Governance Agreement. Contact: The Workman Experience, LLC.

---

## Appendix C: Sample config.yaml

See `we_capture/config.yaml` — authoritative configuration with EULA v1.0 text embedded as YAML literal block scalar.

---

## Appendix D: Change Log

| Version | Date | Changes |
|---|---|---|
| v4.1 | 2026-05-22 | Initial RFQ — baseline 15/28 compliance |
| v4.2 | 2026-05-22 | PI-03, AI-04, PF-01, PI-01/02, MG-01, OP-04, PF-02 partial — 23/28 |
| v4.3 | 2026-05-22 | CL-01/CL-04 code analysis — 25/28 |
| v4.4 | 2026-05-22 | CL-01/CL-04 runtime confirmed, folder classification — 25/28 |
| v4.5 | 2026-05-22 | ffprobe 4.4.6 installed, MG-01 confirmed — 25/28 |
| v4.6 | 2026-05-22 | PF-02 EULA v1.0 attorney-reviewed — 26/28, gate CONDITIONALLY GREEN |
| **v6.0** | **2026-05-22** | **Phase 1 scope defined; full implementation package issued** |

---

*W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. RFQ v6.0*  
*The Workman Experience, LLC | May 2026 | Confidential*  
*EULA v1.0 reviewed by Valerie Workman, Esq. — effective 2026-05-22*  
*Compliance: 26/28 | Gate: CONDITIONALLY GREEN | Tests: 49/49*
