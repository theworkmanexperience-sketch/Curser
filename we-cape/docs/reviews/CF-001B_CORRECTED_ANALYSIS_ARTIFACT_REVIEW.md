# CF-001B — CORRECTED ANALYSIS ARTIFACT REVIEW

**Issued under:** `CF-001` Re-examination Directive, Executive Producer / Chairman, 2026-08-30
**Designation:** `CF-001B` — **recommended, not assigned**
**Prepared by:** Governance Compliance Auditor · **Custody:** `MACHINE` · **Authority:** NONE
**Class:** **engineering evidence review** — no governance determination
**Mode:** READ-ONLY. Nothing modified, created, renamed or committed.
**Measured:** volume `WE_CAPE_OUTPUT` as mounted 2026-08-30 23:2x · repository `2b7f055`

> **Independence.** Every figure below was re-measured from the artifacts as they stand now. **No conclusion from `CF-001` or `CF-001A` is carried forward.** Two of `CF-001A`'s three grounds for rejection do not survive re-measurement, and §9 states plainly why.

---

# 0 · RECOMMENDATION

```
        A C C E P T   F O R   E X E C U T I V E   R E V I E W
        as analysis artifacts, with three stated limitations
```

**Under the purpose the Directive states — timestamp extraction, analytical indexing, machine-assisted evidence collection, timing reference — the corrected artifacts are fit.** `[E]`

| limitation | measurement |
|---|---|
| **L-1** The SRT omits 26 % of the project's caption events | 2,219 of 3,003 caption instances represented; **784 not** |
| **L-2** Duplicate caption events persist | 33 adjacent runs, 35 redundant cues — **originating in the source project, not the export** |
| **L-3** Two editorial changes are present and unexplained | +4 `asset-clip` elements; 1 title text rewritten |

**None of the three is a defect of the export. All three are properties of the project or of the SRT format.**

---

# 1 · THE ARTIFACT SET AS IT NOW STANDS

`…/ALPHA ROUNDUP DAY 2 ANALYSIS/Corrected Video Analysis Files/`

| file | sha256[:16] | bytes | modified |
|---|---|---|---|
| `Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` | `d82c2c3ec0f788cf` | 7,264,164 | 21:42 |
| `Alpha RoudUp Part 2.mov` | `ff34278fe1f47f67` | **29,321,383,259** | 22:27 |
| `Alpha RoudUp Part 2_SRT_English (United States).srt` | `d93d86a1b7cd99c9` | 184,470 | 22:01 |
| `Alpha RoudUp Part 2_analysis_NC_-custom-1.mov` | `b561852803f7ffe6` | 539,575,045 | 18:09 |

## 1.1 · What changed since the earlier measurement `[E]`

| | before | now |
|---|---|---|
| empty `.vob` (0 bytes) | present | **removed** |
| FCPXML bundle | `Alpha RoudUp Part 3.fcpxmld` | `Alpha RoudUp Part 2.fcpxmld` |
| FCPXML hash | `a99f3c8f1a78da33` · 7,264,237 B | **`d82c2c3ec0f788cf` · 7,264,164 B** (−73 B) |
| FCPXML internal project name | `name="Alpha RoudUp Part 3"` | **`name="Alpha RoudUp Part 2"`** |
| `Alpha RoudUp Part 2.mov` | absent | **present, 29.3 GB** |
| SRT bytes | `d93d86a1b7cd99c9` | **`d93d86a1b7cd99c9` — unchanged** |

**The FCPXML was renamed at source and re-exported, not merely renamed on disk.** Its element census is **identical** to the prior export — the 73-byte reduction accompanies the project-name change and no structural change. `[E]`

**The naming discrepancy is fully resolved.** Bundle filename, internal project name and SRT stem now all read `Alpha RoudUp Part 2`, and the media files agree. **No inconsistency remains at any level.** `[E]`

---

