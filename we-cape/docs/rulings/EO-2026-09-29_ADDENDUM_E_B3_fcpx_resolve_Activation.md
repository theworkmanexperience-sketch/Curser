# EO-2026-09-29 — ADDENDUM E: B-3 Activation — `fcpx_resolve.py`
## Governance Status
Instrument: Executive Ruling (Addendum to EO-2026-09-29) · Authority:
Chairman/EP · Date: 2026-10-02 · Rulings: "CHAIRMAN B-3 ACTIVATION RULING —
fcpx_resolve.py ONLY" as confirmed by "CHAIRMAN CONFIRMATION — fcpx_resolve.py
B-3 ACTIVATION". Basis: the Wave 1 qualification evidence in remote custody
(`1def9eae522111d1604e37e02d64ee7d9f509da2`). Register entry deferred (per EO).

The activation ruling as first issued carried a malformed (65-character) SHA-256;
the Confirmation supersedes it as to the producer identity and adds the runtime
binding. The malformed value is not reproduced here. The Confirmation (§5) is
transcribed verbatim; its validation and reporting instructions are execution
instructions, not standing authority, and are not transcribed.

## 1 — ACTIVATION RECORD

| field | value |
|---|---|
| producer | `fcpx_resolve.py` |
| repository path | `intelligence/p2/ess/scripts/fcpx_resolve.py` |
| producer SHA-256 | `faacec8bd67b9be70cda79014953127cffeffd6e134da035d1bfe296ba866038` |
| ECR-GEN-003 commit | `e0a346a16abf77db4a6abe5d59a2b31dadcf4464` |
| Wave 1 qualification-evidence commit | `1def9eae522111d1604e37e02d64ee7d9f509da2` (`docs/engineering/ECR_GEN_003_WAVE1_QUALIFICATION_REPORT.md`, `docs/engineering/ECR_GEN_003_wave1_test_results.json`) |
| qualified interpreter | cpython 3.9.6, arm64, `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9` |
| interpreter binary SHA-256 | `bdea59019a38eb6600cc9e71e984a97fedadc406448431281e7657030f54987e` |
| qualification disposition | **PASS** (E1 `VALIDATED` 191 / 191; E2–E4 STOP cases; output, stdout and exit byte-identical to the pre-ECR oracle; 3 byte-identical reruns per case; zero undeclared writes) |
| status | **EFFECTIVE under B-3** for this exact producer/interpreter identity, within §2 only |

All values above are taken from the committed producer at `e0a346a` and the
committed Wave 1 evidence at `1def9ea`.

**Per-producer criteria (ruling of the B-3 producer ECR scope, item 9, verbatim in §5).**
Approved ECR — ECR-GEN-003. Authorized code changes applied — `e0a346a`. Final script
SHA-256 and commit recorded — above. Toolchain pinned — the qualified interpreter identity
above is part of the binding (§3). Qualification fixture passed and at least two
byte-identical deterministic reruns — three per case. No hidden writes — zero undeclared
writes in 15 current-producer runs. No unauthorized semantic behaviour — resolver output
unchanged from the pre-ECR instrument. Chairman activation of that exact qualified
identity — this addendum.

## 2 — EFFECTIVE SCOPE (measurement and validation only)

Permitted: parsing and validating supplied FCPXML and ETC inputs; producing the declared
resolved-timeline / census output; enforcing the existing validation and STOP conditions;
emitting the approved deterministic provenance sidecar.

Not permitted: adjudicating editorial meaning; assigning beats, segments or episodes;
altering registries; changing source designations; inferring narrative intent; performing
unrelated observation classifications; invoking other producers; releasing regeneration
holds. All Decision B prohibitions (Addendum D) remain in force.

This addendum does not itself run the producer, and does not authorize a run against the
governed 08-24 package; any such run is a separate act.

## 3 — IDENTITY BINDING AND INVALIDATION

The activation binds both the producer SHA-256 and the interpreter binary SHA-256 recorded
in §1. Any change to either — a code change of any size, or a different binary behind the
interpreter path, including behind `/usr/bin/python3` — invalidates this activation until
the successor combination is requalified and separately activated. The path alone is not
the identity.

## 4 — DECISION B PRODUCER STATUS AFTER THIS RULING

Producer authority is per-producer ("No producer inherits authority from another producer",
Addendum D, Decision B).

| producer | status |
|---|---|
| `fcpx_resolve.py` | EFFECTIVE under B-3 for the identity in §1, scope §2 |
| `derive_camera_runs.py` | technically qualified (`178ca2b0c8841cd7c5986b8d7787f97e7d800f5b5f5ea8c00183d07c4bc73d2a`, Wave 1 PASS) but NOT EFFECTIVE, pending semantic reconciliation |
| `produce_audio_rms.py`, `step0_offset.py`, `step0_anchors.py` | NOT EFFECTIVE (not qualified; D2 toolchain held) |
| `produce_video_obs.py` | NOT EFFECTIVE (not qualified; separate HDR / 08-24 semantic ruling required) |

