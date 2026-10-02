# EO-2026-09-29 — ADDENDUM G: B-3 Activation — `step0_anchors.py`
## Governance Status
Instrument: Executive Ruling (Addendum to EO-2026-09-29) · Authority:
Chairman/EP · Date: 2026-10-02 · Ruling: "CHAIRMAN NEXT TRANSACTION — ADDENDUM G /
step0_anchors.py B-3 ACTIVATION". Basis: the Wave 2A qualification evidence in remote custody
(`d491e1d7109bf8c6a28f4c8308f207d02b5e50f3`). Register entry deferred (per EO). The ruling's standing sections 2–8 are
transcribed verbatim in §8; its sourcing, drafting and validation instructions are not standing
authority and are not transcribed. Addenda D, E and F, the Wave 1 and Wave 2A qualification
evidence, the producer, Candidate A and the historical generator and documents are not modified by
this addendum.

## 1 — ACTIVATION RECORD

| field | value |
|---|---|
| producer | `step0_anchors.py` |
| repository path | `intelligence/p2/ess/scripts/step0_anchors.py` |
| producer SHA-256 | `66079f2ada0f60c186edc43cf82fe3f02e9e22568b986695445c5e89535d474e` |
| ECR-GEN-003 commit | `e0a346a16abf77db4a6abe5d59a2b31dadcf4464` |
| Wave 2A qualification-evidence commit | `d491e1d7109bf8c6a28f4c8308f207d02b5e50f3` (`docs/engineering/ECR_GEN_003_WAVE2A_QUALIFICATION_REPORT.md` `ec21b57899fffb9fccc6ce8943a2aa4aafccba3654a438212477c5d8c673c2e6`, `docs/engineering/ECR_GEN_003_wave2a_test_results.json` `c0b246cb8ad5e53155f4a236776e5566df991fb8400423e49ff28dfb515a4886`) |
| qualified interpreter | cpython 3.10.12, arm64, `/Volumes/WE_CAPE_OUTPUT/_b3_toolchains/d2_cp31012_np226/python/bin/python3.10` |
| interpreter binary SHA-256 | `3a855bd1956b302372f02be42ea2ada298306fd57717f8eee1d0c86c9db003a3` |
| NumPy | 2.2.6, installed from wheel `numpy-2.2.6-cp310-cp310-macosx_11_0_arm64.whl` (`8e41fd67c52b86603a91c1a505ebaef50b3314de0213461c7a6e99c9a3beff90`) |
| NumPy installed-file manifest | `36fa915dcd44185fd9361d187e20994281713df429c9c6f77bc7d26578f61f4a` (1008 files, including the bundled `numpy/.dylibs/libscipy_openblas64_.dylib`) |
| BLAS / LAPACK (recorded) | scipy-openblas 0.3.29 (`OpenBLAS 0.3.29  USE64BITINT DYNAMIC_ARCH NO_AFFINITY neoversen1 MAX_THREADS=64`) |
| Candidate A prefix manifest | `07f2ce264213cd8c0a4d48c0f5787aa7ec5b76327db1a8eb62d9559f4b537702` (3139 files) |
| qualification fixture | 08-22 lock SRT `89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b`; 08-22 resolved timeline `ebf99f84ceb9dcf487b4703f1e377dd55296ff90d10aaac6a1c6bd3eacc791f8` |
| qualification disposition | **PASS** — W2A-ID, W2A-TC, W2A-PX, W2A-FX, W2A-SE, W2A-DET, W2A-WA, W2A-OR, W2A-ST, W2A-784 (10 passed, 0 failed) |
| reruns | 3, byte-identical: output `b3e6a204a0d39f922648891782f813b04714abae14a78836e41a0a75bd481a27`, sidecar `fe3f0480c9b8fbfe5cbee4df23a01b4f40f322af2abd59bc9d4a0f7a52bec31d` |
| status | **EFFECTIVE under B-3** for this exact producer/runtime identity, within §3 only |

Values are read from the committed producer at HEAD and the committed Wave 2A evidence at
`d491e1d`. The interpreter's architecture is read from the Candidate A identity record outside
Git, whose SHA-256 the committed Wave 2A report records (`e9d9ae7d02479d062d7b230092bdb940b9a4635acbb15f1c3bd5753feab7f9f3`).

**Per-producer criteria (Addendum E §5.1).** Approved ECR and code applied — ECR-GEN-003,
`e0a346a`. Final script SHA-256 and commit recorded — above. Toolchain pinned — the interpreter
and NumPy identities above are part of the binding (§4). Qualification fixture passed and at least
two byte-identical reruns — three, on the authorized 08-22 fixture. No hidden writes — zero
undeclared writes. No unauthorized semantic behaviour — the producer is statically equivalent to its
pre-ECR version (machine paths only). Chairman activation of that exact qualified identity — this
addendum.

