# CF-001A — CORRECTED CAPTION REPRESENTATION REVIEW

**Issued under:** CLAUDE REVIEW DIRECTIVE `CF-001A`, Executive Producer / Chairman, 2026-08-30
**Prepared by:** Governance Compliance Auditor · **Custody:** `MACHINE` · **Authority:** NONE
**Class:** **engineering evidence review — not a governance determination**
**Mode:** READ-ONLY. Nothing modified, nothing created, nothing committed.
**Measured:** volume `WE_CAPE_OUTPUT` as mounted 2026-08-30 · repository `2b7f055`

> **Attribution correction, first.** The Directive credits me with naming the `Corrected Video Analysis Files` folder. **I did not create it, did not name it, and have written nothing to `WE_CAPE_OUTPUT` at any point in this engagement.** Every action on that volume has been read-only. The folder and its contents are someone else's work. **The provenance discipline it reflects is real and is not mine to accept credit for.**

---

# 0 · RECOMMENDATION

```
                          R E J E C T
```

**The two objectives set by the Directive are both measurable, and both fail on measurement.** `[E]`

| objective | result |
|---|---|
| *"produce a normalized caption representation"* | **NOT ACHIEVED.** 33 duplicate runs / 35 duplicate cues remain — **identical to the source stream, cue for cue** |
| *"while preserving the editorial timeline"* | **NOT ACHIEVED against the picture lock.** The corrected artifacts carry the **analysis-cut** timeline, 4689.500 s — **157.125 s shorter** than the picture lock's 4846.625 s |

**This is `REJECT` rather than `MORE EVIDENCE REQUIRED` because nothing here is undetermined.** The duplicate census is a direct count and it is unchanged from the input. The sequence duration is a declared field and it is a different timeline. **More evidence would not move either number.**

**Three findings would each independently have forced this recommendation.** They are at §7.

---

# 1 · THE ARTIFACTS AS FOUND

`WE_CAPE_OUTPUT/AlphaRoundUp_2026/Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2 ANALYSIS/Corrected Video Analysis Files/`

| file | sha256[:16] | bytes | modified |
|---|---|---|---|
| `Alpha RoudUp Part 3.fcpxmld/Info.fcpxml` | `a99f3c8f1a78da33` | 7,264,237 | 2026-08-30 16:49 |
| `Alpha RoudUp Part 2_analysis_NC_-custom-1.mov` | `b561852803f7ffe6` | 539,575,045 | 2026-08-30 18:09 |
| `Alpha RoudUp Part 3_SRT_English (United States).srt` | `d93d86a1b7cd99c9` | 184,470 | 2026-08-30 19:22 |
| `Alpha RoudUp Part 2_analysis_NC_-custom-1-custom-1.vob` | `e3b0c44298fc1c14` | **0** | 2026-08-30 20:13 |

## 1.1 · Two discrepancies recorded, not normalized

**Per the standing instruction from `PLR-001` — *record the discrepancy, do not normalize or assume*.**

**`D-1` · The `.vob` is empty.** Zero bytes. `e3b0c44298fc1c14` is the SHA-256 of the empty string. **It is the newest file in the folder (20:13), and it carries no data.** Whatever produced it did not write output. `[E]`

**`D-2` · Part 2 / Part 3 naming — RENAME APPLIED BY THE EXECUTIVE, REVIEWED AT §1.2.** As first measured, the FCPXML bundle and the SRT were both `Alpha RoudUp Part 3…`, while the `.mov` and `.vob` were `Part 2`. **The SRT has since been renamed to `Alpha RoudUp Part 2_SRT_English (United States).srt`.** `[E]`

**The rename was executed correctly and the review of it follows at §1.2. It changes no measurement in this document** — hashes, cue counts, duplicate census, sequence duration and content deltas are properties of the bytes. **None of the three grounds for rejection at §7 turns on a filename.** `[E]`

---

## 1.2 · NAMING CONVENTION REVIEW — the rename

**Requested by the Executive. Measured after the rename.**

### The rename preserved the artifact exactly `[E]`

```
before   Alpha RoudUp Part 3_SRT_English (United States).srt
after    Alpha RoudUp Part 2_SRT_English (United States).srt

sha256   d93d86a1b7cd99c9…   UNCHANGED
bytes    184,470             UNCHANGED
mtime    2026-08-30 19:22    UNCHANGED
```

