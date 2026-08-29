# ECR-GEN-002 — CONFORMANCE REPORT

**Instrument:** Engineering Conformance Report
**Task order:** ENGINEERING TASK ORDER — ECR-GEN-002, Generator Conformance & Validator Remediation
**Production fixture:** Alpha RoundUp 2026 Day 2, `AR2-0822` (08-22 editorial lock, `SUPERSEDED_ASSEMBLY`)
**Date:** 2026-08-29
**Custody:** `IMPLEMENTATION / CODEBASE ONLY`
**Repository state at start:** `1414c5f`

---

## 0 · Certification

```
Engineering Certification    ENGINEERING-CONFORMANT
Production Readiness         NOT YET AUTHORIZED
```

**Conformance suite: 16 PASS · 0 FAIL.**

Engineering certification confirms implementation correctness only. It does not
authorise production regeneration. Regeneration remains contingent on Executive
disposition of `B-5` and `B-6`, on authoritative 08-24 inputs, and on formal
regeneration authorisation — none of which this order grants or this report claims.

**Three new conditions were found during execution and are reported, not resolved:
`B-13`, `B-14`, `B-15` (§6).** `B-14` sits on a ratified `EPR-001` beat boundary and
needs an Executive answer.

---

## 1 · Scope executed

| # | Item | Status |
|---|---|---|
| 1 | `B-1` — ETC validator remediation | **COMPLETE** |
| 2 | `B-4` — generator parameterisation | **COMPLETE** for the order's enumerated classes |
| 3 | `B-9` — runtime identity guards | **COMPLETE**, twelve guards |
| 4 | `B-3` — observation producers | **COMPLETE for audio · SPECIFIED-NOT-EQUIVALENT for video** |
| 5 | Regression integrity | **COMPLETE**, gate is clean; a 280-literal residue is reported as `B-13` |

---

## 2 · `B-1` — ETC validator remediation

### 2.1 What was wrong

`fcpx_resolve.py` built its comparison set as `[x for x in rows if x['depth'] == 0]`,
which **includes transitions**; the Editorial Timing Contract's `spine` array
**excludes** them. The two lists were then paired positionally by `zip`, so the
comparison desynchronised at the first transition and never recovered. `zip` also
truncates silently, and `etc_spine_n` and `resolved_spine_n` were both recorded and
never compared.

Measured on the committed pre-change code and the committed 08-22 inputs:

```
etc_spine_n           : 191
resolved_spine_n      : 214       (191 story elements + 23 transitions)
spine_offset_matches  : 1
```

### 2.2 What was changed

```python
d0         = [x for x in rows if x['depth'] == 0]
mine_spine = [x for x in d0 if x['tag'] != 'transition']
```

and the single positional `zip` was replaced by four ordered gates, each of which is
a **STOP with a recorded `stop_reason` and exit 2**, never a downgraded warning:

| gate | condition | verdict on failure |
|---|---|---|
| 1 | ETC `source_sha256` equals the SHA-256 of the FCPXML this run parsed | `FAILED_SOURCE_IDENTITY` |
| 2 | ETC `sequence.duration_s` equals the resolved sequence duration | `FAILED_SEQUENCE_DURATION` |
| 3 | **strict cardinality** — `len(etc.spine) == len(non-transition depth-0)` | `FAILED_CARDINALITY` |
| 4 | element-wise offset and duration agreement across the whole census | `FAILED_COMPARISON` |
| — | resolved spine end equals sequence duration | `FAILED_TIMELINE_CLOSURE` |

Gate 3 runs **before** any pairing, which makes `zip`-style truncation structurally
impossible rather than merely unlikely.

### 2.3 Result

```
etc_validation        : VALIDATED
etc_spine_n           : 191
resolved_spine_n      : 191
depth0_incl_transitions: 214
source_sha256_match   : True
sequence_duration_match: True
spine_comparison      : 191 / 191
spine_end_equals_lock : True
tolerance_s           : 0.0005
exit                  : 0
```

