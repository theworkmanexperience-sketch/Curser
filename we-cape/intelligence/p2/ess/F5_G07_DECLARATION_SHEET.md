# F-5 / G-07 — OUT-OF-RANGE DECLARATION SHEET (AR2-0824)

**Required by:** EO-2026-09-29 Addendum B §F-5 / G-07 · **Date:** 2026-09-30 · **Custody:** `MACHINE` · **Authority:** NONE
**The `DECLARED EXPECTATION` column is reserved to the Chairman and is left empty.** No generator
run may proceed until it is declared (Addendum B). Guard G-07 asserts the resolved out-of-range
count against a **declared** expectation, and this sheet is the input for that declaration.

## Source, hash-asserted before reading

| | path | sha256 |
|---|---|---|
| 08-24 lock (ED-003) | `…/Corrected Video Analysis Files/Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` | `d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80` |
| 08-22 lock (comparison only) | `SPRINT3A_WORK/inputs/Info.fcpxml` | `2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7` |
| resolver | `scripts/fcpx_resolve.py`, run with `NONE`: no ETC, no generator | == HEAD blob |
| machine product | `decision_packet_b5_b14/f5_out_of_range.json` (from `f5_enumerate.py`) | `3a7a79ff02c2c99531f0eea593eda24329f107f6c975bbbda028487de67ed3c5` |

## Definition (the resolver's own predicate, unchanged)

An anchored element is **out of range** when its resolved `abs_in_s < −0.001` **or**
`abs_out_s > 4689.5 + 0.001`. **Correction to packet `aec3a27` §2 wording:** the packet said these
elements "resolve past the sequence end". In fact **10 of the 23 lie before 0 and 13 lie past the
end**. The count (23) is unchanged.

**What these are, measured:** every one of the 23 is an inner component (depth 1–3) of a compound
`clip`, or of a compound nested in an `asset-clip`, whose own inner timebase extends far beyond the
portion the edit uses. The depth-0 anchor of every row lies inside `[0, 4689.5]`, and **the ETC
binding is unaffected (201/201)**. ECR-GEN-002 §2.4 classifies this as an FCPXML nesting
observable, not a binding failure. **This sheet makes no claim about whether any of it is visible
or audible in the program.**

`id` is the resolver's element path. The bracketed number is the resolver's row index, which is
deterministic for this file and resolver.

## Count

```
08-22 (2bf06853)   18
08-24 (d82c2c3e)   23
delta              +5    all 18 of the 08-22 population pair one-to-one into 08-24
                         (key: tag, name, lane, duration); 0 unpaired 08-22 elements
```

**The +5 (rows 19–23) are all components of asset 056 `DJI_20260626135655_0026_D.MP4`.** They hang
off depth-0 tiles at 3185.792 s and 3193.167 s, which is the re-cut S12/S13 region. 3193.167 is the
Tier-3 EPR-05→EPR-06 edge (Addendum A). This is recorded as location only.

## Enumeration

