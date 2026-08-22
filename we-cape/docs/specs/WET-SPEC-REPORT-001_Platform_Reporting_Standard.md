# WET-SPEC-REPORT-001 — Platform Reporting Standard
**Version 1.1** (v1.0 issued 2026-08-22; amended same day by Executive Assessment)
## Governance Status
Document Type: Specification (named-series) · Status: **RATIFIED — IN FORCE** · Date: 2026-08-22
Authority: Executive Producer — Executive Ruling on `DWR-010`, 2026-08-22
Chairman countersignature: ☐ pending
Supersession: **this policy may be superseded only by an ADR that explicitly does so.**
Extends: `WET-WF-001` Gap Register **GAP-03** (locked design decision, 2026-08-11)
Numbering: named-series per `docs/README`. Platform-core sequential series untouched.
Filename note: the version is carried **inside** this document, not in its filename. v1.0 shipped as
`…_v1.0_…md` and was renamed on amendment — putting a version in a filename creates exactly the
collision class CAR-003 §4.4 recorded (`EXECUTIVE_SUMMARY_v4.6`/`v4.7`, `CUE_SHEET`/`CUE_SHEET_v1.1`).
Recorded rather than repeated.

## Amendment 1 (v1.0 → v1.1, 2026-08-22)
Executive Assessment of the v1.0 draft:
1. **`BLOCKED` is NOT ratified** as a component status. It describes *workflow*, not *evidence*, and
   belongs one layer higher — §3.4.
2. **`OPPORTUNITY` is formalized** as a first-class executive insight rather than a status label — §3.5.
Both changes are recorded below. No other clause changed.

---

## 1. The Ruling (verbatim, as issued)
> **Decision: Extend GAP-03.**
>
> **Rationale:** WE CAPE shall continue to report objective component metrics accompanied by a
> plain-language Executive Verdict. Composite readiness or health scores are prohibited unless a
> future ADR explicitly supersedes this policy.
>
> **Percentages are permitted only when they represent directly measurable quantities (e.g. coverage,
> utilization, completion, reconciliation, or validation). They shall not be aggregated into opaque
> composite scores without explicit Executive approval.**

Scope of extension: **Capture Readiness · Acquisition Intelligence · and all future platform health
reporting.** GAP-03's prohibition is no longer a decision about one report. It is the platform's
reporting law.

## 2. Why — recorded so the rule survives the people who made it
GAP-03 was never about numbers. It was about **decision quality**.

`Capture Readiness: 87%` raises more questions than it answers. *Why 87? What is missing? Can I fix
it? Is GPS weighted above timecode? Does missing telemetry matter more than missing audio?* The score
hides the evidence, and hidden weights are unarguable — which is the opposite of what a governed
platform is for.

WE CAPE has consistently evolved toward **explaining rather than rating**. This standard makes that
trajectory normative.

## 3. The Constitutional Reporting Pattern (normative)
Every readiness, health or intelligence report SHALL have three parts, in this order:

```
  1. COMPONENT METRICS      — what is true, per capability, with evidence
  2. OBJECTIVE PERCENTAGES  — measured quantities only (§5)
  3. EXECUTIVE VERDICT      — one plain-language sentence: what to DO
```

### 3.1 Component metrics table — required columns
| column | meaning |
|---|---|
| **Capability** | the thing being reported on |
| **Available** | the source can produce it (device emits it, artifact exists) |
| **Enabled** | it was switched on / actually written / actually captured |
| **Consumed** | the platform actually uses it downstream |
| **Status** | §3.2 |
| **Evidence** | file, line, probe output or hash. **Required.** A row without evidence is an opinion |

The `Available / Enabled / Consumed` triplet is the heart of this standard. It separates three failures
that a single status word collapses:

| pattern | meaning | example from Alpha RoundUp Part 2 |
|---|---|---|
| ✓ ✓ ✓ | working | FCPXML — produced, exported, consumed by the ETC |
| ✓ ✓ **✗** | **capability built and wasted** | embedded timecode: read by `proxy.py::_get_timecode()`, used only to re-stamp proxies |
| ✓ **✗** — | **a setting, not a gap** | GPS: `gps_for_action: true` in the registry, zero `.SRT` files written |
| **✗** — — | genuinely absent | Insta360 X5 timecode — the device emits none |

