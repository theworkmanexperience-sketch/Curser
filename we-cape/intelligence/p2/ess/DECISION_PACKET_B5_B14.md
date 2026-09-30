# DECISION PACKET — B-5 / B-14

**Instrument:** Decision Packet (engineering evidence for an Executive ruling)
**Executed under:** `EO-2026-09-29` D-2 (B-5 mechanical re-derivation) and D-3 (B-14 folded in) · D-1 Parent scope
**Production:** Alpha RoundUp 2026 Day 2, 08-24 lineage, `AR2-0824` (**Parent assembly only**)
**Date:** 2026-09-29 · **Repository state at start:** `3d14d5b`
**Custody:** `MACHINE` · **Inference policy:** `ZERO` · **Authority:** NONE

> **This packet proposes nothing and binds nothing.** It is the machine re-derivation the Order
> asked for. The survive-vs-reauthor question is **RESERVED to the Chairman** (EO D-2). No
> `EPR-001` value was authored, populated, inferred, extended, suggested or defaulted. The
> segment boundaries below are a **machine proposal**, not a ratified segment set (Readiness
> Review G7 → G8).

---

## 0 · Result

| Step | Outcome |
|---|---|
| **A** — resolve and hash the designated inputs | **PASS.** Both SHA-256 values equal their rulings exactly |
| **B** — produce and validate the 08-24 ETC | **PASS.** `etc_validation: VALIDATED`, **201 / 201** at 0.0005 s, exit 0 |
| **C** — re-derive S01…S18, reconcile 157.125 s | **COMPLETE.** 18 rows (plus S19 annex). The lock-to-lock identity closes exactly. **Every segment's Δdur decomposes with residual ≤ 0.001 s. No unexplained deltas.** |
| **D** — S12/S13 overlap evidence | **COMPLETE.** Evidence only. **The contested 6.0 s has no counterpart in the 08-24 lock in picture or in caption.** |
| **E** — commit | this commit |

**No step was halted. No blocker is reported.** Six findings are raised in §7 that the
Chairman should see before ruling. None of them stopped a step.

---

## 1 · STEP A — Designated inputs, hashed at ingest (2026-09-30T00:20:50Z)

| role | ruling | path | SHA-256 measured | bytes | match |
|---|---|---|---|---:|---|
| Picture Lock | `ED-003` §2.1 | `…/Corrected Video Analysis Files/Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` | `d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80` | 7,264,164 | **YES** |
| Canonical Caption Stream | `CF-001` §2.1 | `…/Corrected Video Analysis Files/Alpha RoudUp Part 2_SRT_English (United States).srt` | `d93d86a1b7cd99c9baad2ce8e625f486056a5cb8b6229918d04b3bdcb304ef82` | 184,470 | **YES** |

Root: `/Volumes/WE_CAPE_OUTPUT/AlphaRoundUp_2026/Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2 ANALYSIS/`
(the parent folder name ends in a space, as `DAY2_PARENT_FORENSIC_AUDIT` §1.1 recorded).

**Reference inputs**, used only as the "old" side of the mapping. They carry no 08-24 authority:

| role | path | SHA-256 |
|---|---|---|
| 08-22 FCPXML (`SUPERSEDED_ASSEMBLY`) | `SPRINT3A_WORK/inputs/Info.fcpxml` | `2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7` |
| 08-22 SRT (GT-2, the declared stream in `AR2-0822.context.json`) | `SPRINT3A_WORK/inputs/lock_srt2.srt` | `89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b` |
| 08-22 segment set | `intelligence/p2/ess/context/AR2-0822.observations.json` → `segments` | `b325d9ea867d4c7831e49294cf5817e1f251010ea67fb6c22a9e772211b83e6a` |

Every script asserts all four media hashes before reading them. A mismatch is a STOP.

---

## 2 · STEP B — 08-24 Editorial Timing Contract

**Producer:** `scripts/etc_extract.py` (committed, ED-001A-accepted). **Validator:**
`scripts/fcpx_resolve.py` (ECR-GEN-002 B-1 remediation). Both were run unmodified.

```
AR2-0824_ETC.json   sha256 8c76a8cf460a450ea0dcbcd7802cae7fb3245cb1c8b4576a3a9f55ab185b0aaa   202,550 bytes
spine 201   connected_elements 459   sequence.duration_s 4689.5   format_ref r1   declared_lock null
```

