# ECR-003 — CUE INDEX VALIDATOR · DESIGN REVIEW

**Issued under:** EXECUTIVE REVIEW ORDER EDR-001, Platform Engineering Control section
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. **Nothing was built.** No validator exists, none was written, no citation was checked.
**Measured at:** repository HEAD `1552e42`

> **This is a sufficiency review of a proposed control, not the control.** It asks whether ECR-003 is specified well enough to be implemented later. It does not implement it, and it makes no recommendation about adding timecodes to any citation.

---

# 1 · WHY THIS CONTROL EXISTS

The repository's own dependency inventory states the failure mode:

> *"A wrong timecode is caught by a bounds check. **A wrong cue index is caught by nothing. It always resolves, it never errors**, and the result is a confident misattribution of a quote or a rider to a person who did not say it."*

**No control in the repository detects this.** `CIA-001 R-1` grades it the highest-severity item found, and it exists **today**, independent of ED-004.

**This is a platform integrity control, not part of the Caption Collapse Rule.** ED-004 changes zero citations; `R-1` endangers all of them. Binding the control to the rule would tie a live safeguard to a declaration it does not depend on.

---

# 2 · THE THREE OUTCOMES — CONFIRMED SUFFICIENT

The Order specifies exactly three. **All three are necessary, mutually exclusive, and jointly exhaustive over the citation set as it exists.**

| citation form | result | population |
|---|---|---|
| cue index **+** timecode, and they agree | `VALIDATED` | subset of 82 |
| cue index **+** timecode, and they disagree | `FAILED` | subset of 82 |
| cue index **only** | `UNVALIDATABLE` | **9** |

**82 + 9 = 91.** No citation falls outside the three. `[E]`

## 2.1 · Why `UNVALIDATABLE` must be its own verdict and not a pass

**A two-outcome design would have to classify the nine as passing** — nothing contradicts them, so nothing fails. **That is precisely the failure mode the control exists to remove**: a check that reports success because it had nothing to check.

`UNVALIDATABLE` is not a soft failure or a warning. It is a statement that **the instrument cannot reach these records** — which is the honest result and matches the platform's existing practice of resolving conflicts to an explicit unknown rather than a silent winner.

---

# 3 · CONFIRMING THE CIA-001 ERRATUM

Re-measured for this review, independently of the erratum.

| registry | citations | with timecode | without |
|---|---|---|---|
| `RIDER_REGISTRY.yaml` | 80 | **80** | 0 |
| `PROMPT_REGISTRY.yaml` | 2 | **2** | 0 |
| `MOTORCYCLE_REGISTRY.yaml` | 6 | 0 | **6** |
| `ORGANIZATION_REGISTRY.yaml` | 3 | 0 | **3** |
| **total** | **91** | **82** | **9** |

**CIA-001 ERRATUM 1 is confirmed. 82 eligible, 9 structurally unvalidatable.** `[E]`

## 3.1 · The split is by citation *shape*, not by registry quality

```yaml
# eligible — compound form, index and timecode in one field
RIDER_REGISTRY    cue: "#31 01:51"
PROMPT_REGISTRY   cue: "#… MM:SS"

# unvalidatable — list form and bare-cue form carry no timecode
MOTORCYCLE_REGISTRY    harley-davidson:        cues: ["#280","#776","#1420","#1471","#2031"]
MOTORCYCLE_REGISTRY    vrod_2003_anniversary:  cue:  "#2029"
ORGANIZATION_REGISTRY  ORG03 Buffalo Soldiers: cues: ["#303","#1047"]
ORGANIZATION_REGISTRY  CIV02 Nissan Motor Co.: cue:  "#1148"
```

**The nine are the citations that bind a make, a model and an organisation to a moment in the film.** They are not lower-value records; they are records written in a shape that omitted the second field.

**Whether they should be given timecodes is an Executive decision and is not recommended here**, per the Order. The engineering observation is narrower and is stated as such: **a validator can report their condition; it cannot remedy it.**

---

# 4 · SPECIFICATION SUFFICIENCY

Assessed against what an implementer would need. **Four items are sufficiently specified. Four are not — and one of those four turned out to be a defect rather than an omission.**

> **Revised 2026-08-30.** This section originally counted five sufficient items, including the reference stream. **`CF-001` withdrew that one.**

## 4.1 · Sufficiently specified

| element | why sufficient |
|---|---|
| **Purpose** | *Verify that every cue index resolves to the recorded timecode. Fail closed. No silent misattribution.* Unambiguous |
| **Outcome set** | Three, exhaustive over the population — §2 |
| **Population** | 91 citations, 4 registries, enumerable by a fixed pattern; 91 distinct indices, 0 out of range |
| ~~**Reference stream**~~ | **WITHDRAWN 2026-08-30.** This row claimed the reference stream was sufficiently specified because `RIDER_REGISTRY` declares GT-2. **Measurement shows that declaration is wrong — see `CF-001` and `G-2` below.** The reference stream is now the single least-settled element of this control |
| **Fail-closed posture** | Matches the platform's existing guard architecture — every stop writes zero files |

## 4.2 · NOT sufficiently specified — four gaps

