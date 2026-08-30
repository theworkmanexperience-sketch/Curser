# CCR-001 — CAPTION COLLAPSE REVIEW

**Issued under:** EXECUTIVE REVIEW ORDER CCR-001, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. No repository modification, no engineering, no commit, no determination.
**Measured at:** `WE_CAPE_OUTPUT` volume, live

> **This review recommends an invariant. It does not declare the Caption Collapse Rule.**
> Nothing here recommends where captions should split, what their timing should be, or how they should read. Those are editorial and are outside this review.

---

# 1 · THE ANSWER, FIRST

**The invariant is the ordered token sequence of the transcript after maximal identical-text runs are collapsed — the *merge normal form*.**

**And the Chairman's own three declared assumptions force this answer before any measurement is taken.** If merging is deterministic and splitting is not, then the invariant cannot live on the split side. A representation can always be merged toward a unique normal form; it cannot always be split back. **The only well-defined common object of two representations is the thing you reach by merging both as far as they will go.** That is not a preference. It is the shape the asymmetry leaves.

Measurement then supports it: collapsing the Parent stream reduces 10,209 raw tokens to **5,145**, against **5,151** produced independently by a separate export of the same program region — **0.12 % apart**, where the raw counts differ by 98 %.

---

# 2 · WHAT THE DEFECT ACTUALLY IS

`INGESTION_MANIFEST.yaml` declares `known_defects: [DOUBLED_CUES, NONPOSITIVE_DURATION_CUES]` on the Parent caption stream and blocks ingestion until a collapse rule is declared. **This is what those defects look like in the data.** `[E]`

```
1   00:00:15,125 --> 00:00:15,458    Let's work!
2   00:00:15,458 --> 00:00:15,791    Let's work!
3   00:00:15,875 --> 00:00:17,666    Wake the city, wake the road, just the bridle, let's go,
4   00:00:17,666 --> 00:00:19,458    Wake the city, wake the road, just the bridle, let's go,
5   00:00:19,500 --> 00:00:21,083    one mission, one ride, we go, silence, rock.
6   00:00:21,083 --> 00:00:21,500    one mission, one ride, we go, silence, rock.
```

**Each pair carries the *full* text twice over two *abutting* spans.** Cue 1 ends at 15.458 and cue 2 begins at 15.458. The speaker said "Let's work!" once, across `[15.125, 15.791]`. **Neither cue is individually true. Only their union is.**

## 2.1 · Census of the doubling

| | Parent stream `80a8ed25…` |
|---|---|
| cues | **5,664** |
| cues after collapsing maximal identical-text runs | **2,962** |
| raw tokens | **27,338** |
| collapsed tokens | **14,559** |
| maximal duplicate runs | **2,612** |
| run-length histogram | **`{2: 2569, 4: 42, 8: 1}`** |
| duplicate adjacencies that abut within 2 ms | **2,668 of 2,702 — 98.7 %** |
| non-positive-duration cues | **29** |

**Two mechanical signatures, and they carry the finding.**

**Run lengths are powers of two — 2, 4, 8, and nothing else.** Not 3, not 5, not 7. A semantic repetition would not distribute that way. This is a caption being re-issued once per underlying segment as the segment count doubles, which is precisely the Chairman's declared mechanism: *camera-angle change, not semantic change.*

**98.7 % of duplicate adjacencies abut to within 2 ms.** They are not overlapping copies and not separated repeats. They tile a single continuous span. **The doubling is a partition of one utterance's time, not a repetition of the utterance.** `[E]`

**This corroborates the Executive's declared assumption that duplicate captions are NOT intentional, and it does so from the data rather than from the declaration.**

---

# 3 · THE TWO PHENOMENA ARE DIFFERENT, AND THE INVARIANT MUST SURVIVE BOTH

The Chairman's worked example and the Parent's defect are **not the same transformation**, and conflating them would produce the wrong rule.

| | text | effect on tokens |
|---|---|---|
| **Split** — the Chairman's example: *"We walked down into the basement"* / *"and realized the water was already three feet deep."* | **different** in each cue | **preserved** — concatenation restores the sentence |
| **Duplication** — the Parent defect: *"Let's work!"* / *"Let's work!"* | **identical** in each cue | **doubled** — concatenation says it twice |

