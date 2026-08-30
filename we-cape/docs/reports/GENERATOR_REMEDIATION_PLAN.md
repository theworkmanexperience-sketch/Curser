# GENERATOR REMEDIATION PLAN

**Issued under:** EXECUTIVE ORDER `EO-WET-EXEC-017` — Finding 4, Executive Producer / Chairman, 2026-08-30
**Prepared by:** Governance Compliance Auditor · **Custody:** `MACHINE` · **Authority:** NONE
**Repository:** READ ONLY at `b4d8529` · **Commits:** none

> # THIS IS ENGINEERING PLANNING ONLY
>
> **No code. No commits. No implementation.** Per `EO-WET-EXEC-017` Finding 4, this stage *"is engineering work. It is not governance. It is not an Executive Determination. It remains unauthorized until separately approved."*
>
> **Nothing in this plan is authorized by `EO-WET-EXEC-017`.** Every work item below awaits a separate Executive Order.

---

# 1 · THE STANDING DEFECT SET

`GER-001` reports six exceptions. **Five are BLOCKING or CONTRADICTION. None has been resolved.** `[E]`

| id | defect | class |
|---|---|---|
| `GE-1` | the generator is hard-coded to the **superseded** assembly | **BLOCKING** |
| `GE-2` | the segment table is hard-coded, **in 08-22 seconds**, and still contains `S19` | **BLOCKING** |
| `GE-3` | **the generator cannot run at all** | **BLOCKING** |
| `GE-4` | *"a newly generated `RUN_ID`"* is not implementable by the current code | **CONTRADICTION** |
| `GE-5` | every ingestion precondition is unmet | **BLOCKING** |
| `GE-6` | three ESS PDRs remain OPEN and name two of the seven artifacts | **PROCEDURAL** |

**`GE-3` is the one that governs sequencing.** The generator reads five intermediate JSONs from cloud paths belonging to the 2026-08-22 authoring session:

```
W = "/home/claude/work/out/"
  timeline_resolved.json · step0_offset.json · step0_anchors.json
  die_v_observables.json · camera_runs.json
```

**All five: `NOT FOUND` on both mounted volumes.** *"The generator would raise `FileNotFoundError` on its first `json.load`."* `[E]`

**This is not a configuration problem. The generator has never been runnable in this repository.** `GER-001` names the class: *"committed code carrying dead authoring-environment paths — except here it is fatal rather than a nuisance,"* the same defect already reported for `epr_validate.py`.

---

# 2 · WORK ITEMS

**Enumerated from `EO-WET-EXEC-017` Finding 4 and `GER-001` §3. Nothing added.**

| # | work item | closes | class |
|---|---|---|---|
| **W-1** | Parameterise `SHA` — the four input hashes become inputs | `GE-1` | engineering |
| **W-2** | Parameterise `LOCK` — currently the constant `4846.625`; the 08-24 lineage is `4689.500` | `GE-1` | engineering |
| **W-3** | Parameterise `SEG` — the segment table becomes an input, not a literal | `GE-2` | engineering |
| **W-4** | Parameterise `CUES` | `GE-2` | engineering |
| **W-5** | Parameterise `RUN_ID` — currently two string constants written into **fourteen places across seven artifacts** | `GE-4` | engineering |
| **W-6** | Remove hard-coded assembly assumptions — the generator points at the superseded film | `GE-1` | engineering |
| **W-7** | Remove superseded segment assumptions — `S19` removed per the retirement | `GE-2` | engineering |
| **W-8** | Implement the current execution model — regenerate the five intermediate JSONs via `step0_*.py`, `die_v_observables.py`, `fcpx_resolve.py` rather than reading dead paths | `GE-3` | engineering |
| **W-9** | Ingestion readiness — `IP-1`…`IP-8` | `GE-5` | **mixed — §4** |

**`GER-001` §3 on `W-1`…`W-7`:** *"**Item 5 is a code change to a governed generator.** Under `DOC-002` — regenerate, never patch — and `ADR-009` §2… **the change belongs to the generator, not its output.** It is engineering work and it is not authorized by any Order to date."* `[E]`

**Scale, measured.** `PRR-001`: *"12 of 18 ESS scripts carry `0822` literals · `gen_artifacts.py` 16."* **The hard-coding is not confined to the generator**, and a remediation scoped to `gen_artifacts.py` alone would leave eleven other scripts bound to one edit. `[E]`

---

# 3 · WHAT `W-9` ACTUALLY CONTAINS — AND WHY IT IS NOT ALL ENGINEERING

**`GE-5` records every ingestion precondition unmet.** Four of the seven are **not engineering work at all** — they are Executive determinations that live in Roadmap Stage 2B:

| id | requirement | status | who closes it |
|---|---|---|---|
| `IP-1` | Editorial Timing Contract for the 08-24 lineage | `NOT_PRODUCED` | **producible** — needs `ED-003` first |
| `IP-2` | `fcpx_resolve.py` re-validated against that ETC | `NOT_VALIDATED` | engineering — needs `IP-1` |
| `IP-3` | conformant viewing master exported and designated | `NOT_DESIGNATED` | **Executive — `ED-005`** |
| `IP-4` | collapse rule declared for the doubled Parent SRT cues | `NOT_DECLARED` | **Executive — `ED-004`** |
| `IP-6` | segment set ratified | `NOT_DERIVED` | **Executive ratification** |
| `IP-7` | episode boundaries assigned | `NOT_DERIVABLE` without `IP-1` | derived |
| `IP-8` | `SOP-06` Phase A re-export · `GATE-1` custody audit | `NOT_PERFORMED` | process |

