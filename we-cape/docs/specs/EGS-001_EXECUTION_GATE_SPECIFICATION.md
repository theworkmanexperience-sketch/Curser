# EGS-001 v0.2 — Execution Gate Specification

## Governance Status

Document Type: Specification (named-series) · Status: **DRAFT v0.2 — NOT RATIFIED** · Date: 2026-08-30
Authority: EXECUTIVE ORDER EGS-001 (2026-08-30) · refined under EXECUTIVE ORDER EGS-001A (2026-08-30)
Chairman countersignature: ☐ pending
Custody: `MACHINE` · **Authority: NONE** · **Implementation: NONE**
Numbering: named-series per `docs/README`, alongside `WET-SPEC-GATE-001` and `WET-SPEC-REPORT-001`.
Supersedes: **EGS-001 v0.1** (draft, never ratified). **Extends** `WET-SPEC-GATE-001`. Honours `WET-REV-002`.
Companion: `ARTIFACT_LIFECYCLE_SPECIFICATION.md` v0.2
Readiness: `EGS-001A_RATIFICATION_READINESS_REVIEW.md`

> **Normative in language, non-operative in force.** This document says what an implementation SHALL do. It does not authorize one. `G-12`, the generators, the guards and every registry are untouched.

**Changes from v0.1:** §1A Definitions (new) · §1B Specification Stability (new) · §1C Status Domains (new) · §4A Version Independence (new) · §5.3 the namespace/status materialization clause (**resolves a contradiction in v0.1**) · §7.1 Uniqueness (new, **and it departs from the Order — see §7.1.1**).

---

# 0 · The rule this standard was written to obey

> **`WET-REV-002`:** *"PDR approvals join the existing gate ledger, **never a parallel system**."*

The platform already has a gate ledger — `WET-SPEC-GATE-001`, with `gate_class: EXECUTION_GATE`, two gate kinds, additive composition, computed aggregates and a staleness rule.

**A Gate A / Gate B mechanism invented beside it would be precisely the parallel system `WET-REV-002` forbids.** This specification therefore creates **no new gate kind and no second ledger.** It does two things instead:

1. defines **execution class** as a property of a *run and its outputs* — which the ledger does not express, and which is not a gate;
2. defines **promotion** as an entry in a **register**, on the pattern `APPROVED_VIEWING_MASTER` already establishes — not as a gate per artifact.

**The second decision is load-bearing.** `WET-SPEC-GATE-001 §7` names gate proliferation as a real risk and rules that *"a gate needs a blocking item to exist."* A gate per promoted artifact would produce dozens carrying no blocking item. **The register is the correct precedent and the platform is already using it.**

---

# 1 · Scope

Governs the **execution class** of a run, the **status** of the artifacts a run emits, the **namespace** those artifacts occupy, and the **promotion** act that changes an artifact's status.

**Out of scope, stated so it is never argued:**

- **What any run should compute.** This standard says how a run is *classified*, never what it should *produce*.
- **Whether any particular artifact should be promoted.** An Executive act on a case, not a rule.
- **The resolution of `CF-001`** and the authoritative caption stream. Untouched.
- **Versioning mechanism.** §4A defines the *model* only; how versions are assigned, ordered or stored is out of scope.
- **Storage, file formats, tooling, implementation.** Requirements only.

---

# 1A · Definitions (normative)

**Terms are defined once and used consistently. Where the repository already uses a term, the definition below is a restatement, not a redefinition — §1B.3.**