**A rule that only handles splits leaves the transcript doubled. A rule that only handles duplication cannot reassemble a split sentence.** The invariant has to be defined so that both reduce to the same object, and only the collapsed token sequence does that.

---

# 4 · CANDIDATE INVARIANTS, TESTED

## 4.1 · The test corpus, and its limits

`DAY2_PARENT_FORENSIC_AUDIT` establishes that Part 1's body maps to Parent `[0.000, 1633.083]` at lag `0.000 s`, cross-validated by two independent instruments to within 0.046 s. **That region is captioned twice — once in the Parent export, once in the Part 1 export — and is therefore a genuine pair of representations.**

| stream | cues | collapsed | raw tokens | **collapsed tokens** | duplicate runs |
|---|---|---|---|---|---|
| **Parent, region `[0, 1633.083]`** | 2,179 | 1,079 | 10,209 | **5,145** | 1,056 |
| **Part 1, body** | 909 | 907 | 5,155 | **5,151** | 2 |

**Raw token counts differ by 98 %. Collapsed token counts differ by 0.12 %.** `[E]`

**The limit, stated plainly.** The two streams are not two encodings of one caption file — they are two independent transcription runs of the same audio, and their wording differs (*"wake the city, wake the road"* against *"work the city, work the"*). Token-sequence similarity is 0.6981 collapsed against 0.4875 raw. **So the collapse is validated by convergence, not by identity, and no exact-equality test is available anywhere in this repository.** `[E]` for the convergence; `[O]` for exact invariance.

## 4.2 · Results

| candidate invariant | verdict | evidence |
|---|---|---|
| Cue count | **REJECTED** | 2,179 vs 909 |
| Line count | **REJECTED** | follows cue count |
| Collapsed cue count | **REJECTED** | 1,079 vs 907 |
| Raw total word count | **REJECTED** | 10,209 vs 5,155 — the doubling destroys it |
| Raw token sequence | **REJECTED** | doubled text is not the transcript |
| Per-cue timing | **REJECTED** | boundaries move with every split |
| **Collapsed token count** | **SURVIVES** | 5,145 vs 5,151 — **0.12 %** |
| **Collapsed ordered token sequence** | **SURVIVES — RECOMMENDED** | §1, §5 |
| **Covered time-interval union** | **SURVIVES BY CONSTRUCTION** | §5.2 — not falsifiable on present evidence |
| First spoken instant | **WEAK** | 15.125 vs 15.166 — 0.041 s |
| Last spoken instant | **WEAK** | 1633.416 vs 1632.900 — 0.516 s |
| Underlying transcript identity | **NOT TESTABLE** | no two streams here share a transcription |
| Semantic continuity | **NOT MEASURABLE** | outside governed observables; the platform classifies rather than infers meaning |
| **Cue lineage** | **NOT RECOVERABLE — see §5.1** | the asymmetry forbids it |

---

# 5 · WHY THE MERGE NORMAL FORM IS THE RIGHT OBJECT

## 5.1 · Cue lineage cannot be the invariant, and the Executive's own assumptions prove it

> **Merged captions — deterministic. Split captions — NOT deterministic.**

Merging is a function: any run of contiguous cues has exactly one merged form. Splitting is a relation: one cue admits many valid splits, and the choice is driven by camera cuts, reading rate and line length — none of which are properties of the speech.

**Therefore no map from a cue in representation A to a cue in representation B exists in general.** Cue identity is not conserved, cue count is not conserved, and cue boundaries are an artifact of the picture, not of the transcript. **Any invariant defined on cues fails the moment the edit changes, which is the exact condition the rule must survive.**

**What is conserved is what merging converges to.** Merge is idempotent and confluent here — collapse a stream twice and nothing changes; collapse it from either side and you land in the same place. That makes the collapsed form a **normal form**, and a normal form is precisely what "representation A = representation B" needs to mean.

## 5.2 · The second surviving invariant, and why it is ranked below

**The union of covered time intervals** is invariant by construction under all four transformations. Split a cue at any interior instant: the union is unchanged. Merge two abutting cues: unchanged. Collapse a duplicate run whose members tile one span: unchanged. Expand: unchanged.

It is ranked second for three measured reasons:

- **It is not falsifiable on present evidence.** It is a property of the construction, not a finding from the data.
- **The Parent carries 29 non-positive-duration cues.** A cue with `end ≤ start` contributes an empty or inverted interval, and the union is undefined until that second declared defect is also dispositioned. **The two defects named in the manifest are coupled, and the interval union depends on both.**
- **It carries no text.** Two streams with identical coverage and different words would be declared equal. That is not what the manifest is protecting against.

**It is genuinely useful as a cross-check** — a collapse that changes the covered union has done something other than collapse — and that is where this review would put it.

---

# 6 · THE RANKING

```
1  COLLAPSED ORDERED TOKEN SEQUENCE          RECOMMENDED
   the transcript read in time order, with every maximal run of
   contiguous identical-text cues counted once

     survives   split · merge · collapse · expand
     evidence   10,209 → 5,145 against an independent 5,151 · 0.12 %
     rationale  merge is deterministic, split is not; the normal form
                under the deterministic direction is the only object
                both representations are guaranteed to share

2  COVERED TIME-INTERVAL UNION               SUPPORTING CROSS-CHECK
     survives   all four, by construction
     limits     not falsifiable here · undefined until the 29
                non-positive-duration cues are dispositioned ·
                carries no text

3  FIRST AND LAST SPOKEN INSTANT             WEAK, NOT RECOMMENDED ALONE
     0.041 s and 0.516 s across the pair — near-invariant, but they
     are properties of where transcription started and stopped, and
     the last instant is fragile against the same 29 cues
```

---

# 7 · WHAT THIS REVIEW DOES NOT ESTABLISH

Recorded so the Executive can see the edge of the evidence.

- **No exact-equality test exists in this repository.** Every available pair differs in transcription as well as representation. The recommendation rests on **convergence from 98 % apart to 0.12 % apart**, which is strong and is not proof. `[O]`
- **Normalization is unspecified.** The 0.12 % residual was measured under lowercase, punctuation-stripped, whitespace-split tokenization. **Case, punctuation, hyphenation, numerals and speaker labels each move the count**, and none of them is declared anywhere in the repository. A collapse rule that does not also fix tokenization is not yet reproducible. `[O]`
- **The two declared defects are coupled.** `DOUBLED_CUES` and `NONPOSITIVE_DURATION_CUES` cannot be dispositioned independently: the 29 non-positive cues sit inside runs that the collapse rule will touch. `[E]`
- **A run of 8 exists.** One caption was re-issued eight times. Whatever rule is declared should be checked against that case explicitly rather than against the 2,569 pairs. `[E]`
- **The 91 SRT-cue-index citations** across four registries, recorded in PRR-001 §4.4, are counted against the *un-collapsed* stream. **Declaring the rule changes what `#NNNN` refers to.** This review does not address re-pointing; it notes that the citation set is downstream of this determination. `[E]`

---

# 8 · DELIVERABLE

```
GOVERNED INVARIANT — RECOMMENDED

  The ordered token sequence of the transcript, read in time order,
  with every maximal run of contiguous cues bearing identical text
  counted exactly once.

  Equivalently: the merge normal form of the caption stream.

  Two representations are the same caption stream if and only if
  their merge normal forms are equal.

  Cue count, cue boundaries, line count, per-cue timing and cue
  identity are representation, not content, and none of them is
  conserved.
```

**Supporting cross-check, recommended alongside but not as the invariant:** the covered time-interval union must not change under a valid collapse.

**Not established, and stated as such:** exact invariance, because no two streams in this repository share a transcription; and tokenization, which must be declared for the rule to be reproducible.

---

```
Streams measured           2 primary · 1 genuine representation pair
Parent census              5,664 cues → 2,962 collapsed · 27,338 → 14,559 tokens
Duplicate runs             2,612 · lengths {2:2569, 4:42, 8:1} · 98.7% abutting
Decisive measurement       10,209 → 5,145 vs independent 5,151 · 0.12%
Invariants surviving       2, ranked
Invariants rejected        6
Exact-equality test        NONE AVAILABLE — recorded as a limit
Editorial recommendations  NONE — no split points, timing or style proposed
Determinations made        NONE
```

---

*Prepared under CCR-001. Custody: MACHINE. Authority: NONE. No repository file, registry, caption stream or source file was modified. No commit was made. The Caption Collapse Rule is not declared here and remains reserved to Executive authority.*
