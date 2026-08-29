# WET-EXEC — TECHNICAL ARCHITECTURE REVIEW
## W.E. C.A.P.E. · 32 slides · 45–60 minutes

> **DERIVED VIEW.** Canonical source: `WET_EXEC_MASTER_PRESENTATION.md`.
> Every fact cites an `M-nn` identifier; every principle quotes an `S-nn` statement. **This file introduces no fact absent from the Master and is never independently edited.**

**Audience:** principal engineers · architects · security engineers · AI researchers · technical founders
**Purpose:** explain **how the platform operates**
**Repository measured at:** `0acf42a` · 2026-08-29T06:37:02Z — **re-measure before presenting**

---

## PART I · THE ARCHITECTURE *(slides 1–8)*

### T1 · What this is, in one slide
**Visual:** `G-36` Five-Layer Platform Stack, bottom-up
**Text:** `S-01` · `S-02`
**Notes:** "Read it bottom-up. Knowledge is the foundation, not the output — and that inversion is the architectural claim."

### T2 · Repository architecture — the authority chain
**Visual:** `G-39` — nine levels, with the upward regeneration arrow
**Text:** Executive → Governance → Specifications → Registries → Intelligence → Generators → Runtime → Testing → Commercial
**Notes:** "Not a folder structure — an authority chain. Each level constrains the one beneath it, and any artifact can be regenerated from the level above. `S-09`. A correction is a new run, never an edit." *(beat)* "The broken link is drawn: `D-09`."

### T3 · System components
**Visual:** `G-28` System Component Diagram
**Text:** `wecape/` — `M-06` modules, `M-08` LOC → derived intermediates → `intelligence/` — `M-11` scripts, `M-12` LOC → 7 governed artifacts → gates → publication
**Notes:** "Note the seam. Deterministic engine, read-only ops layer, joined only where defined."

### T4 · Repository topology
**Visual:** `G-29` — treemap, area = file count
**Text:** `M-05` · `M-06` · `M-07` · `M-24`
**Notes:** "`docs/` and `wecape/` are comparable in weight. That comparability *is* `M-07`, rendered spatially."

### T5 · Production workflow
**Visual:** `G-30` — swimlane with a governance rail and human-decision glyphs
**Text:** capture → offload → organise → conform → edit → observe → generate → gate → publish

### T6 · Executive Orders as an architectural input
**Text:** Orders are scoped, dated, binding, and carry **explicit exclusions**. An Order that authorises work does not authorise its preconditions.
**Notes:** "Moment 9 is the proof: an Order authorised a regeneration and the platform refused, because six preconditions were unmet. **The Order was the input, not the permission.**"

### T7 · Specifications
**Text:** 7 specifications · reviewed before freeze · frozen at SHA-256 · 12 formal modifications on `WET-SPEC-DIE-001` before its freeze
**Notes:** "`S-17`. A spec here is a component, not a description."

### T8 · Registries
**Text:** `M-14` registries · `M-15` intelligence artifacts · `M-20` riders, 25 `UNCONF` · every fact timecode-cited · per-record confidence · `missing_data_policy: propagate_unknown`
**Notes:** "The registry is the catalog layer. Clause 3: NLE metadata, filenames and folders are **projections of registry truth**. And a knowledge base that can say 'I don't know' per record is a fundamentally different artifact from one that cannot."

## PART II · RUNTIME AND CONFORMANCE *(slides 9–16)*

### T9 · Runtime guard architecture
**Visual:** `G-32` Runtime Guard Lifecycle — pass path and fail path
**Text:** `M-17` guards, all before the first write. `G-01`–`G-03` identity, lineage, hashes · `G-04`–`G-07` runtime contract, ETC verdict, census, out-of-range · `G-08`/`G-08b` segment shape and declared overlaps · `G-09`–`G-11` cue registry, derived-set provenance, completeness · `G-12`/`G-13` canonical scope and governed narrative boundaries

### T10 · Fail-shut, and what that means operationally
**Text:** `S-11`. A gate missing any required field is treated as CLOSED. `scripts/gate_status.py` computes the aggregate.
**Notes:** "A control artifact fails shut. And the aggregate is *computed* — a governance status nobody can author by hand."

### T11 · The negative test ledger
**Visual:** `G-17` — six faults, six stops
**Text:** wrong `production_id` → `G-01` · foreign source hash → `G-03` · incomplete bundle → `G-11` · undeclared overlap → `G-08b` · erased governed overlap → `G-08b` · complete tidy-up → `G-13`. **Each: exit 2, zero files written.**
**Notes:** "Not a logged warning. **Nothing was produced.**"

