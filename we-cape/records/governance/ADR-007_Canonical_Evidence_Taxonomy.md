# ADR-007 — Canonical Evidence Taxonomy

**Status:** PROPOSED (drafted 2026-08-07 for Chairman ratification; prerequisite to Locking any PDR — WET-SPEC-002 §3, PD-001 X-4)
**Context documents:** ADR-003 (Telemetry Provenance, PROPOSED) · WET-SPEC-002 v0.2/v0.3 · USADDO framework (archived reference)

## Context

Three overlapping evidence vocabularies exist in the corpus: WET-SPEC-001 build statuses (BUILT / ACTIVE DESIGN / ARMED / EXERCISED), ADR-003 telemetry provenance classes with confidence bands, and the USADDO framework's eleven evidence classifications with letter grades. The pilot PDRs demonstrated the need for one canonical epistemic vocabulary spanning telemetry, media artifacts, and editorial decisions — and for one class ADR-003 lacks: content that is *created* rather than captured or transformed from capture.

## Decision

1. **Canonical epistemic classes** (apply to any evidence item or decision artifact, platform-wide):
   - **OBSERVED** — directly captured from a sensor, system, or authoritative source without transformation.
   - **DERIVED** — produced by defined transformation of observed material (e.g., review cut from camera originals, SRT from voice-over).
   - **INTERPOLATED** — estimated between observed points.
   - **ENRICHED** — augmented with material from outside the observed source.
   - **GENERATED** — created rather than captured or transformed from capture (e.g., AI-generated cue, composed narration). *New in this ADR; extends ADR-003.*
2. **Confidence bands** (unchanged from ADR-003): HIGH ≥ 0.90 · MODERATE ≥ 0.70 · LOW ≥ 0.50 · UNUSABLE below.
3. **Conclusions derived from evidence are labeled as DERIVED with the derivation stated** (exercised precedent: EV-SUB-010 coverage arithmetic in PDR-000003 rev 5).
4. **Scope-of-proof attributes** accompany classification where relevant: `coverage_period` (what time span the evidence proves — exercised precedent: subscription evidence) is a first-class attribute in WET-SPEC-002 v0.3 and a PRS-001 core requirement.
5. **Mappings (informative):**
   - WET-SPEC-001 statuses are *maturity* labels, not epistemic classes; they continue unchanged and do not participate in this taxonomy.
   - USADDO kernel classes map as: VERIFIED_PRIMARY → OBSERVED/DERIVED with HIGH confidence and primary custody; MANAGEMENT_REPRESENTATION → recorded as source attribute (who asserts), orthogonal to epistemic class; INFERENCE → DERIVED with stated derivation; NOT_PROVIDED / REQUIRES_SPECIALIST_REVIEW → status markers, retained as-is.
6. ADR-003 is amended by reference: its taxonomy plus GENERATED **is** this canonical taxonomy; no separate vocabulary may be introduced by future specifications without amending this ADR.

## Consequences

- The pending-vocabulary dependency recorded in WET-SPEC-002 §3 and in pilot PDR evidence entries resolves upon ratification; Locking is unblocked (PD-001 X-4).
- PRS-001 must validate classifications against this ADR.
- Any record or specification using a non-canonical class is non-conformant.

## Ratification

Ratified by: ______________________________ (Chairman, W.E.I.C.P. ERB) · Date: ____________
