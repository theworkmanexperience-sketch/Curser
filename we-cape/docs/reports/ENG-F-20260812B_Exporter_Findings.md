# ENG-F-20260812B — fcpxml_export.py Findings (first production use)
## Governance Status
Document Type: Engineering Finding Note · Normative Authority: None · For: engine channel
Evidence: runs WEF_20260812_181350_1029A5, WEF_20260812_211223_5142A4 + FCP import error at asset r2

F3 — Exporter emits non-FCP-importable formats as primary assets:
12 X5 .insv assets caused FCP to abort the ENTIRE import
("Inappropriate file type or format", first asset). REQUIRED: filter
or reference-flag non-importable formats at generation. Interim
mitigation shipped: scripts/fcpxml_fcp_safe.py post-filter.

F4 — Zero-group runs unsupported: exporter requires MULTICAM/*.json
and refuses singles-only runs (WEF_..._5142A4, 7 files, 0 groups).
REQUIRED: singles-only export path (singles handling already proven
in grouped runs).
