# WET-EXEC MASTER PRESENTATION
## The Canonical Source · W.E. C.A.P.E.

**Issued under:** EXECUTIVE ORDER — WET-EXEC-005, Executive Producer / Chairman, 2026-08-29, BINDING
**Custody:** `PRESENTATION PACKAGE ONLY` · **Status:** `CANONICAL SOURCE`
**Repository measured at:** `0acf42a` · 2026-08-29T06:37:02Z

> ## CANONICAL RULE
> **All presentation variants derive exclusively from this file.**
> No derivative deck may introduce a fact not present here. No derivative deck is independently edited.
> **A discrepancy is resolved in favour of this document, and the derivative is corrected before certification.**

---

# 0 · HOW THIS SOURCE PREVENTS ITS OWN DRIFT

**The Canonical Rule creates a synchronisation problem this platform has already met once.**

`T11` is the platform's open finding that a committed artifact matches neither the generator that produced it nor its successor — **three dispositions un-materialised**, because a downstream product was allowed to hold a copy of an upstream truth. Four derivative decks each restating the same figures in prose would reproduce that failure exactly, in the presentation layer, and nobody would notice until a reviewer checked.

**The platform's own answer is `DOC-002` — regenerate, never patch — and the registry pattern: downstream artifacts cite by identifier; they do not hold copies.**

So this Master holds **numbered canonical facts (`M-nn`)** and **numbered canonical statements (`S-nn`)**. Derivative decks **cite the identifier**. A figure appears in exactly one place in this package, and drift becomes detectable by `grep` rather than by reading four documents side by side.

**Consequence for maintenance:** a re-measurement updates §1 of this file and nothing else. That is the property the Canonical Rule is actually asking for.

---

# 1 · CANONICAL FACTS

**Measured at `0acf42a`, 2026-08-29T06:37:02Z. Every fact carries its definition. No derivative may restate a value; it cites the identifier.**

## 1.1 · Repository

| id | fact | value | definition |
|---|---|---|---|
| `M-01` | Commits | **247** | `git rev-list --count HEAD` |
| `M-02` | Span | 2026-05-20 → 2026-08-29 | **102 days** |
| `M-03` | Tags | 7 | incl. `governance-v1.0` |
| `M-04` | Branches | 4 | local |
| `M-24` | Files under `docs/` | 101 | of which 92 are governance documents |

## 1.2 · The headline ratio

| id | fact | value | definition |
|---|---|---|---|
| `M-05` | **Governance documents** | **92** | Markdown files under `docs/` |
| `M-06` | **Engine modules** | **39** | non-test Python under `wecape/`, excluding `__pycache__` |
| `M-07` | **Ratio** | **2.36 : 1** | governance documents per engine module |

## 1.3 · Code and testing

| id | fact | value | definition |
|---|---|---|---|
| `M-08` | Engine lines | 5,802 | non-test Python under `wecape/` |
| `M-09` | **Test lines** | **5,823** | `wecape/tests/test_*.py` — **more test code than engine code** |
| `M-10` | Test modules | 42 | |
| `M-11` | Artifact-pipeline scripts | 31 | Python under `intelligence/` |
| `M-12` | Artifact-pipeline lines | 6,122 | |
| `M-13` | **Pipeline unit tests** | **0** | no file in `wecape/tests/` references `intelligence/` |
| `M-16` | Operational scripts | 25 | `.py` and `.sh` in `scripts/` |
| `M-17` | Runtime guards | **14** | executed before the first byte is written |
| `M-18` | Conformance result | **22 PASS / 0 FAIL** | + 6 negative tests, each exit 2 with 0 files written |

## 1.4 · Governance and knowledge

| id | fact | value |
|---|---|---|
| `M-19` | Ratified architecture clauses | **20** |
| `M-14` | Registries | **14** |
| `M-15` | Intelligence artifacts | 83 (excluding placeholders and OS files) |
| `M-20` | Riders registered | **75** (+5 civic speakers) · **25 marked `UNCONF`** |
| `M-21` | **ADRs in custody** | **2 of 9 cited** — `ADR-001`–`008` are cited and not in git |
| `M-22` | Deferred Work Register | 49 entries |
| `M-23` | Executive package documents | 7 |

