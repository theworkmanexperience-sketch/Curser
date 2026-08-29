# ECR-GEN-001 — CONFORMANCE REPORT

**Task Order:** `ENGINEERING TASK ORDER — ECR-GEN-001` · **Custody:** `IMPLEMENTATION / CODEBASE ONLY`
**Date:** 2026-08-29 · **Phases:** A complete · B partial (two blocked) · C delivered
**Production under conformance:** Alpha RoundUp 2026 — Day 2 Episodic Trilogy (08-24 Lineage)

> **NO GOVERNED ARTIFACT WAS REGENERATED. NO EXECUTIVE CONTENT WAS ALTERED.**
> All generator output written during this task went to scratch directories and none of it is
> committed as a governed artifact.

---

## 0 · Result

| acceptance criterion (Order §Acceptance) | result |
|---|---|
| generator accepts 08-24 inputs dynamically | **MET** — resolves the 08-24 FCPXML, 1096 elements, spine closes at 4689.500 s |
| no 08-22 constants remain | **MET** — 0 occurrences across 10 constant classes |
| retirement of EPR-07 handled without exceptions | **MET** — consumer skips it, returns 6 active beats, no exception |
| parameterized RUN_ID generation functions correctly | **MET** — `auto` yields `WECAPE-AR2-0822-20260829-005139`; `pinned` reproduces the archived id |
| validation suite passes | **8 PASS · 2 BLOCKED · 2 FAIL** — see §4 |
| `DOC-001` instrument agreement satisfied | **MET for the 08-22 baseline. NOT DEMONSTRABLE for the 08-24 lineage** — no ETC exists (T3) |
| no Executive content changed | **MET** — verified byte-level, §5 |

**The single strongest piece of evidence in this report:** the refactored generator, given the
08-22 context, produces **all seven artifacts byte-identical** to the committed generator's output
on identical inputs. **The refactor changed no behaviour.**

---

## 1 · What was wrong, measured

`GER-001` reported the generator was hard-coded to the superseded assembly. Inspection found the
problem is **larger than constants.**

| finding | measurement |
|---|---|
| production constants | 4 input hashes, `LOCK=4846.625`, `GIT`, 2 `RUN_ID` strings |
| **embedded measurement data** | **19 segments · 15 cues · 39 visual events · 26 delta-ledger entries · 5 not-observed entries · 5 progressions · 4 voice-over spans · 19 energy values** — all as Python literals |
| timeline-scale numeric literals after line 85 | **164** |
| prose lines carrying `4846` | **23** |
| the five JSON inputs | referenced on **15 lines in total** out of 1501 |

> **`gen_artifacts.py` was not a generator. It was a serializer for one measurement run, with that
> run's results pasted into the source.** The five "inputs" supplied almost nothing; the artifact
> content lived in the code.

**Three inputs had no producer at all:**

| input | required by | status |
|---|---|---|
| `camera_runs.json` | `gen_artifacts.py` | **RESOLVED this task** — `derive_camera_runs.py` written |
| `video_obs_2fps.npy` | `die_v_observables.py` | **still unproduceable** |
| `audio_rms_0p25.npy` | `step0_offset.py` | **still unproduceable** |

---

## 2 · Phase A — what was built

### 2.1 Separation of context, observation and code

```
gen_artifacts_v2.py  --context CTX.json --observations OBS.json
                     --derived DIR --sources DIR --out DIR --run-id ID|auto|pinned
```

| file | holds |
|---|---|
| **context** | production identity · lineage status · runtime · frame rate · resolution · four input hashes · git commit · RUN_ID policy · proxy facts · SRT facts · ETC facts · source-file names · the ESS-004 ruling |
| **observations** | segments · cues · visual events · not-observed · delta ledger · audio sources · progressions · energy · voice-over · offset model · anchors · DIE-V thresholds |
| **code** | serialization logic and nothing else |

`gen_artifacts.py` **1501 → 1232 lines**, `+87 / −356`, 17 hunks. The reduction is data leaving
the source.

### 2.2 `derive_camera_runs.py` — a missing producer, written and validated

Camera family is parsed from the FCPXML clip name — an editorial fact, not a visual observation.
Validated against the committed baseline:

```
derived        X5 2553.9   DJI 1791.6   COMPOUND 425.4   OM1 75.8      (191 runs)
committed      X5 2553.9   DJI 1791.6   COMPOUND 425.4   OM1 75.8
```

**Exact on all four families.** An orphan input is now a deterministic derivation.

### 2.3 `fcpx_resolve.py` — the ETC is now optional

