# EO-2026-09-29 — ADDENDUM F: B-3 Activation — `derive_camera_runs_v2.py`; correction notice
## Governance Status
Instrument: Executive Ruling (Addendum to EO-2026-09-29) · Authority:
Chairman/EP · Date: 2026-10-02 · Ruling: "CHAIRMAN NEXT TRANSACTION — ADDENDUM F /
derive_camera_runs_v2.py B-3 ACTIVATION". Basis: ECR-GEN-004 engineering custody
(`f2c6e2e1085bf36644b718c36977730d6397fbef`) and its committed qualification evidence. Register entry deferred
(per EO). The ruling's standing sections 2–8 are transcribed verbatim in §8; its
drafting and validation instructions are not standing authority and are not transcribed.
Addendum D, Addendum E, the Wave 1 qualification report, the historical producer and the
historical 08-22 outputs are not modified by this addendum.

## 1 — ACTIVATION RECORD

| field | value |
|---|---|
| producer | `derive_camera_runs_v2.py` (ECR-GEN-004 semantic successor) |
| repository path | `intelligence/p2/ess/scripts/derive_camera_runs_v2.py` |
| producer SHA-256 | `ec253c0595f8b325fecd5bd0a2e86299ede9e1c5f34610ace13419b7dddd6873` |
| ECR-GEN-004 custody commit | `f2c6e2e1085bf36644b718c36977730d6397fbef` |
| ECR-GEN-004 evidence | `docs/engineering/ECR_GEN_004_derive_camera_runs_UNCERTAIN.md` (`bc9d41ec1d125b892eee5607faa01e296af2a806515434284738e93478c31c24`), `docs/engineering/ECR_GEN_004_test_results.json` (`17b982cee78ad21b8eeaef8a602565f63c95e04173107ae04eb88246b79e1861`) |
| qualified interpreter | cpython 3.9.6, arm64, `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9` |
| interpreter binary SHA-256 | `bdea59019a38eb6600cc9e71e984a97fedadc406448431281e7657030f54987e` |
| qualification disposition | **PASS** — S1 PASS, Q1 PASS, Q2 PASS, W1 PASS, T1 PASS (5 passed, 0 failed) |
| status | **EFFECTIVE under B-3** for this exact producer/interpreter identity, within §3 only |

Values are read from the committed objects at `f2c6e2e`. The interpreter's path, version
and binary SHA-256 are from the ECR-GEN-004 results (T1); its architecture is from the committed
Wave 1 report, which records the same binary SHA-256.

**Per-producer criteria (Addendum E §5.1).** Approved ECR and code applied — ECR-GEN-004,
`f2c6e2e`. Final script SHA-256 and commit recorded — above. Toolchain pinned — the
interpreter identity above is part of the binding (§4). Qualification fixture passed and at least
two byte-identical reruns — three per fixture, historical and synthetic. No hidden writes — zero
undeclared writes in six runs. No unauthorized semantic behaviour — the only change from the
predecessor is the authorized fallback (static check 4/4). Chairman activation of that exact
qualified identity — this addendum.

## 2 — APPROVED B-3 SEMANTICS

`derive_camera_runs_v2.py` is a mechanical transcription of the FCPXML clip-name convention:
- a recognized camera-bearing element matching an established family → that recognized family;
- a camera-bearing element whose family cannot be assigned under the established convention → `UNCERTAIN`;
- contributed or non-camera media outside the camera-family convention → `UNCERTAIN`;
- structural or gap material outside the camera-family convention → `UNCERTAIN`;
- no camera family may be inferred from other evidence;
- `COMPOUND` is not an authorized fallback camera-family inference under this producer.

Historical outputs produced by the predecessor remain historical and unchanged.

## 3 — EFFECTIVE SCOPE

Permitted: consuming its explicitly supplied resolved-timeline input; applying the established
recognized-family convention; emitting deterministic camera-run output; emitting its approved
provenance sidecar.

