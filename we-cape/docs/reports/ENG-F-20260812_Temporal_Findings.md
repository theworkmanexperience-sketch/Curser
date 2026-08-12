# ENG-F-20260812 — Temporal Authority Findings (registry-proven)
## Governance Status
Document Type: Engineering Finding Note · Normative Authority: None · For: Claude Code channel ingestion
Evidence: run WEF_20260812_181350_1029A5 · registry content rows P6260017.JPG/.ORF, P6260018.MOV

F1 — corrected_timestamp mixes semantics: mtime-path rows are true UTC
(05:34:40Z = 00:34:40 CDT), embedded-path rows are naive camera-local
mislabeled +00:00 (MOV embedded 01:06:21 vs own local mtime ~01:11 —
a ~5-min clip; true-UTC reading would imply a 5-hour gap). REQUIRED:
per-camera declared timezone (shoot.yaml trusted-clock/SOP-04 field)
as normalization key; store UTC + offset; display local.

F2 — metadata column empty: no timestamp_source / confidence /
fallback level survives to the row. Registry states WHEN without
HOW-KNOWN. REQUIRED: timestamp_source, timestamp_confidence,
tz_semantics as first-class columns (Stage 2 already computes all three).

Context: temporal-authority principle (Chairman, 2026-08-12) — machine
evidence chain outranks human recollection; these findings are the two
gaps between that principle and the current registry row.
