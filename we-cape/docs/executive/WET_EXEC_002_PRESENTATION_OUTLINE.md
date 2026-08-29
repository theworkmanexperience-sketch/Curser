# WET-EXEC-002 — PRESENTATION OUTLINE

**Companion to:** `WET_EXEC_002_EXECUTIVE_BRIEFING.md`
**Targets:** Gamma AI · PowerPoint · Keynote
**Format:** 24 slides · ~30 minutes · heavy graphical treatment
**Custody:** `DOCUMENTATION ONLY`

---

## HOW TO USE THIS OUTLINE

Each slide carries five fields. Build in this order — **the visual is specified before the text**, because a heavy-graphics deck fails when copy is written first and pictures are retrofitted.

- **Objective** — the one thing the slide must land
- **Visual** — the graphic, specified by name from `WET_EXEC_002_GRAPHICS_GUIDE.md`
- **On-slide text** — what the audience reads (keep to what is written here; resist adding)
- **Speaker notes** — what is said aloud
- **Evidence** — the citation, for the appendix and for diligence

**Two rules for the whole deck.** No slide carries a composite score — the platform's reporting standard prohibits it. No slide carries the 85 % utilization figure — it has no producing computation.

---

## ACT I — THE PROBLEM AND THE PERSON (slides 1–5)

### Slide 1 · Twenty-five of seventy-five
**Objective:** open on the human stake, not the technology.
**Visual:** `G-01 Rider Wall` — 75 tiles, 25 rendered as outlines rather than fills.
**On-slide text:**
> 75 riders told us why they ride.
> 25 of their names could not be verified.
> **The registry says so.**

**Speaker notes:** "This is the whole platform in one slide. We could have guessed twenty-five names. Nobody would ever have known. Instead the system marks them UNCONF — unconfirmed — and refuses to fill the field. Everything I'm about to show you is an elaboration of that decision."
**Evidence:** `RIDER_REGISTRY.yaml` — 75 riders, 25 `name: UNCONF`, 5 civic speakers.

### Slide 2 · The problem nobody governs
**Objective:** name the market pain in executive terms.
**Visual:** `G-02 Split Panel` — ungoverned pile vs. governed rail.
**On-slide text:** Terabytes with no chain of custody · timestamps that lie · rights tracked by memory · AI content with no provenance.
**Speaker notes:** "A camera wrote wall-clock time and our pipeline read it as UTC. Five hours of error, invisible to any user. We caught it — because the registry's own data caught it, in a five-minute modification-time delta."
**Evidence:** finding F1, `4d3cb49`.

### Slide 3 · The thesis
**Objective:** state the founding position in one line.
**Visual:** `G-03 Authority Pyramid` — Custody → Evidence → Intelligence → Human Decision.
**On-slide text:**
> **The engines propose. Humans decide.**
> Governance was not added to an AI platform. It was the foundation.

**Speaker notes:** "Note the order. This predates the AI features."
**Evidence:** `DOC-CAND-001` §4.0.

### Slide 4 · One founder, two roles
**Objective:** executive-maturity evidence without bureaucracy theatre.
**Visual:** `G-04 Authority Diagram` — Chairman ⇄ Engineering channel ⇄ git custody.
**On-slide text:** Workman Experience Technologies LLC · W.E.I.C.P. governing body · proposal and ratification held as separate artifacts.
**Speaker notes:** "A company was incorporated inside a commit message on 19 June. One atomic change: product rename, package rename, legal entity, IP reclassification."
**Evidence:** `f8c8878`.

### Slide 5 · The proving ground
**Objective:** real production scale.
**Visual:** `G-05 Production Stat Band`.
**On-slide text:** 4 cameras · ~170 source files · 139 curated exports · 75 interviews · 3-part series · 8-track soundtrack in distribution.
**Speaker notes:** "Smyrna, Tennessee. Four days in June. Everything after this is a consequence of what that shoot broke."
**Evidence:** `PMR-001`.

