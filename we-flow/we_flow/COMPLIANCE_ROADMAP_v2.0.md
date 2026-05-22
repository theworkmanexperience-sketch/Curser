# W.E. FLOW / W.E. FORGE — Compliance Roadmap v2.0
## Privacy by Design · Security by Design · Compliance by Design

**Issued by:** The Workman Experience, LLC  
**Replaces:** COMPLIANCE_ROADMAP.md (v1.0 — planning document only)  
**Status:** Authoritative — governs all phases post-RFQ  
**Last updated:** 2026-05-22

---

## Governing Principle

Compliance, privacy, and security are architectural constraints — not audits
performed after the fact. Every feature at every phase is evaluated against this
framework before a line of code is written.

The test for any compliance claim is: **can it fail?**
If a claim cannot be expressed as a falsifiable test, it is not a compliance
control — it is a wish. This document contains only falsifiable controls.

---

## The Seven Design Principles (Applied to WE Flow)

| Principle | What it means in practice |
|---|---|
| **1. Proactive** | Privacy Impact Assessment (PIA) before every new feature |
| **2. Default-protective** | Most protective setting is always the default; users opt in to exposure |
| **3. Embedded** | Compliance controls are in the engine, not layered on top |
| **4. Full functionality** | Privacy does not degrade capability — both are achievable |
| **5. End-to-end security** | Audit trail begins before Stage 0; temp files securely deleted after Stage 6 |
| **6. Transparent** | User always knows what the engine is doing and why |
| **7. User-centric** | Plain English at every decision point; no jargon in user-facing output |

---

## Quantitative Compliance Metrics

Each metric below is a testable assertion. Pass/fail is binary.
These run as part of the acceptance suite — not as a separate audit.

### Pre-Flight & Attestation

| ID | Metric | Pass Condition | Failure Action |
|---|---|---|---|
| PF-01 | Operator attestation logged | `_preflight.json` exists and contains `event: preflight_accepted` with non-null `attestation_hash` | Block run |
| PF-02 | EULA version recorded | `_preflight.json` contains `eula_version_accepted` matching current EULA version string | Block run |
| PF-03 | System drive detection | If output path resolves to same device as `/`, warning is printed before any processing | Block run if copy mode + input > 10GB |
| PF-04 | Output drive space | Free space on output drive ≥ required minimum before Stage 0 begins | Block run |
| PF-05 | System drive headroom | System drive free space printed in pre-flight summary every run | Warn if < 20GB |
| PF-06 | Input path hash in log | `_preflight.json` contains SHA-256 hash of input path string (not plaintext) | Block run |

### Ingest & Audit Integrity

| ID | Metric | Pass Condition | Failure Action |
|---|---|---|---|
| AI-01 | 100% file coverage | File count in `_ingest.json` == file count returned by `_discover_files()` | Pipeline error |
| AI-02 | No silent drops | Every file discovered appears in exactly one of: `_classification.json`, `_errors.json` | Pipeline error |
| AI-03 | Audit log completeness | All five log streams exist after every run: ingest, classification, grouping, variants, errors | Run flagged incomplete |
| AI-04 | Log tamper-evidence | SHA-256 of each log file written to `_preflight.json` at run close; re-verification passes on demand | Tamper alert |
| AI-05 | Run ID consistency | Same `run_id` appears in all six log files (5 streams + preflight) | Pipeline error |
| AI-06 | Timestamp monotonicity | `logged_at` values within each log stream are non-decreasing | Warn |

### PII Detection

| ID | Metric | Pass Condition | Failure Action |
|---|---|---|---|
| PI-01 | PII pattern scan coverage | 100% of discovered filenames scanned against PII pattern list before Stage 1 | Block run |
| PI-02 | PII warning printed | If any filename matches PII pattern, warning printed in pre-flight before attestation prompt | Required |
| PI-03 | PII not logged | PII-flagged filenames are hashed in logs — plaintext PII never written to any log file | Pipeline error |
| PI-04 | GPS metadata flagged | If ffprobe detects GPS coordinates in any media file, pre-flight warns before processing | Warn |

### Classification Accuracy

| ID | Metric | Pass Condition | Failure Action |
|---|---|---|---|
| CL-01 | Known camera coverage | All camera sources in config.yaml match ≥ 95% of expected files in benchmark dataset | Test failure |
| CL-02 | Zero unclassified drops | Every file receives a classification; `Unknown_Camera` is valid, NULL is not | Pipeline error |
| CL-03 | OMSystem recognition | All `P[0-9]{7}.MOV` files classified as `OMSystem`, not `Unknown_Camera` | Test failure |
| CL-04 | Reference file detection | All `.pdf`, `.docx`, `.srt` files classified as `reference` | Test failure |