| # | id | lane | depth | resolved span (s) | out of range by | content | depth-0 anchor (08-24) | 08-22 counterpart | **DECLARED EXPECTATION** |
|---|---|---|---:|---|---|---|---|---|---|
| 1 | `/sequence/spine/clip/video[43]` | — | 1 | -51.815 → 162.232 | 51.815 s before 0 | `video` · VID_20260626_104336_00_023 - v1 · media `VID_20260626_104336_00_023.mov` | clip `017 · 06-26 10:43:36 · X5 · VID_20260626_104` @ 21.458–26.250 (00:00:21:11) | `/sequence/spine/clip/video[17]` | |
| 2 | `/sequence/spine/clip/clip/gap[45]` | — | 2 | -125.088 → 88.959 | 125.088 s before 0 | `gap` · Gap · no media (gap) | clip `017 · 06-26 10:43:36 · X5 · VID_20260626_104` @ 21.458–26.250 (00:00:21:11) | `/sequence/spine/clip/clip/gap[19]` | |
| 3 | `/sequence/spine/clip/clip/gap/audio[46]` | -1 | 3 | -125.088 → 88.959 | 125.088 s before 0 | `audio` · VID_20260626_104336_00_023 - a1 · media `VID_20260626_104336_00_023.mov` | clip `017 · 06-26 10:43:36 · X5 · VID_20260626_104` @ 21.458–26.250 (00:00:21:11) | `/sequence/spine/clip/clip/gap/audio[20]` | |
| 4 | `/sequence/spine/clip/video[55]` | — | 1 | 25811.334 → 25954.393 | 21264.893 s past end | `video` · DJI_20260626210523_0030_D - v1 · media `DJI_20260626210523_0030_D.MP4` | clip `065 · 06-26 21:05:23 · DJI · DJI_20260626210` @ 35.375–39.000 (00:00:35:09) | `/sequence/spine/clip/video[28]` | |
| 5 | `/sequence/spine/clip/clip/gap[57]` | — | 2 | -37.656 → 105.403 | 37.656 s before 0 | `gap` · Gap · no media (gap) | clip `065 · 06-26 21:05:23 · DJI · DJI_20260626210` @ 35.375–39.000 (00:00:35:09) | `/sequence/spine/clip/clip/gap[30]` | |
| 6 | `/sequence/spine/clip/clip/gap/audio[58]` | -1 | 3 | -37.656 → 105.403 | 37.656 s before 0 | `audio` · DJI_20260626210523_0030_D - a1 · media `DJI_20260626210523_0030_D.MP4` | clip `065 · 06-26 21:05:23 · DJI · DJI_20260626210` @ 35.375–39.000 (00:00:35:09) | `/sequence/spine/clip/clip/gap/audio[31]` | |
| 7 | `/sequence/spine/clip/video[61]` | — | 1 | -41.289 → 101.771 | 41.289 s before 0 | `video` · DJI_20260626210523_0030_D - v1 · media `DJI_20260626210523_0030_D.MP4` | clip `065 · 06-26 21:05:23 · DJI · DJI_20260626210` @ 39.000–39.333 (00:00:39:00) | `/sequence/spine/clip/video[33]` | |
| 8 | `/sequence/spine/clip/video[78]` | — | 1 | 4917.787 → 4933.178 | 243.678 s past end | `video` · DJI_20260626213650_0035_D - v1 · media `DJI_20260626213650_0035_D.MP4` | clip `073 · 06-26 21:36:50 · DJI · DJI_20260626213` @ 53.958–58.750 (00:00:53:23) | `/sequence/spine/clip/video[41]` | |
| 9 | `/sequence/spine/asset-clip/clip/gap[1537]` | — | 2 | -188.119 → 2454.896 | 188.119 s before 0 | `gap` · Gap · no media (gap) | asset-clip `016 · 06-26 10:27:19 · X5 · VID_20260626_102` @ 1805.417–1824.167 (00:30:05:10) | `/sequence/spine/asset-clip/clip/gap[335]` | |
| 10 | `/sequence/spine/asset-clip/clip/gap/audio[1538]` | -1 | 3 | -188.119 → 2454.896 | 188.119 s before 0 | `audio` · DJI_20260626105930_0016_D - a1 · media `DJI_20260626105930_0016_D.MP4` | asset-clip `016 · 06-26 10:27:19 · X5 · VID_20260626_102` @ 1805.417–1824.167 (00:30:05:10) | `/sequence/spine/asset-clip/clip/gap/audio[336]` | |
| 11 | `/sequence/spine/asset-clip/clip/video[1540]` | — | 2 | -41218.067 → -38575.051 | 41218.067 s before 0 | `video` · DJI_20260626105930_0016_D - v1 · media `DJI_20260626105930_0016_D.MP4` | asset-clip `016 · 06-26 10:27:19 · X5 · VID_20260626_102` @ 1805.417–1824.167 (00:30:05:10) | `/sequence/spine/asset-clip/clip/video[338]` | |
| 12 | `/sequence/spine/clip/video[2857]` | — | 1 | 9824.221 → 10468.156 | 5778.656 s past end | `video` · DJI_20260626134039_0025_D - v1 · media `DJI_20260626134039_0025_D.MP4` | clip `049 · 06-26 13:40:39 · DJI · DJI_20260626134` @ 3096.125–3127.083 (00:51:36:03) | `/sequence/spine/clip/video[775]` | |
| 13 | `/sequence/spine/clip/clip/gap[2865]` | — | 2 | 11028.685 → 12847.669 | 8158.169 s past end | `gap` · Gap · no media (gap) | clip `049 · 06-26 13:40:39 · DJI · DJI_20260626134` @ 3096.125–3127.083 (00:51:36:03) | `/sequence/spine/clip/clip/gap[780]` | |
| 14 | `/sequence/spine/clip/clip/gap/audio[2866]` | -1 | 3 | 11028.685 → 12847.669 | 8158.169 s past end | `audio` · DJI_20260626135655_0026_D - a1 · media `DJI_20260626135655_0026_D.MP4` | clip `049 · 06-26 13:40:39 · DJI · DJI_20260626134` @ 3096.125–3127.083 (00:51:36:03) | `/sequence/spine/clip/clip/gap/audio[781]` | |
| 15 | `/sequence/spine/clip/spine/clip/video[2873]` | — | 3 | -7475.895 → -5656.911 | 7475.895 s before 0 | `video` · DJI_20260626135655_0026_D - v1 · media `DJI_20260626135655_0026_D.MP4` | clip `049 · 06-26 13:40:39 · DJI · DJI_20260626134` @ 3096.125–3127.083 (00:51:36:03) | `/sequence/spine/clip/clip/video[784]` | |
| 16 | `/sequence/spine/asset-clip/clip/gap[2945]` | — | 2 | 9963.817 → 11782.801 | 7093.301 s past end | `gap` · Gap · no media (gap) | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3180.083–3185.792 (00:53:00:02) | `/sequence/spine/asset-clip/clip/gap[819]` | |
| 17 | `/sequence/spine/asset-clip/clip/gap/audio[2946]` | -1 | 3 | 9963.817 → 11782.801 | 7093.301 s past end | `audio` · DJI_20260626135655_0026_D - a1 · media `DJI_20260626135655_0026_D.MP4` | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3180.083–3185.792 (00:53:00:02) | `/sequence/spine/asset-clip/clip/gap/audio[820]` | |
| 18 | `/sequence/spine/asset-clip/spine/clip/video[2956]` | — | 3 | 9956.399 → 11775.383 | 7085.883 s past end | `video` · DJI_20260626135655_0026_D - v1 · media `DJI_20260626135655_0026_D.MP4` | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3185.792–3189.458 (00:53:05:19) | `/sequence/spine/asset-clip/spine/clip/video[823]` | |
| 19 | `/sequence/spine/asset-clip/clip/gap[2958]` | — | 2 | 9957.583 → 11776.567 | 7087.067 s past end | `gap` · Gap · no media (gap) | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3185.792–3189.458 (00:53:05:19) | **NEW (+)** | |
| 20 | `/sequence/spine/asset-clip/clip/gap/audio[2959]` | -1 | 3 | 9957.583 → 11776.567 | 7087.067 s past end | `audio` · DJI_20260626135655_0026_D - a1 · media `DJI_20260626135655_0026_D.MP4` | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3185.792–3189.458 (00:53:05:19) | **NEW (+)** | |
| 21 | `/sequence/spine/asset-clip/clip/gap[2963]` | — | 2 | 9963.796 → 11782.780 | 7093.280 s past end | `gap` · Gap · no media (gap) | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3185.792–3189.458 (00:53:05:19) | **NEW (+)** | |
| 22 | `/sequence/spine/asset-clip/clip/gap/audio[2964]` | -1 | 3 | 9963.796 → 11782.780 | 7093.280 s past end | `audio` · DJI_20260626135655_0026_D - a1 · media `DJI_20260626135655_0026_D.MP4` | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3185.792–3189.458 (00:53:05:19) | **NEW (+)** | |
| 23 | `/sequence/spine/asset-clip/spine/clip/video[2979]` | — | 3 | 9956.397 → 11775.381 | 7085.881 s past end | `video` · DJI_20260626135655_0026_D - v1 · media `DJI_20260626135655_0026_D.MP4` | asset-clip `056 · 06-26 13:56:55 · DJI · DJI_20260626135` @ 3193.167–3212.792 (00:53:13:04) | **NEW (+)** | |