| term | definition |
|---|---|
| **Artifact** | A file produced by a run, or admitted to the repository from outside it, whose identity is its `sha256`. **Not its path, not its filename.** |
| **Run** | A single bounded execution of platform code that may emit artifacts. A run has one `execution_class`, declared before it begins. |
| **Execution Class** | The declared standing of a run: `EXPERIMENTAL` or `CANONICAL`. Declared, never inferred. Determines the namespace the run may write to. |
| **Namespace** | The write destination permitted to a run of a given execution class. A **physical** property of where bytes are placed — distinct from status, which is logical. See §5.3. |
| **Promotion** | The governance act by which an artifact's status becomes `CANONICAL`. Effected by a conforming Promotion Register entry and by nothing else. |
| **Custody** | Who held an artifact. `MACHINE`, `HUMAN` or `EXECUTIVE`. **Custody is immutable and is never authority** — `ER-003`. |
| **Authority** | Who may decide about an artifact. `NONE` for every run of every class; the promoting instrument for a canonical artifact. |
| **Canonical** | The status of an artifact that is the authoritative artifact of its kind for its production. Conferred only by promotion; **never by location, filename, age, run success, or absence of objection.** |
| **Experimental** | The status of an artifact produced by a run of execution class `EXPERIMENTAL`. Not governed, and never was. **Carries no implication about quality or correctness.** |
| **Reference Only** | The status of an artifact present in the repository that was **never canonical and not produced by a governed run.** Retained under quarantine so it cannot be used by accident. |
| **Supersession** | The replacement of a canonical artifact by a later promotion. Effected **by promotion of the successor**, never by mutation, deletion or edit of the incumbent. |

---

# 1B · Specification stability (normative)

**This clause exists so that ratification means something durable.** A specification whose terms can be reinterpreted later has ratified nothing.

## 1B.1 · What a future revision MAY do

- **extend** — add states, fields, invariants or requirements that no conforming implementation would have violated;
- **clarify** — restate existing meaning in plainer or more precise language;
- **add compatible states** — new values that do not alter the meaning of existing ones;
- **tighten** — narrow a permission, provided the narrowing is stated as a change and dated.

## 1B.2 · What a future revision SHALL NOT do

- **SHALL NOT reinterpret the meaning of a previously ratified state.** If `CANONICAL` is ratified with the meaning in §1A, no later revision may give it a different one. **A meaning that needs to change requires a new state name and an explicit supersession of the old.**
- **SHALL NOT silently redefine an execution class.** Any change to what `EXPERIMENTAL` or `CANONICAL` means SHALL be stated as a change, dated, and accompanied by the disposition of every artifact classified under the prior meaning.
- **SHALL NOT reclassify existing artifacts by revision.** A specification change does not change what an artifact is. Reclassification is a governance act on a case, recorded per artifact.
- **SHALL NOT weaken an invariant without stating the weakening.** An invariant removed or relaxed SHALL be named, with the reason and the date.

## 1B.3 · Terms already in use

Where this specification defines a term the repository already uses, **the definition is a restatement of existing practice and SHALL NOT be read as changing it.** Where a definition would change existing practice, that is a defect in this specification, not a change to the practice, and SHALL be corrected here.

**This clause is why §4 of the companion maps existing states rather than renaming them.**

## 1B.4 · The prior draft

**v0.1 is superseded and was never ratified.** No artifact, run or record was ever classified under it. **This revision therefore reinterprets nothing** — §1B.2 binds from ratification forward.

---

# 1C · Status domains — four, not one (normative)

**The Order directs that artifact status and governance document status be separated. The repository has four such domains, and conflating any two of them produces a false statement.**

| domain | answers | values | applies to |
|---|---|---|---|
| **ARTIFACT STATUS** | *what is this artifact?* | `EXPERIMENTAL` · `PROMOTION_PENDING` · `CANONICAL` · `SUPERSEDED` · `REFERENCE_ONLY` · `ARCHIVED` | files produced by runs, and files admitted from outside |
| **GOVERNANCE DOCUMENT STATUS** | *what standing does this instrument have?* | `DRAFT` · `RATIFIED` · `ACCEPTED` · `SUPERSEDED` · `RETIRED` | specifications, PDRs, ADRs, Orders, reviews |
| **LINEAGE STATUS** | *what standing does this production lineage have?* | `PRODUCTION` · `SUPERSEDED_ASSEMBLY` | lineages |
| **WORKFLOW STATUS** | *how far has the work reached?* | `AWAITING_INGESTION` · `PREPARED_NOT_EXECUTED` · … | workspaces and processes |

## 1C.1 · They are independent domains

**SHALL:** an implementation SHALL carry these as **separate fields** and SHALL NOT derive one from another.

**The word `SUPERSEDED` appears in three of the four and means something different in each.** A superseded *specification* has been replaced by a later specification. A superseded *artifact* has been displaced by a later promotion. A superseded *lineage* is no longer the governed production. **These are not the same fact and an implementation that stores them in one field will eventually assert one while meaning another.**

