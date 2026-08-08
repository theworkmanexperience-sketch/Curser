# WET-SPEC-002
## Production Decision Record (PDR) Specification
**Version:** 0.2
**Status:** Draft for Pilot Exercise (not for ratification — see §11)
**Date:** 2026-08-06
**Owner:** W.E.I.C.P. Editorial Intelligence Initiative
**Classification:** Foundational Engineering Specification
**Drafting note (independence disclosure):** v0.2 was drafted by the independent AI reviewer that audited v0.1, at the Chairman's direction. Under the implementer-and-reviewer principle, v0.2 should receive review by a party other than its author before ratification. This disclosure is itself an instance of the practice required by §7 Rule 6.

---

### 0. Change Log — v0.1 → v0.2

| Change | Audit item | Type |
|---|---|---|
| Provenance classes aligned to ADR-003; `approved` removed; `confidence` added | C-2 | Blocking |
| Conditional rule CR-1: AI-assisted decisions require session-record evidence before leaving Draft | C-3 | Blocking |
| `evidence[].classification` (epistemic class) added | C-4 | Blocking |
| Conditional rule CR-2: content hash mandatory for file evidence at Locked; resolvable custody for non-file evidence | C-1 | Blocking |
| `timeline.timebase` added; timecode format defined | R-4 | Recommended |
| Conditional rule CR-3: Locked requires ≥1 human approval | R-6 | Recommended |
| `relationships[]` (typed) replaces `metadata.related_pdrs` | R-1 | Recommended |
| `record_revision` added; mutability posture defined (§6) | R-3 | Recommended |
| `generation` block added; `validation` restricted to post-generation verification | R-7 | Recommended |
| Governed `extensions` block added; DP-001 restated | Axis 3 | Recommended |
| Worked example cleaned: supersession claim removed, Suno moved out of validation, illustrative banner added | Axis 4 caution | Recommended |
| Optional `approvals[].gate` linkage to platform Gates 1–3 | R-5 | Recommended |
| `version` renamed `schema_version` for clarity against `record_revision` | R-3 | Editorial |

---

### 1. Purpose

This specification defines the canonical structure of a **Production Decision Record (PDR)** — the atomic unit of governed editorial decision-making within W.E.I.C.P. A PDR records what decision was made, why, from what evidence, what alternatives were rejected, under what rights, by whose approval, and in what current lifecycle state.

A PDR must be independently auditable: a third party holding the record and access to referenced custody must be able to reconstruct the decision without chat history, memoranda, or the original decision-makers.

---

### 2. Design Principle 001 (restated in v0.2)

> A Production Decision Record shall describe an editorial decision through a **stable, domain-neutral core** common to all editorial disciplines, plus **registered, namespaced extension blocks** carrying discipline-specific data. Domain-neutrality is achieved by extension points, not by prohibiting domain vocabulary. The core schema shall not require structural modification to admit a new discipline; a new discipline is admitted by registering an extension namespace and, where needed, a `decision_artifact.type` vocabulary entry.

Rationale: this is the platform's proven pattern (shoot.yaml registered block classes). The v0.1 formulation ("no domain vocabulary anywhere") would have forced discipline-specific facts into free-text notes, destroying auditability while preserving structural purity.

---

### 3. Taxonomy Dependency (explicit, unresolved)

PDR provenance and evidence classification use the ADR-003 vocabulary — **OBSERVED · DERIVED · INTERPOLATED · ENRICHED** — with confidence bands (HIGH ≥ 0.90, MODERATE ≥ 0.70, LOW ≥ 0.50, UNUSABLE below), plus one proposed extension:

- **GENERATED** — content created rather than captured or transformed from capture (e.g., an AI-generated cue, composed narration). *GENERATED is not yet part of ratified/proposed ADR-003 vocabulary. Its adoption requires an ADR-003 amendment or the canonical-taxonomy ADR (ADR-007 candidate). Until then, PDRs using GENERATED carry a pending-vocabulary dependency, recorded here so it cannot be forgotten.*

`approved` is removed from provenance entirely: approval is an act, recorded in `approvals`; lifecycle position is recorded in `status`. Neither is a property of how knowledge was produced.

---

### 4. Core Schema

