# W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Compliance Delta v4.8

**Issued by:** The Workman Experience, LLC
**Date:** 2026-05-27
**Covers:** Phase 1-C (Config Profile System) + preflight verification audit
**Previous delta:** COMPLIANCE_DELTA_v4.7.md (Phase 1-A archive engine fixes)
**Distribution:** Internal — not for client distribution

---

## Changes Since v4.7

### 1. Phase 1-C: Config Profile System — COMPLETE

**Commit:** `4d054e4`
**Tests:** 11/11 passing
**Production validated:** Run `WEF_20260527_185428_26967E` — 103 files, baseline held

New surface area introduced:

| Item | Description | Compliance Impact |
|------|-------------|-------------------|
| `engine/profile.py` | ProfileLoader with deep_merge, system+user dir resolution | Low — reads YAML only, no external calls |
| `profiles/default.yaml` | Annotated reference of all overridable keys | None |
| `profiles/ryderz.yaml` | O-SIX RYDERZ client profile | None |
| `profiles/google_drive.yaml` | Google Drive delivery profile — enables archive engine | Activate only on trusted input sources |
| `--profile` CLI flag | Loads named profile before pipeline instantiation | Operator must verify profile before production run |
| `--list-profiles` CLI flag | Lists available profiles without requiring --input/--output | Safe — read-only |

No new PII surface area. No external network calls. Profile files are YAML read at startup only.

---

### 2. Spec Deviation: Multicam Grouping Window ±5s → ±15s

**Severity:** SPEC DEVIATION — §7 previously LOCKED at ±5s
**Evidence:** Production run `WEF_20260527_042036_FFF7D9` — Ryderz dataset showed
real-world 8-second gap between DJI and Insta360 cameras at identical scene start.
**Decision:** Default changed to `window_seconds: 15` in `config.yaml` and
`profiles/ryderz.yaml`. The ±5s lock is released. Window is now configurable
per-profile with 15s as the production-validated default.

**Impact on compliance:**
- MG-01 (grouping determinism) — PASS maintained, output is still deterministic
- MG-02 (idempotent re-runs) — PASS maintained
- MG-03 (grouping accuracy ≥ 95%) — remains untestable without simultaneous
  multicam dataset. The 15s window increases true-positive grouping rate on
  real-world data; false-positive risk (grouping files that shouldn't be grouped)
  is mitigated by the distinct-camera-source requirement.

**Documents requiring update:** EXECUTIVE_SUMMARY_v4.6.md (states ±5s as product
capability), SYSTEM_FLOW spec (Stage 4 description).

---

### 3. Preflight Verification Audit — May 27, 2026

Full audit of `_preflight.json` output against compliance roadmap spec.

**Verified PASS:**

| Field | Spec Requirement | Actual Output | Status |
|-------|-----------------|---------------|--------|
| `run_id` | Present | `WEF_20260527_185428_26967E` | ✅ |
| `event` | `preflight_accepted` or `preflight_noninteractive` | `preflight_accepted` | ✅ |
| `logged_at` | UTC ISO timestamp | `2026-05-27T18:54:34.729248+00:00` | ✅ |
| `operator` | `os.getenv('USER')` | `twork` | ✅ |
| `input_path_hash` | SHA-256 of path (not plaintext) | `sha256:d0a2c01e...` | ✅ |
| `output_drive` | Output path | `/Volumes/10TB/WE_FLOW_OUTPUT/...` | ✅ |
| `output_on_system_drive` | Boolean | `false` | ✅ |
| `eula_version_accepted` | EULA version string | `"1.0"` | ✅ |
| `attestation_hash` | SHA-256 of attestation text | `sha256:02e02ddf...` | ✅ |
| `file_operation_mode` | `symlink` / `copy` / `move` | `symlink` | ✅ |

**EULA v1.0 acceptance — verified:**
- Text embedded in `config.yaml` lines 197–246
- First-run acceptance recorded `2026-05-25T06:25:48.195482+00:00`
- Operator `twork`, version `1.0`
- Persistence: `~/.weflow/eula_acceptance.json`
- Phase 0 gate condition: **SATISFIED**

**Gaps found:**

| Gap | Spec Requirement | Actual | Risk | Action |
|-----|-----------------|--------|------|--------|
| `output_drive_encrypted` | Required field in preflight record | Field absent — `diskutil info` never called | Low for internal work | Build before retail |
| `pii_flagged_filenames` | PII filenames hashed (never plaintext) | Stores raw filenames | Low — `pii_flagged_count: 0` on all runs to date | Hash before next PII-rich dataset |

**Architectural note:**
EULA text is embedded in `config.yaml` alongside operational configuration. Risk:
accidental modification of legal text during routine config changes. Recommendation:
move EULA text to a separate read-only file (e.g. `legal/EULA_v1.0.txt`) before
retail distribution.

---

### 4. _preflight.json Filename Convention

The file is written as `{run_id}_preflight.json` (e.g.
`WEF_20260527_185428_26967E_preflight.json`), not `_preflight.json`.
All compliance documentation updated to reflect the run-scoped filename.
This is correct behavior — each run produces its own preflight record.

---

### 5. Cumulative Test Count

| Phase | Tests | Status |
|-------|-------|--------|
| Phase 0 (core pipeline) | 49 | ✅ Passing |
| Stage 0.5 (Archive Intelligence) | 21 | ✅ Passing |
| Phase 1-C (Config Profile System) | 11 | ✅ Passing |
| **Total** | **81** | ✅ **81/81** |

---

### 6. System Flow Stage Changes (vs. May 22 Spec)

| Change | May 22 Spec | May 27 Actual |
|--------|-------------|---------------|
| Stage numbering | 0–7 (Pre-flight as Stage 0) | Pre-flight unlabeled; pipeline Stages 0–6 |
| Stage 0.5 | Not in spec | Archive Intelligence (Phase 1 gated) |
| Classification vs. Timestamp order | Timestamp (Stage 2) → Classification (Stage 3) | Classification (Stage 1) → Timestamp (Stage 2) |
| Default grouping window | ±5s LOCKED | ±15s (configurable) |

**SYSTEM_FLOW_v2.md required** to document current authoritative pipeline stages.

---

## Open Compliance Items (Internal Work)

| ID | Item | Priority | Target |
|----|------|----------|--------|
| OP-05 | `output_drive_encrypted` field in preflight | Low | Pre-retail |
| PI-02 | Hash `pii_flagged_filenames` before storage | Medium | Before PII-rich dataset |
| PI-04 | GPS metadata extraction | Low | Phase 1, evidence-driven |
| MG-03 | Grouping accuracy ≥ 95% validation | Low | Bagger World Cup dataset |
| ARCH-01 | Separate EULA text from config.yaml | Low | Pre-retail |

## Deferred to Retail Engagement (Attorney Required)

- EULA v1.0 formal distribution packaging
- Privacy Policy (GDPR Art.13 + CCPA §1798.100)
- Terms of Service
- Data Processing Agreement template
- macOS code signing + Apple notarization
- Output drive encryption check (`diskutil info`)
- Version + update mechanism

---

*Last updated: 2026-05-27*
*Next delta: v4.9 — to be written after SYSTEM_FLOW_v2.md and Phase 1-D completion*
