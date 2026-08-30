# SPECIFICATION FINALIZATION PLAN

**Issued under:** EXECUTIVE ORDER `EO-WET-EXEC-017` — Finding 3, Executive Producer / Chairman, 2026-08-30
**Prepared by:** Governance Compliance Auditor · **Custody:** `MACHINE` · **Authority:** NONE
**Repository:** READ ONLY at `b4d8529` · **Implementation:** NOT AUTHORIZED · **Commits:** none

> **This plan describes a regeneration. It does not perform one.** No specification is amended, no v1.0 is produced, and nothing here is authorized.

---

# 1 · WHAT EXISTS AND WHAT DOES NOT

| artifact | in repository | sha256[:16] |
|---|---|---|
| `docs/specs/EGS-001_EXECUTION_GATE_SPECIFICATION.md` **v0.2** | **yes** | `2361b89eb15ca9bb` |
| `docs/specs/ARTIFACT_LIFECYCLE_SPECIFICATION.md` **v0.2** | **yes** | `be8cc161f5bd4daf` |
| `docs/reviews/ratification/EGS-001_v0.2_RATIFICATION_REDLINE.md` — 9 amendments | **yes** | `51a1887740bcae46` |
| `docs/reviews/ratification/ARTIFACT_LIFECYCLE_v0.2_RATIFICATION_REDLINE.md` — 2 amendments | **yes** | `0ea99ef3af77506e` |
| `EGS-001` **v1.0** | **NO** | — |
| `ARTIFACT_LIFECYCLE_SPECIFICATION` **v1.0** | **NO** | — |

**11 amendments are packaged. 0 are applied.** `[E]`

**The normative target is the redlines, not the briefing.** `CAM-002` §0 states it: *"`EGS-001_v0.2_RATIFICATION_REDLINE.md` and `ARTIFACT_LIFECYCLE_v0.2_RATIFICATION_REDLINE.md` are the normative implementation targets. **CAM-002 is explanatory and confers no normative force on any wording it summarizes.** Where this briefing and a redline differ, **the redline governs.**"* `[E]`

---

# 2 · WHY THIS IS A REGENERATION AND NOT AN EDIT

**`DOC-002` — *regenerate, never patch*.** `ADR-009` §2 applies the same rule to governed artifacts: regenerate-on-mismatch, never hand-edit.

**v1.0 is therefore a new artifact, not a modified v0.2.** Applying nine edits in place to `EGS-001_EXECUTION_GATE_SPECIFICATION.md` would be a patch, would break the doctrine on the document that codifies the doctrine's own gate model, and would leave v0.2 unretrievable.

**Consequence for custody, drawn from the ratified model itself.** Under the Single Active Canonical Authority Model, **v0.2 and v1.0 are the same artifact kind and compete for one canonical slot.** On promotion of v1.0, **v0.2 becomes `SUPERSEDED` — retaining identity, provenance, lineage, hash, promotion history and discoverability, and losing only authority.** `CAM-002` §3.6: *"Supersession occurs by promotion of the successor, never by mutation of the incumbent."* **v0.2 is not deleted and not overwritten.** `[E]`

---

# 3 · ENTRY CONDITIONS

**All four are Stage 2A items. None is satisfied today.**

| # | condition | state |
|---|---|---|
| 1 | `A-8b` adopted by positive Executive act | **not adopted** — `REQUIRES EXECUTIVE ADOPTION` |
| 2 | `GD-01` disposed | **OPEN · HIGH** |
| 3 | Designation confirmed (`ADR-012` recommended, not assigned) | **not assigned** |
| 4 | Both redline packages ratified | **not ratified** |

**`A-8b` is load-bearing and is the one amendment whose wording did not originate with the Executive.** If it is adopted in different words, the `Artifact kind` definition in `EGS-001 §1A` changes with it, and `U-1` — authority uniqueness — changes meaning. **Regeneration cannot begin before adoption, because the adopted text is an input.** `[E]`

---

# 4 · THE REGENERATION

## 4.1 · Inputs, hash-pinned

Each regeneration takes exactly four inputs, and each is pinned by hash at the time of the run:

```
source specification      v0.2, sha256 recorded
amendment package         the ratified redline, sha256 recorded
adopted A-8b text         as adopted, verbatim          (EGS-001 only)
confirmed designation     as assigned
```

**No other input.** `CAM-002` is explanatory and is **not** an input. Nothing is drawn from session context, from this plan, or from engineering interpretation.

## 4.2 · Method

**Each amendment replaces the quoted current wording with the quoted replacement wording, verbatim.** The redlines were written in `current → replacement → authority → reason → traceability` form precisely so that application is mechanical.

