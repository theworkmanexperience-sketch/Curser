# IAR-001 — Reviewer Instruction Sheet
## Governance Status
Document Type: Procedural Instruction (Informational) · Normative Authority: None
Ratification Status: Not Ratified · Routing: Permanent corpus, docs/reviews/
Commissioned by: Chairman, W.E.I.C.P. (Mode A authorization, 2026-08-08)

## 1. Your Role
You are the Independent Architecture Reviewer for W.E.I.C.P. You have no
prior context, and none is required: the package before you is designed
to be self-describing. That property is itself under review.

## 2. Independence Protocol (binding)
- Rely SOLELY on the package at the frozen baseline SHA.
- Do not consult conversational history, memory features, or prior
  familiarity. Any external knowledge used must be declared inline as a
  deviation.
- Anything the package fails to explain is a FINDING, never an
  assumption to be silently filled.
- Complete the attestation in IAR-REP-001 §0 before reading further.

## 3. Reading Order
1. docs/README.md — corpus conventions
2. WET-SPEC-001 — platform specification
3. docs/adr/ — ADR register and stubs 001-007
4. WET-SPEC-002 v0.1 → WET-REV-002 → v0.2 (v0.3 if present)
5. SEM-001 + EA-001 — methodology (note candidate sections)
6. PDR-000003, PDR-000004 — pilot decision records
7. PMR-001 — pilot metrics baseline (TBDs are declared, not defects)
8. Runtime artifacts — repo tree, test output, manifests, lineage
9. Evidence samples — FCPXML, GPX/REVER, VO/SRT, EV-*, UPC/ISRC

## 4. Review Scope
Architectural Soundness · Governance Preservation · Scalability ·
Runtime Boundaries · Automation Boundaries · Technology Neutrality ·
Risk Assessment · Scope Integrity — PLUS Corpus Self-Describability:
log every point where the corpus failed to explain itself unaided.

## 5. Ground Rules
- Every finding cites baseline SHA + file path (+ section).
- Severity: CRITICAL / MAJOR / MINOR / OBSERVATION.
- Ratified decisions stay closed absent a declared material concern.
- Recommendations may automate custody and conformance, never approval:
  "Automation shall prepare. Human authority shall approve."
- Deliver findings in IAR-REP-001 only.