**`G-1` · Tolerance is undefined — and cannot be defined until `CF-001` is dispositioned.** Against `c13df1f4` the offsets are tight (IQR 1.021 s) and a tolerance is specifiable; against the declared GT-2 they span 50 seconds and no tolerance is meaningful. **The tolerance is a function of which stream is declared authoritative.** The original statement follows. A citation reads `#31 01:51`. **The timecode is minute-and-second; cue starts are millisecond.** `#31` in GT-2 begins at some `MM:SS.mmm`, and agreement must be defined — truncation, rounding, or a window. **At `MM:SS` granularity a one-second window can span two cues in dense passages**, which would make some citations ambiguous rather than agreeing or disagreeing. **This is the single most important unspecified item**, because it determines the boundary between `VALIDATED` and `FAILED`.

**`G-2` · The reference stream is declared by convention, and the one declaration is wrong.** **UPGRADED FROM GAP TO DEFECT, 2026-08-30 — see `CF-001`.** `RIDER_REGISTRY` names GT-2 in a free-text header field; **measurement shows the citations resolve against `Part 2 SRT` `c13df1f4…` instead**, confirmed by timing (median +0.125 s vs +16.479 s) and by text (4 of 4 name matches vs 0 of 4). The other three registries name no stream at all. **`G-2` can no longer be closed by specification alone — it requires an Executive disposition of `CF-001` first.**

**`G-3` · Whether a `FAILED` verdict is a stop or a report.** *"Fail closed"* is stated; what fails closed is not. A validator that halts a run on one stale citation behaves very differently from one that emits a census. **Both are defensible; they are not the same control.**

**`G-4` · The four citation shapes must be parsed, and only two are documented.** `cue: "#N MM:SS"`, `cue: "#N"`, `cues: ["#N", …]`, and index ranges spanning both list and scalar forms. A pattern written for the compound form alone would **silently miss the nine** — reporting 82 of 82 validated and never mentioning the rest. **That is `R-1` reproduced inside the control built to detect it.**

---

# 5 · TWO PROPERTIES WORTH PRESERVING IN ANY IMPLEMENTATION

Observations from the evidence, offered because they are cheap and load-bearing.

**The validator must never read the registries as authority for the stream.** It should resolve indices against a **hash-pinned** caption file and stop if that file's hash does not match its declaration — the same `FAILED_SOURCE_IDENTITY` shape the ETC extractor already uses. **A validator that trusts a free-text header inherits exactly the ambiguity it exists to remove.**

**The verdict counts should be reported, not summarised.** `82 VALIDATED · 0 FAILED · 9 UNVALIDATABLE` is a governed result. **A single pass/fail line, or any percentage without its numerator and denominator, would breach `WET-SPEC-REPORT-001`** and would hide the nine — which are the whole reason the third outcome exists.

---

# 6 · SCOPE BOUNDARY

| in scope for ECR-003 | out of scope |
|---|---|
| Verifying index-against-timecode for the 82 | **Adding timecodes to the 9** — Executive |
| Reporting the 9 as `UNVALIDATABLE` | **Re-pointing any citation** — no authority exists |
| Reporting counts by registry and verdict | **Correcting a `FAILED` citation** — the correction is an Executive act on a governed registry |
| Stopping on source-identity mismatch | **Anything to do with ED-004** — the control is independent of it |

**ECR-003 detects. It does not repair.** Repair of a governed registry entry is not an engineering act.

---

# 7 · SUFFICIENCY VERDICT

```
SPECIFIED SUFFICIENTLY IN PURPOSE AND OUTCOME
NOT YET SPECIFIED SUFFICIENTLY TO IMPLEMENT
```

**The control's intent, verdict set and population are clear and correct.** The three outcomes are exhaustive; the 82 / 9 split is confirmed; the reference stream is identifiable for the largest registry.

**Four gaps must be closed before implementation would be deterministic** — `G-1` tolerance, `G-2` per-registry stream binding, `G-3` what "fail closed" acts on, `G-4` all four citation shapes. **`G-1` and `G-4` are the two that could produce a wrong answer rather than no answer**, and `G-4` in particular would let the control repeat the failure it was built to catch.

**None of the four requires an Executive decision.** They are specification work, and specifying them is not authorized here.

---

```
Control reviewed              ECR-003 Cue Index Validator
Implementation                NONE — nothing built, nothing run, no citation checked
Outcomes confirmed            3 — VALIDATED · FAILED · UNVALIDATABLE, exhaustive
CIA-001 ERRATUM 1             CONFIRMED by independent re-measurement — 82 / 9
Specification gaps            4 — G-1 tolerance · G-2 stream binding
                                  G-3 fail-closed target · G-4 citation shapes
G-2 status                    DEFECT, not gap — CF-001 · declared stream is wrong
G-1 status                    BLOCKED on CF-001 disposition
Timecode additions            NOT RECOMMENDED — Executive, per the Order
Registries modified           NONE
Commits                       NONE
```

---

*Prepared under EDR-001, Platform Engineering Control section. Custody: MACHINE. Authority: NONE. No validator was implemented. No registry, citation, runtime component or source file was modified. No commit was made. No recommendation is made regarding the addition of timecodes to any citation.*
