# CANONICAL AUTHORITY MODEL — SPECIFICATION IMPACT ASSESSMENT

**Subject:** EXECUTIVE DETERMINATION — *Canonical Authority Model*, Executive Producer / Chairman, 2026-08-30
**Assessed against:** `EGS-001_EXECUTION_GATE_SPECIFICATION.md` v0.2 · `ARTIFACT_LIFECYCLE_SPECIFICATION.md` v0.2
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. No specification was edited. No runtime component, guard, generator, registry or artifact was modified. No commit was made.
**Measured at:** repository HEAD `1552e42`

> **This assessment identifies required specification updates. It does not make them.** Both v0.2 drafts are delivered unchanged, and the amendments below are proposals awaiting the Chairman's direction.

---

# 0 · VERDICT

```
THE DETERMINATION IS ARCHITECTURALLY SOUND AND INTRODUCES NO CONTRADICTION
WITH ANY RATIFIED STANDARD.

It closes the one open item blocking EGS-001 ratification.

  8 specification updates are required
  2 items need Executive clarification before those updates can be written
  1 designation defect must be corrected before the Determination is filed
```

---

# 1 · THE DESIGNATION DEFECT — CORRECT BEFORE FILING

**The Determination is designated `ED-001`. That designation is already in use, and the conflicting instrument is already committed.**

```
EXECUTIVE DISPOSITION ED-001    Acceptance of PRR-001 & Operational Sequencing
                                 issued 2026-08-30
docs/engineering/ED-001_PHASE1_EXECUTION_RECORD.md    committed at 1552e42
EXECUTIVE AUTHORIZATION ED-001A  Phase 1 Engineering Authorization
                                 cited throughout ETC_EXTRACTOR_VALIDATION_REPORT.md
```

**And the number sits below a live sequence.** `ED-002` Token Normalization, `ED-003` Picture Lock, `ED-004` Caption Collapse, `ED-005` Master Picture and `ED-006` Generator Lock are all pending determinations in `EDR-001`. **A second `ED-001` would sit beneath them while superseding none of them.**

**This is the fourth naming collision this engagement has surfaced**, after the two near-identically-named canonical masters, the three referents of *"Part 3"*, and the wrong stream declared in `RIDER_REGISTRY`. **Every one of them was a case of a name resolving to the wrong thing without erroring** — which is the failure class `EDR-002 §4` recorded as evidence-supported and distinct.

**A foundational determination is the worst possible place to introduce one.** Every downstream instrument will cite it by number, `ED-006` will cite it while depending on `ED-002`, and *"as required by ED-001"* will be ambiguous in a corpus that already contains an `ED-001` saying something else.

**Recommendation, offered without preference between the options:** designate it outside the `ED-nnn` determination sequence — the Determination is not one of the five pending determinations but the model they all assume. `CAM-001` (Canonical Authority Model) is used as a working handle in this assessment purely so the two can be told apart, and **no designation is asserted.** This is the Chairman's to assign.

---

# 2 · WHAT THE DETERMINATION CLOSES

**`EGS-001 v0.2 §7.1.1` recorded a departure from `EGS-001A` and asked the Chairman to confirm or reverse it. The Determination confirms it.**

| | |
|---|---|
| `EGS-001A` Objective 5 specified | uniqueness over `(artifact_kind, production, version)` |
| `EGS-001 v0.2 §7.1 U-1` specified | uniqueness over `(artifact_kind, production)` — version omitted |
| **The Determination establishes** | **Model A — exactly one active canonical per artifact kind per production; version does not determine authority** |

**`U-1` stands as written. §7.1.1 is discharged** and should be replaced by a citation to this Determination — update `S-1` below.

**The Determination also supplies a better formulation than mine** for the same idea:

> *"Version belongs to provenance. Authority belongs to governance."*

**That sentence does more work in nine words than `§4A.2` does in five bullets**, and it should be adopted verbatim — update `S-2`.

**And `EGS-001A`'s ratification blocker is now cleared.** The readiness review returned `RATIFICATION READY — WITH ONE EXECUTIVE DECISION OUTSTANDING`, and that decision is this one.

---

# 3 · CONSISTENCY WITH THE v0.2 DRAFTS