**191 / 191 at 0.0005 s.** The figure the governed artifacts have asserted since
Sprint 3A is now, for the first time, produced by committed code.

### 2.4 A correction made during execution

The first pass folded `n_out_of_range > 0` into the binding verdict. The 08-22 fixture
disproved that immediately: the known-good lineage carries **18** anchored connected
elements whose resolved out-time exceeds the sequence duration, and it binds 191/191.
Out-of-range elements are an FCPXML nesting observable, not an ETC binding failure.

They are not absorbed either. The resolver reports
`out_of_range_status: PRESENT_REQUIRES_DECLARED_DISPOSITION`, and guard `G-07` asserts
the resolved count against a **declared expectation** in the context. The condition is
escalated to a declaration, not swallowed.

---

## 3 · `B-4` — generator parameterisation

### 3.1 Method

A new producer, `build_context.py`, turns a declared context stub into a **measured**
context. It computes every source hash and byte count, the SRT cue census, the ETC
spine/connected/tag censuses, the resolver census and verdict, and the derived lock
timecodes — and **refuses to emit a context whose declared values disagree with the
measured ones**. A disagreement is a STOP; the script never corrects a declaration.

`E6` demonstrates this: a context declaring `srt.cues: 9999` stops the build with
`declared srt.cues (9999) does not equal the measured cue count (2291)`.

**38 whole-line replacements** were then applied to `gen_artifacts_v2.py`, each
asserting its target matched exactly once so a silent no-op was impossible.

### 3.2 Coverage against the order's enumeration

| class the order names | disposition |
|---|---|
| cue totals | `SRTM['cues']`, measured from the SRT |
| resolved element counts | resolver census — `1025` total, `214` depth-0, `191` spine, `404` connected, `40` titles |
| runtime values | `CTX['runtime_s']`, asserted against the resolved spine end |
| lock timecodes | computed from runtime and frame rate |
| byte counts | `source_manifest[*].bytes`, measured by `os.path.getsize` |
| filenames | `display_names` declared per lineage; header alignment computed |
| static production metadata | proxy geometry and frame rate from context |

### 3.3 Regression — the strongest available evidence

The generator was run against the 08-22 fixture with `--run-id pinned` before and
after the change and the outputs compared byte for byte.

```
                                       changed lines    bytes
STEP0_TIMING_CLOSURE.md                     1           14163 -> 14163
CAPTION_REGISTRY.yaml                       1           29763 -> 29764
VISUAL_EVENT_REGISTRY.yaml                  1           33015 -> 33016
EDITORIAL_SYNCHRONIZATION.yaml              1           51773 -> 51774
CONDUCTOR_SCORE.yaml                        1           53890 -> 53891
ESS_VALIDATION_REPORT.md                    1           18608 -> 18608
PRODUCTION_INTELLIGENCE_SEED.yaml           1            4467 ->  4468
                                       ------------------------------
TOTAL                                       7          205679 -> 205684
```

**205 679 bytes of emitted content; seven changed lines; five changed bytes.** Every
one of the 38 substituted measurements reproduces the literal it replaced, exactly.

The seven changed lines are two conditions, both corrections:

**(a) `0.0006 s` → `0.0005 s`** — two artifacts. The published artifacts asserted a
comparison tolerance the code has never used. The value now reads
`validation.tolerance_s`.

**(b) one added space in the header proxy line** — five YAML artifacts. The
hand-aligned input header had one field at width 39 and three at 40. The computed
alignment normalises to 40.

### 3.4 What `B-4` did **not** cover

The order enumerates measurable metadata, and that is what was fixed. It does not
reach the **observational narrative body**, which is a much larger condition and is
raised as `B-13` in §6.1.

---

## 4 · `B-9` — runtime identity guards

