# Brief — Automation of the Domain Map
**Document:** FO-002 · **Date:** 2026-08-07 · **Status:** Advisory brief (non-normative)
**Prepared by:** Independent AI Reviewer (Claude) · **Companion to:** FO-001 Framework Overview

## Governing Principle

**Automate custody and conformance. Never automate judgment.** Every automation candidate below moves evidence, checks rules, or detects drift. None approves, selects, ratifies, or accepts risk — those remain human by architectural identity (Gates 1–3, §6a transitions, W.E.I.C.P. ratification), consistent with the platform's own rule that consequential actions require deterministic authorization outside any model. Automation output enters records as OBSERVED or DERIVED evidence with provenance, same as anything else.

The strategic reason to automate is already on the risk register: **governance capacity**. A single operator services the entire governance surface; automation is the only mitigation that scales the surface without scaling headcount. Documentation debt is the platform's top-ranked risk, and every task below converts a recurring manual obligation into code.

## Automation Posture by Domain (current → target)

| Domain | Today | Automation target |
|---|---|---|
| C.A.P.E. Runtime | **Already the most automated domain** — offload, 7-stage CAPTURE, health report, guards (BUILT); new_shoot orchestrator BUILT, unexercised | Exercise new_shoot end-to-end (v1.0 criterion 1); no new design needed |
| Evidence & Records | Validator automates conformance; hashing/assembly performed manually this week | **Highest-leverage frontier** — A1–A5 below |
| Editorial Intelligence | Interactive by nature (human+AI sessions) | Automate the *evidence assembly around* sessions (A6), never the creative selection |
| Gates | Human, by design | Automate the *evidence presentation* to the gate, never the gate decision |
| Progressions | Compositor automated with refusal contracts (BUILT) | Unchanged |
| EVALUATE | Instruments partially live; FCPXML parsing demonstrated in-session | Scheduled instrument runs (A7) |
| W.E.I.C.P. | Manual, correctly | Only mechanical support: validator in CI, package manifests (ADR-010 candidate) |

## Ranked Automation Candidates

**A1 — PDR scaffold generator (highest leverage, do first).** A repo script that assembles a Draft PDR from primary artifacts: hashes from disk, placements from FCPXML (the parser already exists from this session), timebase from the sequence format, ISRCs from filed release metadata, evidence blocks pre-populated with custody paths. Human fills exactly four things: objective, decision analysis, rationale, approvals. *Evidence basis: this is precisely the manual procedure exercised for PDR-000003/000004 — the pilot was the requirements capture. Directly reduces the cost of the six outstanding cue PDRs and every record after.*

**A2 — Evidence intake watcher.** New files in designated custody folders (Soundtrack/, XML/, records/pdr/evidence/) are hashed and registered automatically. *Structurally closes ER-3 (cue assets outside the registry) as a standing class rather than a one-time fix.*

**A3 — Validator in CI.** Pre-commit / CI hook running the v0.3 validator over `records/pdr/`. A non-conformant record cannot enter the repository. *Converts §5 from policy into enforcement; the house pattern (404 tests) applied to records.*

**A4 — Placement drift detector.** On each FCPXML export, re-extract placements and diff against Locked/Draft PDRs; flag moved or removed cues. *Would have surfaced ER-6 (33:58 vs 43:22) automatically instead of via screenshot inspection. This is EVALUATE's pattern applied to editorial state.*

**A5 — Transition recorder CLI.** A small command that appends §6a transition entries with chain validation (refuses broken chains, checks CR-2/3/4 before permitting a Locked target). *Makes malformed lifecycle history structurally impossible while keeping the actor human.*

**A6 — Session-record capture.** Semi-automated export of AI-session artifacts (prompts, strategy notes, generation parameters) into hashed custody at session end. *Closes the recurring ER-2 class; CR-1 compliance becomes a habit with a tool instead of a request.*

**A7 — Scheduled EVALUATE instruments.** Utilization, intake yield, and custody-integrity runs on a cadence, findings emitted to the governance queue.

## Sequencing and Boundary

Order: **A1 → A3 → A2 → A4 → A5 → A6 → A7.** A1 and A3 pay for themselves on the six pending cue PDRs. Defer any *agentic* orchestration (automation that chains decisions) until PRS-001 exists — the registry is the natural API substrate, and automating against hand-maintained files would build on sand. Revisit the boundary only through an ADR; the line between "assembles evidence" and "makes decisions" is the platform's constitution, and it should take a ratification, not a convenience, to move it.

**One-line summary:** the runtime taught the platform to automate custody of files; the next cycle teaches it to automate custody of decisions — while the deciding stays exactly where it is.