# 2 · QUESTION 1 — DOES THE SRT REPRESENT THE FCPXML TIMELINE?

## 2.1 · The FCPXML carries its own captions, on five lanes `[E]`

```
<caption> elements          3,003        all role="SRT?captionFormat=SRT.en-US"
distinct caption texts      2,410

lane 1   2,397      lane 2     433      lane 3   159
lane 4      13      lane 5       1
```

**This is the decisive structural fact of the review, and it was not previously measured.** The corrected FCPXML is not a picture timeline that happens to have an SRT beside it — **it carries a five-lane caption structure natively.**

## 2.2 · The SRT is faithful and incomplete `[E]`

```
SRT cues                    2,034        distinct texts   1,679

SRT texts present in FCPXML       1,679 of 1,679     100.00 %
SRT texts ABSENT from FCPXML          0
FCPXML texts absent from the SRT    731 distinct
caption INSTANCES represented     2,219 of 3,003      73.9 %
caption INSTANCES omitted           784               26.1 %
```

**Per-lane coverage of distinct texts:**

| lane | captions | distinct | in SRT | coverage |
|---|---|---|---|---|
| 1 | 2,397 | 1,964 | 1,679 | **85.5 %** |
| 2 | 433 | 392 | 51 | **13.0 %** |
| 3 | 159 | 152 | 30 | **19.7 %** |
| 4 | 13 | 13 | 3 | **23.1 %** |
| 5 | 1 | 1 | 0 | **0 %** |

> **Answer to Question 1: NO — not accurately, in the sense of completeness. YES — accurately, in the sense of fidelity.**
>
> **The SRT invents nothing: every one of its 1,679 distinct texts exists verbatim in the FCPXML.** `[E]`
> **The SRT omits a quarter of the project's caption events, including 285 distinct lane-1 texts and almost the whole of lanes 2–5.** `[E]`

**This is a format consequence, not an error.** SRT is single-track; the project's captions are five-lane and overlapping. **A flat SRT cannot represent overlapping captions, so any export must drop or merge them.**

---

# 3 · QUESTION 2 — DOES THE FCPXML PRESERVE THIS ANALYSIS PROJECT'S TIMELINE?

**Measured against the analysis-cut project `1ab3d12f`, which is this project's own predecessor.** `[E]`

| | Corrected `d82c2c3e` | Analysis cut `1ab3d12f` | Δ |
|---|---|---|---|
| `<sequence duration>` | `225096000/48000s` = **4689.500 s** | `225096000/48000s` = **4689.500 s** | **0 — identical to the sample** |
| `tcFormat` · `format` · `tcStart` | `NDF` · `r1` · `0s` | `NDF` · `r1` · `0s` | identical |
| `asset-clip` | 537 | 533 | **+4** |
| `clip` | 62 | 62 | 0 |
| `gap` | 36 | 36 | 0 |
| `title` | 65 | 65 | 0 |
| `transition` | 178 | 178 | 0 |
| `spine` | 115 | 115 | 0 |

> **Answer to Question 2: YES, substantially.** Duration, timecode base, clip count, gaps, transitions, nested spines and title count are all preserved exactly. **Two deliberate-looking changes are present and are identified in full below.**

## 3.1 · The four added `asset-clip` elements — all one source `[E]`

```
"Map traavel to Smyrna Event Center-45"      1  →  3      (+2)
"Map traavel to Smyrna Event Center-47"      0  →  1      (+1)
"Map traavel to Smyrna Event Center-48"      0  →  1      (+1)
```

**All four are map/travel B-roll from a single named source.** **No other asset-clip changed.** The sequence duration did not change, so these were placed within existing time rather than extending the timeline. `[E]`

## 3.2 · One title text was rewritten `[E]`

```
analysis cut   "Day 2: Part 1  - Lower Third Text & Subhead"
corrected      "Day 2: 3 Part Series - Lower Third Text & Subhead"
```