---

## ACT II — WHAT THE EVIDENCE FORCED (slides 6–12)

> **This is the act that wins the room.** It is a sequence of moments where the platform discovered it was wrong. Do not soften them — the candour is the argument.

### Slide 6 · Eleven days of silence
**Objective:** the turning point.
**Visual:** `G-06 Commit Density Strip` — the gap rendered as a void, not a low bar.
**On-slide text:**
> 27 July – 7 August 2026
> **Zero commits.**
> Part 1 was edited and published in this window.

**Speaker notes:** "The platform was not used to make it. We found that by reading the *absence* of records. Within days: scene clustering, a lineage bridge, and a chronological-sets import — locked in as tooling, doctrine, and a hash-pinned record in a single commit."
**Evidence:** repository history; `19727ef`.

### Slide 7 · All prior reports incorrect
**Objective:** the honesty reflex, in the author's own words.
**Visual:** `G-07 Commit Callout` — the raw commit message, monospaced, oversized.
**On-slide text:** the verbatim message.
**Speaker notes:** "Twelve gigabytes versus three hundred and fourteen. Four words invalidating his own published numbers. Nothing was deleted. This is the intellectual birth of our first doctrine: validate the instrument before the measurement."
**Evidence:** `d402855`.

### Slide 8 · When the spec lost to the field
**Objective:** deviation as an artifact class.
**Visual:** `G-08 Before/After Bar` — 67 % ungrouped at spec vs. field-validated value.
**On-slide text:** ±5 s specified · ±15 s measured · **the disagreement was documented, not resolved by editing either side.**
**Evidence:** `3973b19`.

### Slide 9 · From finding to law
**Objective:** the pattern that defines the platform.
**Visual:** `G-09 The Ratification Loop` — Finding → Tool → Doctrine → Hash-pinned record.
**On-slide text:** 20 ratified architecture clauses, every one purchased with production evidence.
**Speaker notes:** "Clause 20: evidence conflicts produce an explicit unresolved state. The platform never picks a silent winner. That clause exists because a camera lied to us about time."
**Evidence:** `CAPE-RAT-20260813`.

### Slide 10 · Constitution day
**Objective:** governance accelerates; it does not slow.
**Visual:** `G-10 Single-Day Timeline Strip` — 20 August, seven governance commits.
**On-slide text:** Assess → freeze at a hash → certify → ratify → specify → 12 modifications → freeze under tag → launch sprint. **One day.**
**Speaker notes:** "And in the middle of it, a paste error in the specification being frozen — caught by a size-reconciliation check. The governance process auditing its own authoring."
**Evidence:** `51d31e2`, `27674d7`, `546918b`, `870ef07`.

### Slide 11 · The densest day is a governance day
**Objective:** kill the process-tax objection with data.
**Visual:** `G-11 Commit Density Chart` — 22 August spike highlighted.
**On-slide text:** **32 commits on 22 August — the densest day in the repository. All governance.**
**Evidence:** repository history.

### Slide 12 · The second cut
**Objective:** what the platform does when identity itself is in question.
**Visual:** `G-12 Divergence Diagram` — two timelines splitting at 00:03:27.
**On-slide text:**
> A second cut of the film existed.
> Diverged at 00:03:27. Ran 157.125 s shorter.
> **The authorised work order was halted.**

**Speaker notes:** "Every registry we had was pinned to a cut that might not be the film. The decision brief that followed carried one instruction: *do not recommend any option.* Three paths, full consequences, no recommendation. That is what decision preparation looks like when the platform has no business deciding."
**Evidence:** `7771e44`; `EXECUTIVE_DECISION_BRIEF_CUSTODY_ALERT_001.md`.

---

## ACT III — THE ARCHITECTURE THAT RESULTED (slides 13–18)