**No contradiction found.** Every clause of the Determination is either already expressed in v0.2, or extends it compatibly.

| Determination clause | v0.2 position | verdict |
|---|---|---|
| Exactly one active canonical per kind per production | `EGS-001 §7.1 U-1` · lifecycle `I-3` | **ALREADY EXPRESSED** |
| Promotion transfers authority | `EGS-001 §7.1 U-2` — successor promoted, incumbent's `active` computed false | **ALREADY EXPRESSED** |
| Incumbent becomes `SUPERSEDED` | lifecycle `§2.1`, `§1.2` | **ALREADY EXPRESSED** |
| Incumbent retains identity, hash, provenance, lineage, promotion history | `EGS-001 §7.4` append-only · lifecycle `P-5` no deletion · `§1.5` identity immutable | **ALREADY EXPRESSED** |
| Incumbent retains **discoverability** | **NOT EXPRESSED** | **UPDATE `S-3`** |
| Supersession shall not delete, rewrite provenance, alter hashes, mutate lineage | lifecycle `P-5` · `EGS-001 §7.4` | **ALREADY EXPRESSED** |
| Historical retrieval through lineage, promotion history, registry history, governed queries | **NOT EXPRESSED — no retrieval model exists** | **UPDATE `S-4`** |
| Historical authority not restored implicitly | lifecycle `P-3` — but `P-3` is **absolute** where this is **conditional** | **UPDATE `S-5`** |
| Version describes historical identity, never authority | `EGS-001 §4A` · lifecycle `§1.5` | **ALREADY EXPRESSED** |
| Consumers requesting a kind receive the active canonical **without ambiguity** | **NOT EXPRESSED — no resolution concept exists** | **UPDATE `S-6`** |
| Historical access explicit, canonical access implicit | **NOT EXPRESSED** | **UPDATE `S-6`** |
| Nine governing principles | 8 of 9 present; principle 6 *"Authority is singular"* is new as a stated principle | **UPDATE `S-7`** |

**Three of the four missing items are the same gap in different clothes: v0.2 defines what *is* canonical and never defines how anyone *asks*.** §4 below.

---

# 4 · REQUIRED SPECIFICATION UPDATES

**Eight. Each names the document, the section, and what changes. None is made here.**

## `S-1` · `EGS-001 §7.1.1` — discharge the departure

Replace the departure notice with a citation to the Determination. **`U-1` is unchanged in substance; only its justification changes** — from *"this specification chose"* to *"the Executive determined."*

## `S-2` · `EGS-001 §4A` and lifecycle `§1.5` — adopt the Determination's formulation

Add, verbatim: **"Version belongs to provenance. Authority belongs to governance."** Retain the existing bullets beneath it as the operative rules.

## `S-3` · `EGS-001 §7` and `§6.5` — discoverability of superseded artifacts

**New requirement.** The Determination guarantees that a superseded artifact retains *discoverability*. **v0.2 guarantees retention but never requires that a superseded artifact remain findable** — `§6.5` enumerates canonical artifacts, `N-1` violations, hash drift and orphaned entries. **A superseded artifact appears in none of those lists.**

Required: enumeration SHALL answer *"every artifact ever promoted for this kind and production, in promotion order, with its current standing."* **Retention without enumeration is a filing cabinet with no index**, and the platform has already learned that a record nothing can find is a record that goes stale unnoticed.

## `S-4` · `EGS-001` — a historical retrieval clause, new section

**New section required.** The Determination names four retrieval paths — lineage, promotion history, registry history, governed queries. **v0.2 defines none of them.**

The clause should state *what a retrieval must return and what it must never do* — never return a superseded artifact in response to an unqualified request, never present a superseded artifact without its standing, never require a consumer to interpret a path or filename to determine standing. **Mechanism stays out of scope.**

## `S-5` · lifecycle `P-3` — align with *"not restored implicitly"*

`P-3` currently reads: *"`SUPERSEDED → CANONICAL` SHALL NOT occur. A new promotion of the same bytes is a new entry citing the same `sha256`."*

The Determination reads: *"Historical authority SHALL NOT be restored **implicitly**."*