Two of those four are cheap to fix and one is free. A composite score renders all four as one number.

### 3.2 Component status vocabulary (enumerable)
| status | meaning |
|---|---|
| `PASS` | available, enabled and consumed |
| `OPPORTUNITY` | available and enabled but **not consumed** — value already paid for, not yet collected |
| `ATTENTION` | available but **not enabled** — an operational or configuration gap, not an engineering one |
| `ABSENT` | not available from this source. Neutral: not every device emits everything |

**`BLOCKED` was proposed in v1.0 and is NOT ratified.** Executive Assessment, 2026-08-22:

> *"Blocked isn't describing data. It's describing workflow. GPS unavailable is not blocked — it's
> unavailable. Whereas 'cannot compute synchronization because no FCPXML exists' is blocked. Those are
> different."*

The four states above already describe the full acquisition lifecycle. The concept the proposal was
reaching for is real, and it is given its own layer in §3.4. The component vocabulary stays at four.

### 3.3 Executive Verdict — required, one sentence, plain language
The verdict says **what to do**, never how to feel. It is written for the report, not selected from an
enum — but it must be a directive sentence a producer can act on.

Reference forms from the ruling: *"Ready for high-confidence synchronization."* · *"Ready with minor
opportunities."* · *"Additional acquisition data recommended before analysis."*

**A verdict SHALL NOT contain a number that summarises the report.**

### 3.4 Processing Status — a separate concern (normative)
Component status describes **evidence**. Processing status describes **workflow**. They are different
questions and they are never mixed in the same column.

| status | meaning |
|---|---|
| `READY` | every precondition the operation requires is present; work may begin |
| `WAITING` | a precondition is expected but has not arrived yet |
| `BLOCKED` | a precondition the operation **requires** is absent, and the operation cannot proceed |
| `COMPLETE` | the operation has run and its outputs exist |

Processing status appears **once, as a report header field**. It never appears as a component row.

#### 3.4.1 The guard — read this before implementing it
There is a way to get this wrong that would quietly undo the whole standard.

**Processing status SHALL name the specific unmet precondition. It SHALL NOT be derived by aggregating
component rows.**

A `BLOCKED` computed from *"three ATTENTION rows and one ABSENT row"* through unpublished rules is a
composite score wearing a word instead of a number — the same opacity, the same invisible weights, the
same unarguable output, and harder to spot because it does not look numeric. Every non-`READY` status
carries the precondition that produced it, in plain language:

> `Processing Status: BLOCKED — no locked FCPXML exists for this production; synchronization cannot be computed.`

not

> `Processing Status: BLOCKED`

A component being `ABSENT` does not imply `BLOCKED`. The Insta360 X5 emits no timecode (`ABSENT`) and
nothing whatsoever is blocked by that.

### 3.5 `OPPORTUNITY` — formalized as an executive insight
Executive Assessment, 2026-08-22: *"You've already invested in the capability. The platform simply
isn't using it. That's very different from missing capability."*

`OPPORTUNITY` (Available ✓ · Enabled ✓ · Consumed ✗) is therefore not merely a status label. It is the
standard's distinct executive finding class:

> **Capability built and wasted.**

An `OPPORTUNITY` row asserts that the platform has *already paid* for a capability — the device emits
it, the setting is on, the extraction may even already run — and is not collecting the return. It is
categorically different from `ABSENT` (nothing was ever built) and from `ATTENTION` (built, but
switched off).

Reports SHOULD surface the `OPPORTUNITY` count in the objective-percentage section as a plain count
with its denominator (e.g. *"4 of 15 capabilities built and unconsumed"*).

**Boundary:** that count SHALL NOT be inverted into a *"capability utilization %"* presented as an
overall health figure. Counting what is unclaimed is a measurement; converting it into a grade for the
production is a composite score, and §4 forbids it.

## 4. Prohibition (normative)
The following SHALL NOT be produced:
- Any single figure presented as an overall measure of readiness, health, quality, maturity or
  intelligence for a production, a capture, a synchronization, or the platform.
