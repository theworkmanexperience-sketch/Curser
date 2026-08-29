# WET-EXEC-002 — PRESENTATION OUTLINE

**Revised under:** EXECUTIVE REVIEW ORDER — WET-EXEC-003
**Companion to:** `WET_EXEC_002_EXECUTIVE_BRIEFING.md`
**Targets:** Gamma AI · PowerPoint · Keynote
**Classification:** Technical & Governance Diligence Package
**Custody:** `EXECUTIVE PRESENTATION PACKAGE ONLY`
**Certification:** `EXECUTIVE PRESENTATION READY`

---

## 0 · THREE DECKS, ONE SOURCE

The package now separates by audience rather than trying to serve five readers with one runtime.

| deck | length | audience | question it answers |
|---|---|---|---|
| **A · Executive Story** | 20–30 min · 18 slides | family, partners, general and executive audiences | *What did we build and why does it matter?* |
| **B · Technical Appendix** | 45–60 min · 16 slides | Marcus, Desmond, principal engineers, CTOs | *How does that actually work, and where is it weak?* |
| **C · Governance Appendix** | 30–40 min · 12 slides | Valerie, board members, compliance and enterprise governance | *How do I defend this to a regulator or a board?* |

**Deck A stands alone.** B and C are held in reserve and deployed on question — which is how technical depth should behave in an executive room. Every slide in B and C traces to a section of the briefing.

**Two rules across all three decks.** No slide carries a composite score. No slide carries the 85 % utilization figure.

**Every metric slide carries its definition.** Re-measure before any presentation — `DOC-001` applies to the deck as much as to the generator.

---

## 1 · HOW TO USE THIS OUTLINE

Each slide carries five fields. Build in this order — **the visual is specified before the text**, because a heavy-graphics deck fails when copy is written first and pictures are retrofitted.

**Objective** · **Visual** (named from `WET_EXEC_002_GRAPHICS_GUIDE.md`) · **On-slide text** · **Speaker notes** · **Evidence**

---

# DECK A — EXECUTIVE STORY
### 18 slides · 20–30 minutes

## ACT I — THE PROBLEM AND THE PERSON

### A1 · Twenty-five of seventy-five
**Objective:** open on the human stake, not the technology.
**Visual:** `G-01 Rider Wall` — 75 tiles, 25 as outlines.
**On-slide text:** 75 riders told us why they ride. 25 of their names could not be verified. **The registry says so.**
**Speaker notes:** "We could have guessed twenty-five names. Nobody would ever have known. The system marks them UNCONF and refuses to fill the field. Everything I'm about to show you is an elaboration of that decision."

### A2 · The thesis
**Objective:** the positioning statement, verbatim.
**Visual:** `G-03 Authority Pyramid`.
**On-slide text:**
> **W.E. C.A.P.E. is a governance-first architecture for human-directed AI collaboration** — decisions traceable to evidence, evolution recorded against the evidence that forced it, and an **auditable** boundary between what the machine may do and what only a human may decide.

**Speaker notes:** "Note the word *auditable*, not *complete*. Seven constitutional decisions in this corpus are not under version control, and that's disclosed on slide 17. I'd rather you hear it from me."

### A3 · Custody is not authority
**Objective:** seed the central idea early, pay it off in Act III.
**Visual:** `G-14 Custody vs Authority` — two orthogonal axes.
**On-slide text:** **Custody is not authority, and custody is immutable.** An actor may hold, author, measure and enforce — and never decide.
**Speaker notes:** "Keep this in your head for the next ten minutes. Everything that follows is a consequence of separating who touched a thing from who may decide about it."
**Evidence:** `ER-003`, `ER-004`.

### A4 · The problem nobody governs
**Visual:** `G-02 Split Panel`.
**On-slide text:** Terabytes with no chain of custody · timestamps that lie · rights tracked by memory · AI content with no provenance.

### A5 · The proving ground
**Visual:** `G-05 Production Stat Band`.
**On-slide text:** 4 cameras · ~170 source files · 139 curated exports · 75 interviews · 3-part series · 8-track soundtrack in distribution.

