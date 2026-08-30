# CAM-001 — IMPACT RESOLUTION

**Issued under:** EXECUTIVE CLARIFICATION ORDER ECO-001, Executive Producer / Chairman, 2026-08-30
**Subject:** EXECUTIVE DETERMINATION — *Canonical Authority Model* (designation pending, §4)
**Applies to:** `EGS-001_EXECUTION_GATE_SPECIFICATION.md` v0.2 · `ARTIFACT_LIFECYCLE_SPECIFICATION.md` v0.2
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. **No specification was edited.** No runtime component, guard, generator, registry or artifact was modified. No commit was made.
**Measured at:** repository HEAD `1552e42`

> **This document specifies exact wording changes. It does not make them.** Both v0.2 drafts stand unchanged and unedited.

---

# 0 · STATE AFTER THE CLARIFICATIONS

```
Open Executive questions        0 of 2 remaining — both answered by ECO-001
Contradictions with v0.2        NONE
Contradictions with ratified
  standards                     NONE — 8 checked, 3 reinforced
Live U-1 violations             NONE — verified, §2.2
Specification updates           8, exact wording at §3
Designation                     RECOMMENDED at §4 — not assigned
```

**Both drafts remain `DRAFT v0.2 — NOT RATIFIED`. Nothing in this document ratifies, amends or implements anything.**

---

# 1 · CLARIFICATION 2 — RESOLVED, AND IT CHANGES THE DETERMINATION, NOT THE SPECIFICATIONS

**The replacement wording is accepted as directed and requires no specification change.**

| | |
|---|---|
| **replace** | *"Existing citations remain valid for the artifact against which they were authored."* |
| **with** | *"Existing citations remain valid for the artifact that CF-001 ultimately determines them to have been authored against."* |

**Location: the Determination's own CITATION IMPLICATIONS section.** Neither `EGS-001` nor the lifecycle specification carries this sentence, so **no update to either document is required.**

**The ambiguity is closed.** The replacement makes the placeholder reading explicit, so no unregistered artifact acquires standing by implication, and `RIDER_REGISTRY`'s declared source remains an open question for `CF-001` to settle. **`CF-001` is untouched and remains `UNRESOLVED — REQUIRES EXECUTIVE DETERMINATION`.**

---

# 2 · CLARIFICATION 1 — RESOLVED, WITH ONE LIVE CONSEQUENCE

**"Production = the work" is adopted. "Production = lineage" is rejected.** The definition is transcribed into `EGS-001 §1A` at update `S-8`.

## 2.1 · The consequence, stated plainly

**Under this clarification, the 08-22 assembly and the 08-24 lineage are the same production.** They are two lineages within one governed creative work.

Therefore, by `U-1`:

> **The render currently carrying `approval_status: APPROVED` and the future 08-24 viewing master cannot both hold canonical authority. Designating the second supersedes the first.**

**`ED-005` Master Picture Designation is therefore also a supersession, and should be issued as one.** A determination that designates without superseding would leave two canonical viewing masters for one production — which `U-1` forbids and `U-4` would report as a defect.

**The register already anticipates this and says so against its own entry:**

> *"Until a conformant master of the 08-24 production is exported and designated, **this register names an approved viewing master for a superseded assembly.** Recorded here rather than corrected, per NO SILENT RECOVERY."*

**The clarification converts that from an anomaly into a scheduled transition.**

## 2.2 · No live violation exists — verified

**Checked rather than assumed.** `APPROVED_VIEWING_MASTER.yaml` contains two occurrences of the string `approval_status: APPROVED`:

```
line 25   inside the header comment, quoting the field name
line 76   the single actual register entry
```

**One entry. One canonical viewing master. `U-1` holds today.** `[E]`

**The same check across other artifact kinds:** one `etc_sha256` declared (`e91318a6…`), one `fcpxml_sha256` declared as editorial ground truth (`2bf06853…`), one file of each generated artifact kind. **No artifact kind currently has two claimants.**

**Adopting "production = the work" creates no immediate conflict.** It creates a scheduled one, at `ED-005`.

---

# 3 · THE EIGHT SPECIFICATION UPDATES — EXACT WORDING

**All eight are accepted in principle by ECO-001 Clarification 4. Exact text follows. None is applied here.**

---

## `S-1` · `EGS-001 §7.1.1` — discharge the departure

**Current heading and content:** *"### 7.1.1 · A departure from the Order, stated openly"* followed by the full disagreement between Objectives 4 and 5.

**Replace the entire subsection with:**

