# W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Implementation Package v6.0
## Phase 0 Gate: CONDITIONALLY GREEN | Compliance: 26/28 | Engine: 49/49 Tests

**The Workman Experience, LLC | May 22, 2026**

---

## Package Contents

| File | Description | Use |
|---|---|---|
| `EXECUTIVE_SUMMARY_v4.6.md` | Phase 0 gate status, capabilities, phase roadmap | Executive briefing |
| `WE_FLOW_RFQ_v6.md` | Contract-grade specification for vendor engagement | Issue to vendors |
| `WE_FLOW_IMPLEMENTATION_PACKAGE_v6.md` | Full technical build package | Engineering reference |
| `PACKAGE_MANIFEST.md` | This file | Navigation |
| `we_capture/` | Complete Phase 0 codebase (Python 3.9+) | Production implementation |

---

## Compliance Evidence Chain

| Delta | Run ID | Score | Key Changes |
|---|---|---|---|
| `COMPLIANCE_DELTA_v4.1.md` | `WEF_20260522_205035_AB4BE3` | 15/28 | Baseline stress test |
| `COMPLIANCE_DELTA_v4.2.md` | `WEF_20260522_220208_9D47BA` | 23/28 | PI-03, AI-04, PF-01, PI-01/02, MG-01, OP-04, PF-02 partial |
| `COMPLIANCE_DELTA_v4.3.md` | *(code analysis only)* | 25/28 | CL-01 100%, CL-04 folder patterns |
| `COMPLIANCE_DELTA_v4.4.md` | `WEF_20260522_225930_32B2F2` | 25/28 | CL-01/04 runtime confirmed |
| `COMPLIANCE_DELTA_v4.5.md` | `WEF_20260522_235702_C02E9C` | 25/28 | ffprobe active, MG-01 confirmed |
| `COMPLIANCE_DELTA_v4.6.md` | commit `31a96c8` | **26/28** | **PF-02 PASS — EULA v1.0 final** |

---

## Codebase Structure (`we_capture/`)

```
we_capture/
├── main.py                           # CLI entry point
├── config.yaml                       # Appendix C authoritative config (EULA v1.0 embedded)
├── requirements.txt                  # pyyaml
├── README.md                         # Deployment + acceptance test map
├── run_tests.py                      # Self-contained acceptance runner (no pytest)
├── benchmark_manifest_example.json   # Appendix B ground-truth format example
├── benchmark_manifest_bagger_world_cup_march29.json  # Bagger World Cup ground-truth
├── engine/
│   ├── classifier.py                 # §6 — camera/camera_audio/generic/reference
│   │                                 #   + folder-based classification (v4.1+)
│   ├── timestamp.py                  # §5 — ffprobe + filename + mtime fallback chain
│   ├── grouper.py                    # §7 — deterministic multicam grouping (±5s LOCKED)
│   ├── variants.py                   # §8 — variant detection + Option B orphan logic
│   ├── output.py                     # §10 — locked directory structure
│   ├── pipeline.py                   # §2–4 — parallel ingest, SHA-256, EULA, idempotency
│   └── audit.py                      # §12 — five mandatory log streams + manifest
├── tests/
│   ├── test_classifier.py            # §17 Test 1 — 7 classification cases
│   ├── test_grouper.py               # §17 Test 3 — 5 multicam grouping cases
│   ├── test_variants.py              # §17 Test 2 — 4 variant detection cases
│   ├── test_output.py                # §17 Tests 4+5 — 15 output + schema cases
│   ├── test_idempotency.py           # §17 Test 6 + §3.x — 11 idempotency cases
│   └── test_timestamp.py             # §5 — 7 fallback chain cases
├── COMPLIANCE_ROADMAP_v2.0.md        # Authoritative compliance framework
├── DATA_GOVERNANCE.md                # Dataset governance + vendor obligations
└── COMPLIANCE_DELTA_v4.1–4.6.md     # Complete compliance evidence chain
```

**Test status: 49/49 passing**  
**FFmpeg requirement:** 4.4.6+ (MacPorts) or 6.0+ (Homebrew); `ffprobe` must be on PATH

---

## Quick Start

```bash
# Clone or extract codebase
cd we_capture

# Install runtime dependency
pip install pyyaml

# Verify ffprobe (required for multicam grouping)
ffprobe -version

# Run acceptance suite (all 49 tests)
python run_tests.py

# Run on real media
python main.py --input /Volumes/DRIVE/shoot_folder --output /Volumes/DRIVE/WE_FLOW_OUTPUT/project

# Verbose output
python run_tests.py --verbose

# Specific test suite (idempotency only)
python run_tests.py --suite 6
```

**Requirements:** Python 3.9+ | FFmpeg (`ffprobe` on PATH) | macOS 14+ or Ubuntu 22.04 LTS

---

## Key Configuration Parameters

| Key | Default | Notes |
|---|---|---|
| `pipeline.file_operation` | `symlink` | Use `symlink` for QC runs; `copy` for delivery |
| `grouping.window_seconds` | `5` | ±5s LOCKED default (§7); configurable per project |
| `compliance.eula.version` | `"1.0"` | Attorney-reviewed EULA text embedded in config |
| `proxies.generate_proxies` | `false` | Must remain false in Phase 0 |
| `performance.max_workers` | `8` | Min 8 for Studio tier |

---

## Phase 0 Gate Status

| Item | Status | Blocks Phase 0? |
|---|---|---|
| 49/49 acceptance tests | **PASS** | — |
| 5 full stress-test runs (152.7 GB) | **PASS** | — |
| Compliance metrics 26/28 | **PASS** | — |
| EULA v1.0 (attorney-reviewed) | **PASS** | — |
| PI-04 GPS extraction | FAIL — Phase 1 | **No** |
| MG-03 grouping accuracy dataset | CANNOT TEST — Phase 1 | **No** |
| Privacy Policy / ToS / DPA | Pending attorney review | **No (pre-distribution)** |
| macOS code signing + notarization | Pending | **No (pre-App Store)** |

---

## Before Issuing the RFQ

1. **Smoke test** — run on 20–30 actual camera files: `python main.py --input /path/to/shoot --output /path/to/output`
2. **Review compliance evidence** — read `COMPLIANCE_DELTA_v4.6.md` for Phase 0 gate status
3. **Confirm ffprobe** — `ffprobe -version` must return ≥ 4.4.6
4. **Build benchmark manifest** — use `benchmark_manifest_example.json` as format template
5. **Attorney review** — Privacy Policy, ToS, and DPA template required before retail distribution

---

*W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Implementation Package v6.0*  
*The Workman Experience, LLC | May 2026*  
*Compliance: 26/28 | Gate: CONDITIONALLY GREEN | Tests: 49/49*
