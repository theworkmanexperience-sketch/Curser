# ARTIFACT LIFECYCLE SPECIFICATION v0.2

## Governance Status

Document Type: Specification (named-series, companion) · Status: **DRAFT v0.2 — NOT RATIFIED** · Date: 2026-08-30
Authority: EXECUTIVE ORDER EGS-001 §3 · refined under EXECUTIVE ORDER EGS-001A
Chairman countersignature: ☐ pending
Custody: `MACHINE` · **Authority: NONE** · **Implementation: NONE**
Parent: `EGS-001_EXECUTION_GATE_SPECIFICATION.md` v0.2
Supersedes: **v0.1** (draft, never ratified). **Formalises** states the repository already uses informally.

> **Normative in language, non-operative in force.** No artifact was reclassified, relabelled, moved or deleted.

**Changes from v0.1:** §1.5 version independence (new) · §3 invariants extended for version and domain separation · §4 the four-domain mapping (was three) · §5 stability inherited from `EGS-001 §1B` · §2.4 materialization aligned to `EGS-001 §5.3`.

---

# 0 · What this specification is doing

**Most of these states already exist in the repository. None of them is defined anywhere.**

`SUPERSEDED_ASSEMBLY`, `REFERENCE_ONLY`, `APPROVED`, `AWAITING_INGESTION`, `PREPARED_NOT_EXECUTED`, *"archived at RE-001"* — the platform has been using a state model for months, expressed in prose, per-register, with no shared vocabulary and no defined transitions.

**This specification names the states, fixes the transitions, and says who may effect each one. It invents as little as possible.**

**Definitions are in `EGS-001 §1A` and are not repeated. Stability rules are in `EGS-001 §1B` and bind this document identically.**

---

# 1 · The state model

## 1.1 · The Order's proposed model, and one revision

The Order proposes:

```
GENERATED → EXPERIMENTAL → PROMOTION PENDING → CANONICAL → SUPERSEDED → ARCHIVED
```

**One revision is recommended, on evidence: `GENERATED` should not be a state.**

If `GENERATED` is distinct from `EXPERIMENTAL`, there is a window in which an artifact exists on disk and **has no status.** That window is the entire hazard this architecture exists to close, and it is the condition the repository has already met twice as unlabelled look-alike files.

**Under `EGS-001 §3.1` the execution class is declared *before* the run.** An artifact is therefore `EXPERIMENTAL` or a canonical candidate **at the instant of its first byte.** There is no moment at which it is merely generated.

`GENERATED` is retained as **an event, not a state** — recorded in `status_history`, never a value of `status`.

## 1.2 · The states (normative)

| state | meaning | authority to enter |
|---|---|---|
| **`EXPERIMENTAL`** | produced by a Gate-A run. Custody `MACHINE`, authority `NONE`. **Not governed, and never was.** Carries no implication about quality | a run declaring `execution_class: EXPERIMENTAL` |
| **`PROMOTION_PENDING`** | nominated for promotion; the register entry is open and incomplete | Executive |
| **`CANONICAL`** | governed. The authoritative artifact of its kind for its production | **Executive only**, via a conforming register entry |
| **`SUPERSEDED`** | was `CANONICAL`; displaced by a later promotion. **Retained, never deleted** | Executive, as a computed consequence of the successor's promotion |
| **`REFERENCE_ONLY`** | present in the repository, **never canonical and not from a governed run.** Retained under quarantine so it cannot be used by accident | Executive |
| **`ARCHIVED`** | terminal. Retained for the record; **not consumable by any run** | Executive |

## 1.3 · `REFERENCE_ONLY` — the state the proposed model omits

**The repository already holds artifacts in this state and they fit nowhere in the proposed chain.**

`APPROVED_VIEWING_MASTER` holds a render at `approval_status: REFERENCE_ONLY`, `hazard: HIGH`, quarantined by Executive Order 2026-08-26 §2. **It was never experimental — no governed run produced it. It was never canonical. It is not superseded, because it never held the position it would have been displaced from.**

**It entered the repository from outside the lifecycle.** A model that cannot express that will mislabel such artifacts or leave them unlabelled — **and unlabelled is how this one became a hazard.**

