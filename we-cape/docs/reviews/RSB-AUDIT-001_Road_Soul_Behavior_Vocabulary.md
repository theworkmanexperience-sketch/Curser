# RSB-AUDIT-001 — Is Road Soul™ a governed musical language yet?
## Governance Status
Document Type: **Audit** — findings and recommendations only. **No implementation authorized.**
Date: 2026-08-22 · Prepared by: Implementation Engineer · For: Executive Review · **Amendment 1 appended (Executive rulings + three corrections)**
Prompted by: Executive Observation, 2026-08-22 (§1) · Subject: `CONDUCTOR_SCORE.yaml` v1.1.0
Method: every `behaviour_states` entry across all 15 cues and 3 conducted silences, tabulated. Counting, not opinion.

---

## 1. The observation under audit

> *"We're separating editing from composition. Most productions blur those together. WE CAPE is saying:
> 1. Determine where music belongs. 2. Determine why it belongs. 3. Only then compose it. … Road
> Soul™ won't just become a soundtrack — it will become a governed musical language whose behaviors
> can be explained, reproduced, and evolved without sacrificing artistry."*

Three claims are embedded here. They are not equally supported, so this audit takes them separately.

| claim | verdict | basis |
|---|---|---|
| **The process separates placement from composition** | **SUPPORTED — with one correction to the framing** (§2) | cue sheet → ESS/EVS → cue PDR → generation, all gated |
| **Road Soul behaves like a language** | **SUPPORTED, and by more evidence than the claim assumes** (§3) | a closed 10-state vocabulary and a family-determined grammar, both already present |
| **Its behaviors can be explained, reproduced, and evolved** | **NOT YET DEMONSTRABLE** (§4, §5) | 5 of 10 states carry no pass/fail test; the grammar is undeclared and unenforced; reproducibility has never been tested |

---

## 2. Correction to the framing — it is not editing vs composition

The separation is real. But **editing is not one of the two things being separated.** Picture is
locked. The ETC is frozen and hash-pinned. Editing finished before any of this began, and nothing in
the MIE pipeline can move it — SOP-06 B2 makes a picture change void the lock outright.

What is actually being separated is:

| | what it decides | who owns it | when |
|---|---|---|---|
| **Specification** | where music belongs, why it belongs, how it must behave | Executive Producer, via cue sheet + ESS/EVS + PDR | before there is any music |
| **Realization** | what the music *is* — notes, instruments, performance | MIE generation, then Executive selection | after, and only after |

**Specification vs realization**, both downstream of a lock neither may touch. Precision matters here
because "separating editing from composition" suggests picture and music are being negotiated against
each other. They are not. Picture won that negotiation before the process started, and every cue
boundary in ESS-002 is a question about **fitting music to a finished edit** — which is exactly why
EVS-001's boundary question is decidable from picture alone.

*This is a sharpening of the observation, not a disagreement with it.* The discipline the Executive
identified is real and unusual. It is just more constrained — and therefore stronger — than the
phrasing implies.

---

## 3. The finding that supports the "language" claim more than expected

`CONDUCTOR_SCORE.yaml` v1.1.0 already contains a **closed vocabulary of 10 behaviour states**, and
**family determines which states a cue gets.** Neither fact is written down anywhere. Both are
measurable from the artifact today.

### 3.1 The vocabulary — 10 states, no more

| state | cues using it | carries a number? | parameter |
|---|---|---|---|
| `ENTER` | 13 / 15 | **no** | — |
| `DUCK` | 13 / 15 | **yes** | `target_db`, `sidechain` |
| `REBUILD` | 13 / 15 | **yes** | `budget_s` |
| `HANDOFF` | 13 / 15 | **no** | — |
| `SUSTAIN` | 8 / 15 | **no** | — |
| `LEAD` | 5 / 15 | **no** | — |
| `BREATHE` | 4 / 15 | **yes** | `max_gain_db`, `permitted_between_answers` |
| `APPROACH` | 2 (silences) | **yes** | `window_s` |
| `FLOOR` | 2 (silences) | **no** | — |
| `RETURN` | 2 (silences) | **yes** | `window_s` |

### 3.2 The grammar — family determines the state set

