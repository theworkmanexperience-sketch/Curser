# B-5 re-derivation — VERSION 2 (correction)

> **RATIFIED (G8) by the Chairman, 2026-09-30.** See Addendum B, G8 section. The candidate status
> line below is preserved as written at issue.

**Status: CANDIDATE — PENDING CHAIRMAN G8 RATIFICATION.** v1 (`../rederivation.json`,
`5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117`) remains the ratified G8
artifact until the Chairman rules. v1 is unmodified and still reproduces byte-for-byte
(`../run.sh`). Authorized by the Chairman on 2026-09-30 ("Correct, then reopen R6").

| artifact | sha256 |
|---|---|
| `rederivation_v2.json` | `5bd4af486e9eb745660504b41290154fb5d8c0b511b6bc74cca5102dd4b0a28b` |
| `reconciliation.json` (v2) | `de3e3ca034fd99e84b99f1a4530d34de07daa595a54b534b501c77dc8e76b293` |
| `mapping_table.csv` (v2) | `f3df302ade255c96a4cb215805306280cbbb29517a11f2a2895fb9bdff18ef66` |
| instrument `../rederive_segments_v2.py` | `3ee564ea91e03b26ad2ca56bb068ecf23dedfaa4f5b2e39fc337d6d9765c19ac` |
| inputs | identical to v1, hash-asserted: lock `d82c2c3e…`, 08-22 `2bf06853…`, CF-001 `d93d86a1…`, GT-2 `89d61f96…` |

Reproduce: `../run_v2.sh [outdir]`. It is deterministic; two runs gave identical bytes.

## Why

v1 gave media identity only to overlay picture that was a direct child of a spine gap. In
both locks, the picture after asset 056 is a **secondary storyline attached to a spine clip
that runs on over the following gap** (X5 044). v1 could not see it. It booked the 08-22 S14
body as REMOVED (R5, 42.083 s) and the **same footage** in 08-24 as ADDED ("A2", 34.840 s).
Verified by source range: 044 source 16.125–29.625, 68.167–79.458 and 86.75–96.75 s appear in
both locks. The host-wrap audio clip "Map traavel to Smyrna Event Center-13" (0–43.308 s)
appears in both locks, lag −69.799. And 99 caption words align at +69.746 (IQR 0.256).

## Corrections

- **C1 — identity over spine gaps.** Overlay picture is collected from every depth-0 element
  and clipped to the spine-gap spans. Wherever the spine has a clip, identity is unchanged
  from v1.
- **C2 — caption check at snapped boundaries.** The lag comparison is not evidence of
  position there. v2 reports `NOT_EVALUATED_AT_SNAPPED_BOUNDARY`, plus the position the
  captions project for the original boundary. v1's S14-end `CORROBORATED` was an artifact
  of this flaw.
- **C3 — sub-frame overlap.** The chain admits overlaps shorter than one frame between
  successive pieces. The ledger carries `overlap_absorbed_s` (0.027 s: one 08-22 instant
  at 3325.125–3325.152 is laid end to end in 08-24), so the identity is exact:
  `4846.625 − 161.077 + 3.925 + 0.027 = 4689.500`.

## v1 → v2 differences (complete)

| | v1 | v2 |
|---|---|---|
| **S14** | 3205.702 → 3212.743 (7.041 s), end SNAPPED −40.958 | **3205.702 → 3246.432 (40.730 s)**, end **MAPPED** (lag −77.568), Δdur **−7.270** |
| S14 caption end | CORROBORATED (C2 flaw) | **DIVERGENT**: speech lag −69.741 vs picture −77.568, a 7.827 s difference |
| S12 caption end | DIVERGENT | NOT_EVALUATED_AT_SNAPPED_BOUNDARY (projected 3207.134) |
| S13, S15 caption start | INCOHERENT / INSUFFICIENT | NOT_EVALUATED_AT_SNAPPED_BOUNDARY |
| removed / added | 218.547 / 61.422 | **161.077 / 3.925** (+0.027 overlap) |
| R5 (08-22 3283.042–3325.125, 42.083 s) | REMOVED | **only 7.292 s removed** (08-22 3307.860–3315.152, 044 source 79.458–86.75); the rest is retained |
| "A2" (08-24 3212.743–3247.583, 34.840 s) | ADDED, unsegmented | **does not exist.** It is the relocated S14 body; what remains added is 0.048 s at 3212.743 (the 056 boundary fact) and 0.004 s at 3237.58 |
| 22.708 s gap in S11 | GAP_REPOSITIONED (keyless) | retained **by identity** (overlay picture matched) |
| excluded cross-matches | 14 / 72.083 s | 14 / 72.083 s (identical set) |
| **all other segments** (S01–S13, S15–S19) | — | **boundaries and statuses unchanged** |

**Decided rows:** R1–R5, R7 and R8 rest on unchanged boundaries. The R4 edge (3193.167) is
unchanged. **R6 (S14) was decided on the v1 premise** and has been reopened for
re-presentation at the Chairman's direction. **R9's premise, the 34.840 s unsegmented A2,
does not survive v2.** The TIMELINE Tier-1 proposal (`c5a72dc`) is unaffected, since
S14 was not rebased there.
