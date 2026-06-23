# W.E. C.A.P.E. — Codebase Full Audit
**Date:** 2026-06-23 · **Auditor:** Claude (Cowork) · **Scope:** `~/Curser/we-cape` as mounted

---

## 0. What I could and couldn't verify (read this first)

This is the most important section, because it bounds everything below.

- **No chat log was accessible.** You asked me to reference it; `list_sessions` returned none. Your prior conversation history is not reachable from this session. CLAUDE.md is effectively the only persisted context, and CLAUDE.md is a self-report — not an independent source of truth.
- **The mounted folder is not a git repository** (no `.git`). Every commit hash in CLAUDE.md (`04d3910`, `083889c`, `f8c8878`, `940cb62`, etc.), the "Phase 1 COMPLETE" status, and the commit-tagged Measures table are **unverifiable here**. I audited the files as they sit on disk, not the history.
- **The test suite could not be run.** `pytest` is not installed and the sandbox has no PyPI access. The headline **"171/171 passing" is unverified.** Partial positive signal: all 16 `wecape` source modules import cleanly with zero errors.

So: treat the green checkmarks in CLAUDE.md as claims, not facts. Several of them do not survive contact with the code.

---

## 1. Verdict

The working pipeline (`wecape/capture/`) is real, reasonably disciplined, and the privacy guarantee (P2) genuinely holds in code. But the **platform architecture that the entire investment thesis rests on is largely documentation, not implementation.** The extension API, the append-only registry guarantee, and the target package layout are described in CLAUDE.md as if built; on disk they are empty, unused, or contradicted by the code. The gap between the narrative and the artifact is the single biggest risk in this repo.

---

## 2. Findings by severity

### HIGH — the extensibility architecture is not implemented

CLAUDE.md presents `PipelineStage` (ABC) as the spine of the system: *"Every stage — current and future — implements this. This becomes the public extension API at J3."* That is the basis for principle **P4 (Extensibility Without Coupling)** and for the J3 public-API pricing tier ($499–999/seat).

In the actual code:
- **Nothing subclasses `PipelineStage`.** `grep "(PipelineStage)"` across the source returns zero hits.
- **`pipeline.py` never references it** — no `PipelineStage`, `StageContext`, or `StageResult` anywhere in the 728-line orchestrator.
- The one thing called a stage, `ArchiveIntelligenceStage` (`wecape/archive/stage.py`), is a **plain class with no base** and its own ad-hoc `Stage05Result` dataclass.

The ABC is a 105-line file (`wecape/core/stage.py`) that is imported only by its own test. The "public extension API at J3" does not exist as a contract the pipeline obeys; it is aspirational scaffolding. **The unspoken truth: you are pricing and roadmapping (J3, J5) against an architecture you have documented but not built.** Every J-tier slide assumes this seam exists.

### HIGH — registry overwrites content, contradicting P5

Principle **P5** states the registry is *"append-only, never overwritten."* `wecape/registry/writer.py:124` does:

```python
INSERT OR REPLACE INTO content (...) VALUES (...)
```

`INSERT OR REPLACE` deletes the existing row and inserts a new one. `write_content` builds its column list only from the fields the caller passes, so **any enrichment column not supplied on a later write is silently reset** (NULL/default). The at-risk columns are exactly the ones that make the registry valuable later: `quality_score`, `content_tags`, `alignment_offset_ms`, `highlight_score`, `model_version`, `embedding_*`.

Concretely: the moment J2/J3/J4 ever re-ingest a file (same hash) without recomputing every AI field, the prior AI results are wiped. This **directly undermines the J5 "cross-project content registry"** that is the platform's most valuable claimed asset — and it violates the principle the compliance story is built on. `write_stage_result` and `finalize_run` also use `UPDATE`, so "append-only" is not true at the row level today.

### MEDIUM–HIGH — the documented empty-run guard does not exist

CLAUDE.md, "Known Registry Anomaly": *"Rule: All aggregate queries must include `WHERE file_count > 0`"* to exclude the garbage run `WEF_20260622_020843_66257B` (0 files, ran against an empty source mid-rsync).