**This is on-screen title text, not a caption.** It is the only title difference of the 65.

---

# 4 · QUESTION 3 — DO DUPLICATED CAPTION EVENTS STILL EXIST?

**Yes. Measured on both sides, and the mechanism is now identified.** `[E]`

```
SRT      adjacent duplicate runs   33      cues involved   68      redundant   35
FCPXML   caption instances      3,003      distinct     2,410      redundant  593
```

## 4.1 · Two different phenomena, held apart

**Global text repetition is not a defect.** The most repeated FCPXML caption texts are `"All right."` ×67, `"Okay."` ×26, `"Nice."` ×23, `"Why do you ride?"` ×22. **Across a 78-minute film with dozens of speakers these are ordinary speech, and counting them as duplicates would be an error.** The defect-relevant metric is **adjacent identical cues**, and that is what the 33 runs measure. `[E]`

## 4.2 · Mechanism — roughly half are lane flattening `[E]`

**For each of the 33 SRT duplicate runs, the FCPXML was queried for the lanes carrying that text:**

```
runs whose text appears on MORE THAN ONE lane     16 of 33
runs whose text appears on one lane only          17 of 33
```

| SRT run | ×N | FCPXML instances | lanes |
|---|---|---|---|
| `#103–#104` `"I like that."` | 2 | 9 | **lane 1 ×8, lane 2 ×1** |
| `#367–#368` `"How you doing?"` | 2 | 16 | **lanes 1, 2, 3, 4** |
| `#666–#667` `"There you go."` | 2 | 11 | **lane 3 ×1, lane 1 ×10** |
| `#93–#94` `"KC?"` | 2 | 2 | lane 1 only |
| `#229–#230` `"I love that."` | 2 | 13 | lane 1 only |

> **Answer to Question 3: YES, duplicates persist — and they are not introduced by the export.**
>
> **16 of 33 are consistent with flattening a multi-lane caption structure into a single track.** `[P]`
> **17 of 33 exist as adjacent repeats within lane 1 of the source project itself.** `[E]`
>
> **The correction pass did not fail to remove duplicates. The duplicates are in the project.**

---

# 5 · QUESTION 4 — WAS DIALOGUE ALTERED, REMOVED, MERGED OR REWRITTEN?

**The answer depends entirely on what the SRT is measured against, and both measurements are reported.**

## 5.1 · By the export, against its own FCPXML — **NO** `[E]`

```
SRT texts present verbatim in the FCPXML      1,679 of 1,679     100.00 %
SRT texts not found in the FCPXML                  0
```

**The export altered nothing, invented nothing and rewrote nothing.** Every line it carries exists in the project.

## 5.2 · By the project, against the earlier analysis-cut export — **YES, six changes** `[E]`

**Direct test: are the changed texts in this FCPXML, and are the originals?**

| text | in corrected FCPXML |
|---|---|
| `uh, wonderful and warm and what we **make** community.` | **IN** |
| `vice mayor, Mark Atkins**,** and Todd Skimmer, and we` | **IN** |
| `and then Shannon LaCase**,** Shannon, where are you?` | **IN** |
| `**Run**ford County schools, helping 100 students per` | **IN** |
| `uh, wonderful and warm and what we **made** community.` *(original)* | **NOT** |
| `**Rut**ford County schools, helping 100 students per` *(original)* | **NOT** |
| `Hey, David.` *(original)* | **NOT** |

> **The edits were made inside the Final Cut project. The SRT export reports them faithfully.** `[E]`
>
> **`CF-001A` attributed these six changes to the correction pass. That attribution was wrong** — it compared two sibling SRT exports and inferred an export defect. **The measurement above locates them in the project, where they are an editorial act.**

**The `"Hey, David."` line remains absent from this project's captions, and `Rutford` → `Runford` remains a proper-noun change.** **Both are real; neither is an export failure.** Whether either is an improvement is an editorial judgment on audio and **is not made here.** `[O]`