Not permitted: inferring camera families from unrelated evidence; adjudicating editorial meaning;
assigning beats, segments or episodes; altering registries; altering source designations;
invoking other producers; changing narrative state; releasing regeneration holds. All Decision B
prohibitions (Addendum D) remain in force.

This addendum does not run the producer and does not authorize a run against the governed 08-24
package.

## 4 — IDENTITY BINDING AND INVALIDATION

The activation binds both the producer SHA-256 and the interpreter binary SHA-256 in §1, the
ECR-GEN-004 custody commit and its committed qualification evidence. Any change to the producer
bytes or to the bound interpreter binary invalidates this activation until the new combination is
requalified and separately activated. The path alone is not the identity.

## 5 — HISTORICAL PREDECESSOR

`intelligence/p2/ess/scripts/derive_camera_runs.py` (`178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a`) is preserved unchanged as the historical
implementation. Its Wave 1 qualification (`docs/engineering/ECR_GEN_003_WAVE1_QUALIFICATION_REPORT.md`)
remains valid historical evidence of that implementation's behaviour. It is not eligible for
activation under the corrected Decision B semantics. Its bytes are not deleted, edited, renamed or
superseded.

## 6 — CORRECTION NOTICE (additive; no record is rewritten)

The Wave 1 qualification report (§5) and Addendum E (§4) describe the nine historical `COMPOUND`
rows of the 08-22 fixture output as "contributed media and gaps" (Addendum E: "nine
contributed-media and gap elements, none a compound clip"), and attribute the wording "unknown
camera families are marked UNCERTAIN, not inferred" to Addendum D. Both documents are preserved
unchanged. This notice corrects them as follows:

1. **Composition.** The semantic audit recorded in the committed ECR-GEN-004 document (§6) establishes
   the more precise composition of those nine rows: five composite elements, one contributed asset
   and three gaps. Some rows are contributed or non-camera material, some are structural gaps, and
   some contain mixed or composite media; none is an FCP compound clip. The classification is cited
   from that evidence, not re-derived here.
2. **Attribution.** The UNCERTAIN wording is the Decision B packet's per-producer scope, which
   Addendum D incorporates by reference ("individual scopes exactly as specified in Decision B"); it
   is not text of Addendum D itself. The same rule is stated in `ENGINEERING_READINESS_REVIEW_ETC_GATE.md` G5.
3. **Conclusion unchanged.** The nine historical rows do not establish an authorized `COMPOUND`
   fallback camera-family category under Decision B / G5. They are not evidence that an unknown
   camera family should be inferred or emitted as `COMPOUND`.

The historical 08-22 outputs themselves are not altered.

## 7 — DECISION B PRODUCER STATE AFTER THIS RULING

Producer authority is per-producer (Addendum D, Decision B; Addendum E §4).

| producer | status |
|---|---|
| `fcpx_resolve.py` (`faacec8bd67b9be70cda79014953127cffeffd6e134da035d1bfe296ba866038`) | EFFECTIVE under B-3 pursuant to Addendum E (`5cf7ce0a67659236dd4f0a044b917eb80e1f1f50b749bf0a8343288f9d5cb294`, commit `894aff6`) |
| `derive_camera_runs_v2.py` (`ec253c0595f8b325fecd5bd0a2e86299ede9e1c5f34610ace13419b7dddd6873`) | EFFECTIVE under B-3 pursuant to this Addendum F |
| `derive_camera_runs.py` (`178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a`) | inactive; historical only |
| `produce_audio_rms.py` | not effective — pending D2 and qualification |
| `step0_offset.py` | not effective — pending D2 and qualification, plus applicable D4 constraints |
| `step0_anchors.py` | not effective — pending D2 and qualification |
| `produce_video_obs.py` | not effective — pending the separate HDR / 08-24 ruling and qualification |

Decision B as a complete producer package therefore remains incomplete.

## 8 — VERBATIM: CHAIRMAN RULING (sections 2–8)
```text
2. Correct the earlier historical-row characterization
Addendum F must record a correction notice, without rewriting historical records in place.
The Wave-1 report and Addendum E used an overbroad description of the nine historical COMPOUND rows.
Preserve those documents unchanged, but state that ECR-GEN-004's semantic audit established the more precise composition recorded in the committed ECR-GEN-004 evidence.
The correction must preserve this substantive conclusion:
the nine historical rows do not establish an authorized COMPOUND fallback camera-family category under Decision B/G5.
In particular:
- some rows are contributed/non-camera or structural material;
- some contain mixed/composite media;
- they are not evidence that an unknown camera family should be inferred or emitted as COMPOUND.
Cite the committed ECR-GEN-004 evidence rather than re-deriving the row classification.
Do not alter the historical 08-22 outputs themselves.
3. Activate the versioned successor
Activate only the exact qualified:
derive_camera_runs_v2.py
producer/runtime identity.
Use the existing status vocabulary:
EFFECTIVE under B-3
Bind activation to:
- exact successor script SHA-256;
- exact interpreter binary identity used during requalification;
- ECR-GEN-004 custody commit;
- committed ECR-GEN-004 qualification evidence.
Any future change to either the producer bytes or bound interpreter binary invalidates the activation until the new combination is requalified and separately activated.
4. Approved B-3 semantics
Addendum F must state the corrected producer semantics:
- recognized camera-bearing element matching an established family → that recognized family;
- camera-bearing element whose family cannot be assigned under the established convention → UNCERTAIN;
- contributed/non-camera media outside the camera-family convention → UNCERTAIN;
- structural/gap material outside the camera-family convention → UNCERTAIN;
- no camera family may be inferred from other evidence;
- COMPOUND is not an authorized fallback camera-family inference under this producer.
Historical outputs produced by the predecessor remain historical and unchanged.
5. Historical predecessor status
Record that:
derive_camera_runs.py
remains preserved as the historical implementation and its prior Wave-1 qualification remains valid historical evidence of that implementation's behavior.
It is not eligible for activation under the corrected Decision-B semantics.
Do not delete, edit, rename, or supersede its bytes.
6. Scope and prohibitions
The active derive_camera_runs_v2.py identity is authorized only for the established mechanical B-3 camera-run scope.
It may:
- consume its explicitly supplied resolved-timeline input;
- apply the established recognized-family convention;
- emit deterministic camera-run output;
- emit its approved provenance sidecar.
It may not:
- infer camera families from unrelated evidence;
- adjudicate editorial meaning;
- assign beats, segments, or episodes;
- alter registries;
- alter source designations;
- invoke other producers;
- change narrative state;
- release regeneration holds.
7. Decision-B state after Addendum F
Record the producer state explicitly:
- fcpx_resolve.py — EFFECTIVE under B-3 pursuant to Addendum E;
- derive_camera_runs_v2.py — EFFECTIVE under B-3 pursuant to Addendum F;
- historical derive_camera_runs.py — inactive/historical only;
- produce_audio_rms.py — not effective, pending D2 and qualification;
- step0_offset.py — not effective, pending D2 and qualification plus applicable D4 constraints;
- step0_anchors.py — not effective, pending D2 and qualification;
- produce_video_obs.py — not effective, pending the separate HDR/08-24 ruling and qualification.
Decision B as a complete producer package therefore remains incomplete.
Do not invent a new package-level status token.
8. Preserve all other gates
Addendum F does not:
- provision D2;
- resolve D4/S19;
- resolve D5 BLOCKED classes;
- complete D6/G-01–G-09;
- authorize an 08-24 observation run;
- create AR2-0824.observations.json;
- release either regeneration hold.
```

## SCOPE
This addendum does not provision D2, resolve D4/S19, resolve D5 BLOCKED classes, complete D6
(G-01–G-09), authorize an 08-24 observation run, or create `AR2-0824.observations.json`. No
producer code, registry, Decision A or Decision C artifact is changed. No producer is run. Both
regeneration holds (v1.14.0, v1.15.0) remain HELD.
