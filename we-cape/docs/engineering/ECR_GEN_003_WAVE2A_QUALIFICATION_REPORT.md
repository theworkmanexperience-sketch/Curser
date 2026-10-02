# ECR-GEN-003 — B-3 Qualification, Wave 2A: `step0_anchors.py` (Candidate A)

**Status:** TECHNICALLY QUALIFIED under Candidate A on the authorized historical (08-22) fixture.
**This is not a B-3 activation.** `step0_anchors.py` is NOT EFFECTIVE until a separate activation
ruling reaches custody. Decision B remains incomplete; both regeneration holds remain HELD. This
qualification does not establish Candidate A fidelity for `step0_offset.py`.
**Authority:** CHAIRMAN AUTHORIZATION — D2 QUALIFICATION WAVE 2A / step0_anchors.py ONLY; CHAIRMAN
HOLD — 0.784 PROVENANCE AUDIT; CHAIRMAN ACCEPTANCE — step0_anchors.py WAVE-2A TECHNICAL
QUALIFICATION (2026-10-02).
**Code under test:** ECR-GEN-003 engineering custody commit `e0a346a16abf77db4a6abe5d59a2b31dadcf4464`. Machine-readable results:
`docs/engineering/ECR_GEN_003_wave2a_test_results.json` (10 passed, 0 failed).

## 1 · Identities

| item | identity |
|---|---|
| `step0_anchors.py` (qualified, current) | `66079f2ada0f60c186edc43cf82fe3f02e9e22568b986695445c5e89535d474e` |
| behavioural oracle (pre-ECR, `795a847` = `8f70dee`) | `f3825ca3d878fe1f96320aa45157c9bcd198047877993eecd8c7c543d5cf66d0` (not run — see §3) |
| harness `b3_qualify.py` | `8019565de14775c215efddccbfeda7381003f453c0523eb55db99875f48e0ded` |

**Candidate A toolchain** (`/Volumes/WE_CAPE_OUTPUT/_b3_toolchains/d2_cp31012_np226/`, outside Git):

| component | identity |
|---|---|
| CPython | 3.10.12, `/Volumes/WE_CAPE_OUTPUT/_b3_toolchains/d2_cp31012_np226/python/bin/python3.10`, SHA-256 `3a855bd1956b302372f02be42ea2ada298306fd57717f8eee1d0c86c9db003a3` |
| CPython archive | `cpython-3.10.12+20230726-aarch64-apple-darwin-install_only.tar.gz`, SHA-256 `bc66c706ea8c5fc891635fda8f9da971a1a901d41342f6798c20ad0b2a25d1d6` |
| NumPy | 2.2.6, wheel `numpy-2.2.6-cp310-cp310-macosx_11_0_arm64.whl`, SHA-256 `8e41fd67c52b86603a91c1a505ebaef50b3314de0213461c7a6e99c9a3beff90` |
| NumPy installed-file manifest | `36fa915dcd44185fd9361d187e20994281713df429c9c6f77bc7d26578f61f4a` (1008 files, RECORD verified) |
| BLAS / LAPACK | scipy-openblas 0.3.29 (`OpenBLAS 0.3.29  USE64BITINT DYNAMIC_ARCH NO_AFFINITY neoversen1 MAX_THREADS=64`) |
| deterministic prefix manifest | `07f2ce264213cd8c0a4d48c0f5787aa7ec5b76327db1a8eb62d9559f4b537702` (3139 files: archive 2129, wheel 1005, pip-install 5) |
| identity record `candidate_a_toolchain.json` | `e9d9ae7d02479d062d7b230092bdb940b9a4635acbb15f1c3bd5753feab7f9f3` |
| record `prefix_manifest.json` | `2b7e13751e8c0b3e6c5d800b9721fe3862c5dbdc626c3220b1f92ceff9af04fb` |
| record `numpy_installed_manifest.json` | `167fbdc43756aa4f1864d60848d00a09102c6fda9a404b102d85e6f944267a11` |

Environment fixed by the harness: `PATH=/usr/bin:/bin`, `LANG=C`, `TZ=UTC`, `PYTHONHASHSEED=0`,
`PYTHONDONTWRITEBYTECODE=1`. No ffmpeg (tools: none); no ffmpeg candidate selected.

## 2 · Fixture manifest

