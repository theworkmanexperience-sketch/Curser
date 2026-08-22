# DOC-001 — Validate the instrument before the measurement
## Governance Status
Document Type: Doctrine (ratified) · Status: **RATIFIED** · Date: 2026-08-22
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