## 2 — WHAT WAVE 2A QUALIFIED

The committed Wave 2A evidence establishes, under Candidate A on the authorized 08-22 fixture:
- all 19 producer rows reproduce;
- the committed downstream `abs(delta) <= 2.5` selection reproduces the historical 11-row consumer set;
- row identity, order and delta values reproduce;
- the committed median (+0.708 s), span, coverage, drift and CI evidence within the
  producer/consumer chain reproduces as documented;
- three reruns are byte-identical;
- provenance sidecars are byte-identical;
- zero undeclared writes occurred;
- Candidate A did not drift.

The 11-row selection is a consumer rule (`gen_artifacts.py`); it is not part of this producer and
this activation does not move it into the producer.

## 3 — EFFECTIVE SCOPE

Permitted: consuming explicitly supplied SRT and resolved-timeline inputs; mechanically deriving its
established anchor output; preserving the qualified ordering and statistical behaviour; emitting its
deterministic provenance sidecar.

Not permitted: inferring editorial meaning; assigning beats, segments or episodes; changing source
designations; modifying registries; changing thresholds or filtering rules; invoking other producers;
adjudicating the historical 0.784 narrative; releasing regeneration holds. All Decision B
prohibitions (Addendum D) remain in force.

This addendum does not run the producer and does not authorize a run against the governed 08-24
package.

## 4 — IDENTITY BINDING AND INVALIDATION

The activation is valid only for the qualified producer/runtime combination:
- the producer bytes, SHA-256 `66079f2ada0f60c186edc43cf82fe3f02e9e22568b986695445c5e89535d474e`;
- the Candidate A interpreter binary, SHA-256 `3a855bd1956b302372f02be42ea2ada298306fd57717f8eee1d0c86c9db003a3`;
- the NumPy 2.2.6 installation used in qualification, installed-file manifest `36fa915dcd44185fd9361d187e20994281713df429c9c6f77bc7d26578f61f4a` (from
  wheel `8e41fd67c52b86603a91c1a505ebaef50b3314de0213461c7a6e99c9a3beff90`), which includes the bundled OpenBLAS library behind the recorded BLAS/LAPACK
  configuration.

A change to the producer SHA-256, the interpreter binary identity, the NumPy package identity, or the
qualified numeric-runtime identity recorded in §1 (the BLAS/LAPACK configuration and the Candidate A
prefix manifest) invalidates this activation until the new combination is requalified and separately
activated. The path alone is not the identity. ffmpeg and ffprobe do not participate in
`step0_anchors.py` and are not part of this binding.

## 5 — THE 0.784 CLARIFICATION (cited from the committed Wave 2A evidence)

A calculation capable of reproducing 0.784 was identified in scratch, but no committed evidence establishes that calculation as the historical source of the literal. The value is not part of step0_anchors.py's output contract and is outside this producer qualification.

As recorded in the committed Wave 2A report (§6):
- `step0_anchors.py` emits no SD field;
- no producer-output schema requires an SD field;
- a scratch calculation capable of reproducing 0.784 was identified; it is diagnostic only;
- no committed evidence establishes that calculation as the historical source of the literal;
- 0.784 is outside the producer's qualified output contract;
- the historical generator and document text remains unchanged.

This addendum does not adopt the scratch calculation as provenance and does not adjudicate the
historical 0.784 narrative.

## 6 — LIMITS OF THE CANDIDATE A QUALIFICATION

Qualification of `step0_anchors.py` under Candidate A does not establish:
- Candidate A fidelity for `step0_offset.py`, which retains its independent NumPy, RNG and BLAS
  qualification requirement;
- Candidate A + F1 suitability for `produce_audio_rms.py`;
- Candidate A + F2 suitability for `produce_audio_rms.py`;
- qualification of any ffmpeg implementation;
- qualification for the governed 08-24 source.

## 7 — DECISION B PRODUCER STATE AFTER THIS RULING

Producer authority is per-producer (Addendum D, Decision B; Addendum E §4).

| producer | status |
|---|---|
| `fcpx_resolve.py` (`faacec8bd67b9be70cda79014953127cffeffd6e134da035d1bfe296ba866038`) | EFFECTIVE under B-3 pursuant to Addendum E (`5cf7ce0a67659236dd4f0a044b917eb80e1f1f50b749bf0a8343288f9d5cb294`, commit `894aff6`) |
| `derive_camera_runs_v2.py` (`ec253c0595f8b325fecd5bd0a2e86299ede9e1c5f34610ace13419b7dddd6873`) | EFFECTIVE under B-3 pursuant to Addendum F (`d218e25012885fdc033360b5f04cfb3034ef2ad0a77ab115a0e9ad29af39d7c3`, commit `bc32e85`) |
| `step0_anchors.py` (`66079f2ada0f60c186edc43cf82fe3f02e9e22568b986695445c5e89535d474e`) | EFFECTIVE under B-3 pursuant to this Addendum G |
| `derive_camera_runs.py` (`178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a`) | inactive; historical only |
| `produce_audio_rms.py` | not effective — qualification pending |
| `step0_offset.py` | not effective — qualification pending, plus applicable D4 constraints |
| `produce_video_obs.py` | not effective — the separate HDR / 08-24 ruling and qualification pending |

