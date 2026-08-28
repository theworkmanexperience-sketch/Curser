# EPR-001 — VALIDATION REPORT UNDER PATH B

**Subject:** `EMOTIONAL_PROGRESSION_REGISTRY.yaml` v1.2.0 · **Custody:** `MACHINE`
**Occasion:** `EXECUTIVE ORDER — CUSTODY_ALERT_001 FINAL DISPOSITION & WORKBOOK GENERATION`,
2026-08-28, §2.4 · **Date:** 2026-08-28
**Supersedes for validation purposes:** the V-1…V-6 table in `IR-002` §2, which was run against
v1.1.0 before the production identity was ratified.

---

## 0 · Headline

**All six criteria PASS, and that is the finding — not the reassurance.**

> **V-2 resolves 17 of 17 segment references, including `S19`. `S19` does not exist in the
> governed production.** The validator checks against `TIMELINE_REGISTRY v1.0.0`, which is the
> segment authority of the **superseded assembly**. A validator whose reference is superseded
> cannot detect that its subject has been superseded.

`EPR-07` is broken, `V-2` says it is fine, and **both statements are correct**. §3 sets out why,
and §4 states what would have to change for a validator to catch it.

---

## 1 · Structural validation — `epr_validate.py`, V-1 … V-6

Run 2026-08-28 against `EMOTIONAL_PROGRESSION_REGISTRY.yaml` v1.2.0 and
`TIMELINE_REGISTRY.yaml` v1.0.0.

```
criterion status  measurement
V-1       PASS    7/7 conforming
V-2       PASS    17/17 resolve
V-3       PASS    0 prohibited keys; timecode-shaped scalars outside prose: 0
V-4       PASS    file source_class=EXECUTIVE; non-conforming entries: none
V-5       PASS    observed=17 expected=19 percentage=89.47%; undeclared: ['S04','S17']
V-6       PASS    declared field-values=7; AWAITING_EXECUTIVE_INPUT=29; out-of-vocabulary
                  intensity: none
```

**Delta against the v1.1.0 run in `IR-002`: none in any criterion.** Every number is identical.
That is itself evidence for §3 — **ratifying a new production changed nothing the validator can
see.**

### 1.1 Two defects found and corrected during this run, reported rather than buried

| # | defect | resolution |
|---|---|---|
| **VD-1** | The v1.2.0 draft introduced **timecode-shaped strings** into explanatory notes. `timecodes` is a `prohibited_field` of this registry; `V-3` counted 3. **The defect was mine, in the very edit that records the ratification.** | All numeric spans removed from EPR-001. It now speaks in segment identifiers only, and defers every figure to this report. `V-3` back to 0 |
| **VD-2** | A consequence record was drafted with `disposition: AWAITING_EXECUTIVE_INPUT`, which **inflated V-6's census from 29 to 30 without any Executive field being empty** | Token changed to `AWAITING_EXECUTIVE_DECLARATION`, with the reason recorded in the file. `V-6` back to 29 |

**VD-2 is worth more than its size.** `AWAITING_EXECUTIVE_INPUT` is not a word, it is a
**census marker**. Any future author who uses it as ordinary prose will move a governed count
without touching a governed field.

### 1.2 A defect in the validator itself — not corrected, reported

`epr_validate.py` will not run from the repository. Its `sys.argv` fallback points at
`/home/claude/work/epr/…` and `/mnt/user-data/uploads/…` — **paths in an authoring environment
that no longer exists.**

```
FileNotFoundError: '/home/claude/work/epr/EMOTIONAL_PROGRESSION_REGISTRY.yaml'
```

It runs correctly when both paths are passed explicitly, which is how this report's table was
produced. **Fixing the default is a code change and is not authorized by the Order. Registered
here so the next person to run it does not conclude the registry is missing.**

---

## 2 · The measurements EPR-001 must not carry

`timecodes` is a prohibited field of EPR-001. These figures live here so the registry can cite
them without holding them.

**Governed production runtime — `Alpha RoundUp 2026 · Day 2 Episodic Trilogy (08-24 Lineage)`:**

```
Info.fcpxml  1ab3d12f0dd150c63907a4b2e4bac4253baf8100910dfda74daa3a5378b6b4d2   4689.500 s  = 78:09.500
audio        4b43968a0f9d4f06c5e441de10b060a797e4bf26e2f52597d7dc993978617fe2   4689.557 s
```

**Every `TIMELINE_REGISTRY` v1.0.0 segment against that runtime.** Spans below are positions in
the **superseded 08-22 assembly** and are **not** positions in the governed production. They are
listed to locate the two that fall out of range, nothing more.

