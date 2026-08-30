# EGS-001A — RATIFICATION READINESS REVIEW

**Issued under:** EXECUTIVE ORDER EGS-001A, Objective 6, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. No runtime component, guard, generator, registry or artifact was modified. No commit was made.
**Subjects:** `EGS-001_EXECUTION_GATE_SPECIFICATION.md` v0.2 · `ARTIFACT_LIFECYCLE_SPECIFICATION.md` v0.2

---

# 0 · VERDICT

```
RATIFICATION READY — WITH ONE EXECUTIVE DECISION OUTSTANDING
```

**Both drafts are internally consistent, introduce no governance contradiction, weaken no existing standard, and contain no implementation.**

**One item cannot be closed by engineering: the Order contradicts itself on the uniqueness key, and the specification chose a reading.** §3.1. That choice needs the Chairman's confirmation or reversal before ratification, because the two readings produce materially different platforms.

---

# 1 · OBJECTIVE-BY-OBJECTIVE

| # | objective | state | where |
|---|---|---|---|
| 1 | Specification Stability Clause | **APPLIED** | `EGS-001 §1B`, inherited by the companion §5 |
| 2 | Governance Status Separation | **APPLIED, AND EXTENDED** | `EGS-001 §1C` · companion §4.1 — **four domains, not two** |
| 3 | Normative Definitions | **APPLIED** | `EGS-001 §1A` — 11 terms, all repository-consistent |
| 4 | Version Independence | **APPLIED** | `EGS-001 §4A` · companion §1.5 |
| 5 | Promotion Register Uniqueness | **APPLIED WITH A STATED DEPARTURE** | `EGS-001 §7.1` · **departure at §7.1.1** — see §3.1 below |
| 6 | Ratification Readiness Review | this document | |

## 1.1 · Objective 2 was extended, and the extension is the point

The Order names **two** domains — artifact status and governance document status. **The repository has four.** `LINEAGE STATUS` and `WORKFLOW STATUS` are already in live use in `AR2-0824.context.json` and `INGESTION_MANIFEST.yaml`, and both were separated in v0.1.

**Separating only the two the Order named would have left the other two conflated**, which is the failure the objective exists to prevent. All four are now separate fields with an explicit `SHALL NOT` against merging.

**v0.1 got this partly wrong and v0.2 fixes it.** v0.1 listed governance document status as *"out of scope"* rather than as a distinct domain. **It is not out of scope — it is a fourth axis**, and the Order was right to name it.

---

# 2 · INTERNAL CONSISTENCY — THREE CONTRADICTIONS FOUND

**Objective 6 asks whether new contradictions exist. The review found three, two of them in my own v0.1, and all three are resolved or disclosed.**

## 2.1 · `RESOLVED` — v0.1's namespace/status deadlock

**v0.1 asserted three rules that cannot all hold.**

```
N-1   namespace and status SHALL agree
N-3   an artifact SHALL NOT be moved or copied into the canonical namespace
§4.6  promotion SHALL NOT be coupled to regeneration
```

**Promote an experimental artifact and all three bind at once: it must be canonical (status), it must be in the canonical namespace (`N-1`), it cannot be moved there (`N-3`), and it cannot be regenerated there (§4.6).** There is no legal outcome.

v0.1 deferred this as *"an implementation question."* **It is not. It is a specification question**, and leaving it open would have produced canonical artifacts sitting in the experimental namespace with nothing recording why — **the unlabelled-artifact condition this whole architecture exists to close.**

**Resolved at `EGS-001 §5.3`** by a required `materialization` field: `REGENERATED` (the default, consistent with `DOC-002`) or `IN_PLACE` (permitted only where regeneration is impossible, recorded as a **standing enumerable exception** for as long as the artifact holds canonical status).

**This is the most substantive change from v0.1, and it was found by this review rather than by the Order.**

## 2.2 · `RESOLVED` — v0.1 conflated execution class with status

