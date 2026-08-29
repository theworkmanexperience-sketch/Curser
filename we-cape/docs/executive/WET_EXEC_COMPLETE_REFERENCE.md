# WET-EXEC — COMPLETE EXECUTIVE REFERENCE
## W.E. C.A.P.E. · 56 slides · archival

> **DERIVED VIEW — the definitive presentation.** Canonical source: `WET_EXEC_MASTER_PRESENTATION.md`.
> Every fact cites an `M-nn` identifier; every principle quotes an `S-nn` statement; the disclosure set `D-01`…`D-13` appears complete. **This file introduces no fact absent from the Master and is never independently edited.**

**Audience:** complete archival reference — the full presentation from which any subset is drawn
**Repository measured at:** `0acf42a` · 2026-08-29T06:37:02Z — **re-measure before presenting**
**Constituent views:** `WET_EXEC_EXECUTIVE_SUMMARY.md` (16) · `WET_EXEC_TECHNICAL_ARCHITECTURE.md` (32)

---

## 0 · HOW TO USE THIS REFERENCE

This is the **complete** deck. It is not intended to be delivered end to end — at 56 slides it runs roughly two hours — but every slide in every other view exists here, in sequence, with its speaker notes.

**Three ways to use it:**

1. **As the archival record.** The presentation as it stood at `0acf42a`, complete.
2. **As the source for a bespoke deck.** Select slides by identifier; do not rewrite them.
3. **As the answer bench.** When a question exceeds a shorter deck, the slide already exists here.

**Slide identifiers** map to their source view: `E-nn` Executive Summary · `T-nn` Technical Architecture · `C-nn` Complete-only.

---

# PART I · WHY THIS EXISTS *(C1–C5)*

| # | slide | visual | content |
|---|---|---|---|
| **C1** | Twenty-five of seventy-five | `G-01` | `M-20` · *"We could have guessed twenty-five names. Nobody would ever have known."* |
| **C2** | Two problems | `G-02` | business problem · personal problem · **the engineering exists because the ethics demanded instrumentation** *(Master §3.1)* |
| **C3** | The founding tell | — | `2682811` — engine **and acceptance suite**, day one. Attorney-reviewed EULA, day three. **Legal instrumentation preceded the product.** |
| **C4** | A company inside a commit message | `G-07` | `f8c8878` — product rename, package rename, legal entity, IP reclassification, one atomic change |
| **C5** | The proving ground | `G-05` | `M-25` · `M-26` · `M-27` |

# PART II · WHAT IT IS *(C6–C12)*

| # | slide | visual | content |
|---|---|---|---|
| **C6** | The definition | `G-36` | `S-01` · `S-02` · five layers bottom-up |
| **C7** | What makes it an operating environment | — | deterministic `M-31` · governed `M-05` · collaborative *(two channels)* · fail-shut `M-17` · self-auditing *(Moment 10)* |
| **C8** | Repository architecture | `G-39` | nine-level authority chain · `S-09` · the broken link drawn, `D-09` |
| **C9** | Repository topology | `G-29` | `M-05` · `M-06` · `M-07` · `M-24` |
| **C10** | System components | `G-28` | `M-06`/`M-08` → intermediates → `M-11`/`M-12` → 7 artifacts; pipeline marked `M-13` |
| **C11** | Production workflow | `G-30` | swimlane, governance rail, human-decision glyphs |
| **C12** | Custody is not authority | `G-14` | `S-04` |

# PART III · THE JOURNEY *(C13–C20)*

| # | slide | visual | content |
|---|---|---|---|
| **C13** | 102 days | `G-47` | `M-01` · `M-02` · `M-03` · **`M-32`** |
| **C14** | Era I — governance first | — | gates before features; EULA day three; **governance existed before the platform had a name** |
| **C15** | Era III — engineering acceleration | — | 68 commits · `M-28` · the NLE bridge · *"all prior reports incorrect"* |
| **C16** | Era IV — measurement | — | `M-29` filed **before** the production it measures · `M-30` |
| **C17** | **The silence** | `G-06` | **`M-33`** — the gap drawn as a void |
| **C18** | Era V — findings become law | — | F1/F2 · chrono-sets locked as tool + doctrine + record in one commit · `M-19` ratified |
| **C19** | Era VI — constitution creation | `G-10` | assess → freeze → certify → ratify → specify → freeze → launch, **one day** · **`M-32`** |
| **C20** | Era VII — conformance certification | — | custody crisis · Executive authoring · `M-17` guards · `M-18` · `governance-v1.0` |

