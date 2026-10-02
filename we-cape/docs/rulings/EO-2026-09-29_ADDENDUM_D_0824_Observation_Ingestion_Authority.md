# EO-2026-09-29 — ADDENDUM D: 08-24 Observation / Ingestion Authority
## Governance Status
Instrument: Executive Ruling (Addendum to EO-2026-09-29) · Authority:
Chairman/EP · Date: 2026-10-01 (§4: 2026-10-02) · Rulings: "CHAIRMAN
RULING — 08-24 OBSERVATION / INGESTION AUTHORITY", "CHAIRMAN CORRECTION —
DECISION C / 08-24 INGESTION" and "CHAIRMAN RULING — DECISION C FINAL
SEMANTICS". Basis: the 08-24 observation/ingestion readiness audit and
authority decision packet (read-only, 2026-10-01). Register entry deferred
(per EO). This addendum is the durable record required by the ruling's
transaction step 1 ("Durably record the Decision A and Decision C Chairman
authority using the existing repository ruling/designation mechanism").
All three rulings are transcribed verbatim below; the execution instructions that
followed each (transaction steps, report list, STOP conditions) are not
standing authority and are not transcribed.

## 1 — EFFECT, AS CORRECTED (summary; the verbatim text in §2–§4 governs)
- **Decision A — APPROVED.** `Alpha RoudUp Part 2.mov`, sha256
  `ff34278fe1f47f678b36066780c3498633d27761655001ea97163099da9bbffe`
  (`WE_CAPE_OUTPUT/AlphaRoundUp_2026/Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2
  ANALYSIS/Corrected Video Analysis Files/`), is the designated 08-24
  OBSERVATION SOURCE for AR2-0824, observed directly. No proxy, derived-media,
  viewing-master, ED-005/SOP-06, regeneration, adjudication or editorial
  authority is added.
- **Decision B — CONDITIONALLY APPROVED, NOT YET EFFECTIVE.** Correction item
  4: the producer names `stage_offset.py` / `stage_anchors.py` were a typo for
  `step0_offset.py` / `step0_anchors.py`. No B-3 producer authority is
  effective; every listed prerequisite still applies.
- **Decision C — APPROVED, AS CORRECTED.** The declared ETC lock is
  `01:18:09:11` (last valid frame 112547; exclusive boundary 112548;
  boundary time 01:18:09.500), carried by a **successor** ETC; the incumbent
  ETC (sha256 `8c76a8cf460a450ea0dcbcd7802cae7fb3245cb1c8b4576a3a9f55ab185b0aaa`,
  `declared_lock: null`) is preserved unedited as historical evidence. The
  earlier value `01:18:09:12` is superseded.
  `regeneration_scope.mode: CANONICAL_EDITORIAL_TIMELINE` (no hold is
  released). ERO-001 GNB-001 (the 08-22 S12/S13 transitional overlap) is NOT
  carried into the 08-24 context; R4 makes that edge a single cut.
- **Decision D — ADOPTED** as mandatory prerequisites to generating
  `AR2-0824.observations.json`.
- **Final semantics (§4).** `git_commit` in the 08-24 context is the 08-24
  ingestion commit itself (Commit A), recorded by a following
  provenance-closure commit (Commit B); `de0c902` is the repository basis,
  not the field's value. `regen_run_id` is absent before generation (the
  generator then uses its own `RUN_ID`). The successor manifest's `Music/`
  entry is repaired to valid YAML, its value unchanged; v0.1.0 is preserved
  with its defect. IP-1 to IP-8 are unchanged.