v0.1's §3.6 table listed a governed production run as producing artifacts with `status: CANONICAL`. **That is wrong.** A `CANONICAL`-class run produces a **candidate**; status is conferred by promotion and by nothing else. v0.1 therefore contradicted its own §4.1.

**Corrected in `EGS-001 §3.6`:** *"Execution class is a permission to write to a namespace; it is not a grant of status."* Both columns now read `CANONICAL` **after promotion**.

**Left uncorrected, this would have permitted exactly the shortcut the architecture forbids** — a run declaring itself canonical and thereby being canonical.

## 2.3 · `DISCLOSED, NOT RESOLVED` — the Order contradicts itself

**§3.1 below. This one is not mine to resolve.**

---

# 3 · THE ONE OPEN ITEM

## 3.1 · The uniqueness key — Objectives 4 and 5 disagree

| | text |
|---|---|
| **Objective 4** | *"multiple versions of an artifact may exist, while **only one version may hold canonical status at a time**"* |
| **Objective 5** | *"For a given artifact kind, production, **version**, there may exist only one active CANONICAL promotion"* |

**Including `version` in the uniqueness key permits one active canonical promotion *per version* — that is, many at once.** That is the opposite of Objective 4.

**The specification chose Objective 4's reading**, on two grounds:

1. **It matches existing practice.** `APPROVED_VIEWING_MASTER`: *"EXACTLY ONE entry per production may carry status: APPROVED."* No version qualifier.
2. **Version is what distinguishes the candidates. It cannot also scope the uniqueness, or uniqueness does no work** — every version would trivially be unique in its own bucket.

**Recorded at `EGS-001 §7.1.1` rather than resolved silently, and the alternative is stated in full so the Chairman can reverse it.** If per-version canonicity is intended, `U-1` restores the Order's tuple and `§4A.2` is amended to match.

**These are materially different platforms.** One has a single authoritative artifact per kind; the other has a set of them, and every downstream consumer must then carry a version to know which it means.

---

# 4 · NO EXISTING STANDARD IS WEAKENED

Checked against every standard the drafts touch.

| standard | interaction | verdict |
|---|---|---|
| **`WET-REV-002`** — *never a parallel system* | No new gate kind, no second ledger. Promotion is a **register**, on the `APPROVED_VIEWING_MASTER` precedent | **HONOURED** |
| **`WET-SPEC-GATE-001`** | Extended, not amended. Borrows its fail-shut posture (§3), marker discovery (§4), computed aggregates (§5), proliferation controls (§7) | **UNWEAKENED** |
| **`WET-SPEC-REPORT-001`** | Restated in `EGS-001 §4.5` — percentages carry numerator, denominator, source; **no composite scores** | **UNWEAKENED** |
| **`DOC-002`** — regenerate, never patch | Applied three times: append-only entries (§7.4), `P-3` no reinstatement, `REGENERATED` as the default materialization | **REINFORCED** |
| **`DOC-001`** — validate the instrument | `R-5` enumeration, including the `T11` detector | **REINFORCED** |
| **`ER-003`** — custody is not authority | The architecture's foundation. `custody: MACHINE` **unchanged in both columns** of §3.6 | **PRESERVED** |
| **`EPR-001 §2.3`** — an empty field remains empty | `I-5`: absence is not a state; an unlabelled artifact is `REFERENCE_ONLY`, **not defaulted to anything permissive** | **CONSISTENT** |
| **Order 2026-08-28 §2.2** — `approval_status` is canonical | **Explicitly not renamed** — companion §1.4 | **PRESERVED** |
| **`ERO-001 §2`** — `G-12`'s assertions | `R-2` requires they *continue unchanged* for `CANONICAL` runs | **UNWEAKENED** |

**One deliberate strengthening, recorded as such:** `EGS-001 §4.4` requires a promotion to declare when an artifact **cannot be regenerated**. No existing standard requires this. It is added because the repository has three recorded instances of unreproducible governed artifacts — `191/191`, the missing ETC producer, and `CF-001` — **and a register that could not express the condition would have recorded all three as sound.**

---

