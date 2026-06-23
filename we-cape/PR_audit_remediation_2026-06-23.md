# Audit Remediation + run_stages() Rewire — 2026-06-23

**Branch suggestion:** `audit-remediation-2026-06-23`
**Status:** ready to commit/push · 189/189 tests green · equivalence-validated on synthetic + real footage

---

## Summary

A full codebase audit (see `CODEBASE_AUDIT_2026-06-23.md`) found that several
architectural claims in `CLAUDE.md` were documentation-only. This change makes
them true in code, fixes two real data-integrity bugs, finishes the half-done
`wecape/` migration, and rewires the production orchestrator to run through the
`PipelineStage` seam — all without breaking the proven pipeline (legacy path is
retained behind a flag for instant rollback).

Test count: **171 → 189** (18 new tests). All green via `pytest wecape/tests/`
and the pytest-free `run_tests.py`.

---

## Changes

### Data integrity (registry)
- **Field-preserving content writes (P5).** `RegistryWriter.write_content` now
  uses `INSERT … ON CONFLICT(id) DO UPDATE` with `COALESCE`, so re-ingesting a
  file never nulls prior enrichment (quality scores, tags, embeddings). Was
  `INSERT OR REPLACE`, which silently wiped columns.
- **Empty-run guard.** `reader.list_runs`/`get_aggregate_stats` exclude
  `file_count = 0` by default; `finalize_run` prunes a run that ends with zero
  files. Implements the previously docs-only rule for the `WEF_20260622_020843`
  anomaly.
- **Schema v2 migration.** `runs.we_forge_version → we_cape_version`, applied
  idempotently and losslessly on registry open (`schema.migrate()`); legacy v1
  DBs auto-upgrade. Rebrand also swept from manifest/constants.

### Architecture (PipelineStage seam)
- **Stage contract made real.** `wecape/capture/stages.py` adds conforming
  Archive/Classify/Group/Variant/Proxy stages; `core/stage.run_stages()` is the
  reusable driver (validate → execute → mandatory registry write → on_error).
- **Production pipeline rewired.** `pipeline.run()` now routes the 7 main stages
  through `run_stages()` by default. The 7 blocks were extracted to `_stage_*`
  methods sharing a `StageContext`; the **same methods** back a `legacy` path
  (`pipeline.engine: legacy` or `--engine legacy`) for rollback. Proxy + registry
  + audit-close remain in the always-run `finally`.
- **Strict audit mode (P3).** `registry.strict: true` (default) aborts a run that
  can't write its audit record, via new `core/errors.RegistryAuditError`.
- **AI hook placeholder (P6).** Disabled `_NullIntelligenceStage`; appended only
  when `intelligence.enabled: true`. v1 still ships zero AI.

### Migration finished
- All tests moved to `wecape/tests/`; `config.yaml` + `profiles/` moved to
  `wecape/`; entry point is `python -m wecape`; `we_capture/` reduced to
  deprecation shims.
- **Bug fixed by the move:** `ProfileLoader` resolved `wecape/profiles/`, which
  didn't exist — `--profile ryderz` was silently broken. Now works.

### CLI fixes (found during real-footage validation)
- `--proxy` now enables proxies with **or without** `--profile` (was silently
  ignored unless a profile was passed).
- Added `--engine stages|legacy` for per-run engine selection (A/B testing /
  rollback without editing config).

### Housekeeping / docs
- `.weflow → .wecape` paths; 0-byte junk files quarantined to `.trash_junk/`;
  `DATA_GOVERNANCE.md` expanded from a 9-line stub.
- `CLAUDE.md` corrected to match reality (structure, test count/command, schema,
  resolved registry anomaly, remediation log).
- Added `VALIDATION_PROTOCOL.md` (real-footage A/B procedure).

---

## Validation

- **Unit/integration:** 189/189 pass (`pytest wecape/tests/ -q`).
- **Synthetic equivalence:** generated 1080p multicam footage (GoPro/DJI/Insta360)
  — `legacy` vs `stages` produced identical metrics, output tree, and audit-log
  counts (2 groups, 1 variant, 7 proxies).
- **Real-footage equivalence:** 6-file DJI shoot (11.5 GB) — `legacy` vs `stages`
  → **TREES IDENTICAL**, `Files: 6 | Groups: 0 | Variants: 0 | Errors: 0`. Proxy
  stage transcoded 5/6 (1 correctly skipped: no video stream), 0 failed.

---

## Behavioral notes / breaking changes

- Registry **auto-migrates v1 → v2** on first open. Back up
  `~/.wecape/registry/wecape.db` before first run (lossless, but no undo).
- Default orchestration is now `engine: stages`. Set `pipeline.engine: legacy`
  (or `--engine legacy`) to roll back instantly.
- `stages` additionally writes per-stage results to `runs.stage_results`
  (audit gain) — the one intentional difference vs the legacy path.

## Known gaps / follow-ups

- **Real multicam grouping untested on real footage** — validation card was
  single-camera (0 groups was correct). Confirm on the next 2+ camera shoot.
- `archive_engine.enabled: true` in the active config — spec says off by default;
  confirm intent.
- `core/config.py` from the Target structure still not present (config still
  loaded via `capture/profile.py`).
- DJI telemetry timestamp correction (`_extract_dji_telemetry`) still an
  unintegrated stub; grouping-window deviation (±15s) remains the interim
  mitigation.

---

## Key files

```
NEW   wecape/core/errors.py, wecape/capture/stages.py, wecape/__main__.py,
      wecape/capture/main.py, VALIDATION_PROTOCOL.md, CODEBASE_AUDIT_2026-06-23.md
EDIT  wecape/capture/pipeline.py (rewire), core/stage.py (run_stages),
      registry/{writer,reader,schema}.py, capture/profile.py, config.yaml, CLAUDE.md
TESTS wecape/tests/test_{registry_preservation,registry_empty_runs,strict_audit,
      pipeline_stages,schema_migration,engine_equivalence}.py
MOVED we_capture/tests → wecape/tests ; we_capture/{config.yaml,profiles} → wecape/
```