`REFERENCE_ONLY` is therefore **an entry point, not merely a transition.**

## 1.4 · The `status` field is not `approval_status`

`APPROVED_VIEWING_MASTER` uses `approval_status`, affirmed by Executive Order 2026-08-28 §2.2 as that register's canonical schema key — while `reference_status` was retained non-canonical *"so that the quarantine's authorizing language stays legible."*

**This specification SHALL NOT rename that key.** A conforming implementation SHALL treat `approval_status` there as the register-local expression of `status`. **Reconciling the two vocabularies is an Executive act.**

**Recorded because renaming a governed key to fit a new standard is exactly the silent reclassification the platform has already refused once, on the record.**

## 1.5 · Version independence (normative)

**Model only, per `EGS-001 §4A`. No versioning mechanism is designed.**

```
IDENTITY   sha256, immutable      two bytes differ → a different artifact
VERSION    an ordering label       within an artifact kind
STATUS     §1.2                    what standing it holds
```

**SHALL:** three separate fields; none derived from another.

- **Many versions may exist at once.** Existence is not standing.
- **Many versions may be `EXPERIMENTAL` at once.** That is the normal state of rehearsal.
- **At most one version may be `CANONICAL` at a time** per artifact kind per production — `EGS-001 §7.1 U-1`.
- **A version is not superseded by being older.** Supersession is an act, not a consequence of ordering. **An artifact is `SUPERSEDED` when a successor is promoted, and not before.**
- **Status change does not change identity.** The same `sha256` may be `EXPERIMENTAL` today and `CANONICAL` tomorrow — **promotion changes standing, not bytes.**

---

# 2 · Transitions (normative)

```
                  ┌──────────────────────────────────────────────┐
   Gate-A run ───►│  EXPERIMENTAL                                │
                  └───────┬──────────────────────────────┬───────┘
                          │ Executive nominates          │ Executive
                          ▼                              ▼
                  ┌───────────────────┐          ┌──────────────┐
                  │ PROMOTION_PENDING │          │  ARCHIVED    │
                  └───────┬───────┬───┘          └──────────────┘
        entry conforms    │       │  withdrawn / refused
                          ▼       └──────────► back to EXPERIMENTAL
                  ┌──────────────┐
   Gate-B ───────►│  CANONICAL   │◄──── promotion from REFERENCE_ONLY (Executive, §2.2)
                  └───────┬──────┘
                          │ a successor is promoted in its place
                          ▼
                  ┌──────────────┐          ┌──────────────┐
                  │  SUPERSEDED  │────────► │   ARCHIVED   │
                  └──────────────┘          └──────────────┘

   outside the lifecycle ──► REFERENCE_ONLY ──► ARCHIVED
                                    │
                                    └────────► CANONICAL (Executive, §2.2)
```

## 2.1 · Permitted transitions

| from | to | who | condition |
|---|---|---|---|
| *(none)* | `EXPERIMENTAL` | a run | `execution_class: EXPERIMENTAL` declared before execution |
| *(none)* | `REFERENCE_ONLY` | Executive | an artifact present without a governed producing run |
| `EXPERIMENTAL` | `PROMOTION_PENDING` | Executive | nomination |
| `PROMOTION_PENDING` | `CANONICAL` | Executive | a **conforming** register entry — `EGS-001 §7` |
| `PROMOTION_PENDING` | `EXPERIMENTAL` | Executive | nomination withdrawn or refused |
| `REFERENCE_ONLY` | `CANONICAL` | Executive | §2.2 |
| `CANONICAL` | `SUPERSEDED` | Executive | **computed** when a successor is promoted — `U-2` |
| any | `ARCHIVED` | Executive | terminal retention |

## 2.2 · `REFERENCE_ONLY → CANONICAL` requires evidence of identity

**This transition SHALL require evidence of identity, not merely a determination.** An artifact in `REFERENCE_ONLY` has, by definition, no governed producing run — so nothing establishes what it is.

The live case is exact. `APPROVED_VIEWING_MASTER` records of its quarantined render:

> *"Runtime matches the 2026-08-24 divergent-cut FCPXML to the millisecond. **Whether this render was produced from that FCPXML is NOT asserted — equality of duration is not identity of source, and no comparison of this file's picture against that timeline has been performed.**"*