**No amendment is paraphrased, merged, reordered, or improved in application.** Where a redline's *reason* explains an amendment, the reason is not carried into the specification.

## 4.3 · What the regeneration must not do

| | |
|---|---|
| Introduce wording not in a ratified redline | **prohibited** |
| Apply `A-8b` before it is adopted | **prohibited** |
| Renumber, restructure or reformat sections not named by an amendment | **prohibited** |
| Modify, delete or overwrite v0.2 | **prohibited** — `DOC-002`, §2 |
| Carry `CAM-002` wording into a specification | **prohibited** — `CAM-002` confers no normative force |
| Resolve `CF-001` or any `ED-00x` | **prohibited** — out of scope |
| Instantiate a Promotion Register | **prohibited** |

**`EPR-001 §2.3` governs here as everywhere: nothing is authored, populated, inferred, extended, suggested or defaulted.**

---

# 5 · ACCEPTANCE — PROPOSED, NOT SET

> **The acceptance criterion for a regenerated governed artifact is an Executive act. The criteria below are proposed for adoption and are not in force.** `[O]`

| # | proposed criterion |
|---|---|
| **A-1** | **Amendment completeness** — all 9 `EGS-001` amendments and both Lifecycle amendments present in v1.0; **11 of 11**, enumerable |
| **A-2** | **Amendment exclusivity** — a diff v0.2 → v1.0 shows **no change not traceable to a ratified amendment**. Every changed region maps to an amendment ID |
| **A-3** | **Verbatim replacement** — each replaced region matches the redline's replacement wording byte-for-byte |
| **A-4** | **Non-mutation of the incumbent** — v0.2's sha256 is unchanged from §1 after the run |
| **A-5** | **Authority uniqueness** — exactly one active canonical artifact per kind after promotion; **`active` computed, never authored** |
| **A-6** | **Traceability** — `RATIFICATION_TRACEABILITY_MATRIX` resolves against v1.0 with 11 of 11 rows satisfied |

**`A-2` is the criterion that does the work.** `A-1` catches omission; **`A-2` catches insertion** — the failure mode where a regeneration quietly improves wording nobody ratified. **That is the mechanism by which engineering wording becomes Executive authority, and `EO-WET-EXEC-014` forbids it explicitly:** *"Do not silently elevate engineering wording into Executive authority."* `[E]`

**Byte-equality is not available as a gate here, and the difference from `ED-001A` is worth stating.** The ETC extractor could be gated on byte equality because a reference artifact existed to reproduce. **No v1.0 exists to compare against — the regeneration produces the first one.** `A-2` is the substitute: not *"does it match a known answer"* but *"is every difference authorized."*

---

# 6 · OUTPUT AND CUSTODY

| | |
|---|---|
| `EGS-001` v1.0 | `docs/specs/` · status `RATIFIED` |
| `ARTIFACT_LIFECYCLE_SPECIFICATION` v1.0 | `docs/specs/` · status `RATIFIED` |
| v0.2 of each | **retained**, status `SUPERSEDED`, discoverable |
| Regeneration record | inputs and their hashes, amendments applied, `A-1`…`A-6` results |

**Filename question, raised not decided.** Whether v1.0 occupies the same path as v0.2 or a version-bearing path determines whether v0.2 remains retrievable by path or only by history. **`EGS-001` §4A holds that version belongs to provenance and authority to governance — which settles the authority question and not the filesystem one.** This is a naming decision reserved to the Executive. `[O]`

---

# 7 · WHAT THIS STAGE DOES NOT DO

**No implementation occurs during Specification Finalization.** No runtime component, guard, generator or registry is touched. No Promotion Register is instantiated. No `execution_class` is implemented. **The five runtime requirements in `EGS-001` remain requirements and await a separate Order.**

**Ratifying a specification does not change behaviour.** `CAM-002` §2.4: *"`G-12` continues to admit one mode. No guard changes. No generator changes."* `[E]`

---

```
SPECIFICATION FINALIZATION PLAN       PLAN ONLY

Specifications to regenerate          2
Amendments to apply                   11   ·   applied 0
Entry conditions                      4    ·   satisfied 0
Proposed acceptance criteria          6    ·   in force 0
Load-bearing dependency               A-8b adopted text

Specifications amended                NONE
Implementation                        NONE
Commits                               NONE
Architecture                          FROZEN — EO-WET-EXEC-014 intact
```

---

*Prepared under `EO-WET-EXEC-017` Finding 3. Custody: `MACHINE`. Authority: NONE. No specification was amended or regenerated, no acceptance criterion set, no designation assigned, and no commit made.*