> ### 7.1.1 · The uniqueness key, determined
>
> **`U-1` keys uniqueness on `(artifact_kind, production)`. Version is excluded.**
>
> This was recorded in v0.2 as a departure from `EGS-001A` Objective 5, which specified a three-part key including version. **The Executive Determination — Canonical Authority Model resolved it: Model A is adopted, version describes historical identity and does not determine canonical authority.**
>
> The departure is discharged. `U-1` stands as written, on Executive determination rather than on this specification's reasoning.

**Rationale for the wording:** the original recorded *"the specification chose"*; the replacement records *"the Executive determined."* **The substance of `U-1` is unchanged; only its authority changes**, and per `§1B.2` that is a clarification rather than a reinterpretation.

---

## `S-2` · `EGS-001 §4A` and lifecycle `§1.5` — adopt the Determination's formulation

**In `EGS-001 §4A`, immediately beneath the heading, insert:**

> **Version belongs to provenance. Authority belongs to governance.**

**In the lifecycle specification `§1.5`, immediately beneath the heading, insert the same sentence.**

**Retain all existing bullets in both** as the operative rules beneath it. The sentence is the principle; the bullets are how it binds.

---

## `S-3` · `EGS-001 §6.5` and `§7` — discoverability of superseded artifacts

**In `§6.5`, append a sixth enumeration requirement:**

> - **every artifact ever promoted for a given `artifact_kind` and `production`, in promotion order, each with its current standing.**

**And in `§7`, add after `§7.4`:**

> ## 7.5 · Discoverability
>
> **A superseded artifact SHALL remain discoverable.** Supersession removes canonical authority and removes nothing else — not identity, not provenance, not lineage, not hash, not promotion history, and **not findability.**
>
> **SHALL:** the register SHALL retain every entry it has ever held, and enumeration (`§6.5`) SHALL be able to return the complete promotion history of an `artifact_kind` and `production` without a human reading the register.
>
> **Retention without enumeration is a filing cabinet with no index.** The platform has already learned that a record nothing can find is a record that goes stale unnoticed — `WET-SPEC-GATE-001 §6` says the same thing about gates.

---

## `S-4` · `EGS-001` — new `§7.6`, historical retrieval

**Add:**

> ## 7.6 · Historical retrieval
>
> **Historical states SHALL be retrievable, and the retrieval SHALL be explicit.**
>
> Four paths carry historical standing, and an implementation SHALL support retrieval through them: **lineage · promotion history · registry history · governed queries.**
>
> **A retrieval SHALL:**
> - return every artifact with its standing at the time requested, and its standing now;
> - identify each returned artifact by `sha256`.
>
> **A retrieval SHALL NOT:**
> - return a superseded artifact in response to an unqualified request — `§7.7`;
> - present any artifact without its standing;
> - require a consumer to interpret a path, filename or directory to determine standing — `N-5`;
> - restore canonical authority. **Retrieval reads; it never promotes.**
>
> **Mechanism is out of scope.** This clause states what a retrieval must return and must never do.

---

## `S-5` · lifecycle `P-3` — align with *"not restored implicitly"*

**Current text:** *"`P-3` · `SUPERSEDED → CANONICAL` SHALL NOT occur. A superseded artifact is not reinstated; a new promotion of the same bytes is a **new entry** citing the same `sha256`. `DOC-002` applied to status."*

**Replace with:**

> **`P-3` · `SUPERSEDED → CANONICAL` SHALL NOT occur as a transition, and historical authority SHALL NOT be restored implicitly.** A superseded artifact regains canonical authority **only by a new promotion entry** citing the same `sha256` — never by transition, never by mutation of an existing entry, and never implicitly. `DOC-002` applied to status.

**Why the change is needed:** the Determination forbids *implicit* restoration, which by implication permits explicit restoration. `P-3` as written reads as an absolute prohibition. **They are compatible — `P-3`'s second sentence already supplies the explicit mechanism — but a future reader could conclude that one forbids what the other permits.** The replacement makes the equivalence textual.

---

## `S-6` · `EGS-001` — new `§7.7`, resolution

**The most substantive addition. v0.2 defines what is canonical and never defines how anything asks.**

> ## 7.7 · Resolution — how a consumer asks
>
> **An unqualified request naming an `artifact_kind` and a `production` SHALL resolve to the single active canonical artifact for that pair, and to nothing else.**
>
> **`RES-1` · Canonical access is implicit.** A consumer requesting `PICTURE_LOCK` for a production receives the active canonical artifact without qualifying the request and without ambiguity.
>
> **`RES-2` · Historical access is explicit.** A consumer requesting a superseded or historical artifact SHALL say so, and the retrieval SHALL carry that artifact's standing — `§7.6`.
>
> **`RES-3` · An unqualified request that resolves to zero, or to more than one, SHALL fail shut.** It SHALL NOT return an arbitrary member, the most recent, the highest version, or a default. **`WET-SPEC-GATE-001 §3`: a control artifact that cannot answer conclusively is treated as closed.**
>
> **`RES-4` · Resolution SHALL NOT consult a path, filename, directory or modification time.** The register is the only source of standing — `N-5`, `§7.3`.
>
> **`RES-3` is the clause that matters.** `U-4` already declares more than one active canonical a defect that SHALL be enumerable. **Resolution is where that defect would otherwise stop being visible and start being answered** — and an arbitrary answer to *"which is the picture lock?"* is the failure this platform exists to prevent.

