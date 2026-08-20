# DIE-CONFORM-001 — Sprint 1 Kickoff Brief
## Governance Status
Document Type: Work Order (Implementation) · Issued By: Chairman, W.E.I.C.P. · Date: 2026-08-20
Authority: WET-SPEC-DIE-001 v0.2 (FROZEN — tag wet-spec-die-001-v0.2-frozen, commit 870ef07)
Target Environment: Claude Code channel

NOTE: The Chairman's full twelve-section brief is issued verbatim in the
Sprint 1 channel handoff. This custody record preserves its governing
skeleton plus the Engineering Addendum.

OBJECTIVE: Implement the first conforming Documentary Intelligence Engine.
Conformance to the frozen specification — not historical replay. Deviations
from the founding fixture SHALL carry categorized explanations (V-7).
DELIVERABLES: D1 DIE-X extractor · D2 DIE-R resolution engine · D3 registry
generator (all nine, immutable IDs) · D4 validation suite (V-1..V-7) ·
D5 machine-readable conformance report (requirement/status/evidence/
explanation; PASS | PASS WITH EXPLANATION | FAIL) · D6 fixture comparison
(differences: Expected | Explained | Specification-compliant | Failure —
no unexplained differences).
CONSTRAINTS: immutable observations · provenance preserved · DIE-X/DIE-R
separated · replay supported · deterministic validation · registry ownership
preserved · enrichment namespaces honored.
OUT OF SCOPE: NIE, MIE, PIE, themes, sentiment, cues, VO, publication.
GOVERNANCE: registry creation is internal; no emission authorized;
consent_status recorded at current known values (event_context_appearance
where policy is pending), never inferred upward.

## Engineering Addendum (accepted into this work order)
A1 GOVERNING HASH: WET-SPEC-DIE-001 v0.2 SHA-256
ca1933b22721fa55d65d40e81a3040a009e390d45d2e1a8df1a128ab3209bac5 at 546918b.
A2 FIXTURE CUSTODY: the founding fixture enters custody as a machine-readable
expected-values file (structural expectations and counts only — no verbatim
personal content pending the Sprint-2 consent ruling): docs/fixtures/
DIE_part2_expected.yaml. Ground Truth input pinned by local path + SHA-256
recorded in that file; full-detail comparison executes locally.
A3 CLOSURE: Sprint results and the conformance report return to the
governance channel for review; implementation lessons route to AIS-001
Rev A.