```yaml
pdr:
  # ── Identity ─────────────────────────────────────────────
  id: string                     # Issued by the registry (PRS-001 is sole issuer); sequential, zero-padded (e.g., PDR-000003); never reused
  schema_version: string         # Schema this record conforms to (e.g., "0.2")
  record_revision: integer       # Increments on every persisted change to this record (see §6)
  created_at: datetime           # ISO 8601, UTC
  updated_at: datetime           # ISO 8601, UTC

  # ── Production Context ───────────────────────────────────
  production: string             # e.g., "Alpha RoundUp Part 1"
  production_unit: string        # Attribute only (e.g., "PU-003"); not a first-class object

  # ── Decision Artifact ────────────────────────────────────
  decision_artifact:
    type: string                 # From the registered type vocabulary (governed, extensible by registration; not a frozen enum)
    identifier: string           # e.g., "BLACKTOP HYPNOSIS"
    description: string          # Optional

  # ── Temporal Scope (conditional — see CR-4) ──────────────
  timeline:
    timebase:
      fps: number                # e.g., 29.97
      drop_frame: boolean
    in: string                   # HH:MM:SS:FF in the declared timebase
    out: string                  # HH:MM:SS:FF
    duration: string             # Optional, derived

  # ── Objective ────────────────────────────────────────────
  objective: string              # The editorial goal this decision serves

  # ── Evidence Layer ───────────────────────────────────────
  evidence:
    - id: string                 # e.g., EV-GPX-001
      type: string               # Format/source type: review_mp4 | voice_over | srt | gpx | graphics | session_record | document | other
      classification: string     # Epistemic class per §3: OBSERVED | DERIVED | INTERPOLATED | ENRICHED | GENERATED
      confidence: string         # HIGH | MODERATE | LOW | UNUSABLE (per §3 bands); optional numeric value
      reference: string          # Path, URI, or identifier
      content_hash: string       # SHA-256; see CR-2
      custody: string            # Platform custody pointer (registry entry, manifest block, archive location)
      notes: string              # Optional

  # ── Decision Analysis ────────────────────────────────────
  decision_analysis:
    selected:
      identifier: string
      selection_basis: string
    rejected:                    # Strongly recommended; rejection is first-class
      - identifier: string
        rejection_basis: string

  # ── Structured Rationale ─────────────────────────────────
  decision_rationale:
    primary_factors: [string]
    rejected_factors: [string]

  # ── Generation (how the artifact came to exist) ──────────
  generation:
    method: string               # e.g., "Suno AI" | "Human" | "Hybrid"
    tools: [string]              # Generation tools only — never validation tools
    session_evidence: [string]   # Evidence IDs of type session_record documenting the generation/selection reasoning (see CR-1)

  # ── Validation (post-generation verification ONLY) ───────
  validation:
    methods: [string]            # e.g., "Final Cut Pro timeline review" | "Human Approval" | "A/B Test"
                                 # A tool that created the artifact may not appear here in a generation role
    result: string               # Passed | Conditional | Failed
    notes: string

  # ── Provenance (of the decision artifact) ────────────────
  provenance:
    class: string                # Per §3: OBSERVED | DERIVED | INTERPOLATED | ENRICHED | GENERATED
    confidence: string           # HIGH | MODERATE | LOW | UNUSABLE
    sources: [string]            # Upstream sources or evidence IDs

  # ── Rights (first-class, reusable object) ────────────────
  rights:
    generator: string            # Tool or person that created the artifact
    account: string              # Account / tier in effect at generation time
    license_basis: string        # Legal / contractual basis
    attribution: string          # Required attribution text, if any
    commercial_use: boolean
    restrictions: string
    gate_clearance_ref: string   # Optional pointer to a gate1_clearances entry or equivalent
    notes: string

  # ── Outcome ──────────────────────────────────────────────
  outcome:
    status: string               # Applied | Pending Integration | Archived
    artifact_reference: string   # Resulting asset or timeline placement
    notes: string

  # ── Approvals ────────────────────────────────────────────
  approvals:
    - actor: string
      role: string               # e.g., Editor | Producer | Chairman
      decision: string           # Approved | Rejected | Conditional
      timestamp: datetime        # ISO 8601, UTC
      gate: string               # Optional platform gate reference: Gate-1 | Gate-2 | Gate-3
      independence_note: string  # Required when approver and ratifying authority are the same person (see §7 Rule 6)
      notes: string

  # ── Lifecycle Status (current state only) ────────────────
  status: string                 # Allowed values and all transitions are governed by WET-SPEC-003.
                                 # Direct mutation without a recorded transition is prohibited.
                                 # (Any illustrative state chains in prior drafts are non-binding;
                                 #  WET-SPEC-003 MUST include rejection and supersession terminal states.)

  # ── Relationships (typed; semantics governed by PRS-001) ─
  relationships:
    - pdr_id: string
      relation: string           # supersedes | superseded_by | depends_on | informs | conflicts_with

  # ── Extensions (governed, namespaced, registered) ────────
  extensions:
    # <registered_namespace>:    # e.g., soundtrack: { cue_energy: ..., key: ... }
    #   ...                      # Registration process mirrors shoot.yaml block classes;
                                 # unregistered namespaces render a record non-conformant

  # ── Metadata ─────────────────────────────────────────────
  metadata:
    tags: [string]
    notes: string
```