**A rename that alters no content is the correct execution of a rename.** No re-export, no re-save, no round-trip through an editor. **Verified, and it is the part that most often goes wrong.**

### `[F-1]` · The `Part 3` label originates inside Final Cut Pro, not in the filesystem `[E]`

The FCPXML's own declared project name is:

```xml
name="Alpha RoudUp Part 3"
```

**`Part 3` is what the FCP project calls itself**, inside `AlphaRoundUp_2026.fcpbundle`. It is not a filename typo applied at export. **Renaming the `.fcpxmld` bundle would therefore not make the artifact say `Part 2` — it would create a bundle whose filename and whose internal project name disagree.**

### `[F-2]` · The rename broke the SRT ↔ FCPXML stem pairing `[E]`

**The governed convention on this volume pairs an SRT to its project by shared filename stem.** The picture-lock pair demonstrates it:

```
Final Data Source Files/
  Alpha RoudUp Part 2.fcpxmld
  Alpha RoudUp Part 2_SRT__SRT 2_English (United States).srt      ← same stem
```

**That shared stem is the mechanism by which the `CF-001` evidence review established which caption stream came from which editorial timeline.** It is not cosmetic; it is the provenance link.

| | SRT | FCPXML bundle | FCPXML internal name | paired? |
|---|---|---|---|---|
| **before rename** | `Part 3` | `Part 3` | `Part 3` | **YES** — and inconsistent only with the media filenames |
| **after rename** | **`Part 2`** | `Part 3` | `Part 3` | **NO** |

**Before the rename, the SRT and its project agreed and the media filenames were the outlier. After it, the SRT agrees with the media and no longer agrees with the project that produced it.** `[E]`

**The rename optimized for consistency with the `.mov` and `.vob`, at the cost of the one relationship that carries lineage.**

### `[F-3]` · The content is Part 2 material `[E]`

**This is not in doubt and it is why the rename is defensible on substance.** The corrected FCPXML's sequence duration `225096000/48000s` = 4689.500 s is identical to the **Part 2 analysis cut** `1ab3d12f`, and the SRT is a 2-cue derivative of the Part 2 analysis-cut SRT `2a16dd70`. **The material is Part 2. The project that exported it is named Part 3.**

### Dispositions — recommended, not assigned `[O]`

| # | option | consequence |
|---|---|---|
| **1** | Rename the `.fcpxmld` bundle to `Part 2` as well | Restores the stem pairing. **Bundle filename would then disagree with the project's internal `name="Alpha RoudUp Part 3"`** — one inconsistency traded for another, and the internal name is the one a parser reads |
| **2** | Rename the project inside Final Cut Pro and re-export | **The only option producing agreement at every level.** Requires a re-export — editorial work, not authorized, and it would produce new hashes requiring re-measurement |
| **3** | Revert the SRT to `Part 3` and treat the media filenames as the outlier | Restores the pairing at once, costs nothing, and records the `Part 3` project name as the fact it is |
| **4** | Leave as-is and record the split | **Not recommended.** An SRT whose stem matches no project is the condition that made `CF-001` possible |

**Option 2 is the only one that removes the discrepancy rather than relocating it.** **Option 3 is the only one available without a re-export.** **The choice is the Executive's; I record the trade and do not make it.**

### Nothing downstream is broken by the rename `[E]`

**No committed artifact references either filename.** `git grep` for both stems across `2b7f055` returns nothing: these artifacts are dated 2026-08-30, are in no registry, and are cited by no governed document. **The rename creates no dangling reference.**

---

# 2 · QUESTION 1 — TIMELINE INTEGRITY

**The corrected FCPXML must be compared against the right predecessor, and the evidence identifies which one.**

| artifact | `<sequence duration>` | seconds |
|---|---|---|
| **Corrected** `a99f3c8f` | `225096000/48000s` | **4689.500** |
| Analysis cut `1ab3d12f` | `225096000/48000s` | **4689.500** |
| **Picture lock** `2bf06853` | `232638000/48000s` | **4846.625** |

> **The corrected FCPXML's sequence duration is identical to the analysis cut's, to the sample. It is 157.125 s shorter than the picture lock's.** `[E]`

