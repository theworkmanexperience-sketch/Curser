# WET-EXEC-002 — PRESENTATION OUTLINE · **VERSION 2.0**

> **CANONICAL SOURCE:** `WET_EXEC_MASTER_PRESENTATION.md` (WET-EXEC-005).
> **This outline is superseded as a delivery instrument by the three governed views** — `WET_EXEC_EXECUTIVE_SUMMARY.md` (16 slides) · `WET_EXEC_TECHNICAL_ARCHITECTURE.md` (32) · `WET_EXEC_COMPLETE_REFERENCE.md` (56). It is retained as the **design record** for Decks A/B/C and for its delivery notes. **Do not build a deck from this file**; build from a governed view. The Master governs any discrepancy.

**Revised under:** WET-EXEC-003 (finalization) · **WET-EXEC-004 (architecture narrative elevation)**
**Companion to:** `WET_EXEC_002_EXECUTIVE_BRIEFING.md` v2.0
**Targets:** Gamma AI · PowerPoint · Keynote
**Classification:** Technical & Governance Diligence Package · Platform Architecture Review
**Certification:** `EXECUTIVE PRESENTATION READY`

---

## 0 · THE NARRATIVE FRAME

**One sentence governs every slide in this package:**

> **We did not build a documentary. We built a governed AI platform, and validated it by producing a documentary.**

Wherever the older framing survives — *"a film project that grew a platform"* — it is replaced. The documentary is the **proving ground**, never the destination. Speaker notes throughout are written to that frame.

## 0.1 · Three decks, one source

| deck | length | audience | question answered |
|---|---|---|---|
| **A · Executive Story** | 30–35 min · **24 slides** | family, partners, executives, general | *What is it, why does it exist, why does it matter?* |
| **B · Technical Appendix** | 45–60 min · **18 slides** | Marcus, Desmond, principal engineers, CTOs, AI researchers | *How does it work, and where is it weak?* |
| **C · Governance Appendix** | 30–40 min · **14 slides** | Valerie, board directors, CHROs, compliance, enterprise governance | *How do I defend this to a regulator or a board?* |

**Deck A stands alone.** B and C deploy on question. A technical question in an executive room is answered with **one slide from Deck B**, never by extending Deck A.

**Three rules across all decks.** No composite scores. No 85 % utilization figure. Every metric carries its definition — and **re-measure before every presentation.**

---

# DECK A — EXECUTIVE STORY · 24 slides

## ACT I — WHAT THIS IS *(slides 1–7)*

### A1 · Twenty-five of seventy-five
**Visual:** `G-01 Rider Wall` — 75 tiles, 25 as outlines.
**Text:** 75 riders told us why they ride. 25 of their names could not be verified. **The registry says so.**
**Notes:** "We could have guessed twenty-five names. Nobody would ever have known. The system marks them UNCONF and refuses to fill the field. Everything that follows is an elaboration of that decision."

### A2 · Why this exists
**Visual:** `G-02 Split Panel`.
**Text:** Terabytes with no chain of custody · timestamps that lie · rights tracked by memory · AI content with no provenance.

### A3 · **What is W.E. C.A.P.E.?** *(new — Section A)*
**Visual:** `G-36 Five-Layer Platform Stack` — Knowledge · Intelligence · Governance · Engineering · Production.
**Text:** **A governed collaborative AI operating environment for deterministic creative production.**
**Notes:** "Not a tool. Not a prompt framework. An operating environment — layers where humans and AI do different work under different custody, and where the same inputs produce the same outputs or the run stops." *(beat)* "**The documentary was never the destination. It became the proving ground.**" *(beat)* "Read the stack bottom-up. Knowledge is the foundation, not the output."
**Evidence:** Briefing §3.

### A4 · Custody is not authority
**Visual:** `G-14 Custody vs Authority` — two orthogonal axes.
**Text:** **Custody is not authority, and custody is immutable.** An actor may hold, author, measure and enforce — and never decide.
**Notes:** "Hold this for the next twenty minutes. Everything that follows is a consequence of separating who touched a thing from who may decide about it."

### A5 · **Governance first** *(new — Section C)*
**Visual:** `G-37 Governance-First Comparison` — two columns, side by side.
**Text:** Traditional AI: Prompt → Output → Review → Fix. **W.E. C.A.P.E.: Governance → Evidence → Executive Review → Engineering → Testing → Production.**
**Notes:** "The difference isn't that we have governance. It's **where governance sits in the sequence.** In a review-last workflow, governance is a filter on output that already exists — it can reject, it cannot prevent. Here it's a precondition: ungoverned output can't be produced in the first place." *(beat)* "Concretely: a guard compares production identity before the first byte is written. The run exits 2 with **zero files produced.**"
**Evidence:** Briefing §5.