### Slide 13 · Six layers, and only two of them act
**Objective:** the whole architecture in one read.
**Visual:** `G-13 Six-Layer Stack` — verbs emphasised over box labels.
**On-slide text:** Executive **decides** · Governance **constrains** · Engineering **proposes** · Runtime **refuses** · Production **produces** · Commercial **distributes**.
**Speaker notes:** "Read the verbs. The Executive layer decides. The Runtime layer refuses. Nothing in between decides anything."

### Slide 14 · Custody is not authority
**Objective:** the conceptual centre.
**Visual:** `G-14 Custody vs Authority` — two orthogonal axes, deliberately not a hierarchy.
**On-slide text:**
> **Custody is not authority, and custody is immutable.**
> An actor may hold, author, measure and enforce — and never decide.

**Speaker notes:** "This is the breakthrough. Every AI governance framework I've seen conflates who touched a thing with who may decide about it. Separating them is what lets an AI write a specification and a governance guard without acquiring a single decision right."
**Evidence:** `ER-003`, `ER-004`.

### Slide 15 · The intelligence stack
**Objective:** the AI story, governed.
**Visual:** `G-15 Four-Layer Stack` — layers labelled by question, not by engine name.
**On-slide text:** What exists? · Why does it matter? · How should it feel? · What products result?
**Speaker notes:** "Two rules keep it honest. Engines consume governed outputs — never raw media without authorisation. And transcript output is evidence of speech, not verified speech. That second rule is why twenty-five names are still unconfirmed."
**Evidence:** `AIS-001`, `WET-REV-AIS001`.

### Slide 16 · The platform cannot interpolate
**Objective:** the most counter-market design decision in the deck.
**Visual:** `G-16 Ordinal Scale` — five discrete steps, with the smooth curve struck through.
**On-slide text:** LOW → MODERATE → HIGH → ELEVATED → CLIMACTIC · **ordinal, non-numeric, no gradient computable.**
**Speaker notes:** "Every creative-AI product on the market is racing to interpolate emotional curves. We made it structurally impossible and wrote down why."
**Evidence:** Invariant B, `EPR-001`.

### Slide 17 · Fourteen guards, and what they refuse
**Objective:** runtime integrity for the technical audience.
**Visual:** `G-17 Guard Gate Diagram` — a run halted before the first write.
**On-slide text:** Four injected faults · four stops · **exit 2 · zero files written.**
**Speaker notes:** "Not a warning. Nothing was produced. And a control artifact fails shut — a gate missing any required field is treated as CLOSED."
**Evidence:** `runtime_guards.py`; ECR-GEN-002 negatives.

### Slide 18 · An empty field remains empty
**Objective:** the human-authority boundary, demonstrated.
**Visual:** `G-18 Authoring Boundary` — the EPR workbook with a reserved column.
**On-slide text:**
> *"The platform SHALL NOT author, populate, infer, extend, suggest, or default ANY value.*
> ***An empty field remains empty.***"

**Speaker notes:** "Six emotional beats, authored by the Executive one at a time, transcribed verbatim across eleven registry versions. When he said 'my inclination would be retire,' the platform recorded the inclination and waited for a ruling."
**Evidence:** `EPR-001` §2.3.

---

## ACT IV — WHAT IT PROVES (slides 19–24)

### Slide 19 · Four refusals
**Objective:** the single most defensible claim in the deck.
**Visual:** `G-19 Refusal Ledger` — four rows, each with the authorised action and the reason for refusal.
**On-slide text:**
| authorised | refused because |
|---|---|
| atomic regeneration (Executive Order) | six preconditions unmet — would have emitted the wrong film |
| convert an inclination to a disposition | an inclination is not a ruling |
| accept an unverified host key | silent substitution on the Chairman's behalf |
| claim fixture equivalence | 3 of 9 columns unrecoverable without inference |

**Speaker notes:** "Four times the easy, permitted, helpful action was available. Four times it was declined. Four times the evidence later showed the refusal was right. **A control that has never fired is not a control.**"