# 5 · TERMINOLOGY CONSISTENCY

| check | result |
|---|---|
| Every defined term used consistently across both drafts | **PASS** — 11 terms, `EGS-001 §1A`, not redefined in the companion |
| No term redefined against repository usage | **PASS** — §1B.3 forbids it; §4 maps rather than renames |
| `SUPERSEDED` disambiguated across domains | **PASS** — three meanings named explicitly, `§1C.1` and companion `§4.1` |
| `custody` / `authority` consistent with `ER-003` | **PASS** |
| `CANONICAL` never conferred by location, name, age or run success | **PASS** — §1A, §4.1, §7.3 |
| Companion does not restate parent definitions | **PASS** — cites `EGS-001 §1A` |

---

# 6 · NO IMPLEMENTATION LANGUAGE HAS LEAKED

| check | result |
|---|---|
| File formats, paths, directory names specified | **NONE** — namespace is defined as a property, never as a location |
| Storage mechanism specified | **NONE** — `§7` is schema only |
| Code, pseudocode, function or module names | **NONE** — `G-12` is *cited* as existing, never modified |
| Versioning mechanism designed | **NONE** — `§4A` is a model, per the Order |
| Register instantiated | **NONE** — verified: `register_class: PROMOTION_REGISTER` appears **0 times** in the repository |
| `G-12` modified | **NONE** — verified unchanged, still single-mode |
| Any artifact reclassified | **NONE** |

**`R-2` is the closest approach to implementation and stays on the right side.** It states *what an admissible set must contain*, not how a guard is written. **It does not modify `G-12`; it states a requirement on a future implementation of it.**

---

# 7 · WHAT RATIFICATION WOULD AND WOULD NOT DO

| would | would not |
|---|---|
| Fix the meaning of six artifact states | Create any artifact in any of them |
| Fix four status domains as separate | Change any existing field |
| Bind future revisions to §1B stability | Bind any past artifact |
| Establish the Promotion Register schema | Create the register |
| Establish five runtime requirements | Authorize their implementation |
| Make `EGS-001` citable | Change what any run currently does |

**Ratification authorizes a specification. Implementation requires a separate Order.**

---

# 8 · RECOMMENDATION

```
RATIFICATION READY — WITH ONE EXECUTIVE DECISION OUTSTANDING

  §3.1   the uniqueness key.  Confirm (artifact_kind, production)
         as specified, or reverse to the Order's tuple including version.
         The specification chose; the Executive decides.
```

**Nothing else blocks ratification.** Two contradictions in my own v0.1 were found and resolved by this review; the third is the Order's and is disclosed rather than papered over.

**One observation offered without recommendation.** These specifications describe a platform that can rehearse — one where the ETC extractor may be pointed at an unratified lineage and the generator exercised against real inputs without any of it becoming governed. **The single largest constraint on this platform today is that it cannot rehearse**, and the reason the ETC extractor's validation needed a bespoke Order was that no standing category existed for a run that produces bytes and claims nothing. **Gate A is the honest home for work that has already happened.**

---

```
EGS-001                     DRAFT v0.2 — NOT RATIFIED
ARTIFACT LIFECYCLE          DRAFT v0.2 — NOT RATIFIED
Objectives applied          5 of 5, one with a stated departure
Contradictions found        3 — 2 resolved (mine, v0.1) · 1 disclosed (the Order's)
Existing standards weakened NONE — 9 checked
Standards reinforced        3 — DOC-001 · DOC-002 · ER-003
Implementation language     NONE
Register instantiated       NONE — verified 0 occurrences
G-12 modified               NONE — verified unchanged
Artifacts reclassified      NONE
Commits                     NONE

VERDICT                     RATIFICATION READY, pending §3.1
```

---

*Prepared under EXECUTIVE ORDER EGS-001A Objective 6. Custody: MACHINE. Authority: NONE. No runtime component, guard, generator, registry, caption stream or artifact was modified. No Promotion Register was instantiated. No commit was made. Nothing is ratified by this document.*
