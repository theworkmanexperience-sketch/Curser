# W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Implementation Package v6.0
## Complete Technical Build Reference
**The Workman Experience, LLC | May 22, 2026 | Confidential**

---

## 1. System Overview

W.E. C.A.P.E. CAPTURE is a deterministic, auditable media ingestion engine for professional video production. It ingests raw footage from mixed-camera shoots and produces a structured, classified project folder with five tamper-evident audit log streams.

**Design principles:** Every decision is deterministic and reproducible. The same input always produces the same output. No probabilistic classification, no ML inference, no internet dependency in Phase 0.

**Governing document:** `we_capture/COMPLIANCE_ROADMAP_v2.0.md` — all compliance controls are falsifiable tests, not assertions.

### System Flow

```
Stage 0: Pre-flight         → disk check, EULA, PII scan, attestation, drive encryption check
Stage 1: Ingest             → parallel file discovery, SHA-256, dedup flag
Stage 2: Timestamp          → ffprobe → filename parse → mtime fallback
Stage 3: Classification     → filename prefix → folder pattern → camera pattern → extension
Stage 4: Grouping           → UTC timestamp pairs within ±5s window → SHA-256 group ID
Stage 5: Variant detection  → indexed/suffix/keyword patterns → parent selection
Stage 6: Output             → locked directory structure, symlinks or copy/move
Stage 7: Audit close        → five log streams flushed, SHA-256 manifest written
```

---

## 2. Architecture

### Module Map

| Module | Section | Responsibility |
|---|---|---|
| `main.py` | CLI | Argument parsing, config load, pipeline instantiation |
| `engine/pipeline.py` | §2–4 | Orchestration, parallel ingest, pre-flight, EULA, idempotency |
| `engine/classifier.py` | §6 | File classification (8 camera sources + generic + reference) |
| `engine/timestamp.py` | §5 | Three-level timestamp fallback chain |
| `engine/grouper.py` | §7 | Deterministic multicam grouping with SHA-256 group IDs |
| `engine/variants.py` | §8 | Variant detection, parent selection, Option B orphan logic |
| `engine/output.py` | §10 | Locked output directory structure, symlink/copy/move |
| `engine/audit.py` | §12 | Five mandatory log streams + SHA-256 manifest |

### Classification Priority Order (§6 LOCKED)

```
1. generic_filename_prefixes    → Screen Recording, grok-video-, ChatGPT Image, T_Workman_, etc.
2. reference_folder_patterns    → MEDIA KIT FILES, PRESS KIT, MEDIA KIT
3. generic_folder_patterns      → Media File vid and pics, Media Files, 2. Road Glide
4. camera source patterns       → DJI, Insta360, iPhone, GoPro, Sony, Canon, Blackmagic, OMSystem
5. audio field recorder         → ZOOM, ZH, SD_, F*_*, TASCAM_, DR*_ → Camera-Audio
6. audio embedded metadata      → ffprobe codec_type=audio → Camera-Audio
7. reference extensions         → .pdf, .docx, .srt, .aaf, .edl, .fcpxml, etc.
8. default                      → generic
```

Priority 1 always wins. Folder patterns (2, 3) are evaluated before camera detection (4). Reference folder pattern takes priority over generic folder pattern.

### Timestamp Fallback Chain (§5 LOCKED)

| Level | Method | Confidence | Notes |
|---|---|---|---|
| 0 | Filename parse | high | `DJI_YYYYMMDDHHMMSS`, `VID_YYYYMMDD_HHMMSS`, `IMG_NNNN`, etc. |
| 1 | ffprobe `creation_time` | high | UTC from container metadata; requires ffprobe on PATH |
| 2 | `file_stat_mtime` | low | Filesystem modification time; unreliable across copies |

DJI and Insta360 both encode UTC in `creation_time` and local time in filenames. The engine resolves timezone-consistent pairs for multicam grouping.

### Multicam Grouping (§7 LOCKED)

- Window: ±5 seconds (configurable via `grouping.window_seconds`)
- Group ID: SHA-256 of sorted member file paths → deterministic across runs
- Per-camera UTC offset correction: `grouping.camera_offsets` (seconds, default 0)
- Graceful degradation: if ffprobe not found, warning printed, grouping skipped (not crashed)
- Output: `MULTICAM/MCG_{sha256_prefix}.json` — one file per group

### Variant Detection (§8 LOCKED)

Patterns detected:
- **Indexed:** `filename(1).mp4`, `filename[2].mov` — regex `[\(\[](\d+)[\)\]]`
- **Suffix:** `_v2`, `_edit`, `_final`, `_export`, `_rev1`
- **Keyword:** `copy`, `final`, `backup`, `duplicate` in filename

Parent selection (configurable):
- `largest_file` (default) — parent is the largest variant
- `lowest_index` — parent is the original (un-indexed) file
- `earliest_timestamp` — parent is the earliest by timestamp

