# Data Governance & Privacy Addendum
## W.E. FLOW / W.E. FORGE — RFQ Package

**Issued by:** The Workman Experience, LLC  
**Applies to:** All vendors receiving benchmark datasets under this RFQ

---

## 1. Benchmark Dataset Classification

Benchmark datasets distributed under this RFQ may contain:
- Real footage of identifiable individuals (talent, crew, event attendees)
- GPS/location metadata embedded in media files (EXIF, MP4 creation metadata)
- Device serial numbers and operator identifiers in file metadata
- Proprietary/unreleased commercial content under active distribution agreements

Datasets are classified **Confidential** unless explicitly marked otherwise.

---

## 2. Vendor Obligations

By accepting a benchmark dataset, the vendor agrees to:

1. **Use limitation** — Dataset is licensed for acceptance testing purposes only. No secondary use, publication, training data, or commercial exploitation.
2. **Retention limit** — All dataset files must be deleted within 30 days of contract award or disqualification, whichever comes first.
3. **No redistribution** — Dataset may not be shared with subcontractors, affiliates, or third parties without written consent.
4. **Metadata handling** — Embedded metadata (GPS, device IDs, timestamps) must be treated as confidential and not extracted or published separately.
5. **Secure storage** — Dataset must be stored on encrypted drives (AES-256 or equivalent) during the testing period.

---

## 3. Personally Identifiable Information (PII)

Media files may contain biometric data (faces) and location data subject to:
- **GDPR** (EU/UK subjects)
- **CCPA** (California residents)
- **Illinois BIPA** (biometric identifiers)

Vendors must not perform facial recognition, biometric extraction, or location profiling on any benchmark dataset.

---

## 4. Chain of Custody

The W.E. FLOW engine generates five mandatory audit log streams (§12):
- `ingest.json` — SHA-256 hash of every file at ingest time
- `classification.json` — Classification decision per file
- `grouping.json` — Multicam group assignments
- `variants.json` — Parent-child variant links
- `errors.json` — All processing errors

These logs constitute the chain of custody for all benchmark runs. Vendors must submit the complete `LOGS/` folder with their acceptance test results. Results submitted without logs will be disqualified.

---

## 5. Audit Log Retention

| Log type | Retention | Access |
|---|---|---|
| Ingest + Classification | 90 days | Project leads only |
| Grouping + Variants | 90 days | Project leads only |
| Errors | 90 days | Project leads + engineering |
| Run summaries | 1 year | Authorized staff |

Logs are stored locally on encrypted drives. Logs must not be synced to iCloud, Dropbox, or other cloud storage without explicit authorization.

---

## 6. Pre-Distribution Checklist

Before distributing any benchmark dataset to a vendor, confirm:

- [ ] Talent/subject releases cover vendor/commercial testing use
- [ ] NDA signed and on file for receiving vendor
- [ ] GPS metadata scrubbed from sample files (use `exiftool -gps:all= -overwrite_original`)
- [ ] No unreleased client deliverables included in dataset
- [ ] Dataset size and file list documented in delivery receipt
- [ ] Vendor deletion deadline communicated in writing

---

## 7. Incident Response

If a vendor reports unauthorized access, data breach, or accidental disclosure:
1. Notify The Workman Experience, LLC within 24 hours
2. Preserve all access logs
3. Do not delete or modify affected files until instructed
4. Cooperate fully with any investigation

---

*This addendum is incorporated by reference into all RFQ responses and vendor contracts.*
