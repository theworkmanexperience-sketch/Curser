# GER-001 — GOVERNANCE EXCEPTION REPORT

**Occasion:** `EXECUTIVE ORDER — EPR-001 RATIFICATION & RUN_ID LOCK RELEASE`, 2026-08-28, §3
**Reported under:** that Order's own §4 — *"All governance exceptions shall be reported for
Executive review"* · *"The platform SHALL NOT … silently resolve governance exceptions"*
**Custody:** `MACHINE` · **Date:** 2026-08-29
**Status:** **THE REGENERATION WAS NOT EXECUTED.**

---

## 0 · Headline

**§1 and §2 of the Order are applied. §3 is not.**

> The committed `gen_artifacts.py` is **hard-coded to the 2026-08-22 assembly** — the edit this
> platform now classifies `SUPERSEDED_ASSEMBLY`. It cannot run, cannot emit a new `RUN_ID`, and
> if the first two problems were fixed it would emit **seven artifacts describing the wrong
> film**, stamped as the governed record.

Six exceptions follow. **None was resolved, worked around, or patched.** Each is stated with the
evidence that establishes it.

**Why this is reported before execution rather than after.** §4 requires exceptions be reported;
it does not say when. But a regeneration is not a reversible probe — its output *is* the governed
record, and `DOC-002` forbids partial or patched regeneration. Running first and reporting second
would have placed seven artifacts describing a superseded edit into the record under a fresh
`RUN_ID`, and reporting afterwards would not have removed them. **`DOC-001`: validate the
instrument by conformance before trusting its fidelity.** The instrument was inspected, and it
does not conform.

---

## 1 · What WAS applied

| § | action | state |
|---|---|---|
| **§1 · Q10** | `EPR-07` disposition **`RETIRE`**, transcribed verbatim. Entry **retired, not deleted**. `beat: Ride_Home`, `audience_state: Completion`, `segment_refs: [S19]` all untouched. No migration. No replacement content inferred. | **APPLIED** |
| **§1 · consequence** | `EPR-06.terminal_beat_status` `CONTINGENT_ON_EPR-07_DISPOSITION` → **`TERMINAL`** | **APPLIED** |
| **§2** | `EPR-001` **`RATIFIED`**, recorded under `registry_ratification` with the Order's six scope items verbatim, co-ratifying the Authoring Workbook | **APPLIED** |
| **§3** | one atomic regeneration under a new `RUN_ID` | **NOT EXECUTED — see §2 below** |

`EPR-001` is at **v1.13.0**. `V-1`…`V-6` **PASS**. Coverage `observed=19 expected=19`.

---

## 2 · The six exceptions

### `GE-1` — the generator is hard-coded to the superseded assembly · **BLOCKING**

`intelligence/p2/ess/scripts/gen_artifacts.py`, lines 31–37:

```python
SHA=dict(
 mp4  ="a53655fc…f47e",   # Filmage_Editor.mp4, the 320x180 08-22 proxy
 fcpxml="2bf06853…58e7",   # 08-22 lock project
 srt  ="89d61f96…a1c6b",   # 08-22 lock SRT, 2291 cues
 etc  ="e91318a6…010d")    # P2_LOCK_timing.json
LOCK=4846.625
```

**Every one of those four hashes belongs to the assembly the Executive declared
`SUPERSEDED_ASSEMBLY` on 2026-08-28.** The governed production is the 08-24 lineage at
**4689.500 s**. `LOCK` is a constant, not a parameter.

**Consequence if executed:** seven artifacts — `STEP0_TIMING_CLOSURE`, `CAPTION_REGISTRY`,
`VISUAL_EVENT_REGISTRY`, `EDITORIAL_SYNCHRONIZATION`, `CONDUCTOR_SCORE`, `ESS_VALIDATION_REPORT`,
`PRODUCTION_INTELLIGENCE_SEED` — all describing the superseded edit, all stamped as the current
governed record under a fresh `RUN_ID`. **This is the failure class `CUSTODY_ALERT_001` was
raised to prevent and Path B was ratified to correct.**

### `GE-2` — the segment table is hard-coded, in 08-22 seconds, and still contains `S19` · **BLOCKING**

Lines 71–81 hold all nineteen segments as literal second-offsets:

```python
("S16",3523,3985,…), ("S17",3985,4008,…),
("S18",4165,4780,…), ("S19",4784,4846,"friday_wrap_part3_tease",None,[])
```