Option B orphan logic: variant with no other group members is promoted to standalone (not discarded).

---

## 3. Compliance Framework

### Privacy by Design (Seven Principles)

| Principle | Implementation |
|---|---|
| Proactive | PIA required before every new feature (template in COMPLIANCE_ROADMAP_v2.0.md) |
| Default-protective | `file_operation: symlink`, `generate_proxies: false`, PII hashed by default |
| Embedded | PII detection and audit logging are in the engine, not optional flags |
| Full functionality | Privacy does not degrade capability |
| End-to-end security | Audit trail begins Stage 0; temp files deleted after Stage 6 |
| Transparent | Plain-English pre-flight output; every decision logged |
| User-centric | No jargon in user-facing terminal output |

### Audit Log Architecture

Five mandatory log streams written after every run:

| Log | Content | Compliance metric |
|---|---|---|
| `{run_id}_ingest.json` | Every discovered file, path hash, size, mtime | AI-01, AI-02 |
| `{run_id}_classification.json` | Classification, camera source, detection method | CL-01–04 |
| `{run_id}_grouping.json` | Groups formed, members, confidence; ungrouped camera files | MG-01–04 |
| `{run_id}_variants.json` | Variant groups, parent selection, orphan promotion | OP-01 |
| `{run_id}_errors.json` | Every file that could not be processed, with reason | AI-02 |

Manifest: `{run_id}_manifest.json` — SHA-256 of each of the five streams, written after flush. Tamper-evidence: any log modification after close changes the manifest hash.

### PII Controls

- **Scan:** 100% of discovered filenames scanned against PII pattern list before Stage 1
- **Warning:** PII-flagged filenames printed in pre-flight (operator sees the warning before proceeding)
- **Logging:** PII-flagged filenames hashed (SHA-256) in all log records — plaintext never written
- **Pattern matching:** Segment-boundary anchors `(?:^|_)T_Workman_(?:_|$)` — not `\b` (underscore is `\w`)

### EULA Acceptance Flow

```
First interactive run:
  1. Full EULA v1.0 text displayed in terminal (15 sections, ~1,200 words)
  2. Operator types YES
  3. Acceptance stored: ~/.weflow/eula_acceptance.json
     { "version": "1.0", "accepted_at": "...", "operator": "..." }
  4. `_preflight.json` records: eula_version_accepted: "1.0"

Subsequent runs:
  - Version silently confirmed against ~/.weflow/eula_acceptance.json
  - No re-prompt unless version changes

Non-interactive (CI/test):
  - Version recorded in _preflight.json without prompting
  - tty guard: sys.stdin.isatty() check prevents CI blocking
```

EULA version bump (e.g., `"1.0"` → `"1.1"`) triggers re-acceptance on next interactive run.

---

## 4. Configuration Reference

Full authoritative sample: `config.yaml` (Appendix C of RFQ)

```yaml
pipeline:
  file_operation: symlink          # copy | move | symlink
  enable_duplicate_content_detection: false

grouping:
  window_seconds: 5                # ±5s LOCKED default (§7)
  min_cameras: 2
  camera_offsets:
    DJI: 0
    Insta360: 0
    iPhone: 0
    GoPro: 0

variant_detection:
  parent_selection: largest_file   # largest_file | lowest_index | earliest_timestamp

proxies:
  generate_proxies: false          # Phase 1 only — must be false in Phase 0

performance:
  max_workers: 8                   # Min 8 for Studio tier

compliance:
  eula:
    version: "1.0"
    accepted: false
    text: |
      [Full 15-section EULA text — embedded in config.yaml]
```

---

## 5. Output Structure (§10 LOCKED)

```
PROJECT_ROOT/
├── YYYY-MM-DD/
│   ├── CAMERA/
│   │   ├── DJI/
│   │   ├── iPhone/
│   │   ├── Insta360/
│   │   ├── GoPro/
│   │   ├── Sony/
│   │   ├── Canon/
│   │   ├── Blackmagic/
│   │   ├── OMSystem/
│   │   └── Unknown_Camera/
│   ├── CAMERA_AUDIO/            ← field recorders (Zoom, Sound Devices, Tascam, etc.)
│   ├── GENERIC/
│   ├── PROXIES/                 ← Phase 1; created empty in Phase 0
│   ├── MULTICAM/
│   │   └── MCG_{sha256}.json   ← one per group
│   └── OUTPUTS/
├── REFERENCES/
├── LOGS/
│   ├── {run_id}_preflight.json
│   ├── {run_id}_manifest.json
│   ├── {run_id}_ingest.json
│   ├── {run_id}_classification.json
│   ├── {run_id}_grouping.json
│   ├── {run_id}_variants.json
│   ├── {run_id}_errors.json
│   └── {run_id}_summary.md
└── {run_id}_index.json
```

---