## ACT II — WHAT THE EVIDENCE FORCED

> **This act wins the room. Do not soften it — the candour is the argument.**

### A6 · Eleven days of silence
**Objective:** the turning point.
**Visual:** `G-06 Commit Density Strip` — the gap as a void.
**On-slide text:** 27 July – 7 August 2026 · **Zero commits.** Part 1 was edited and published in this window.
**Speaker notes:** "The platform was not used to make it. We found that by reading the *absence* of records."

### A7 · Ten moments — the structure
**Objective:** set the frame before the moments.
**Visual:** `G-25 Moment Card Template` — the six-field card, empty.
**On-slide text:** The position on record · What the evidence showed · Decision · Governance artifact produced · Long-term impact
**Speaker notes:** "Ten times, evidence forced a change of direction. Each one is recorded the same way. Note what the second field is *not* — it isn't 'what we believed.' The platform is prohibited from telling you what anyone believed. It can only show you what the record said."

### A8–A12 · Five moments, one per slide
**Visual:** `G-25` populated, one card per slide.
Use **Moments 2, 4, 5, 7, 9** for Deck A — *all prior reports incorrect* · the eleven silent days · the timestamp that lied · custody is not authority · the refusal to infer.
**Speaker notes (A12, the refusal):** "An Executive Order authorised a regeneration. The platform refused and filed six exceptions. The shallowest would have taken minutes to fix — and would have produced a running generator emitting the wrong film."
*(Moments 1, 3, 6, 8, 10 move to Deck B.)*

### A13 · Four refusals
**Objective:** the most defensible claim in the package.
**Visual:** `G-19 Refusal Ledger`.
**On-slide text:** four rows — authorised action | refused because.
**Speaker notes:** "**A control that has never fired is not a control. These fired.**"

## ACT III — WHAT IT PROVES

### A14 · Six layers, and only two of them act
**Visual:** `G-13 Six-Layer Stack` — verbs at display weight.
**Speaker notes:** "Read the verbs. Executive decides. Runtime refuses. Nothing in between decides anything."

### A15 · Ninety to thirty-nine
**Objective:** the ratio that describes the initiative.
**Visual:** `G-21 Ratio Bar` with definitions on-slide.
**On-slide text:** **90 governance documents** *(Markdown under `docs/`)* · **39 engine modules** *(non-test Python under `wecape/`)* · **2.3 : 1**
**Speaker notes:** "Nobody planned that ratio. And the load-bearing instruments — custody, the evidence hierarchy, the reporting standard — contain nothing about video. They were written for a motorcycle documentary and they already apply anywhere. **That is the asset.**"

### A16 · Why now
**Visual:** `G-26 Why-Now Timing Panel`.
**On-slide text:** Provenance becoming mandatory · "human oversight" being defined in regulation · AI content entering distribution ahead of rights frameworks · enterprises writing policy without reference implementations.
**Speaker notes:** "Governance-first was a constraint in May. It's becoming a requirement. We didn't reposition for it — the corpus was written for a documentary and already applies."

### A17 · What this deck does not claim
**Objective:** disclose before you are asked. **Do not skip.**
**Visual:** `G-23 Disclosure Panel` — deliberately undesigned.
**On-slide text:**
- The 85 % utilization figure is **not carried forward** — no producing computation exists.
- Seven constitutional decisions (`ADR-001`–`008`) are **not in version control**.
- The 6,122-line artifact pipeline has **no unit tests**.
- **No dependency manifest, no release version since May, no CI, no independent security audit.**
- **One ratifying authority, no succession instrument.**
- Every "mature" characterisation rests on **n = 1**.
- The soundtrack rights posture is **routed to specialist review**.

**Speaker notes:** "Every one of these was surfaced by the governance system, not by an outside reviewer. That we can list them precisely is the strongest argument for everything else."