### Slide 20 · The number that was never computed
**Objective:** the self-audit that proves the model.
**Visual:** `G-20 Validator Comparison` — 1/191 vs 191/191.
**On-slide text:** A figure cited in three governed artifacts, for three months, as a hard-coded string. **No committed code had ever produced it.**
**Speaker notes:** "It was true. Remediation reproduced it exactly. But for three months our foundational measurement was an assertion wearing a measurement's clothes — and we found that ourselves, in our own audit."
**Evidence:** ECR-GEN-002 §2.1.

### Slide 21 · Ninety-two to eighty-five
**Objective:** the ratio that describes the initiative.
**Visual:** `G-21 Ratio Bar` — governance documents vs engine modules.
**On-slide text:** **92 governance documents · 85 engine modules.** Nobody planned that ratio.
**Speaker notes:** "The load-bearing instruments — custody, evidence hierarchy, the reporting standard, the doctrines — contain nothing about video. They were written for a motorcycle documentary and they apply to any governed machine-assisted work. **That is the asset.**"

### Slide 22 · Why this matters, by audience
**Objective:** let each stakeholder find themselves.
**Visual:** `G-22 Four-Quadrant Audience Map`.
**On-slide text:** Engineering: *make the wrong comparison unrepresentable* · Security: *you can audit what it declined to do* · Information architecture: *a knowledge base that can say "I don't know" per record* · Governance: *separation of duties with dissent on the record*.

### Slide 23 · What this deck does not claim
**Objective:** disclose before you are asked. **Do not skip this slide.**
**Visual:** `G-23 Disclosure Panel` — plain, no styling flourishes.
**On-slide text:**
- No composite readiness or maturity score appears in this package.
- The 85 % utilization figure is **not carried forward** — no producing computation exists.
- Every "mature" characterisation rests on **n = 1**.
- The soundtrack rights posture is **routed to specialist review**.
- The governed 08-24 lineage has **never been ingested**.

**Speaker notes:** "Every one of these was surfaced by the governance system, not by an outside reviewer. That we can list them precisely is the strongest argument for everything else in this deck."

### Slide 24 · The system improves itself
**Objective:** the close.
**Visual:** `G-24 Improvement Loop` — Produce → Measure → Find → Ratify → Tool → Produce.
**On-slide text:**
> A question becomes a finding.
> A finding becomes law.
> Law becomes tooling.
> Tooling changes the next production.

**Speaker notes:** "Nine of the ten moments that changed this platform are moments where it discovered it was wrong. The story isn't what it became. It's what it did every time the evidence disagreed with it." *(pause)* "Seventy-five riders told us why they ride. Twenty-five of those names are still marked unconfirmed. That isn't a gap in the work. **That is the work.**"

---

## APPENDIX SLIDES (hold in reserve, deploy on question)

| # | topic | trigger |
|---|---|---|
| A1 | Repository metrics table | *"how big is this really?"* |
| A2 | The 20 ratified clauses | *"show me the governance"* |
| A3 | Test and conformance history | *"is it tested?"* |
| A4 | Seven-era timeline | *"how did it evolve?"* |
| A5 | Technical debt register | *"what's broken?"* — **answer this one honestly and early** |
| A6 | Commercial tiers | *"how does this make money?"* |
| A7 | ER-007 instrument | *"how do you know what you learned?"* |

---

## DELIVERY NOTES

**Run time.** 24 slides, ~30 minutes. Act II is the longest and should be. If you must cut, cut from Act III, never Act II — the architecture is inferable from the story, but the story is not inferable from the architecture.

**The two slides that carry the deck** are 6 (eleven days of silence) and 19 (four refusals). Everything else supports them.

**Slide 23 is not optional.** Every audience named in this Order — security, governance, investors — is trained to look for what a deck omits. Disclosing first converts your biggest vulnerability into your strongest credibility signal.

**Tone.** Nine of the ten moments are failures. Deliver them level, without apology and without drama. The candour is the product.
