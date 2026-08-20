# WET-SPEC-DIE-001 — Documentary Intelligence Engine
## Specification v0.2 (Draft)

## Governance Status
Document Type: Specification (Draft v0.2) · Series: Intelligence (named-series per docs/README)
Normative Authority: None until frozen · Route: Engineering Review → Freeze
Constitution: AIS-001 v1.0 (51d31e2, certified) · Acceptance Memorandum (27674d7)
Founding Fixture: Part 2 Canonical SRT Registry Extraction (2026-08-20) — Appendix A

## Change Log v0.1 → v0.2 (Chairman review, 12 modifications + rulings)
M1 spec/fixture separation (§9 normative, Appendix A observed) · M2 immutable
registry identifiers · M3 registry_version + registry_schema_version · M4 run
metadata (§3) · M5 extraction source_confidence, nullable ruling · M6 registry
independence · M7 processing states · M8 TIMELINE_REGISTRY expansion w/
enrichment-namespace ruling · M9 motorcycle evidence triplets · M10
PROMPT_REGISTRY · M11 machine-readability requirement · M12 WHY_RIDE elevated
to Strategic Registry w/ research-consent ruling · Rename: "W.E. Ground Truth
Contract" (governs authority, provenance, hierarchy, verification, confidence
— not only quality).

## 1. Scope
Governs the Documentary Intelligence Engine: extraction of ground-truth facts
from canonical production sources into governed registries (DIE-X), and
resolution of those facts into canonical entities (DIE-R). Out of scope:
narrative interpretation (NIE), musical intelligence (MIE), publication
products (PIE), storage internals (PRS-001).

## 2. The W.E. Ground Truth Contract
Every source document SHALL carry: a grade — GT-1 (raw ASR output) · GT-2
(canonical transcript, production-designated) · GT-3 (human-verified) — plus
SHA-256, version, and provenance. Under Transcript Authority, GT-1/GT-2 facts
are evidence of speech, not verified speech; only GT-3 sources may set
verification_status=VERIFIED. A DIE run SHALL record the grade, hash, and
version of every source consumed. The contract governs authority (which
source wins), provenance (where it came from), hierarchy (GT-3 > GT-2 > GT-1),
verification (upgrade path), and confidence (per-fact, where the source
provides it).

## 3. Run Metadata (reproducibility envelope)
Every DIE execution SHALL produce a run record containing: run_id (WEF_
convention) · timestamp · model identifier · prompt revision · source
document SHA-256 + version + GT-grade · operator · repository commit ·
specification version. A run lacking any field is non-conforming and its
outputs are ineligible for registry custody.

## 4. DIE-X — Extraction (normative)
X-1 Every fact is verbatim-of-source with citation: source SHA-256, cue
reference, timecode. X-2 Zero interpretation: no spelling correction, no
normalization, no inference at extraction. X-3 Fact envelope: fact_id ·
source_sha · cue_ref · timecode · verbatim_text · source_quality (GT-grade) ·
source_confidence (REQUIRED field, NULLABLE value — populated only when the
ASR system emits per-segment confidence; NEVER fabricated; GT-2 SRT sources
typically carry none) · verification_status (TRANSCRIBED | VERIFIED) ·
evidence_class (OBSERVED). X-4 Coverage reconciliation: every run reports
cues consumed vs cues present, with categorized exclusions (music-bed,
ambience, crowd, non-speech) — no unexplained deltas. X-5 Model-mediated
extraction SHALL pass validator fixtures before outputs enter custody.

## 5. DIE-R — Resolution (normative)
R-1 Resolution maps verbatim renderings to canonical entities: entity_id ·
canonical_name · renderings[] · resolution_confidence (HIGH|MEDIUM|LOW) ·
resolution_evidence[] · conflict_state. R-2 Resolution is DERIVED-class and
never overwrites DIE-X facts; renderings are preserved permanently. R-3
Conflicts produce UNCONFIRMED or CONFLICTED, never a silent winner. Canonical
naming requires GT-3 verification OR two or more independent evidence classes.
R-4 Identity evidence precedence: human-verified declaration → visual or
document asset → corroborated multi-rendering convergence → single-rendering
inference (LOW, auto-UNCONFIRMED). R-5 Person entities additionally carry:
consent_status · rights_class · anonymization_eligibility ·
research_use_consent (distinct from appearance consent). R-6 Processing
state per entity: DISCOVERED → EXTRACTED → RESOLVED → VERIFIED → LOCKED
(LOCKED = custody-frozen at a hash; state transitions are recorded).