| seg | span (superseded assembly) | activity | status vs governed runtime |
|---|---|---|---|
| S01 | 00:00–01:13 | cold_open | within range |
| S02 | 01:13–01:51 | host_day_brief | within range |
| S03 | 01:51–27:02 | interview_gauntlet_1 | within range |
| S04 | 27:02–27:23 | ride_brief | within range |
| S05 | 27:40–29:10 | escort_ride | within range |
| S06 | 31:43–32:33 | librarian_speech | within range |
| S07 | 32:45–33:50 | council_profile | within range |
| S08 | 33:51–35:56 | town_proclamation | within range |
| S09 | 36:03–36:30 | first_ride_moment | within range |
| S10 | 36:59–38:52 | state_proclamation | within range |
| S11 | 38:55–52:00 | interview_gauntlet_2 | within range |
| S12 | 52:04–53:56 | organizer_honors_and_silence | within range |
| S13 | 53:50–54:35 | group_photo | within range |
| S14 | 54:36–55:24 | service_wrap_preview | within range |
| S15 | 56:10–58:43 | riding_music_passage | within range |
| S16 | 58:43–66:25 | bike_night_arrivals | within range |
| S17 | 66:25–66:48 | audience_cta | within range |
| **S18** | **69:25–79:40** | bike_night_ambience | **END out of range by 90.500 s** |
| **S19** | **79:44–80:46** | friday_wrap_part3_tease | **ENTIRELY out of range** |

**"Within range" means only that the arithmetic does not place the span past the end of the
governed runtime.** It is **not** a statement that the segment is correctly positioned in the
governed production — the two timelines diverge at `00:03:27.208` and are related by five
distinct piecewise lags. **Sixteen of these eighteen spans are unverified, not verified.**

---

## 3 · Why every criterion passes while `EPR-07` is broken

```
EPR-07 · beat Ride_Home · segment_refs [S19]

  V-2 asks:  does S19 exist in TIMELINE_REGISTRY v1.0.0?          -> YES.  PASS.
  Reality:   does S19 exist in the governed 08-24 production?     -> NO.
```

**The validator's reference and the registry's subject are no longer the same film.** `V-2` was
built to catch an EPR entry pointing at a segment the authority does not contain. It cannot
catch an authority that has itself been superseded, because **nothing in the authority says so.**

This is the `ER-003` failure class in a new place. `ER-003` arose because a report labelled
*"every shot, authoritative"* showed 214 of 1025 elements — a true statement about a filtered
view, presented as a statement about the whole. **`V-2 PASS` is the same shape:** true about
`TIMELINE_REGISTRY v1.0.0`, and not true about the production.

### 3.1 What `IR-002` predicted, and what actually happened

`IR-002` §4.1 wrote: *"`V-2` catches an unresolvable `segment_ref` — but `V-2` only reports. It
does not say what to do."*

**That understated it.** The failure mode was not that `V-2` would report and fall silent. It is
that **`V-2` does not report at all.** The prediction assumed the segment authority would be
re-derived before the mismatch mattered. Under the Order's §4 suspension, the ratification lands
first and the re-derivation waits — so for the whole of that interval the validator is
authoritative-looking and blind.

---

## 4 · What would have to be true for a validator to catch this

**Stated as engineering analysis. Not implemented — implementation is not authorized.**

| # | requirement |
|---|---|
| **R-1** | The segment authority must **declare which production it describes**. `TIMELINE_REGISTRY` v1.0.0 carries `sources.runtime_lock_s: 4846.625` but no production identifier — so it cannot be compared against a ratified production identity |
| **R-2** | A validator must **compare the authority's production against the registry's production**, and fail when they differ. Today neither artifact states one in a form the other could read |
| **R-3** | Segment spans must be **bounds-checked against the governed runtime**. §2's table is that check, run by hand for this report — no committed script performs it |
| **R-4** | `V-2 PASS` must be reportable as **`INDETERMINATE`** when the authority is flagged `SUPERSEDED_PENDING_REDERIVATION`, which EPR-001 v1.2.0 now sets. **A validator that cannot say "I do not know" will say "PASS" instead** |

**R-4 is the general lesson and outlives this production.** Every criterion in this suite is
binary. None can express *"my reference is stale."*

---

## 5 · Consequences recorded in EPR-001 v1.2.0

Processed under Order §2.4 — **reported, none repaired, no replacement content inferred.**

