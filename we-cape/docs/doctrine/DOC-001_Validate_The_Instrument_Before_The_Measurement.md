# DOC-001 — Validate the instrument before the measurement
## Governance Status
Document Type: Doctrine (ratified) · Status: **RATIFIED** · Date: 2026-08-22 · **Amendment 1: 2026-08-22**
Authority: Executive Producer (Executive Assessment, Sprint 3A, 2026-08-22)
Chairman countersignature: ☐ pending
Promoted from: `DOC-SRC-001` §2 candidate **DC-01** · Proved by: **RE-001**
Scope: PLATFORM — binds every engine, module and analysis in WE CAPE.

## The doctrine
> **A derived instrument earns trust by reproducing a known-good result first. Only then may its novel
> output enter registry custody.**

## What it requires, operationally
1. Any tool that *derives* values — a parser, a resolver, a correlator, a classifier — SHALL be run
   first against a set whose correct answers are already governed.
2. The reproduction result SHALL be stated as a **ratio, not an adjective**: `191/191`, not "validated".
3. Novel output from an instrument that has not passed step 1 is **ineligible for registry custody**.
   It may be reported; it may not be relied upon.
4. Where a second, independent check is available at low cost, take it. Two weak instruments that
   agree beat one strong instrument that cannot be contradicted.

## Why it is doctrine and not merely good practice
Sprint 3A did not adopt this as a preference. It was forced into it and then rescued by it.

`P2_LOCK_timing.json` published `timeline_offset_s: null` for all 404 connected elements and referenced
parents by non-unique clip name. The two artifacts Step 0 existed to produce — exact in/outs for the 16
audio-lane elements and the 40 titles — were not derivable from the contract that was supposed to carry
them. They had to be re-derived from FCPXML nesting by a resolver written during the run.

A resolver written during the run is exactly the kind of instrument nobody should believe. It was
believed because it was made to reproduce **191 of 191** ETC spine offsets to within 0.0006 s and to
terminate at exactly 4846.625 s *before* its novel output was read. Then a picture probe caught the
hardest remaining case — a title nested inside a compound clip — in rendered frames.

The counterfactual is the point. Had the resolver been trusted on its plausibility, a systematic
off-by-one in compound-clip recursion would have silently shifted the position of every nested caption,
and the error would have entered the registry wearing the same confidence as everything else.

## The companion rule
The same run showed the inverse failure. Two segments returned confident-looking timebase shifts of
−6.75 s and −3.25 s. Both were artefacts of a saturated speech mask. They were caught by making the
correlation prove itself against a null distribution.

> **A correlation peak with no null behind it is not evidence.**

Recorded here as the measurement-side companion to the instrument-side rule; carried in `DOC-SRC-001`
as candidate **DC-02** and promotable on the same reasoning.

## Non-goals
This doctrine does not require a formal test suite for every script, and it is not a mandate for
ceremony. A single ratio against governed values discharges it. The cost of compliance in Sprint 3A was
one function and about four minutes.

## Provenance
`DOC-SRC-001` §1 bullet 2 (verbatim reflection, 2026-08-22) → candidate DC-01 → Executive Assessment,
Sprint 3A ("That is no longer merely a reflection. Sprint 3A proved it.") → **DOC-001**.
Evidence of record: `RE-001` §6.2 · `intelligence/p2/ess/STEP0_TIMING_CLOSURE.md` §4 ·
`intelligence/p2/ess/ESS_VALIDATION_REPORT.md` §1.

---

# Amendment 1 — 2026-08-22: the instrument must also be the *right* instrument

**Authority:** Executive Producer, 2026-08-22 · **Occasion:** an editorial-resolution viewing master was
located before `EVS-001` · **Status:** amendment to ratified doctrine, Chairman countersignature ☐ pending

## A1.1 The Executive Amendment, as issued

> *"Whenever an editorial-resolution viewing master exists, Executive Viewing Sessions (EVS) shall use
> that master in preference to engineering proxies. Engineering artifacts may continue using proxies
> where resolution does not materially affect the governed task (e.g., synchronization, timing,
> registry extraction). Creative and editorial judgments shall preferentially use the highest-fidelity
> approved viewing master."*

**Adopted.** It does not change Sprint 3A, whose proxy use was appropriate to its tasks and is
explicitly preserved by the amendment's second clause.

## A1.2 The engineering addition — fidelity is not the selection criterion

Applying the amendment to `EVS-001` immediately produced a finding that the amendment as written would
not have caught, and it belongs in the doctrine rather than in a session brief.