### Multicam Grouping

| ID | Metric | Pass Condition | Failure Action |
|---|---|---|---|
| MG-01 | ffprobe availability | If ffprobe not on PATH, warning printed and multicam grouping skipped (not crashed) | Warn + skip |
| MG-02 | Group ID determinism | Re-running on same input produces identical group IDs (SHA-256 verified) | Test failure |
| MG-03 | Grouping accuracy | ≥ 95% of eligible camera files in correct group (benchmark manifest) | Test failure |
| MG-04 | Window compliance | No group contains files outside ±5s window (§7 LOCKED) | Pipeline error |

### Output & Idempotency

| ID | Metric | Pass Condition | Failure Action |
|---|---|---|---|
| OP-01 | Idempotent re-runs | Re-running on same input + output produces identical index JSON (no `_1` suffix artifacts) | Test failure |
| OP-02 | No system drive writes | In symlink mode, zero bytes of media data written to system drive | Pipeline error |
| OP-03 | Symlink integrity | All symlinks in output resolve to existing source files | Post-run check |
| OP-04 | Secure temp deletion | No temp files remain in `/tmp` or system temp after run completes | Post-run check |

---

## Stress Test Protocol — Harley Press Ride (PII Production Content)

**Dataset:** `/Volumes/10TB/2026 Harley-Davidson Chronicles/Harley Press Ride for Claude`  
**Purpose:** Validate engine against real PII, messy metadata, mixed audio, and multi-day structure  
**Releases on file:** Yes — confirmed by content owner  
**Run before:** Phase 0 retail gate

### Pre-test documentation (required before running)
- [ ] Document known PII present: faces, GPS locations, names in filenames
- [ ] Document expected camera sources and file counts per day
- [ ] Document known messy files: zero-byte, corrupt, wrong extension, special characters
- [ ] Establish ground-truth file count for comparison

### Test execution
```bash
# Run with symlink mode, output to 10TB, verbose logging
python3 main.py \
  --input "/Volumes/10TB/2026 Harley-Davidson Chronicles/Harley Press Ride for Claude" \
  --output "/Volumes/10TB/WE_FLOW_OUTPUT/stress_test_press_ride"
```

### Pass criteria (all must pass)
- [ ] **PF-01 through PF-06** — Pre-flight and attestation metrics
- [ ] **AI-01 through AI-06** — Ingest and audit integrity metrics
- [ ] **PI-01 through PI-04** — PII detection metrics
- [ ] **CL-01 through CL-04** — Classification accuracy metrics
- [ ] **OP-01 through OP-04** — Output and idempotency metrics
- [ ] Engine does not crash on any file regardless of corruption or metadata state
- [ ] All multi-day folders correctly separated by date in output structure
- [ ] Mixed audio (field recorder + scratch) correctly classified
- [ ] Run summary accurately reflects actual file counts (no off-by-one)
- [ ] Second run on same input produces byte-identical index JSON

### Evidence artifacts (attach to compliance gate)
- `_preflight.json` from the run
- `_summary.md` from the run
- Screenshot of pre-flight terminal output
- Diff of two consecutive run index JSON files (must be empty)
- List of any PII warnings triggered and confirmation they were hashed in logs

---

## Phase Gate Checklists (Revised — Evidence Required)

### Phase 0 Retail Gate
Each item requires attached evidence, not just a tick.

**Engine**
- [ ] All 49 acceptance tests pass — `run_tests.py` output attached
- [ ] Stress test protocol complete — evidence artifacts attached
- [ ] Quantitative metrics PF-01 through OP-04 all pass — test output attached
- [ ] ffprobe installed, multicam grouping validated on benchmark dataset
- [ ] OMSystem classification fix tested (config v4.1.1) — test output attached

**Pre-flight & Compliance Controls**
- [ ] Operator attestation implemented — `_preflight.json` sample attached
- [ ] EULA first-run acceptance logged — screenshot + log sample attached
- [ ] Output drive encryption check implemented — test on encrypted + unencrypted drive attached
- [ ] PII filename detection implemented — test showing warning + hash (not plaintext) in log
- [ ] Secure temp file deletion implemented — `/tmp` scan after run shows zero artifacts
- [ ] Audit log SHA-256 signing implemented — tamper test (modify log → re-verify fails) attached
- [ ] System drive detection tested — screenshot of warning on system drive output path