---

# 6 · QUESTION 5 — SUITABILITY AS ANALYSIS ARTIFACTS

**Assessed only against the purpose the Directive states, and independent of any canonical determination.**

| purpose | FCPXML `d82c2c3e` | SRT `d93d86a1` |
|---|---|---|
| **timestamp extraction** | **SUITABLE** — complete, 3,003 events, five lanes, native offsets | **SUITABLE WITH LOSS** — 2,034 flat cues, 26 % of events absent |
| **analytical indexing** | **SUITABLE** | **SUITABLE WITH A RECALL GAP** — an index built on it will silently miss 784 caption events |
| **machine-assisted evidence collection** | **SUITABLE** | **SUITABLE** — 100 % precision; nothing it returns is invented |
| **timing reference points** | **SUITABLE** | **SUITABLE** — internally consistent, §6.1 |

## 6.1 · SRT internal quality — clean `[E]`

```
zero-length cues        0        non-positive durations   0
out-of-order cues       0        overlapping cues         0
index sequence          1 … 2,034 contiguous
last cue end            4688.958 s   ·   sequence 4689.500 s   — fits
```

> **Answer to Question 5: YES, suitable as analysis artifacts, with `L-1` stated.**
>
> **The FCPXML is the better analysis artifact and should be preferred wherever completeness matters. The SRT is a faithful but lossy convenience view of it, and anything built on the SRT alone is working from 73.9 % of the project's caption events.**

---

# 7 · QUESTION 6 — EVIDENCE, OBSERVATION, IMPLICATION

## 7.1 · Engineering evidence `[E]`

- FCPXML: 4689.500 s, identical to its predecessor; +4 `asset-clip`; all other structure unchanged.
- FCPXML carries 3,003 captions on 5 lanes; 2,410 distinct; 593 redundant instances.
- SRT: 2,034 cues, 1,679 distinct, **100 % contained in the FCPXML, 0 inventions**.
- SRT omits 784 caption instances (26.1 %), including 285 distinct lane-1 texts and 92 % of lanes 2–5.
- SRT internal quality: 0 zero-length, 0 non-positive, 0 out-of-order, 0 overlapping, contiguous indices.
- 33 adjacent duplicate runs; 16 involve text present on more than one lane.
- Naming is consistent at every level; the empty `.vob` is gone; a 29.3 GB master export is now present.

## 7.2 · Editorial observations — reported, not judged `[O]`

- Four map/travel clips were added to the analysis timeline without changing its duration.
- One lower-third title was rewritten from *"Day 2: Part 1"* to *"Day 2: 3 Part Series"*.
- Six caption texts differ from the earlier analysis-cut export, including one utterance now absent and one proper-noun spelling changed.
- **Whether any of these is correct is an editorial judgment on picture and audio. None is made here.**

## 7.3 · Governance implications — stated, not exercised `[O]`

- **None of this bears on `CF-001`.** These artifacts are not a candidate for the governed caption stream, and the Directive says so. **`CF-001` remains `UNRESOLVED`.**
- **No canonical status is created or implied.** `ED-003`, `ED-004`, `ED-005` are untouched.
- **These artifacts are in no registry and cited by no committed document** — `git grep` at `2b7f055` returns 0 hits for every filename and for the folder name. **They carry no repository authority and this review confers none.**
- **One structural point worth the Executive's notice, offered as observation:** the corrected FCPXML is the first artifact in this program to carry its captions natively on five lanes. **Any future caption work that consumes an SRT of it will be working from a flattened 74 % view.** That is a property of the format, and it is the sort of thing that becomes invisible once a downstream artifact is built.

---

# 8 · ASSUMPTIONS AFFECTING THE RECOMMENDATION

