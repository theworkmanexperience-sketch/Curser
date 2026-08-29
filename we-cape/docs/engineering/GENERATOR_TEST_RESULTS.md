# GENERATOR TEST RESULTS

**Scope:** the WE CAPE ESS artifact generator and its input pipeline
**Fixture:** `AR2-0822` — 08-22 editorial lock, the only lineage with four hashed sources, a published artifact set and a known-good ETC
**Last updated:** 2026-08-29, under **ECR-GEN-002**
**Custody:** `IMPLEMENTATION / CODEBASE ONLY`

Supersedes the ECR-GEN-001 edition of this document. ECR-GEN-001 results are retained
in §4 with their current disposition, so nothing is lost by the update.

---

## 1 · Headline

```
ECR-GEN-002 conformance suite      16 PASS  ·  0 FAIL
Engineering Certification          ENGINEERING-CONFORMANT
Production Readiness               NOT YET AUTHORIZED
```

A PASS here means the implementation is correct on the fixture. It does not mean the
08-24 lineage can be generated, and it does not authorise regeneration of anything.

---

## 2 · ECR-GEN-002 suite

`intelligence/p2/ess/scripts/ecr_gen_002_suite.py`

| id | test | result | evidence |
|---|---|---|---|
| `E1` | ETC binding validates on the 08-22 fixture | **PASS** | `VALIDATED`, 191 / 191, tolerance 0.0005 s, exit 0 |
| `E2` | short ETC stops on cardinality, no comparison attempted | **PASS** | `FAILED_CARDINALITY`, exit 2 |
| `E3` | ETC naming another export stops on source identity | **PASS** | `FAILED_SOURCE_IDENTITY`, exit 2 |
| `E4` | 2 ms drift at one spine element stops the binding | **PASS** | `FAILED_COMPARISON`, 190 / 191, exit 2 |
| `E5` | context values measured from the named sources | **PASS** | spine 191 · connected 404 · titles 40 · resolver total 1025 |
| `E6` | a declared value disagreeing with measurement stops the build | **PASS** | exit 2 on `srt.cues 9999` vs measured 2291 |
| `E7` | derived camera runs match the resolved spine census | **PASS** | 191 runs |
| `E8` | all runtime identity guards pass and generation completes | **PASS** | 12 guards, exit 0 |
| `E9` | wrong `production_id` stops at `G-01` | **PASS** | exit 2, **0 files written** |
| `E10` | observations pinning another source stop at `G-03` | **PASS** | exit 2, 0 files |
| `E11` | incomplete observation bundle stops at `G-11` | **PASS** | exit 2, 0 files |
| `E12` | undeclared segment overlap stops at `G-08b` | **PASS** | exit 2, 0 files |
| `E13` | no production-identifying literal remains (`TR-1`) | **PASS** | 0 hits; 280 `TR-2` literals reported as `B-13` |
| `E14` | regression against the pre-change artifact set | **PASS** | 7 changed lines; 205 679 → 205 684 bytes |
| `E15` | audio RMS producer reproduces the fixture | **PASS** | bitwise identical, 19 386 samples |
| `E16` | visual observation producer exists and is specified | **PASS** | schema written; **fixture equivalence not claimed** |

---

## 3 · Runtime identity guards

Twelve guards, all executed **before the first byte of the first artifact is written**.

| guard | asserts | proven by |
|---|---|---|
| `G-01` | production_id agreement | `E8` positive, `E9` negative |
| `G-02` | lineage agreement | `E8` |
| `G-03` | source hash agreement | `E8`, `E10` negative |
| `G-04` | declared runtime == resolved spine end | `E8` |
| `G-05` | ETC verdict `VALIDATED`, or a declared absence | `E8` |
| `G-06` | ETC spine census == resolved census | `E8` |
| `G-07` | out-of-range count == declared expectation | `E8` (18 declared, 18 resolved) |
| `G-08` | segments in range and in order | `E8` |
| `G-08b` | every segment overlap declared | `E8` positive, `E12` negative |
| `G-09` | cues in range, ordered, non-overlapping | `E8` |
| `G-10` | camera-run count == resolved spine census | `E8` |
| `G-11` | all twelve observation classes present | `E8`, `E11` negative |

The guards are **output-neutral**: the artifact set generated with guards active is
byte-identical to the set generated without them.

---

## 4 · ECR-GEN-001 tests — current disposition