### A6 · **The collaborative AI model** *(new — Section D)*
**Visual:** `G-38 Collaborative AI Model` — two channels, both at zero authority.
**Text:** Executive Authority → Executive Orders → **Creative Direction (ChatGPT) · Engineering Channel (Claude)** → Verification → Governance → Executive Approval → Production.
**Notes:** "Two AI channels. Different custody, different work, **neither holds decision authority.** Every arrow begins and ends at a human — the channels occupy the middle exclusively." *(beat)* "**AI executes. Governance verifies. Authority remains human.**"
**Evidence:** `PR-001` records *"Creative Direction (ChatGPT) contributed the narrative and behavioural framing."* Briefing §6.

### A7 · The proving ground
**Visual:** `G-05 Production Stat Band`.
**Text:** 4 cameras · ~170 source files · 139 curated exports · 75 interviews · 3-part series · 8-track soundtrack in distribution.

## ACT II — WHAT THE EVIDENCE FORCED *(slides 8–14)*

> **This act wins the room. Do not soften it — the candour is the argument.**

### A8 · Eleven days of silence
**Visual:** `G-06 Commit Density Strip` — the gap as a void.
**Text:** 27 July – 7 August 2026 · **Zero commits.** Part 1 was edited and published in this window.
**Notes:** "The platform was not used to make it. We found that by reading the *absence* of records."

### A9 · The moment card
**Visual:** `G-25 Moment Card Template` — the seven-field card, empty.
**Notes:** "Ten times, evidence forced a change of direction. Each recorded identically. Note what the second field is *not* — it isn't 'what we believed.' The platform is prohibited from telling you what anyone believed. It can only show you what the record said."