## 2 — CHAIRMAN RULING — VERBATIM (Decisions A–D)
```text
CHAIRMAN RULING — 08-24 OBSERVATION / INGESTION AUTHORITY
The 08-24 observation/ingestion decision packet is approved with the following dispositions.
DECISION A — B-7 OBSERVATION SOURCE: APPROVED
Approve the exact Alpha RoundUp Part 2.mov source and SHA-256 identified in Decision A as the designated 08-24 OBSERVATION SOURCE for AR2-0824.
Authority added is limited to:
- direct decode and measurement of that exact hash-bound source;
- only by a valid B-3-designated observation producer;
- only for producing the authorized observation intermediates and eventual AR2-0824.observations.json;
- SHA-256 must be reverified before every read.
This designation supersedes the contradictory template language concerning observation-use authority.
It does not add:
- proxy or derived-media authority;
- authority to generate a new proxy;
- viewing-master authority;
- ED-005/SOP-06 export authority;
- regeneration authority;
- episode/segment adjudication authority;
- narrative/editorial authority.
Existing review and excerpt authority is unchanged.
No derived proxy is authorized. Observe the designated MOV directly.
DECISION B — B-3 OBSERVATION PRODUCERS: CONDITIONALLY APPROVED, NOT YET EFFECTIVE
Approve the producer set and individual scopes exactly as specified in Decision B:
- produce_audio_rms.py
- produce_video_obs.py
- fcpx_resolve.py
- derive_camera_runs.py
- stage_offset.py / stage_anchors.py within their specified scope
However, this is a conditional designation specification only.
No B-3 producer authority becomes effective until:
1. the required path-parameterization ECR is approved and applied;
2. the parameterized versions are reverified on the required fixture;
3. each final script SHA-256 / commit identity is recorded;
4. the required ffmpeg/ffprobe, Python, and numpy versions are pinned and reproducible;
5. byte-identical deterministic reruns are demonstrated.
No producer inherits authority from another producer or from video_producer.
die_v_observables.py is not designated, because it performs threshold classification.
All prohibitions stated in the Decision B packet remain in force, including no editorial inference, beat/segment assignment, unsupported classification, narrative determination, or registry modification.
DECISION C — 08-24 INGESTION AND PINNING: APPROVED
Approve the exact proposed Decision C target state.
This includes:
- the exact source-file paths identified in the packet;
- the measured/recoverable SHA values;
- the Decision A MOV as source_files.mp4;
- direct-source use with no derived proxy designation;
- the measured ETC census/connectivity values;
- the declared ETC lock identified in the packet;
- ETC acceptance;
- the approved 08-24 regeneration scope;
- the approved governed-narrative-boundary / overlap carry-over exactly as specified;
- factual display names and measured ffprobe properties;
- repository/ingestion provenance recorded by the ingestion transaction;
- supersession of the existing ingestion manifest according to repository procedure.
Do not invent or normalize any measured value. If a proposed declared value does not equal the remeasured value, stop and report the discrepancy.
regen_run_id or equivalent generation state must remain in its pre-generation / awaiting-generation condition. This transaction does not constitute regeneration.
DECISION D — PRE-OBSERVATION GENERATION GATE: ADOPTED
Adopt all Decision D conditions as mandatory prerequisites to generating AR2-0824.observations.json.
In particular, observation generation is prohibited until:
1. Decisions A, B, and C are fully effective;
2. the producer ECR/toolchain work is completed and reverified;
3. the 08-24 context is ingested and hash-bound;
4. an explicit S19 observation-segment disposition exists;
5. every currently BLOCKED observation class has either valid rebase/re-derivation authority or a specific Chairman declaration that it is NOT_OBSERVED for this run;
6. all applicable G-01 through G-09 dry-run guards pass with deterministic reassembly;
7. both regeneration holds remain HELD.
No placeholder observation values are permitted.
Absence of authority is not evidence of NOT_OBSERVED; that status requires an explicit governing declaration where required.
```

## 3 — CHAIRMAN CORRECTION — VERBATIM (items 1–4)
```text
CHAIRMAN CORRECTION — DECISION C / 08-24 INGESTION
The scratch audit is accepted. The previous Decision C authorization is corrected as follows.
1. ETC declared lock — choose option (b)
The previously approved 01:18:09:12 value was incorrect.
The repository convention records the last valid frame, not the exclusive boundary frame.
For the 08-24 source duration of 4689.500 s at 24 fps:
- exclusive boundary = frame 112548;
- last valid frame = frame 112547;
- correct declared-lock timecode = 01:18:09:11;
- measured boundary time remains 01:18:09.500.
Supersede the earlier Decision C declared-lock value with:
declared_lock: 01:18:09:11
Do not rewrite the existing ETC contract whose hash is 8c76a8cf... and whose declared_lock is null.
Instead, use the established ETC procedure to create a successor ETC contract with declared_lock: 01:18:09:11.
The successor ETC necessarily receives a new SHA-256 and must be re-pinned through the normal ingestion/context process.
Preserve the original ETC and its hash as historical evidence.
If producing the successor ETC changes anything other than the authorized declared-lock addition plus metadata mechanically required by the ETC contract format, stop and report.
2. 08-24 regeneration scope
Set the 08-24:
regeneration_scope.mode: CANONICAL_EDITORIAL_TIMELINE
Use the repository's existing token exactly.
This authorization applies to the 08-24 ingestion/context state only. It does not release either regeneration hold and does not authorize a regeneration run.
3. GNB-001 / overlap carry-over
Do not carry forward ERO-001 GNB-001's 08-22 S12/S13 transitional overlap into the 08-24 context.
R4 establishes the corresponding 08-24 edge as a single cut.
Therefore, for that S12/S13 edge:
- no transitional overlap is declared;
- use the existing schema representation for no declared overlap / empty overlap set;
- do not invent a new status/token.
This ruling is limited to the former GNB-001 S12/S13 overlap. Do not delete or alter any unrelated governed-narrative-boundary information.
4. Decision B filename correction
Confirm the prior packet contained a naming typo.
The intended script names are:
- step0_offset.py
- step0_anchors.py
not:
- stage_offset.py
- stage_anchors.py
This correction does not make their B-3 producer designation effective. All previously specified ECR, parameterization, toolchain-pinning, hash-recording, fixture-verification, and determinism prerequisites still apply.
```