That rule is **not implemented anywhere.** `wecape/registry/reader.py` `list_runs()` (line 32) is a bare `SELECT * FROM runs ORDER BY timestamp DESC` with no filter, and `search_content`/`get_run_summary` have no equivalent. Worse, the anomaly is structural, not incidental: `write_run` inserts the run row **at run start, before any content is known** (`pipeline.py:~356`), and nothing deletes or flags it if the source turns out empty. So the bad run is persisted and will surface in any listing or aggregate. The "rule" is a comment in a doc, not a safeguard in code.

### MEDIUM — registry (audit trail) failures are silently swallowed

`pipeline.py` wraps all registry I/O in try/except that sets `self._registry = None` and prints a warning (`:70–85`, `:364`, `:621`). A run can therefore **complete successfully while writing no audit record at all**, leaving only console output. For a product whose pitch is *"Compliance first-class / Auditability built into every stage"* (P3: *"every run produces a complete manifest"*), a best-effort, failure-is-invisible audit trail is a contradiction. Robustness of the pipeline is good; doing it silently is the problem.

### MEDIUM — the wecape/ migration is half-finished

CLAUDE.md marks the migration "COMPLETE (083889c)" and states *"Test file location after reorganization: `wecape/tests/`."* On disk:
- Source did move: `we_capture/engine/` and `we_capture/archive_engine/` **no longer exist** (only 236 LOC of leftovers in `we_capture/`; the real 4,692 LOC are in `wecape/`).
- But **112 of the 171 test files still physically live in `we_capture/tests/`** — they just import `wecape.capture.*`. Only 59 tests are in `wecape/tests/`.
- `we_capture/` still holds the live `main.py`, `config.yaml`, and `profiles/`. There are effectively **two package roots**, and the entry point is still the old one.

The "171" reconciles only as `112 (we_capture) + 112... `→ 112 + 59 = 171. It is a sum across two trees, not a clean suite in `wecape/`.

### MEDIUM — the "Target Package Structure" is mostly empty stubs

CLAUDE.md's Target layout is presented as the Phase-2 destination. Reality:

| Target dir | Documented contents | On disk |
|---|---|---|
| `wecape/core/` | stage, sync, manifest, **config, errors** | stage, sync, manifest only — **config.py and errors.py missing** |
| `wecape/flow/` | ingest, archive, scaffold, proxy, audit, main | **empty** (`__init__.py` only) — code actually lives in `wecape/capture/` |
| `wecape/sync/` | local, lan, cloud | **empty** — `LocalOnlySyncAdapter` is in `core/sync.py` instead |
| `wecape/api/` | extensions, contracts | **empty** |
| `wecape/intelligence/` | camera, quality, alignment, editorial | **empty** (expected — J1+) |
| `wecape/registry/` | schema, writer, reader | present and complete ✓ |

So the namespace exists but the working code went to `capture/`, not the documented `flow/`, and four of the target subpackages are placeholder directories. The diagram in CLAUDE.md describes an intended state, not the built one.

### LOW–MEDIUM — the rebrand leaked into the schema

The June 22 rebrand (FORGE→C.A.P.E.) is incomplete in code: **21 `forge`/`flow` references remain** in source, including ones baked into the data layer — the registry column **`we_forge_version`**, the constant `WEFORGE_VERSION` (`core/manifest.py:25`), and `_weforge_root` path vars. Because the column name is in the SQLite schema, fixing it later requires a **migration**, not a rename. Today every audit/manifest record is literally stamped `we_forge_version`. (CLAUDE.md's own schema block also says `we_forge_version`, so it is "consistent" — but consistently wrong post-rebrand.)

### LOW — the DJI telemetry feature is a dead stub, and you're shipping a workaround for it

`_extract_dji_telemetry` (`wecape/capture/timestamp.py:47`) is **defined, never called, and has no tests** — confirmed against CLAUDE.md's own note. This matters more than "unfinished function": it is the root-cause fix for the camera clock drift that forced your **RFQ §7 deviation** (grouping window widened from the spec's 5s to 15s). You are documenting a spec deviation as "field calibration" to compensate for an enrichment feature that was scaffolded and abandoned. Defensible short-term; worth naming honestly as deferred work, not a permanent calibration.