## 1.5 · Production

| id | fact | value |
|---|---|---|
| `M-25` | Cameras | 4 systems · ~170 source files · 139 curated exports |
| `M-26` | Part 1 | published, 33:58, YouTube + Opus |
| `M-27` | Soundtrack | 8 tracks · DistroKid · **UPC 882436051388** · released 2026-08-04 |
| `M-28` | Processing improvement | **16×** (hardware decode) · NVMe contributed 2.96× separately |
| `M-29` | Pre-platform baseline | **64 hours**, filed *before* the platform's own production |
| `M-30` | Measured actuals | curation 38 h · Part 1 edit 12 h |
| `M-31` | Regeneration proof | 205,679 bytes → **7 changed lines, 5 changed bytes** |
| `M-32` | Densest day | **22 August — 32 commits, all governance** |
| `M-33` | The silence | **27 July – 7 August · 11 days · 0 commits** |

## 1.6 · Measurement drift — a live demonstration

**Between the WET-EXEC-003 basis (`db69f5b`, 05:34 UTC) and this measurement (`0acf42a`, 06:37 UTC) — one hour:**

```
commits              245 → 247
governance documents  90 →  92
executive documents    6 →   7
```

**The drift was caused by this package's own commits.** The package is a set of files in the repository it describes, so describing the repository changes it.

`S-00` · **A measured figure is true at a commit, not in general.** Every derivative deck carries the measurement commit and timestamp on its metrics slide, and **re-measurement precedes every presentation.** This is `DOC-001` — *validate the instrument before the measurement* — applied to the package itself.

---

# 2 · CANONICAL STATEMENTS

**Derivative decks quote these by identifier. They are not paraphrased.**

| id | statement | grade |
|---|---|---|
| `S-01` | **W.E. C.A.P.E. is a governed collaborative AI operating environment for deterministic creative production.** | `[E]` |
| `S-02` | **The documentary was never the destination. It became the proving ground.** | `[E]` |
| `S-03` | **We did not build a documentary. We built a governed AI platform, and validated it by producing a documentary.** | `[E]` |
| `S-04` | **Custody is not authority, and custody is immutable.** | `[E]` `ER-003` |
| `S-05` | **Evidence does not move. Products do.** | `[E]` `ER-004` |
| `S-06` | **The platform prepares decisions; it does not make artistic ones.** | `[E]` `DOC-CAND-001` |
| `S-07` | **An empty field remains empty.** | `[E]` `EPR-001 §2.3` |
| `S-08` | **Validate the instrument before the measurement.** | `[E]` `DOC-001` |
| `S-09` | **Regenerate, never patch.** | `[E]` `DOC-002` |
| `S-10` | **Evidence conflicts produce an explicit unresolved state; the platform never picks a silent winner.** | `[E]` `CAPE-RAT` cl. 20 |
| `S-11` | **A control artifact fails shut. The aggregate is computed, never authored.** | `[E]` `WET-SPEC-GATE-001` |
| `S-12` | **The platform explains rather than rates.** | `[E]` `WET-SPEC-REPORT-001` |
| `S-13` | **A control that has never fired is not a control. These fired.** | `[E]` four refusals |
| `S-14` | **A claim without a producing computation is not a measurement.** | `[E]` Moment 10 |
| `S-15` | **AI accelerated the work. Governance made it trustworthy. Human judgment made it valuable.** | `[E]` |
| `S-16` | **AI was not unnecessary. AI was insufficient — and the architecture made the combination trustworthy.** | `[E]` |
| `S-17` | **In this platform a specification is not a description of the system. It is a component of it.** | `[E]` |
| `S-18` | **A registry that has never been reused is a well-designed registry, not an appreciating asset.** | `[O]` `n = 1` |
| `S-19` | **The story of this platform is not what it became. It is what it did each time the evidence disagreed with it.** | `[E]` |
| `S-20` | **Twenty-five of seventy-five names are still marked unconfirmed. That is not a gap in the work. That is the work.** | `[E]` `M-20` |
| `S-21` | **Don't validate the comparison — make the wrong comparison unrepresentable.** | `[E]` Moment 10 |
| `S-22` | **You can audit what the system declined to do, not just what it did.** | `[E]` |
| `S-23` | **Documentation became production infrastructure — not documentation about the code, but documentation the code obeys.** | `[E]` |