### A18 · The gated horizon, and the close
**Visual:** `G-27 Gated Strategic Horizon`.
**On-slide text:** Today → *Gate A* → Multiple productions → *Gate B* → Studio → *Gate C* → Enterprise → *Gate D* → Governed Human–AI Collaboration Platform. **Healthcare · Government · Education: separate regulated programmes, not rungs.**
**Speaker notes:** "We're before Gate A. Four production inputs are missing. And the highest-value thing available isn't a feature — it's a second production, because every compounding claim we make is unfalsifiable at n = 1." *(pause)* "Nine of the ten moments that changed this platform are moments where it discovered it was wrong. The story isn't what it became. **It's what it did every time the evidence disagreed with it.**" *(pause)* "Seventy-five riders told us why they ride. Twenty-five of those names are still marked unconfirmed. That isn't a gap in the work. **That is the work.**"

---

# DECK B — TECHNICAL APPENDIX
### 16 slides · 45–60 minutes · Marcus · Desmond · principal engineers · CTOs

### B1 · System architecture
**Visual:** `G-28 System Component Diagram` — actual modules and data flow.
**On-slide text:** `wecape/` acquisition engine (39 modules, 5,802 LOC) → derived intermediates → `intelligence/` artifact pipeline (31 scripts, 6,122 LOC) → seven governed artifacts.

### B2 · Repository topology
**Visual:** `G-29 Repository Topology` — treemap by directory, sized by file count.

### B3 · The workflow
**Visual:** `G-30 Production Workflow` — capture → offload → organise → conform → edit → observe → generate → gate → publish.

### B4 · Testing hierarchy
**Visual:** `G-31 Testing Hierarchy`.
**On-slide text:** four harnesses, **not additive** — engine unit suite 384 · acceptance 99/99 · ECR conformance 22 PASS/0 FAIL · 6 negative tests, each exit 2 with 0 files written.
**Speaker notes:** "Four numbers, four different things. And the inversion you'll want to know about is next."

### B5 · The testing inversion — disclosed
**On-slide text:** Engine: 5,802 LOC / **5,823 test LOC**. Artifact pipeline: 6,122 LOC / **0 unit tests**.
**Speaker notes:** "More test code than engine code — and the pipeline that produces every governed artifact has none. It's covered end-to-end by 22 conformance tests with proven negatives, and that's it. It's the first thing I'd fix."

### B6 · Runtime guard lifecycle
**Visual:** `G-32 Runtime Guard Lifecycle` — inputs → 14 guards → ✗ → first write never reached.

### B7 · Negative test ledger
**Visual:** `G-17` ledger strip — six faults, six stops, zero files written.

### B8 · The `zip()` that never compared anything
**Visual:** `G-20 Validator Comparison` — 1/191 at true scale.
**Speaker notes:** "**Don't validate the comparison — make the wrong comparison unrepresentable.** Cardinality is now asserted before pairing, so truncation is structurally impossible."

### B9 · The equivalence proof
**On-slide text:** 205,679 bytes · 7 changed lines · 5 changed bytes · every change explained.

### B10 · Parameterisation as diagnosis
**On-slide text:** 74.3 % of emitted text is literal prose *(38,056 of 51,237 characters, `traceability_scan.py`)*.
**Speaker notes:** "*You cannot see an assumption until you try to make it a parameter.*"

### B11 · Local-first security architecture
**Visual:** `G-33 Local-First Security` — enforced network invariant, no egress from the engine path.
**On-slide text:** media never leaves the machine · PII gated off by default · path redaction on egress · encrypted offsite · restore-proven 3-2-1.

### B12 · Observability of refusal
**On-slide text:** `FAILED_SOURCE_IDENTITY` · `FAILED_CARDINALITY` · `FAILED_COMPARISON` · `FAILED_TIMELINE_CLOSURE`
**Speaker notes:** "You can audit what the system declined to do, not just what it did. In an incident review, that's the log that matters."

### B13 · Dependency and version disclosure
**On-slide text:** **No `requirements.txt`, no `pyproject.toml`, no `setup.py`. No product release tag since 2026-05-27.** The two later tags are a document freeze and a corpus tag, not releases.
**Speaker notes:** "Three months of the most significant work carries no release version. Hours of work, not architecture — and it's the first thing procurement asks."

