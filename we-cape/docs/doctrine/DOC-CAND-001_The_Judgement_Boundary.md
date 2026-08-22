# DOC-CAND-001 — The Judgement Boundary
## Governance Status
Document Type: **Doctrine Candidate** — NOT doctrine · Status: **PROPOSED 2026-08-22, awaiting a second instance**
Origin: Executive observation, 2026-08-22, following the ESS-004 disposition
Promotion rule: a candidate becomes doctrine when it has been **exercised twice and held both times**.
This one has one instance. See §4.

---

## 1. The observation as issued

> *"We're starting to see a pattern. Engineering gets us 90% of the way. The remaining 10% is
> precisely where creative direction belongs. That's not a weakness. That's the architecture working."*

The substance is right and it should be recorded. Two things about the **framing** need correcting
first, because if the framing goes into doctrine as written it will cause trouble later.

---

## 2. Correction 1 — the platform's own reporting standard forbids the number

`WET-SPEC-REPORT-001` v1.1, following the Executive Ruling on DWR-010 (EXTEND GAP-03):

> *Percentages are permitted only when they represent directly measurable quantities. They shall not
> be aggregated into opaque composite scores without explicit Executive approval.*

**"Engineering gets us 90%" is a composite score.** It collapses coverage, correctness, decidability
and confidence into one figure with invisible weights, and there is no denominator. It is precisely
the thing the ruling was written to prohibit — and it is a good sign for the rule that it catches its
own author, in conversation, three hours after being issued.

This is not pedantry about a figure of speech. If the phrase enters doctrine with the number attached,
someone will eventually cite "90%" as a platform metric, and it will not survive contact with a
question like *90% of what?*

**Recorded, therefore, without a number.**

## 3. Correction 2 — it is not a remainder. It is a different axis.

The sharper problem with "90 / 10" is that it implies a **single scale** on which engineering reached
90 and could, with more effort, reach 95. That framing invites exactly the over-reach the platform is
built to prevent: an engineer who believes the last 10% is *nearly* reachable will keep reaching.

The evidence says otherwise. Look at what actually happened in ESS-004:

| axis | where engineering got to |
|---|---|
| **What is factually true** — which elements exist, their provenance, their spans, whether the covenant is breached | **Complete.** 0 breaches, machine-checkable, reproducible from the locked FCPXML alone |
| **What it should mean** — what `MANDATORY_SILENCE` prohibits | **Zero, and correctly zero.** Not 90% of the way. Engineering had no claim on this at all |

It is not one scale at 90/10. It is **two axes**, and engineering ran one of them to the end while
having no standing on the other. That distinction matters practically:

- On the **fact** axis, an incomplete answer is a defect. Push it to completion.
- On the **judgement** axis, *any* engineering answer is an over-reach. Do not push at all — prepare
  the decision and stop.

ESS-004 is the proof. My engineering conclusion — *"definition 1 is currently unrulable"* — was an
attempt to reason on the judgement axis using fact-axis tools. It was wrong, and it was wrong in the
specific way this doctrine predicts: it foreclosed an option that was the Executive's to take.

## 4. The candidate, stated for testing

> **The Judgement Boundary.** Every governed question has a factual axis and a judgement axis.
> Engineering owns the factual axis completely and must run it to exhaustion — every measurement
> taken, every delta categorized, every option costed. Engineering owns none of the judgement axis.
> Its work there is to **prepare the decision, not to narrow it**: name the options, price each one,
> declare what the evidence cannot settle, and stop.
>
> **The failure mode is not stopping too early. It is continuing past the boundary in the language of
> measurement** — presenting a preference as a finding, or an undecidable question as a closed one.

**Falsifiable test.** In each governed decision, classify every engineering statement as fact-axis or
judgement-axis. The candidate holds if fact-axis statements survive Executive review unamended, and
if the engineering record's judgement-axis statements are the ones that get corrected.

| instance | fact-axis statements amended by the Executive | judgement-axis statements amended |
|---|---|---|
| **ESS-004** | 0 — provenance classification, spans, breach count all stood | **1 — "definition 1 is unrulable" was overturned** |
| ESS-002 | *pending* | *pending* |

**One instance is not a pattern.** ESS-002's disposition is the second test. If the same split appears
there — measurements stand, engineering's judgement-adjacent claims get corrected — this is promoted
to `DOC-004`. If it does not, it stays a candidate and the record says why.

## 5. What promotion would change

Nothing about how work is done; it is already how the platform behaves. Promotion would give the
behavior a citable name, so that:

- a future review can cite *"DOC-004 §judgement axis"* instead of re-arguing it;
- an engineering report that narrows an Executive option can be **failed against a rule** rather than
  caught by chance, as it was this time;
- session classes (`ELS`, `EVS`) have a stated reason to exist: they are the mechanism for handing a
  judgement-axis question to the only authority that can answer it.

## 6. Relationship to existing doctrine
`DOC-001` (validate the instrument before the measurement) and `DOC-002` (regenerate, never patch)
are both **fact-axis** doctrines — they govern how engineering does its own work. This candidate is
the first that governs the **boundary** of that work. That is why it deserves its own number rather
than an amendment to either.

---
*Recorded 2026-08-22 by the Implementation Engineer at Executive prompting. Not doctrine. Not citable
as authority. One instance.*
