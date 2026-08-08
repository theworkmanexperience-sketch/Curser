# WET-SPEC-002
## Production Decision Record (PDR) Specification
**Version:** 0.3
**Status:** Draft for Final Independent Review (freeze candidate — see §11)
**Date:** 2026-08-07
**Owner:** W.E.I.C.P. Editorial Intelligence Initiative
**Classification:** Foundational Engineering Specification
**Drafting note (independence disclosure):** v0.2 and v0.3 were drafted by the independent AI reviewer that audited v0.1. Per §11, the final review before freeze must be performed by a party other than this author.

---

### 0. Change Log — v0.2 → v0.3

| Change | Origin | Type |
|---|---|---|
| `timeline.placements[]` replaces single in/out — cues may be placed multiple times | PF-2 (PDR-000004: 3 placements) | Structural |
| Rational time recorded as the OBSERVED value; timecode fields explicitly DERIVED | PF-3 (audio-sample-aligned edits are not frame-exact) | Structural |
| Temporal-scope requirement binds at **Locked**, not Draft (CR-4 restated) | PF-1 (honest Drafts could not carry in/out yet) | Rule |
| §6a Interim Transition Record + `transitions[]` block; CR-5 restated to require a transition chain | Locking chicken-and-egg vs. unwritten WET-SPEC-003 | Rule |
| `evidence[].coverage_period` added (what time span the evidence proves) | EV-SUB series (subscription/entitlement evidence) | Structural |
| §3 taxonomy now cites ADR-007 (canonical taxonomy incl. GENERATED); pending-vocabulary language resolves on ADR-007 ratification | ADR-007 draft | Governance |
| Validator updated to v0.3 (schema + rules + fixtures) | R-2 continuity | Tooling |

Records at `schema_version: "0.2"` remain valid v0.2 records; new records use "0.3". The two pilot PDRs migrate to 0.3 at their Locking revision.

---

### 1. Purpose

Unchanged from v0.2: this specification defines the Production Decision Record — the atomic unit of governed editorial decision-making. A PDR must be independently auditable: a third party holding the record and access to referenced custody must be able to reconstruct the decision without chat history, memoranda, or the original decision-makers.

### 2. Design Principle 001

Unchanged from v0.2 (restated form): a stable, domain-neutral core plus registered, namespaced extension blocks. Neutrality by extension points, not by prohibiting domain vocabulary.

### 3. Taxonomy

Provenance and evidence classification use the **canonical taxonomy defined by ADR-007**: OBSERVED · DERIVED · INTERPOLATED · ENRICHED · GENERATED, with confidence bands HIGH ≥ 0.90 / MODERATE ≥ 0.70 / LOW ≥ 0.50 / UNUSABLE. Conclusions derived from evidence are labeled DERIVED with the derivation stated in the record. **ADR-007 ratification is a prerequisite to any Locked status** (PD-001 exit criterion X-4).

### 4. Core Schema (v0.3 — changed blocks shown in full; unchanged blocks noted)

```yaml
pdr:
  # Identity — unchanged from v0.2 (id, schema_version: "0.3", record_revision, created_at, updated_at)
  # Production Context — unchanged (production, production_unit)
  # Decision Artifact — unchanged (type from registered vocabulary, identifier, description)

  # ── Temporal Scope (CHANGED: multi-placement; conditional per CR-4) ──
  timeline:
    timebase:
      fps: number                # e.g., 24
      drop_frame: boolean
    placements:
      - lane: integer            # NLE lane/track (negative = audio lanes in FCPXML convention)
        in_rational: string      # OBSERVED value, exact rational seconds (e.g., "50381/60s")
        out_rational: string     # OBSERVED
        in_tc: string            # DERIVED HH:MM:SS:FF at the declared timebase
        out_tc: string           # DERIVED
        duration_s: string       # OBSERVED or derived; state which
        source_evidence: string  # Evidence ID of the placement authority (e.g., the FCPXML)

  # Objective — unchanged
  # ── Evidence Layer (CHANGED: coverage_period added) ──
  evidence:
    - id: string
      type: string               # review_mp4 | voice_over | srt | gpx | graphics | session_record | document | other
      classification: string     # ADR-007 canonical class
      confidence: string         # ADR-007 band
      reference: string
      content_hash: string       # SHA-256; CR-2
      custody: string
      coverage_period:           # OPTIONAL — what time span this evidence proves
        from: string             # ISO 8601 date
        to: string
      notes: string

  # Decision Analysis — unchanged (selected + rejected[] with bases)
  # Decision Rationale — unchanged
  # Generation — unchanged (method, tools, session_evidence; CR-1)
  # Validation — unchanged (post-generation verification only; §7 Rule 5)
  # Provenance — unchanged (ADR-007 class + confidence + sources)
  # Rights — unchanged (incl. gate_clearance_ref)
  # Outcome — unchanged
  # Approvals — unchanged (incl. gate, independence_note)

  # ── Lifecycle (CHANGED: transition chain is now part of the record) ──
  status: string                 # Current state only. Allowed-state graph remains WET-SPEC-003's;
                                 # until 003 exists, §6a governs how states change.
  transitions:
    - from: string
      to: string
      actor: string              # Human actor authorizing the transition
      timestamp: datetime        # ISO 8601 UTC
      basis: string              # Why the transition is valid (criteria satisfied)
      evidence_refs: [string]    # Evidence IDs supporting the basis

  # Relationships — unchanged (typed)
  # Extensions — unchanged (governed, namespaced, registered)
  # Metadata — unchanged
```

