# ED-001 — PHASE 1 EXECUTION RECORD
## Completion of the 08-24 Ingestion Lineage · First Execution Pass

**Issued under:** EXECUTIVE DISPOSITION ED-001, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE
**Measured at:** repository HEAD `dac9a34` · `WE_CAPE_OUTPUT` volume, live
**State:** one objective **COMPLETE**, one **BLOCKED ON A MISSING PRODUCER**, three **BLOCKED ON EXECUTIVE DETERMINATION**
**Commits made:** none. PD-001's *"no commits unless explicitly authorized"* was not lifted by ED-001 in those words.

---

# 1 · OBJECTIVE STATE

| # | ED-001 Phase 1 objective | state | blocked on |
|---|---|---|---|
| 1 | Produce the missing `sha.etc` artifact | **BLOCKED** | The ETC producer **does not exist in version control**, and the source FCPXML is undesignated — §3, §4.1 |
| 2 | Clear the active generator lock | **BLOCKED** | Release condition is Workbook completion **and** EPR-001 ratification — both Executive acts — §4.2 |
| 3 | Complete the governed ingestion chain | **BLOCKED** | Master picture undesignated · caption collapse rule undeclared — §4.3, §4.4 |
| 4 | **Validate doctrine against the timestamp conflict** | **COMPLETE** | — §2 |
| 5 | Close the current production lineage | **BLOCKED** | Depends on 1–3 |

**One of five objectives was executable by the platform. It was executed, and the doctrine held.**

---

# 2 · OBJECTIVE 4 — DOCTRINE VALIDATED AGAINST REAL EVIDENCE CONFLICT

**COMPLETE.** This is the first time the ratified time clauses have been run against a live conflict rather than described.

## 2.1 · The instrument, declared before the measurement

Per `DOC-001`. Three time expressions were read per file and are named individually, because **two of them are the same source wearing different clothes.**

| expression | how obtained | independent of the camera clock? |
|---|---|---|
| filename token | `20181002_HHMMSS` in the name | **no** — written by the camera |
| embedded `creation_time` | `ffprobe -show_entries format_tags=creation_time` | **no** — written by the camera |
| filesystem `mtime` | `stat -c %y` | **only where the copy did not preserve it** |

**Counting three sources that agree would have been the error this doctrine exists to prevent.** Two of the three derive from one clock. Agreement between them is not corroboration.

## 2.2 · Measurement

Ten files. Insta360 X5. Neither `.DS_Store` nor brand assets; shoot media.

```
file                              filename token    embedded creation_time      mtime                  dur (s)
LRV_20181002_004856_01_001.lrv    20181002_004856   2018-10-02T05:48:56Z        2018-10-02 05:51:42     164.44
LRV_20181002_005205_01_002.lrv    20181002_005205   2018-10-02T05:52:05Z        2018-10-02 06:22:07    1798.00
LRV_20181002_005205_01_003.lrv    20181002_005205   2018-10-02T06:22:04Z        2018-10-02 06:52:05    1798.00
LRV_20181002_005205_01_004.lrv    20181002_005205   2018-10-02T06:52:02Z        2018-10-02 07:22:04    1798.00
LRV_20181002_005205_01_005.lrv    20181002_005205   2018-10-02T07:22:01Z        2026-06-25 08:24:40    1681.40
VID_20181002_004856_00_001.insv   20181002_004856   2018-10-02T05:48:56Z        2018-10-02 05:51:41     164.42
VID_20181002_005205_00_002.insv   20181002_005205   2018-10-02T05:52:05Z        2018-10-02 06:22:06    1798.00
VID_20181002_005205_00_003.insv   20181002_005205   2018-10-02T06:22:04Z        2018-10-02 06:52:04    1798.00
VID_20181002_005205_00_004.insv   20181002_005205   2018-10-02T06:52:02Z        2018-10-02 07:22:03    1798.00
VID_20181002_005205_00_005.insv   20181002_005205   2018-10-02T07:22:01Z        2026-06-25 08:24:40    1681.40
```

## 2.3 · Three structural observations

**O-1 · The camera-clock chain is internally perfect.** Each clip's `creation_time` plus its duration lands within ~2 s of the next clip's `creation_time`:

```
001  05:48:56 + 164.44  → 05:51:40    next 05:52:05
002  05:52:05 + 1798    → 06:22:03    next 06:22:04
003  06:22:04 + 1798    → 06:52:02    next 06:52:02
004  06:52:02 + 1798    → 07:22:00    next 07:22:01
005  07:22:01 + 1681.4  → 07:50:02
```

**One continuous ~2-hour recording run, chaptered at 30 minutes.** The clock is consistent. It is consistently *wrong*, which is a different property, and no internal check could have caught it.