| validator gate | result |
|---|---|
| 1 · source identity | `source_sha256_match: true` (`d82c2c3e…` both sides) |
| 2 · sequence duration | `4689.5 == 4689.5` |
| 3 · strict cardinality | ETC 201 == resolved non-transition depth-0 201 (225 incl. 24 transitions) |
| 4 · element-wise | **`201 / 201`**, 0 mismatches, tolerance 0.0005 s |
| closure | `spine_end_s 4689.5 == lock` |
| **verdict** | **`VALIDATED`**, exit 0 |

**Determinism:** three runs produced one hash. A full re-run of `run.sh` into a second directory
reproduced every product byte for byte.

**Against the Readiness Review §3 acceptance criteria:**

| | status |
|---|---|
| ETC-A1 source | absolute path recorded |
| **ETC-A2 source_sha256** | **carries `d82c2c3e…`. §3 names `1ab3d12f…` as the required value, but `ED-003` (issued after the review) designated `d82c2c3e`. §3 is stale on this point. See §7 F-1** |
| ETC-A3 sequence | `duration_s 4689.5` ✓ · `format_ref r1` ✓ · **`declared_lock: null`**. The lock timecode is a human declaration, and none has been issued for 08-24. The extractor does not invent one |
| ETC-A4 spine | 201 entries, nine fields each, non-null offset and duration ✓ (the §3 expectation of 201 holds for `d82c2c3e`) |
| ETC-A5 connected | 459. Accepted **on trust**, as §3 discloses: the platform does not validate this class |
| ETC-A6 independence | produced by `etc_extract.py`, not `fcpx_resolve.py` ✓. Stated plainly: both instruments parse the same FCPXML, so the agreement shows the two parsers agree. It does not show that the editorial system agrees |
| ETC-A7 completeness | now **enforced** by gate 3 ✓ |
| ETC-A8 pinning | **NOT performed.** Writing `AR2-0824.context.json` is gate G2, and this Order does not authorize it. See §7 F-2 |

**Out-of-range observable:** 23 anchored elements resolve past the sequence end
(`out_of_range_status: PRESENT_REQUIRES_DECLARED_DISPOSITION`); 08-22 had 18. Under ECR-GEN-002
§2.4 this is a nesting observable, not a binding failure. **It is reported and not dispositioned.**
Full list: `decision_packet_b5_b14/etc_validation_stdout.txt`.

---

## 3 · STEP C — Method

`decision_packet_b5_b14/rederive_segments.py` holds the full declaration. It is stdlib-only,
read-only and deterministic. In summary:

1. **Tile** both timelines with their non-transition depth-0 spine children. These tile
   `[0, lock]` contiguously; the script asserts contiguity. Picture carried *above* a spine gap
   (positive-lane clips and secondary storylines) gets its own keyed pseudo-tiles, because a gap
   has no media identity but its lanes do.
2. **Identity** is the FCP asset `uid` (the media signature) plus the source-time interval. It
   does not use names or positions.
3. **Retained material** is the per-identity intersection of source intervals. A **maximum-length
   order-preserving chain** discards cross-matches caused by source reuse: 14 pieces, 72.083 s,
   each listed in `rederivation.json → excluded_pieces`. All 14 are the same shot used at two
   places. If a genuine reorder existed it would show up there; none does.
4. **Boundary mapping.** A boundary inside retained material is **MAPPED** (`t + lag`). A boundary
   inside removed material is **SNAPPED** by one declared rule: a start moves forward and an end
   moves back to the nearest retained 08-22 time, then maps. Every snap distance is printed. No
   boundary was AMBIGUOUS or UNMAPPABLE.
5. **Caption corroboration.** This check is independent of the picture. The 08-22 caption words
   in the 20 s inside each boundary are aligned against the **whole** CF-001 word stream, counting
   only runs of 3 or more identical words. The median lag is then compared with the picture lag
   (≤ 1.0 s). A match whose lags scatter (IQR > 2 s) is `INCOHERENT` and counts neither way.

**Independent cross-check.** The picture-derived lag steps reproduce, to within 0.002 s, the
audio-envelope lags that `DAY2_PARENT_FORENSIC_AUDIT` D-1 measured with a different instrument on
different evidence:

| retained block (08-22 s) | picture lag (this packet) | forensic D-1 (Parent→AVM, sign inverted) |
|---|---:|---:|
| 0 – 136.8 | 0.000 | 0.000 |
| 136.8 – 1820.7 | +3.500 (sub-frame re-trims 3.449–3.503) | +3.500 |
| 1851.9 – 2409.7 | −27.708 | −27.710 |
| 2410.9 – 3214.8 | −28.958 (−28.875 on one clip) | −28.960 |
| 3222.3 – 3229.7 | −36.51 | — |
| 3263.5 – 3283.0 | −70.298 | — |
| 3325.1 – 3368.1 | −77.542 | — |
| 3410.2 – 3947.2 | −119.542 | −119.540 |
| 3984.8 – 4846.6 | **−157.125** | *no counterpart found* — see §7 F-4 |

---

## 4 · STEP C — S01…S18 mapping table

Seconds are absolute from sequence start (`tcStart 0s`). TC is 24 fps NDF. **Δ = 08-24 − 08-22.**
"removed / added in seg" are the removed and added intervals that fall inside the segment.
**residual = Δdur − (added − removed)**, which must be 0: that is the "no unexplained delta" test.

| Seg | label | 08-22 in → out | 08-24 in → out | Δin | Δout | Δdur | boundary | removed in seg | added in seg | resid. |
|---|---|---|---|---:|---:|---:|---|---:|---:|---:|
| S01 | cold_open | 0.000 → 73.000 | 0.000 → 73.000 | 0.000 | 0.000 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S02 | host_day_brief | 73.000 → 111.000 | 73.000 → 111.000 | 0.000 | 0.000 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S03 | interview_gauntlet_1 | 111.000 → 1622.000 | 111.000 → 1625.454 | 0.000 | +3.454 | +3.454 | M / M | 0.141 | 3.594 | 0.001 |
| S04 | ride_brief | 1622.000 → 1643.000 | 1625.454 → 1646.500 | +3.454 | +3.500 | +0.046 | M / M | 0.000 | 0.047 | −0.001 |
| S05 | escort_ride | 1660.000 → 1750.000 | 1663.500 → 1753.500 | +3.500 | +3.500 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S06 | librarian_speech | 1903.000 → 1953.000 | 1875.292 → 1925.292 | −27.708 | −27.708 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S07 | council_profile | 1965.000 → 2030.000 | 1937.292 → 2002.292 | −27.708 | −27.708 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S08 | town_proclamation | 2031.000 → 2156.000 | 2003.292 → 2128.292 | −27.708 | −27.708 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S09 | first_ride_moment | 2163.000 → 2190.000 | 2135.292 → 2162.292 | −27.708 | −27.708 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S10 | state_proclamation | 2219.000 → 2332.000 | 2191.292 → 2304.292 | −27.708 | −27.708 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S11 | interview_gauntlet_2 | 2335.000 → 3120.000 | 2307.292 → 3091.042 | −27.708 | −28.958 | −1.250 | M / M | 23.959 | 22.709 | 0.000 |
| S12 | organizer_honors_and_silence | 3124.000 → 3236.000 | 3095.042 → 3193.167 | −28.958 | −42.833 | −13.875 | M / **S −6.322** | 13.874 | 0.000 | −0.001 |
| S13 | group_photo | 3230.000 → 3275.000 | 3193.167 → 3204.702 | −36.833 | −70.298 | −33.465 | **S +33.465** / M | 33.465 | 0.000 | 0.000 |
| S14 | service_wrap_preview | 3276.000 → 3324.000 | 3205.702 → 3212.743 | −70.298 | −111.257 | −40.958 | M / **S −40.958** | 40.958 | 0.000 | 0.000 |
| S15 | riding_music_passage | 3370.000 → 3523.000 | 3290.667 → 3403.458 | −79.333 | −119.542 | −40.208 | **S +40.208** / M | 40.333 | 0.125 | 0.000 |
| S16 | bike_night_arrivals | 3523.000 → 3985.000 | 3403.458 → 3827.875 | −119.542 | −157.125 | −37.583 | M / M | 37.584 | 0.000 | 0.001 |
| S17 | audience_cta | 3985.000 → 4008.000 | 3827.875 → 3850.875 | −157.125 | −157.125 | 0.000 | M / M | 0.000 | 0.000 | 0.000 |
| S18 | bike_night_ambience | 4165.000 → 4780.000 | 4007.875 → 4622.875 | −157.125 | −157.125 | 0.000 | M / M | 0.024 | 0.024 | 0.000 |
| *S19 †* | *friday_wrap_part3_tease* | *4784.000 → 4846.000* | *4626.875 → 4688.875* | *−157.125* | *−157.125* | *0.000* | *M / M* | *0.000* | *0.000* | *0.000* |