Twelve guards in `runtime_guards.py`, called after every input is loaded and **before
the first byte of the first artifact is written**. A failure raises `GuardFailure`,
which the generator turns into exit 2 with nothing published.

| guard | asserts |
|---|---|
| `G-01` | context `production_id` == observations `production_id` |
| `G-02` | context `lineage` == observations `lineage` |
| `G-03` | every source hash agrees between context and observations |
| `G-04` | declared runtime equals the resolved spine end at 0.0005 s |
| `G-05` | ETC verdict is `VALIDATED`, or `NOT_VALIDATED` **and** the context declares the absence |
| `G-06` | ETC spine census equals the resolved non-transition census |
| `G-07` | resolved out-of-range count equals the declared expectation |
| `G-08` | segments in range, correctly ordered, well-formed |
| `G-08b` | every segment overlap is declared; an undeclared or stale declaration stops |
| `G-09` | cues in range, ordered, non-overlapping |
| `G-10` | derived camera-run count equals the resolved spine census |
| `G-11` | all twelve observation classes present |

`G-05` closes a gap the Readiness Review did not name: without it, a lineage resolved
with no ETC would generate silently. It now requires the context to declare the
absence explicitly. **An unvalidated lineage cannot be generated by default.**

Run on the 08-22 fixture: **12 guards PASS**, and the generated artifacts are
**byte-identical** to the run without guards — the guards add no output, only refusal.

### 4.1 Negative tests

| test | injected fault | result |
|---|---|---|
| `E9` | observations declare `production_id: AR2-0824` | `G-01` STOP · exit 2 · **0 files written** |
| `E10` | observations pin a different FCPXML hash | `G-03` STOP · exit 2 · **0 files** |
| `E11` | observation bundle missing a class | `G-11` STOP · exit 2 · **0 files** |
| `E12` | an undeclared segment overlap | `G-08b` STOP · exit 2 · **0 files** |

`R-4` — *wrong film, right format, no error* — is closed. The pairing that produced it
now stops before anything is written.

---

## 5 · `B-3` — observation producers

### 5.1 The inputs were never missing; their producers were

`video_obs_2fps.npy` and `audio_rms_0p25.npy` were found **present** on the work
volume. What has never existed is a script that makes them. The volume's own
`STATUS.txt` records the run —

```
11:48:01 START die_v
11:48:07 PASS A done: 19386 rms samples (4846.5s)
```

— and a search of the entire work volume returns **no `.py` file of any kind**.

### 5.2 `audio_rms_0p25.npy` — recovered exactly

`produce_audio_rms.py`. Recipe recovered by conformance testing across sample rates:

```
ffmpeg -i <media> -ac 1 -ar 16000 -f s16le -
int16 -> float32, non-overlapping 0.25 s (4000-sample) windows, trailing partial
window DISCARDED, rms = sqrt(mean((x/32768)^2)), float32
```

```
shape (19386,)  covered_s 4846.500
max_abs_err vs the 08-22 fixture : 0.00000000
bitwise identical                : True
run1 == run2                     : True
```

### 5.3 `video_obs_2fps.npy` — specified, NOT fixture-equivalent

`produce_video_obs.py` produces a **new, fully specified** array and writes its column
schema beside it. It is deterministic (`run1 == run2` bitwise). It does **not**
reproduce the legacy array and does not claim to.

Column semantics recovered by conformance against all 9 693 legacy samples:

| col | name | mean abs difference | status |
|---|---|---|---|
| 0 | mean R | 0.027 | RECOVERED |
| 1 | mean G | 0.026 | RECOVERED |
| 2 | mean B | 0.054 | RECOVERED |
| 3 | mean luma, Rec.601 | 0.024 | RECOVERED |
| 4 | *(declared: std luma)* | 5.122 | **NOT RECOVERED** |
| 5 | *(temporal difference)* | 5.104 | **PARTIAL** — zero on the first sample, formulation unrecovered |
| 6 | *(declared: middle band)* | 82.680 | **NOT RECOVERED** |
| 7 | mean luma, top band | 0.087 | RECOVERED |
| 8 | mean luma, bottom band | 0.032 | RECOVERED |