### T12 · Observability of refusal
**Text:** `FAILED_SOURCE_IDENTITY` · `FAILED_CARDINALITY` · `FAILED_COMPARISON` · `FAILED_TIMELINE_CLOSURE` — each with a recorded `stop_reason`
**Notes:** "`S-22`. In an incident review, that's the log that matters."

### T13 · Conformance validation
**Text:** `M-18` — 22 PASS / 0 FAIL, with adversarial negatives. Strict cardinality asserted **before** comparison.
**Notes:** "`S-21`."

### T14 · Testing hierarchy
**Visual:** `G-31` — four blocks, **not summed**
**Text:** engine unit **384 green** *(peak 404/404 recorded)* · acceptance **99/99** · ECR conformance `M-18` · negatives 6
**Notes:** "Four numbers, four different things, and they are not additive. Each block carries what it does *not* cover."

### T15 · The testing inversion — disclosed
**Visual:** `G-31b` — the pipeline's test bar drawn as an empty outline
**Text:** Engine `M-08` LOC / **`M-09` test LOC**. Pipeline `M-12` LOC / **`M-13`**. `D-06`
**Notes:** "More test code than engine code — and the pipeline that produces every governed artifact has none. Covered end-to-end by `M-18` with proven negatives, and that's it. **It's the first thing I'd fix.**"

### T16 · Evidence grading
**Text:** `[E]` evidenced with citation · `[P]` projection · `[O]` open. Percentages require numerator, denominator and source. Composite scores **prohibited** — `S-12`.

## PART III · THE GENERATOR PIPELINE *(slides 17–22)*

### T17 · Deterministic generation
**Visual:** `G-46` — two runs, byte-diff at true proportion
**Text:** `M-31` — 205,679 bytes → 7 changed lines, 5 changed bytes, every one explained
**Notes:** "That's how you prove a refactor is behaviour-neutral when the output is documents rather than data structures."

### T18 · Measured context
**Text:** `build_context.py` turns a *declared* context into a *measured* one — hashes, byte counts, cue census, ETC census, resolver census — and **refuses to emit a context whose declared values disagree with measurement.**
**Notes:** "A declared value that disagrees with a measured one is a governance condition, not a formatting error. The script stops; it does not correct the declaration."

### T19 · The `zip()` that never compared anything
**Visual:** `G-20` — 1/191 at true scale → 191/191
**Text:** A validator compared the resolver's depth-0 set (includes transitions) against the contract's spine census (excludes them), paired positionally. It scored **1 of 191** on data that agrees perfectly. The published `191/191` was a **hard-coded string literal**; `git log` proved no committed code had ever produced it.
**Notes:** "`S-14`. And the fix is the transferable part: `S-21` — cardinality is now asserted before any pairing, so truncation is structurally impossible rather than merely unlikely."

### T20 · Parameterisation as diagnosis
**Text:** `D-05` — 74.3 % of emitted text is literal prose *(38,056 of 51,237 characters, `traceability_scan.py`)*
**Notes:** "Removing constants was expected to be tedious. It was diagnostic. **You cannot see an assumption until you try to make it a parameter.**"

### T21 · Editorial Intelligence Stack
**Visual:** `G-15` — four layers labelled by question
**Text:** DIE *what exists?* `[E]` exercised · NIE *why does it matter?* · MIE *how should it feel?* · PIE *what products result?*
**Notes:** "Two rules keep it honest, and both were **engineering modifications to the Chairman's vision, accepted at ratification**: engines consume governed outputs, never raw media unauthorised; and transcript output is *evidence of speech*, not verified speech. That second rule is why `M-20` shows 25 unconfirmed."

### T22 · Non-interpolation
**Visual:** `G-16` — five discrete steps, the smooth curve struck through
**Text:** `LOW → MODERATE → HIGH → ELEVATED → CLIMACTIC` — **ordinal, non-numeric, no gradient computable**
**Notes:** "Every creative-AI product on the market is racing to interpolate emotional curves. We made it structurally impossible and wrote down why."

## PART IV · GOVERNANCE AS ARCHITECTURE *(slides 23–27)*