**Legal**
- [ ] EULA drafted and reviewed by qualified attorney
- [ ] Privacy Policy drafted and reviewed by qualified attorney
- [ ] Terms of Service drafted and reviewed
- [ ] Data Processing Agreement template ready for B2B sales
- [ ] DATA_GOVERNANCE.md reviewed by attorney

**Distribution**
- [ ] macOS code signing complete
- [ ] Apple notarization passed — notarization ticket attached
- [ ] Version number scheme established
- [ ] Update check mechanism tested

### Phase 1 Retail Gate
- [ ] All Phase 0 gate items with evidence
- [ ] PIA completed for proxy generation feature
- [ ] FFmpeg temp file secure deletion confirmed — scan attached
- [ ] Proxy metadata stripping tested — `exiftool` output on proxy sample attached
- [ ] Installer package EULA acceptance tested
- [ ] Pre-flight proxy output drive check tested

### Phase 2+ Retail Gate
- [ ] All Phase 1 gate items with evidence
- [ ] PIA completed for every AI feature before implementation
- [ ] On-device vs cloud inference decision documented and disclosed in Privacy Policy
- [ ] Biometric data policy in place if face/body detection added — attorney reviewed
- [ ] EU AI Act compliance review completed (required for EU distribution)
- [ ] App store privacy nutrition labels completed and reviewed
- [ ] Penetration test completed — report attached
- [ ] Threat model document completed and reviewed

---

## Regional Regulatory Matrix (Revised)

| Regulation | Region | Phase 0 Requirement | Phase 1 Additional | Phase 2+ Additional |
|---|---|---|---|---|
| **GDPR** | EU / UK | Attestation + audit logs + Privacy Policy + DPA template | Proxy metadata policy | AI inference disclosure + DPIA |
| **CCPA** | California | Privacy Policy + opt-out notice + data inventory | Same | Right to deletion for derived data |
| **PIPEDA** | Canada | Consent documentation + privacy notice | Same | Same |
| **LGPD** | Brazil | Consent-first + DPA equivalent | Same | Same |
| **POPIA** | South Africa | GDPR-equivalent controls | Same | Same |
| **BIPA** | Illinois | N/A Phase 0 | N/A | Required if face detection — written consent per subject |
| **CUBI** | Texas | N/A Phase 0 | N/A | Required if face detection |
| **EU AI Act** | EU | N/A Phase 0 | N/A | Required — conformity assessment for high-risk AI |
| **HIPAA** | USA | Low risk — flag if medical content detected | Low risk | Flag if medical content |

---

## Privacy Impact Assessment Template

Required before every new feature. Complete and attach to feature PR.

```
Feature name:
Phase:
Author:
Date:

1. What personal data does this feature touch?

2. Is this data necessary for the feature to work?
   (If no, remove it. Data minimization is not optional.)

3. What is the lawful basis for processing? (GDPR Art.6)
   [ ] Consent  [ ] Contract  [ ] Legal obligation
   [ ] Vital interests  [ ] Public task  [ ] Legitimate interests

4. Where is the data stored and for how long?

5. Who can access it?

6. What happens if this data is breached?

7. Can this feature be built with less data or less access?

8. Is there a falsifiable compliance test for this feature?
   (If no, define one before proceeding.)

Approved by: ________________  Date: ________
```

---

## Legal Documents Required (Pre-Retail)

> These require a qualified attorney. They may not be AI-generated.

| Document | Needed by | Notes |
|---|---|---|
| End User License Agreement (EULA) | Phase 0 retail | Governs all use; must survive jurisdiction analysis |
| Privacy Policy | Phase 0 retail | GDPR Art.13 + CCPA §1798.100 minimum |
| Terms of Service | Phase 0 retail | App store requirement |
| Data Processing Agreement (DPA) template | Phase 0 retail | Required for any B2B sale under GDPR |
| Biometric Data Consent Form | Phase 2+ | If face/body detection added — per-subject consent |
| AI Transparency Statement | Phase 2+ | EU AI Act conformity |

---

*Every compliance claim in this document is falsifiable.*  
*If a test cannot be written for a claim, the claim is removed.*  
*Legal documents require qualified attorney review — not AI-generated.*  
*Last updated: 2026-05-22*