Passing `NONE` runs the resolver and reports `etc_validation: NOT_VALIDATED` with a reason,
**rather than proceeding as though validation had occurred.** Verified the 08-22 resolve is
byte-unchanged by this edit.

---

## 3 · Phase A verification — the regression proof

**Method.** Rebuild the five intermediates, run the **committed** generator (v1) and the
**refactored** generator (v2) on identical inputs, compare byte-for-byte.

```
artifact                            sha256 (v1)        sha256 (v2)        verdict
STEP0_TIMING_CLOSURE.md             ca84b369f0dca2cc   ca84b369f0dca2cc   IDENTICAL
CAPTION_REGISTRY.yaml               3cdb1d8cae8dfbe0   3cdb1d8cae8dfbe0   IDENTICAL
VISUAL_EVENT_REGISTRY.yaml          802ae9973e5c8527   802ae9973e5c8527   IDENTICAL
EDITORIAL_SYNCHRONIZATION.yaml      f205ee412fd54f13   f205ee412fd54f13   IDENTICAL
CONDUCTOR_SCORE.yaml                fc481954623c63e3   fc481954623c63e3   IDENTICAL
ESS_VALIDATION_REPORT.md            ccd53e2c9f138c76   ccd53e2c9f138c76   IDENTICAL
PRODUCTION_INTELLIGENCE_SEED.yaml   bc0c6c6670fe94f7   bc0c6c6670fe94f7   IDENTICAL
```

**7 of 7 byte-identical.** This is the `DOC-001` instrument agreement for the refactor: the
instrument was validated by conformance against a known-good result before being trusted on new
material.

**Independent corroboration.** **Six of the seven committed artifacts reproduce byte-identically
from source** — meaning the reconstructed intermediates are exactly right and the 08-22 pipeline
is genuinely reproducible. The seventh is §4's `T11`.

---

## 4 · Phase B — conformance against the 08-24 lineage

| id | test | status | measurement |
|---|---|---|---|
| **T1** | FCPXML ingestion | **PASS** | 1096 elements; spine closes at `4689.5` = sequence `4689.5` |
| **T2** | SRT ingestion | **PASS** | 2036 cues; sha `2a16dd700148488f…`; last cue `4688.958` s |
| **T3** | ETC binding | **BLOCKED** | `NOT_PRODUCED` |
| **T4** | Segment binding | **BLOCKED** | no observation dataset exists for 08-24 |
| **T5** | Caption binding | **PASS** | 65 titles resolved; 2036 SRT cues |
| **T6** | EPR-001 integration | **PASS** | v1.13.0, 7 entries, 19 segment_refs `S01..S19` |
| **T7** | EPR-07 retirement | **PASS** | consumer skipped it, 6 active beats, no exception |
| **T8** | RUN_ID generation | **PASS** | `auto` ≠ `pinned`, correct prefix |
| **T9** | no 08-22 constants | **PASS** | 0 across 10 classes |
| **T10** | refactor equivalence | **PASS** | 7/7 byte-identical |
| **T11** | committed artifacts match committed generator | **FAIL** | 1 of 7 stale — see below |
| **T12** | every input has a producer | **FAIL** | 2 still unproduceable |

Measured facts for the governed lineage, all matching the custody record:

```
Info_analysiscut.fcpxml   1ab3d12f0dd150c6…   4689.500 s   1096 elements   225 depth-0
                          201 primary spine (excl. transitions)   65 titles   178 transitions
srt_analysiscut.srt       2a16dd700148488f…   2036 cues   0.375 s -> 4688.958 s
camera families           X5 2486.7  DJI 1747.1  COMPOUND 380.0  OM1 75.8
```

### 4.1 `T11` — the repository is carrying a stale governed artifact

**`CONDUCTOR_SCORE.yaml` in the repository is not what the committed generator produces.**

```
committed CONDUCTOR_SCORE.yaml   1464e335…   contains instrumentation_guidance      x13
committed generator produces     fc481954…   contains inherited_expressive_guidance x13
```

Git history explains it:

```
3054bed  gov(ess-004): artifacts regenerated          <- CONDUCTOR_SCORE.yaml last written here
319f234  impl(cs): Option C implemented - inherited expressive guidance frozen
0f3d12c  prod(mie): MOTION sidechain corrected
```

**The generator was committed twice after the artifact was last regenerated.** Two
Executive-dispositioned changes — the Option C inherited-expressive-guidance treatment and the
MOTION `DUCK` sidechain correction — **exist in the generator and not in the artifact.** Under
`DOC-002` (*regenerate, never patch*) and `ADR-009` §2 (*regenerate-on-mismatch, never
hand-edited*) this is a live drift condition.

**Reported, not corrected.** Correcting it means regenerating a governed artifact, which this
Order forbids and `GER-001`'s exceptions independently block.