## 4 — CHAIRMAN RULING — DECISION C FINAL SEMANTICS — VERBATIM (sections 1–5)
```text
CHAIRMAN RULING — DECISION C FINAL SEMANTICS
The two stop conditions are resolved as follows.
1. git_commit — OPTION (a)
For the 08-24 Decision C context:
git_commit
means the 08-24 ingestion commit itself, consistent with:
- ERO-001's "08-24 ingestion commit" language;
- B-8 treating it as a missing ingestion input;
- generator output describing it as repository provenance.
Do not set git_commit to the earlier basis commit de0c902….
That commit remains provenance for the repository state from which the ingestion was constructed, but it is not the value of this field.
Because the ingestion commit cannot contain its own hash, use the following controlled two-commit procedure locally:
Commit A — ingestion custody
- Apply the already-authorized Decision C files and corrected successor-manifest YAML.
- Keep git_commit absent/unset exactly as permitted by the existing pre-ingestion representation; do not invent a placeholder token.
- Apply the regen_run_id ruling below.
- Run all validation possible on this provisional ingestion state.
- Create Commit A locally only.
- Do not push.
Commit A's full Git hash becomes the authoritative:
git_commit
value for this ingestion.
Commit B — provenance closure
- Set git_commit to the full hash of Commit A.
- Update only mechanically dependent hashes/manifests/validation artifacts required because the context bytes changed.
- Record that Commit A is the ingestion commit and Commit B is the provenance-closure commit.
- Re-run complete deterministic validation.
- Create Commit B locally only.
Do not push either commit until Chairman review of the final Commit-B state.
If repository precedent prohibits this two-commit closure model, stop before Commit A and report the conflicting rule.
2. regen_run_id — OPTION (b)
Remove regen_run_id from the pre-generation 08-24 context.
Rationale:
- AWAITING_INGESTION has an established meaning of ingestion not yet complete and becomes false once Decision C closes;
- NOT_COMPUTED is not an appropriate regeneration-run identity;
- no new token should be invented;
- the generator already implements the intended behavior:
CTX.get('regen_run_id', RUN_ID)
so absence of the key causes the actual regeneration run to use its own RUN_ID.
The absence of regen_run_id before generation therefore means no regeneration run has yet been assigned.
Before applying this ruling, verify that no operative schema requires the key to exist.
If an operative schema requires a value, stop and report the conflict rather than choosing another token.
Do not modify generator code to accommodate this ruling.
3. Successor-manifest YAML repair — APPROVED
Apply the already prepared repair to the v0.2.0 successor manifest only.
Convert the invalid Music/ flow-mapping/block-scalar construction into valid YAML while preserving its semantic text exactly.
Requirements:
- successor v0.2.0 parses successfully;
- semantic value is unchanged;
- preserved v0.1.0 remains byte-identical, including its historical syntax defect;
- no unrelated manifest cleanup.
4. Intermediate products
Leave IP-1 through IP-8 unchanged.
No B-3 producer has run, so this ingestion transaction does not authorize positive observation/intermediate-product statuses.
5. Existing Decision C state remains authoritative
Preserve:
- Decision A source designation and SHA identity;
- successor ETC with declared_lock: 01:18:09:11;
- regeneration_scope.mode: CANONICAL_EDITORIAL_TIMELINE;
- no S12/S13 transitional-overlap carry-over;
- the measured source hashes and counts already validated;
- committed resolver evidence without rerunning fcpx_resolve.py;
- the corrected script names step0_offset.py and step0_anchors.py.
The local-volume integrity audit does not change the governed Decision C source set.
```

## SCOPE
No EPR-001 or TIMELINE value is changed by this addendum. No observation is
produced, no B-3 producer is made effective, no proxy is created or
designated, and no regeneration is authorized; both regeneration holds
(v1.14.0, v1.15.0) remain HELD. S19 observation treatment, PBC-3 and
PDR-2026-08-22-ESS-001 are not resolved.