**These are compatible but not identical.** `P-3` forbids the *transition*; the Determination forbids *implicit* restoration and by implication permits explicit restoration — which `P-3`'s second sentence already provides as a new entry.

**Required: state the equivalence explicitly**, so no future reader concludes that `P-3` forbids what the Determination permits, or vice versa. Suggested: *"a superseded artifact regains canonical authority only by a new promotion entry, never by transition, and never implicitly."*

## `S-6` · `EGS-001` — a resolution clause, new section

**The most substantive gap.** The Determination states:

> *"Consumers requesting `PICTURE_LOCK` shall receive the active canonical artifact without ambiguity… Historical access is explicit. Canonical access is implicit."*

**v0.2 has no concept of a consumer request at all.** The register determines *what is canonical*; nothing defines *how anything asks*. Required clauses:

- an **unqualified request** by `artifact_kind` and `production` resolves to the single active canonical artifact, and to nothing else;
- an unqualified request that resolves to **zero or more than one** artifact SHALL fail shut — consistent with `WET-SPEC-GATE-001 §3`, where a non-conforming control artifact is treated as closed;
- a **historical request** SHALL be explicit and SHALL carry the standing of what it returns;
- **resolution SHALL NOT consult a path, filename or directory** — `N-5`.

**The second clause matters most.** `U-4` already says more than one active canonical is a defect that SHALL be enumerable. **Resolution is where that defect would otherwise become an arbitrary answer**, and an arbitrary answer to *"which is the picture lock?"* is the failure this platform exists to prevent.

## `S-7` · `EGS-001` — record the nine governing principles

Add the Determination's nine principles as a cited block. **Eight restate v0.2 rules; principle 6, *"Authority is singular,"* is the Determination's own contribution** and is the sentence `U-1` exists to enforce.

## `S-8` · `EGS-001 §1A` — define `artifact kind` and `production`

**This is my gap, and the Determination makes it load-bearing.**

**`U-1`'s uniqueness key is `(artifact_kind, production)`. Neither term is defined in `§1A`, and neither is defined anywhere in the repository** — verified: zero governed definitions of either.

**The entire authority model rests on a two-part key whose parts are undefined.** Two readings of *"artifact kind"* produce different platforms: if `CONDUCTOR_SCORE` and `CONDUCTOR_SCORE v1.1` are the same kind, there is one canonical score; if they are different kinds, there are two. **The Determination cannot be enforced until both terms are fixed**, and `§4B` below is why `production` is harder than it looks.

---

# 5 · TWO ITEMS NEEDING EXECUTIVE CLARIFICATION

**Neither is a contradiction. Both are places where the Determination's text admits two readings, and the readings differ materially.**

## 5.1 · Is a *production* the same thing as a *lineage*?

**The uniqueness key is per `production`. The repository's identity axis is `lineage`.**

```
lineage_status: PRODUCTION            AR2-0824.context.json
08_22_assembly_lock_status:
        SUPERSEDED_ASSEMBLY           CUSTODY_ALERT_001 amendment
```

**The live case makes the difference concrete.** The Approved Viewing Master carries `approval_status: APPROVED` — canonical — **while its lineage is `SUPERSEDED_ASSEMBLY`**, and the register raises this against itself:

> *"this register names an approved viewing master for a **superseded assembly**."*

| reading | consequence |
|---|---|
| **production = lineage** | 08-22 and 08-24 are different productions. **Both may hold a canonical viewing master simultaneously**, and the current `APPROVED` entry is not in conflict with a future 08-24 master |
| **production = the work** | 08-22 and 08-24 are one production. **The current `APPROVED` entry must be superseded** the moment an 08-24 master is designated, and `U-1` is violated in the interval between |

**Both are defensible. They are not the same platform**, and `ED-005` Master Picture Designation lands directly on this question. **Answering it before `ED-005` costs nothing; answering it afterwards may cost a re-designation.**

## 5.2 · The citation clause may pre-dispose `CF-001`

**The Determination states it does not resolve `CF-001`. One sentence may nonetheless decide it.**

> *"Existing citations remain valid for the artifact against which they were authored."*

**`CF-001` established, by timing and by text, that the 91 citations were authored against `c13df1f4…` — a file that appears zero times in the repository and has never been hashed, registered or declared.**

