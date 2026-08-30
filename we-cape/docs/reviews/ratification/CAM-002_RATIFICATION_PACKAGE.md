# CAM-002 — RATIFICATION PACKAGE

**Issued under:** EXECUTIVE ORDER EO-WET-EXEC-013, Executive Producer / Chairman, 2026-08-30
**Subject:** Canonical Authority Model · `EGS-001` v0.2 · `ARTIFACT_LIFECYCLE_SPECIFICATION` v0.2
**Working designation:** `ADR-012 (Proposed)` — **pending Executive ratification. Not assigned.**
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NOT AUTHORIZED
**Repository:** READ ONLY at HEAD `1552e42` · **Commits:** none

> # STATUS OF THIS DOCUMENT
>
> **This document is an Executive ratification briefing. It summarizes the proposed amendments. Normative language resides only within the accompanying ratification redline packages upon Executive ratification.**
>
> `EGS-001_v0.2_RATIFICATION_REDLINE.md` and `ARTIFACT_LIFECYCLE_v0.2_RATIFICATION_REDLINE.md` are the normative implementation targets. **CAM-002 is explanatory and confers no normative force on any wording it summarizes.** Where this briefing and a redline differ, **the redline governs.**

> **This package prepares ratification. It does not execute it.** Nothing here amends a specification, assigns a designation, changes runtime behaviour, or creates a commit.

---

# 1 · EXECUTIVE SUMMARY

## 1.1 · Purpose

To place before the Executive, in one reading, everything required to ratify the Canonical Authority Model and the two specifications that express it — **so that ratification is a single act rather than a sequence of clarifications.**

## 1.2 · Scope

| in scope | out of scope |
|---|---|
| The Canonical Authority Model as an architectural determination | Any implementation of it |
| `EGS-001` v0.2 and its 9 packaged amendments | Runtime, guards, generators, registries |
| `ARTIFACT_LIFECYCLE_SPECIFICATION` v0.2 and its 2 packaged amendments | Creation of a Promotion Register |
| A recommended designation | Assignment of that designation |
| | `CF-001`, `ED-002` … `ED-005` |

## 1.3 · Repository state

```
HEAD                     1552e42
Working tree             CLEAN — verified
Specifications amended   0
Runtime modified         NONE   ·   Guards   NONE   ·   Generators   NONE
Registries modified      NONE
Promotion Register       does not exist — 0 occurrences
execution_class          appears in 0 contexts
Commits                  NONE
```

## 1.4 · Evidence reviewed

| instrument | contribution |
|---|---|
| `PRR-001` | platform phase; the coupling measurement |
| `PLR-001` · `CCR-001` · `CIA-001` (Errata 1, 2) | the determinations' evidentiary base |
| `CF-001` | the provenance conflict, unresolved and excluded |
| `EDR-001` · `EDR-002` | readiness; the Gate A/B architecture; provenance as a class |
| `EGS-001` v0.1 → v0.2 · `EGS-001A` readiness review | the specification and its consistency review |
| `CAM-001` impact assessment · `ECO-001` clarifications | the eight amendments and their authority |
| Live repository measurement | `U-1` violation check; designation collision; standards check |

## 1.5 · Readiness

```
Open Executive questions          0
Contradictions                    NONE — 8 ratified standards checked, 3 reinforced
Live U-1 violations               NONE — verified
Amendments packaged               11, traceable to ECO-001 or the Determination
Positive acts required            2 — §5
```

## 1.6 · Ratification decision

**The decision before the Executive is a single one: ratify the Canonical Authority Model and, with it, `EGS-001` v1.0 and `ARTIFACT_LIFECYCLE_SPECIFICATION` v1.0 as amended by the two redline packages.**

Two items require a positive act rather than assent — §5. **Neither blocks the decision; both must be answered within it.**

---

# 2 · WHAT IS BEING AMENDED, AND WHAT IS NOT

## 2.1 · Specifications being amended

| specification | current | amendments | becomes |
|---|---|---|---|
| `EGS-001_EXECUTION_GATE_SPECIFICATION.md` | DRAFT v0.2 | **9** | v1.0, RATIFIED |
| `ARTIFACT_LIFECYCLE_SPECIFICATION.md` | DRAFT v0.2 | **2** | v1.0, RATIFIED |

