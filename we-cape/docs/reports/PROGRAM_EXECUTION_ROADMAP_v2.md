# PROGRAM EXECUTION ROADMAP v2

**Issued under:** EXECUTIVE ORDER `EO-WET-EXEC-017` — Program Roadmap Revision, Executive Producer / Chairman, 2026-08-30
**Prepared by:** Governance Compliance Auditor · **Custody:** `MACHINE` · **Authority:** NONE
**Repository:** READ ONLY at `b4d8529` · **Implementation:** NOT AUTHORIZED · **Commits:** none

> **This is an execution roadmap. It is not an authorization.** No stage below is authorized by this document. Each stage names the instrument that would have to authorize it.

> **Note on "replace."** `EO-WET-EXEC-017` directs that this document *replace the previous roadmap.* **No roadmap document exists in the repository.** The prior sequence existed only as an Executive message in session. **v2 therefore supersedes an uncommitted predecessor, and this is its first repository-shaped statement.** Recorded rather than assumed. `[E]`

---

# 0 · WHAT CHANGED AND WHY

| v1 | v2 | authority |
|---|---|---|
| Stage 2 — Ratification *and* `ED-002`…`ED-005` | **split into 2A Governance Ratification and 2B Production Determinations** | `EO-017` Finding 2 |
| *(absent)* | **Stage 3 — Specification Finalization** | `EO-017` Finding 3 |
| Stage 3 — "lift the generator lock when prerequisites are met" | **superseded.** Lock state is contradictory; remediation is the real stage | `EO-017` Finding 1 · Finding 4 |
| *(absent)* | **Stage 4 — Generator Remediation** (engineering) | `EO-017` Finding 4 |
| Stage 4 — conform to *the certified baseline* | **conform to the *ratified* specifications** | `EO-017` Finding 5 |
| Stage 5 — "resume" production | **Stage 6 — Production Activation**, gated on all five predecessors | `EO-017` Finding 6 |
| `ED-002` listed as an Executive decision | **reclassified** — see §8 | `EO-017` Clarification |

**Two structural corrections underlie the rest.** Governance ratification and production determinations were entangled and are now independent. And the roadmap named no stage for the only work that is engineering — which is the work that actually stands between the platform and a processed frame.

---

# 1 · STAGE 1 — GOVERNANCE BASELINE · **COMPLETE** `[E]`

| | |
|---|---|
| Authority | `EO-WET-EXEC-015` certification · `EO-WET-EXEC-016` custody |
| Evidence | commit `b4d8529`, pushed; 19 documents + `BASELINE_MANIFEST.md` |
| State | **COMPLETE** — 19 of 19 under repository custody, byte-verified |
| Status of artifacts | `CERTIFIED — NOT YET RATIFIED` |

**Residual items** are recorded in `GO-001` (drafted, not filed) and are `NO ACTION REQUIRED`.

---

# 2 · STAGE 2A — GOVERNANCE RATIFICATION

**Class: GOVERNANCE.** Executive acts on the governance corpus. **No production fact is decided here.**

| # | item | current state | evidence |
|---|---|---|---|
| 2A-1 | **`A-8b` — adopt the `Artifact kind` definition** | `REQUIRES EXECUTIVE ADOPTION` | `RATIFICATION_TRACEABILITY_MATRIX` — the one amendment whose wording did not originate with the Executive |
| 2A-2 | **`GD-01` disposition** | **OPEN · HIGH** | `CAR-003 GD-01`: four referenced ADRs absent — *"this repository cannot resolve its own governance references"* |
| 2A-3 | **ADR designation** | recommended `ADR-012`, **not assigned** | `CAM-002` §5.2 |
| 2A-4 | **Ratify `EGS-001` and `ARTIFACT_LIFECYCLE_SPECIFICATION`** | `CERTIFIED — NOT YET RATIFIED` | `CAM-002` §1.6 |

**Ordering constraint, from the committed corpus.** `CAM-002` §5.2 makes `GD-01` a **condition** on the designation: *"Either close `GD-01` first, or record the series' state inside the ADR. Filing silently into the series as though it were sound is the one disposition not recommended."* **`2A-2` therefore precedes or is discharged within `2A-3`.** `[E]`

**Exit condition:** all four items disposed. **Nothing in 2A depends on any production determination.**

---

# 3 · STAGE 2B — PRODUCTION DETERMINATIONS

**Class: EXECUTIVE DECISION.** These determine production truth. **They are independent of Stage 2A and may run concurrently with it.**

| # | item | state | blocked on |
|---|---|---|---|
| 2B-1 | **`CF-001` — Citation Provenance** | `UNRESOLVED — REQUIRES EXECUTIVE DETERMINATION` · **CRITICAL** | nothing — decidable now |
| 2B-2 | **`ED-003` — Picture Lock Designation** | `READY WITH CONDITIONS` | nothing — decidable now |
| 2B-3 | **`ED-004` — Caption Collapse Rule** | `READY WITH CONDITIONS` | **`CF-001`** |
| 2B-4 | **`ED-005` — Master Picture Designation** | `NOT READY` | `ED-003` · and it is now **also a supersession** |