| family | cues | state signature |
|---|---|---|
| **CONVERSATION** | CUE-02a, 02b, 02c, 04 | `ENTER · SUSTAIN · DUCK · REBUILD · HANDOFF · BREATHE` |
| **MOTION** | CUE-03, 07 | `ENTER · LEAD · DUCK · REBUILD · HANDOFF` |
| **CELEBRATION** | CUE-08, 09a, 09b | `ENTER · LEAD · DUCK · REBUILD · HANDOFF` |
| **REFLECTION / LEGACY** | CUE-01, 05, 06, 10 | `ENTER · SUSTAIN · DUCK · REBUILD · HANDOFF` |
| **conducted silence** | SIL-01, SIL-02, R46 | `APPROACH · FLOOR · RETURN` |

**Four signatures across five families, with zero exceptions in 15 cues.** `BREATHE` appears only in
CONVERSATION. `LEAD` appears only in MOTION and CELEBRATION. `SUSTAIN` and `LEAD` are mutually
exclusive in every cue. That is a grammar — a finite rule that predicts which states a cue will carry
from a single attribute.

### 3.3 The action strings are converging on their own

If the `action` fields were free prose, 13 uses of `ENTER` would produce ~13 different sentences.
They do not:

| state | uses | distinct strings |
|---|---|---|
| `ENTER` | 13 | **3** |
| `HANDOFF` | 13 | **3** |
| `SUSTAIN` | 8 | **2** |
| `LEAD` | 5 | **1** |
| `REBUILD` | 4 | 2 *(differ only in a measured gap figure)* |
| `DUCK` · `APPROACH` · `FLOOR` · `RETURN` | 2–4 | **1 each** |

Thirty-nine `action` values reduce to **fourteen distinct behaviors.** A vocabulary that compresses
like that is not prose that happens to repeat. It is a language that has not been told it is one.

**This is the audit's headline: Road Soul already behaves like a language. It is not yet *governed* as
one.** The distance between those two is a specification, and the specification is mostly
transcription of what the artifact already contains.

---

## 4. What is missing — five gaps, ranked

| # | gap | why it blocks the claim | priority |
|---|---|---|---|
| **G1** | **No state is defined anywhere.** There is no document stating what `ENTER` means, what fields it requires, or what would make an implementation non-conforming. Every definition is implicit in an `action` sentence | "explained" fails. A behavior that exists only as a sentence inside one cue cannot be cited, tested, or taught | **P1** |
| **G2** | **The vocabulary is not declared closed.** Nothing states there are ten states. Nothing prevents cue 16 from introducing `SWELL`, and nothing would flag it | "evolved" fails. Evolution needs a baseline to evolve *from* and an amendment path | **P1** |
| **G3** | **The family→signature grammar is emergent, undeclared, unenforced.** It holds in 15 of 15 cues by convention, not by rule | A regularity no validator checks is a coincidence waiting to break | **P1** |
| **G4** | **5 of 10 states carry no pass/fail test.** `ENTER`, `SUSTAIN`, `LEAD`, `HANDOFF`, `FLOOR` are prose-only. You cannot determine whether a delivered cue satisfies them | **"reproduced" fails outright.** This is the load-bearing gap — see §5 | **P1** |
| **G5** | **Required vs optional is unstated.** `SUSTAIN` appears in 8 of 15 cues. Is a MOTION cue without `SUSTAIN` conforming, or defective? Nothing says | Ambiguity here defeats any validator built on the other four | **P2** |

### 4.1 One structural risk worth naming separately
**MOTION has only two cues — CUE-03 and CUE-07 — and CUE-03 is the one currently under dispute.**
The MOTION grammar therefore rests on the thinnest evidence of any family, while carrying the
decision in front of the Executive right now. Whatever EVS-001 rules about CUE-03 becomes **half the
evidence base for how MOTION behaves.** CUE-07 RIDE_PASSAGE is the only independent check, and it is
unscored today.

---

## 5. The test the reproducibility claim must pass

*"Reproducible"* has a specific meaning, and it is not "we wrote it down."

> **The reproducibility test.** Give two independent realizations — two composers, two generation
> runs, two candidate sets — the same behavior specification for the same span. If both satisfy the
> same pass/fail criteria, the specification is reproducible. If satisfaction cannot be determined
> without asking the person who wrote the spec, it is not a specification. It is a preference with
> formatting.

**Current state against that test:**