## 1C.2 · The combinations are real

**A canonical artifact of a superseded lineage is a coherent object, and the repository holds one right now.** The Approved Viewing Master carries `approval_status: APPROVED` while its lineage is `SUPERSEDED_ASSEMBLY` — and the register raises that itself rather than resolving it. **Any model that collapses the two axes would have to call that artifact either canonical or superseded, and both would be false.**

**This document is `DRAFT` in the governance domain and confers no artifact status on anything.**

---

# 2 · The two gates — one question each

| | question answered | custody | authority | governed by |
|---|---|---|---|---|
| **Gate A** | *May this code execute?* | `MACHINE` | **NONE** | the standing execution authority |
| **Gate B** | *May this output become a governed artifact?* | `EXECUTIVE` | **DECIDES** | a Promotion Register entry (§7) |

**Precedence, stated once.** Gate A **never** confers Gate B. A Gate-A run that completes successfully, passes every guard, and produces bytes identical to a canonical artifact has produced **nothing governed.** Passing Gate A is not evidence for Gate B and SHALL NOT be cited as such.

**This is `ER-003` applied to execution: custody is not authority.**

---

# 3 · Gate A — the runtime model (normative)

## 3.1 · Execution state

Every run SHALL declare its execution class **before execution**, in the context, as machine-readable data:

```
execution_class:  EXPERIMENTAL | CANONICAL
```

A run whose `execution_class` is **absent, unrecognised, or inconsistent with any other declared field SHALL fail shut** — non-zero exit, **zero files written**.

**The class SHALL be declared, never inferred.** An implementation SHALL NOT default it, derive it from a path, infer it from a caller, or assign it after the fact. **An undeclared class is a stop, not a default.**

## 3.2 · Custody and authority

| field | Gate A value | normative |
|---|---|---|
| `custody` | `MACHINE` | SHALL |
| `authority` | `NONE` | SHALL |
| `status` | `EXPERIMENTAL` | SHALL — on every artifact emitted |

## 3.3 · Lifecycle of a Gate-A run

```
context declares execution_class: EXPERIMENTAL
        ↓
all existing guards, unchanged, PLUS the destination guard §6.3
        ↓                              ↘  any failure → non-zero exit, 0 files
outputs written to the experimental namespace ONLY
        ↓
every artifact carries  status EXPERIMENTAL · custody MACHINE · authority NONE
        ↓
the run ends. Nothing is promoted. Nothing is governed.
```

**A Gate-A run has no successful terminal state that produces a governed artifact.**

## 3.4 · Permitted outputs

Any artifact the platform can generate, **provided every one carries the §3.2 fields and lands in the experimental namespace.**

**Gate A exists so the platform can rehearse.** Under it the ETC extractor may be pointed at an unratified lineage, the generator exercised against real inputs, a validator run against live registries — **none of which becomes governed by having been run.**

## 3.5 · Prohibited outputs

A Gate-A run SHALL NOT:

1. write to the canonical namespace, by any path, including one supplied by a caller;
2. emit an artifact without the §3.2 fields, or with `status` other than `EXPERIMENTAL`;
3. modify, overwrite, delete or rename any existing canonical artifact;
4. write to any registry, of any kind;
5. create, alter or close a gate file as defined by `WET-SPEC-GATE-001`;
6. write a Promotion Register entry — **promotion is not a runtime act**;
7. assert, in any emitted text, that its output is governed, canonical, approved or authoritative.

**Prohibition 7 is not decorative.** The current generator template writes `Sprint: … governed production run` into every artifact header, and a Gate-A run would reproduce it verbatim. **An implementation SHALL replace that phrase with the computed `status` field.**

## 3.6 · How a Gate-A run differs from a governed production run

| property | Gate A | governed production run |
|---|---|---|
| `execution_class` | `EXPERIMENTAL` | `CANONICAL` |
| artifact `status` | `EXPERIMENTAL` | `CANONICAL` **after promotion** — §5.3 |
| artifact `custody` | `MACHINE` | `MACHINE` — *unchanged; custody is immutable* |
| artifact `authority` | `NONE` | **the promoting instrument** |
| destination | experimental namespace only | canonical namespace |
| may overwrite canonical | **never** | only by regeneration under authority |
| may write registries | **never** | only by authority |
| standing after success | **nothing is governed** | **nothing is governed until promoted** |
| `RUN_ID`, `git_commit`, input hashes | present, identical in form | present |