**The corrected artifacts are a derivative of the analysis cut, not of the picture lock.** The Directive frames the comparison as *Original Picture Lock → Corrected Picture Lock*; **the evidence does not support that framing.**

## 2.1 · Structural comparison

| element | Corrected `a99f3c8f` | Analysis cut `1ab3d12f` | Δ | Picture lock `2bf06853` | Δ |
|---|---|---|---|---|---|
| `asset-clip` | 537 | 533 | **+4** | 478 | **+59** |
| `clip` | 62 | 62 | 0 | 61 | +1 |
| `gap` | 36 | 36 | 0 | 33 | +3 |
| `title` | 65 | 65 | 0 | 57 | **+8** |
| `transition` | 178 | 178 | 0 | 180 | −2 |
| `spine` | 115 | 115 | 0 | 110 | +5 |

**Against the analysis cut:** everything matches except **four additional `asset-clip` elements.** Duration, titles, gaps, transitions and nested spines are unchanged. `[E]`

**Against the picture lock:** +59 asset-clips, +8 titles, +3 gaps, −2 transitions, +5 spines, and a 157-second-shorter sequence. **Those are picture-edit differences, not caption-representation differences.** `[E]`

## 2.2 · Verdict on the four sub-questions

| | vs analysis cut | vs picture lock |
|---|---|---|
| picture edit unchanged | **NO** — +4 `asset-clip` | **NO** — +59 `asset-clip`, +8 `title` |
| sequence duration unchanged | **YES** — identical to the sample | **NO** — −157.125 s |
| clip ordering unchanged | **YES** — element counts and order preserved | **NO** — different element population |
| editorial timing unchanged | **YES** — §4.2, median delta 0.000 s | **NO** |

**Deviation reported, as required: the corrected artifacts do not preserve the picture-lock editorial timeline. They preserve the analysis-cut timeline, with four added asset-clips.**

---

# 3 · QUESTION 2 — CAPTION NORMALIZATION · **THE DECISIVE FAILURE**

**Full structural census of all four streams, computed identically.** `[E]`

| stream | cues | **dup runs** | **dup cues** | zero-length | non-positive | out-of-order | overlapping | index seq | last cue end |
|---|---|---|---|---|---|---|---|---|---|
| **Corrected `d93d86a1`** | **2,034** | **33** | **35** | 0 | 0 | 0 | 0 | ✓ | 4688.958 |
| Analysis cut `2a16dd70` | 2,036 | **33** | **35** | 0 | 0 | 0 | 0 | ✓ | 4688.958 |
| `c13df1f4` | 2,290 | 39 | 41 | 0 | 0 | 0 | 0 | ✓ | 4840.833 |
| GT-2 `89d61f96` | 2,291 | 41 | 44 | 0 | 0 | 0 | 0 | ✓ | 4841.208 |

> ## **The corrected stream carries exactly the same duplicate profile as its source: 33 runs, 35 cues. Not one duplicate run was eliminated.** `[E]`

**Duplicate runs still present in the corrected stream — first six of thirty-three:**

```
#93–#94     x2   "KC?"                [273.000 .. 274.250]
#103–#104   x2   "I like that."       [283.750 .. 284.625]
#117–#118   x2   "Love that."         [308.958 .. 309.833]
#229–#230   x2   "I love that."       [477.083 .. 478.083]
#353–#354   x2   "This is nice."      [654.083 .. 654.958]
#367–#368   x2   "How you doing?"     [670.333 .. 671.458]
```

**These are the doubled-run pattern `CCR-001` and `CIA-001` examined. They survive the correction unchanged.**

## 3.1 · Verdict on the four sub-questions

| | result |
|---|---|
| duplicated caption runs eliminated | **NO** — 33 runs / 35 cues, identical to source |
| one spoken utterance maps to one caption | **NO** — 35 cues remain in multi-cue runs |
| cue ordering deterministic | **YES** — indices `1…2034` strictly sequential, 0 out-of-order, 0 overlapping |
| cue timing internally consistent | **YES** — 0 zero-length, 0 non-positive durations |

**Two of four pass. The two that fail are the two the correction exists to achieve.**

---