Even the recovered columns do not match bitwise, and **no native frame in the proxy
carries the legacy array's first-sample mean** — so the residual is a decode path this
work could not reconstruct.

Recovering columns 4, 5 and 6 would mean inferring an unrecorded specification from
its own output. That is prohibited, so the condition is reported.

**Consequence, stated so it is not discovered later.** The DIE-V cut threshold
(`48.27`), the night-luma in/out thresholds (`70.0` / `85.0`), the motion terciles
(`13.04`, `23.55`) and the 39 visual events built on them all rest on an observable
this producer does not reproduce. Adopting it obliges those values to be re-derived.
**Re-derivation is a regeneration and is not authorised by this order.**

---

## 6 · Conditions found during execution

### 6.1 `B-13` — the generator is a report with variable substitution

The Readiness Review measured 47 lines carrying 08-22 literals. Measuring the emitted
**text** rather than the lines gives the real figure:

| artifact | literal chars | interpolated chars | literal share |
|---|---:|---:|---:|
| STEP0_TIMING_CLOSURE.md | 5 475 | 1 758 | 75.7 % |
| CAPTION_REGISTRY.yaml | 2 409 | 1 252 | 65.8 % |
| VISUAL_EVENT_REGISTRY.yaml | 5 195 | 1 420 | 78.5 % |
| EDITORIAL_SYNCHRONIZATION.yaml | 2 205 | 2 101 | 51.2 % |
| CONDUCTOR_SCORE.yaml | 11 018 | 3 496 | 75.9 % |
| ESS_VALIDATION_REPORT.md | 9 595 | 1 926 | 83.3 % |
| PRODUCTION_INTELLIGENCE_SEED.yaml | 2 159 | 1 228 | 63.7 % |
| **TOTAL** | **38 056** | **13 181** | **74.3 %** |

**Three quarters of what the generator emits is literal prose written into it.**
`TR-2` enumerates **280 untraceable numerals and timecodes across 166 lines** inside
that prose — probe windows and findings, caption-class breakdowns, uncovered-span
descriptions, correlation-method figures, dB targets, contact-sheet counts.

These are 08-22 **observations** written as text. They belong in the observation
bundle. Relocating them is a change of a different kind and magnitude from the one
this order scoped, and it has a consequence that must be decided before it is
attempted: a generator whose narrative comes from observations will emit an artifact
set with **empty narrative** for any lineage whose observations do not supply
equivalent prose — and no such 08-24 observations exist.

**`B-13` is raised, not fixed.**

### 6.2 `B-14` — two segments claim the same six seconds, on an EPR beat boundary

Guard `G-08b` fired on the governed 08-22 registry:

```
S12  organizer_honors_and_silence   3124.0 - 3236.0
S13  group_photo                    3230.0 - 3275.0
                                    ^^^^^^^^^^^^^^^  6.0 s claimed twice
```

Every other segment pair in the registry is disjoint, so the registry's intent is
plainly non-overlapping.

**Why it has never been reported:** the only code that touches segment coverage takes
a **union**. Declared segment duration totals 4 418.0 s; covered runtime is 4 412.0 s;
only the union figure is ever published. The 6.0 s discrepancy has been arithmetically
absorbed for the life of the artifact set.

**Why it matters now.** `EPR-001` v1.13.0 binds `S12` to **EPR-05 · Deepening ·
CLIMACTIC** and `S13` to **EPR-06 · Celebration · ELEVATED**. The contested span sits
exactly on the CLIMACTIC → ELEVATED transition. Six seconds of runtime belong to two
declared dramatic beats at once.