---

# 3 · REQUIRED ADDITIONS — canonical text

## 3.1 · WHY THIS REPOSITORY EXISTS

**Two problems, and they are not the same problem.**

**The business problem** `[E]` — content production at scale is an ungoverned pipeline. Mixed-camera shoots produce incompatible metadata. Consumer tools silently misdate media. Rights and consent tracking is manual or absent. AI-assisted content has no provenance trail.

**The personal problem**, which the repository shows more honestly than prose `[E]` — `RIDER_REGISTRY.yaml` holds **75 riders** (`M-20`). **Twenty-five carry `name: UNCONF`.**

A third of the people who told their story cannot be reliably named from the evidence available. The registry marks them unknown rather than guessing. Every doctrine in this platform is a technical restatement of one commitment: **these people trusted us, and we will not put words in their mouths.**

**The engineering exists because the ethics demanded instrumentation.**

*Governing statement:* `S-20`

## 3.2 · WHAT IS W.E. C.A.P.E.?

`S-01` — and `S-02`.

Not a tool. Not a prompt framework. An **operating environment**: layers in which humans and AI channels do different kinds of work under different custody, and in which the same inputs produce the same outputs every time or the run stops.

```
┌────────────────────────────────────────────────────────────┐
│  PRODUCTION     what gets made          3-part series ·    │
│                                         8-track album      │
├────────────────────────────────────────────────────────────┤
│  ENGINEERING    what makes it,          M-06 modules ·     │
│                 deterministically       M-17 guards        │
├────────────────────────────────────────────────────────────┤
│  GOVERNANCE     what may be made,       M-05 documents ·   │
│                 and by whom             M-19 clauses       │
├────────────────────────────────────────────────────────────┤
│  INTELLIGENCE   what the evidence       4 engines ·        │
│                 means                   4 questions        │
├────────────────────────────────────────────────────────────┤
│  KNOWLEDGE      what is known, and      M-14 registries ·  │
│                 how certainly           M-20 riders        │
└────────────────────────────────────────────────────────────┘
```

**Read it bottom-up. Knowledge is the foundation, not the output.**

## 3.3 · GOVERNANCE FIRST

**The difference is not that this platform has governance. It is where governance sits in the sequence.**

```
   TRADITIONAL                    W.E. C.A.P.E.

   PROMPT                         GOVERNANCE      what may be done
     ↓                                ↓
   OUTPUT                         EVIDENCE        what is actually true
     ↓                                ↓
   REVIEW  ← governance          EXECUTIVE REVIEW human decision
     ↓       arrives here             ↓
   FIX                            ENGINEERING     implementation
                                      ↓
   A filter on output that        TESTING         proof
   already exists.                    ↓
   It can reject.                 PRODUCTION
   It cannot prevent.
                                  A precondition. Ungoverned output
                                  cannot be produced in the first place.
```

**Concretely** `[E]`: guard `G-01` compares the production identity of the context against the observation bundle **before the first byte is written.** The run exits 2 with **zero files produced**. In a review-last workflow, those files exist and review may or may not catch them.

**And the evidence that this is not a claim:** `SOP-06` — the publication gates — was *"committed pre-exercise (a platform first)"*, before the picture lock it governs. It caught real rights exposure the same evening.

## 3.4 · KNOWLEDGE COMPOUNDS