### T23 · Custody is not authority
**Visual:** `G-14`
**Text:** `S-04` — three immutable custody classes: `MACHINE` · `HUMAN` · `EXECUTIVE`
**Notes:** "Closer to a capability model than RBAC — and applied to an AI agent. This is what lets an AI author a specification, run a forensic audit and write a governance guard while holding zero decision rights."

### T24 · Evidence hierarchy
**Text:** `PRIMARY SOURCE → DERIVED VIEW → OBSERVATION → DISPOSITION → REGENERATION → GOVERNED ARTIFACT` · `S-05`
**Plus** `S-10` and clause 18 — no unexplained deltas at any stage boundary.

### T25 · Executive / Engineering separation
**Visual:** `G-35` Governance Authority Boundaries — the `decide` column has **exactly one mark**
**Text:** proposal and ratification are different artifacts with different custody *(Moment 6)*
**Notes:** "The engineering channel assessed the Chairman's architecture and returned *'sound with modifications.'* The modifications were ratified, not overruled. And when the channel *disagreed* with a governance decision, it recorded the objection inside the register, complied, and wrote that silently reclassifying a Chairman ruling **would be the platform making a governance decision that is not its to make.**"

### T26 · Engineering reviews and change orders
**Text:** `ECR-GEN-001` parameterisation · Engineering Readiness Review · `ECR-GEN-002` validator remediation → `M-18`. Certification: **`ENGINEERING-CONFORMANT` / production readiness `NOT YET AUTHORIZED`**.
**Notes:** "That separation is a product of the governance model, not a limitation. Engineering may certify that the platform *can* execute correctly. Only Executive authority can authorise that it *may*."

### T27 · Local-first security architecture
**Visual:** `G-33` — boundary diagram with the egress arrow struck through
**Text:** enforced network invariant in the engine path · PII gated **off** by default · path redaction on egress · encrypted offsite · restore-proven 3-2-1 · data-loss-first threat model
**Notes:** "Media never leaves the machine. And the threat model here isn't 'attacker' — it's **'the system convinced itself of something false.'**"

## PART V · EVOLUTION AND DISCOVERIES *(slides 28–32)*

### T28 · Timeline and milestones
**Visual:** `G-47` — months on the axis, eras as the structure
**Text:** `M-01` · `M-02` · **`M-32`** · **`M-33`**
**Notes:** "Governance and engineering intensified together. The densest day in the repository is a governance day."

### T29 · Architecture evolution
**Text:** W.E. FLOW *(gates before features)* → W.E. FORGE *(platform foundation)* → **W.E. C.A.P.E.** *(identity, performance, the NLE bridge)* → measurement → **findings become law** → constitution → conformance certification

### T30–T31 · The ten discoveries
**Visual:** `G-25` — seven-field cards, Master §4
**Text:** all ten, in sequence
**Notes:** "Nine of the ten are moments where the platform discovered it was wrong. One — custody is not authority — is where it discovered what it had built."

### T32 · What this deck does not claim
**Visual:** `G-23` Disclosure Panel — deliberately undesigned
**Text:** **`D-01` … `D-13`, complete and unshortened**
**Notes:** "Every one surfaced by the governance system, not by an outside reviewer. `S-19`."

---

## APPENDIX SLIDES — deploy on question

| # | topic | trigger |
|---|---|---|
| `TA1` | Technical debt register — `G-34` | *"what's broken?"* — **answer this early and honestly** |
| `TA2` | The 20 ratified clauses, verbatim | *"show me the governance"* |
| `TA3` | Dependency and version disclosure — `D-07` | *"how do I deploy this?"* |
| `TA4` | Knowledge compounds, technical view — `G-40` | *"what's the actual asset?"* |
| `TA5` | `ER-007` evidence-driven evolution instrument | *"how do you know what you learned?"* |
| `TA6` | Repository metrics, full — `G-41` | *"how big is this really?"* |

---

## DELIVERY

**32 slides · 45–60 minutes.** Parts II and III are the technical core and should carry the most time.

**The four slides that carry this deck:** T2 (authority chain) · T15 (the testing inversion) · T19 (the `zip()` bug) · T32 (disclosure).

**T15 and T19 are why this audience will trust the rest.** Both are self-found defects, disclosed before being asked. Lead into T19 with the finding, not the fix.

**`D-01`…`D-13` may not be shortened.** A reader who finds a material disclosure *outside* the disclosure slide stops trusting the disclosure slide.

---

*Derived view. Canonical source: `WET_EXEC_MASTER_PRESENTATION.md`. Custody: `PRESENTATION PACKAGE ONLY`.*