**O-2 · The only non-camera timestamp disagrees, and it is shared by exactly two files.** `mtime 2026-06-25 08:24:40.010` appears on precisely the `.insv`/`.lrv` pair of clip `_005` **and on nothing else on the card.** A single timestamp shared by one clip's two representations is the signature of a **file-copy event, not a recording event.** The other eight files retain camera-derived mtimes because the copy preserved them.

**O-3 · The camera's own sequence counter is continuous across the clock change.** On the same card:

```
VID_20181002_005205_00_005.insv     ← stamped 2018-10-02
VID_20260625_040546_00_006.insv     ← stamped 2026-06-25 04:05:46
VID_20260625_041537_00_007.insv
VID_20260625_043319_00_008.insv …
```

**`_005` and `_006` are consecutive clips in one unbroken counter.** The camera did not reset. The clock was corrected between them.

## 2.4 · Disposition, per doctrine

The ratified clause requires that **canonical time be derived from evidence** and that **evidence conflicts produce an explicit unresolved state, never a silent winner.**

```
CHRONOLOGY_CONFLICT           CC-001
files                         10  (5 clips × .insv/.lrv)
camera clock                  FALSIFIED — claims 2018-10-02 on a 2026 production
independent absolute source   NONE PRESENT IN THE FILES

ESTABLISHED
  relative ordering           these 10 files precede VID_20260625_040546_00_006
                              in the camera's own unbroken sequence, same card
  internal continuity         one ~2h run, chaptered at 30 min, no internal gap
  upper bound                 recorded before 2026-06-25 04:05:46 camera-corrected time

NOT ESTABLISHED
  absolute recording time     the only clock that recorded it is falsified
  shoot-day assignment        UNRESOLVED
  Day 3 membership            these files carry no 2026 date token and are NOT
                              in the 98-file Day 3 census

DISPOSITION                   UNRESOLVED — REQUIRES DECLARED DISPOSITION
SILENT RECONCILIATION         PROHIBITED and not performed
```

**The tempting inference was available and was not taken.** `_005`'s copy timestamp is 25 June 2026 and `_006` is stamped 25 June 2026 — it would have been easy to assign the run to Day 1 and move on. **A copy time is not a recording time, and an adjacent clip's clock is not this clip's clock.** The platform records the ordering it can prove and stops at the date it cannot.

**Doctrine outcome: the clauses worked.** They produced a bounded, useful, honest result — an ordering and an upper bound — and refused the date. That is `DOC-001` and the conflict clause functioning on real evidence for the first time, and it is the substantive success of Phase 1.

---

# 3 · OBJECTIVE 1 — THE ETC PRODUCER IS NOT IN VERSION CONTROL

**This is the third instance of the platform's signature failure pattern, and the most consequential.**

```
P2_LOCK_timing.json          the 08-22 Editorial Timing Contract
present in repository        NO      (find returns nothing)
git history                  NONE    (git log --all returns nothing)
committed code that writes   NONE
committed code that reads    fcpx_resolve.py · build_context.py · gen_artifacts.py · gen_artifacts_v2.py
documents citing as authority 10
```

**Every committed script consumes the ETC. None produces it.** The artifact that `PDR-2026-08-20-ETC-001` elevated to *"a first-class governed artifact class"* — one of four authoritative production artifacts — was made by something that was never committed.

The same shape as the missing `.npy` producers and the `191/191` hard-coded string: **a governed artifact whose authority rests on a producer that cannot be inspected, re-run, or verified.**

## 3.1 · What is recoverable

The 08-22 ETC exists on the volume in **two byte-identical copies** (`e91318a6719c81e4…`), and its `source_sha256` matches `PDR-2026-08-20-ETC-001` exactly:

```
source_sha256        2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7   ✓ matches the PDR
sequence             {duration_s: 4846.625, format_ref: "r1", declared_lock: "01:20:46:14"}
spine                list[191]   {depth, duration_s, lane, name, parent, rel_offset_s,
connected_elements   list[404]    source_start_s, tag, timeline_offset_s}
```

**The output contract is fully specified by the surviving instance.** A conformant FCPXML→ETC extractor is buildable, and its correctness is testable the only way that counts: **regenerate the 08-22 ETC from the 08-22 FCPXML and require byte equality with `e91318a6…` before it is ever pointed at 08-24.** That is `DOC-001` — validate the instrument before the measurement — and it is the same method that caught the `191/191` defect.

## 3.2 · Why this requires your word

ED-001's Engineering Constraint: *"No new platform capabilities shall be introduced during execution **unless a critical operational defect prevents completion**."*

**A missing producer for a first-class governed artifact is that defect.** Objective 1 cannot be executed without building the extractor. I am not treating the exception as self-invoking — building it is real engineering, and it also changes what the repository says about the 08-22 ETC's provenance.

---

# 4 · FOUR DETERMINATIONS ONLY THE EXECUTIVE CAN MAKE

ED-001 states *"No further governance instruments are required before operational work begins."* **That is correct for beginning and not correct for completing.** These are not new instruments — they are four specific determinations, each of which the repository explicitly reserves.