**A promotion recorded on duration equality alone would be a promotion on coincidence.** `EGS-001 §4.4` requires `reproducible: NO` with a reason, and this transition is why that field exists.

## 2.3 · Prohibited transitions

**`P-1` · No run of any class SHALL change any artifact's status.** Runs create artifacts in a declared state. **Status changes are governance events without exception.**

**`P-2` · `EXPERIMENTAL → CANONICAL` SHALL NOT occur directly.** It passes through `PROMOTION_PENDING`, so a nomination exists as a record even where promotion is refused. **A refused promotion is evidence and SHALL be retained.**

**`P-3` · `SUPERSEDED → CANONICAL` SHALL NOT occur.** A superseded artifact is not reinstated; a new promotion of the same bytes is a **new entry** citing the same `sha256`. `DOC-002` applied to status.

**`P-4` · `ARCHIVED` is terminal.** No transition leaves it.

**`P-5` · No artifact SHALL be deleted to effect a state change.** `SUPERSEDED`, `REFERENCE_ONLY` and `ARCHIVED` all mean *retained*. The repository's practice is already this — *"retained, not deleted; marked; do not edit."*

## 2.4 · Materialization at promotion

A transition to `CANONICAL` SHALL declare `materialization` per `EGS-001 §5.3`:

- **`REGENERATED`** — the default, and the only form consistent with `DOC-002`;
- **`IN_PLACE`** — permitted only where regeneration is impossible, recorded as a **standing, enumerable exception** for as long as the artifact holds canonical status.

**`IN_PLACE` is the honest disposition for the `REFERENCE_ONLY → CANONICAL` path, because an artifact with no producing run cannot be regenerated by definition.**

---

# 3 · Required invariants

**`I-1` · Every artifact has exactly one status at any time.** None unlabelled, none carrying two.

**`I-2` · Status and namespace agree**, except a declared `IN_PLACE` exception, which SHALL be enumerable — `EGS-001 §5.3`, `§6.5`.

**`I-3` · At most one `CANONICAL` artifact per artifact kind per production**, regardless of how many versions exist — `EGS-001 §7.1 U-1`, §1.5. The pattern `APPROVED_VIEWING_MASTER` already enforces: *"EXACTLY ONE entry per production may carry status: APPROVED."*

**`I-4` · Status history is append-only.** Every transition records date, authority and note. **A status you cannot trace to a decision is not a governed status.**

**`I-5` · Absence is not a state.** An artifact with no status is **non-conforming and SHALL be treated as `REFERENCE_ONLY`** — the most restrictive state permitting retention. Failing shut, applied to classification.

**`I-6` · Status is carried by the artifact, not only by a register.** `EGS-001 §6.1`. A register alone means an artifact separated from its register — copied, moved, sent — carries no indication of what it is. **That is the look-alike hazard, and it has occurred twice.**

**`I-7` · Identity, version and status are three fields.** None derived from another — §1.5.

**`I-8` · Artifact status is never stored in the same field as governance document status, lineage status or workflow status** — §4.1.

---

# 4 · Reconciliation with states already in use

**Mapping, not renaming. Nothing is reclassified by this document** — `EGS-001 §1B.2`.

| existing expression | where | maps to | note |
|---|---|---|---|
| `approval_status: APPROVED` | `APPROVED_VIEWING_MASTER` | `CANONICAL` | register-local key retained — §1.4 |
| `approval_status: REFERENCE_ONLY` | same | `REFERENCE_ONLY` | direct |
| `08_22_assembly_lock_status: SUPERSEDED_ASSEMBLY` | `CUSTODY_ALERT_001` amendment | **LINEAGE STATUS** | **not an artifact status** — §4.1 |
| `lineage_status: PRODUCTION` | `AR2-0824.context.json` | **LINEAGE STATUS** | not an artifact status |
| `ingestion_status: AWAITING_INGESTION` | `INGESTION_MANIFEST` | **WORKFLOW STATUS** | not an artifact status |
| `state: PREPARED_NOT_EXECUTED` | `INGESTION_MANIFEST` | **WORKFLOW STATUS** | not an artifact status |
| *"archived at RE-001"* | `CONDUCTOR_SCORE.yaml` header | `ARCHIVED` | prose today; would become a field |
| `Status: RATIFIED` / `DRAFT` / `ACCEPTED` | governance documents | **GOVERNANCE DOCUMENT STATUS** | **§4.1 — a separate domain, not out of scope** |