Three problems in one table:

1. **The spans are 08-22 positions.** The two timelines diverge at `00:03:27.208` and are related
   by five distinct piecewise lags, with regions after ≈`01:04` that have no counterpart at all.
2. **`S19` is baked in** — the segment the Executive **retired minutes ago**. So is `CUE-10` at
   `4784–4846` (line 292). A run would re-emit retired material.
3. **`S18` runs to 4780 s**, beyond the governed production's 4689.500 s end (`PBC-2`).

### `GE-3` — the generator cannot run at all · **BLOCKING**

Lines 39–43 read five intermediate files from cloud paths belonging to the 2026-08-22 session:

```
W = "/home/claude/work/out/"
  timeline_resolved.json · step0_offset.json · step0_anchors.json
  die_v_observables.json · camera_runs.json
```

**Searched both mounted volumes. All five: `NOT FOUND`.**

```
timeline_resolved.json   -> NOT FOUND
step0_offset.json        -> NOT FOUND
step0_anchors.json       -> NOT FOUND
die_v_observables.json   -> NOT FOUND
camera_runs.json         -> NOT FOUND
```

The generator would raise `FileNotFoundError` on its first `json.load`. **This is the same defect
class already reported for `epr_validate.py` in `EPR-001_VALIDATION_REPORT_PATH_B.md` §1.2 —
committed code carrying dead authoring-environment paths — except here it is fatal rather than a
nuisance.**

### `GE-4` — "a newly generated `RUN_ID`" is not implementable by the current code · **CONTRADICTION**

Lines 14–15:

```python
RUN_ID     ="WECAPE-AR2-SPRINT3A-20260822-114028"
REGEN_RUN_ID="WECAPE-AR2-ESS004-REGEN-20260822-174500"
```

Both are **string constants**, written into fourteen places across the seven artifacts.

§3 instructs two things that cannot both hold:

> *"execute one and only one atomic regeneration pass **under a newly generated RUN_ID**"*
> *"Execute the generator **exactly as governed by the current platform architecture**."*

**The current implementation cannot generate a `RUN_ID`.** Making it do so is a code change, which
the second sentence forecloses. **Raised, not resolved — the platform did not edit the generator
to satisfy the Order.**

### `GE-5` — every ingestion precondition is unmet · **BLOCKING**

From `intelligence/p2/ingest_0824/INGESTION_MANIFEST.yaml`, prepared under the 2026-08-28 Order §2.5:

| id | requirement | status |
|---|---|---|
| `IP-1` | Editorial Timing Contract for the 08-24 lineage | **`NOT_PRODUCED`** |
| `IP-2` | `fcpx_resolve.py` re-validated against that ETC (`DOC-001`) | **`NOT_VALIDATED`** |
| `IP-3` | conformant viewing master exported and designated | **`NOT_DESIGNATED`** |
| `IP-4` | collapse rule declared for the doubled Parent SRT cues | **`NOT_DECLARED`** |
| `IP-6` | segment set for the governed production ratified | **`NOT_DERIVED`** |
| `IP-7` | episode boundaries assigned to segments | **`NOT_DERIVABLE`** without `IP-1` |
| `IP-8` | `SOP-06` Phase A re-export and `GATE-1` custody audit | **`NOT_PERFORMED`** |

**`IP-2` is the one that matters most under `DOC-001`.** `fcpx_resolve.py` is validated 191/191
against the **08-22** ETC. There is no ETC for the 08-24 lineage to validate it against. An
unvalidated resolver measuring an unmeasured timeline produces numbers that look authoritative and
are not.

### `GE-6` — three ESS PDRs remain OPEN and name two of the seven artifacts · **PROCEDURAL**

`GATE-2026-08-22-MIE-DOWNSTREAM` reads `state: CLOSED`, `authorized: false`, `open: 3`.

| PDR | status | `regenerates_on_disposition` |
|---|---|---|
| `ESS-001` S16 label vs observed illumination | **OPEN** | `EDITORIAL_SYNCHRONIZATION`, `CONDUCTOR_SCORE` |
| `ESS-002` escort ride vs CUE-03 span | **OPEN** | `EDITORIAL_SYNCHRONIZATION`, `CONDUCTOR_SCORE` |
| `ESS-003` caption policy vs locked cut | **OPEN** | `CAPTION_REGISTRY`, `EDITORIAL_SYNCHRONIZATION` |