### 4.2 `T3` and `T4` — why they are blocked and what unblocks them

**`T3`.** No Editorial Timing Contract exists for the 08-24 lineage. The resolver now says so
explicitly instead of proceeding. **`DOC-001` instrument agreement cannot be demonstrated for this
lineage until an ETC is produced** — the 191/191 agreement on record is against the *08-22* ETC.

**`T4`.** The generator no longer contains a segment table; it accepts one. **None exists for the
08-24 lineage.** Deriving it is measurement, and ratifying it is Executive. The blocker moved from
*"the code hard-codes the wrong segments"* to *"the right segments have not been declared"* —
which is the correct place for it to sit.

---

## 5 · Constraint compliance

| Order constraint — engineering SHALL NOT | evidence |
|---|---|
| alter Executive declarations | `EMOTIONAL_PROGRESSION_REGISTRY.yaml` was **read only**. No write path touches it |
| alter EPR narrative fields | none touched; `T6`/`T7` are read-only consumers |
| alter governing registries | no registry written |
| regenerate production artifacts | all output went to `out0822/`, `out_v1/`, `out_auto/`, `out0824/` — **scratch only** |
| overwrite approved outputs | `base/` copies are read-only comparison inputs |
| infer missing Executive values | none inferred; `T3`/`T4` are reported `BLOCKED` rather than filled |

| Order constraint — engineering SHALL | evidence |
|---|---|
| report implementation defects | `T11` stale artifact · `T12` missing producers · dead paths in `epr_validate.py` (carried from the Path B report) |
| report unresolved dependencies | `T3` ETC · `T4` segment set · `video_obs_2fps.npy` · `audio_rms_0p25.npy` |
| report residual risks | §6 |
| stop on governance violations | no violation encountered; the two blocked bindings were reported, not worked around |

---

## 6 · Residual risks

| # | risk |
|---|---|
| **R-1** | **The observation dataset for 08-24 does not exist and cannot be derived from committed code.** 39 visual events and the DIE-V thresholds require `video_obs_2fps.npy`; the offset model requires `audio_rms_0p25.npy`. Neither has a producer. **Parameterizing the generator does not create observations — it only stops the generator from pretending it has them.** |
| **R-2** | **The 08-22 offset model and anchors in the committed observation dataset are RECONSTRUCTED from `STEP0_TIMING_CLOSURE.md`, not re-measured.** Their provenance is recorded in the dataset. For those specific fields the regression is a round-trip, not an independent reproduction — stated so the proof is not read as stronger than it is. |
| **R-3** | **`gen_artifacts.py` v1 is retained** so the equivalence test stays runnable. It still contains the 08-22 constants. It is marked superseded; **whether to delete it is an Executive call**, because deleting it removes the ability to re-verify §3. |
| **R-4** | **A conformant 08-24 run would still emit 08-22 observations** if someone supplied `AR2-0822.observations.json` with `AR2-0824.context.json`. **The generator does not currently cross-check that context and observations describe the same production.** A `production_id` assertion is the obvious guard and is **not** implemented — it would be a behaviour change, and Phase A's proof rests on there being none. |
| **R-5** | `T11`'s stale `CONDUCTOR_SCORE.yaml` means the repository's most-cited musical artifact does not reflect two Executive dispositions. Every downstream reader of it today is reading pre-Option-C content. |

**`R-4` is the one to act on first.** It is cheap, and it is the exact failure mode this whole task
order exists to prevent — **wrong film, right format, no error.**

---

## 7 · What still stands between here and a conformant regeneration

Unchanged from `GER-001` §3 except where this task closed an item.

| # | prerequisite | status after ECR-GEN-001 |
|---|---|---|
| 1 | `SOP-06` Phase A re-export; `GATE-1` custody audit | **outstanding** |
| 2 | four input hashes pinned; **ETC produced** | fcpxml + srt hashes measured; **ETC still `NOT_PRODUCED`** |
| 3 | resolver re-validated against that ETC | **blocked by 2** |
| 4 | five intermediates regenerated | `timeline_resolved` ✅ · `camera_runs` ✅ · **3 still blocked** |
| 5 | generator parameterised | **DONE** |
| 6 | segment set re-derived and Executive-ratified | **outstanding** |
| 7 | conformant viewing master designated | **outstanding** |

**Item 5 was this task order. It is complete. Items 1–4, 6 and 7 are not engineering work I am
authorized to perform, and four of them are not engineering work at all.**

---

*Custody `IMPLEMENTATION / CODEBASE ONLY`. No governed artifact regenerated. No Executive content
altered, and none read except as input to a read-only test.*