| id | condition | disposition | owner |
|---|---|---|---|
| **PBC-1** | `EPR-07`'s segment reference is unresolvable in the governed production | `UNRESOLVED_PENDING_EXECUTIVE` | **Executive** |
| **PBC-2** | `S18`'s declared end falls outside the governed runtime by 90.500 s | `BOUNDARY_OUT_OF_RANGE_PENDING_REDERIVATION` | platform, after regeneration is authorized |
| **PBC-3** | no segment-to-episode assignment exists, and none is derivable without inference | `NOT_DERIVABLE_WITHOUT_REGENERATION` | platform, after regeneration is authorized |
| **PBC-4** | intensity-scale ordinality still undeclared | `AWAITING_EXECUTIVE_DECLARATION` | **Executive** |
| **PBC-5** | precondition contract still unsatisfiable (`IR-002 I1`) | `RAISED_NOT_RESOLVED` | **Executive** |

### 5.1 On `EPR-07` specifically

**Nothing was done to it.** It was not deleted, not re-keyed to another segment, not folded into
`EPR-06`, and its `beat: Ride_Home` and `audience_state: Completion` — both `EXECUTIVE` custody —
stand exactly as declared. `missing_data_policy: propagate_unknown` was applied as written: **the
unknown is propagated.**

Order §2.4: *"Do not infer replacement narrative content."* **None was inferred.** Whether
`Ride_Home` survives into the trilogy, migrates, or retires is Executive work, and it is asked as
an explicit question in the Authoring Workbook rather than assumed either way.

### 5.2 On `PBC-3`, which is the one that will bite next

The Order calls `S01–S18` *"active episodic segments."* **No segment-to-episode assignment
exists.** `DAY2_PARENT_FORENSIC_AUDIT` establishes which contiguous Parent region each Part body
is drawn from —

```
Part 1 body  ->  Parent 00:00:00.000 - 00:27:13.083
Part 2 body  ->  Parent 00:27:13.630 - 00:53:32.541
Part 3 body  ->  Parent 00:53:33.430 - 01:18:05.113
```

— but placing `S01…S18` inside those regions needs each segment's position **in the 08-24
Parent**, which does not exist anywhere. The only positions on record are the superseded
assembly's, and the two timelines are related by five distinct piecewise lags with unmatched
regions after roughly `01:04`. **Any episode assignment produced today would be inference. None
was produced.**

**The Authoring Workbook therefore does not ask the Executive to author per-episode intent, and
does not present segments grouped by episode.** Doing either would smuggle an assignment the
platform is not entitled to make.

---

## 6 · Verification of the v1.2.0 edit

Parse-and-compare against v1.1.0, run before the file was written back:

```
entries                                    7 -> 7
executive-custody fields altered           0
  (beat · segment_refs · dramatic_intensity · audience_state ·
   governing_theme · editorial_transition · executive_notes · provenance)
AWAITING_EXECUTIVE_INPUT in entries        28 -> 28    (29 including intensity_scale.ordered)
governing_invariants                       unchanged
prohibited_fields                          unchanged
intensity_scale.categories                 unchanged
undeclared_segments                        ['S04','S17']  unchanged
```

**No Executive value was authored, inferred, extended, suggested or defaulted.** The increment
records a ratification and processes a consequence; it declares nothing.

### 6.1 The version increment arms a trigger that must not fire

The ratification order §4.5 makes a `registry_version` increment **the regeneration trigger**.
§4 of the 2026-08-28 Order suspends regeneration until the workbook is complete and EPR-001 is
ratified.

> **v1.2.0 therefore arms a trigger that is held shut by a later Order.**

Recorded in the registry and here rather than avoided by declining to bump the version — **an
unbumped version would have been a silent change, which is worse than an armed trigger that is
documented.** `IR-002` Q3 anticipated this increment; it did not anticipate it landing during a
suspension.

---

## 7 · Standing state

```
production_identity              RATIFIED   Path B, 2026-08-28
EPR-001                          v1.2.0     structurally valid; content unratified
EPR-001 content ratification     PENDING    awaits the Executive Authoring Workbook
segment authority                SUPERSEDED_PENDING_REDERIVATION
gen_artifacts.py                 LOCKED     RUN_ID lock held by Order section 4
downstream regeneration          SUSPENDED
registry population              NOT PERFORMED
Conductor Score generation       NOT PERFORMED
```

*Custody `MACHINE`. Two defects of my own making found and corrected (VD-1, VD-2); one defect in
the validator reported and not corrected. Six criteria PASS, and §3 explains why that is not the
same as EPR-001 being correct for this production.*