**Two rows deserve attention.**

`custody` does not change. Custody records who held the artifact and is immutable. **Gate A does not change custody; it changes nothing about the facts. What it adds is the *declaration* of something that was always true and never written down — that a run holds no authority.**

**And `status` is `CANONICAL` only after promotion, in both columns.** A `CANONICAL`-class run produces a *candidate*. **Execution class is a permission to write to a namespace; it is not a grant of status.** v0.1 blurred this and v0.2 does not.

---

# 4 · Gate B — the promotion model (normative)

## 4.1 · Promotion is an explicit governance event

Promotion SHALL be **explicit** — never implied by location, filename, age, success or absence of objection; **recorded** — the register entry *is* the promotion; **executive**; and **per-artifact** — never a blanket promotion of a run's whole output.

> **`APPROVED_VIEWING_MASTER` states the principle already, and this specification adopts it verbatim: *"A render absent from this register is NOT approved. Silence is not approval."***

## 4.2 · Required inputs

| input | requirement |
|---|---|
| the artifact | identified by `sha256`, **not by path or filename** |
| the producing run | `RUN_ID`, `git_commit`, `execution_class` |
| the input chain | every input hash the run consumed |
| the target status | `CANONICAL`, and what it supersedes if anything |

**Identification SHALL be by hash.** `CF-001` is what informal identification produces, and the `APPROVED_VIEWING_MASTER` hazard entry records two files *"distinguishable only by directory, size, runtime and hash"* with **identical filenames**.

## 4.3 · Required approvals

| act | competent authority |
|---|---|
| promote to `CANONICAL` | Executive |
| supersede a `CANONICAL` artifact | Executive |
| record `REFERENCE_ONLY` quarantine | Executive — precedent: Order 2026-08-26 §2 |
| any status change effected by a run | **none — runs do not change status** |

## 4.4 · Required lineage

The entry SHALL record lineage such that **the artifact can be regenerated from its declared inputs.** Where it cannot, **the entry SHALL say so explicitly** and the promotion SHALL be marked as resting on an unreproducible artifact.

**This clause exists because the repository has three recorded instances of exactly that condition** — a published figure with no producing computation, a first-class artifact class with no committed producer, and ninety-one citations resting on an unregistered file. **A register that could not express "this cannot be regenerated" would have recorded all three as sound.**

## 4.5 · Required evidence

| claim | evidence |
|---|---|
| the artifact is what it says | `sha256`, computed at promotion |
| it came from the declared run | `RUN_ID` and inputs as carried in the artifact |
| it conforms to its governing contract | the conformance result, by name and verdict |
| it supersedes a prior artifact | that artifact's `sha256` |

**Percentages SHALL carry numerator, denominator and source, and no composite readiness, health, quality or maturity score SHALL be recorded** — `WET-SPEC-REPORT-001`, unweakened.

## 4.6 · What promotion does not do

Promotion **does not** re-run, re-verify, re-derive or re-measure. **It records a decision about an artifact that already exists.** Promotion SHALL NOT be coupled to regeneration; `DOC-002` governs regeneration and is untouched. **Materialization is a separate question and is answered in §5.3.**

---

# 4A · Version independence (normative)

**Model only. No versioning mechanism is designed and none is authorized.**

## 4A.1 · Three independent properties

```
IDENTITY   what an artifact IS          its sha256. Immutable. Two bytes differ → different artifact
VERSION    which iteration it is        an ordering label within an artifact kind
STATUS     what standing it has         §1C ARTIFACT STATUS
```

**SHALL:** these are three fields. An implementation SHALL NOT derive any from another.

## 4A.2 · Consequences

- **Many versions may exist simultaneously.** Existence is not standing.
- **Many versions may hold `EXPERIMENTAL` at once.** That is the normal state of rehearsal.
- **At most one version may hold `CANONICAL` at a time**, per artifact kind per production — §7.1.
- **A version is not superseded by being older.** Supersession is an act (§1A), not a consequence of ordering. **An artifact is `SUPERSEDED` when a successor is promoted, and not before.**
- **Identity does not change with status.** The same `sha256` may be `EXPERIMENTAL` today and `CANONICAL` tomorrow. **Promotion changes standing, not bytes.**