# 4 · QUESTIONS 3 & 4 — FCPXML AND SRT COMPARISON

## 4.1 · FCPXML

**Caption-representation differences:** none detectable at the structural level. **`title` count is identical to the analysis cut (65) and the corrected FCPXML carries no caption element the analysis cut lacks.** `[E]`

**Metadata differences:** `tcFormat="NDF"` and `format="r1"` identical across all three. `[E]`

**Structural differences:** **four additional `asset-clip` elements** against the analysis cut. **This is the one structural change, and it is not a caption change.** Per the Directive I do not treat caption normalization as an editorial change — **but four added asset-clips are not caption normalization**, and they are reported as a structural deviation of unknown purpose. `[O]`

## 4.2 · SRT — corrected against its source

```
cue count            2,036 → 2,034      (−2)
text similarity      0.9961             (sequence-level, 2,034 vs 2,036 lines)
timing deltas        n = 2,027 matched cues
                     median  0.000 s    ·   max  0.000 s
                     min    −0.042 s    ·   non-zero  3 of 2,027
```

**Timing is preserved.** Three cues shift by at most 42 ms; every other matched cue is identical to the millisecond. `[E]`

**Ordering is preserved.** Indices renumber contiguously `1…2034`; no reordering, no gaps. `[E]`

---

# 5 · QUESTION 5 — EDITORIAL FIDELITY · **SPOKEN CONTENT CHANGED**

> **The Directive requires: if content changed, identify every instance. It changed. All six are below.** `[E]`

| # | analysis cut | corrected | class |
|---|---|---|---|
| **1** | `uh, wonderful and warm and what we made community.` | `uh, wonderful and warm and what we make community.` | **word changed** — *made* → *make* |
| **2** | `vice mayor, Mark Atkins and Todd Skimmer, and we` | `vice mayor, Mark Atkins, and Todd Skimmer, and we` | punctuation added |
| **3** | `and then Shannon LaCase.` **+** `Shannon, where are you?` | `and then Shannon LaCase, Shannon, where are you?` | **two cues merged into one** |
| **4** | `a, tell us a little about what it is and how impactful,` **+** `um, how we then is going to be for this town.` | `a, tell us a little about what it is and how impactful` **+** `how we then is going to be for this town.` | **`um,` deleted**; comma dropped |
| **5** | `ride with us today, our town manager, David.` **+** `Hey, David.` | `ride with us today, our town manager, David?` | **`"Hey, David."` DELETED**; `.` → `?` |
| **6** | `Rutford County schools, helping 100 students per` | `Runford County schools, helping 100 students per` | **proper noun changed** — *Rutford* → *Runford* |

**Answer to Question 5: YES. Spoken content changed, in six instances.** `[E]`

**Two warrant particular attention, and I classify neither as improvement or corruption — that is an editorial judgment on audio I cannot make.** `[O]`

- **`#5` is a deletion.** The utterance `"Hey, David."` exists in the source and does not exist in the corrected stream. **It is not merged into a neighbour — the neighbouring cue's text is unchanged apart from its final punctuation.** One spoken line is gone.
- **`#6` changes a proper noun.** *Rutford County* → *Runford County*. **A place name is a governed fact class**; whichever spelling is right, the correction pass altered one without a recorded basis.