**Media → knowledge → registries → governance → institutional intelligence.**

Four levels of reuse, **different in kind, not degrees of the same thing.** Most AI workflows operate at level one and stop.

| level | what is reused | persists across | status |
|---|---|---|---|
| **1 · PROMPT** | the words you type | a session | universal · no advantage |
| **2 · KNOWLEDGE** | facts extracted once | a project | common · fragile — an ungoverned fact has no provenance |
| **3 · REGISTRY** | governed, cited, confidence-graded records | **every future production** | `[E]` exists · `[O]` compounding unproven |
| **4 · INTELLIGENCE** | **the apparatus that decides what counts as a fact** | **every future domain** | `[E]` exists · `[O]` compounding unproven |

**Level 3's argument, concretely** `[E]`: `RIDER_REGISTRY.yaml` records 75 riders, each with a timecode citation, a confidence level, a consent status, and for 25 an explicit `UNCONF`. **That record is usable by a person who was not present, five years from now, without re-watching the footage.**

**Level 4 is the level almost nobody reaches.** It is not the facts that transfer — it is the apparatus. `S-08` · `S-09` · `S-10` · `S-04` govern any evidence-bearing pipeline in any domain, and they were written for a motorcycle documentary. `ER-003`, `ER-004`, `DOC-001`, `DOC-002` and `WET-SPEC-REPORT-001` **contain nothing about video.**

**The honest boundary, and it belongs on the slide:** `S-18`. One production has been governed. `CAR-004`: *"value unproven until a second production exists to compare."* `[O]`

## 3.5 · WHY HUMAN + AI WAS REQUIRED

**Four things in this repository could not have been produced by a model working alone.** Each is evidenced.

**An AI cannot grant itself authority it does not have.** `ER-003` and `ER-004` were ratified by a human; the engineering channel only *proposed* the custody model. **A model can write a constitution. It cannot ratify one.** `[E]`

**An AI cannot decide what the film means.** Six emotional beats authored by the Executive, one at a time, transcribed verbatim across eleven registry versions. `S-07`. Twenty-five rider names remain `UNCONF` for the same reason. `[E]`

**An AI cannot be the one who refuses.** Four times the engineering channel declined explicitly authorised work — and **each refusal was escalated to a human who then decided.** A model refusing itself is a loop, not a control. `[E]`

**An AI cannot know which failure matters.** The eleven silent days (`M-33`) were found by reading an *absence* of records. The question *"why did nothing get committed for eleven days?"* comes from someone who knew what should have been there. `[E]`

```
     THIS PLATFORM              A PROMPT WORKFLOW

     Human Judgment                  Prompt
          │                            ↓
     Executive Authority             LLM
          │                            ↓
     Governance                     Output
          │
     Evidence                  Three steps. No custody
          │                    boundary. No refusal path.
     Engineering               No record of what was declined.
          │
     AI Collaboration          Nothing here can say
          │                    "I will not do that,
     Repeatable Production      and here is why."
```

`S-15` — and its converse, `S-16`.

## 3.6 · FINAL LEGACY SLIDE

```
        The documentary proved the platform.
                        ↓
        The platform produced knowledge.
                        ↓
        The knowledge became the asset.
                        ↓
        The governance became the differentiator.
                        ↓
        The methodology becomes the legacy.
```

**Each arrow is evidenced except the last, which is a projection and is graded as one.**

| link | grade | evidence |
|---|---|---|
| The documentary proved the platform | `[E]` | every ratified clause was purchased with a production failure |
| The platform produced knowledge | `[E]` | `M-14` registries · `M-20` riders |
| The knowledge became the asset | `[E]` exists · `[O]` compounding | `S-18` — `n = 1` |
| The governance became the differentiator | `[E]` | `ER-003`/`ER-004`/`DOC-001`/`DOC-002` contain nothing about video |
| **The methodology becomes the legacy** | **`[P]`** | **a projection. It requires adoption by someone who did not write it.** |

