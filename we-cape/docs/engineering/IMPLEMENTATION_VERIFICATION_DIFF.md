# IMPLEMENTATION VERIFICATION DIFF — ECR-GEN-001

**Task Order:** `ECR-GEN-001` · **Custody:** `IMPLEMENTATION / CODEBASE ONLY` · **Date:** 2026-08-29

**Subject:** `gen_artifacts.py` → `gen_artifacts_v2.py`, plus `fcpx_resolve.py` and one new producer.

> **Every change below is to CODE. No governed artifact, registry or Executive declaration is touched.**


---

## 0 · Change summary

| file | change | lines |
|---|---|---|
| `gen_artifacts.py` → `gen_artifacts_v2.py` | constants and embedded measurement data replaced by supplied context + observations | **1501 → 1232**, +87 / −356, 17 hunks |
| `fcpx_resolve.py` | ETC argument accepts `NONE`; reports `etc_validation: NOT_VALIDATED` instead of proceeding | +14 |
| `derive_camera_runs.py` | **NEW** — replaces the orphan `camera_runs.json` with a deterministic derivation | +49 |


## 1 · What moved out of the code, and where it went

| literal block, was in source | entries | now supplied by |
|---|---|---|
| `segments` | 19 | `--observations` |
| `cues` | 15 | `--observations` |
| `visual_events` | 39 | `--observations` |
| `not_observed` | 5 | `--observations` |
| `delta_ledger` | 26 | `--observations` |
| `progressions` | 5 | `--observations` |
| `voice_over` | 4 | `--observations` |
| `energy` | 19 | `--observations` |
| `offset_model.per_segment` | 19 | `--observations` |
| `anchors` | 11 | `--observations` |
| four input SHA-256 pins | 4 | `--context` |
| `LOCK` runtime | 1 | `--context` |
| `GIT` commit | 1 | `--context` |
| `RUN_ID` / `REGEN_RUN_ID` | 2 | `--context` / `--run-id` |
| `RULING` (ESS-004) | 1 | `--context` |
| DIE-V thresholds | 4 | `--observations` |
| source-file paths | 3 | `--context` + `--sources` |


## 2 · The diff, by hunk

Full unified diff at `scripts/verification.diff`. Every hunk classified:

| # | at | what changed | class |
|---|---|---|---|
| 1 | `@@ -1,46 +1,64 @@` | constants + loaders -> CLI, context, observations | REPLACE |
| 2 | `@@ -58,8 +76,5 @@` | literal table -> OBS_DS lookup | REPLACE |
| 3 | `@@ -69,15 +84,5 @@` | literal table -> OBS_DS lookup | REPLACE |
| 4 | `@@ -91,187 +96,6 @@` | literal table -> OBS_DS lookup | REPLACE |
| 5 | `@@ -287,8 +111,5 @@` | literal table -> OBS_DS lookup | REPLACE |
| 6 | `@@ -299,94 +120,5 @@` | literal table -> OBS_DS lookup | REPLACE |
| 7 | `@@ -415,5 +147,5 @@` | prose constant -> context interpolation | TEMPLATE |
| 8 | `@@ -438,8 +170,8 @@` | prose constant -> context interpolation | TEMPLATE |
| 9 | `@@ -486,5 +218,5 @@` | literal -> supplied value | REPLACE |
| 10 | `@@ -525,5 +257,5 @@` | literal -> supplied value | REPLACE |
| 11 | `@@ -542,5 +274,5 @@` | literal -> supplied value | REPLACE |
| 12 | `@@ -627,9 +359,11 @@` | literal table -> OBS_DS lookup | REPLACE |
| 13 | `@@ -717,10 +451,7 @@` | literal table -> OBS_DS lookup | REPLACE |
| 14 | `@@ -849,5 +580,5 @@` | literal -> supplied value | REPLACE |
| 15 | `@@ -1268,9 +999,9 @@` | prose constant -> context interpolation | TEMPLATE |
| 16 | `@@ -1279,5 +1010,5 @@` | literal -> supplied value | REPLACE |
| 17 | `@@ -1433,5 +1164,5 @@` | prose constant -> context interpolation | TEMPLATE |

**No hunk changes control flow, arithmetic, formatting or output ordering.** Classes used: REPLACE, TEMPLATE. That claim is not an assertion — §3 proves it.


## 3 · Proof the diff changed no behaviour

Both generators run on identical inputs; output compared byte-for-byte.

```
artifact                            sha256 v1          sha256 v2          verdict

STEP0_TIMING_CLOSURE.md             ca84b369f0dca2cc   ca84b369f0dca2cc   IDENTICAL
CAPTION_REGISTRY.yaml               3cdb1d8cae8dfbe0   3cdb1d8cae8dfbe0   IDENTICAL
VISUAL_EVENT_REGISTRY.yaml          802ae9973e5c8527   802ae9973e5c8527   IDENTICAL
EDITORIAL_SYNCHRONIZATION.yaml      f205ee412fd54f13   f205ee412fd54f13   IDENTICAL
CONDUCTOR_SCORE.yaml                fc481954623c63e3   fc481954623c63e3   IDENTICAL
ESS_VALIDATION_REPORT.md            ccd53e2c9f138c76   ccd53e2c9f138c76   IDENTICAL
PRODUCTION_INTELLIGENCE_SEED.yaml   bc0c6c6670fe94f7   bc0c6c6670fe94f7   IDENTICAL
```

**7 of 7 byte-identical.**


## 4 · Independent corroboration against the repository

The committed generator, re-run today from source, reproduces the committed artifacts:

```
artifact                            committed          regenerated        verdict

STEP0_TIMING_CLOSURE.md             ca84b369f0dca2cc   ca84b369f0dca2cc   MATCH
CAPTION_REGISTRY.yaml               3cdb1d8cae8dfbe0   3cdb1d8cae8dfbe0   MATCH
VISUAL_EVENT_REGISTRY.yaml          802ae9973e5c8527   802ae9973e5c8527   MATCH
EDITORIAL_SYNCHRONIZATION.yaml      f205ee412fd54f13   f205ee412fd54f13   MATCH
CONDUCTOR_SCORE.yaml                1464e33595add5b6   fc481954623c63e3   *** STALE IN REPO ***
ESS_VALIDATION_REPORT.md            ccd53e2c9f138c76   ccd53e2c9f138c76   MATCH
PRODUCTION_INTELLIGENCE_SEED.yaml   bc0c6c6670fe94f7   bc0c6c6670fe94f7   MATCH
```

**Six of seven match**, which validates the reconstructed intermediates. The seventh is a pre-existing repository drift, not a product of this task — see the Conformance Report §4.1.


## 5 · New producer, validated

`derive_camera_runs.py` replaces an input that no committed script produced.

```
            derived    committed
X5          2553.9     2553.9
DJI         1791.6     1791.6
COMPOUND     425.4      425.4
OM1           75.8       75.8
runs           191
```

**Exact on all four families.**


---

*Custody `IMPLEMENTATION / CODEBASE ONLY`. Code only. No governed artifact regenerated; no Executive content altered.*