`M` = MAPPED · `S` = SNAPPED (with snap distance) · † S19 is outside the Order's S01…S18 scope.
It is in the 08-22 segment set and is bound by EPR-07, which is **RETIRED**. It is shown only so
the timeline is accounted for end to end.

The same table with timecodes and caption columns is in
`decision_packet_b5_b14/mapping_table.csv`.

### 4.1 · Structural readings of the table (measurement only)

- **11 of 18 segments keep their duration to within 0.05 s** (S01, S02, S04–S10, S17, S18).
  They only move, by one of four constant lags. **S03 grows +3.454 s** (insert A1 plus
  re-trims). **S11 changes by −1.250 s** (removal R2 of 1.167 s plus re-trims; the 22.708 s gap
  moves with its block and nets to zero).
- **Five segments shrink materially, and all five sit in one contiguous region**, 08-22
  `3124 → 3985` (`00:52:04 → 01:06:25`): S12 −13.875 · S13 −33.465 · S14 −40.958 · S15 −40.208 ·
  S16 −37.583.
- **Four boundaries SNAP, all in that same region.** S13 keeps **11.535 s of 45.0 s**. S14 keeps
  **7.041 s of 48.0 s**. A snap means the 08-22 boundary itself fell in material the 08-24 lock
  does not contain. **Whether a segment reduced this far still exists as that segment is an
  editorial question, and this packet does not answer it.**
- **Order is preserved.** The re-derived boundaries are monotone and no segment pair overlaps
  (S12/S13: §6).

### 4.2 · Caption corroboration (CF-001)

| result | boundaries (S01–S18, n = 36) |
|---|---:|
| CORROBORATED (caption lag within 1.0 s of picture lag) | **18** |
| DIVERGENT (coherent caption lag ≠ picture lag) | **3**: S04 start, S04 end, S12 end |
| INCOHERENT (common phrases matched at scattered places) | 8 |
| INSUFFICIENT (too few caption words or matches; ambience or music) | 7 |

**No corroborated boundary disagrees with the picture.** The three divergences:

- **S04 (both edges):** picture +3.454 / +3.500; captions **+6.634** (29 words, IQR 0.529). The
  08-24 lock re-lays connected material here. `WE OUT – Stagger formation` music beds and
  `Map traavel…` clips are added or moved on lanes −1 to −3, and `Travel_to_center` moves by +3.5 s.
  **Cause: `INSUFFICIENT_OBSERVATION`.** Settling whether the speech moved independently of the
  picture needs an audio measurement, which is out of scope here.
- **S12 end:** see §6. It is the S12/S13 evidence.

---

## 5 · STEP C — Reconciliation of the 157.125 s aggregate

### 5.1 · What the 157.125 s is

```
08-22 lock (2bf06853, SUPERSEDED_ASSEMBLY)    4846.625 s
08-24 lock (d82c2c3e, ED-003)                 4689.500 s
                                              ──────────
delta                                         −157.125 s
```

### 5.2 · The identity, exact, from media identity (Fraction arithmetic)

```
4846.625 − removed 218.547 + added 61.422 = 4689.500   ✓  closes: true
```

| category (declared rule, `build_tables.py`) | removed (08-22) | added (08-24) | net |
|---|---:|---:|---:|
| `MICRO_RETRIM`: intervals < 0.2 s at edit points (10 removed, 7 added) | 0.377 | 0.412 | +0.035 |
| `GAP_REPOSITIONED`: a keyless 22.708 s gap moved with its block (S11) | 22.708 | 22.708 | 0.000 |
| `REMOVED_MATERIAL` / `ADDED_MATERIAL` | 195.460 | 38.302 | −157.158 |
| **total** | **218.545** | **61.422** | **−157.123** |

Per-interval rounding accounts for the 0.002 s between −157.123 and the exact −157.125. The exact
ledger is in `rederivation.json → ledger`.

**Every removed and added interval, located:**