### B14–B15 · Moments 1, 3, 6, 8, 10
**Visual:** `G-25` populated. The five technical moments held back from Deck A.

### B16 · Technical debt register
**Visual:** `G-34 Risk & Debt Register`.
**On-slide text:** `B-13` narrative binding · `T11` stale artifact, three dispositions un-materialised · `B-3` visual producer not fixture-equivalent · `B-16` no timeline slicing · no CI · ADR custody gap.

---

# DECK C — GOVERNANCE APPENDIX
### 12 slides · 30–40 minutes · Valerie · board · compliance · enterprise governance

### C1 · Governance authority boundaries
**Visual:** `G-35 Governance Authority Boundaries` — who may propose, who may ratify, who may refuse, who may never decide.

### C2 · The instrument classes
**On-slide text:** CAR → ADR → SPEC → PDR → ER, plus DOC · DOC-SRC · RE · DWR · Execution Gates. *ADRs govern the platform · PDRs govern productions · Reference Executions govern comparison.*

### C3 · Custody without authority
**Visual:** `G-14`.
**Speaker notes:** "Closer to a capability model than to RBAC — and applied to an AI agent."

### C4 · Evidence hierarchy
**Visual:** `G-09 Ratification Loop` with the five-stage cycle.
**On-slide text:** *"Evidence does not move. Products do."*

### C5 · Human oversight, tested
**Visual:** `G-19 Refusal Ledger`.
**Speaker notes:** "A policy saying a human is in the loop is not evidence. A recorded refusal of an authorised action, with the reason and the vindication, is."

### C6 · Separation of duties, with dissent on the record
**On-slide text:** the `EXECUTIVE_RULINGS` objection, verbatim, ending `recommendation: NONE — this is a governance decision, not an engineering one`.

### C7 · Fail-shut controls
**On-slide text:** a gate missing any required field is treated as CLOSED · **the aggregate is computed, never authored**.

### C8 · Regulatory defensibility
**On-slide text:** consent per person, publication rights **not inferred** · rights filtering at emission · AI disclosure **before** upload · retention clocks armed at approval · every artifact hash-pinned.

### C9 · The composite-score prohibition
**On-slide text:** *"Composite readiness, health, quality, maturity or intelligence scores are **PROHIBITED**"* — superseded only by an ADR that explicitly does so. **The platform explains rather than rates.**

### C10 · Governance succession — the open risk
**Visual:** `G-34 Risk & Debt Register`, governance rows.
**On-slide text:** **One ratifying authority. No quorum, no delegation instrument, no succession clause.**
**Speaker notes:** "This is the honest state of a one-person operation and it's a governance risk, not a feature. I'd put it first on a board risk register. Any enterprise adoption of this corpus needs a succession instrument that doesn't exist yet."

### C11 · Risk register
**Visual:** `G-34` full — likelihood × impact × owner × mitigation.

### C12 · What the system found about itself
**On-slide text:** two live risks disclosed — an AI-generated soundtrack in distribution with an unresolved rights posture, and a single ratifying authority with no succession.
**Speaker notes:** "Both were surfaced by the governance system, not by an external reviewer. That's the demonstration."

---

## DELIVERY NOTES

**Deck A run time:** 18 slides, 20–30 minutes. Act II is the longest and should be. If you must cut, cut Act III — the architecture is inferable from the story; the story is not inferable from the architecture.

**The three slides that carry Deck A:** A6 (eleven days), A13 (four refusals), A17 (disclosure). Everything else supports them.

**A17 is not optional.** Every audience this package names is trained to look for what a deck omits. Disclosing first converts the biggest vulnerability into the strongest credibility signal.

**Do not merge B or C into A.** The reason to have three decks is that A stays 20 minutes long. A technical question in an executive room is answered with *"there's a slide for that"* and one slide from Deck B — not by extending A.

**Tone.** Nine of the ten moments are failures. Deliver them level, without apology and without drama.