| # | assumption | effect if wrong |
|---|---|---|
| **A-1** | The analysis cut `1ab3d12f` is the correct baseline for *"the intended editorial timeline of this analysis project."* | If a different baseline is intended, §3 must be re-measured against it. **The Directive does not name a baseline; this one was chosen because the corrected project's duration matches it to the sample.** `[P]` |
| **A-2** | The four added clips and the retitled lower third are **intended** editorial changes. | If unintended, they are regressions and the recommendation becomes `MORE EVIDENCE REQUIRED`. **Intent is not measurable from the artifacts.** `[O]` |
| **A-3** | Caption correspondence was measured **by text**, not by resolved timeline. | FCPXML caption offsets are local to their parent element — the maximum observed offset is 70,666 s against a 4,689 s sequence — so timeline resolution requires the `fcpx_resolve` logic. **A resolved comparison could reveal position mismatches this text-level test cannot see.** `[O]` |

---

# 9 · WHERE THIS REVIEW CONTRADICTS `CF-001A`

**Reported as the Directive requires — the new measurements stand, the earlier conclusions do not.**

| `CF-001A` ground for `REJECT` | status after re-measurement |
|---|---|
| **1 · Duplicates were not eliminated** — 33 runs / 35 cues | **Measurement confirmed. Interpretation withdrawn.** The duplicates are in the source project — 16 of 33 attributable to multi-lane flattening. **The export did not fail to remove them; they were never the export's to remove.** |
| **2 · The timeline is the analysis cut, not the picture lock** | **Withdrawn.** `CF-001A` measured against the picture lock because the earlier Directive framed the comparison as *"Original Picture Lock → Corrected Picture Lock."* **Under the correct frame — an analysis artifact judged against its own analysis project — the timeline is preserved exactly.** |
| **3 · Spoken content changed in six places** | **Measurement confirmed. Attribution corrected.** The changes are in the Final Cut project, not the export: all four changed texts are in the FCPXML and all three originals are absent. **The export is 100 % faithful.** |
| *(also)* empty `.vob`; Part 2 / Part 3 naming split | **Both resolved.** The `.vob` is gone; naming is consistent at bundle, project and SRT level. |

**`CF-001A`'s recommendation of `REJECT` does not survive.** **Its second ground was an artifact of the frame it was given, and I inherited that frame without challenging it. That was my error, and the correction is recorded here rather than folded away.**

---

# 10 · CONSTRAINTS OBSERVED

**Nothing was modified, created, renamed, moved or committed. No canonical status was designated. `CF-001` was not resolved. `ED-003`, `ED-004` and `ED-005` were not determined. No governance was inferred and no repository authority asserted.**

---

```
CF-001B — CORRECTED ANALYSIS ARTIFACT REVIEW          ENGINEERING EVIDENCE

FCPXML          d82c2c3e   4689.500 s   captions 3,003 / 5 lanes / 2,410 distinct
SRT             d93d86a1   2,034 cues   1,679 distinct
Fidelity        100.00 % of SRT texts present in FCPXML   ·   0 inventions
Completeness    2,219 of 3,003 caption instances   ·   784 omitted (26.1 %)

Timeline vs analysis project      duration Δ 0   ·   +4 asset-clip   ·   1 title retitled
Duplicates                        33 adjacent runs   ·   16 multi-lane   ·   source-side
Dialogue altered by the export    NONE
Dialogue altered in the project   6 instances   ·   editorial, not judged
SRT internal quality              0 / 0 / 0 / 0   ·   indices contiguous

RECOMMENDATION    ACCEPT FOR EXECUTIVE REVIEW  —  analysis artifacts, L-1..L-3 stated

CF-001A grounds   1 reinterpreted   ·   1 withdrawn   ·   1 re-attributed
Determination     NONE       Files modified   NONE       Commits   NONE
```

---

*Prepared under the `CF-001` Re-examination Directive. Custody: `MACHINE`. Authority: NONE. This is an engineering evidence review of analysis artifacts. No governance determination was made, no artifact designated canonical, no caption stream declared authoritative, nothing modified, and no commit created.*
