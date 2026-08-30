# PLR-001 — PICTURE LOCK REVIEW

**Issued under:** EXECUTIVE REVIEW ORDER PLR-001, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. No repository modification, no engineering, no commit, no determination.
**Measured at:** repository HEAD `1552e42` · `WE_CAPE_OUTPUT` volume, live

> **This review recommends. It does not designate.** Designation of the Picture Lock is Executive authority and is not exercised here.

---

# 1 · THE CANDIDATE, AND A PATH DISCREPANCY

## 1.1 · Recorded, not normalized

The Order names:

```
…/ALPHA ROUND UP Day 2 Part 2/Analysis_Day_2_Part_1_video/Alpha RoundUp Part 2.fcpxml
```

The filesystem holds:

```
…/ALPHA ROUND UP Day 2 Part 2/Analysis_Day_2_Part_1_video/Alpha RoudUp Part 2.fcpxmld/Info.fcpxml
```

**Two differences, neither normalized nor assumed:**

| | Order | filesystem |
|---|---|---|
| container | `.fcpxml` — a flat file | **`.fcpxmld` — a bundle directory**, whose FCPXML is `Info.fcpxml` inside it |
| spelling | `Alpha RoundUp Part 2` | **`Alpha RoudUp Part 2`** — missing `n`, and the same misspelling appears in the FCPXML's own `<project name>` attribute |

**The Chairman confirmed the `.fcpxmld` bundle path during this review.** The candidate is therefore identified without ambiguity. The misspelling is carried in the project name itself and is a property of the edit, not a filesystem accident — it is recorded because a future search on the correct spelling will not find this file.

## 1.2 · Identity by hash

```
Alpha RoudUp Part 2.fcpxmld/Info.fcpxml
  sha256      1ab3d12f0dd150c63907a4b2e4bac4253baf8100910dfda74daa3a5378b6b4d2
  bytes       5,144,601
  mtime       2026-08-24 17:14
```

**This file is byte-identical to `SPRINT3A_WORK/analysis_cut/Info_analysiscut.fcpxml`.** Two paths, one artifact. `[E]`

---

# 2 · IDENTITY — DOES IT REPRESENT ONE GOVERNED EDITORIAL SEQUENCE?

**Yes, structurally.** `[E]`

```
fcpxml version   1.14
sequences        1          format r1 · tcStart 0s · tcFormat NDF · audioRate 48k
projects         1          name "Alpha RoudUp Part 2"
                            uid  4E6BD95F-6D09-48A2-9336-E9CBB2CF74B1
                            modDate 2026-08-23 22:11:47 -0500
events           1          name "P2_CHRONO_SETS"
sequence duration 225096000/48000s = 4689.500 s
```

**Exactly one sequence.** The ETC extractor's first guard — *expected exactly 1 `<sequence>`* — passes. A multi-sequence project would not be a single picture lock and would stop the extractor.

**One observation, unresolved.** The project `modDate` is **2026-08-23 22:11:47 −0500**. The lineage this file is proposed to lock is designated *08-24*. The edit therefore predates the lineage label by roughly one day. This is consistent with the file having been *found* on 08-24 rather than *made* on 08-24, which is what `CUSTODY_ALERT_001` records. **No conclusion is drawn.** `[O]`

---

# 3 · COMPLETENESS — CAN THE ETC BE GENERATED FROM IT?

**Yes, with one field that is never derivable from any FCPXML.** `[E]`

Every input the committed extractor requires is present:

| ETC field | source in this file | present |
|---|---|---|
| `source_sha256` | computed over the file | ✓ |
| `sequence.duration_s` | `<sequence duration>` → 4689.500 | ✓ |
| `sequence.format_ref` | `<sequence format>` → `r1` | ✓ |
| `spine` | 201 depth-0 elements | ✓ |
| `connected_elements` | 455 emitted descendants | ✓ |
| `sequence.declared_lock` | **not present, and not present in any FCPXML** | ✗ |

**`declared_lock` is a human declaration.** It does not appear in the 08-22 lock either — verified by direct search — and the extractor emits `null` rather than inventing one. **A picture-lock designation that does not also declare a lock timecode yields an ETC with a null in that field.** That is a governed outcome, not a failure, but the Executive should know it is a consequence of the determination.

## 3.1 · The census this file would produce

**Derived by structural parse only. No ETC artifact was written for this lineage** — ED-001A §3 and §6 forbid it and the authorization is concluded.

| | **candidate** `1ab3d12f` | 08-22 governed lock `2bf06853` | delta |
|---|---|---|---|
| sequence duration | **4689.500 s** | 4846.625 s | **−157.125 s** |
| raw depth-0 children | 225 | 214 | +11 |
| — asset-clip | 188 | 180 | +8 |
| — transition | 24 | 23 | +1 |
| — clip | 8 | 8 | 0 |
| — gap | **5** | **3** | **+2** |
| **ETC spine** | **201** | 191 | +10 |
| **ETC connected** | **455** | 404 | +51 |