**No other document is amended by this package.**

## 2.2 · Specifications and instruments remaining unchanged

`WET-SPEC-GATE-001` · `WET-SPEC-REPORT-001` · `WET-SPEC-DIE-001` · `WET-SPEC-002` · `DWR-001` · `docs/README.md` · `SOP-04` `SOP-05` `SOP-06` · `DOC-001` `DOC-002` · `ADR-007` `ADR-009` · `ER-003` · `EPR-001` · `APPROVED_VIEWING_MASTER.yaml` · every registry · every runtime component · every generator · every guard.

## 2.3 · What becomes normative on ratification

- The **Single Active Canonical Authority Model** — one active canonical artifact per artifact kind per production.
- The **definition of a production** — a complete governed creative work from which one public master is ultimately designated; **not a lineage**.
- The **definition of an artifact kind** — subject to §5.
- The **six artifact states** and the transitions between them.
- The **four status domains**, held apart as separate fields.
- The **Promotion Register schema** — as a schema.
- The **resolution model** — canonical access implicit, historical access explicit, ambiguity fails shut.
- The **historical retrieval model** — four paths, with what a retrieval must and must not do.
- The **nine governing principles**.
- The **five runtime requirements** — as requirements.
- **Specification stability** — no future revision may reinterpret a ratified state's meaning.

## 2.4 · What does not become normative

- **No runtime behaviour.** `G-12` continues to admit one mode. No guard changes. No generator changes.
- **No Promotion Register exists.** A schema is ratified; a register is not created.
- **No artifact is reclassified.** Nothing acquires or loses a status.
- **No implementation is authorized.** The five runtime requirements await a separate Order.
- **No designation is assigned.**
- **`CF-001` is not resolved**, and no caption stream becomes authoritative.
- **`ED-002` … `ED-005` are not determined.**

---

# 3 · EXECUTIVE FINDINGS

## 3.1 · Canonical Authority Model — Model A adopted

Two models were available. **Model A** places authority in exactly one artifact per kind per production; promotion transfers it; the incumbent becomes `SUPERSEDED` and loses nothing but authority. **Model B** would have let each version retain authority for its own historical state, requiring every downstream consumer to become version-aware.

**Model A is adopted.** It preserves the separations the platform has held throughout — custody from authority, execution from promotion, artifact from registry, lineage from workflow, evidence from governance — and it keeps authority singular rather than contextual.

## 3.2 · Production defined

> *A complete governed creative work from which one public master is ultimately designated.*

**Not a lineage, not an assembly, not an intermediate cut, not a timeline revision.** Lineages exist *within* a production, and one production may hold multiple assemblies, multiple picture locks and multiple superseded artifacts.

**One consequence follows and is recorded here rather than discovered later.** The 08-22 assembly and the 08-24 lineage are the same production. **Designating an 08-24 viewing master therefore supersedes the current one** — so `ED-005` is a designation *and* a supersession, and should be issued as one instrument.

## 3.3 · Artifact kind defined

The class an artifact belongs to, independent of version or content. **Kind is the axis on which authority is unique; version is not.** Two artifacts differing only in version are the same kind and compete for one canonical slot.

**This definition is the one item in the package not authored by the Executive — §5.**

## 3.4 · Resolution model

**Canonical access is implicit. Historical access is explicit.** A request naming a kind and a production returns the single active canonical artifact. A request for anything historical must say so and carries the artifact's standing.

**And a request that resolves to zero or to more than one fails shut** — never an arbitrary member, never the most recent, never the highest version. **An arbitrary answer to *"which is the picture lock?"* is the failure this platform exists to prevent.**

## 3.5 · Historical retrieval

Four paths carry historical standing: **lineage · promotion history · registry history · governed queries.** A retrieval returns every artifact with its standing then and now, identified by hash. **It never returns a superseded artifact to an unqualified request, never presents an artifact without its standing, never requires a path to be interpreted, and never restores authority. Retrieval reads; it never promotes.**

## 3.6 · Supersession model

**Supersession occurs by promotion of the successor, never by mutation of the incumbent.** The incumbent retains identity, provenance, lineage, hash, promotion history and **discoverability**. Only authority moves.