| fixture | origin | SHA-256 |
|---|---|---|
| 08-22 lock SRT | `/Volumes/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/inputs/lock_srt2.srt` (existing, read-only); committed record: `EXECUTION_LOG.md` input 3 | `89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b` |
| 08-22 resolved timeline | `/Volumes/WE_CAPE_OUTPUT/_b3_qualification/wave1_20261002/fixtures_derived/timeline_resolved_0822.json`; the Wave 1 E1 primary output (committed Wave 1 report §2) | `ebf99f84ceb9dcf487b4703f1e377dd55296ff90d10aaac6a1c6bd3eacc791f8` |

No 08-24 material was used. No fixture was created for this wave.

## 3 · Pre-ECR oracle and static equivalence

The pre-ECR producer hard-codes `/mnt/user-data/…` and `/home/claude/work/out/…`; running it
would require creating system paths or editing it, so it was not run. Equivalence is established
statically instead:

- `ecr_gen_003_static_check.py --base 795a847`, `step0_anchors.py` checks: PASS S1, PASS S2, PASS S3, PASS S4, PASS S5
  (only the machine-path statements changed).
- `fcpx_resolve.py` `Resolver`, `rt` and `f2` are AST-identical between `8f70dee` and HEAD, so the
  fixture timeline carries the same title times and text the historical anchors came from.

## 4 · Results

Three Candidate A runs through `b3_qualify.py` (harness verdict PASS, every check true):

| run | exit | primary output `step0_anchors.json` | sidecar `.provenance.json` | undeclared writes |
|---|---|---|---|---|
| 1 | 0 | `b3e6a204a0d39f922648891782f813b04714abae14a78836e41a0a75bd481a27` | `fe3f0480c9b8fbfe5cbee4df23a01b4f40f322af2abd59bc9d4a0f7a52bec31d` | 0 |
| 2 | 0 | `b3e6a204a0d39f922648891782f813b04714abae14a78836e41a0a75bd481a27` | `fe3f0480c9b8fbfe5cbee4df23a01b4f40f322af2abd59bc9d4a0f7a52bec31d` | 0 |
| 3 | 0 | `b3e6a204a0d39f922648891782f813b04714abae14a78836e41a0a75bd481a27` | `fe3f0480c9b8fbfe5cbee4df23a01b4f40f322af2abd59bc9d4a0f7a52bec31d` | 0 |

Stdout identical in every run (`574f4f7adb9f13448b7defcdb149517be0fe0957ad02bbfbc4544775dd04fbb9`); stderr empty. Each sidecar records producer
`66079f2a…`, both inputs by SHA-256, CPython 3.10.12 and NumPy
2.2.6, with no wall-clock value.

**Filesystem-write audit:** zero undeclared writes; exactly the declared outputs in each run. Watch
roots: the run directory, the repository scripts directory, both fixture directories, the Candidate
A `python/` prefix and the user temp directory.

**Candidate A drift:** the prefix manifest recomputed before the runs, after the runs and at
packaging equals the provisioned `07f2ce264213cd8c0a4d48c0f5787aa7ec5b76327db1a8eb62d9559f4b537702`; the interpreter binary is unchanged.

## 5 · Historical-oracle comparison

The producer's output contract is a JSON list of rows with keys `cue`, `cue_s`, `cue_text`, `delta_title_minus_cue`, `match`, `title`, `title_in`.
It emits **19** rows. The committed historical set of **11** anchors is a consumer
selection: `gen_artifacts.py` (and `gen_artifacts_v2.py`) keep rows with
`abs(delta_title_minus_cue) <= 2.5`. Applying that committed filter to the producer rows reproduces
the committed anchors in `AR2-0822.observations.json` and the `STEP0_TIMING_CLOSURE.md` table
exactly (title_in, delta, title, order):

| title in (s) | delta (s) | title text |
|---|---|---|
| 119.292 | +0.084 | Initiated ? |
| 229.304 | +0.846 | Why Do You Ride ? |
| 244.963 | -0.162 | What's Your Nam e |
| 261.772 | +0.897 | Why Do You Ride ? |
| 291.792 | +0.209 | Why Do You Ride ? |
| 2116.333 | +0.708 | Mayor, Mary Esther Reed |
| 2378.042 | +0.792 | Why Do You Ride ? |
| 3116.042 | -1.124 | The Journey Reveals The Why |
| 4827.750 | +0.584 | Why Do You Ride ? |
| 4835.500 | +0.917 | How Long You Been Rid' n |
| 4840.708 | +2.250 | ..and that's what's good! |

Excluded rows (|delta| > 2.5): -22.916, -17.333, -5.750, -4.291, +4.167, +9.029, +23.167, +24.750.