### LOW — repo hygiene

- **Four 0-byte junk files at the repo root** — `1`, `4`, `~60`, `v4.8` — are stray shell-redirect artifacts (e.g. `… > 1`, `… > v4.8`). Harmless but they're sitting in what you're calling a commercial codebase.
- **Documentation sprawl:** 21 markdown docs at the top two levels, including six `COMPLIANCE_DELTA_v4.x` files and two `EXECUTIVE_SUMMARY` versions. Hard to tell which is current.
- `DATA_GOVERNANCE.md` is a **9-line stub** for a product whose central differentiator is compliance.

---

## 3. What's actually solid (so this isn't all teeth)

- **P2 (Privacy) holds in code.** No `socket`/`urllib`/`requests`/`http`/cloud-SDK imports anywhere in `wecape` source. The only `connect()` is local `sqlite3`. The "local engine cannot make network calls" claim is true today.
- **No secrets in the repo.** No API keys, tokens, or rclone config committed. ffmpeg/ffprobe are invoked via `subprocess`, as expected.
- **Determinism (P1) is respected on the hot path.** Main ingest traversal is `sorted(input_path.rglob('*'))` (`pipeline.py:686`); grouping sorts by `(timestamp, filename)`; profile loading sorts globs. Reproducibility is designed in, not accidental.
- **Registry isolation for tests** — pipeline refuses to write to the production DB in test mode (`pipeline.py:75`). Good instinct.
- **Schema is complete** — all four documented tables (`runs`, `content`, `preferences`, `schema_version`) exist as specified.
- **Clean imports** — 16/16 source modules load without error.

---

## 4. Claim-vs-reality scorecard

| CLAUDE.md claim | Reality on disk |
|---|---|
| 171/171 tests passing | **Unverifiable** (no pytest/PyPI); 112 tests still in old tree |
| PipelineStage = public extension API | **Unused** — 0 subclasses, not referenced by pipeline |
| Registry append-only, never overwritten (P5) | **Contradicted** — `INSERT OR REPLACE` + `UPDATE` |
| Aggregate queries filter `file_count > 0` | **Not implemented** in reader.py |
| Local engine makes no network calls (P2) | **True** ✓ |
| Deterministic (P1) | **True on hot path** ✓ |
| wecape/ migration COMPLETE | **Partial** — tests + entry point still in we_capture/ |
| Rebrand FORGE→C.A.P.E. complete | **Partial** — `we_forge_version` in schema, 21 refs remain |
| Compliance/audit first-class (P3) | **Aspirational** — audit writes are best-effort/silent; governance doc is a stub |

---

## 5. Recommended order of operations

1. **Decide what `PipelineStage` is for.** Either make `ArchiveIntelligenceStage` and the capture stages actually implement it (so P4/J3 are real), or stop advertising it as the extension API. Right now it's neither.
2. **Fix `write_content` before the registry accumulates value.** Move to column-wise `UPDATE … SET` that preserves unspecified fields, or `INSERT … ON CONFLICT DO UPDATE` with an explicit field list. Do this *now* — every run makes the eventual data-loss surface bigger.
3. **Implement the empty-run guard you already documented** — filter `file_count > 0` in `reader.py`, and don't persist a run row until at least one file is confirmed (or delete it on empty finalize).
4. **Decide if audit failures should be fatal.** For a compliance product, a run that can't write its audit record arguably shouldn't be called a success.
5. **Finish the migration or stop claiming it's done** — move the 112 tests, retire `we_capture/`'s duplicate `main.py`/`config.yaml`, update CLAUDE.md's structure diagrams to match `capture/`.
6. **Plan the `we_forge_version` schema migration** while the registry is still small.
7. **Housekeeping:** delete the 0-byte junk files; consolidate the compliance/exec-summary doc versions; expand `DATA_GOVERNANCE.md`.

---

*Audit limited to static inspection of the mounted working tree. Re-run against the actual git repo with the test suite installed to confirm §0 items.*