- Named instances, for the avoidance of doubt: *Production Intelligence Score · Capture Readiness Score
  · Health Score · Synchronization Score · Acquisition Score.*
- Any weighted aggregation across dissimilar dimensions where the weights are not visible and arguable.
- Any **processing status derived by aggregation** rather than by naming an unmet precondition (§3.4.1).

## 5. Percentages — permitted, and bounded
**Permitted** when the figure is a directly measurable quantity with a stated numerator and
denominator: coverage · utilization · completion · reconciliation · validation.

Each published percentage SHALL carry its numerator, denominator and source. `Timecode coverage 38.5%`
is a fact. `38.5%` alone is decoration.

**Prohibited:** aggregating permitted percentages into a composite without explicit Executive approval.
Four honest percentages side by side are not a score; averaging them is.

## 6. Scope boundary — what this prohibition does NOT cover
Written because a rule this strong will otherwise be over-applied, and a compliance sweep of the
repository found score-shaped values that are **legitimate and must not be removed**:

| construct | where | ruling |
|---|---|---|
| `quality_score`, `highlight_score` per asset | `wecape/registry/`, `reader.py::min_quality_score` | **PERMITTED** — a per-item measurement attached to one asset, not an aggregate standing in for a judgement |
| `camera_confidence` (0.0–1.0) | `WEFORGE_Architecture_v1.0.md` schema | **PERMITTED** — per-detection confidence with a stated derivation |
| `energy` 1–5 per segment | `ENERGY_CURVE.yaml` | **PERMITTED** — an editorial descriptor, per segment, each carrying a `basis` field |
| `resolution_confidence` HIGH/MEDIUM/LOW; DIE-V `confidence` HIGH/MEDIUM/LOW/UNCERTAIN | `WET-SPEC-DIE-001` R-1, `VISUAL_EVENT_REGISTRY` | **PERMITTED** — ordinal classifications, not scores |
| `timestamp_confidence` + `fallback_level` | `wecape/capture/timestamp.py` | **PERMITTED** — per-file, with the level that produced it visible |

**The line:** a value that describes **one thing**, carries its **basis**, and can be **argued with** is
a measurement. A value that collapses **many dimensions** into one figure with **invisible weights** is
a score. The first is evidence. The second is a substitute for evidence.

## 7. Applies to
`Production Health` · `Acquisition / Capture Readiness` · `Editorial Synchronization` ·
`Music Readiness` · `Publication Readiness` · `Production Intelligence Review` · `Executive Dashboard`
— and any future report of this class.

> **One language. One philosophy.**
> Component Metrics → Objective Percentages → Executive Verdict.

## 8. Compliance status at ratification
A sweep of the repository on 2026-08-22 found **no composite readiness or health score in any governed
artifact.** Every `score` occurrence in `intelligence/` is the *musical* score (`CONDUCTOR_SCORE`), a
different sense of the word. The platform is **compliant on the day the standard is issued** — the
ruling ratifies existing behaviour rather than correcting it.

Two forward-looking notes: `EXECUTIVE_SUMMARY_v4.6.md` describes future *"confidence-scored grouping"*
(permitted under §6, per-item); and `RE-001_SCORECARD.yaml` is named *scorecard* but contains no score
— it is a fingerprint of counts, ratios, booleans and statuses, and it already states in its own text
that no subjective score exists or should be added. **Naming risk noted; no change required.**

## 9. Precedent — Sprint 3A already worked this way
Sprint 3A did not report a synchronization score. It reported `offset 0.000` · `drift +0.684 s
(95% CI −0.541…+1.909)` · `probes 3/3 PASS` · `conflicts 3` · `uncategorized deltas 0`, and the
Executive Team drew the conclusion. This standard names the practice the platform had already found.

## 10. Related
`WET-WF-001` GAP-03 (origin) · `DWR-010` (the question) · `CAR-003` findings §2 item 8 ·
`CAR-004` §6 S-5 and Appendix B (first application) · `DOC-001` (evidence discipline) ·
`DOC-003` (explainable decisions over automation — the philosophy this standard implements) ·
`SPEC_Production_Health_Report.md` (the original locked design).