## 6. Testing Protocol

### Acceptance Suite (49/49)

```bash
python run_tests.py          # all 49 tests
python run_tests.py --verbose
python run_tests.py --suite 1   # classification
python run_tests.py --suite 2   # variants
python run_tests.py --suite 3   # multicam grouping
python run_tests.py --suite 4   # output structure
python run_tests.py --suite 5   # logging
python run_tests.py --suite 6   # idempotency
```

### Test Map (§17 Acceptance Criteria)

| Test File | §17 Test | Cases | Status |
|---|---|---|---|
| `test_classifier.py` | Test 1 — Classification | 7 | PASS |
| `test_variants.py` | Test 2 — Variant detection | 4 | PASS |
| `test_grouper.py` | Test 3 — Multicam grouping | 5 | PASS |
| `test_output.py` | Tests 4+5 — Output + metadata schema | 15 | PASS |
| `test_idempotency.py` | Test 6 + §3.x — Idempotency | 11 | PASS |
| `test_timestamp.py` | §5 — Fallback chain | 7 | PASS |

### Stress Test Protocol

Reference dataset: Harley Press Ride, March 4, 2026 (152.7 GB, 178 files, 7 camera sources)

```bash
python3 main.py \
  --input "/Volumes/10TB/2026 Harley-Davidson Chronicles/Harley Press Ride for Claude" \
  --output "/Volumes/10TB/WE_FLOW_OUTPUT/stress_test"
```

Pass criteria:
- All PF-01 through OP-04 metrics pass
- No crash on any file regardless of corruption or metadata state
- Multi-day folders separated by date
- Mixed audio correctly classified
- Second run on same input → byte-identical index JSON

---

## 7. Performance

Reference hardware: 16-core CPU, 64 GB RAM, NVMe SSD

| Tier | Dataset | Min Throughput | Max Memory | Wall Time |
|---|---|---|---|---|
| Novice | 100 GB | ≥50 GB/hr | ≤16 GB | ≤4 hrs |
| Pro | 500 GB | ≥120 GB/hr | ≤32 GB | ≤6 hrs |
| Studio | 1 TB | ≥80 GB/hr | ≤64 GB | ≤12 hrs |

**Stress test result (v4.5):** 152.7 GB in 772s = **712 GB/hr** (14.2× novice benchmark)

SHA-256 hashing uses streaming reads — files are never fully loaded into memory.

---

## 8. Deployment

### Requirements

```
Python 3.9+
pyyaml
ffprobe ≥ 4.4.6 (MacPorts) or ≥ 6.0 (Homebrew) — on PATH
macOS 14+ or Ubuntu 22.04 LTS
```

### Installation

```bash
git clone <repo>
cd we_capture
pip install -r requirements.txt

# Verify dependencies
python3 --version    # ≥ 3.9
ffprobe -version     # ≥ 4.4.6
```

### FFmpeg Installation (macOS)

```bash
# Homebrew (recommended for new installs)
brew install ffmpeg

# MacPorts (confirmed working — v4.4.6 used in stress tests)
sudo port install ffmpeg
# Path: /opt/local/bin/ffprobe
```

### Pre-Flight Storage Layout

| Role | Location | Notes |
|---|---|---|
| Input media | External media drive (e.g., `/Volumes/10TB`) | Never system drive |
| Output / project | External drive, min 5 GB free (symlink mode) | Same or separate |
| System drive | `/` | Keep ≥ 20 GB free |

---

## 9. Phase Roadmap Summary

| Phase | Status | Primary Deliverable | Compliance Gate |
|---|---|---|---|
| Phase 0 | **CONDITIONALLY GREEN** | Deterministic ingest engine, 26/28 compliance | Attorney EULA + first EULA acceptance run |
| Phase 1 | Planned (6–10 weeks) | Proxy generation, GPS extraction, summary enhancements | PIA + Privacy Policy + ToS + DPA + notarization |
| Phase 2 | Planned (12–20 weeks post-P1) | AI scene detection, content tagging, smart grouping | PIA per feature + EU AI Act + pen test |
| Phase 3 | Planned (16–24 weeks post-P2) | REST API, multi-operator, NLE plugins, cloud sync | Multi-tenant security review |
| W.E. C.A.P.E. | Platform layer above all phases | Production management, client portal, delivery pipeline | Inherits all phase compliance gates |

---

## 10. Data Governance

Governed by `DATA_GOVERNANCE.md`. Key obligations:

- Benchmark datasets are **Confidential** — vendors must delete within 30 days of contract close
- PII in test content is authorized for compliance stress testing (releases on file)
- GPS metadata extraction is Phase 1 — not implemented in Phase 0 code
- All PII in logs is SHA-256 hashed — plaintext PII never appears in any log file

---

*W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Implementation Package v6.0*  
*The Workman Experience, LLC | May 2026*  
*Proprietary and Confidential*
