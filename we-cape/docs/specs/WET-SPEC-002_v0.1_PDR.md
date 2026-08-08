# WET-SPEC-002
## Production Decision Record (PDR) Specification
**Version:** 0.1  
**Status:** Draft for Review  
**Date:** 2026-08-06  
**Owner:** W.E.I.C.P. Editorial Intelligence Initiative  
**Classification:** Foundational Engineering Specification

---

### 1. Purpose

This specification defines the canonical structure of a **Production Decision Record (PDR)**.

A PDR is the atomic unit of governed editorial decision-making within W.E.I.C.P. It records what decision was made, why it was made, what evidence supported it, what alternatives were rejected, the rights basis, and the current lifecycle state.

The PDR is intentionally domain-neutral. It must serve soundtrack decisions, motion graphics, narration, color grading, editing, sound design, visual effects, publishing, and any future editorial discipline without structural modification.

---

### 2. Design Principle 001

> A Production Decision Record (PDR) shall describe an editorial decision independently of any specific editorial discipline. The schema shall be equally applicable to soundtrack generation, graphics, narration, editing, color grading, sound design, visual effects, publishing, and future editorial domains without structural modification.

This principle is mandatory. Any field that embeds domain-specific vocabulary as first-class structure violates this specification.

---

### 3. Core Schema

```yaml
pdr:
  # Identity
  id: string                    # Unique PDR identifier (e.g., PDR-000003)
  version: string               # Schema version this record conforms to (e.g., "0.1")
  created_at: datetime
  updated_at: datetime

  # Production Context
  production: string            # Human-readable production name (e.g., "Alpha RoundUp Part 1")
  production_unit: string       # Attribute only (e.g., "PU-003"). Not a first-class object.

  # Decision Artifact (domain-neutral)
  decision_artifact:
    type: string                # e.g., "soundtrack" | "motion_graphic" | "color_grade" | "voice_over" | "edit" | "vfx" | "publish"
    identifier: string          # Human-readable name or title of the artifact (e.g., "BLACKTOP HYPNOSIS")
    description: string         # Optional short description

  # Temporal Scope
  timeline:
    in: string                  # Timecode or timestamp (e.g., "13:59:19")
    out: string                 # Timecode or timestamp (e.g., "16:37:02")
    duration: string            # Optional calculated duration

  # Objective
  objective: string             # Clear statement of the editorial goal this decision serves

  # Evidence Layer (separated from decision)
  evidence:
    - id: string                # Evidence identifier
      type: string              # e.g., "review_mp4" | "voice_over" | "srt" | "gpx" | "graphics" | "session_record" | "hash"
      reference: string         # Path, URI, or custody pointer
      content_hash: string      # Optional cryptographic hash
      custody: string           # Optional custody / platform reference
      notes: string             # Optional

  # Decision Analysis (includes failure recording)
  decision_analysis:
    selected:
      identifier: string
      selection_basis: string   # Why this option was chosen
    rejected:
      - identifier: string
        rejection_basis: string # Why this option was discarded
    # At least one selected entry is required. Rejected entries are strongly recommended.

  # Structured Rationale (machine-readable factors)
  decision_rationale:
    primary_factors:            # Factors that drove the selection
      - string
    rejected_factors:           # Factors that were considered and discarded
      - string

  # Validation
  validation:
    methods:                    # List of validation methods applied
      - string                  # e.g., "Suno" | "Final Cut Pro" | "Human Review" | "A/B Test"
    result: string              # e.g., "Passed" | "Conditional" | "Failed"
    notes: string

  # Provenance Classification
  provenance:
    class: string               # "observed" | "derived" | "generated" | "approved"
    sources:                    # Optional list of upstream sources
      - string
    generation_method: string   # e.g., "Suno AI" | "Human" | "Hybrid"

  # Rights Object (standalone, reusable)
  rights:
    generator: string           # Tool or person that created the artifact
    account: string             # Account / tier used (if applicable)
    license_basis: string       # Legal / contractual basis
    attribution: string         # Required attribution text (if any)
    commercial_use: boolean
    restrictions: string        # Any known restrictions
    notes: string

  # Outcome
  outcome:
    status: string              # e.g., "Applied" | "Pending Integration" | "Archived"
    artifact_reference: string  # Pointer to the resulting asset or timeline placement
    notes: string

  # Approvals
  approvals:
    - actor: string
      role: string              # e.g., "Editor" | "Producer" | "Chairman"
      decision: string          # "Approved" | "Rejected" | "Conditional"
      timestamp: datetime
      notes: string

  # Lifecycle Status (current state only — transitions are governed by WET-SPEC-003)
  status: string                # Current lifecycle state (see WET-SPEC-003)
  # Allowed values will be defined in WET-SPEC-003. Example progression:
  # Created → Draft → Evidence Complete → Under Review → Validated → Approved → Locked → Archived

  # Optional Metadata
  metadata:
    tags: [string]
    related_pdrs: [string]      # Cross-references to other PDRs
    notes: string
```

---

### 4. Required vs Optional Fields

