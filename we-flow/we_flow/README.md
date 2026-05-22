# W.E. FLOW / W.E. FORGE — v4.1 ENHANCED
**Deterministic Media Ingestion Engine — Phase 0**

---

## Quick Start (New Users — Read This First)

**The one rule that prevents 95% of problems:**

> Your media and project output must always go on an **external drive** — never on your Mac's internal drive.

**How to tell the difference:**
- Open **Finder** and look at the left sidebar under **Locations**
- Anything listed there (like `10TB`, `Got My BackUP`, `FreeAgent`) is an external drive ✓
- Your Mac's internal drive is called **Macintosh HD** — never use this for output ✗

**The correct command looks like this:**
```bash
python3 main.py \
  --input  /Volumes/YOUR_DRIVE/shoot_folder \
  --output /Volumes/YOUR_DRIVE/WE_FLOW_OUTPUT/project_name
```

**Before every run, the engine will print a Pre-Flight Check:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  W.E. FLOW — Pre-Flight Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Input media:    /Volumes/10TB/shoot     141.0 GB · 49,602 files
  Output folder:  /Volumes/10TB/WE_FLOW   887.0 GB free  ✓
  File mode:      symlink mode — no files copied
  Space needed:   5.0 GB minimum on output drive
  System drive:   147.0 GB free  ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If you see a **⚠ WARNING**, stop and read it before pressing Enter. The engine will tell you exactly what to fix and how.

**Keep your Mac's internal drive above 20 GB free at all times.** If it drops below that, move files to an external drive before running the engine.

---

## Requirements
- Python 3.9+
- FFmpeg 6.0+ (`ffprobe` must be on PATH) — **required for multicam grouping**
- OS: macOS 14+ or Ubuntu 22.04 LTS

```bash
ffprobe -version   # confirm ≥ 6.0
python3 --version  # confirm ≥ 3.9
```

> **Without ffprobe:** Classification and variant detection work. Multicam grouping is disabled — all camera files fall back to `file_stat_mtime` (low confidence) and 0 groups will be formed. Install ffprobe before issuing the RFQ benchmark.

---

## Pre-Flight Requirements

**Always point `--output` to an external drive for shoots over 10 GB.**

The engine enforces a pre-flight disk check before starting:
- `file_operation: copy` (default off) — requires ~110% of input size free on output drive
- `file_operation: symlink` (recommended) — requires 5 GB minimum free
- Engine aborts with a clear error if space is insufficient

**Recommended storage layout:**

| Role | Drive | Notes |
|---|---|---|
| Input media | Dedicated media drive (e.g. 10TB) | Never the system drive |
| Output / project | Same media drive or separate external | Min 5 GB free for symlink mode |
| System drive | macOS system only | Keep ≥ 20 GB free at all times |

**Use `symlink` mode for smoke tests and QC runs.** Use `copy` or `move` only when delivering a self-contained project folder.

```bash
# Correct — output to external drive, symlink mode (config.yaml default)
python main.py --input /Volumes/10TB/shoot --output /Volumes/10TB/WE_FLOW_OUTPUT/project

# Dangerous — output to system drive with copy mode will exhaust disk
# python main.py --input /Volumes/10TB/large_shoot --output ~/Desktop/output
```

---

## Installation

```bash
git clone <repo>
cd we_flow
pip install -r requirements.txt
```

---

## Usage

```bash
# Default: single-folder ingest (§3 primary mode)
python main.py --input /path/to/media --output /path/to/project

# Custom config
python main.py --input ./raw --output ./project --config ./custom.yaml

# Studio tier — override workers (min 8 required)
python main.py --input ./1TB_shoot --output ./project --workers 16
```

---

## Output Structure (§10 LOCKED)

```
PROJECT/
  YYYY-MM-DD/
    CAMERA/
      DJI/
      iPhone/
      Unknown_Camera/
    CAMERA_AUDIO/        ← field recorders (Zoom, Sound Devices)
    GENERIC/
    PROXIES/             ← Phase 1 reserved; created empty in Phase 0
    MULTICAM/
      MCG_XXXXXXXX.json  ← one metadata file per group
    OUTPUTS/
  REFERENCES/
  LOGS/
    {run_id}_ingest.json
    {run_id}_classification.json
    {run_id}_grouping.json
    {run_id}_variants.json
    {run_id}_errors.json
    {run_id}_summary.md
  {run_id}_index.json
```

---

## Configuration (Appendix C)

All rules are externally configurable via `config.yaml`.
Key parameters:

| Key | Default | Description |
|-----|---------|-------------|
| `pipeline.file_operation` | `symlink` | `copy` / `move` / `symlink` — use `symlink` for QC runs |
| `grouping.window_seconds` | `5` | Multicam sync window (§7) |
| `grouping.camera_offsets` | all `0` | Per-camera UTC offset (seconds) |
| `variant_detection.parent_selection` | `largest_file` | `largest_file` / `lowest_index` / `earliest_timestamp` |
| `audio_classification.field_recorder_patterns` | Zoom/SD/Tascam | Regex list → Camera-Audio |
| `proxies.generate_proxies` | `false` | **Must remain false in Phase 0** |
| `performance.max_workers` | `8` | Parallel threads (≥8 for Studio tier) |
| `pipeline.enable_duplicate_content_detection` | `false` | SHA-256 dedup |

---

## Acceptance Tests (§17)

```bash
pytest tests/ -v
```

Tests map to §17 acceptance criteria:

| Test file | §17 test |
|-----------|----------|
| `test_classifier.py` | Test 1 — Classification |
| `test_variants.py` | Test 2 — Variant detection |
| `test_grouper.py` | Test 3 — Multicam grouping |
| Pipeline output structure | Test 4 — Output + metadata schema |
| Log file existence | Test 5 — Comprehensive logging |
| Re-run on same input | Test 6 — Idempotency & robustness |

Tests 4–6 require the client benchmark datasets and `benchmark_manifest.json`
(Appendix B). Contact The Workman Experience, LLC for access.

---

## Performance (§6.x)

Reference hardware: 16-core CPU, 64 GB RAM, NVMe SSD.

| Tier | Dataset | Min throughput | Max memory | Wall time |
|------|---------|----------------|------------|-----------|
| Novice | 100 GB | ≥50 GB/hr | ≤16 GB | ≤4 hrs |
| Pro | 500 GB | ≥120 GB/hr | ≤32 GB | ≤6 hrs |
| Studio | 1 TB | ≥80 GB/hr | ≤64 GB | ≤12 hrs |

Studio tier requires `performance.max_workers: 8` minimum.
SHA-256 hashing uses streaming reads — 50 GB files never fully loaded into memory.

---

## Phase 0 Scope (§3 LOCKED)

✅ Deterministic ingest + classification + grouping + variant detection  
✅ Structured auditable output  
✅ Five mandatory log streams  
✅ CAMERA_AUDIO classification + multicam timestamp association  
❌ No AI editing  
❌ No scene detection  
❌ No proxy generation (Phase 1)  
❌ No UI beyond config files  