**This is the plan's most important structural finding: Generator Remediation cannot fully complete inside its own stage.** `W-1`…`W-8` are pure engineering and can be authorized as one body of work. **`W-9` is blocked on Stage 2B determinations that no amount of engineering can supply.** `[E]`

**`IP-2` carries the sharpest risk, and `GER-001` states it:** *"`fcpx_resolve.py` is validated 191/191 against the **08-22** ETC. There is no ETC for the 08-24 lineage to validate it against. **An unvalidated resolver measuring an unmeasured timeline produces numbers that look authoritative and are not.**"* **`DOC-001` — validate the instrument before the measurement — is the doctrine that forbids proceeding here.** `[E]`

---

# 4 · ENTRY CONDITIONS

| # | condition | state |
|---|---|---|
| 1 | Stage 3 complete — `EGS-001` v1.0 and Lifecycle v1.0 exist and are ratified | **not started** |
| 2 | **`ED-006` — the `RUN_ID` lock state determined** | **CONTRADICTION — Executive determination required** |
| 3 | A separate Executive Order authorizing engineering work | **does not exist** |
| 4 | For `W-9` only: Stage 2B determinations `CF-001` `ED-003` `ED-004` `ED-005` | **all open** |

**On condition 2.** `LOCK_RECONCILIATION_REVIEW.md` finds one lock instrument recorded in two states. **The determination is required before this stage regardless of which way it resolves** — and `GER-001` §6 records why resolving it is necessary but not sufficient: *"The lock is released and the door behind it does not open onto the governed production."* `[E]`

---

# 5 · PROPOSED ACCEPTANCE — NOT SET

> **Acceptance criteria for engineering work are an Executive act. Proposed for adoption; not in force.** `[O]`

| # | proposed criterion |
|---|---|
| **G-1** | **No literal remains.** `SHA` `LOCK` `SEG` `CUES` `RUN_ID` are parameters. Zero `0822` literals in the remediated generator, enumerable |
| **G-2** | **The generator runs.** `GE-3` closed — five intermediate JSONs produced by their own producers, not read from dead paths |
| **G-3** | **Regression on the known-good lineage.** The remediated generator, given the 08-22 inputs, reproduces the 08-22 artifacts **byte-for-byte** |
| **G-4** | **Second-lineage execution.** It runs against the 08-24 lineage without code change — parameters only |
| **G-5** | **Fail-shut.** Every stop writes zero files. `S19` cannot re-enter |
| **G-6** | **`DOC-002` respected.** Artifacts regenerated, never patched |
| **G-7** | **No Executive field authored.** `EPR-001 §2.3` — nothing populated, inferred, extended, suggested or defaulted |

**`G-3` is the criterion worth insisting on, and there is precedent.** `ED-001A` gated the ETC extractor on byte-equality against the surviving 08-22 artifact, and it held — `e91318a6…010d`, 183,116 bytes, reproduced exactly. **The same instrument is available here:** the seven 08-22 artifacts exist and were produced by the pre-remediation generator. **A remediation that cannot reproduce them has changed behaviour while claiming to change only structure.**

**One honest limit on `G-3`.** It can only be run if the five intermediate JSONs can be reconstituted for the 08-22 inputs — which is `W-8`, and `GE-3` records the originals as `NOT FOUND`. **If they cannot be reconstituted, `G-3` is unavailable and the remediation has no regression gate.** That is a material risk and it is stated rather than assumed away. `[O]`

---

# 6 · RISKS RECORDED

| risk | basis |
|---|---|
| **`G-3` may be unavailable** — the 08-22 intermediates are `NOT FOUND`; reconstituting them is itself `W-8` | `GE-3` `[E]` |
| **Remediation scoped to one file leaves 11 other scripts hard-coded** — 12 of 18 ESS scripts carry `0822` literals | `PRR-001` `[E]` |
| **`W-9` cannot complete inside this stage** — four of seven ingestion preconditions are Executive determinations | `GE-5` `[E]` |
| **`IP-2` invites an authoritative-looking wrong answer** — unvalidated resolver, unmeasured timeline | `DOC-001` `[E]` |
| **`GE-6` — three ESS PDRs OPEN**, naming two of the seven artifacts; procedural, not closed by code | `GER-001` `[E]` |

---

# 7 · WHAT THIS PLAN DID NOT DO

| | |
|---|---|
| Write, modify or propose code | **no** |
| Modify `gen_artifacts.py` or any script | **no** |
| Change any lock state | **no** |
| Resolve any `GE-` exception | **no** |
| Set an acceptance criterion | **no — proposed only** |
| Authorize any work item | **no** |
| Create a commit | **no** |

---

```
GENERATOR REMEDIATION PLAN            PLANNING ONLY

Standing exceptions                   6   ·   5 BLOCKING/CONTRADICTION   ·   0 resolved
Work items                            9   ·   8 pure engineering   ·   1 mixed (W-9)
Entry conditions                      4   ·   satisfied 0
Proposed acceptance criteria          7   ·   in force 0
Ingestion preconditions               7   ·   met 0   ·   4 are Executive acts

Code written                          NONE
Generator modified                    NONE
Lock state changed                    NONE
Commits                               NONE
Authorization                         NOT GRANTED — separate Order required
```

---

*Prepared under `EO-WET-EXEC-017` Finding 4. Custody: `MACHINE`. Authority: NONE. No code was written, no generator modified, no defect resolved, no acceptance criterion set, no work authorized, and no commit made.*