**The candidate is 157.125 s shorter and carries 8 more asset-clips.** More material in less time — a denser cut. The duration matches the Parent audio (4689.557 s) to within 0.057 s, and `DAY2_PARENT_FORENSIC_AUDIT` independently records the −157.068 s relationship to the governed lock. **Three measurements agree.** `[E]`

---

# 4 · STABILITY

| dimension | finding | grade |
|---|---|---|
| **Sequence identity** | One sequence, one project, one event. Stable | `[E]` |
| **Spine identity** | 201 elements, no nested-spine leakage, parses cleanly | `[E]` |
| **Duration** | 4689.500 s, corroborated by the Parent audio and by the forensic audit | `[E]` |
| **Asset census** | 188 asset-clips vs 180 in the lock | `[E]` |
| **Connected census** | 455 vs 404 | `[E]` |
| **Transitions** | 24, excluded from the spine by contract — the same exclusion that produced the B-1 defect | `[E]` |
| **Gaps** | **5, against 3 in the governed lock** | `[O]` |

**The gap count is the one stability item worth the Executive's attention.** A `gap` in a spine is a structural hole — a span with no primary picture. The candidate has two more than the governed lock did. **This review does not interpret them.** Whether five gaps is consistent with *"no further cuts, trims, or re-orders"* is an editorial judgement, and gaps in FCP arise from deliberate structure as readily as from unfinished work. **It is flagged because a picture lock with more holes than its predecessor is a fact a Chairman should hold before declaring.** `[O]`

---

# 5 · LINEAGE — AND THE FINDING THAT MATTERS MOST

## 5.1 · No governed downstream artifact traces to this file

**Every governed artifact in the repository traces to the 08-22 lock, not to the candidate.** `[E]`

```
2bf06853…  (08-22 lock)      CAPTION_REGISTRY.yaml — 8+ per-entry source bindings
                              APPROVED_VIEWING_MASTER.yaml — fcpxml_sha256
                              → the governed registry chain

1ab3d12f…  (candidate)        INGESTION_MANIFEST.yaml        describes it
                              AR2-0824.context.json          declares it as the lineage source
                              APPROVED_VIEWING_MASTER.yaml   names it as the "divergent-cut FCPXML"
                              ECR_GEN_001_CONFORMANCE_REPORT describes it
                              CUSTODY_ALERT_001_Divergent_Cut raises it
                              EXECUTIVE_DECISION_BRIEF        compares it
                              EPR-001_VALIDATION_REPORT_PATH_B measures it
                              ENGINEERING_READINESS_REVIEW    cites it
```

**Eight references, and every one describes the candidate rather than deriving from it.** No registry entry, no timecode-bound artifact, no governed output has this file as its upstream.

**Lineage classification: `MISSING`, not broken.** Nothing points at it because nothing has been generated from it. That is the expected state for an undesignated source and it is *clean* — there is no half-built lineage to unwind.

## 5.2 · The repository already has two names for this file

This is the single most decision-relevant fact in the review.

| name used | where |
|---|---|
| **"analysis cut"** | `AR2-0824.context.json` → `analysis_cut/Info_analysiscut.fcpxml` · `ECR_GEN_001_CONFORMANCE_REPORT.md` |
| **"divergent cut"** | `APPROVED_VIEWING_MASTER.yaml` — *"the 2026-08-24 divergent-cut FCPXML"* · `docs/reviews/CUSTODY_ALERT_001_Divergent_Cut.md` |

**Neither name is dispositive.** `CUSTODY_ALERT_001` was raised on 2026-08-24 precisely because *"a second cut of Part 2 exists, and it is not the governed lock"* — and its Amendment records the Executive's own answer, `Q1_later_cut_exists: "no"`, followed by Path B and the designation of the 08-24 lineage as `PRODUCTION`.

**So the repository already resolved the question of whether this cut is legitimate. It has not resolved whether it is locked.** Those are different questions and the record keeps them apart. `[E]`

## 5.3 · What the repository actually defines as a Picture Lock

`SOP-06_Edit_Wrap_Publication_Gates.md`, the governing instrument:

> **Trigger.** *"The Chairman declares PICTURE LOCK: no further cuts, trims, or re-orders. Sound, music, VO, and graphics may still change; timing may not."*
>
> **Phase A1.** *"Fresh FCPXML export of the locked timeline → `XML/` (File > Export XML; name `P2_LOCK_<date>.fcpxml`)."*

**Two consequences, and the Executive should weigh both.**

**First: under the repository's own definition, a picture lock is an act, not a property of a file.** No FCPXML can satisfy the trigger by inspection, because the trigger is a declaration. Asked literally — *does this file satisfy the repository's existing definition* — the answer for **every** file in the repository is no, until declared. That is not evasion; it is what SOP-06 says.