| statistic (committed `STEP0_TIMING_CLOSURE.md`) | documented | reproduced |
|---|---|---|
| median delta | +0.708 s | +0.708 s (11 rows); +0.708 s (all 19) |
| anchor span | 119.3–4840.7 s | 119.3–4840.7 s |
| runtime coverage | 97.4% | 97.4% |
| drift over 4846.625 s | +0.684 s | +0.684 s |
| 95% CI of drift | [-0.541, +1.909] s | [-0.541, +1.909] s (OLS slope ± 1.96·SE) |

**Disposition:** every producer-contract value with a committed historical record reproduces.
`step0_anchors.py` `66079f2a…` — **PASS** under Candidate A.

## 6 · The "sd 0.784 s" value — provenance clarification

A calculation capable of reproducing 0.784 was identified in scratch, but no committed evidence establishes that calculation as the historical source of the literal. The value is not part of step0_anchors.py's output contract and is outside this producer qualification.

- **Producer:** `step0_anchors.py` emits no SD field and no producer-output schema requires one.
  Its stdout prints a diagnostic population SD over all 19 rows (10.564), which is not 0.784.
- **Where the value lives:** it first appears as committed narrative text in
  `STEP0_TIMING_CLOSURE.md` (`3fe7365`), then as a hard-coded literal in `gen_artifacts.py`
  (`8f70dee`, unchanged in every later version) and `gen_artifacts_v2.py`, and as copied text in the
  D-12 delta-ledger entry and the validation report. Occurrences at HEAD:
  - `intelligence/p2/ess/ESS_VALIDATION_REPORT.md:139`
  - `intelligence/p2/ess/STEP0_TIMING_CLOSURE.md:45`
  - `intelligence/p2/ess/context/AR2-0822.observations.json:1257`
  - `intelligence/p2/ess/scripts/gen_artifacts.py:343`
  - `intelligence/p2/ess/scripts/gen_artifacts.py:473`
  - `intelligence/p2/ess/scripts/gen_artifacts_v2.py:237`
  - `intelligence/p2/ess/scripts/verification.diff:374`
- **Origin:** no committed code calculates it and no commit message, ECR, ruling or evidence file
  establishes its computational origin. No decision rests on it: D-12's magnitude is the median and
  the ±6 s closure rests on the drift CI.

**Diagnostic analysis (scratch, not adopted as provenance).** Values computed from the producer rows:

| interpretation | value | 3 dp |
|---|---|---|
| 19 rows population sd (producer stdout diagnostic) | 10.564456 | 10.564 |
| 19 rows sample sd | 10.853946 | 10.854 |
| 11 rows population sd | 0.795432 | 0.795 |
| 11 rows sample sd | 0.834256 | 0.834 |
| 11-row regression residual sd, ddof 0 | 0.747239 | 0.747 |
| 11-row regression residual sd, ddof 1 | 0.783711 | 0.784 |
| 11-row regression residual sd, ddof 2 | 0.826104 | 0.826 |

The ddof-1 residual SD of the documented delta-on-time regression reproduces 0.784. It is recorded
as a candidate origin only: it is not in committed code, it uses a different degrees-of-freedom
convention than the CI computed alongside it, and with several candidates tested a coincidental
3-dp match cannot be excluded. No subset of nine or more rows gives 0.784 under either SD convention.

The historical generator and document text is unchanged by this qualification; any correction is a
separate matter.

## 7 · Scope and state

- `step0_anchors.py` `66079f2ada0f60c186edc43cf82fe3f02e9e22568b986695445c5e89535d474e`: TECHNICALLY QUALIFIED under Candidate A; eligible for a later
  B-3 activation ruling; NOT EFFECTIVE.
- `fcpx_resolve.py` EFFECTIVE under Addendum E; `derive_camera_runs_v2.py` EFFECTIVE under Addendum F.
- `produce_audio_rms.py`, `step0_offset.py`, `produce_video_obs.py`: inactive, not run. This wave
  exercised no BLAS or RNG path and gives no evidence on Candidate A fidelity for `step0_offset.py`.
- No producer was run against the governed 08-24 package; no observation was created.

## 8 · External evidence (not committed)

The raw workspace `/Volumes/WE_CAPE_OUTPUT/_b3_qualification/wave2a_20261002/` (oracle copy, spec, run outputs, harness report) remains outside Git, as
does the Candidate A toolchain. Harness report `anchors_candidateA.json` `7d808952341f8fea36efd8f75999338e960718dbfea1469d0948f9e14663cfe4`; spec
`anchors_candidateA.json` `5d9c99012acb795bb4b9c24559e7582e2c46f8f804fb3cfc70eb356ed854d1a6`.