| state | testable today? | the test, or what is missing |
|---|---|---|
| `DUCK` | **YES** | −18 dB under dialogue; the Yield Law's fail condition (*"any word requiring effort fails the candidate regardless of musical merit"*) is a genuine, checkable criterion |
| `REBUILD` | **YES** | return to bed level within `budget_s`, measured per span |
| `BREATHE` | **YES** | ≤ `max_gain_db` between answers, returning before the next question |
| `APPROACH` · `RETURN` | **YES** | within `window_s` of the boundary |
| `ENTER` | **no** | *"≤2 s"* is testable; *"never a downbeat announcement"* and *"on a movement, not on a cut"* are not, as written |
| `HANDOFF` | **no** | *"crossfade ≤4 s"* is testable; *"inaudible as an event"* is not |
| `SUSTAIN` | **no** | *"zero builds, zero drops, zero risers"* is nearly testable — it needs a definition of "build" |
| `LEAD` | **no** | *"ambient engine and crowd sound must remain audible"* — audible relative to what, measured how? |
| `FLOOR` | **partly** | *"no tail, no reverb return bleeding across the boundary"* is testable against the FCPXML; *"absolute silence"* is now defined by the ESS-004 provenance test |

**Score: 5 of 10 testable, 1 partly, 4 not.** The four untestable states are the ones that carry the
artistry — which is exactly why they resisted quantification, and exactly why leaving them prose
means the claim *"reproduced without sacrificing artistry"* is currently unearned.

**The encouraging half:** the five that *are* testable were quantified without visible loss. `DUCK`
with a decibel target and a fail condition is not a lesser behavior than `DUCK` as a sentence — it is
the same behavior, now arguable. There is no evidence in this artifact that quantification costs
artistry. There is evidence that it has not been attempted on the remaining four.

---

## 6. Recommendation — one specification, mostly transcription

**`WET-SPEC-RSB-001` — Road Soul Behavior Vocabulary.** Recommended, not authorized.

Contents, in dependency order:

1. **The closed vocabulary** — ten states, declared closed, with an amendment path (G2).
2. **A definition per state** — what it means, required fields, optional fields, what makes an
   instance non-conforming (G1, G5).
3. **The family grammar** — the four signatures in §3.2, declared as a rule rather than a pattern,
   with a validator that fails a cue carrying a state its family does not license (G3).
4. **A pass/fail test per state** — the five that exist, transcribed; the five that do not,
   *drafted and marked `PROVISIONAL` until exercised* (G4). Do not force a number where none is
   honest — an explicitly provisional test is governance; a fabricated threshold is not.
5. **Two worked examples** — one CONVERSATION cue, one MOTION cue, showing a conforming and a
   non-conforming instance of each state.

**Cost.** Items 1–3 are transcription of the artifact as it stands; the content already exists and
this audit contains most of it. Item 4 is the real work, and only for four states. Item 5 is a day.

**Sequencing — and a caution.** This is a **P1 recommendation with a deliberate P2 start.** Writing
the vocabulary before CUE-03 and CUE-07 exist risks freezing the MOTION grammar on two unrealized
cues (§4.1) — the same premature-freezing risk that `ESS-002` §A2.4 names for the boundary. The
recommended order:

> ESS-002 boundary → CUE-03 realized → CUE-07 realized → **then** write `WET-SPEC-RSB-001` from four
> families with evidence rather than three families with evidence and one with a plan.

Items 1–3 could be written today and would be correct today. Item 4's MOTION tests should not be.

---

## 7. Register entries raised by this audit

| id | title | class | priority |
|---|---|---|---|
| `DWR-039` | Road Soul behaviour vocabulary is undeclared, undefined and unenforced | IMPLEMENTATION | P1 |
| `DWR-040` | 4 of 10 behaviour states carry no pass/fail test — reproducibility untestable | DECISION | P1 |
| `DWR-041` | MOTION family grammar rests on two cues, neither realized | IMPLEMENTATION | P2 |

## 8. What this audit does not do
No specification is written. No state is defined. No validator is built. No cue is changed. This is
observation, classification and recommendation, returned for Executive Review — per the standing
constraint on reviews.

---

## Appendix A — the claim, restated at the confidence the evidence supports