**Internal dependency, evidenced.** `ED-004` cannot be determined while the authoritative caption stream is unidentified — `CF-001` records that the 91 governed citations resolve against `c13df1f4` (0 repository references) rather than the declared `89d61f96` (70 references). **`CF-001` is the head of this stage.** `[E]`

**One consequence recorded in advance, not discovered later.** `CAM-002` §3.2: the 08-22 assembly and the 08-24 lineage are **the same production**, so designating an 08-24 viewing master **supersedes the current one**. `ED-005` is a designation *and* a supersession and should issue as one instrument. `[E]`

---

# 4 · STAGE 3 — SPECIFICATION FINALIZATION

**Class: GOVERNANCE.** **No implementation occurs in this stage.**

**The repository holds `EGS-001` v0.2, `ARTIFACT_LIFECYCLE_SPECIFICATION` v0.2, and two redline packages. It does not hold v1.0 of either.** `[E]`

Per `EO-WET-EXEC-017` Finding 3 and `DOC-002` — *regenerate, never patch* — v1.0 of each is a **regenerated governed artifact**, produced from the ratified redlines. **Detail in `SPECIFICATION_FINALIZATION_PLAN.md`.**

| | |
|---|---|
| Entry condition | Stage 2A complete — the redlines are ratified, `A-8b` adopted |
| Output | `EGS-001` **v1.0** · `ARTIFACT_LIFECYCLE_SPECIFICATION` **v1.0**, both `RATIFIED` |
| Authorization required | a commit authorization; `EO-017` grants none |

**Why this stage cannot be skipped.** Stage 5 measures conformance against the **ratified** specification. Conforming to v0.2 would measure against the pre-amendment text — **11 packaged amendments would go unenforced, including `A-8b`, which is what makes authority uniqueness do any work.** `[E]`

---

# 5 · STAGE 4 — GENERATOR REMEDIATION

**Class: ENGINEERING.** **Not governance. Not an Executive Determination. Unauthorized until separately approved.**

**Detail in `GENERATOR_REMEDIATION_PLAN.md`.** The work is enumerated by `GER-001` §3, which states plainly: *"**Item 5 is a code change to a governed generator**… It is engineering work and it is not authorized by any Order to date."* `[E]`

| | |
|---|---|
| Entry condition | Stage 3 complete · **and** the `RUN_ID` lock state determined — §7 |
| Scope | parameterise `SHA` `LOCK` `SEG` `CUES` `RUN_ID`; remove hard-coded assembly and superseded-segment assumptions; ingestion readiness |
| Blocking exceptions closed | `GE-1` `GE-2` `GE-3` `GE-4` `GE-5` |
| Authorization required | a separate Executive Order |

---

# 6 · STAGE 5 — CONFORMANCE VERIFICATION

**Class: VERIFICATION.** **No governance redesign occurs here.**

**Measured against the *ratified* specifications produced by Stage 3 — not against the certified baseline.** These are different documents; see §4. `[E]`

| surface measured | current recorded state |
|---|---|
| **Runtime** | `runtime_guards.py` `23e2b841d8b0` · `G-12` admits one mode · `G-09` tests `b < a` |
| **Generators** | `gen_artifacts_v2.py` `f4ce0f6259d6` · unmodified |
| **Guards** | `G-01`…`G-13` |
| **Registries** | `APPROVED_VIEWING_MASTER.yaml` `600e357db71b` · one approved master |
| **Generated artifacts** | none emitted — `GER-001` §6: `artifacts emitted NONE` |

**Return path, already governed.** A conformance failure caused by an **ambiguous specification** rather than by the implementation reopens design only under `EO-WET-EXEC-014`'s single exception: *"Only documented contradictions may reopen design."* **The backward edge exists, is narrow, and is not a redesign licence.** `[E]`

---

# 7 · THE LOCK — RESOLVED AS A DEPENDENCY, NOT AS A STAGE

**v1 Stage 3 assumed the generator lock release was outstanding work. `LOCK_RECONCILIATION_REVIEW.md` finds:**

```
Lock instruments      1 — EVIDENCED
Lock state            GOVERNANCE CONTRADICTION — EXECUTIVE DETERMINATION REQUIRED
                      8 committed artifacts record HELD · 1 records RELEASED
Release condition     1 of 2 evidenced satisfied · 1 UNDETERMINABLE
```

**The lock is therefore not a stage. It is a determination that gates Stage 4.** `GER-001` §6, committed: *"The lock is released and the door behind it does not open onto the governed production."* **Whichever way the contradiction resolves, `GE-1`…`GE-5` still stand between the lock and a running generator.** `[E]`

**Recorded as `ED-006`** in `EDR-001` §6 — `NOT READY`, *"1 of 8 prerequisites satisfied, or 0 of 2 under the Order in force."*

---

# 8 · `ED-002` — RECLASSIFIED

Per `EO-WET-EXEC-017`, and replacing every earlier characterization of `ED-002` as a decision awaiting disposition:

> **`ED-002` is `NOT READY FOR EXECUTIVE DETERMINATION` because its prerequisite governing specification does not yet exist. The Executive determination occurs only after the specification is authored and reviewed.**

**`ED-002` appears in no stage of this roadmap.** Authoring that specification is unassigned work and is not authorized by any instrument to date. `[O]`

---

# 9 · STAGE 6 — PRODUCTION ACTIVATION

**Entry condition: Stages 2A, 2B, 3, 4 and 5 all complete.** Only then may the **08-24 lineage** and **Alpha RoundUp Day 3** enter governed production.

**One correction to the v1 wording.** v1 said *resume*. **The 08-24 lineage was never closed:** `ED-001` Phase 1 records **1 of 5 objectives COMPLETE**, four blocked — the ETC artifact, the generator lock, the ingestion chain, and lineage closure. Objective 1's producer gap was closed at `1552e42`, but the artifact was not produced, because the 08-24 picture lock is undesignated (`ED-003`, Stage 2B). **Production activation opens a phase that never began; it does not resume one that paused.** `[E]`

---

# 10 · DEPENDENCY SUMMARY

**Revised under `EO-WET-EXEC-017A` — Program Dependency Clarification.** Stages 2A and 2B are **independent in authority and partially ordered in execution**: no edge runs between them, and both converge before Specification Finalization.

```
Stage 1  Governance Baseline          COMPLETE
   │
   ├─────────────────────────┬──────────────────────
   ▼                         ▼
Stage 2A                  Stage 2B          (parallel Executive workstreams
Governance Ratification   Production         — NO edge between them)
GD-01 → ADR-012           Determinations
      → ratify both       CF-001 → ED-004
        specifications    ED-003 → ED-005
   │                         │
   └────────────┬────────────┘
                ▼                             ← CONVERGENCE
Stage 3  Specification Finalization           EGS-001 v1.0 · Lifecycle v1.0
                ▼
      ED-006 lock determination               ← GATE, not a stage
                ▼
Stage 4  Generator Remediation                ENGINEERING · separately authorized
                ▼
Stage 5  Conformance Verification             against RATIFIED specs
                ▼
Stage 6  Production Activation                08-24 lineage · Alpha RoundUp Day 3
```

**Critical path — three heads, all Executive acts:** `CF-001` → `ED-004`; `ED-003` → `ED-005`; `GD-01` → `ADR-012` → ratification → v1.0 regeneration. **None is blocked by missing evidence; all three are blocked only on determination.**

## 10.1 · Execution Note — legend

> **Execution Note:** *Stage 3 is scheduled after completion of both Stage 2A and Stage 2B as an Executive governance policy. This sequencing is not an input dependency. Specification Finalization consumes only Stage 2A outputs.*
>
> — adopted verbatim from the Executive Assessment of `EO-WET-EXEC-017A`, Finding 1.

**The four inputs to Specification Finalization, for the avoidance of doubt:** the v0.2 source specification, the ratified redline package, the adopted `A-8b` text, and the confirmed designation. **All four are Stage 2A outputs.** `CF-001`, `ED-003`, `ED-004` and `ED-005` feed the generator, not the specification. See `PROGRAM_DEPENDENCY_DIAGRAM.md` Rev A §4.2.

---

# 11 · ACCEPTANCE CRITERIA — `EO-WET-EXEC-017`

| # | criterion | result |
|---|---|---|
| 1 | Preserve the Governance Architecture | **MET** — no architectural statement altered |
| 2 | Preserve the architecture freeze | **MET** — `EO-WET-EXEC-014` intact; one documented contradiction reported, not resolved |
| 3 | Resolve the Stage 3 dependency ambiguity | **MET** — reconciled to a determination gating Stage 4; §7 |
| 4 | Separate governance from production determinations | **MET** — Stages 2A and 2B, independent |
| 5 | Introduce Specification Finalization as its own stage | **MET** — Stage 3 |
| 6 | Introduce Generator Remediation as its own engineering stage | **MET** — Stage 4 |
| 7 | Maintain traceability to committed governance artifacts | **MET** — every state cites a committed artifact |
| 8 | Authorize no implementation | **MET** — no commit, no code, no lock change |

---

```
PROGRAM EXECUTION ROADMAP v2         READ-ONLY

Stages                  6   ·   1 complete   ·   5 outstanding
Classes                 GOVERNANCE · EXECUTIVE DECISION · ENGINEERING ·
                        VERIFICATION · PRODUCTION
Gates                   1   ·   ED-006 lock determination
Open contradictions     1   ·   RUN_ID lock state
Acceptance criteria     8 of 8 MET

Architecture            FROZEN — EO-WET-EXEC-014 intact
Repository              READ ONLY at b4d8529   ·   clean
Implementation          NOT AUTHORIZED
```

---

*Prepared under `EO-WET-EXEC-017`. Custody: `MACHINE`. Authority: NONE. No specification was amended, no artifact reclassified, no lock state changed, no runtime component, guard, generator or registry modified, and no commit made.*