**Read one way, the sentence is a safe placeholder** — *whatever artifact `CF-001` determines they were authored against, they remain valid for it.* No disposition.

**Read the other way, it is a disposition** — *authoring provenance confers validity*, therefore the citations are valid against `c13df1f4`, therefore `RIDER_REGISTRY`'s declared source stays wrong and an unregistered file acquires standing by implication.

**The second reading would resolve `CF-001` in a Determination that says it does not resolve `CF-001`.**

**Recommended: amend the sentence to make the first reading explicit** — for example, *"remain valid for the artifact `CF-001` determines them to have been authored against."* **This is a wording change, not a substantive one**, and it costs nothing to make now.

---

# 6 · RATIFIED STANDARDS — NO CONTRADICTION

| standard | interaction | verdict |
|---|---|---|
| **`APPROVED_VIEWING_MASTER`** — *"EXACTLY ONE entry per production may carry status: APPROVED"* | The Determination generalises this rule from one artifact kind to all | **CONFIRMED, and the Determination's precedent** |
| **`ER-003`** — custody is not authority | *"Supersession transfers authority, never identity"* is the same distinction applied to time | **REINFORCED** |
| **`DOC-002`** — regenerate, never patch | *"Supersession SHALL occur by promotion, never by mutation"* | **REINFORCED** |
| **`WET-SPEC-GATE-001 §5`** — computed, never authored | `active` computed, not authored (`U-3`) | **CONSISTENT** |
| **`WET-SPEC-REPORT-001`** | Untouched; the Determination records no metric | **UNAFFECTED** |
| **`EPR-001 §2.3`** — an empty field remains empty | *"Silence is never approval"* — principle 5 | **CONSISTENT** |
| **`WET-REV-002`** — never a parallel system | The Determination creates no instrument | **UNAFFECTED** |
| **`EGS-001 §1B.2`** — no revision may reinterpret a ratified state | **The Determination fixes `CANONICAL`'s meaning *before* ratification.** Nothing is reinterpreted | **CONSISTENT** |

**`§1B.2` deserves a note.** The stability clause forbids reinterpreting a *ratified* state's meaning. **The Determination arrives while both drafts are `DRAFT` and no artifact has ever been classified under them** — so it fixes a meaning rather than changing one. **Had it arrived after ratification, principle 6 would have required a new state name.** The sequencing is correct and worth recording as such.

---

# 7 · WHAT THIS ASSESSMENT DOES NOT DO

- **It does not amend either specification.** The eight updates are proposals; both v0.2 drafts stand unchanged.
- **It does not assign a designation** to the Determination — §1 is a recommendation.
- **It does not resolve `CF-001`, `ED-002`, `ED-003`, `ED-004` or `ED-005`.**
- **It does not answer whether a production is a lineage** — §5.1 is the Executive's.
- **It does not implement anything.** No runtime, guard, generator, registry or artifact was touched.
- **It does not ratify anything.**

---

# 8 · CERTIFICATION

```
Determination assessed        Canonical Authority Model — Single Active Canonical
Model adopted                 Model A · exactly one active canonical per kind per production

Contradictions with v0.2      NONE
Contradictions with ratified
  standards                   NONE — 8 checked · 3 reinforced
Open item closed              EGS-001 §7.1.1 — U-1 confirmed as written
EGS-001A blocker              CLEARED

Specification updates required  8   S-1 … S-8
  of which new sections         2   historical retrieval (S-4) · resolution (S-6)
  of which my own gap           1   S-8 — artifact_kind and production undefined

Executive clarifications        2   is a production a lineage? (§5.1)
                                    does the citation clause pre-dispose CF-001? (§5.2)

Designation defect              1   ED-001 already in use, and committed

Specifications amended          NONE
Runtime / guards / generators   UNTOUCHED
Registries                      UNTOUCHED
Artifacts reclassified          NONE
Commits                         NONE
```

---

*Prepared in response to the EXECUTIVE DETERMINATION — Canonical Authority Model. Custody: MACHINE. Authority: NONE. No specification was amended, no artifact reclassified, no runtime component, guard, generator or registry modified, and no commit made. Nothing is ratified or determined by this document.*