---

### 5. Validity Rules

**5.1 Required for any valid PDR (minimum viable record):**
`id` · `schema_version` · `record_revision` · `production` · `decision_artifact.type` · `decision_artifact.identifier` · `objective` · `decision_analysis.selected` · `provenance.class` · `status`

**5.2 Conditional rules:**

- **CR-1 — AI-assisted decisions require session evidence.** If `generation.method` or `provenance.class` indicates AI generation or assistance (including Hybrid), the record must contain at least one `evidence` entry of `type: session_record` with a resolvable `custody` pointer, referenced from `generation.session_evidence`, **before the record may leave Draft.**
- **CR-2 — Custody at Locked.** A record may not reach Locked status unless every evidence entry that references a file artifact carries a `content_hash`, and every non-file evidence entry (session records, interviews, statements) carries a resolvable `custody` pointer. A Locked PDR with placeholder custody values is invalid.
- **CR-3 — Human approval at Locked.** A record may not reach Locked status without at least one `approvals` entry with `decision: Approved` from a human actor. (Transition mechanics belong to WET-SPEC-003; this is a record-validity floor.)
- **CR-4 — Temporal scope is conditional on artifact type.** `timeline` (including `timebase`) is required for artifact types with timeline placement (soundtrack, edit, vfx, motion_graphic, color_grade, voice_over, and similar). For types without temporal placement (e.g., publish, licensing), `timeline` is omitted and the registered type vocabulary marks the type as non-temporal. "Equivalent temporal scope" language from v0.1 is retired.
- **CR-5 — Status mutation.** `status` changes only through transitions governed by WET-SPEC-003, each producing a recorded transition event. Direct mutation is prohibited.

**5.3 Strongly recommended for audit readiness:**
`evidence` (≥1 entry) · `decision_analysis.rejected` with bases · `decision_rationale` · `evidence[].classification` (required at Locked) · `rights.license_basis` · `approvals`

A record lacking Required fields is incomplete and must not advance beyond Draft.

---

### 6. Mutability Posture

- **Draft:** freely editable; `record_revision` increments on every persisted change.
- **Beyond Draft:** append-only revisions; every change increments `record_revision` and must be attributable (who, when).
- **Locked:** immutable. Correction occurs only by superseding: a new PDR carrying `relationships: [{pdr_id, relation: supersedes}]`, with the old record marked `superseded_by` via a governed transition.
- Full state semantics are WET-SPEC-003's; the mutability posture above is a property of the record itself and is normative here.

---

### 7. Governance Notes

1. **Status is not free-text** (unchanged from v0.1; see CR-5).
2. **Rejection recording is intentional** (unchanged). Engineering organizations learn more from rejected options than accepted ones.
3. **Evidence precedes decision** (unchanged), and in v0.2 evidence carries its own epistemic class and confidence so that ADR-003's principle does not stop at the PDR boundary.
4. **Rights are first-class** (unchanged), now with an optional bridge to the platform's ratified gate system (`rights.gate_clearance_ref`, `approvals[].gate`).
5. **Generation is not validation.** A tool that created an artifact may not be cited as having validated it. The two blocks are separate so the truthfulness rule is structural, not behavioral.
6. **Independence is disclosed, not pretended.** When the approver and the ratifying authority are the same person — the normal condition at current organizational scale — `approvals[].independence_note` records it. Disclosure of the limitation is the control.
7. **This specification defines the record only.** Registry, lineage semantics, indexing, and querying are PRS-001's; lifecycle transitions are WET-SPEC-003's.

---

### 8. Worked Example — ILLUSTRATIVE ONLY

> **This example is not PDR-000003 and supersedes nothing.** Values marked `TBD` must come from primary artifacts (the actual FCP timeline, the actual Suno session, real hashes) when the real record is populated. Populating from the ERB-RM-001 narrative is prohibited — that would launder a memorandum into a record.

