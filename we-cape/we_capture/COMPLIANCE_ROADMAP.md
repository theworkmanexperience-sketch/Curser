# W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Compliance Roadmap
## Privacy · Governance · Global Regulatory · Security

**Issued by:** The Workman Experience, LLC  
**Applies to:** All phases of the W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. product build  
**Status:** Living document — update at each phase gate before release

---

## Overview

W.E. C.A.P.E. CAPTURE processes personal media — video, photos, and audio that may contain
identifiable individuals, biometric data, GPS locations, and proprietary content.
Compliance is not optional at retail. This roadmap defines what must be built,
reviewed, and certified at each phase before distribution.

---

## Compliance Requirements by Phase

### Phase 0 — Current (CLI, Local Processing)
**Distribution: RFQ vendors → Retail (CLI)**

| Requirement | Status | Action Required |
|---|---|---|
| Local-only processing (no external calls) | ✓ Done | — |
| Five mandatory audit log streams | ✓ Done | — |
| Deterministic, reproducible output | ✓ Done | — |
| Pre-flight disk check (usability) | ✓ Done | — |
| **Pre-flight operator attestation** | ✅ Done | Verified — `_preflight.json` written every run |
| **EULA accepted + logged at first run** | ✅ Done | Verified — v1.0 accepted 2026-05-25; persisted to `~/.weflow/` |
| **Privacy Policy linked at startup** | ⏸ Deferred | Internal work only — engage attorney pre-retail |
| **Audit log tamper-evidence** | ✗ Missing | SHA-256 log signing — pre-retail |
| **Output drive encryption check** | ⚠️ Partial | `output_drive_encrypted` field missing from preflight — pre-retail |
| **PII filename detection + warning** | ⚠️ Partial | Wiring built; `pii_flagged_filenames` stores plaintext — fix before PII-rich dataset |
| **Secure temp file deletion** | ✅ Done | OP-04 — `tempfile.TemporaryDirectory` cleaned in finally block |
| **Version + update mechanism** | ⏸ Deferred | Internal work only — required pre-retail |
| Data Governance Addendum (vendors) | ✓ Done | — |
| Reference Hardware documented | ✓ Done | — |

---

### Phase 1 — Proxy Generation
**Distribution: Retail (CLI + potential installer)**
**New surface area:** FFmpeg transcoding, larger temp files, new output artifacts

| Requirement | Status | Action Required |
|---|---|---|
| All Phase 0 compliance items | Must be complete | Gate: do not ship Phase 1 without Phase 0 compliance |
| **Proxy files contain embedded metadata** | New risk | Strip or document what metadata proxies carry |
| **Temp transcoding files** | New risk | Secure deletion of intermediate FFmpeg temp files |
| **Proxy storage on encrypted drive** | New risk | Pre-flight must verify proxy output drive encryption |
| **Bandwidth/resource disclosure** | New | Document CPU/disk load for multi-hour proxy jobs |
| **Error handling for corrupt media** | New | Corrupt files must not crash pipeline or leak partial data |
| Installer package (if applicable) | New | Must include EULA acceptance at install time |
| Code signing (macOS Gatekeeper) | New | Required for Mac distribution — Apple notarization |
| Code signing (Windows) | New | Required if Windows distribution planned |

---

### Phase 2+ — AI Editing / Scene Detection / UI
**Distribution: Retail (packaged app)**
**New surface area:** AI inference on media content, GUI, potential cloud features

| Requirement | Status | Action Required |
|---|---|---|
| All Phase 0 + Phase 1 compliance | Must be complete | Gate requirement |
| **AI model transparency** | New | Disclose what models run, what data they see |
| **Biometric data handling** | Critical | If AI analyzes faces: GDPR Art.9, Illinois BIPA, Texas CUBI apply |
| **On-device vs cloud inference** | Critical | Cloud inference = data leaves device = full GDPR/CCPA obligations |
| **Scene detection data retention** | New | Scene metadata is derived personal data — retention policy required |
| **GUI accessibility** | New | WCAG 2.1 AA minimum for retail app |
| **GUI privacy notices** | New | In-app privacy notice required (GDPR Art.13, CCPA §1798.100) |
| **Auto-update mechanism** | New | Security patches must reach users; update mechanism must itself be secure |
| **Crash reporting** | New | If any crash data collected: explicit opt-in required |
| **App store compliance** | New | Apple Mac App Store: privacy nutrition labels, entitlements review |
| **Windows Store compliance** | New | If applicable: Microsoft Partner Center policy review |

---

## Compliant Pre-Flight — Retail Specification

The current pre-flight checks disk space and warns about the system drive.
For retail, it must also capture operator attestation and log it.

### What the compliant pre-flight must do (every run):

1. **Print the full pre-flight summary** (current — ✓ done)
2. **Warn on system drive output** (current — ✓ done)
3. **Verify output drive encryption** (to build)
   - macOS: check if volume is FileVault/APFS encrypted via `diskutil info`
   - Warn if unencrypted; block if `require_encrypted_output: true` in config
4. **Display EULA reference** (to build)
   - First run: display EULA, require `YES` to accept, log acceptance
   - Subsequent runs: confirm acceptance on file, display version
5. **Operator attestation prompt** (to build)
   - Print attestation statement
   - Require typed `YES` to continue
   - Log: timestamp, username (`os.getenv('USER')`), run ID, attestation text hash