`lane` "—" = none (the element sits on its parent's storyline). All spans are absolute sequence
seconds as computed by the resolver.

## Summary for declaration

| population | count |
|---|---:|
| before 0 | 10 |
| past end | 13 |
| carried from 08-22 (paired) | 18 |
| new in 08-24 (all asset 056) | 5 |
| **total** | **23** |

## DECLARED EXPECTATION — Chairman, 2026-09-30 (verbatim; applies to rows 1–23 as enumerated above)

Declare rows 1–23, preserving their existing enumerated identifiers in
the evidence sheet at `e79a2b3`, as `EXPECTED_STRUCTURAL_NESTING
(ECR-GEN-002 §2.4)`, scoped to the designated lock and source bindings
represented by that evidence.

The declared census is 23 elements: 10 resolving before zero and 13
resolving past the program end; 18 carried and 5 new. This declaration
records expected structural nesting. It does not endorse those
elements as program content, waive a binding error, or authorize their
inclusion in an emitted artifact.

Retain G-07's stated expectation of exactly these twenty-three
enumerated elements—not merely any set totaling twenty-three. A
mismatch requires the existing stop-and-review process; the
expectation must not be silently updated to match a changed result.

Preserve the asset-056 cross-reference for rows 16–23, including the
connection to Tier-3 disposition rows 3–5 and 9. If those rulings
change the relevant resolver inputs, boundaries, or nesting structure,
re-enumerate the affected evidence and obtain a renewed declaration
before relying on the prior expectation.

This declaration does not decide the nine editorial disposition cells,
ratify EPR-001 `v1.14.0-PROPOSED`, or authorize a regeneration run.

*(The empty per-row column above is satisfied by this declaration for
rows 1–23; G-07's machine-readable expectation is wired from this
block, id-pinned, under a future generator-run order.)*