> Road Soul is **already** a musical language: ten behaviors, a family-determined grammar, and
> thirty-nine specifications that compress to fourteen distinct behaviors — none of it declared,
> all of it consistent across fifteen cues.
>
> It is **not yet** a *governed* language, and the gap is precise: four of its ten behaviors cannot
> be checked by anyone who did not write them.
>
> Closing that gap is the difference between a house style and a specification. The evidence so far
> says the closing is affordable and has not yet cost any artistry — but that evidence comes from the
> five easiest states, and the four that remain are the ones that carry the music.


---

# Amendment 1 — 2026-08-22: Executive rulings recorded, with three corrections

The Executive accepted DWR-039/040/041 as classified and added four things: a **four-layer stack**, a
**three-class test taxonomy**, the **Conductor's Score / Road Soul distinction**, and a direction to
stop theorizing and hold EVS-001. All four are recorded here. **No specification is written and none
is authorized** — this amendment is the record, not the work.

## A1.1 The Road Soul stack — ACCEPTED

```
Lexicon      the words          ENTER · LEAD · BREATHE · HANDOFF
   ↓
Grammar      the rules          which words are legal, where, in what order
   ↓
Behaviour    the meaning        what each word actually requires
   ↓
Composition  the music          the artistic realization
```

This is the right decomposition, and it does something the audit did not: it separates **Lexicon**
from **Behaviour**. The audit treated "the vocabulary exists but is undefined" as one gap (G1+G2). The
stack correctly makes it two layers — you can close the Lexicon (declare the ten words, close the set)
without yet closing Behaviour (define what each requires). **That is a cheaper first step than the
audit proposed**, and it is the half that is pure transcription.

## A1.2 The three test classes — ACCEPTED, with the examples corrected

| class | meaning | verdict |
|---|---|---|
| **Type A** | machine-testable | accepted |
| **Type B** | observable now, measurable eventually | accepted — this is the class the audit was missing, and it is the important one |
| **Type C** | Executive judgement, may never quantify | accepted **with a guardrail** (§A1.5) |

**Type B is the real contribution.** The audit offered a binary — testable or prose — which forced
every hard behaviour into the same bucket as the impossible ones. Type B says: *this is checkable by a
person today, and the criterion is stable enough that a measurement may be found later.* That is both
honest and progressive, and it is where most of the four untestable states actually belong.

### Correction 1 — the Type C example is misattributed

> *"Type C · Executive Judgement · Example: `LEAD → Never a downbeat announcement.`"*

**"Never a downbeat announcement" is not `LEAD`. It is `ENTER`**, and it appears in exactly four cues —
CUE-02a, 02b, 02c, 04, all CONVERSATION:

> `ENTER`: *"fade-in ≤2 s under the preceding handoff; **never a downbeat announcement**"*

`LEAD`'s actual text, identical across all five cues that carry it (CUE-03, 07, 08, 09a, 09b), is:

> `LEAD`: *"music carries the span; ambient engine and crowd sound sit under it but **must remain audible**"*

**This changes the classification.** *"Ambient sound must remain audible"* is not a judgement that
resists measurement — it is an **audibility relationship between two signals**, which is Type B and
plausibly becomes Type A once a ratio is chosen. The genuine Type C candidate in the same sentence is
`ENTER`'s *"never a downbeat announcement"*, which asks whether a musical entry reads as an
**announcement** — a question about perceived rhetorical function, not level.

Corrected assignment, offered as a starting point and **not** as a completed classification:

| state | proposed class | why |
|---|---|---|
| `DUCK` · `REBUILD` · `BREATHE` · `APPROACH` · `RETURN` | **A** | already carry numeric criteria |
| `FLOOR` | **A** | the ESS-004 provenance test made it machine-checkable from the FCPXML |
| `LEAD` | **B → plausibly A** | audibility of ambient under music is a measurable relationship |
| `HANDOFF` | **B** | *"inaudible as an event"* is observable now; a transient-detection test is conceivable |
| `SUSTAIN` | **B** | *"zero builds, zero drops, zero risers"* needs only a definition of "build" |
| `ENTER` | **A + C, split** | *"≤2 s"* is Type A. *"Never a downbeat announcement"* is Type C |

**`ENTER` is the finding here: a single state carrying both a Type A and a Type C criterion.** The
taxonomy must classify **criteria**, not states — several states will split the way `ENTER` does.

### Correction 2 — two of the four grammar rules cannot be checked against the artifact