Decision B as a complete producer package therefore remains incomplete.

## 8 — VERBATIM: CHAIRMAN RULING (sections 2–8)
```text
2. Activation binding
Bind the activation to the exact combination that was qualified:
- exact step0_anchors.py bytes;
- exact Candidate-A Python interpreter binary;
- exact NumPy installation/package identity used during qualification.
The activation is valid only for that qualified producer/runtime combination.
A change to any of the following invalidates the activation until requalification and a new activation ruling:
- producer SHA-256;
- Python interpreter binary identity;
- NumPy package identity;
- materially relevant qualified numeric-runtime identity.
Do not bind this producer to ffmpeg or ffprobe; neither participates in step0_anchors.py.
3. Approved B-3 scope
Upon Addendum G reaching remote custody, the exact qualified step0_anchors.py identity becomes:
EFFECTIVE under B-3 within its qualified scope only.
Its scope is limited to:
- consuming explicitly supplied SRT/timeline inputs;
- mechanically deriving its established anchor output;
- preserving the qualified ordering/statistical behavior;
- emitting its deterministic provenance sidecar.
It receives no authority to:
- infer editorial meaning;
- assign beats, segments, or episodes;
- change source designations;
- modify registries;
- change thresholds or filtering rules;
- invoke other producers;
- adjudicate the historical 0.784 narrative;
- release regeneration holds.
4. Preserve the 0.784 qualification clarification
Addendum G should cite the committed Wave-2A evidence and preserve its finding:
- step0_anchors.py emits no SD field;
- no producer-output schema requires an SD field;
- a scratch calculation capable of reproducing 0.784 was identified;
- no committed evidence establishes that calculation as the historical source of the literal;
- 0.784 is outside the producer's qualified output contract;
- historical generator/document text remains unchanged.
Do not repeat the earlier false formulation that no computation can produce 0.784.
Do not promote the scratch calculation into governing provenance.
5. State what Wave-2A actually qualified
Record that qualification established:
- all 19 producer rows reproduce;
- the committed downstream abs(delta) <= 2.5 selection reproduces the historical 11-row consumer set;
- row identity/order/delta values reproduce;
- the committed median/span/coverage/drift/CI evidence within the producer/consumer chain reproduces as documented;
- three reruns are byte-identical;
- provenance sidecars are byte-identical;
- zero undeclared writes occurred;
- Candidate A did not drift.
6. Do not over-generalize Candidate A
Addendum G must explicitly state that qualification of step0_anchors.py under Candidate A does not establish:
- Candidate-A fidelity for step0_offset.py;
- Candidate-A + F1 suitability for produce_audio_rms.py;
- Candidate-A + F2 suitability for produce_audio_rms.py;
- qualification of any ffmpeg implementation;
- qualification for the governed 08-24 source.
step0_offset.py retains its independent NumPy/RNG/BLAS qualification requirement.
7. Per-producer state after Addendum G
Record:
- fcpx_resolve.py — EFFECTIVE under B-3 / Addendum E;
- derive_camera_runs_v2.py — EFFECTIVE under B-3 / Addendum F;
- step0_anchors.py — EFFECTIVE under B-3 / Addendum G;
- historical derive_camera_runs.py — inactive / historical only;
- produce_audio_rms.py — not effective, qualification pending;
- step0_offset.py — not effective, qualification pending plus applicable D4 constraints;
- produce_video_obs.py — not effective, HDR/08-24 ruling and qualification pending.
Decision B as a complete producer package remains incomplete.
8. Preserve all remaining gates
Addendum G does not:
- select F1 or F2;
- qualify produce_audio_rms.py;
- qualify step0_offset.py;
- authorize any 08-24 producer execution;
- resolve D4/S19;
- resolve D5;
- complete D6;
- create AR2-0824.observations.json;
- release either regeneration hold.
```

## SCOPE
This addendum does not select F1 or F2, qualify `produce_audio_rms.py` or `step0_offset.py`,
authorize any 08-24 producer execution, resolve D4/S19, resolve D5, complete D6, or create
`AR2-0824.observations.json`. No producer code, Candidate A file, registry, prior Addendum,
qualification evidence, or Decision A or Decision C artifact is changed. No producer is run. Both
regeneration holds (v1.14.0, v1.15.0) remain HELD.