6. **Write pre-flight record to audit log** (to build)
   - New log stream: `{run_id}_preflight.json`
   - Contains: timestamp, operator, input path hash (not plaintext), output drive,
     encryption status, EULA version accepted, attestation captured

### Attestation text (plain English, non-negotiable):

```
  BEFORE YOU CONTINUE — please confirm all of the following:

  [ ] I am authorized to process the media files in the input folder
  [ ] These files comply with all applicable NDAs and client agreements
  [ ] I understand that W.E. C.A.P.E. CAPTURE will read every file in the input folder
  [ ] The output drive meets my organization's encryption requirements

  Type YES and press Enter to confirm, or Ctrl+C to cancel.
```

### Pre-flight log record format:

```json
{
  "run_id": "WEF_20260522_183359_12FEDB",
  "event": "preflight_accepted",
  "logged_at": "2026-05-22T18:33:59.000000+00:00",
  "operator": "twork",
  "input_path_hash": "sha256:abc123...",
  "output_drive": "/Volumes/10TB",
  "output_on_system_drive": false,
  "output_drive_encrypted": true,
  "system_drive_free_gb": 147.4,
  "output_drive_free_gb": 887.2,
  "eula_version_accepted": "1.0",
  "attestation_hash": "sha256:xyz789...",
  "file_operation_mode": "symlink"
}
```

---

## Regional Regulatory Matrix

| Regulation | Region | Trigger | Phase 0 | Phase 1 | Phase 2+ |
|---|---|---|---|---|---|
| **GDPR** | EU / UK | Any EU/UK subject data | Attestation + audit logs | + proxy metadata | + AI inference disclosure |
| **CCPA** | California | CA residents' data | Privacy Policy + opt-out notice | Same | + Right to deletion for scene data |
| **PIPEDA** | Canada | Canadian users | Consent documentation | Same | Same |
| **LGPD** | Brazil | Brazilian users | Consent-first processing | Same | Same |
| **POPIA** | South Africa | SA users | Similar to GDPR | Same | Same |
| **BIPA** | Illinois, USA | Biometric identifiers | N/A Phase 0 | N/A | Required if face detection added |
| **CUBI** | Texas, USA | Biometric identifiers | N/A Phase 0 | N/A | Required if face detection added |
| **HIPAA** | USA | Medical information in media | Low risk | Low risk | Flag if medical content detected |

---

## Legal Documents Required Before Retail

These cannot be written by Claude or any AI tool — they require a qualified attorney:

| Document | Required by | Needed for |
|---|---|---|
| **End User License Agreement (EULA)** | All retail distribution | Phase 0 retail |
| **Privacy Policy** | GDPR Art.13, CCPA §1798.100 | Phase 0 retail |
| **Terms of Service** | App store requirements | Phase 0 retail |
| **Data Processing Agreement template** | GDPR Art.28 (B2B sales) | Phase 0 retail |
| **Biometric Data Policy** | BIPA, CUBI, GDPR Art.9 | Phase 2+ only |
| **AI Transparency Statement** | EU AI Act (2026+) | Phase 2+ only |

---

## Security Requirements by Phase

| Control | Phase 0 | Phase 1 | Phase 2+ |
|---|---|---|---|
| Audit log integrity (SHA-256 signing) | Required | Required | Required |
| Secure temp file deletion | Required | Required | Required |
| Output drive encryption check | Required | Required | Required |
| Code signing (macOS notarization) | Required at retail | Required | Required |
| Dependency vulnerability scanning | Recommended | Required | Required |
| Penetration test | Not required | Recommended | Required |
| SOC 2 Type II | Not required | Optional | Recommended for enterprise |

---

## Phase Gate Checklist

Before releasing any phase to retail, all items must be checked:

### Phase 0 Retail Gate
- [ ] EULA drafted by attorney and reviewed
- [ ] Privacy Policy drafted by attorney and reviewed
- [ ] Pre-flight operator attestation implemented and tested
- [ ] EULA acceptance logged to `_preflight.json` on first run
- [ ] Audit log SHA-256 signing implemented
- [ ] Output drive encryption check implemented
- [ ] Secure deletion of temp files implemented
- [ ] macOS code signing + Apple notarization complete
- [ ] Version number + update check mechanism in place
- [ ] DATA_GOVERNANCE.md reviewed by attorney
- [ ] ffprobe installed and multicam grouping validated
- [ ] OM System classification fix tested (config v4.1.1)

### Phase 1 Retail Gate
- [ ] All Phase 0 gate items complete
- [ ] Proxy metadata stripping implemented or documented
- [ ] FFmpeg temp file secure deletion confirmed
- [ ] Installer package includes EULA acceptance
- [ ] Proxy output drive encryption check added to pre-flight

### Phase 2+ Retail Gate
- [ ] All Phase 1 gate items complete
- [ ] AI model transparency statement published
- [ ] Biometric data policy in place (if face/body detection added)
- [ ] On-device vs cloud inference decision documented and disclosed
- [ ] GUI privacy notices implemented
- [ ] App store privacy nutrition labels completed
- [ ] EU AI Act compliance review (if AI features shipped to EU)

---

*This document must be reviewed and updated at every phase gate.*  
*Legal documents must be reviewed by a qualified attorney before retail distribution.*  
*Last updated: 2026-05-27 — status updated per COMPLIANCE_DELTA_v4.8.md*