| # | 08-22 interval (s) | dur | material (FCP clip names) | lies in |
|---|---|---:|---|---|
| R1 | 1820.667 – 1851.875 | 31.208 | `016 · X5 · VID_20260626_102715…` ×2 | **between S05 and S06** |
| R2 | 2409.708 – 2410.875 | 1.167 | `018 · X5 · VID_20260626_104732…` | S11 |
| R3 | 3214.750 – 3222.299 | 7.549 | `056 · DJI · DJI_20260626135655_0026_D` | S12 |
| R4 | 3229.678 – 3263.465 | 33.787 | `056 · DJI · …0026_D` | S12 6.322 · S13 33.465 · **overlap 6.0 counted in both** |
| R5 | 3283.042 – 3325.125 | 42.083 | spine gap (no lane picture) | S14 40.958 · inter 1.125 |
| R6 | 3368.125 – 3410.208 | 42.083 | spine gap + lane `044 · X5 · VID_20260626_133107…` | S15 40.208 · inter 1.875 |
| R7 | 3947.208 – 3984.792 | 37.583 | `055 · X5`, gap, `048 · DJI` | S16 |
| | | **195.460** | | in segments 161.252 (unique) · between segments 34.208 |

| # | 08-24 interval (s) | dur | material | lies in (re-derived) |
|---|---|---:|---|---|
| A1 | 216.917 – 220.378 | 3.462 | `HO11YWOOD_GP` + `028 · DJI` | S03 |
| A2 | 3212.743 – 3247.583 | 34.840 | `056 · DJI`, two spine gaps carrying `Map traavel…-13`, `Round Up`, and the title **`Day 2: Part 3 - Lower Third Text & Subhead`** (at 3213.333 s), lane `044 · X5` | **between S14 and S15** |
| | | **38.302** | | |

**A2 is measured as the Part 3 entry.** It opens with a title element named
`Day 2: Part 3 - Lower Third Text & Subhead`. The forensic audit (F.3) places the Part 3 body start
at Parent `00:53:33.430` = 3213.430 s, 0.1 s from this title. That is recorded as coincidence of
position. **No editorial intent is attributed.**

### 5.3 · The 73.800 s openings and the 15.0–19.6 s tails are not components of the 157.125 s

**Both the Order and the Readiness Review §2.2 name these as the explanation of the 157.125 s. The
measurement does not support that.** They belong to a different comparison:

| quantity | compares | value | source |
|---|---|---:|---|
| **157.125 s** | 08-22 lock **vs** 08-24 lock (both Parent timelines) | −157.125 | this packet §5.2, exact |
| **194.319 s** | sum of the three **Part files vs the 08-24 Parent** | +194.319 | forensic F.1 |

The 73.800 s openings (×2, D-2), the 1.4/1.8 s joins (D-3) and the 15.000/14.800/19.600 s tails
(D-4) are **items in the 194.319 s ledger**. They are material inside the Part extracts that is not
in the Parent. **The 08-24 Parent timeline `d82c2c3e` contains none of them.** Its spine opens
with the same shots at lag 0.000 as 08-22 (S01 and S02 unchanged) and ends at 4689.5 s, so their
contribution to the lock-to-lock 157.125 s is **0.000 s**.

The 0.057 s between the forensic figure (−157.068 s) and this one (−157.125 s) is the Parent
**audio container** (4689.557333 s, ffprobe) against the **sequence** duration (4689.500 s).

Under D-1 (Parent scope) the Part-level openings and tails lie outside this packet. They are
recorded here so the aggregate is not attributed to them in the ruling.

---

## 6 · STEP D — S12/S13 overlap (B-14): evidence only, no assignment

### 6.1 · The condition, as declared in 08-22

```
S12  organizer_honors_and_silence   3124.0 – 3236.0    EPR-05 Deepening    · CLIMACTIC
S13  group_photo                    3230.0 – 3275.0    EPR-06 Celebration  · ELEVATED
contested                           3230.0 – 3236.0    00:53:50:00 – 00:53:56:00   (6.0 s)
```

It sits on the **EPR-05 → EPR-06 beat boundary** (the CLIMACTIC → ELEVATED transition).
`EPR-001` v1.13.0 was read (sha256 `1d54e674…`) and not written.

### 6.2 · The contested span in the 08-22 lock

| instrument | content of 3230.0 – 3236.0 |
|---|---|
| picture (spine) | `056 · 06-26 13:56:55 · DJI · DJI_20260626135655_0026_D.MP4`, tile 3215.042–3283.042, **source 22927.765 – 22933.765 s** |
| captions (GT-2) | #1855 `3230.375` "So now these." · #1856 `3231.458` "You're about to get out of here now." · #1857 `3232.541` "You got good timing." · #1858 `3233.333` "We're gonna go out." · #1859 `3234.500–3238.250` "Just get to the underpass, the little portico." |
| immediately before (S12 only) | #1852 `3214.750` "Real quick little moment of silence." · #1853 `3216.083` "And at the end of it, shout out the name." |