# PART IV · THE TEN DISCOVERIES *(C21–C30)*

**Seven-field cards, `G-25`. Master §4 carries the canonical content for all ten.**

| # | moment | long-term principle |
|---|---|---|
| **C21** | The gate declared green twice | a claim that outruns its evidence is corrected in public |
| **C22** | "All prior reports incorrect" | measurement is something the platform is **accountable for** |
| **C23** | The specification lost to the field | a wrong specification is written down, not fixed silently |
| **C24** | **Eleven days of silence** | **finding → tool → doctrine → immutable record** |
| **C25** | The timestamp that lied | **software with documentation became law with an implementation** |
| **C26** | Separation of Executive and Engineering authority | proposal and ratification are different artifacts with different custody |
| **C27** | **Custody is not authority** | **the conceptual breakthrough — every AI-governance claim rests here** |
| **C28** | The second cut | when identity is in question — stop, enumerate, refuse to recommend |
| **C29** | The refusal to infer | `S-07` — **even when filling it was authorised** |
| **C30** | **`191 / 191`** | `S-14` |

**C30a · The shape of all ten** — nine are moments where the platform discovered it was wrong; one is where it discovered what it had built. `S-19`

# PART V · GOVERNANCE *(C31–C38)*

| # | slide | visual | content |
|---|---|---|---|
| **C31** | Governance first | `G-37` | *(Master §3.3)* — governance as precondition, not filter |
| **C32** | Governance authority boundaries | `G-35` | the `decide` column has **exactly one mark**; `refuse` has two |
| **C33** | Instrument classes | — | CAR → ADR → SPEC → PDR → ER + DOC · DOC-SRC · RE · DWR · Gates |
| **C34** | Evidence hierarchy | `G-09` | `S-05` · `S-10` · clause 18 |
| **C35** | Fail-shut controls | — | `S-11` |
| **C36** | Non-interpolation | `G-16` | Invariant A and B · ordinal, non-numeric |
| **C37** | Separation of duties, dissent preserved | — | the `EXECUTIVE_RULINGS` objection, verbatim |
| **C38** | **Governance succession — the open risk** | `G-34` | **`D-08`** — one ratifying authority; no quorum, no delegation, no succession clause |

# PART VI · ENGINEERING *(C39–C46)*

| # | slide | visual | content |
|---|---|---|---|
| **C39** | Runtime guard lifecycle | `G-32` | `M-17` · pass path and fail path |
| **C40** | Negative test ledger | `G-17` | six faults, six stops, **zero files written** |
| **C41** | Observability of refusal | — | `S-22` · the four named stop conditions |
| **C42** | Testing hierarchy | `G-31` | four harnesses, **not additive** |
| **C43** | **The testing inversion** | `G-31b` | `M-08`/`M-09` against `M-12`/`M-13` · **`D-06`** |
| **C44** | Deterministic generation | `G-46` | `M-31` |
| **C45** | **The `zip()` that never compared** | `G-20` | 1 of 191 · `S-14` · `S-21` |
| **C46** | Engineering practice matrix | `G-42` | ten practices with evidence, and the honest gaps block at equal weight |

# PART VII · INTELLIGENCE & KNOWLEDGE *(C47–C50)*

| # | slide | visual | content |
|---|---|---|---|
| **C47** | Editorial Intelligence Stack | `G-15` | four layers, labelled by question · Progressive Intelligence · Transcript Authority |
| **C48** | Registries | — | `M-14` · `M-15` · `M-20` · timecode-cited · per-record confidence · `propagate_unknown` |
| **C49** | **Knowledge compounds** | `G-40` | four levels *(Master §3.4)* · **`S-18`** |
| **C50** | Media ecosystem | `G-44` | every node graded; every spoke originates at the **Knowledge Repository**, never at Capture · `D-11` |

# PART VIII · COLLABORATION *(C51–C53)*

| # | slide | visual | content |
|---|---|---|---|
| **C51** | The collaborative AI model | `G-38` | two channels, both `authority: NONE`; human at both ends |
| **C52** | Four refusals | `G-19` | `S-13` |
| **C53** | **Why human + AI was required** | `G-43` | *(Master §3.5)* · `S-15` · `S-16` · seven links against three, **true scale** |