| rule | kind | status |
|---|---|---|
| *BREATHE only in CONVERSATION* | set-constraint | **VERIFIED — 0 violations.** All 4 CONVERSATION cues carry it; no other cue does |
| *LEAD forbidden during SILENCE* | set-constraint | **VERIFIED — 0 violations.** Silences carry only `APPROACH · FLOOR · RETURN` |
| *LEAD never follows LEAD* | **transition-constraint** | **UNCHECKABLE** |
| *HANDOFF cannot begin inside DUCK* | **transition-constraint** | **UNCHECKABLE** |

**Why:** `behaviour_states` is a **set**, not a **machine**. Every field ever used on a behaviour state
is `state · action · target_db · sidechain · budget_s · max_gain_db · permitted_between_answers ·
window_s`. **There is no field expressing time, order, sequence, or transition condition anywhere in
the artifact.** The list *reads* chronologically — ENTER, SUSTAIN, DUCK, REBUILD, HANDOFF — but nothing
declares that, and `DUCK`/`REBUILD` plainly recur throughout a cue rather than occurring once in
sequence.

Half of the proposed Grammar layer therefore has a prerequisite the audit did not identify: **a state
transition model.** Until states have entry conditions, exit conditions and legal successors, rules
about what may follow what have nothing to bind to.

*This is not an argument against the rules.* Both transition rules are musically sound. It is an
argument that the Grammar layer costs more than the Lexicon layer, and that the two should not be
scheduled as one job. → **`DWR-042`.**

### Correction 3 — the Conductor's Score / Road Soul distinction finds a live violation

> *"Conductor's Score is behavior. Road Soul is expression. One governs. One performs. Those should
> never be merged."*

**Accepted, and it is the sharpest thing said today.** Applied to the artifact, it immediately finds
something:

`CONDUCTOR_SCORE.yaml` carries `instrumentation_guidance` on **13 of 15 cues**, with fields
`colour · instruments · tempo · tonality · prohibited` — for example *"fingerpicked or clean electric
guitar, pad, brushed kit or no kit, low strings; slow to mid; warm major or dorian."* Each cue also
carries `road_soul_family`.

**That is expression, sitting inside the behaviour artifact.** By the distinction just drawn, colour,
instruments, tempo and tonality belong to Road Soul; only `prohibited` reads as behaviour, and only
where it is phrased as a constraint on function (*"no percussion transients that read as an event"*)
rather than on material.

The principle is right and the artifact does not yet obey it. **Flagged, not fixed** — splitting the
artifact now would be exactly the restructuring the Executive just deprioritized, and it would land
on `CONDUCTOR_SCORE` while ESS-002 is still open against it. → **`DWR-043`.**

## A1.5 The guardrail Type C needs

> *"Not everything should become math."*

Agreed, without reservation. But **Type C carries a price that should be stated once, in writing,
before the class is used:**

1. **A Type C criterion can never be validated without the Executive in the room.** Every cue carrying
   one is a standing, recurring call on Executive attention — per cue, per candidate, per revision,
   for the life of the production and every production after it. That is a real operating cost, and
   it is the correct cost for genuinely irreducible judgements. It is a bad cost for a behaviour that
   was merely hard to think about on the day.
2. **Without a rule, Type C becomes the drawer.** Anything difficult ends up there, and the
   classification stops carrying information.

**Recommended, not authorized:** a Type C assignment records **(a)** why the criterion resists
measurement — a stated reason, not a shrug — and **(b)** a re-review trigger, so the classification is
revisited rather than inherited. Type C should be **provisional by default and permanent only by
decision.**

## A1.6 Direction accepted — this document stops here

> *"I think we're ready to stop theorizing and start validating. The next milestone is no longer
> another governance document. It's EVS-001."*

**Accepted.** No specification is written. No state is classified beyond the starting point offered
above. No artifact is split. `WET-SPEC-RSB-001` remains sequenced behind CUE-03 and CUE-07
(`DWR-041`), and now behind a transition model as well (`DWR-042`).

**Register entries raised by this amendment:**

| id | title | class | priority |
|---|---|---|---|
| `DWR-042` | Behaviour states carry no transition model — half the Grammar layer is unbindable | IMPLEMENTATION | P2 |
| `DWR-043` | Expression content sits inside CONDUCTOR_SCORE, contrary to the governs/performs distinction | DECISION | P2 |

---
*Amendment 1 recorded 2026-08-22. Findings and corrections only. No implementation authorized.*
