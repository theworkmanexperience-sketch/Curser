# W.E. FLOW / W.E. FORGE — Implementation Package v4.1 ENHANCED

## Package Contents

| File | Description | Use |
|------|-------------|-----|
| `WE_FLOW_RFQ_v4.1_ENHANCED.docx` | Complete consolidated RFQ document | Issue to vendors |
| `we_flow_v4.1_ENHANCED_final.tar.gz` | Complete Phase 0 codebase | Reference implementation |
| `PACKAGE_MANIFEST.md` | This file | Navigation |

---

## RFQ Document (`WE_FLOW_RFQ_v4.1_ENHANCED.docx`)

Complete 30+ page contract-grade specification. Sections:

- §1–2: Executive Summary + System Flow
- §3–3.x: System Locks + Edge Case Matrix (10 cases)
- §4–5: Input Methodology + Detection Priority (§5 fallback chain)
- §6–6.x: File Classification + Performance & Scalability
- §7–9: Multicam Grouping + Variant Processing + Parent Selection
- §10–12: Output Structure + Metadata Schema + Logging
- §13–16: Edge Case Handling + Config + Technical Stack + Security
- §17: Acceptance Criteria (6 tests, quantitative thresholds)
- §18: Deliverables + Payment Terms (30/40/30)
- Appendix A: Assumptions & Validation Status (normative)
- Appendix B: Benchmark Datasets + Ground-Truth Manifest format
- Appendix C: Sample config.yaml + example run output + metadata JSON
- Appendix D: Change Log (6 rounds, all amendments)

---

## Codebase (`we_flow_v4.1_ENHANCED_final.tar.gz`)

```
we_flow/
├── main.py                     # CLI entry point
├── config.yaml                 # Appendix C authoritative config
├── requirements.txt            # pyyaml
├── README.md                   # Deployment + acceptance test map
├── run_tests.py                # Self-contained acceptance runner (no pytest)
├── benchmark_manifest_example.json  # Appendix B ground-truth format example
├── engine/
│   ├── classifier.py           # §6 — camera/camera_audio/generic/reference
│   ├── timestamp.py            # §5 — fallback chain + confidence flag
│   ├── grouper.py              # §7 — deterministic multicam grouping
│   ├── variants.py             # §8 — variant detection + Option B orphan logic
│   ├── output.py               # §10 — locked directory structure
│   ├── pipeline.py             # §2-4 — parallel ingest, SHA-256, idempotency
│   └── audit.py                # §12 — five mandatory log streams
└── tests/
    ├── test_classifier.py      # §17 Test 1 (7 cases)
    ├── test_grouper.py         # §17 Test 3 (5 cases)
    ├── test_variants.py        # §17 Test 2 (4 cases)
    ├── test_output.py          # §17 Tests 4+5 (15 cases)
    ├── test_idempotency.py     # §17 Test 6 + §3.x (11 cases)
    └── test_timestamp.py       # §5 fallback chain (7 cases)
```

**Test status: 49/49 passing**

---

## Quick Start

```bash
# Extract codebase
tar -xzf we_flow_v4.1_ENHANCED_final.tar.gz
cd we_flow

# Install dependency
pip install pyyaml

# Run acceptance suite
python run_tests.py

# Run on real media (smoke test before issuing RFQ)
python main.py --input /path/to/real/shoot --output /path/to/project

# Run with verbose output
python run_tests.py --verbose

# Run specific test suite
python run_tests.py --suite 6   # idempotency only
```

**Requirements:** Python 3.11+, FFmpeg 6.0+ (`ffprobe` on PATH)

---

## Before Issuing the RFQ

1. **Smoke test on real media** — run on 20–30 actual camera files before issuing
2. **Initialize git repo** — `git init && git add . && git commit -m "feat: Phase 0 engine v4.1 ENHANCED — 49/49 tests" && git tag v4.1.0`
3. **Build benchmark datasets** — use `benchmark_manifest_example.json` as the format template
4. **Confirm reference hardware spec** — document exact CPU model and NVMe speed for vendor testing

---

*Generated: May 2026 | W.E. FLOW / W.E. FORGE RFQ v4.1 ENHANCED*