**The final line is the only one in this package written in the future tense, and it is graded `[P]` deliberately.** A legacy is conferred by other people. The platform can earn it and cannot declare it.

*Closing statement:* `S-19`, then `S-20`.

---

# 4 · THE TEN MOMENTS — canonical cards

Seven fields. **The second field is `THE POSITION ON RECORD`, never "what we believed"** — `ER-007 §3` prohibits the platform inferring Executive belief. Reflection is `ER-007` Executive Reflection content, `AWAITING_EXECUTIVE_DECLARATION`.

| # | moment | date · commit | position on record | evidence showed | decision | governance artifact | engineering | long-term principle |
|---|---|---|---|---|---|---|---|---|
| **1** | The gate declared green twice | 05-25 · `c899aa3` | *"Phase 0 retail gate GREEN"* | next commit restates it *"honest… status"*; smoke test follows | correct in the open; preserve both | the correction pattern → `DOC-001` | end-to-end smoke test as the gate's precondition | a claim that outruns its evidence is corrected in public |
| **2** | "All prior reports incorrect" | 06-22 · `d402855` | published free-space figures | reading OS volume not Data volume — 12 GB vs 314 GB | invalidate own published numbers; delete nothing | `DOC-001` — `S-08` | `sys_free_gb` reads via `Path.home()` | measurement is something the platform is **accountable for** |
| **3** | The specification lost to the field | 06-23 · `3973b19` | `RFQ` §7 — ±5 s window | **67 % ungrouped** at spec; ±15 s field-validated | change neither quietly; document the disagreement | the **formal deviation** artifact class | window widened, deviation cited in config | a wrong specification is written down, not fixed silently |
| **4** | Eleven days of silence | 07-27→08-07 · `M-33` | the platform was the production system | 11 days, 0 commits; Part 1 shipped around it | close the gap; make the closure permanent | `19727ef` — generator + `SOP-05` + record, one commit | scene clustering, lineage bridge, 80/80 reconciled | **finding → tool → doctrine → immutable record** |
| **5** | The timestamp that lied | 08-12 · `4d3cb49` | camera time authoritative, read as UTC | local wall-clock — proven by a 5-min mtime delta. **F1** | ratify the principle, not the parser | `CAPE-RAT` — `M-19` clauses | provenance + confidence on every timestamp; originals never rewritten | **software with documentation became law with an implementation** |
| **6** | Separation of Executive and Engineering authority | 08-20 · `27674d7` | `AIS-001` — the Chairman's vision | assessment: *"sound **with modifications**"* | ratify **with** modifications; preserve the assessment | **Chairman's Acceptance Memorandum** (new class) | DIE split; Transcript Authority as `UNCONF` marking | proposal and ratification are different artifacts with different custody |
| **7** | Custody is not authority | 08-22 · `72439ae` | custody was a filing question | the question needs *held* separated from *may decide* | three immutable custody classes | `ER-003` · `ER-004` — `S-04` · `S-05` | custody stamped on every generated artifact | **the conceptual breakthrough — every AI-governance claim rests here** |
| **8** | The second cut | 08-24 · `7771e44` | the 08-22 lock was the governed film | *"diverges at 00:03:27, runs 157.125 s shorter"* | **halt authorised work**; enumerate, recommend none | `CUSTODY_ALERT_001` · *"Do not recommend any option"* | forensic audit, custody `MACHINE`, inference `ZERO` | when identity is in question — stop, enumerate, refuse to recommend |
| **9** | The refusal to infer | 08-28 · `c7b5d3a` | an Order **authorised** regeneration | six preconditions unmet — would emit the wrong film | **refuse the authorised work** | `GER-001` · `EPR-001` ratified | `epr_validate.py` V-1..V-6; workbook with zero pre-filled values | `S-07` — **even when filling it was authorised** |
| **10** | `191 / 191` | 08-29 · `57c9ed1` | cited in three governed artifacts as the frame-accuracy licence | validator scored **1 of 191**; the figure was a hard-coded string | report, remediate, disclose what stays open | `ECR-GEN-002` conformance report | cardinality asserted **before** pairing; `M-17` guards; `M-18` | `S-14` |