```yaml
pdr:
  id: PDR-000003                      # TBD — registry-issued
  schema_version: "0.2"
  record_revision: 1
  created_at: "TBD"
  updated_at: "TBD"

  production: "Alpha RoundUp Part 1"
  production_unit: "PU-003"

  decision_artifact:
    type: "soundtrack"
    identifier: "BLACKTOP HYPNOSIS"
    description: "Cue bridging fuel stop into sustained highway rhythm"

  timeline:
    timebase: { fps: TBD, drop_frame: TBD }   # From the FCP project settings
    in: "TBD"                                  # HH:MM:SS:FF in that timebase
    out: "TBD"

  objective: "Transition from fuel stop into highway rhythm while maintaining documentary authenticity and avoiding generic biker tropes."

  evidence:
    - id: "EV-REVIEW-001"
      type: "review_mp4"
      classification: "DERIVED"        # Review cut derived from camera originals
      confidence: "HIGH"
      reference: "TBD"
      content_hash: "TBD"
      custody: "TBD"
    - id: "EV-GPX-001"
      type: "gpx"
      classification: "TBD"            # OBSERVED if raw track; INTERPOLATED/ENRICHED per ADR-003 if processed
      confidence: "TBD"
      reference: "TBD"
      content_hash: "TBD"
      custody: "TBD"
    - id: "EV-SESSION-001"
      type: "session_record"
      classification: "GENERATED"      # Pending-vocabulary dependency, §3
      reference: "TBD"                 # Exported session transcript or summary
      custody: "TBD"                   # Platform custody, not vendor-side only
      notes: "Cue-strategy and lyric development session (CR-1)."

  decision_analysis:
    selected:
      identifier: "BLACKTOP HYPNOSIS"
      selection_basis: "Matched narration gap, geography, and editorial pacing; supported observed highway transition without generic tropes."
    rejected:
      - identifier: "HIGHWAY GHOSTS"
        rejection_basis: "Overlapped narration; poor documentary fit."
      - identifier: "Documentary Cue A"
        rejection_basis: "Insufficient energy for highway segment."

  decision_rationale:
    primary_factors: ["narration_gap", "highway_transition", "geography", "editorial_pacing"]
    rejected_factors: ["generic_biker_theme", "repeated_hook"]

  generation:
    method: "Hybrid"
    tools: ["Suno"]
    session_evidence: ["EV-SESSION-001"]

  validation:
    methods: ["Final Cut Pro timeline review", "Human Approval"]   # Suno does not appear here (§7 Rule 5)
    result: "Passed"
    notes: "Human gate confirmed fit against source footage."

  provenance:
    class: "GENERATED"
    confidence: "HIGH"
    sources: ["EV-REVIEW-001", "EV-GPX-001", "EV-SESSION-001"]

  rights:
    generator: "Suno"
    account: "TBD"                     # Tier at generation time
    license_basis: "TBD"               # REQUIRES_SPECIALIST_REVIEW for commercial sufficiency
    attribution: "TBD"
    commercial_use: true
    restrictions: "TBD"
    gate_clearance_ref: "TBD"

  outcome:
    status: "Applied"
    artifact_reference: "TBD"

  approvals:
    - actor: "Antonio Workman"
      role: "Producer / Editor"
      decision: "Approved"
      timestamp: "TBD"
      gate: ""
      independence_note: "Approver is also ratifying authority (single-operator condition; §7 Rule 6)."
      notes: "Terminal human gate."

  status: "Draft"                      # A record with TBD custody cannot be Locked (CR-2)

  relationships: []

  extensions: {}                       # soundtrack namespace to be registered when discipline-specific fields are needed

  metadata:
    tags: ["soundtrack", "highway", "transition"]
    notes: ""
```

Note the example's own status is **Draft** — under CR-2 it cannot claim Locked while custody values are TBD. The v0.1 example claimed Locked with placeholders; v0.2 makes that structurally impossible to assert honestly.

---

### 9. Open Items for v0.3 (to be settled by the pilot exercise)

1. Whether GENERATED is ratified into the canonical taxonomy (ADR-003 amendment or ADR-007) — **must be settled before any PDR is Locked.**
2. Registered `decision_artifact.type` vocabulary — seed list and registration procedure.
3. First registered extension namespace (expected: `soundtrack`) — defined by what the two pilots actually need, not anticipated.
4. Minimum evidence requirements per artifact type.
5. Executable validator (JSON Schema + fixture tests in the repository) — conformance must become mechanical before freeze.
6. Whether `production` should be an identifier rather than a display name (registry concern; PRS-001 will decide, but pilots should note friction).

### 10. Related Specifications

- **PRS-001** — Production Registry Specification — *deferred until this schema is exercised.*
- **WET-SPEC-003** — Production Lifecycle Specification — *must include rejection and supersession terminal states.*

### 11. Path to Ratification

v0.2 (this document) → populate two pilot PDRs from primary artifacts (BLACKTOP HYPNOSIS, OUT HERE) → fold pilot findings into v0.3 → independent review of v0.3 by a party other than this draft's author → freeze → PRS-001.

**End of WET-SPEC-002 v0.2**