| id | test | ECR-GEN-001 | now | note |
|---|---|---|---|---|
| `T1` | FCPXML ingestion | PASS | **PASS** | 08-24: 1096 elements, spine closes 4689.5 |
| `T2` | SRT ingestion | PASS | **PASS** | 2036 cues, `2a16dd70…` |
| `T3` | ETC binding | BLOCKED | **PASS on 08-22** | the 08-22 ETC was never tested; it now validates 191/191. **Still BLOCKED for 08-24** — no ETC exists |
| `T4` | segment binding | BLOCKED | **BLOCKED** | depends on `T3` for 08-24 |
| `T5` | caption binding | PASS | **PASS** | 65 titles |
| `T6` | EPR integration | PASS | **PASS** | v1.13.0, 7 entries, 19 refs, read-only |
| `T7` | EPR-07 retirement handling | PASS | **PASS** | 6 active beats, no exception |
| `T8` | RUN_ID generation | PASS | **PASS** | `auto` and `pinned` both verified |
| `T9` | no embedded constants | PASS | **SUPERSEDED by `E13`** | `T9`'s ten classes covered computation inputs only; `E13` covers emitted text |
| `T10` | v1/v2 equivalence | PASS | **SUPERSEDED by `E14`** | equivalence is now measured against the pre-ECR-GEN-002 set |
| `T11` | committed artifacts match the committed generator | FAIL | **FAIL, wider** | see §5 |
| `T12` | every input has a producer | FAIL | **PARTIAL** | audio producer exact; visual producer specified but not fixture-equivalent |

### 4.1 `T9` was passing on an insufficient scope

`T9` tested the ten classes feeding **computation** — hashes, runtime lock, git commit,
`RUN_ID`, segments, cues, visual events, delta ledger, not-observed set, source roots —
and reported `0 across 10 classes`. It did not test literals written directly into
**output text**, because output text was assumed to derive from those classes. It does
not, everywhere. `E13` replaces `T9` and scans the emitted text itself.

---

## 5 · `T11` — repository drift, now three dispositions deep

```
committed   CONDUCTOR_SCORE.yaml            1464e33595add5b6
pre-ECR-GEN-002 generator produces          fc481954623c63e3
ECR-GEN-002 generator produces              952948cb26f0fc05
```

The repository's copy matches neither. Three Executive-dispositioned generator changes
are now un-materialised rather than two. Every downstream consumer reading that file
is reading a pre-disposition state.

**Not corrected here.** Correcting it means regenerating a governed artifact, which
requires regeneration authority that ECR-GEN-002 explicitly withholds.

---

## 6 · `T12` — producers, and what the fixture can still prove

| input | ECR-GEN-001 | now |
|---|---|---|
| `audio_rms_0p25.npy` | no producer | **`produce_audio_rms.py` — bitwise identical to the fixture** |
| `video_obs_2fps.npy` | no producer | **`produce_video_obs.py` — specified and deterministic; does not reproduce the fixture** |

Six of nine legacy columns were recovered to a mean absolute difference of 0.02–0.09;
three were not (means 5.12, 5.10, 82.68). No native frame in the proxy carries the
legacy array's first-sample mean, so the residual is an unreconstructable decode path.
Recovering the remainder would require inferring an unrecorded specification from its
own output.

**Downstream consequence:** the DIE-V cut threshold, night-luma thresholds, motion
terciles and the 39 visual events rest on the legacy array. Adopting the new producer
obliges their re-derivation, which is a regeneration.

---

## 7 · How to re-run

```
# 1. resolve the timeline (ETC optional: pass NONE, and declare the absence in context)
python3 fcpx_resolve.py <Info.fcpxml> <P2_LOCK_timing.json|NONE> derived/timeline_resolved.json

# 2. derive camera runs
python3 derive_camera_runs.py derived/timeline_resolved.json derived/camera_runs.json

# 3. measure the context  (STOPS if any declared value disagrees with measurement)
python3 build_context.py --in context/AR2-0822.context.json --out work/ctx.json \
                         --sources <SPRINT3A_WORK root> \
                         --timeline derived/timeline_resolved.json \
                         --mp4 <designated proxy>

# 4. observation producers
python3 produce_audio_rms.py <proxy> work/audio_rms_0p25.npy --verify <fixture.npy>
python3 produce_video_obs.py <proxy> work/video_obs_2fps.npy --compare <legacy.npy>

# 5. generate (scratch output only; 12 guards run before the first write)
python3 gen_artifacts_v2.py --context      work/ctx.json \
                            --observations context/AR2-0822.observations.json \
                            --derived      derived/ \
                            --sources      <SPRINT3A_WORK root> \
                            --out          scratch/ \
                            --run-id       pinned

# 6. traceability gate
python3 traceability_scan.py gen_artifacts_v2.py --context work/ctx.json

# 7. full suite
python3 ecr_gen_002_suite.py --scripts . --context-dir context --sources <root> \
                             --mp4 <proxy> --work work --baseline <prior artifact set>
```

`--run-id pinned` reproduces the archived id, so the only variable under test is the
change itself.

---

## 8 · What a PASS here does and does not mean

| a PASS means | a PASS does NOT mean |
|---|---|
| the implementation accepts the input and binds it structurally | the input is the right input |
| the generator carries no value that names or measures one production | the generator's narrative is lineage-neutral — 74.3 % of its emitted text is still literal prose (`B-13`) |
| a mismatched input pairing stops before anything is written | the 08-24 pairing exists to be tested |
| the ETC binding is measured, not asserted | an 08-24 ETC exists |
| the audio observable is reproducible from its source | the visual observable is |
| the fixture regenerates to within seven lines of its archive | any governed artifact may be regenerated |

**Engineering may certify that the platform can execute correctly. Only Executive
authority can authorise that it may execute.**
