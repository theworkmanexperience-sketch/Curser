# W.E. Platform Framework Overview
### From W.E. C.A.P.E. field capture to the Editorial Intelligence Platform

**Document:** FO-001 · **Date:** 2026-08-07 · **Status:** Reference overview (descriptive, non-normative — the cited specs govern)
**Prepared by:** Independent AI Reviewer (Claude) · **Source basis:** WET-SPEC-001 v1.0, ADR-001/-003/-007(draft), WET-SPEC-002 v0.3, PD-001, pilot records PDR-000003/000004 and filed evidence

**Status legend (house discipline):** `BUILT` = production-verified with cited evidence · `EXERCISED` = demonstrated on real production, pre-ratification · `PILOT` = exercised inside the Soundtrack Domain Pilot · `DESIGN` = declared design, not yet verified · `PROPOSED` = drafted, awaiting ratification · `PLANNED` = named, not yet authored

---

## 1. The Domain Map

The architecture is five cooperating domains. No domain commands another; they intersect through **standards, records, and gates** (ADR-001's ratified principle).

```
                      ┌─────────────────────────────────────────────────────┐
                      │              W.E.I.C.P.  (GOVERNANCE)               │
                      │   ADRs · Specs · Standards · Phase declarations     │
                      │   Ratifies. Never executes.                         │
                      └───────▲──────────────────────────────┬──────────────┘
                       findings│                              │standards
                              │                              ▼
┌──────────────────┐   ┌──────┴───────────────┐   ┌─────────────────────────┐
│  W.E. C.A.P.E.   │   │   EVIDENCE & RECORDS │   │  EDITORIAL INTELLIGENCE │
│    (RUNTIME)     │──▶│        LAYER         │◀──│   (EMERGING PLATFORM)   │
│ Capture·Archive· │   │ Registry · Manifests │   │  Human+AI sessions:     │
│ Pulse·Evaluate   │   │ Lineage · PDRs ·     │   │  semantic reasoning,    │
│ deterministic,   │   │ Evidence custody ·   │   │  cue strategy, genera-  │
│ fail-closed      │   │ Validator            │   │  tion. PROPOSES ONLY.   │
└────────┬─────────┘   └──────────┬───────────┘   └────────────┬────────────┘
         │ media + telemetry      │ governed records            │ proposals w/
         ▼                        ▼                             ▼ provenance
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ENFORCEMENT GATES (RUNTIME CONTRACTS)                   │
│   Gate 1 Rights (EXERCISED) · Gate 2 Claims (ARMED) · Gate 3 Publication    │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     ▼
                      ┌──────────────────────────────┐
                      │  W.E. PROGRESSIONS (PUBLISH)  │
                      │  Gate-cleared artifacts only  │
                      └──────────────────────────────┘
```

**Authority model in one sentence:** Intelligence proposes → humans gate → Runtime executes → EVALUATE measures → W.E.I.C.P. ratifies → standards return to every domain.

---

## 2. The End-to-End Workflow

How one production (exercised: AlphaRoundUp 2026) flows through the platforms:

**Stage 1 — Field capture → custody (W.E. C.A.P.E., `BUILT`).** Cards from registered camera bodies are offloaded hash-verified to dual destinations (5 offloads, MISMATCH 0); `shoot.yaml` is authored with a trusted-clock declaration. Camera identity comes from file metadata, never card labels. From this point, every original has a SHA-256 in the append-only registry.

**Stage 2 — Deterministic ingestion (`BUILT`).** CAPTURE's seven stages (ingest → classify → group → variant → output → proxy → audit) produce proxies and run records; the Health Report audits clock/grouping against the trusted anchor; the output-inside-input guard refuses contamination. Registry: 726 content rows for this production.

**Stage 3 — Editorial assembly (FCP Tier-1 interface, `BUILT` integration).** The draft cut is built in Final Cut Pro over FCP_MEDIA symlinks. FCPXML round-trip provides the platform's measurement tap (utilization instruments) and — as of the pilot — the **authoritative placement evidence** for editorial decisions. Review artifacts emerge here: review MP4, voice-over, SRT.

**Stage 4 — Editorial Intelligence session (`PILOT` — the emerging platform).** Human + AI reason semantically across the review cut, narration, SRT, telemetry, and production notes to produce *proposals*: cue strategy before lyrics, lyrics, style prompts, generation via Suno, editorial placement intent. This is the DDM-001 capability set, now operating under governance instead of outside it. Its work products carry no execution authority — they become real only through Stage 5's records and Stage 6's gates. (Chartering as a formal domain is the ADR-009 candidate, evidence-triggered.)

**Stage 5 — Governed recording (WET-SPEC-002, `PILOT` → freeze candidate).** Each editorial decision becomes a **Production Decision Record**: evidence with canonical classification (ADR-007) and hashes, decision analysis with rejected alternatives, generation separated from validation, rights as a first-class object (ISRC/UPC/entitlement coverage), human approvals with independence disclosure, and a §6a transition chain. The executable validator enforces conformance mechanically (12/12 fixtures). Exercised: PDR-000003 (BLACKTOP HYPNOSIS v3), PDR-000004 (OUT HERE), 18 evidence objects in hashed custody.

**Stage 6 — Gates (`Gate 1 EXERCISED · Gates 2–3 ARMED`).** Rights (Gate 1: no contributed media without recorded scoped consent — caught a real violation), factual claims (Gate 2), and publication approval (Gate 3, which starts retention clocks). PDR rights blocks and `gate_clearance_ref` bridge the record system into the gate system so publication decisions are record-backed.

**Stage 7 — Publication (W.E. Progressions).** Gate-cleared artifacts publish; the SHA-gated compositor enforces brand integrity with a four-rule refusal contract (no fallback path exists). Parallel commercial track exercised in the pilot: the soundtrack itself released via DistroKid (8 tracks, UPC 882436051388) — with entitlement coverage evidenced in the records.

**Stage 8 — Measurement → governance (EVALUATE `partially live` → W.E.I.C.P.).** Instruments (Criterion-2 baseline, production clock, utilization, intake yield, custody integrity) convert operations into findings; W.E.I.C.P. ratifies findings into ADRs and standards; standards flow back into runtime contracts, record schemas, and intelligence-session rules. The pilot itself ran this loop at spec scale: pilot findings PF-1/2/3 → WET-SPEC-002 v0.3.

---

## 3. Where Each Governing Document Sits

| Instrument | Governs | Status |
|---|---|---|
| WET-SPEC-001 v1.0 | Platform identity, runtime modules, gates, data model, v1.0 criteria | Authoritative baseline |
| ADR-001 | Runtime/Governance domain separation | RATIFIED |
| ADR-003 | Telemetry provenance classes + confidence | PROPOSED (absorbed by ADR-007) |
| ADR-007 | Canonical evidence taxonomy (incl. GENERATED), coverage-period, derived-conclusion rule | PROPOSED — gates Locking (PD-001 X-4) |
| WET-SPEC-002 v0.3 | The PDR — atomic governed editorial decision record; §6a interim transitions | Freeze candidate, awaiting final independent review |
| PD-001 | Soundtrack Domain Pilot final-validation phase: exit criteria X-1..X-5 | Awaiting Chairman ratification |
| PRS-001 | Registry: ID issuance, evidence IDs w/ checksums, lineage, querying | PLANNED (post-freeze) |
| WET-SPEC-003 | Lifecycle state graph (inherits §6a chains; Rejected/Superseded mandatory) | PLANNED (post-freeze) |
| ADR-009 candidate | Editorial Intelligence domain charter (proposal-only authority, graduation criteria) | IDENTIFIED — evidence-triggered |
| USADDO framework | Assurance/diligence reference; kernel extraction only | ARCHIVED reference (per first ERB review) |

---

## 4. The Three Feedback Loops That Make It a Platform

1. **Measurement loop:** Runtime → EVALUATE instruments → findings → W.E.I.C.P. → standards → Runtime. (WET-SPEC-001's operating model: Policy → Code → Test → Evidence → Evaluate → Ratify → Standard.)
2. **Records loop:** Intelligence session → PDR + evidence custody → validator → gates → publication; every decision auditable without chat history or the decision-makers. (The pilot's contribution — the loop that did not exist three days ago.)
3. **Spec-evolution loop:** Real records break specs in informative ways → pilot findings → spec revision → validator update → records migrate. (Exercised: v0.1 → v0.3 in one pilot cycle.)

## 5. Honest Maturity Snapshot

`BUILT`: offload, CAPTURE, compositor, guards, registry, Gate 1. `EXERCISED/PILOT`: PDR record system, evidence custody, validator, entitlement-coverage evidencing, intelligence workflow (soundtrack discipline only). `ARMED`: Gates 2–3. `DESIGN`: ARCHIVE, PULSE, EVALUATE completion. `PROPOSED`: ADR-007, v0.3 freeze, PD-001. `PLANNED`: PRS-001, WET-SPEC-003, ADR-009 charter, remaining six cue PDRs (first production use of v1.0). Top standing risks remain governance-capacity (documentation debt) and single-node deployment — both acknowledged in the baseline and unchanged by the pilot.

**The through-line:** the platform's founding idea — *verifiable custody of files* — has now been extended one ring outward to *verifiable custody of decisions*. The Editorial Intelligence Platform is not a new machine; it is the existing discipline applied to the most human part of the pipeline, with AI proposals entering the same custody, classification, and gating that camera originals have had since the first offload.