The platform will not assign it. Under Invariant B the platform may not infer an
intermediate or blended state between declared levels, and under `EPR-001` §2.3 it may
not author, extend or default any EPR value. **The overlap has been declared in the
context as a known condition so the fixture runs; the assignment is an Executive
question and is open.**

### 6.3 `B-15` — a second file named `Filmage_Editor.mp4`

Locating the designated proxy found two files with that exact name:

```
.../Thursday Aug 20th/Final Data Source Files/Filmage_Editor.mp4
    a53655fc673945a0d99dde3d5b60c9a126d8b41e4e44a7c7eedeb058ba0f47e8   <- designated
.../Thursday Aug 20th/Reduced Files/Filmage_Editor.mp4
    acbfd729d7867ba94ce4704479982d648b50f6c69a2f85f593b7a2bea5ed3959   <- NOT the proxy
```

Same filename, different content, sibling directories. This is the `CUSTODY_ALERT_001`
hazard class, in the proxy layer rather than the master layer. The designated path is
now declared in `AR2-0822.context.json` and its hash is asserted by `build_context.py`,
so this specific confusion can no longer occur silently in a generator run.

**No registry was written.** Registering the look-alike requires a registry exception,
which this order does not grant.

---

## 7 · Conformance suite

`ecr_gen_002_suite.py` — **16 PASS · 0 FAIL**.

| id | test | result | evidence |
|---|---|---|---|
| `E1` | ETC binding validates on the 08-22 fixture | **PASS** | `VALIDATED` 191 / 191, tol 0.0005, exit 0 |
| `E2` | short ETC stops on cardinality, no comparison | **PASS** | `FAILED_CARDINALITY`, exit 2, no partial comparison recorded |
| `E3` | ETC naming another export stops on identity | **PASS** | `FAILED_SOURCE_IDENTITY`, exit 2 |
| `E4` | 2 ms drift at one element stops the binding | **PASS** | `FAILED_COMPARISON` 190 / 191, exit 2 |
| `E5` | context values measured from the named sources | **PASS** | spine 191, connected 404, titles 40, resolver total 1025 |
| `E6` | a declared value that disagrees stops the build | **PASS** | exit 2 on `srt.cues 9999` vs measured 2291 |
| `E7` | derived camera runs match the resolved spine census | **PASS** | 191 runs |
| `E8` | all runtime identity guards pass, generation completes | **PASS** | 12 guards, exit 0 |
| `E9` | wrong `production_id` stops at `G-01` | **PASS** | exit 2, 0 files written |
| `E10` | observations pin another source, stops at `G-03` | **PASS** | exit 2, 0 files |
| `E11` | observation bundle incomplete, stops at `G-11` | **PASS** | exit 2, 0 files |
| `E12` | undeclared segment overlap stops at `G-08b` | **PASS** | exit 2, 0 files |
| `E13` | no production-identifying literal remains (`TR-1`) | **PASS** | 0 hits; 280 `TR-2` literals reported as `B-13` |
| `E14` | regression vs the pre-change artifact set | **PASS** | 7 changed lines, 205 679 → 205 684 bytes |
| `E15` | audio RMS producer reproduces the fixture | **PASS** | bitwise identical, 19 386 samples |
| `E16` | visual observation producer exists and is specified | **PASS** | schema written; fixture equivalence **not claimed** |

`E16` passes on the criterion "a specified, deterministic producer exists". It does
**not** assert fixture equivalence — see §5.3.

---

## 8 · Artifact hashes produced under ECR-GEN-002

Scratch output only. **No governed artifact path was written.**

```
STEP0_TIMING_CLOSURE.md            8c1ccbc7a8d9899e
CAPTION_REGISTRY.yaml              0ea923403cdae86d
VISUAL_EVENT_REGISTRY.yaml         5f050392b7130cf5
EDITORIAL_SYNCHRONIZATION.yaml     8813ed2a47e9f4bd
CONDUCTOR_SCORE.yaml               952948cb26f0fc05
ESS_VALIDATION_REPORT.md           a636da05fb2228da
PRODUCTION_INTELLIGENCE_SEED.yaml  f102840413b004b2
```