Regenerating now would emit those artifacts **ahead of three dispositions whose stated purpose is
to change them.** The gate's `unblock_condition` is explicit: *"Partial disposition does not
partially open this gate."*

**Note on scope, so this is not overstated:** this gate governs downstream **MIE** work, and the
Order released the **`RUN_ID`** lock, which is a different instrument. `GE-6` is raised as a
procedural exception, **not** as a claim that the gate forbids the run.

---

## 3 · What a conforming execution would require

**Stated as analysis. No part of it is authorized, and none of it was done.**

| # | prerequisite | maps to |
|---|---|---|
| **1** | `SOP-06` Phase A re-export of the 08-24 lineage; `GATE-1` custody audit recorded | `IP-8` |
| **2** | four input hashes pinned; **Editorial Timing Contract produced** | `IP-1` |
| **3** | `fcpx_resolve.py` **re-validated** against that ETC, agreement stated as a number | `IP-2`, `DOC-001` |
| **4** | the five intermediate JSONs regenerated by `step0_*.py`, `die_v_observables.py`, `fcpx_resolve.py` | `GE-3` |
| **5** | `gen_artifacts.py` parameterised: `SHA`, `LOCK`, `SEG`, `CUES`, `RUN_ID` become inputs, not constants | `GE-1`, `GE-2`, `GE-4` |
| **6** | segment set re-derived and **Executive-ratified**; `S19` removed per the retirement | `IP-6`, `GE-2` |
| **7** | conformant viewing master exported and designated | `IP-3` |

**Item 5 is a code change to a governed generator.** Under `DOC-002` — *regenerate, never patch* —
and `ADR-009` §2 — these artifacts are regenerate-on-mismatch and never hand-edited — the change
belongs to the generator, not its output. **It is engineering work and it is not authorized by any
Order to date.**

---

## 4 · What the platform did NOT do

Enumerated against the Order's own §4 prohibitions.

| §4 prohibition | compliance |
|---|---|
| infer Executive intent | **none inferred.** `RETIRE` was transcribed; the four `EPR-07` fields were left literally `AWAITING_EXECUTIVE_INPUT` rather than overwritten with a tidier sentinel |
| repair Executive declarations | **none repaired.** `EPR-06`'s `editorial_transition` was **not** re-read or rewritten against its new terminal status |
| populate missing Executive fields | **none populated** |
| silently resolve governance exceptions | **none resolved.** Six are reported here and nothing was patched to get past them |
| regenerate a second `RUN_ID` without authorization | **no `RUN_ID` was generated and no regeneration ran at all** |

**Also not done, and worth naming:** the generator was **not** edited to make the run possible.
Fixing `GE-3`'s dead paths would have taken minutes and would have produced a *running* generator
that emitted the wrong film — **the most dangerous of the available outcomes, because it would
have looked like success.**

---

## 5 · One consequence of the retirement, reported not resolved

`EPR-07` is retired. Its four fields remain literally `AWAITING_EXECUTIVE_INPUT` because they were
never declared and now never will be. **The platform did not overwrite them** — writing into an
Executive-custody field to tidy a count would be authoring.

> **`V-6` will therefore keep reporting `AWAITING_EXECUTIVE_INPUT=4` on a ratified registry.**
> That count is a property of a retired entry, not outstanding Executive work.

Whether the validator should distinguish "never declared" from "retired without declaration" is an
**engineering question requiring a code change.** None is authorized. Raised so the number is not
later misread as an incomplete ratification.

---

## 6 · Standing state

```
Q10                              ADJUDICATED - RETIRE
EPR-001                          RATIFIED, v1.13.0, V-1..V-6 PASS
EPR-06                           TERMINAL
segment coverage S01-S18         COMPLETE - observed=19 expected=19
RUN_ID lock                      RELEASED by Executive Order
atomic regeneration              NOT EXECUTED - GE-1..GE-6
artifacts emitted                NONE
gen_artifacts.py                 UNMODIFIED
registries populated             NONE
Conductor Score                  NOT GENERATED
GATE-2026-08-22-MIE-DOWNSTREAM   CLOSED - 3 of 4 PDRs OPEN, unchanged
```

**The lock is released and the door behind it does not open onto the governed production.** The
authoring phase is complete; the *ingestion* phase never began, and the generator still points at
the film that was superseded.

*Custody `MACHINE`. Six exceptions reported, none resolved. No artifact was generated, no
generator was modified, no Executive field was populated or repaired.*
