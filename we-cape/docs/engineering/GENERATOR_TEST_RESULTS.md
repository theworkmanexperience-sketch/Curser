# GENERATOR TEST RESULTS — ECR-GEN-001

**Task Order:** `ECR-GEN-001` Phase C · **Custody:** `IMPLEMENTATION / CODEBASE ONLY` · **Date:** 2026-08-29
**Suite:** `scripts/conformance_suite.py` — read-only; writes no governed artifact.

---

## 0 · Summary

```
PASS 8    BLOCKED 2    FAIL 2    total 12
```

**Neither FAIL is caused by this task order.** `T11` is a pre-existing repository drift and `T12` is a pre-existing gap in the pipeline. Both were found by this suite and are reported rather than repaired — repairing either requires authority this Order does not grant.

**Neither BLOCKED test can be unblocked by engineering.** `T3` needs an Editorial Timing Contract that does not exist; `T4` needs a segment set that must be re-derived and then ratified by the Executive.


## 1 · Results

| id | test | status | measurement |
|---|---|---|---|
| **T1** | FCPXML ingestion (08-24) | **PASS** | 1096 elements resolved; spine closes at 4689.5 s vs sequence 4689.5 s |
| **T2** | SRT ingestion (08-24) | **PASS** | 2036 cues parsed; sha 2a16dd700148488f...; last cue ends 4688.958 s vs runtime 4689.5 s |
| **T3** | Editorial Timing Contract binding | **BLOCKED** | CTX.sha.etc = NOT_PRODUCED; CTX.source_files.etc = NOT_PRODUCED |
| **T4** | Segment binding (08-24) | **BLOCKED** | no observation dataset exists for the 08-24 lineage |
| **T5** | Caption binding (08-24) | **PASS** | 65 title elements resolved from the 08-24 FCPXML; SRT carries 2036 cues |
| **T6** | EPR-001 integration | **PASS** | EPR-001 v1.13.0 loads; 7 entries; 19 distinct segment_refs S01..S19 |
| **T7** | EPR-07 retirement handled without exception | **PASS** | retirement.disposition=RETIRE; consumer skipped it and returned 6 active beats; exception=None |
| **T8** | Parameterized RUN_ID generation | **PASS** | --run-id auto -> WECAPE-AR2-0822-20260829-005139; --run-id pinned -> WECAPE-AR2-SPRINT3A-20260822-114028 |
| **T9** | No 08-22 constants remain in the generator | **PASS** | {"runtime": 0, "mp4_sha": 0, "fcpxml_sha": 0, "srt_sha": 0, "etc_sha": 0, "run_id": 0, "git": 0, "segment_table": 0, "cue_table": 0, "abs_path": 0} |
| **T10** | Refactor equivalence v1 == v2 on identical inputs | **PASS** | 7/7 artifacts byte-identical |
| **T11** | Committed artifacts match the committed generator | **FAIL** | 1 of 7 committed artifacts differ: ['CONDUCTOR_SCORE.yaml'] |
| **T12** | Every pipeline input has a producer | **FAIL** | 2 inputs unproduceable; camera_runs.json RESOLVED by derive_camera_runs.py this task |

## 2 · Notes carried by individual tests

**T1 · FCPXML ingestion (08-24)**

> resolver ran without an ETC; see T3

**T3 · Editorial Timing Contract binding**

> IP-1. No ETC exists for the 08-24 lineage. The resolver reports etc_validation NOT_VALIDATED rather than silently proceeding. DOC-001 instrument agreement CANNOT be demonstrated for this lineage until an ETC is produced.

**T4 · Segment binding (08-24)**

> IP-6. The segment set must be re-derived against the governed timeline and ratified by the Executive. The generator now ACCEPTS a segment table as data - it no longer contains one.

**T5 · Caption binding (08-24)**

> structural binding only; a collapse rule for doubled Parent-SRT cues is still undeclared (IP-4)

**T6 · EPR-001 integration**

> EPR is segment-keyed, so it binds by identifier and needs no timecode. Resolving those identifiers to spans still requires the re-derived segment set (T4).

**T7 · EPR-07 retirement handled without exception**

> EPR-07 remains present with beat, audience_state and segment_refs intact; only the consumer skips it.

**T11 · Committed artifacts match the committed generator**

> gen_artifacts.py was committed twice AFTER CONDUCTOR_SCORE.yaml was last regenerated (319f234 Option C, 0f3d12c MOTION sidechain). Under DOC-002 the artifact is stale.

**T12 · Every pipeline input has a producer**

> video_obs_2fps.npy (required by die_v_observables.py) - no producer in the repository; audio_rms_0p25.npy (required by step0_offset.py) - no producer in the repository


## 3 · How to re-run

```
# 1. resolve the timeline (ETC optional: pass NONE)
python3 fcpx_resolve.py <Info.fcpxml> <P2_LOCK_timing.json|NONE> derived/timeline_resolved.json

# 2. derive camera runs
python3 derive_camera_runs.py derived/timeline_resolved.json derived/camera_runs.json

# 3. generate (scratch output only)
python3 gen_artifacts_v2.py --context      context/AR2-0822.context.json \
                            --observations context/AR2-0822.observations.json \
                            --derived      derived/ \
                            --sources      <SPRINT3A_WORK root> \
                            --out          scratch/ \
                            --run-id       auto        # or 'pinned' to reproduce the archive

# 4. conformance suite
python3 conformance_suite.py
```

`--run-id pinned` is what makes the equivalence test in the Verification Diff repeatable: it reproduces the archived RUN_ID so the only variable under test is the refactor itself.


## 4 · What a PASS here does and does not mean

| a PASS means | a PASS does NOT mean |
|---|---|
| the implementation accepts the input and binds it structurally | the input is the right input |
| the generator no longer carries 08-22 assumptions | 08-24 artifacts can be produced |
| `T10`'s seven byte-identical artifacts prove the refactor is behaviour-neutral | the artifacts are correct for the governed production |
| `T7` proves a retired EPR entry raises no exception | the retirement's downstream consequences are all handled |

**`T1`, `T2` and `T5` pass against the governed 08-24 lineage and produce nothing usable**, because
`T3` and `T4` are blocked. That is the intended outcome: the generator now stops for a stated
reason instead of emitting confident output about the wrong film.


---

*Read-only suite. No governed artifact written, no Executive content read except as test input.*