### 5. Validity Rules

**5.1 Required minimum** — unchanged from v0.2, plus: `transitions` must be present (empty list permitted only while status is the initial Draft).

**5.2 Conditional rules:**

- **CR-1** (unchanged): AI-assisted decisions require session-record evidence with resolvable custody, referenced from `generation.session_evidence`, before leaving Draft.
- **CR-2** (unchanged): Locked requires real content hashes on file evidence, resolvable custody on non-file evidence, and `classification` on every evidence entry.
- **CR-3** (unchanged): Locked requires ≥1 human approval with decision Approved.
- **CR-4 (restated per PF-1):** for artifact types with timeline placement, `timeline` (timebase + ≥1 placement) is required **at Locked**. A Draft may honestly omit placements not yet in custody. Non-temporal types omit `timeline` at all stages.
- **CR-5 (restated):** any status other than the initial Draft requires an unbroken `transitions` chain from Draft to the current status, each entry per §6a. Direct status mutation without a chain entry renders the record non-conformant.

**5.3 Strongly recommended** — unchanged; add `coverage_period` on any entitlement, subscription, or time-scoped evidence.

### 6. Mutability Posture

Unchanged from v0.2: Draft freely editable with `record_revision` increments; append-only beyond Draft; Locked immutable except by supersession via typed relationships.

### 6a. Interim Transition Record (until WET-SPEC-003)

WET-SPEC-003 will define the full state graph and transition governance. Until it is ratified, the following minimal rule is normative so that records are not blocked from Locking by an unwritten specification:

1. A transition is performed by a named human actor and appended to `transitions` with from, to, actor, timestamp, basis, and evidence_refs.
2. A transition to **Locked** is valid only when CR-2, CR-3, and CR-4 are satisfied and ADR-007 is ratified; the basis field must say so and evidence_refs must cite the satisfying evidence.
3. Rejection and supersession are legal transition targets now (states `Rejected`, `Superseded`); WET-SPEC-003 inherits and may refine them but may not remove them.
4. When WET-SPEC-003 is ratified, chains recorded under this section remain valid history; 003 governs transitions from that point forward.

### 7. Governance Notes

Rules 1–7 unchanged from v0.2 (status not free-text; rejection first-class; evidence precedes decision; rights first-class with gate bridge; generation ≠ validation; independence disclosed; record-only scope). One addition:

8. **Evidence proves a span, not a feeling of coverage.** Where evidence is time-scoped (subscriptions, terms, certifications), record `coverage_period` and derive coverage conclusions explicitly (ADR-007 rule 3). Exercised precedent: EV-SUB-010.

### 8. Worked Example

The v0.2 illustrative example is retired. **The exercised pilot records are the reference examples**: PDR-000003 (multi-evidence, supersession of a version, derived coverage conclusion) and PDR-000004 (multi-placement, in-progress honesty, empty-approvals discipline), at `records/pdr/`. A specification whose examples are real records is the point of the pilot.

### 9. Open Items for v1.0 Freeze Review

1. Registered `decision_artifact.type` seed vocabulary — confirm the pilot list (soundtrack, edit, vfx, motion_graphic, color_grade, voice_over, publish, licensing) and the registration procedure.
2. First registered extension namespace (`soundtrack`) — confirm whether the pilots needed one (to date: no; core sufficed).
3. Validator v0.3 adopted into the repository with CI execution.
4. Disposition of PF-1/2/3 confirmed by the independent reviewer of this draft.

### 10. Related Specifications

- **PRS-001** — registry; core requirements from the pilot: registry-issued immutable evidence IDs with versions/checksums; coverage_period as first-class attribute; sole issuer of PDR IDs.
- **WET-SPEC-003** — lifecycle; inherits §6a chains and the Rejected/Superseded terminal states; must not define a success-only state graph.

### 11. Path to Freeze

This draft (v0.3) → exit criteria X-1..X-5 of PD-001 complete (pilots Locked under §6a) → any resulting defects folded in → **final independent engineering review by a party other than this draft's author** → freeze as v1.0, with the freeze record citing the two Locked PDR IDs, revision counts, validator result, and PF dispositions.

**End of WET-SPEC-002 v0.3**