## 6. Registry Framework (normative, all registries)
F-1 Immutable identifiers name every registry (schema, storage, APIs,
documentation); display numbering is presentational only. F-2 Every registry
carries registry_version and registry_schema_version. F-3 Registries SHALL be
independently consumable — no consumer is required to ingest all registries
to use one. F-4 Every registry SHALL be serializable into structured formats
suitable for downstream intelligence systems, including JSON, YAML, SQL,
graph databases, and vector indices. F-5 Registries containing personal data
are governed artifacts: access-controlled, emission-filtered, consent-checked
per person.

## 7. The Registries (immutable IDs)
RIDER_REGISTRY — person entities + affiliation refs + first_cue + R-5 fields.
MOTORCYCLE_REGISTRY — evidence triplets, never overwritten: spoken_make /
spoken_model · visual_make / visual_model · verified_make / verified_model.
Spoken-evidence ceiling is explicit: absent visual/verified values remain
NULL, never inferred.
INTERVIEW_REGISTRY — subject ref, cue span, setting context.
PROMPT_REGISTRY — prompts with prompt_class: interview_question | narration |
production | ai_prompt; template IDs + variants[].
WHY_RIDE_REGISTRY (Strategic Registry) — verbatim answers + subject ref +
timecode. Elevated: longitudinal research dataset accumulating across
productions; research use requires research_use_consent independent of
appearance consent.
ORGANIZATION_REGISTRY — entities + renderings + chapter/location attributes.
LOCATION_REGISTRY — entities + role (venue | origin | route | civic).
QUOTE_REGISTRY — verbatim + speaker ref + context tag.
TIMELINE_REGISTRY — DIE-owned observed fields: segment_id · start · end ·
primary_activity · participants[] · location_ref · vehicles[] ·
music_present · interview_count. Reserved enrichment namespaces — nie.* ·
mie.* · pie.* — are annotated by higher engines under their own governance
and SHALL NOT be written by DIE (narrative importance, cue suggestions,
energy, and product candidates are NIE/MIE/PIE-class outputs).

## 8. Progressive Intelligence Compliance
DIE consumes only W.E. Ground Truth Contract sources. DIE registries are the
sole authorized input for higher engines; re-analysis of raw sources by
NIE/MIE/PIE requires explicit, recorded governance authorization.

## 9. Validation Requirements (normative — fixture-independent)
Every conforming implementation SHALL: V-1 cite every fact to source SHA +
timecode; V-2 mark every unresolved or ASR-suspect proper noun UNCONFIRMED;
V-3 perform zero silent resolutions; V-4 emit coverage reconciliation with
categorized exclusions summing exactly to source cue count; V-5 populate all
nine registries or report each empty registry with reason; V-6 emit the §3
run record; V-7 reproduce reference-fixture results within categorized-
explanation tolerance — deviations without categorized explanation are
failures.

## 10. Governance
All DIE outputs are advisory under the Principle of Human Editorial
Authority. Registry exports are emissions (Gate/consent filtering applies).
Decisions arising from DIE content are PDR-recorded.

## 11. Non-Goals
No theme detection, sentiment, or narrative inference. No biometric speaker
identification. No autonomous publication of registry content.

## Appendix A — Reference Fixture (observed values; validates, never defines)
Fixture: Alpha RoundUp Part 2 Canonical SRT (GT-2) · 2,290 cues ·
00:00:00–01:20:40. Observed: 75 rider interviews + 5 civic speakers · 9
registries populated · 14 temporal sets · UNCONFIRMED discipline exercised
on ASR-corrupted proper nouns · extraction of record: 2026-08-20.