**`T11` is unchanged and is now wider.** The committed `CONDUCTOR_SCORE.yaml` is
`1464e33595add5b6`; the pre-change generator produced `fc481954623c63e3`; this
generator produces `952948cb26f0fc05`. Three generator dispositions are now
un-materialised in the repository rather than two. Closing the gap requires
regeneration authority, which this order withholds.

---

## 9 · Files changed

| path | change |
|---|---|
| `ess/scripts/fcpx_resolve.py` | `B-1`: comparison set corrected, five ordered STOP gates, census block · 135 → 246 lines |
| `ess/scripts/gen_artifacts_v2.py` | `B-4`: 39 line replacements + measured-input bindings; `B-9`: guard call · 1232 → 1272 lines |
| `ess/scripts/runtime_guards.py` | **NEW** — twelve fail-fast guards · 228 lines |
| `ess/scripts/build_context.py` | **NEW** — measured context producer |
| `ess/scripts/produce_audio_rms.py` | **NEW** — `B-3`, reproduces the fixture bitwise |
| `ess/scripts/produce_video_obs.py` | **NEW** — `B-3`, specified producer, equivalence not claimed |
| `ess/scripts/traceability_scan.py` | **NEW** — `TR-1` gate and `TR-2` census |
| `ess/scripts/ecr_gen_002_suite.py` | **NEW** — 16-test conformance suite |
| `ess/context/AR2-0822.context.json` | `display_names`, `source_files.mp4`, `declared_segment_overlaps` |
| `ess/context/AR2-0822.observations.json` | `production_id`, `lineage`, `source_sha` — required by `G-01`…`G-03` |

---

## 10 · Executive exclusions — compliance

Enumerated against the order's own §"Explicit Executive Exclusions".

| the ECR shall not | what was done |
|---|---|
| determine `B-5` (segment re-binding) | not touched. `B-14` raises a new, adjacent Executive question and answers none of it |
| determine `B-6` (regeneration target scope) | not touched |
| modify any Executive declaration within `EPR-001` | `EMOTIONAL_PROGRESSION_REGISTRY.yaml` was **read only**, never written |
| regenerate governed production artifacts | all generation went to scratch; no governed path written |
| overwrite `CONDUCTOR_SCORE.yaml` | not written. Its drift is reported in §8 |
| alter governance registries | no registry written, including the `B-15` look-alike |

Additionally, and beyond the enumerated exclusions: **no missing value was populated or
defaulted**, **no defect was silently repaired** — every one is either fixed with its
evidence stated or reported uncorrected — and **no compliance score, ranking, or
readiness percentage is stated anywhere in this report**.

---

## 11 · Standing state

```
ETC validator                     REMEDIATED - 191/191 at 0.0005 s, five STOP gates
runtime identity guards           IMPLEMENTED - 12 guards, fail-fast, 4 negatives proven
production-identifying literals   NONE (TR-1 clean)
narrative literals                280 across 166 lines - B-13, reported
audio observation producer        EXACT - bitwise identical to the 08-22 fixture
visual observation producer       SPECIFIED - fixture equivalence NOT established
segment overlap S12/S13           DECLARED as present - B-14, assignment OPEN (EXECUTIVE)
look-alike proxy                  B-15, reported, not registered
CONDUCTOR_SCORE.yaml              STALE - three dispositions un-materialised
08-24 observations                ABSENT
08-24 proxy                       NOT_DESIGNATED
08-24 ETC                         NOT_PRODUCED
Path B regeneration target        UNDECLARED
Engineering Certification         ENGINEERING-CONFORMANT
Production Readiness              NOT YET AUTHORIZED
```

**Prepared for Executive review. No execution is directed by this document.**