# PART IX · COMMERCIAL & FUTURE *(C54–C56)*

| # | slide | visual | content |
|---|---|---|---|
| **C54** | Four value categories | — | **TIME** `M-28`/`M-29`/`M-30` · **PROCESS** `M-31` · **QUALITY** `S-22` · **VALUE** `M-14`, `[O]` compounding. **No projection, no sizing, no ask.** |
| **C55** | Gated strategic horizon **+ full disclosure** | `G-27` + `G-23` | Gates A–D · regulated verticals **detached** · **`D-01`…`D-13` complete** |
| **C56** | **Final legacy slide** | `G-48` | the five-link chain *(Master §3.6)*, **last link graded `[P]`** · `S-19` · `S-20` |

---

# PRESENTATION GUIDANCE

## Selecting a subset

| you have | deliver | source |
|---|---|---|
| 20–25 min, executive room | 16 slides | `WET_EXEC_EXECUTIVE_SUMMARY.md` |
| 45–60 min, technical room | 32 slides | `WET_EXEC_TECHNICAL_ARCHITECTURE.md` |
| 30–40 min, board / compliance | C1, C6, C12, C17, C31–C38, C51–C53, C55, C56 | this file |
| 10 min, hallway | C1, C6, C17, C27, C53, C55, C56 | this file |
| 2 hours, archival walkthrough | all 56 | this file |

**Never assemble a deck by rewriting slides.** Select by identifier. A slide that needs different content needs the **Master** amended first.

## The slides that carry any subset

**C17** — the eleven days. The pivot of the narrative, and negative evidence nobody expects.
**C27** — custody is not authority. The most portable idea in the corpus.
**C43** and **C45** — the testing inversion and the `zip()` bug. Both self-found, both disclosed before being asked. **These two are why a technical audience trusts the rest.**
**C53** — why human + AI was required. The only philosophical claim in the package, and it rests on four evidenced points.
**C55** — the disclosure set. **Never shortened.**

## Tone

Nine of the ten discoveries are failures. Deliver them level, without apology and without drama. **The candour is the product** — and every disclosure in `D-01`…`D-13` was surfaced by the governance system rather than by an external reviewer, which is the argument the whole package is making.

## The three rules that survive every subset

1. **No composite scores.** `WET-SPEC-REPORT-001` prohibits them; a deck about this platform cannot contain one.
2. **The disclosure set is complete or the deck is not certified.** `D-01`…`D-13` may be reordered, never shortened.
3. **Re-measure before presenting.** `S-00`. The figures drifted 245 → 247 in one hour between two revisions of this package, because the package is a set of files in the repository it describes.

---

# PRESENTATION CERTIFICATION

```
Package                    WET-EXEC presentation architecture
Canonical source           WET_EXEC_MASTER_PRESENTATION.md
Derived views              3  (Executive Summary · Technical Architecture ·
                               Complete Reference)
Supporting documents       6  (Briefing · Outline · Graphics Guide · Timeline ·
                               Commercial Strategy · Change Logs)

Canonical facts            M-01 … M-33   each with its definition
Canonical statements       S-00 … S-23
Disclosure set             D-01 … D-13   complete in every view
Graphics specifications    49

Repository measured        0acf42a · 2026-08-29T06:37:02Z
Prior basis                db69f5b · drift documented in Master §1.6

Evidence grading           PRESERVED in all views
Composite scores           NONE
Unsupported metrics        NONE
85% utilization figure     EXCLUDED  (D-02)
Independent derivative edits  NONE — all views cite Master identifiers
Engineering modifications  NONE
Registry modifications     NONE
Governance corpus          UNCHANGED

              PRESENTATION ARCHITECTURE COMPLETE
```

**Standing condition.** This certification attests that the package is internally consistent, evidence-graded, and accurate against the repository **as measured at `0acf42a`**. It does not survive repository drift, and the drift is measurable: `M-01` moved 245 → 247 and `M-05` moved 90 → 92 in the hour between the previous certification and this one.

**One governed presentation source. Multiple governed presentation views. Re-measure before every presentation.**

---

*Derived view. Canonical source: `WET_EXEC_MASTER_PRESENTATION.md`. Custody: `PRESENTATION PACKAGE ONLY`. No engineering artifact, registry, generator, Executive Order, narrative declaration, or production artifact was modified.*