## 4A.3 · What version is not

**Version SHALL NOT be used as evidence of standing.** *"v1.2 is newer than v1.1"* establishes ordering and nothing else. **The register is the only source of standing.**

---

# 5 · Namespace model (normative)

## 5.1 · Two namespaces, one boundary

| namespace | receives writes from | holds |
|---|---|---|
| **canonical** | runs declaring `execution_class: CANONICAL` | canonical candidates, canonical and superseded artifacts |
| **experimental** | runs declaring `execution_class: EXPERIMENTAL` | experimental artifacts |

**Namespace is physical — where bytes are written. Status is logical — what the register says. §5.3 governs their relationship.**

## 5.2 · Required invariants

**`N-1` · Namespace and status SHALL agree, and disagreement SHALL be enumerable.** See §5.3 for the one permitted disagreement and how it is recorded.

**`N-2` · Namespace SHALL be a function of `execution_class`, decided once.** An implementation SHALL NOT accept a destination and a class as independent inputs. **Two independent flags reproduce the failure this standard exists to prevent** — one will eventually be wrong and nothing will notice.

**`N-3` · Crossing the status boundary SHALL be a promotion, not a copy.** Promotion records a decision; it does not by itself relocate bytes.

**`N-4` · The canonical namespace SHALL be closed by default.** Any write to it from a run not declared `CANONICAL` SHALL fail shut before the first byte.

**`N-5` · Filenames SHALL NOT be relied on to distinguish namespaces.** `WET-SPEC-GATE-001 §4` established the principle for gates — *"filenames drift, get copied, get renamed"* — and this repository has two recorded look-alike incidents that prove it for artifacts.

## 5.3 · Materialization — resolving a contradiction in v0.1

> **v0.1 contained a contradiction and this clause resolves it.** `N-1` required namespace and status to agree; `N-3` forbade moving an artifact into the canonical namespace; §4.6 forbade coupling promotion to regeneration. **Those three cannot all hold for an experimental artifact that is promoted.** v0.1 deferred this as "an implementation question." It is not — it is a specification question, and leaving it open would have produced canonical artifacts sitting in the experimental namespace with nothing recording why.

**A promotion SHALL declare how the artifact is materialized:**

| `materialization` | meaning | when |
|---|---|---|
| `REGENERATED` | a `CANONICAL`-class run reproduced the artifact into the canonical namespace from the same declared inputs. **`N-1` holds without exception.** | the **default**, and the only form consistent with `DOC-002` |
| `IN_PLACE` | the artifact is promoted where it lies. **`N-1` is knowingly and visibly violated for this artifact.** | permitted **only** where regeneration is impossible — a `REFERENCE_ONLY` artifact with no producing run, or an artifact whose producer does not exist |

**SHALL:** where `materialization: IN_PLACE`, the entry SHALL record `reproducible: NO` or `UNKNOWN` with a reason (§4.4), and the artifact SHALL be reported by enumeration (§6.5) as a standing `N-1` exception **for as long as it holds canonical status.**

**`IN_PLACE` is not a convenience. It is a declared, visible, permanent exception**, and it exists because the repository already holds artifacts that could never be regenerated — which is a fact about the past, not a licence for the future.

---

# 6 · Runtime requirements (normative)

**Requirements only. No implementation is authorized.**

## 6.1 · `R-1` — machine-readable status field

Every emitted artifact SHALL carry, **as structured data rather than as a comment**:

```
status      EXPERIMENTAL | CANONICAL | SUPERSEDED | REFERENCE_ONLY | ARCHIVED
custody     MACHINE
authority   NONE | <promoting instrument>
run_id      <the producing run>
```

**The value SHALL be computed from the declared `execution_class`, never written into a template.** The existing free-text `governed production run` string SHALL be removed — **a template phrase cannot distinguish the runs it is copied into.**

## 6.2 · `R-2` — coupled regeneration mode

`G-12` currently admits exactly one value and fails shut on every other, which makes an honest `EXPERIMENTAL` declaration unrunnable. An implementation SHALL extend the admissible set such that:

```
execution_class CANONICAL     → mode CANONICAL_EDITORIAL_TIMELINE → canonical namespace
execution_class EXPERIMENTAL  → mode EXPERIMENTAL                 → experimental namespace
anything else                 → fail shut, unchanged
```

**`G-12`'s existing `ERO-001 §2` assertions SHALL continue to apply unchanged to `CANONICAL` runs.** Nothing here relaxes a canonical run's obligations. **Mode and namespace SHALL be one decision (`N-2`), not two.**

## 6.3 · `R-3` — destination guard

A guard SHALL assert, **before the first write**, that the resolved output destination is permitted for the declared `execution_class`, and SHALL fail shut with a named stop reason otherwise — non-zero exit, **zero files written.**

## 6.4 · `R-4` — promotion record

The Promotion Register SHALL be **discoverable by marker rather than by filename** (`WET-SPEC-GATE-001 §4`), and its aggregate state SHALL be **computed, never authored** (`§5`).

## 6.5 · `R-5` — enumeration and staleness

Enumeration SHALL answer, without human reading:

- every artifact and its status;
- every `N-1` violation **that is not a declared `IN_PLACE` exception**, and separately every declared exception;
- every canonical artifact whose declared inputs no longer hash as declared;
- every promotion entry citing a run that cannot be found;
- **every artifact kind and production holding more than one active `CANONICAL` promotion** (§7.1).

**The third is the `T11` detector this repository has needed since a committed artifact was found matching neither its generator nor its successor.**

---

# 7 · The Promotion Register — governance record schema (normative)

**A register, not a gate. Schema only — storage, format and tooling are out of scope.**

| field | requirement | meaning |
|---|---|---|
| `register_class: PROMOTION_REGISTER` | SHALL | the discovery marker (`R-4`) |
| `schema_version` | SHALL | the version of this standard the entry conforms to |
| `entry_id` | SHALL | stable, unique, **never reused** |
| `artifact_sha256` | SHALL | **the identity. Not the path, not the filename** |
| `artifact_path_at_promotion` | SHALL | recorded as *observed*, **explicitly non-authoritative** |
| `artifact_kind` | SHALL | the kind for uniqueness (§7.1) |
| `production` | SHALL | the production for uniqueness (§7.1) |
| `artifact_version` | SHOULD | ordering label; **not evidence of standing** (§4A.3) |
| `from_status` | SHALL | `EXPERIMENTAL` \| `REFERENCE_ONLY` |
| `to_status` | SHALL | `CANONICAL` |
| `materialization` | SHALL | `REGENERATED` \| `IN_PLACE` — §5.3 |
| `producing_run.run_id` | SHALL | |
| `producing_run.git_commit` | SHALL | |
| `producing_run.execution_class` | SHALL | the class the run declared |
| `input_hashes[]` | SHALL | every input the run consumed |
| `reproducible` | SHALL | `YES` \| `NO` \| `UNKNOWN` — §4.4 |
| `reproducibility_note` | SHALL, when not `YES` | why it cannot be regenerated |
| `conformance[]` | SHALL | each check by name and verdict; **an empty list is a declaration that none was run** |
| `supersedes_sha256` | SHALL, when superseding | the artifact displaced |
| `active` | SHALL | computed, not authored — §7.1 |
| `authority` | SHALL | the instrument effecting the promotion |
| `promoted_by` | SHALL | the competent authority |
| `promoted_date` | SHALL | ISO date |
| `status_history[]` | SHALL | **append-only**; every change with date, authority, note |

## 7.1 · Uniqueness (normative)

**`U-1` · For a given `artifact_kind` and `production`, at most ONE promotion entry SHALL be active with `to_status: CANONICAL` at any time.**

**`U-2` · Supersession SHALL occur by promotion of the successor, never by mutation of the incumbent.** Promoting a successor sets the incumbent's `active` to false **as a computed consequence**, and appends to both entries' `status_history`. **No entry is edited to effect it.**

**`U-3` · `active` SHALL be computed, never authored** — `WET-SPEC-GATE-001 §5`: *"a summary someone has to remember to update is a summary that will eventually lie."*