**Selecting a viewing master by fidelity alone would have been wrong two times in three.** Seven
candidate renders of Alpha RoundUp Part 2 exist on the media volume. Measured:

| candidate | size | duration | resolution | vs lock 4846.625 s |
|---|---|---|---|---|
| `XML retry/Thursday Aug 20th/Alpha RoudUp Part 2.m4v` | 12 GB | **4846.625000 s** | 3840×2160 | **EXACT — 0.000 s** ✅ |
| `Reduced Files/Alpha RoudUp Part 2.mp4` | 1.6 GB | **4846.625000 s** | 720×480 | EXACT — 0.000 s ✅ |
| `Filmage_Editor.mp4` (Sprint 3A proxy) | 381 MB | 4846.747000 s | 320×180 | +0.122 s (2.9 frames) |
| `Saftey File/…_SRT_.m4v` | 941 MB | 4848.125000 s | 854×480 | **+1.500 s** ❌ |
| `Alpha RoundUp Part 2 /Reduced_Part_2.mp4` | 389 MB | 4850.810000 s | 320×180 | **+4.185 s** ❌ |
| `Saftey File/…Safe 2.m4v` | **12 GB** | 4861.833333 s | **3840×2160** | **+15.208 s** ❌ |
| `Saftey File/… - Saftey .m4v` | **12 GB** | 4868.625000 s | **3840×2160** | **+22.000 s** ❌ |

**Three of the seven are 4K. Only one of those three is lock-conformant.** The two rejects are the same
size, the same codec, the same resolution and nearly the same filename as the correct file. In a
directory listing they are indistinguishable. Chosen by fidelity, a viewing session would have had a
one-in-three chance of running on a timebase up to **22 seconds** away from the FCPXML — and every
timecode the Executive recorded would have been wrong by an amount nothing in the session would reveal.

Note also that the **720×480 reduced file is lock-conformant** while two 4K files are not. Fidelity and
conformance are independent properties, and only one of them makes a timecode mean anything.

## A1.3 The rule

> **An instrument is validated by conformance first and fidelity second. For any judgement expressed
> in timecode, the viewing master SHALL be verified against the governed lock — duration, frame rate,
> and hash — before it is used, and its hash recorded. Among conformant candidates, prefer the
> highest fidelity. A non-conformant candidate is not a lower-quality option; it is a different film.**

This is the same doctrine, not a new one. `191/191` validated a resolver against governed values before
its novel output was read. `4846.625000 s` validates a viewing master against the same lock before an
Executive's eyes are spent on it. Rule 2 applies unchanged: **state the result as a number, not an
adjective.** "The 4K master" is an adjective. "4846.625000 s, exact" is a validation.

## A1.4 The approved viewing master for Alpha RoundUp Part 2

```
path      Alpha RoundUp Part 2 /XML retry/Thursday Aug 20th/Alpha RoudUp Part 2.m4v
duration  4846.625000 s   EXACT match to the editorial lock
video     3840x2160 h264, 24/1 fps NDF
audio     AAC 48 kHz stereo   (the Sprint 3A proxy carried 44.1 kHz)
size      12,199,752,138 bytes
sha256    89e911b1bffe14cefe330f8e4270d467dc06393b622143350ca42de8dbf8cd46
status    APPROVED VIEWING MASTER for Executive creative judgement, Alpha RoundUp Part 2
excluded  the three non-conformant renders in A1.2 are NOT approved for any timecoded judgement
```

## A1.5 Rule 4 exercised — the two instruments agree

The doctrine's fourth requirement — *"where a second, independent check is available at low cost, take
it"* — was discharged rather than assumed. The `EVS-001` region metrics were recomputed from the master
and compared with the proxy figures they were originally derived from:

| measurement | from the master | from the proxy | agreement |
|---|---|---|---|
| across CUE-03 out (29:10) | **+0.5565 dB** | +0.5251 dB | **0.031 dB** |
| across SIL-01 in (31:43) | **−7.6244 dB** | −7.6476 dB | **0.023 dB** |

Two instruments — a 320×180 / 44.1 kHz proxy and a 3840×2160 / 48 kHz master — agree to within
**0.03 dB** on both deltas that carry the finding. The Sprint 3A metrics stand, and now stand on two
independent measurements rather than one. The verdicts are unchanged: **no audible event at 29:10**
(+0.556 dB, below the ~1 dB JND); **a large audible event at 31:43** (−7.624 dB).

*Recorded 2026-08-22. Amends ratified doctrine at Executive direction.*