**Three of the six (#2, #4, #5) alter punctuation in ways that change sentence force** — `David.` becomes `David?`. **Under `WET-SPEC-DIE-001` rule X-2, cited by `CAPTION_REGISTRY` as *"No caption text was corrected, normalised or re-spaced: verbatim extraction"*, these are exactly the class of change verbatim extraction forbids.** `[E]`

---

# 6 · QUESTION 6 — MACHINE READINESS

**Assessed as candidacy only. Nothing is designated canonical.**

| consumer | suitable? | reason |
|---|---|---|
| **Editorial Timing Contract generation** | **NO** | `PDR-2026-08-20-ETC-001` derives the ETC from the **picture-locked** FCPXML. This FCPXML is the analysis cut — 4689.500 s against the lock's 4846.625 s. **An ETC generated here would describe a different film.** |
| **Citation indexing** | **NO** | 2,034 cues against the 2,290 the 91 governed citations index. **Every citation index would resolve — and resolve wrongly.** This is the exact `CF-001` mechanism, reproduced on a third stream. |
| **ESS generation** | **NO** | `gen_artifacts.py` binds `LOCK=4846.625` and GT-2 `89d61f96`. Neither matches. |
| **Generator inputs** | **NO** | `GE-1`/`GE-2` remain: the generator is hard-coded to the lock assembly. Supplying analysis-cut inputs would produce artifacts on an ungoverned timebase. |

**One qualified positive, recorded because the Directive asks for candidacy and not only for rejection.** **As a *caption-cleanliness* candidate the corrected stream is internally sound** — 0 zero-length cues, 0 non-positive durations, 0 out-of-order cues, 0 overlaps, contiguous indices, timing preserved to a 42 ms maximum deviation. **Its defects are that it did not remove the duplicates it exists to remove, that it altered content, and that it is bound to the wrong timeline.** `[E]`

---

# 7 · THE THREE INDEPENDENT GROUNDS FOR REJECTION

**Any one of these alone would be sufficient.**

1. **Duplicates were not eliminated.** 33 runs / 35 cues, byte-for-byte the same population as the input. **The stated purpose of the artifact is unachieved and the measurement is a direct count.**
2. **The timeline is the analysis cut, not the picture lock.** 4689.500 s against 4846.625 s. **157.125 seconds of the governed film are absent.**
3. **Spoken content changed in six places, including one outright deletion**, against a specification that requires verbatim extraction.

**And one process observation, outside the three:** the correction was applied to a stream in the **`c13df1f4` / analysis-cut lineage** — the family `CF-001` identified as having **no custody record and no governed FCPXML pairing**. **A correction pass on the unregistered lineage produces a fourth unregistered stream.** `[E]`

---

# 8 · WHAT WOULD CHANGE THIS RECOMMENDATION

**Stated so the rejection is actionable rather than terminal.**

- A corrected stream derived from the **picture lock** `2bf06853` at **4846.625 s**;
- with the **duplicate run count reduced** and the reduction enumerable against a stated rule;
- with **zero content changes** — no deletions, no word substitutions, no punctuation edits — or, if changes are intended, an **explicit, Executive-authorized** editorial pass recorded as such rather than folded into a normalization;
- and a **non-empty** `.vob`, or its removal from the set.

**Whether the picture lock or `c13df1f4` is the correct base is `CF-001`'s question and is not touched here.**

---

# 9 · CONSTRAINTS OBSERVED

| the Directive prohibits | performed |
|---|---|
| declaring `CF-001` resolved | **no** — `CF-001` is untouched and unresolved |
| determining `ED-003` | **no** |
| determining `ED-004` | **no** |
| determining `ED-005` | **no** |
| inferring governance | **no** |
| inferring repository authority | **no** — §6 cites existing bindings, asserts none |
| designating the artifacts canonical | **no** — §6 assesses candidacy only |

**Nothing was modified, created, moved or committed. No governance determination is made.**

---

```
CF-001A — CORRECTED CAPTION REPRESENTATION REVIEW      ENGINEERING EVIDENCE

Artifacts reviewed              4   ·   1 empty (0 bytes)
Naming discrepancies            1   ·   Part 2 / Part 3 mixed in one folder

Timeline base                   ANALYSIS CUT 4689.500 s
Picture lock                    4846.625 s          Δ  −157.125 s
Structural delta vs analysis    +4 asset-clip       vs lock  +59 asset-clip

Duplicate runs   source 33  →  corrected 33         eliminated  0
Duplicate cues   source 35  →  corrected 35         eliminated  0
Zero-length 0 · non-positive 0 · out-of-order 0 · overlapping 0
Timing            median Δ 0.000 s · max |Δ| 0.042 s · 3 of 2,027 non-zero
Spoken content    CHANGED — 6 instances, 1 deletion, 1 proper noun

Machine readiness               ETC no · citations no · ESS no · generator no

RECOMMENDATION                  R E J E C T

Determination made              NONE        Files modified   NONE
Commits                         NONE        Canonical status NOT DESIGNATED
```

---

*Prepared under Review Directive `CF-001A`. Custody: `MACHINE`. Authority: NONE. This is an engineering evidence review. No governance determination was made, no artifact designated canonical, no registry or stream modified, and no commit created.*