## 4.1 · Four domains, and they SHALL NOT be conflated

**v0.1 separated three. The Order adds a fourth, and it was right to: governance document status is a distinct domain that v0.1 dismissed as merely "out of scope."**

```
ARTIFACT STATUS      what an artifact IS         EXPERIMENTAL · CANONICAL · SUPERSEDED …
GOVERNANCE STATUS    an instrument's standing    DRAFT · RATIFIED · ACCEPTED · SUPERSEDED · RETIRED
LINEAGE STATUS       a lineage's standing        PRODUCTION · SUPERSEDED_ASSEMBLY
WORKFLOW STATUS      how far work has reached    AWAITING_INGESTION · PREPARED_NOT_EXECUTED
```

**`SHALL`: four separate fields. An implementation SHALL NOT store any two in one field, and SHALL NOT derive one from another** (`I-8`).

**`SUPERSEDED` appears in three of the four and means something different in each.** A superseded *specification* was replaced by a later specification. A superseded *artifact* was displaced by a later promotion. A superseded *lineage* is no longer the governed production. **Three different facts, one word.**

**And the combinations are real, not theoretical.** The Approved Viewing Master is `APPROVED` in the artifact domain while its lineage is `SUPERSEDED_ASSEMBLY` — and **this specification is `DRAFT` in the governance domain while conferring no artifact status on anything at all.** An implementation that collapses these axes would have to call that render either canonical or superseded, and both would be false.

---

# 5 · Specification stability

**`EGS-001 §1B` binds this document identically and is not restated.** In particular: no future revision may reinterpret a ratified state's meaning, silently redefine a state, or reclassify existing artifacts by revision.

**v0.1 is superseded and was never ratified. No artifact, run or record was ever classified under it, so this revision reinterprets nothing.**

---

# 6 · Conformance

An implementation conforms when:

1. every artifact carries exactly one status, as structured data (`I-1`, `I-6`);
2. no run changes any artifact's status (`P-1`);
3. `EXPERIMENTAL → CANONICAL` passes through `PROMOTION_PENDING` (`P-2`);
4. status and namespace agree, or a declared `IN_PLACE` exception is enumerable (`I-2`);
5. status history is append-only with authority recorded (`I-4`);
6. an artifact without a status is treated as `REFERENCE_ONLY` (`I-5`);
7. the four status domains are separate fields (`I-8`, §4.1);
8. identity, version and status are separate fields (`I-7`);
9. at most one canonical artifact per kind per production, across all versions (`I-3`);
10. no state change is effected by deletion (`P-5`).

---

# 7 · What this specification does not do

- **It does not reclassify any existing artifact.** The §4 mapping is a reading, not a relabelling.
- **It does not rename `approval_status`** or any governed key — §1.4.
- **It does not create the Promotion Register.** `EGS-001 §7` defines a schema; neither document instantiates it.
- **It does not design a versioning mechanism** — §1.5 is a model.
- **It does not resolve `CF-001`, choose a caption stream, or touch `G-12`.**
- **It authorizes no implementation.**

---

```
ARTIFACT LIFECYCLE          DRAFT v0.2 — NOT RATIFIED
Supersedes                  v0.1 draft, never ratified, never applied
States defined              6, of which 5 already exist informally in the repository
Added to the Order's model  1 — REFERENCE_ONLY, an entry point
Removed from it             1 — GENERATED, demoted to an event
Status domains separated    4 — artifact · governance · lineage · workflow
Version model               identity · version · status, independent
Artifacts reclassified      NONE   ·   Governed keys renamed   NONE
Registries modified         NONE   ·   Implementation authorized   NONE
Commits                     NONE
```

---

*Prepared under EXECUTIVE ORDERS EGS-001 §3 and EGS-001A. Custody: MACHINE. Authority: NONE. No artifact was reclassified, relabelled, moved or deleted. No registry, runtime component or governed key was modified. Normative in language, non-operative in force.*
