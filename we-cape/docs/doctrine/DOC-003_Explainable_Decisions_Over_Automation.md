# DOC-003 — Explainable decisions over automation
## Governance Status
Document Type: Doctrine (ratified) · Status: **RATIFIED** · Date: 2026-08-22
Authority: Executive Producer (Executive Assessment, 2026-08-22)
Chairman countersignature: ☐ pending
Scope: PLATFORM — the north star for every engine, module, artifact and report in WE CAPE.

---

## The doctrine
> **WE CAPE does not optimize for automation; it optimizes for explainable decisions. Every significant
> platform conclusion shall be traceable to objective evidence, presented through measurable component
> metrics, and communicated with an Executive Verdict that explains what the evidence means and what
> action, if any, is recommended.**

*Issued verbatim by the Executive Producer, 2026-08-22. This paragraph is the doctrine. Everything
below is context, and nothing below narrows it.*

## What it settles
It gives future contributors a north star without constraining implementation. Read as four
commitments already in force across the platform:

| commitment | already realised as |
|---|---|
| Traceable to objective evidence | `DOC-001` — validate the instrument before the measurement |
| Presented through measurable component metrics | `WET-SPEC-REPORT-001` §3 — Component Metrics → Objective Percentages → Executive Verdict |
| Communicated with a verdict that explains | `WET-SPEC-REPORT-001` §3.3 — the verdict says what to **do**, never how to feel |
| Not optimized for automation | `ADR-009` — advisory under Human Editorial Authority; `DOC-002` — regenerate, never patch |

## The operative test
The sharpest form of this doctrine in practice is the measurement/score distinction carried in
`WET-SPEC-REPORT-001` §6:

> A value that describes **one thing**, carries its **basis**, and can be **argued with** is a
> measurement. A value that collapses **many dimensions** into one figure with **invisible weights**
> is a score. The first is evidence. The second is a substitute for evidence.

That test is the doctrine applied to a single number. It generalises: any platform output that cannot
be argued with has stopped explaining and started asserting.

## The architecture it rejects
```
   Measurement  →  Score  →  Confusion          (rejected)
   Measurement  →  Decision  →  Action          (adopted)
```

## Where it came from
Four consecutive pieces of work, each establishing one pillar:

| origin | established |
|---|---|
| **Sprint 3A / RE-001** | **Evidence First** — offset 0.000, drift 95% CI, probes 3/3, deltas 25 with 0 uncategorized. No synchronization score was reported; the Executive Team drew the conclusion |
| **CAR-003** | **Discoverability** — capabilities can exist without anyone realising they exist; information architecture matters as much as software architecture |
| **CAR-004** | **Acquisition Intelligence** — the gap is not capability, it is custody at the moment of acquisition |
| **WET-SPEC-REPORT-001** | **Explainability** — component metrics and a verdict, never a composite score |

Those four are the philosophical backbone of the platform. DOC-003 is the sentence that holds them
together.

## Non-goals
This doctrine does not prohibit automation, prefer slow work, or require a human in every loop. It
requires that when the platform reaches a conclusion, the evidence that produced it remains visible
and arguable. Automate freely; explain always.

## Provenance
Executive Assessment, 2026-08-22 (*"a single paragraph in the platform philosophy … that captures what
we've learned"*) → **DOC-003**. Related: `DOC-001`, `DOC-002`, `DOC-SRC-001`,
`WET-SPEC-REPORT-001`, `ADR-009`, `RE-001`, `CAR-003`, `CAR-004`.