**Nine of the ten are moments where the platform discovered it was wrong.** One — Moment 7 — is where it discovered what it had built. `S-19`.

---

# 5 · WHAT THE PACKAGE DOES NOT CLAIM
### canonical disclosure set — `D-01` … `D-13`

**Every derivative deck carries this set complete. It may be reordered; it may not be shortened.**

| id | disclosure |
|---|---|
| `D-01` | **No composite maturity, readiness or quality score** appears anywhere in this package |
| `D-02` | **The 85 % utilization figure and the ~45× density claim are not carried forward** — no governed artifact, measurement record, or producing computation exists. The utilization instrument is graded **PARTIAL** with *"No governed artifact class"* |
| `D-03` | **Seven constitutional decisions are not in version control** — `M-21` |
| `D-04` | **`GNB-001`, an Executive determination, is enforced but not filed** in any instrument with governance standing |
| `D-05` | **74.3 % of the artifact generator's emitted text is literal prose** (`B-13`) |
| `D-06` | **The artifact pipeline has no unit tests** — `M-12` lines, `M-13` |
| `D-07` | **No dependency manifest, no release version since 2026-05-27, no CI, no code signing, no independent security audit** |
| `D-08` | **The governance model has a single ratifying authority and no succession instrument** |
| `D-09` | **`CONDUCTOR_SCORE.yaml` is stale** — three generator dispositions un-materialised (`T11`) |
| `D-10` | **Every "mature" characterisation rests on `n = 1`** |
| `D-11` | **Instagram, community and education are not operating channels** — no repository artifact supports them |
| `D-12` | **The soundtrack rights posture is unresolved** — Suno commercial-use sufficiency and DistroKid AI-content policy compliance are `REQUIRES_SPECIALIST_REVIEW` |
| `D-13` | **The 08-24 production lineage has never been ingested** — four inputs absent |

**A deck that omitted these would fail this package's own evidence standard.** That they can be listed — precisely, with citations, by the system that found them — is the strongest single argument for everything else.

---

# 6 · DERIVATION MAP

| view | file | length | audience | derives |
|---|---|---|---|---|
| **Executive Summary** | `WET_EXEC_EXECUTIVE_SUMMARY.md` | 16 slides | executives · board · investors · partners · family | §3 in full · `S-01`…`S-04`, `S-13`…`S-20` · `M-01`, `M-05`–`M-07`, `M-14`, `M-17`–`M-20`, `M-26`–`M-33` · `D-01`…`D-13` |
| **Technical Architecture** | `WET_EXEC_TECHNICAL_ARCHITECTURE.md` | 32 slides | principal engineers · architects · security · AI researchers · technical founders | §4 in full · all `M-nn` · `S-04`…`S-14`, `S-17`, `S-21`, `S-22` · `D-01`…`D-13` |
| **Complete Reference** | `WET_EXEC_COMPLETE_REFERENCE.md` | 56 slides | archival | **everything** |

**No derivative introduces a fact absent from this file.** A derivative needing a new fact amends this file first.

---

# 7 · EVIDENCE GRADING

| grade | meaning |
|---|---|
| `[E]` | **Evidenced** — a governed artifact or repository record supports it, and it is cited |
| `[P]` | **Projection** — an opportunity, a design, a forward statement. Not evidenced |
| `[O]` | **Open** — a question raised and unresolved |

`WET-SPEC-REPORT-001` prohibits composite readiness, quality or maturity scores. **This package contains none, and none may be added to a derivative.**

---

*Canonical source. Prepared under EXECUTIVE ORDER WET-EXEC-005. Custody: PRESENTATION PACKAGE ONLY. No engineering artifact, registry, generator, Executive Order, narrative declaration, or production artifact was modified.*