**Second: the candidate does not match SOP-06 Phase A1's export convention.** It is not named `P2_LOCK_<date>.fcpxml` and it does not live in `XML/`. It is a project bundle in an analysis folder. **This does not disqualify it** — A1 describes what to export *after* the declaration, not what qualifies before it. **But it means declaring this file the lock and performing A1 are two different acts**, and A1 would produce a *different file* from a re-export.

---

# 6 · EXCLUSIVITY — IS THERE A COMPETING CANDIDATE?

**No structurally viable competitor exists.** `[E]`

Every FCPXML on the volume was censused:

| file | sha | seqs | duration | depth-0 | verdict |
|---|---|---|---|---|---|
| **candidate** | `1ab3d12f` | 1 | 4689.500 | 225 | the subject of this review |
| 08-22 governed lock | `2bf06853` | 1 | 4846.625 | 214 | **formally `SUPERSEDED_ASSEMBLY`** — cannot be the 08-24 lock |
| `Part 2 SRT .fcpxmld/Info.fcpxml` | `91488774` | 1 | 4848.125 | **1** | **not an edit** — a single asset-clip caption carrier |
| `XML retry/…/SRT PART 2.fcpxmld/Info.fcpxml` | `7f243ddc` | 1 | 4848.125 | **1** | **not an edit** — same class |
| `XML/P2_CHRONO_SETS.fcpxml` | `d7cd8600` | — | — | — | **no sequence, no spine** — a chrono-sets import, not a timeline |
| Jul 29 snapshot bundles | `f274a284`, `b0f5962d` | — | — | — | superseded by date; predate the Day 2 edit entirely |

**Two files carry only one depth-0 element each.** They are caption containers, not cuts. **One carries no sequence at all.** The only file in the repository that is both a complete Day 2 timeline and not already superseded is the candidate.

**The competing candidate is therefore the 08-22 lock, and it is not available** — `CUSTODY_ALERT_001` Amendment 1 records `08_22_assembly_lock_status: SUPERSEDED_ASSEMBLY`, ratified 2026-08-28. **The conflict is not resolved here and does not need to be: it was already resolved by the Order that created Path B.** `[E]`

---

# 7 · WHAT WOULD CHANGE THIS RECOMMENDATION

Stated so the Executive can see the recommendation's own failure conditions.

| condition | effect |
|---|---|
| A later Day 2 cut exists that has not been found | The candidate is superseded. `CUSTODY_ALERT_001` asked this and the recorded answer was `Q1_later_cut_exists: "no"` |
| The five gaps represent unfinished picture | Timing is not final; SOP-06's trigger cannot honestly be declared |
| A re-export under SOP-06 A1 is intended | The lock would be a **different file** with a **different hash**, and this review would be about the wrong artifact |

---

# 8 · RECOMMENDATION

**Structurally, the candidate is complete, unique, uncontested, and free of lineage debt.** It parses to exactly one sequence, produces a full census, matches the Parent audio and the forensic audit to within 0.057 s, and no governed artifact anywhere depends on it — so designating it starts a clean lineage rather than reconciling a tangled one. Every alternative is either superseded, not an edit, or not a timeline.

**Two things it is not.** It is not named a lock anywhere in the repository — it is named an *analysis cut* and a *divergent cut*. And under SOP-06 it cannot become one by inspection, because SOP-06 makes picture lock a declaration.

```
RECOMMENDED PICTURE LOCK
```

**Recommended on structural and lineage evidence only, and subject to three Executive facts this review cannot establish:** that no later Day 2 cut exists; that the five gaps are deliberate and the timing is final; and whether the designation is of *this file as it stands* or of a fresh SOP-06 A1 export, which would be a different artifact with a different hash.

**This is a recommendation. It is not a designation, and nothing in this review should be read as one.**

---

```
Candidate                  Alpha RoudUp Part 2.fcpxmld/Info.fcpxml
                           1ab3d12f0dd150c63907a4b2e4bac4253baf8100910dfda74daa3a5378b6b4d2
Path discrepancy           RECORDED — .fcpxmld bundle, "RoudUp" spelling
Identity                   one sequence, one project, one event
Completeness for ETC       COMPLETE except declared_lock, which no FCPXML carries
Stability                  stable; 5 gaps vs 3 flagged, not interpreted
Lineage                    MISSING, not broken — no governed artifact derives from it
Exclusivity                UNCONTESTED — no other viable candidate exists
ETC written for 08-24      NONE — ED-001A §3/§6 observed
Determinations made        NONE
```

---

*Prepared under PLR-001. Custody: MACHINE. Authority: NONE. No repository file, registry, generator, artifact or source file was modified. No commit was made. No Executive determination was made, inferred, substituted or defaulted.*
