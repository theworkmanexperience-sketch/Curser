# WET-REV-002 — Disposition: WET-SPEC-002 v0.1 (Production Decision Record)
Status: RATIFIED PATH FORWARD · Date: 2026-08-07 · Reviewer: Office of the Chief AI Engineering Architect

## Decision
CONCUR WITH COMMENTS — forward. PDR adopted as the platform's editorial
decision artifact (implements the Intelligence Domain review's
distribute-not-domain recommendation).

## Required consolidations (v0.2)
1. ONE provenance vocabulary: OBSERVED/DERIVED/INTERPOLATED/ENRICHED/GENERATED
   (harmonize with ADR-003; "approved" removed — it is lifecycle, not provenance)
2. ONE rights ledger: pdr.rights = record of truth; shoot.yaml music_rights
   becomes an index of PDR IDs
3. Gate-linked approvals: optional gate: gate1|gate2|gate3 per approval entry —
   PDR approvals join the existing gate ledger, never a parallel system
4. Timecode convention declared: timeline.format = video_hms|source_tc|wall_clock

## Boundary (one sentence, canonical)
ADRs govern the platform; PDRs govern productions.

## Exercise-first order
Populate 8-10 retroactive PDRs from Part 1 decisions (placed cues, rejected
cues incl. HIGHWAY GHOSTS, NOTOR1OUS Gate-1 clearance, 46-mph stat demotion)
BEFORE v0.2 refinement. PRS-001 and WET-SPEC-003 remain deferred until then.

## CIM consolidation
PDR subsumes the proposed Cue and Claim entities in ADR-006's model.