**Historical authority is never restored implicitly.** A superseded artifact regains authority only by a new promotion entry.

## 3.7 · Authority uniqueness

**At most one active canonical promotion per artifact kind per production.** `active` is computed, never authored. More than one is a defect, enumerable and reported rather than silently resolved.

**Verified against the live repository: no violation exists today.** One approved viewing master, one editorial timing contract, one editorial ground truth, one file per generated artifact kind.

---

# 4 · REMAINING OPEN MATTERS

**Intentionally deferred. Nothing in this package advances any of them.**

| item | state |
|---|---|
| **`CF-001`** Citation Provenance | `UNRESOLVED — REQUIRES EXECUTIVE DETERMINATION` |
| **`ED-002`** Token Normalization | `NOT READY` — no governing artifact defines any of the eight elements |
| **`ED-003`** Picture Lock Designation | `READY WITH CONDITIONS` |
| **`ED-004`** Caption Collapse Rule | `READY WITH CONDITIONS` |
| **`ED-005`** Master Picture Designation | `NOT READY` — and now also a supersession, §3.2 |
| **Generator implementation** | Not authorized. Includes release of the generator lock |
| **Runtime implementation** | Not authorized. The five requirements await a separate Order |

---

# 5 · TWO POSITIVE ACTS REQUIRED AT RATIFICATION

**Neither is a tick. Both require a decision inside the ratification.**

## 5.1 · Adopt the `Artifact kind` definition

**`A-8b` is the only amendment in the package whose wording did not originate with the Executive.** `ECO-001` Clarification 4 authorizes new definitions — that grants authority for the amendment, not for the text.

**It is consequential.** The definition settles that `CONDUCTOR_SCORE` and `CONDUCTOR_SCORE v1.1` are the same kind. **The alternative — that a version change creates a new kind — would let every version be canonical in its own right and make authority uniqueness do no work.**

## 5.2 · Confirm the designation

**Recommended: `ADR-012`.** `docs/README.md` states the class boundary — *"ADRs govern the platform"* — and this governs the platform. Not `ADR-010` or `ADR-011`; both are already cited. **The gaps at 002, 004 and 005 must not be backfilled**, because `CAR-003` records that some ADRs may live in a corpus this repository cannot read.

**One condition.** The ADR series carries an open **HIGH** finding — `CAR-003 GD-01`: four referenced ADRs absent, *"this repository cannot resolve its own governance references."* **Either close `GD-01` first, or record the series' state inside the ADR itself.** Filing silently as though the series were sound is the one disposition not recommended.

---

# 6 · THE PACKAGE

| document | contains |
|---|---|
| **`CAM-002_RATIFICATION_PACKAGE.md`** | this document — the Executive review |
| `EGS-001_v0.2_RATIFICATION_REDLINE.md` | 9 amendments, current → replacement → authority → reason → traceability |
| `ARTIFACT_LIFECYCLE_v0.2_RATIFICATION_REDLINE.md` | 2 amendments, same structure |
| `RATIFICATION_TRACEABILITY_MATRIX.md` | 11 rows; every amendment traced to `ECO-001` or the Determination |
| `RATIFICATION_CHECKLIST.md` | repository · architecture · specifications · runtime · standards · certification |

---

```
CANONICAL AUTHORITY MODEL          READY FOR EXECUTIVE RATIFICATION

Specifications to ratify           2   EGS-001 v1.0 · Artifact Lifecycle v1.0
Amendments packaged                11  ·  applied 0
Open Executive questions           0
Contradictions                     NONE
Positive acts required             2   §5.1 artifact kind · §5.2 designation

NOT RATIFIED   ·   NOT IMPLEMENTED   ·   NOT DESIGNATED
Runtime unchanged  ·  Registries unchanged  ·  Repository clean at 1552e42
Commits                            NONE
```

---

*Prepared under EXECUTIVE ORDER EO-WET-EXEC-013. Custody: MACHINE. Authority: NONE. No specification was amended, no designation assigned, no artifact reclassified, no runtime component, guard, generator or registry modified, and no commit made. This package prepares ratification and does not execute it.*