## 4.1 · Which FCPXML is the 08-24 picture lock

`PDR-2026-08-20-ETC-001` derives the ETC from the **picture-locked** FCPXML. The 08-24 context points at `analysis_cut/Info_analysiscut.fcpxml` (`1ab3d12f…`, 4689.5 s). **An analysis cut is not a picture lock**, and the repository nowhere declares that it is.

## 4.2 · Release of the generator lock

```
gen_artifacts_py         LOCKED
run_id_lock_held_by      EXECUTIVE ORDER 2026-08-28 section 4
release condition        Executive Authoring Workbook complete AND EPR-001 formally ratified
```

`EPR-001 §2.3`: *"The platform SHALL NOT author, populate, infer, extend, suggest, or default ANY EPR-001 value. An empty field remains empty."* **The platform cannot complete the Workbook and cannot ratify EPR-001.** Objective 2 is not a platform act.

## 4.3 · Designation of the master picture

`INGESTION_MANIFEST.yaml`, verbatim:

> `current_register_status: REFERENCE_ONLY` · `ingestion_status: BLOCKED`
> *"…quarantined REFERENCE_ONLY hazard HIGH… **EQUALITY OF DURATION IS NOT IDENTITY OF SOURCE** and no comparison of its picture against the governed timeline has been performed. **Whether it is the production's viewing master is an EXECUTIVE determination. NOT ASSERTED HERE.**"*

## 4.4 · The caption collapse rule

`INGESTION_MANIFEST.yaml`, verbatim:

> `known_defects: [DOUBLED_CUES, NONPOSITIVE_DURATION_CUES]`
> *"A declared collapse rule for the doubled cues **MUST precede ingestion.** Any consumer that counts cues or sums caption time will otherwise be wrong. **No collapse rule has been declared. NOT AUTHORED HERE.**"*

This one has reach beyond ingestion: **the 91 SRT-cue-index citations across four registries** identified in PRR-001 §4.4 are counted against a caption stream whose cue count is currently undefined.

---

# 5 · ONE HYPOTHESIS TESTED AND WITHDRAWN

Recorded because a review that published only its successes would misrepresent the method.

**I computed that the three episodes sum to 4884.23 s against a parent sequence of 4689.5 s and formed the hypothesis that they overlap at the seams and therefore are not a partition of the parent** — which, had it held, would have meant an ETC derived from the parent could not describe the episodes.

**`DAY2_PARENT_FORENSIC_AUDIT.md` had already resolved it, correctly and more rigorously than my arithmetic.** Findings F-1, F-2 and G-1: the Parts are *contiguous, in-order, non-overlapping extracts spanning the Parent end to end*. The 194.32 s excess is fully itemised — two 73.8 s re-prepended openings, two joins of 1.4 s and 1.8 s, three uncaptioned tails — with `UNACCOUNTED_RUNTIME = 0.000 s`, and the audit explicitly declines to treat its own 0.001 s residual as independent validation.

**My hypothesis was wrong and is withdrawn.** The audit is sound and Phase 1 inherits a correct partition.

---

# 6 · WHAT PROCEEDS WITHOUT ANY FURTHER DETERMINATION

- **`CC-001` stands as recorded** — the chronology conflict is classified, bounded, and explicitly unresolved. It requires a declared disposition, not further measurement.
- **Day 3 source census** is complete and holds: 98 files, 179.0 GB, three cameras.
- **Front-half tooling** remains runnable on any material at any time.

## What does not

Everything downstream of the four determinations in §4, and Objective 1 pending your word on §3.2.

---

# 7 · THE SHORTEST PATH YOU HAVE

Stated as sequence, not as recommendation. Each item is one determination or one bounded build.

```
1  declare which FCPXML is the 08-24 picture lock                    §4.1
2  authorize the ETC extractor under the ED-001 critical-defect
   exception, gated on byte-reproducing the 08-22 ETC first          §3.2
3  declare the caption collapse rule                                 §4.4
4  determine the master picture, or declare it out of scope for
   the ETC                                                           §4.3
5  complete the Workbook and ratify EPR-001 — releases the lock      §4.2
6  declare a disposition for CC-001                                  §2.4
```

**Item 2 is the one with lasting value beyond this lineage.** A committed, tested ETC extractor converts the ETC from an artifact the platform trusts into one it can produce — and that is the single largest remaining piece of the back-half coupling PRR-001 measured.

---

```
Objectives complete                1 of 5
Doctrine validated on real evidence YES — CC-001, first live exercise
Silent reconciliation performed     NONE
Hypotheses withdrawn                1, recorded
Files modified                      0
Commits made                        0
Executive determinations required   4, plus one authorization
```

---

*Prepared under ED-001 Phase 1. Custody: MACHINE. Authority: NONE. No engineering artifact, registry, generator, specification, doctrine, Executive Order, narrative declaration, production artifact, or source file was modified. Nothing was committed.*
