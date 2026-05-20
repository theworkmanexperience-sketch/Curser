# W.E. FLOW / W.E. FORGE — v4.1 ENHANCED
**Deterministic Media Ingestion Engine — Phase 0**

---

## Requirements
- Python 3.11+
- FFmpeg 6.0+ (`ffprobe` must be on PATH)
- OS: macOS 14+ or Ubuntu 22.04 LTS

```bash
ffprobe -version   # confirm ≥ 6.0
python --version   # confirm ≥ 3.11
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
| `pipeline.file_operation` | `copy` | `copy` / `move` / `symlink` |
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