**`U-4` · More than one active canonical promotion for a kind-and-production pair is a defect, SHALL be enumerable (§6.5), and SHALL be reported rather than silently resolved.**

### 7.1.1 · A departure from the Order, stated openly

**EGS-001A Objective 5 specifies uniqueness over the tuple `(artifact kind, production, version)`. This specification uses `(artifact kind, production)` and omits version. The departure is deliberate and is recorded here rather than made quietly.**

**Including `version` in the uniqueness key would permit one active canonical promotion *per version* — that is, many simultaneously.** That contradicts Objective 4 of the same Order, which states that *"only one version may hold canonical status at a time,"* and it contradicts the precedent the register is built on: `APPROVED_VIEWING_MASTER` — *"EXACTLY ONE entry per production may carry status: APPROVED."*

**Version is what distinguishes the candidates. It cannot also be what scopes the uniqueness, or uniqueness does no work.**

**This is a recommendation, not a determination.** If the Executive intends per-version canonicity — several versions canonical at once, distinguished by version — then `U-1` should be restored to the Order's tuple and §4A.2 amended to match. **The two cannot both stand, and this specification chose the reading consistent with Objective 4 and with existing practice.**

## 7.2 · Failing shut

**An entry missing any SHALL field is non-conforming, and the artifact it describes SHALL be treated as NOT PROMOTED.** `WET-SPEC-GATE-001 §3` establishes this posture: **failing shut is the only safe default for a control artifact.**

## 7.3 · Silence

**An artifact absent from the register is not canonical.** No inference of promotion SHALL be drawn from a path, a filename, a date, a successful run, or the absence of an objection.

## 7.4 · Immutability

Entries SHALL be **append-only.** A promotion is not edited; it is superseded by a later entry citing it. **`DOC-002` applied to the record of promotion.**

---

# 8 · Conformance

An implementation conforms when:

1. every run declares `execution_class` before execution and fails shut without it (§3.1);
2. every emitted artifact carries `status`, `custody`, `authority`, `run_id` as structured data (§6.1);
3. namespace is a function of `execution_class`, decided once (`N-2`);
4. a destination guard fails shut before the first write (§6.3);
5. no run of any class writes a Promotion Register entry (§3.5.6) or changes any status (§4.3);
6. the register is discoverable by marker and its aggregate computed (§6.4, `U-3`);
7. enumeration answers all five questions in §6.5;
8. namespace and status agree except where a declared `IN_PLACE` exception is recorded (`N-1`, §5.3);
9. at most one active canonical promotion exists per artifact kind per production (`U-1`);
10. artifact status, governance document status, lineage status and workflow status are separate fields (§1C.1).

**Nothing here is in force until ratified, and ratification authorizes a specification, not an implementation.**

---

# 9 · What this specification does not do

- **It does not implement either gate.** No runtime component, guard, generator, context or registry is modified.
- **It does not modify `G-12`.** §6.2 states a requirement on a future implementation.
- **It does not resolve `CF-001` or choose an authoritative caption stream.**
- **It does not create a new gate kind or a second ledger** — §0.
- **It does not instantiate a Promotion Register.** §7 defines a schema; nothing creates the register.
- **It does not design a versioning mechanism.** §4A is a model.
- **It does not reclassify any artifact** — §1B.2.
- **It does not authorize the runtime requirements.** They await an implementation order.

---

```
EGS-001                     DRAFT v0.2 — NOT RATIFIED
Supersedes                  v0.1 draft, never ratified, never applied to any artifact
Gate kinds created          NONE — WET-REV-002 honoured
Registers created           NONE — schema defined, register not instantiated
Contradictions resolved     2 — v0.1 namespace/status (§5.3) · Order tuple (§7.1.1)
Runtime modified            NONE   ·   G-12 modified   NONE
Generators modified         NONE   ·   Registries      NONE
Artifacts reclassified      NONE
CF-001                      UNRESOLVED   ·   Authoritative stream   NOT CHOSEN
Implementation authorized   NONE   ·   Commits   NONE
```

---

*Prepared under EXECUTIVE ORDERS EGS-001 and EGS-001A. Custody: MACHINE. Authority: NONE. Normative in language, non-operative in force. Ratification would authorize a specification, not an implementation.*