### 6.3 · The contested span in the 08-24 lock

| instrument | finding |
|---|---|
| **picture** | **Source 22927.765–22933.765 is not in the 08-24 spine.** The 08-24 tiles of asset 056 cover 22920.064–22927.443 (3185.792–3193.167), then jump to 22961.230 (3193.167–3212.792). The whole contested span lies inside removed interval **R4** (08-22 3229.678–3263.465, 33.787 s) |
| **captions (CF-001)** | **Cues #1855–#1859 have no coherent counterpart.** Word-run alignment of 08-22 3222–3245 against the whole CF-001 stream finds only four 3–5-word runs, at 161 s, 750 s, 1644 s and 3001 s. These are common phrases at scattered places, not an alignment |
| what survives next to it | the moment-of-silence speech (#1852–#1853) **is** present: CF-001 #1658 `3185.750–3189.416` (`00:53:05:18`) "do a quick little moment of silence and at the end of it shout out the name". Caption lag −28.87 s, which continues S11/S12's −28.958 block. It is carried over **different picture** from the same asset (source 22920.1–22927.4, where 08-22 had 22912.8+) |
| what follows it | CF-001 #1659–#1664 `3196.166–3212.291` ("community service event" · "big thanks to the national committee…" · "big shout out to the smyrna police…" · "hey y'all we still got the bike night" · "series and that's what's good") sit over the retained picture block at lag −70.298 (08-22 3263.465–3283.042). **GT-2 has no cue at all in 08-22 3260.3–3282.6**, so these words have no 08-22 caption counterpart. Whether the audio differs or the 08-22 transcription missed this speech is `INSUFFICIENT_OBSERVATION` without an audio measurement |

### 6.4 · What the mechanical rule produced at this boundary, and why

```
re-derived S12   3095.042 – 3193.167   00:51:35:01 – 00:53:13:04   end SNAPPED back 6.322 s
re-derived S13   3193.167 – 3204.702   00:53:13:04 – 00:53:24:17   start SNAPPED forward 33.465 s
overlap in the re-derived set          0.000 s  (contiguous at 3193.167)
```

**The overlap is not resolved by this. It disappears because the material it concerned is not in
the 08-24 lock.** Both snapped boundaries land on the same 08-24 time, the cut
between asset 056 source 22927.443 (the last surviving S12 frame, from 08-22 3229.678) and source
22961.230 (the first surviving S13 frame, from 08-22 3263.465). **The 6 s has not been
assigned to either beat. It has no 08-24 existence to assign.**

Three facts the ruling may need, stated without a recommendation:

1. The **S12 end** caption evidence (the moment of silence, −28.87 s) and the picture evidence
   (−36.51 s after snap) disagree by **7.645 s** at this boundary. That is the S12-end DIVERGENT
   row in §4.2.
2. Re-derived **S13 keeps 11.535 of 45.0 s.** Its surviving picture is 08-22 3263.465–3275.0.
   None of GT-2's S13 cues (#1855–#1867) has a coherent CF-001 match.
3. The **EPR-05/EPR-06 boundary** was declared against 08-22 seconds. In the re-derived set, the
   edge between S12 (EPR-05) and S13 (EPR-06) is 3193.167 s / `00:53:13:04`. **Whether EPR-05 and
   EPR-06 carry over to these re-derived segments is the reserved survive-vs-reauthor question.
   This packet does not answer it.**

---

## 7 · Findings raised (none halted a step)

| # | finding | class |
|---|---|---|
| **F-1** | Readiness Review §3 **ETC-A2** requires `source_sha256 == 1ab3d12f…` (the PLR-001 candidate). `ED-003` later designated `d82c2c3e…`. The criterion as written is **stale**, and a literal reading would reject the designated lock. This ETC carries `d82c2c3e`, following ED-003. The two are identical in depth-0 structure (225/201), so ETC-A4's 201 still holds | governance text drift |
| **F-2** | `context/AR2-0824.context.json` **still pins `sha.fcpxml = 1ab3d12f…` and `sha.srt = 2a16dd70…`**, neither of which is designated. Its `srt.cues: 2036` describes that stream; the CF-001 stream has **2,034**. The file was **not modified**: pinning is G2, and this Order does not authorize it. **Any generator run against this context would bind the wrong lock and the wrong captions** | stale input, R-4 class |
| **F-3** | `ED-003` §1 lists the accompanying SRT as `…_SRT_English (US).srt`. The filesystem and `CF-001` §1 read `…(United States).srt`. **The hash resolves it** (`d93d86a1…`), so the designated file is unambiguous. The ED-003 text is an abbreviation | citation text |
| **F-4** | **Conflict with forensic D-1.** The audit's audio-envelope sweep found **no counterpart at any lag** for Parent windows 01:04–01:16. This packet finds that span (08-22 3984.8–4846.6 → 08-24 3827.7–4689.5) **retained at a constant −157.125 s by media identity**, and at S19 by caption words (−156.96 / −156.91, CORROBORATED). Same picture and same dialogue alongside an unmatched envelope is consistent with a changed audio bed, but that is `INSUFFICIENT_OBSERVATION`. **Recorded, not resolved.** It does not affect any boundary here, which is picture-derived | cross-instrument disagreement |
| **F-5** | 23 out-of-range anchored elements (08-22: 18) are `PRESENT_REQUIRES_DECLARED_DISPOSITION`. Guard G-07 needs a declared expectation before any generator run | undeclared observable |
| **F-6** | The readiness review and this Order both attribute the 157.125 s to the 73.8 s openings and the tails. **§5.3 shows those belong to the 194.319 s Part-vs-Parent ledger**, and the lock-to-lock 157.125 s is fully itemized by R1–R7 / A1–A2 | attribution error in the record |

---

## 8 · Constraints, discharged

| constraint | how |
|---|---|
| no EPR-001 writes | `EMOTIONAL_PROGRESSION_REGISTRY.yaml` was read only. Its hash is unchanged (`1d54e674…`), and the commit does not touch it |
| no episode generator | none written or run. Parent timeline only (D-1) |
| no regeneration run | `gen_artifacts*.py` not invoked. No governed artifact regenerated. `context/` untouched |
| no silent recovery | every snap, exclusion, divergence and incoherence is enumerated. Each category rule is declared in code |
| no inference | no segment is relabelled, merged, dropped or bound to a beat. The shrunken segments (§4.1) and the vanished overlap (§6.4) are reported, not interpreted |

---

## 9 · Packet contents — `intelligence/p2/ess/decision_packet_b5_b14/`

| file | what | sha256 |
|---|---|---|
| `AR2-0824_ETC.json` | the 08-24 ETC (Step B) | `8c76a8cf460a450e…` |
| `etc_validation_stdout.txt` | validator verdict and census (Step B) | — |
| `rederivation.json` | full machine product: inputs and hashes, ledger, lag blocks, excluded pieces, removed/added, per-boundary mapping and caption evidence | `5d6994b3f36de5bc…` |
| `mapping_table.csv` / `.md` | the S01–S19 table with timecodes | `41cf7075469ee9fc…` |
| `reconciliation.json` | categorized 157.125 s ledger and the per-segment residual test | `116e6e192be54197…` |
| `rederive_segments.py` · `build_tables.py` | the instruments (stdlib, read-only, deterministic) | — |
| `run.sh` | reproduces everything above from the volume. Takes an output directory argument | — |
| `run_stdout.txt` | console record of the committed run | — |

**Reproduce:** `intelligence/p2/ess/decision_packet_b5_b14/run.sh [outdir]`. This needs
`/Volumes/WE_CAPE_OUTPUT` mounted, and every input hash is asserted.

---

## 10 · Standing state after this packet

```
ED-003 Picture Lock            d82c2c3e   hashed at ingest, MATCH
CF-001 Caption Stream          d93d86a1   hashed at ingest, MATCH
08-24 ETC                      8c76a8cf   PRODUCED · VALIDATED 201/201 · NOT PINNED (G2 unauthorized)
08-24 segment set              MACHINE PROPOSAL — unratified (G8)
157.125 s                      RECONCILED — closes exactly, 0 unexplained deltas
S12/S13 overlap                contested 6.0 s absent from 08-24 in picture and caption; NOT ASSIGNED
EPR-001                        UNTOUCHED · survive-vs-reauthor RESERVED to the Chairman
AR2-0824.context.json          STALE (F-2) — unmodified
Episode generator / regen      NOT RUN
```

*Prepared for Executive review under EO-2026-09-29. No execution is directed by this document.*