---

## `S-7` · `EGS-001` — new `§1D`, the governing principles

**Add after `§1C`:**

> # 1D · Governing principles (declared)
>
> **Transcribed from the Executive Determination — Canonical Authority Model. Eight restate rules already in this specification; principle 6 is the Determination's own contribution and is the sentence `U-1` exists to enforce.**
>
> 1. Custody never implies authority.
> 2. Execution never implies governance.
> 3. Promotion records a decision; it never creates one.
> 4. Reproducibility is preferred; exceptions must be explicitly declared.
> 5. Silence is never approval.
> 6. **Authority is singular.**
> 7. Evidence is immutable.
> 8. History is preserved.
> 9. Supersession transfers authority, never identity.

**Transcribed, not paraphrased**, consistent with how the platform carries ratified Executive text elsewhere.

---

## `S-8` · `EGS-001 §1A` — define `artifact kind` and `production`

**The uniqueness key rests on two terms neither this specification nor the repository defines. Verified: zero governed definitions of either.**

**Add two rows to the `§1A` definitions table:**

| term | definition |
|---|---|
| **Production** | **A complete governed creative work from which one public master is ultimately designated.** A production is **not** a lineage, an editorial assembly, an intermediate cut, an engineering generation, or a timeline revision. **Lineages exist within a production**, and one production may contain multiple assemblies, multiple picture locks, multiple intermediate timelines and multiple superseded artifacts. |
| **Artifact kind** | The class of artifact an artifact belongs to, independent of its version or its content — for example `PICTURE_LOCK`, `EDITORIAL_TIMING_CONTRACT`, `CONDUCTOR_SCORE`, `VIEWING_MASTER`. **Kind is the axis on which canonical authority is unique** (`U-1`); **version is not** (`§4A`). Two artifacts differing only in version are **the same kind.** |

**The `Production` definition is transcribed verbatim from ECO-001 Clarification 1.**

**`Artifact kind` is proposed, not transcribed**, and the Executive should read it deliberately: **it settles that `CONDUCTOR_SCORE` and `CONDUCTOR_SCORE v1.1` are the same kind and therefore compete for one canonical slot.** The alternative reading — that a version change makes a new kind — would let every version be canonical in its own right and would make `U-1` do no work. **The definition above is the one consistent with Model A; it is flagged because it is mine, not yours.**

---

# 4 · DESIGNATION — RECOMMENDATION

**`docs/README.md` is the authoritative numbering policy and it states the class boundary directly:**

> *"ADRs govern the platform · PDRs govern productions · Reference Executions govern comparison."*

**The Determination governs the platform.** It establishes the authority model every future promotion, supersession and implementation will assume. It is not a production decision and not a comparison record. **By the repository's own boundary it is an Architecture Decision Record.**

## 4.1 · Recommendation

```
RECOMMENDED:   ADR-012 — Canonical Authority Model
               held in docs/adr/
               Chairman countersignature, per platform-scope convention
```

## 4.2 · Why `ADR-012` and not `ADR-010`

**Because 010 and 011 are already taken, in two different senses, and both would collide.**

| number | state |
|---|---|
| `ADR-010` | cited twice — as *"ADR-010 candidate"* in `BRIEF_Domain_Map_Automation.md`, **and named in `CAR-003 F4` as a referenced ADR with no document in this repository** |
| `ADR-011` | cited in `EXECUTIVE_RULINGS.yaml` as part of a proposed ER reclassification — **a proposal closed by Executive Clarification 3, Option A adopted** |
| `ADR-002` · `ADR-004` · `ADR-005` | **cited nowhere in this repository** |

**The gaps SHALL NOT be backfilled, and this is the load-bearing reason.** `CAR-003 GD-01` records that `ADR-001` *"may live in the W.E.I.C.P. corpus, which this review cannot see."* **A number that looks free here may be assigned in a corpus this repository cannot read.** Taking the next number above the highest cited — 011 — avoids that entirely.

## 4.3 · One condition, and it is not cosmetic

**The ADR series carries an open HIGH-severity finding.** `CAR-003 GD-01`:

> *"**ADR-001, ADR-003, ADR-006, ADR-010 referenced but absent from this repository.** ADR-003 is cited 16 times… **this repository cannot resolve its own governance references.**" · severity **HIGH***

**Filing a foundational determination into a series that cannot resolve its own references means the foundational instrument inherits that condition.** Every downstream citation of `ADR-012` would sit in a register where four of its siblings are unresolvable.

**Two dispositions, offered without preference:**

- **Close `GD-01` first** — locate or formally retire `ADR-001`, `-003`, `-006`, `-010` — then file. Cleanest, and it retires a HIGH finding that has been open since `CAR-003`.
- **File now, and record the series' state inside the ADR itself** — a short provenance note stating that four sibling ADRs are unresolvable at the time of filing. **Honest, immediate, and consistent with NO SILENT RECOVERY.**

**What should not happen is filing silently into the series as though it were sound.**

## 4.4 · Why not a new document class

**Considered and not recommended.** `docs/README.md` already carries six document classes, and the platform has twice chosen restraint over proliferation — `ADR-009` chose a module over a fifth engine, and `WET-SPEC-GATE-001 §7` names gate proliferation as a real risk with four explicit controls.

**A Canonical Authority Model is exactly what an ADR is for.** Creating a class to hold one instrument would be the proliferation those precedents exist to prevent.

**The identifier is recommended, not assigned. Assignment awaits Executive confirmation.**

---

# 5 · CONTRADICTIONS — NONE REMAIN

| check | result |
|---|---|
| Determination vs `EGS-001 v0.2` | **NONE** — 11 clauses checked; 7 already expressed, 4 additive (`S-3`, `S-4`, `S-6`, `S-7`) |
| Determination vs lifecycle v0.2 | **NONE** — one wording alignment required (`S-5`) |
| ECO-001 Clarification 1 vs live repository state | **NONE** — verified, §2.2 |
| ECO-001 Clarification 2 vs `CF-001` | **RESOLVED** — the pre-disposition risk is closed, §1 |
| The eight updates against each other | **NONE** — `S-6` `RES-3` depends on `U-4`, which is unchanged; `S-8` supplies terms `U-1` already used |
| `APPROVED_VIEWING_MASTER` | **CONFIRMED as the precedent** — its *"EXACTLY ONE entry per production"* rule is `U-1` for one artifact kind |
| `ER-003` · `DOC-002` · `DOC-001` | **REINFORCED** |
| `WET-SPEC-GATE-001` · `WET-SPEC-REPORT-001` · `WET-REV-002` · `EPR-001 §2.3` | **UNWEAKENED** |
| `EGS-001 §1B.2` stability clause | **CONSISTENT** — both drafts remain `DRAFT`; no ratified meaning is reinterpreted |

## 5.1 · One item carried forward, unchanged

**`ED-005` Master Picture Designation is now also a supersession** — §2.1. That is a consequence of Clarification 1, not a contradiction, and it is recorded so `ED-005` can be drafted as one instrument rather than discovered as two.

---

# 6 · WHAT THIS DOCUMENT DOES NOT DO

- **It does not edit either specification.** Both v0.2 drafts stand unchanged; §3 is text awaiting an amendment order.
- **It does not assign a designation** — §4 is a recommendation.
- **It does not ratify anything.**
- **It does not resolve `CF-001`, `ED-002`, `ED-003`, `ED-004` or `ED-005`.**
- **It does not implement anything.** No runtime, guard, generator, registry or artifact was touched.
- **It does not close `CAR-003 GD-01`** — §4.3 names it as a condition, nothing more.

---

# 7 · CERTIFICATION

```
ECO-001 clarifications applied    4 of 4
  C1  production = the work        ADOPTED · transcribed at S-8 · consequence at §2.1
  C2  citation wording             RESOLVED · changes the Determination, not the specs
  C3  designation                  RECOMMENDED ADR-012, with one condition · NOT ASSIGNED
  C4  eight updates                EXACT WORDING at §3

Open Executive questions          0
Contradictions remaining          NONE
Live U-1 violations               NONE — verified
Updates requiring Executive read  1 — S-8 'artifact kind' is proposed, not transcribed

Specifications edited             NONE
Determination amended             NONE — §1 states the change; it is not made here
Designation assigned              NONE
Runtime / guards / generators     UNTOUCHED
Registries                        UNTOUCHED
Artifacts reclassified            NONE
Commits                           NONE
```

---

*Prepared under EXECUTIVE CLARIFICATION ORDER ECO-001. Custody: MACHINE. Authority: NONE. No specification was edited, no designation assigned, no artifact reclassified, no runtime component, guard, generator or registry modified, and no commit made. Nothing is ratified or determined by this document.*
