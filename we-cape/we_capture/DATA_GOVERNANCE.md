# W.E. C.A.P.E. — Data Governance

_Last reviewed: 2026-06-23. This document states what the code actually does
today; aspirational items are marked **[planned]**._

## Scope

Governs how W.E. C.A.P.E. CAPTURE handles creator production data: media files,
their derived proxies/scaffolds, and the local production registry
(`~/.wecape/registry/wecape.db`).

## Core guarantees (enforced in code)

- **Local-first / no network egress (P2).** The capture engine makes no network
  calls. There are no HTTP/socket/cloud-SDK imports in the engine; the only
  external process invoked is local `ffmpeg`/`ffprobe`. Verified by audit
  2026-06-23. Cloud sync is opt-in and not present in v1 (`LocalOnlySyncAdapter`
  is a no-op default).
- **Creator data sovereignty (P7).** All originals, proxies, and registry data
  live on creator-controlled storage. Nothing is uploaded by default, ever.
- **Determinism (P1).** Identical input + config yields identical output;
  ingest traversal and grouping are sorted, not order-dependent.
- **Auditable, non-destructive registry (P3, P5).** Every run with ≥1 file is
  recorded. Content records are written with a field-preserving upsert: re-
  ingesting a file never nulls previously captured enrichment (quality scores,
  tags, embeddings). `first_seen` is immutable; empty/no-op runs are pruned and
  excluded from aggregates.
- **Strict audit mode (P3).** By default a run aborts if it cannot write its
  audit record (`registry.strict: true`). Operators may opt out per deployment.
- **Path privacy.** File paths are recorded with SHA-256 hashing in the audit
  log streams (§12). Content identity is the SHA-256 content hash.

## Data retention & creator control

- The registry is append-style local history; the creator may export or delete
  it at any time (it is a single SQLite file under `~/.wecape`).
- Schema is versioned and migrated forward non-destructively (`schema_version`
  table; current v2). Migrations preserve existing rows.
- **[planned]** First-class `export` and `purge` CLI verbs; documented retention
  windows per data class.

## Compliance posture

- Archive Intelligence (Stage 0.5) is Phase-1 gated and disabled by default to
  preserve locked v4.1 retail determinism.
- EULA enforcement and the Phase-0 retail gate were closed 2026-05-25 against
  the locked v4.1 spec.
- **[planned]** RFQ Appendix B quantitative thresholds (Test 6) — pending
  receipt from the contract holder; see CLAUDE.md "RFQ Compliance Notes".
- **Known deviation:** grouping `window_seconds` is 15 (RFQ spec: 5), a
  field-calibrated compensation for DJI/Insta360 clock drift; validated, logged,
  and documented as intentional.

## Open governance gaps (tracked)

- Telemetry-based timestamp correction (`_extract_dji_telemetry`) is not yet
  integrated; the grouping-window deviation above is the interim mitigation.
- Several backup-coverage risks exist at the storage layer (see CLAUDE.md
  "Storage Map") — these are operational, not engine, concerns.