**Required for a valid PDR (minimum viable record):**
- `id`
- `production`
- `decision_artifact.type`
- `decision_artifact.identifier`
- `timeline.in` and `timeline.out` (or equivalent temporal scope)
- `objective`
- `decision_analysis.selected`
- `status`

**Strongly Recommended (should be present for audit readiness):**
- `evidence` (at least one entry)
- `decision_analysis.rejected` (with rejection_basis)
- `decision_rationale`
- `provenance.class`
- `rights.license_basis`
- `approvals`

**Optional:**
- All other fields

A record that lacks the Required fields is incomplete and must not be advanced beyond Draft status.

---

### 5. Example: BLACKTOP HYPNOSIS (Illustrative)

```yaml
pdr:
  id: PDR-000003
  version: "0.1"
  created_at: "2026-07-XXT00:00:00Z"   # placeholder — replace with actual
  updated_at: "2026-08-06T00:00:00Z"

  production: "Alpha RoundUp Part 1"
  production_unit: "PU-003"

  decision_artifact:
    type: "soundtrack"
    identifier: "BLACKTOP HYPNOSIS"
    description: "Cue bridging fuel stop into sustained highway rhythm"

  timeline:
    in: "13:59:19"
    out: "16:37:02"

  objective: "Transition from fuel stop into highway rhythm while maintaining documentary authenticity and avoiding generic biker tropes."

  evidence:
    - id: "EV-REVIEW-001"
      type: "review_mp4"
      reference: "..."                 # custody pointer or path
      content_hash: "..."              # if available
    - id: "EV-VO-001"
      type: "voice_over"
      reference: "..."
    - id: "EV-SRT-001"
      type: "srt"
      reference: "..."
    - id: "EV-GPX-001"
      type: "gpx"
      reference: "..."

  decision_analysis:
    selected:
      identifier: "BLACKTOP HYPNOSIS"
      selection_basis: "Matched narration gap, geography, and editorial pacing; supported observed highway transition without generic tropes."
    rejected:
      - identifier: "HIGHWAY GHOSTS"
        rejection_basis: "Overlapped narration and poor documentary fit."
      - identifier: "Documentary Cue A"
        rejection_basis: "Insufficient energy for highway segment."
      - identifier: "Documentary Cue B"
        rejection_basis: "Thematic mismatch with observed location."

  decision_rationale:
    primary_factors:
      - "narration_gap"
      - "highway_transition"
      - "geography"
      - "editorial_pacing"
    rejected_factors:
      - "generic_biker_theme"
      - "repeated_hook"

  validation:
    methods:
      - "Suno"
      - "Final Cut Pro"
      - "Human Approval"
    result: "Passed"
    notes: "Human gate confirmed fit after review against source footage."

  provenance:
    class: "generated"
    generation_method: "Suno AI + Human Selection"
    sources:
      - "Observed location audio/visual"
      - "Narration track"

  rights:
    generator: "Suno"
    account: "..."                     # tier / account identifier
    license_basis: "..."               # contractual basis
    attribution: "..."
    commercial_use: true
    restrictions: "..."
    notes: ""

  outcome:
    status: "Applied"
    artifact_reference: "..."          # timeline placement or asset path
    notes: ""

  approvals:
    - actor: "Antonio Workman"
      role: "Producer / Editor"
      decision: "Approved"
      timestamp: "2026-07-XXT00:00:00Z"
      notes: "Terminal human gate."

  status: "Locked"                     # subject to WET-SPEC-003 transition rules

  metadata:
    tags: ["soundtrack", "highway", "transition"]
    related_pdrs: []
    notes: "First full PDR created under WET-SPEC-002 v0.1. ERB-RM-001 narrative is superseded by this record."
```

---

### 6. Governance Notes

1. **Status is not free-text.** The `status` field holds only the current state. All state changes must occur through governed transitions defined in WET-SPEC-003. Direct mutation of status without a recorded transition event is prohibited.

2. **Rejection recording is intentional.** Engineering organizations learn more from rejected options than from accepted ones. Capturing `rejection_basis` creates durable editorial intelligence.

3. **Evidence precedes Decision.** The schema deliberately separates the evidence layer from the decision layer so that later automation and audit can inspect supporting materials independently of the conclusion.

4. **Rights are first-class.** Rights metadata is treated as a reusable object so the same structure can be applied across every editorial domain.

5. **This specification defines the record only.** Indexing, lineage relationships, version history across records, and query behavior are deferred to PRS-001 (Production Registry Specification).

---

### 7. Open Items for v0.2

- Finalize exact allowed values for `decision_artifact.type`
- Finalize exact allowed values for `provenance.class`
- Decide whether `content_hash` is mandatory for Locked status
- Define minimum evidence requirements per artifact type (if any)
- Align datetime and timecode formats with platform standards
- Confirm ID generation scheme (sequential vs UUID vs hybrid)

---

### 8. Related Specifications

- **PRS-001** — Production Registry Specification (relationships, indexing, lineage, querying) — *deferred until this schema is exercised*
- **WET-SPEC-003** — Production Lifecycle Specification (state machine and governed transitions) — *next after initial population*

---

**End of WET-SPEC-002 v0.1**