### A10–A13 · Four moments
**Visual:** `G-25` populated. Deck A carries **Moments 2, 4, 5, 9**.
*(1, 3, 6, 7, 8, 10 move to Deck B — except Moment 7, which is already A4's thesis and returns as A15.)*

### A14 · Four refusals
**Visual:** `G-19 Refusal Ledger`.
**Notes:** "**A control that has never fired is not a control. These fired.**"

## ACT III — WHAT IT PROVES *(slides 15–20)*

### A15 · **Repository architecture** *(new — Section B)*
**Visual:** `G-39 Repository Authority Chain` — nine levels, Executive to Commercial.
**Text:** Every downstream artifact is **governed, not authored independently.**
**Notes:** "This isn't a folder structure. It's an authority chain — each level constrains the one beneath it. And any artifact can be regenerated from the level above. `DOC-002` makes that binding: **regenerate, never patch.** A correction is a new run, never an edit." *(beat)* "Where it's currently broken is on the disclosure slide."
**Evidence:** Briefing §4.

### A16 · **Knowledge compounds** *(new — Section F · central theme)*
**Visual:** `G-40 Four Levels of Reuse`.
**Text:** Prompt reuse → Knowledge reuse → **Registry reuse** → **Intelligence reuse**
**Notes:** "Most AI workflows operate at level one and stop. Prompt reuse saves typing — worthless when the model changes. Knowledge reuse saves research — but an ungoverned fact has no provenance, so you can't trust it at the moment it matters." *(beat)* "**Registry reuse is different in kind.** Seventy-five riders, each with a timecode citation, a confidence grade, a consent status, and for twenty-five of them an explicit UNCONF. **Usable by someone who wasn't there, five years from now, without re-watching the footage.**" *(beat)* "And level four is the one almost nobody reaches: it isn't the facts that transfer, it's **the apparatus that decides what counts as a fact.**" *(beat)* "The honest part: levels 3 and 4 exist. Their compounding is unproven. **n = 1.**"
**Evidence:** Briefing §8.

### A17 · **Repository scale** *(expanded — Section E)*
**Visual:** `G-41 Repository Scale Panel` — instrument counts with definitions.
**Text:** **90 governance documents** *(Markdown under `docs/`)* · **39 engine modules** *(non-test Python under `wecape/`)* · **2.3 : 1** · 20 ratified clauses · 14 registries · 14 runtime guards · 4 Executive Rulings · 7 CARs · 7 specifications · 8 PDRs · 6 doctrines · 22 PASS / 0 FAIL.
**Notes:** "**Documentation became production infrastructure**, and I mean that literally. A gate missing any required field is treated as CLOSED — the document *is* the control. A context whose declared values disagree with measurement **stops the build**. In this platform a specification isn't a description of the system. **It's a component of it.**"
**Evidence:** Briefing §11.

### A18 · **Engineering excellence** *(new — Section J)*
**Visual:** `G-42 Engineering Practice Matrix` — practice, implementation, evidence, and an honest gaps column.
**Text:** Fail-fast · deterministic generation · runtime guards · conformance validation · executive separation of authority · evidence grading.
**Notes:** "205,679 bytes of governed output regenerate with seven changed lines. A prompt framework has none of these ten practices — and none of the six gaps underneath them. **The gaps are the kind an infrastructure project has.**"
**Evidence:** Briefing §13.

### A19 · **Why W.E. C.A.P.E. could not have been built by AI alone** *(new — the essential slide)*
**Visual:** `G-43 Human Judgment Chain vs Prompt Chain` — seven links against three.
**Text:**
> **AI accelerated the work.**
> **Governance made it trustworthy.**
> **Human judgment made it valuable.**

**Notes:** "Four things here could not have been produced by a model working alone. **An AI cannot grant itself authority it doesn't have** — it can write a constitution, it cannot ratify one. **An AI cannot decide what the film means** — six emotional beats were authored by a human, one at a time, and twenty-five names stay unknown for the same reason. **An AI cannot be the one who refuses** — each of those four refusals was escalated to a human who then decided; a model refusing itself is a loop, not a control. **And an AI cannot know which failure matters** — the eleven silent days were found by someone who knew what should have been there." *(beat)* "And the honest converse: none of it could have been built by a human alone at this pace either. **The claim isn't that AI was unnecessary. It's that AI was insufficient — and the architecture is what made the combination trustworthy.**"
**Evidence:** Briefing §7.

### A20 · **Media ecosystem** *(expanded — Section K)*
**Visual:** `G-44 Ecosystem Reuse Map` — every node graded.
**Notes:** "Note the shape. **Every downstream node draws from the Knowledge Repository, not from the footage.** That's Progressive Intelligence enforced architecturally. Two channels are operating and evidenced; four are designed and marked as projections. I'd rather show you which is which."
**Evidence:** Briefing §15.

## ACT IV — WHERE IT GOES *(slides 21–24)*

### A21 · **Four tiers, no blurred boundaries** *(Section L)*
**Visual:** `G-45 Four-Tier Future` — CURRENT / NEAR TERM / LONG TERM / ASPIRATIONAL, each graded.
**Text:** Current `[E]` · Near term `[P]` with gates · Long term `[P]` with gates · **Aspirational: separate regulated programmes, not rungs.**

### A22 · Why now
**Visual:** `G-26 Why-Now Timing Panel`.
**Text:** Provenance becoming mandatory · human oversight being defined in regulation · AI content entering distribution ahead of rights frameworks · enterprises writing policy without reference implementations.

### A23 · What this deck does not claim
**Visual:** `G-23 Disclosure Panel` — deliberately undesigned. **Do not skip.**
**Text:**
- The 85 % utilization figure is **not carried forward** — no producing computation exists.
- Seven constitutional decisions (`ADR-001`–`008`) are **not in version control**.
- The 6,122-line artifact pipeline has **no unit tests**.
- **No dependency manifest, no release version since May, no CI, no independent security audit.**
- **One ratifying authority, no succession instrument.**
- `CONDUCTOR_SCORE.yaml` is stale — three dispositions un-materialised.
- Every "mature" characterisation rests on **n = 1**.
- The soundtrack rights posture is **routed to specialist review**.

**Notes:** "Every one of these was surfaced by the governance system, not by an outside reviewer. That we can list them precisely is the strongest argument for everything else."

### A24 · The gated horizon, and the close
**Visual:** `G-27 Gated Strategic Horizon`.
**Notes:** "We're before Gate A. Four production inputs are missing. And the highest-value thing available isn't a feature — **it's a second production**, because every compounding claim we make is unfalsifiable at n = 1." *(pause)* "Nine of the ten moments that changed this platform are moments where it discovered it was wrong. **The story isn't what it became. It's what it did every time the evidence disagreed with it.**" *(pause)* "Seventy-five riders told us why they ride. Twenty-five of those names are still marked unconfirmed. That isn't a gap in the work. **That is the work.**"

---

# DECK B — TECHNICAL APPENDIX · 18 slides

| # | slide | visual | key content |
|---|---|---|---|
| **B1** | System architecture | `G-28` | `wecape/` 39 modules / 5,802 LOC → intermediates → `intelligence/` 31 scripts / 6,122 LOC → 7 artifacts. **Pipeline block marked `0 unit tests`.** |
| **B2** | Repository topology | `G-29` | treemap; `docs/` and `wecape/` visually comparable — the 2.3 : 1 finding, spatial |
| **B3** | Production workflow | `G-30` | capture → offload → organise → conform → edit → observe → generate → gate → publish, with human-decision glyphs |
| **B4** | Testing hierarchy | `G-31` | four harnesses, **not additive**, each with *what it does not cover* |
| **B5** | The testing inversion | `G-31b` | engine 5,802 LOC / **5,823 test LOC**; pipeline 6,122 LOC / **0** |
| **B6** | Runtime guard lifecycle | `G-32` | 14 guards; pass path and fail path; write stage drawn as void when a guard fires |
| **B7** | Negative test ledger | `G-17` | six faults, six stops, **zero files written** |
| **B8** | The `zip()` that never compared | `G-20` | 1/191 at true scale → 191/191. *Make the wrong comparison unrepresentable.* |
| **B9** | The equivalence proof | — | 205,679 bytes · 7 changed lines · 5 changed bytes |
| **B10** | Parameterisation as diagnosis | — | 74.3 % literal prose *(38,056 of 51,237 chars, `traceability_scan.py`)* |
| **B11** | Deterministic generation | `G-46` | measured context; refuses on declared-vs-measured disagreement; `--run-id pinned` |
| **B12** | Local-first security | `G-33` | enforced network invariant, no egress from the engine path |
| **B13** | Observability of refusal | — | `FAILED_SOURCE_IDENTITY` · `FAILED_CARDINALITY` · `FAILED_COMPARISON` · `FAILED_TIMELINE_CLOSURE` |
| **B14** | Dependency & version disclosure | — | no manifest, no release tag since 2026-05-27 |
| **B15–B16** | Moments 1, 3, 6, 8, 10 | `G-25` | the five technical moments, seven-field cards |
| **B17** | Technical debt register | `G-34` | `B-13` · `T11` · `B-3` · `B-16` · no CI · ADR custody gap |
| **B18** | Knowledge compounds — technical view | `G-40` | why registry reuse is a *schema* property, not a content property |

---

# DECK C — GOVERNANCE APPENDIX · 14 slides

| # | slide | visual | key content |
|---|---|---|---|
| **C1** | Governance authority boundaries | `G-35` | responsibility grid; the `decide` column has **exactly one mark** |
| **C2** | Instrument classes | — | CAR → ADR → SPEC → PDR → ER + DOC · DOC-SRC · RE · DWR · Gates |
| **C3** | Custody without authority | `G-14` | closer to a capability model than RBAC — applied to an AI agent |
| **C4** | Governance-first sequencing | `G-37` | governance as precondition, not filter |
| **C5** | The collaborative AI model | `G-38` | two channels, zero authority, human at both ends |
| **C6** | Evidence hierarchy | `G-09` | *"Evidence does not move. Products do."* |
| **C7** | Human oversight, tested | `G-19` | four refusals — a policy is not evidence; a recorded refusal is |
| **C8** | Separation of duties, dissent preserved | — | the `EXECUTIVE_RULINGS` objection, verbatim |
| **C9** | Fail-shut controls | — | a gate missing a field is CLOSED; **the aggregate is computed, never authored** |
| **C10** | Regulatory defensibility | — | consent per person, rights not inferred · disclosure before upload · retention clocks · hash-pinning |
| **C11** | Composite-score prohibition | — | *"the platform explains rather than rates"* |
| **C12** | **Governance succession — the open risk** | `G-34` | one ratifying authority; no quorum, no delegation, no succession clause |
| **C13** | Risk register | `G-34` | likelihood × impact × **owner** × mitigation — an empty owner cell is a finding |
| **C14** | What the system found about itself | — | two live risks, both surfaced internally |

---

## DELIVERY NOTES

**Deck A run time:** 24 slides, 30–35 minutes. **Act II remains the longest and should be.** If you must cut, cut from Act III — the architecture is inferable from the story; the story is not inferable from the architecture.

**The four slides that carry Deck A:** **A3** (what it is), **A8** (eleven days), **A19** (could not have been built by AI alone), **A23** (disclosure). Everything else supports them.

**A19 is the slide to rehearse.** It is the one Marcus, Desmond and Valerie will each remember for different reasons, and it is the only slide in the package that makes a philosophical claim. Deliver it slowly and let the three lines land separately.

**A23 is not optional.** Every audience named is trained to look for what a deck omits.

**Do not merge B or C into A.** The reason to have three decks is that A stays 30 minutes.

**Tone.** Nine of the ten moments are failures. Deliver them level, without apology and without drama. **The candour is the product.**