Decision B as a complete producer package therefore remains incomplete.

**Noted, not resolved:** the Decision B scope approved in Addendum D says unknown camera
families are marked UNCERTAIN, not inferred; the qualified `derive_camera_runs.py` labels
unmatched elements COMPOUND (on the 08-22 fixture, nine contributed-media and gap elements,
none a compound clip). That producer and its designation are not changed by this addendum.

## 5 — VERBATIM

### 5.1 — Per-producer activation criteria (CHAIRMAN RULING — B-3 PRODUCER ECR SCOPE / D2 TOOLCHAIN HOLD, item 9)
```text
9. Decision-B activation remains producer-specific
Producer identities may ultimately be qualified individually.
No producer becomes effective until its own final identity satisfies:
- approved ECR;
- authorized code changes applied;
- final script SHA-256 recorded;
- final commit recorded;
- toolchain pinned;
- qualification fixture passed;
- at least two byte-identical deterministic reruns;
- no hidden writes;
- no unauthorized semantic behavior;
- Chairman activation of that exact qualified identity.
produce_video_obs.py additionally requires the separate HDR/08-24 semantic ruling before activation for the governed source.
```

### 5.2 — CHAIRMAN CONFIRMATION — fcpx_resolve.py B-3 ACTIVATION (sections 1–5)
```text
CHAIRMAN CONFIRMATION — fcpx_resolve.py B-3 ACTIVATION
The prior ruling contained a SHA-256 transcription error.
The exact producer identity authorized for activation is:
faacec8bd67b9be70cda79014953127cffeffd6e134da035d1bfe296ba866038
Use the exact 64-character value above.
Do not use or preserve the malformed 65-character value from the prior instruction.
1. Runtime identity binding
Bind this activation to both:
- the exact qualified fcpx_resolve.py SHA-256 above; and
- the exact Python interpreter identity recorded in the committed Wave-1 qualification evidence.
Source the interpreter's full path, implementation/version, architecture, and full binary SHA-256 directly from the committed qualification evidence. Do not manually reconstruct or abbreviate its hash from this instruction.
Rationale: for fcpx_resolve.py, the interpreter is the applicable runtime toolchain. The qualification established behavior under that exact interpreter identity.
Any future change to either:
- producer SHA-256; or
- qualified interpreter binary identity
invalidates this activation until the successor combination is requalified and separately activated.
A path remaining /usr/bin/python3 is not sufficient if the binary behind that path changes.
2. Activation mechanism
Use the established EO-2026-09-29 addendum mechanism identified in the read-only check.
Prepare:
docs/rulings/EO-2026-09-29_ADDENDUM_E_B3_fcpx_resolve_Activation.md
Addendum E should record:
- producer: fcpx_resolve.py;
- exact producer SHA-256;
- producer repository path;
- ECR-GEN-003 commit:
  e0a346a16abf77db4a6abe5d59a2b31dadcf4464;
- Wave-1 qualification-evidence commit:
  1def9eae522111d1604e37e02d64ee7d9f509da2;
- exact qualified interpreter identity from that evidence;
- qualification disposition: PASS;
- permitted B-3 measurement/validation scope;
- prohibited actions;
- identity-invalidation rule described above.
3. Effective scope
This exact producer/runtime identity becomes effective under B-3 only for its approved scope:
- parsing and validating supplied FCPXML and ETC inputs;
- producing its declared resolved-timeline/census output;
- enforcing its existing validation and STOP conditions;
- emitting its approved deterministic provenance sidecar;
- factual measurement and validation only.
It does not receive authority to:
- adjudicate editorial meaning;
- assign beats, segments, or episodes;
- alter registries;
- change source designations;
- infer narrative intent;
- perform unrelated observation classifications;
- invoke other producers;
- release regeneration holds.
4. Partial Decision-B effectiveness
Record explicitly that producer authority is per-producer.
After this ruling:
- fcpx_resolve.py = ACTIVE/EFFECTIVE under B-3 for the exact bound identity;
- derive_camera_runs.py = technically qualified but INACTIVE, pending semantic reconciliation;
- all other Decision-B producers remain inactive/pending;
- Decision B as a complete producer package remains incomplete.
Do not invent a new package-level status token if none exists; state the condition in the ruling text.
5. Preserve the camera-runs mismatch
Addendum E may note, but must not resolve:
- Decision-B wording: unknown camera families → UNCERTAIN;
- qualified derive_camera_runs.py behavior: unmatched elements → COMPOUND.
Do not modify that producer or its designation.
```

## SCOPE
No producer code, registry, Decision A or Decision C artifact is changed by this addendum.
No producer is run. No observation artifact is created. D2 remains HELD. Both regeneration
holds (v1.14.0, v1.15.0) remain HELD. S19, PBC-3 and PDR-2026-08-22-ESS-001 are not resolved.
