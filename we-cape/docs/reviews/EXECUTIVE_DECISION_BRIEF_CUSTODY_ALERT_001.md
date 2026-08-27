# EXECUTIVE DECISION BRIEF — `CUSTODY_ALERT_001` §5

**Task Order:** Prepare an Executive Decision Brief for `CUSTODY_ALERT_001` §5
**Authority:** Executive Producer / Chairman · **Priority:** CRITICAL
**Custody:** `ANALYSIS ONLY` · **Prepared:** 2026-08-26
**Constraint honoured:** **No disposition is recommended. No path is preferred, scored, or ranked.**
No code, registry, or commit was changed in producing this brief.

**Status:** **ACCEPTED** as the official Executive Decision Brief for `CUSTODY_ALERT_001`,
Executive Producer / Chairman, 2026-08-26.
**Amended:** `AMENDMENT 1`, 2026-08-26 — see below.

---

## AMENDMENT 1 — 2026-08-26 · `Q2` CLOSED by Executive Order

**Amendment, not revision. Nothing in the original brief is deleted or rewritten.** What follows
is what the Executive has since declared, and where in the brief that declaration lands. Affected
passages below are **annotated in place and left standing**, so the brief continues to read as it
did when it was accepted.

**Source:** *EXECUTIVE ORDER — `CUSTODY_ALERT_001` §5 (INTERIM CLARIFICATION)*, Executive
Producer / Chairman, 2026-08-26, **BINDING (LIMITED SCOPE)**. Transcribed in full at
`docs/rulings/EXECUTIVE_ORDER_2026-08-26_CUSTODY_ALERT_001_INTERIM_CLARIFICATION.md`.

### What the Order declares

| # | declaration |
|---|---|
| **D1** | **Day 2 Part 1 is the published public release.** |
| **D2** | **Day 2 Part 2 is a scheduled public YouTube Premiere.** |
| **D3** | **Day 2 Part 3 is a scheduled public YouTube Premiere.** |
| **D4** | The three Parts constitute the **authoritative public distribution deliverables** for Alpha RoundUp 2026 Day 2 — `three_parts_status: DISTRIBUTION_DELIVERABLES` |
| **D5** | The ≈80-minute Parent timeline is an **assembly artifact** used in creating the serialized releases |
| **D6** | The governed record **shall explicitly distinguish** *assembly assets* (internal editorial lineage) from *public distribution assets* (released deliverables) |

### What the Order expressly does **not** do

> *"This clarification establishes the role of each asset only. It does not determine production
> lineage, custody precedence, or regeneration authority."*

It does not determine whether a later cut exists · does not select Path A, B or C · does not
authorize registry regeneration or re-keying · does not modify custody precedence · does not
alter any governed registry. **The platform is not authorized to infer additional custody
implications from it, and has not.**

### Effect on this brief

| brief location | effect |
|---|---|
| **§8.1 `Q2`** | **CLOSED.** Answer recorded verbatim |
| **§8.1 `Q1`** | **OPEN.** Reserved to a separate Executive ruling |
| **§8.2** | the observation stands as written; its concluding uncertainty is **overtaken** — annotated in place |
| **§7**, row *"status of the three Parts"* | **overtaken by D4 and reserved** — annotated in place, **not re-derived** |
| **§C.4 item C-2** | **ANSWERED by D4/D5** |
| **§9** decision record | `Q2` fields populated with the Executive's own words, transcribed. **Every other field remains blank** |
| **everything else** | **unchanged.** No path analysis was re-run; §4, §5, §6 and the remainder of §7 stand exactly as accepted |

**Five questions the Order's text raises and does not settle** — including its own governance
class, and how D6's two roles relate to any future four-token classification — are recorded in
§5 of the Order transcription. **They are questions. None is answered there or here.**

---

## 0 · What this document is, and what it deliberately is not

This is a **decision package**, not an argument. Every path below is presented on the same
template, at the same depth, with its costs and its benefits stated in the same voice. Where a
path carries a consequence the others do not, that consequence is named — **naming an asymmetry
is not recommending against it**, and several of the sharpest asymmetries in this brief cut in
directions that a reader might not expect.

**Section 8 is the section to read if you read only one.** It sets out what this brief cannot
tell you, where the three-path framing may itself be doing work, and the two questions whose
answers would change the shape of the decision — neither of which the platform holds.

---

## 1 · The decision in one page

### 1.1 The two artifacts

| | **08-22 Lock** | **08-24 Cut** |
|---|---|---|
| runtime | **4846.625 s** (01:20:46.625) | **4689.500 s** fcpxml · **4689.557 s** audio (01:18:09.557) |
| primary-spine elements | 191 | **201** |
| all resolved elements | 1025 | 1096 |
| titles | 57 | **65** |
| transitions | 180 | 178 |
| FCPXML sha256 | `2bf06853…58e7` | `1ab3d12f…b4d2` |
| SRT sha256 | `89d61f96…a1c6b` (2291 cues) | `2a16dd70…3869` (2036 cues) |
| viewing master | `89e911b1…cd46`, **APPROVED** | none designated |
| status in the record | governed production | **`AWAITING_EXECUTIVE_DISPOSITION`** |

The two cuts are **identical to the millisecond for the first 26 primary-spine elements —
`00:00:00` to `00:03:27.208`.** Everything after that point differs. The 08-24 cut is
**157.125 s shorter and carries ten more primary elements.** *That is a re-edit, not a trim.*

### 1.2 What the forensic audit added (2026-08-26)

`DAY2_PARENT_FORENSIC_AUDIT.md` established three facts that bear directly on §5:

1. **The 08-24 lineage has a downstream product.** Three extracts — `Day 2 Part 1/2/3` — tile
   the 08-24 Parent end to end, in order, with no internal edits. Each carries a
   **73.800 s re-prepended opening** and a **15–20 s appended tail**. Each ships with a
   `-Cover.jpg`.
2. **The 08-24 audio is not the Approved Viewing Master.** It matches the AVM only in five
   piecewise-shifted blocks (lags `0.000`, `−3.500`, `+27.710`, `+28.960`, `+119.540` s) with
   **no match at any lag after ≈ 01:04:00.**
3. **One `CUSTODY_ALERT_001` §1 item is resolved.** `Analysis_Day_2_Part_1_video.WAV` is
   byte-identical to `Day 2 Part 1.WAV`. It is an extract, not an unexplained program.

**Fact 1 is the one that changes the §5 landscape**, and §8.2 returns to it.

### 1.3 The rule that governs whichever way you rule

> **`SOP-06 B2`** — *"Any picture change during this window voids the lock: return to A1
> (re-export, re-audit). Deltas explained, always."*

Recorded in the gate's own `sop06_placement.caution`. **This is a Phase-B custody event.** The
three paths differ in *what the picture change is held to be*, not in whether the rule applies.

---

## 2 · The dependency surface — what the ruling actually touches

Measured from the repository, not recalled. **186 tracked `.yaml` / `.md` / `.json` documents;
31 of them cite one of the four governed input hashes or the lock runtime; within the
intelligence layer and the DWR, 29 artifacts carry time-bearing values.**

### 2.1 Five dependency classes

| class | what binds it to a cut | artifacts |
|---|---|---|
| **T — timecode-bound** | values are positions in one specific edit | `CONDUCTOR_SCORE` · `EDITORIAL_SYNCHRONIZATION` · `VISUAL_EVENT_REGISTRY` · `CAPTION_REGISTRY` · `STEP0_TIMING_CLOSURE` · `ESS_VALIDATION_REPORT` · `PRODUCTION_INTELLIGENCE_SEED` · `MUSIC_OVERLAY_TIMELINE` · `VOICE_PRIORITY_MAP` · `BEHAVIORAL_FINGERPRINT` · `CUE_SHEET` · `CUE_SHEET_v1.1` · `TIMELINE_REGISTRY` · `VOICE_OVER_REGISTRY` · `DOCUMENTARY_PROGRESSION` · `QUOTE_LIBRARY` · `WHY_I_RIDE_REGISTRY` · `APPROVED_VIEWING_MASTER` · `MIE_INPUT_PACKAGE` · `EVS-001` · `EMB-CUE-03 skeleton` |
| **X — SRT-cue-index-bound** | cite `#NNNN` positions in the GT-2 caption stream | `RIDER_REGISTRY` (80 citations) · `MOTORCYCLE_REGISTRY` (6) · `ORGANIZATION_REGISTRY` (3) · `PROMPT_REGISTRY` (2) |
| **S — segment-keyed** | survive iff the `S01…S19` **ID set** survives | `EMOTIONAL_PROGRESSION_REGISTRY` (EPR-001) · `EMOTIONAL_ARC` (superseded) · `ENERGY_CURVE` |
| **I — cut-independent** | doctrine, rulings, specs, standards | `DOC-001/002/003` · `DOC-SRC-001` · `DOC-CAND-001` · `VPD-001` · `EXECUTIVE_RULINGS` v1.5.0 · `ADR-009` · `AIS-001` · all `WET-SPEC-*` · `SOP-04/05/06` · `WET-SPEC-GATE-001` · `DWR-001` · `CAR-001/003/004` |
| **H — historical by design** | records of a moment; never re-pointed | `RE-001` META/SCORECARD/narrative · `CUSTODY_ALERT_001` · `DAY2_PARENT_FORENSIC_AUDIT` · `PR-001` · `IR-001` · `IR-002` · all four `PDR-2026-08-22-ESS-*` |

### 2.2 The heaviest time-bearing artifacts, by count of time values

```
VOICE_PRIORITY_MAP.yaml        1564        CAPTION_REGISTRY.yaml           115
VISUAL_EVENT_REGISTRY.yaml      206        EDITORIAL_SYNCHRONIZATION.yaml  105
CONDUCTOR_SCORE.yaml            121        STEP0_TIMING_CLOSURE.md          94
MUSIC_OVERLAY_TIMELINE.yaml      85        RIDER_REGISTRY.yaml              80
WHY_I_RIDE_REGISTRY.yaml         66        TIMELINE_REGISTRY.yaml           41
BEHAVIORAL_FINGERPRINT.yaml      30        CUE_SHEET(+v1.1).yaml            64
```

### 2.3 The regeneration boundary — what a machine can rebuild, and what it cannot

| | artifacts | mechanism |
|---|---|---|
| **machine-regenerable** | **7** — `STEP0_TIMING_CLOSURE` · `CAPTION_REGISTRY` · `VISUAL_EVENT_REGISTRY` · `EDITORIAL_SYNCHRONIZATION` · `CONDUCTOR_SCORE` · `ESS_VALIDATION_REPORT` · `PRODUCTION_INTELLIGENCE_SEED` | `gen_artifacts.py`, one atomic run, from FCPXML + SRT + ETC |
| **script-assisted** | 3 — `VOICE_PRIORITY_MAP` · `MUSIC_OVERLAY_TIMELINE` · `BEHAVIORAL_FINGERPRINT` | dedicated generators committed at `intelligence/p2/mie/scripts/`; inputs must be re-pinned |
| **hand-authored, no generator** | **the rest of class T and all of class X** — `TIMELINE_REGISTRY`, `VOICE_OVER_REGISTRY`, `DOCUMENTARY_PROGRESSION`, `QUOTE_LIBRARY`, `RIDER_REGISTRY`, `WHY_I_RIDE_REGISTRY`, `MOTORCYCLE_REGISTRY`, `ORGANIZATION_REGISTRY`, `PROMPT_REGISTRY`, `CUE_SHEET*`, `EVS-001` | re-derivation is human work |

**This boundary is the single largest cost driver among the three paths, and it is not visible
from the artifact list.** Seven files rebuild themselves. Roughly a dozen do not.

### 2.4 One arithmetic consequence that is already determined

`TIMELINE_REGISTRY` declares **S19 `Ride_Home` at span `79:44–80:46`** and **S18 ending at
`79:40`**. The 08-24 cut ends at **`78:09.5`**.

> **S19 lies entirely outside the 08-24 runtime. S18's declared end lies outside it.**

And in `EMOTIONAL_PROGRESSION_REGISTRY`:

```
EPR-07   beat: Ride_Home    segment_refs: [S19]          <-- sole anchor
EPR-06   beat: Celebration  segment_refs: [S13,S14,S15,S16,S18]
```

**`EPR-07` is an Executive-custody declaration whose only anchor is a segment that does not
exist in the 08-24 cut.** `V-2` detects the unresolvable reference — **but `V-2` only reports.
It does not say what to do, and under order §2.3 the platform may not author, infer, or default
a replacement.** This was raised in `IR-002` §4.1 as a hypothetical. It is no longer
hypothetical; it is arithmetic.

Eight further artifacts declare positions beyond `78:09.5`: `EDITORIAL_SYNCHRONIZATION`,
`CUE_SHEET`, `CUE_SHEET_v1.1`, `VOICE_PRIORITY_MAP`, `DOCUMENTARY_PROGRESSION`,
`VOICE_OVER_REGISTRY` (VO04), `QUOTE_LIBRARY` (`t: 80:38`), `PROMPT_REGISTRY` (`80:22`).

---

# PATH A — the 08-22 Lock remains the Production

*The 08-24 cut is a working export. The governed record stands.*

## A.1 Operational consequences

**Registry impact**

| registry | effect |
|---|---|
| `APPROVED_VIEWING_MASTER` v1.0.0 | **one addition** — the 08-24 assets are entered under `reference_only` with `editorial_conformance: NON_CONFORMANT`, `delta_vs_lock_s: 157.125`, `hazard: HIGH`. This is the register's designed purpose; it already carries six such entries |
| all other registries | **untouched.** No version bump, no re-derivation, no re-pin |
| `TIMELINE_REGISTRY` | **one correction unrelated to the ruling** — its `delta_note` still claims a ±6 s segment tolerance *"until Sprint lock-SRT reconciliation."* Step 0 closed that reconciliation at offset 0.000 s. The note is stale under every path, and is listed here because A is the only path in which it would otherwise go unnoticed |

**Regeneration impact — none.** No artifact regenerates. `gen_artifacts.py` is not run. The
gate's `on_open` regeneration remains keyed to the ESS disposition sequence, not to this ruling.

**Custody implications**

- `SOP-06 B2` is satisfied by **declaring that no picture change occurred to the governed
  production** — the 08-24 file is a divergent export outside the lock's custody chain.
- `RE-001`'s four input hashes continue to describe the production. `reference_status: ACTIVE`
  is unchanged.
- The **08-24 lineage acquires a custody status it does not currently have**: `REFERENCE_ONLY`.
  Today it has none, which is why it was reachable by a work order.
- **The three Parts inherit that status.** They become reference extracts of a reference cut.

**Downstream artifact effects — nil.** `CONDUCTOR_SCORE` v1.1.0, `EDITORIAL_SYNCHRONIZATION`
v1.1.0, `CAPTION_REGISTRY` 0.2.1, `VISUAL_EVENT_REGISTRY` 1.0.1, `VOICE_PRIORITY_MAP`,
`MUSIC_OVERLAY_TIMELINE`, `BEHAVIORAL_FINGERPRINT`, `EPR-001`, `EVS-001`, `ESS-002` and the gate
all continue exactly as they stand. **`ESS-002`'s boundary at `00:29:10.000` remains a live
question about a live picture.**

## A.2 Risks

| # | risk |
|---|---|
| **A-R1** | **The ruling may be describing an edit that has already moved on.** The 08-24 cut is dated two days after the lock and carries eight more titles — the direction of travel is forward. If a 08-26 or later cut exists, Path A rules on the wrong pair |
| **A-R2** | **Look-alike exposure is reduced but not removed.** `APPROVED_VIEWING_MASTER` already records two `hazard: HIGH` 12 GB 4K renders whose filenames differ from the approved master by three characters. Adding a seventh reference entry does not shrink that surface — it documents it |
| **A-R3** | **The Parts become orphans.** Three extracts with cover art, tiling a `REFERENCE_ONLY` cut, would have a distribution shape and no governed status. Nothing in the platform stops someone treating them as deliverables |
| **A-R4** | **Effort already spent on the 08-24 lineage is not recoverable into the record.** The forensic audit's measurements remain historical observation and never become governed values |
| **A-R5** | **The stale `TIMELINE_REGISTRY` tolerance note persists** unless corrected as a follow-on |

## A.3 Benefits

| # | benefit |
|---|---|
| **A-B1** | **Zero regeneration.** No artifact is rebuilt, so no artifact can be rebuilt wrongly |
| **A-B2** | **The Approved Viewing Master survives.** `89e911b1…`, `CONFORMANT` to the millisecond, is the only render in the tree with that property, and `EVS-001` is prepared against it |
| **A-B3** | **`ESS-002` / `EVS-001` proceed immediately.** The gate's disposition sequence resumes at step 2 with no re-scoping |
| **A-B4** | **`EPR-07` keeps its anchor.** `S19` exists; the Executive's seven declarations all resolve; the 29 empty fields stay exactly where they are |
| **A-B5** | **`RE-001` remains a live baseline rather than a historical one**, and `RE-ARCHIVE-01` / `D-26` keep their planned remedy window at RE-002 |
| **A-B6** | **Cheapest to reverse.** A later ruling to path B or C costs the same as ruling B or C today, plus the reference entry |

## A.4 Required follow-on actions

| # | action | owner |
|---|---|---|
| A-1 | Enter the 08-24 assets in `APPROVED_VIEWING_MASTER` under `reference_only`, `NON_CONFORMANT`, `delta_vs_lock_s: 157.125`, `hazard: HIGH`, with the fcpxml/SRT/m4a hashes | platform |
| A-2 | Enter the three Parts as `REFERENCE_ONLY` extracts of that entry, citing `DAY2_PARENT_FORENSIC_AUDIT` | platform |
| A-3 | Amend `CUSTODY_ALERT_001` §1 for the resolved `Analysis_Day_2_Part_1_video.WAV` identification | platform |
| A-4 | Correct `TIMELINE_REGISTRY`'s stale `delta_note` | platform |
| A-5 | Resume the gate at step 2 — `ESS-002` via `EVS-001` | **Executive** |
| A-6 | Record whether any cut later than 08-24 exists (see §8.1 Q1) | **Executive** |

## A.5 Authoritative under Path A

**Everything currently in the record, unchanged.** Classes T, X, S, I all remain authoritative:
the seven ESS artifacts, all fourteen p2 registries, `EPR-001` v1.1.0, `APPROVED_VIEWING_MASTER`
v1.0.0 (v1.1.0 after A-1/A-2), `EXECUTIVE_RULINGS` v1.5.0, all doctrine, `RE-001`, the gate at
v1.3.0, the 49-entry `DEFERRED_WORK_REGISTER`.

## A.6 `REFERENCE_ONLY` under Path A

```
08-24 Info.fcpxml                 1ab3d12f…b4d2   4689.500 s
08-24 SRT                         2a16dd70…3869   2036 cues
08-24 m4a                         fd78b5a2…8173   4689.557 s
PARENT m4a (ANALYSIS folder)      4b43968a…4f06   4689.557 s
PARENT SRT                        80a8ed25…62b4   5664 cues
Day 2 Part 1 WAV / SRT            bcc17b2b… / c057fccf…
Day 2 Part 2 WAV / SRT            a9416a6f… / 65a313bc…
Day 2 Part 3 WAV / SRT            1badf1c3… / 96bbee5d…
DAY2_PARENT_FORENSIC_AUDIT.md     observational record of a REFERENCE_ONLY lineage
```

---

# PATH B — the 08-24 Cut becomes the Production

*The lock is void under `SOP-06 B2`. The record is rebuilt against the new picture.*

## B.1 Operational consequences

**Registry impact — the largest of the three paths, and unevenly distributed.**

| registry | effect |
|---|---|
| `APPROVED_VIEWING_MASTER` | **invalidated as a designation.** `89e911b1…` at 4846.625 s is no longer conformant to the governed lock. **A new master must be exported and designated; there is no conformant 4K render of the 08-24 cut in the tree today.** Until one exists, **no Executive Viewing Session can be held** — the register's own rule is that a render absent from it is not approved, and silence is not approval |
| `TIMELINE_REGISTRY` | **full re-derivation.** All nineteen segment spans move. **`S19` and part of `S18` cease to exist** (§2.4). Whether the *ID set* survives is not a platform decision |
| `CAPTION_REGISTRY` · `VISUAL_EVENT_REGISTRY` | regenerate from the new FCPXML + SRT (machine) |
| `VOICE_OVER_REGISTRY` · `DOCUMENTARY_PROGRESSION` · `QUOTE_LIBRARY` · `ENERGY_CURVE` | hand re-derivation; VO04, P5's end, and `t: 80:38` are outside the new runtime |
| `RIDER` · `MOTORCYCLE` · `ORGANIZATION` · `PROMPT` | **91 SRT cue-index citations re-point.** The 08-24 SRT holds 2036 cues against the lock's 2291. **`#1420` is a different sentence in the new stream.** This class fails *silently* — a cue index is always resolvable and never raises an error |
| `EMOTIONAL_PROGRESSION_REGISTRY` | **`EPR-07` loses its sole anchor.** `V-2` reports; nothing may fill it (order §2.3). **Only the Executive can re-key or retire that beat** |

**Regeneration impact**

- **One atomic `gen_artifacts.py` run** rebuilds seven artifacts — after the new FCPXML, SRT and
  ETC are hashed and pinned. `DOC-002`: regenerate, never patch. Partial regeneration is the
  state that doctrine exists to prevent.
- `VOICE_PRIORITY_MAP` (1564 time values), `MUSIC_OVERLAY_TIMELINE`, `BEHAVIORAL_FINGERPRINT`
  re-run against new inputs.
- **`fcpx_resolve.py` must be re-validated before it is trusted on the new XML.** It is validated
  191/191 against the *lock's* ETC. `DOC-001`: validate the instrument before the measurement.
  **There is no ETC for the 08-24 cut** — one must be produced, and the resolver re-validated
  against it. *This is a prerequisite, not a step.*
- The hand-authored class in §2.3 has **no generator at all.**

**Custody implications**

- `SOP-06 B2` fires in full: **return to A1 — re-export, re-audit, re-hash.** `GATE-1` timeline
  custody audit is re-run.
- `RE-001` becomes a **historical baseline of a superseded cut** — which is precisely what a
  Reference Execution is for. `reference_status` moves `ACTIVE → SUPERSEDED`; nothing in it is
  edited (`DOC-002`, and RE-001's own immutability clause).
- **`RE-ARCHIVE-01` becomes urgent rather than deferred.** RE-001 holds no copy of the artifacts
  its scorecard describes; they are recoverable only from commit `b197e74`. Under Path B the
  live paths are overwritten and that recovery route becomes the *only* route.
- Every `EXECUTIVE` -custody value keyed to a moved or vanished segment must be **re-declared by
  the Executive.** The platform may not carry it forward and may not infer it.

**Downstream artifact effects**

`ESS-001`, `ESS-002` and `ESS-003` are all **re-scoped to a different picture**. `ESS-002`'s
boundary at `00:29:10.000` may not exist in the new cut — `CUSTODY_ALERT_001` §2 already showed
the escort sequence has moved and that `SIL-02`'s `00:52:04.000` boundary lands on an unrelated
clip. `EVS-001` is void until a new master is designated. `EMB-CUE-03`, `CUE_SHEET`,
`CUE_SHEET_v1.1` and `MIE_INPUT_PACKAGE` all re-derive.

## B.2 Risks

| # | risk |
|---|---|
| **B-R1** | **Silent failure of the 91 cue-index citations.** A wrong timecode is caught by a validator; a wrong cue index is not. This is the highest-severity technical risk on any path because it produces confident, wrong attributions of quotes and riders |
| **B-R2** | **`EPR-07` and any re-keyed segment force Executive re-declaration.** The volume of that work is not knowable until the new segment set exists |
| **B-R3** | **No conformant viewing master exists yet.** Executive judgement in timecode is blocked until one is exported and validated |
| **B-R4** | **The resolver is unvalidated on the new XML and there is no ETC to validate it against.** Producing an ETC is itself the largest single engineering item on this path |
| **B-R5** | **Re-edit recurrence.** If the picture moved once on 08-24 it can move again; Path B pays the full cost each time and has no mechanism that makes the second time cheaper |
| **B-R6** | **`RE-ARCHIVE-01` escalates.** The pre-ruling artifacts survive only in git history |
| **B-R7** | **Hand-authored registries carry the largest re-derivation cost and the least tooling** — RIDER (80 entries), WHY_I_RIDE (66), QUOTE (12), TIMELINE (19) |

## B.3 Benefits

| # | benefit |
|---|---|
| **B-B1** | **The governed record describes the film that is actually being made.** Every downstream artifact becomes true of the current picture rather than of a superseded one |
| **B-B2** | **`RE-001` does the job it was designed for.** Superseding it is not a loss of a baseline; it is the first exercise of the baseline mechanism, and the RE-001 → RE-002 delta becomes a documented record of a real editorial change |
| **B-B3** | **One custody event, ruled once.** The ambiguity that has been open across three work orders closes, and no future work order can reach an ungoverned cut |
| **B-B4** | **The 08-24 cut carries more editorial material** — ten more primary elements and eight more titles — which becomes governed rather than invisible |
| **B-B5** | **The three Parts acquire a legitimate parent**, and the forensic audit's measurements become governed values rather than reference observation |
| **B-B6** | **`RE-ARCHIVE-01` and `D-26` get fixed** — RE-002's archival is their planned remedy window, and Path B forces that window open now |

## B.4 Required follow-on actions

**Ordered by dependency. Items 1–4 are prerequisites, not steps.**

| # | action | owner |
|---|---|---|
| B-1 | Re-export the picture and record `GATE-1` timeline custody audit (`SOP-06 A1→A4`) | production |
| B-2 | Hash the new FCPXML, SRT, MP4 and produce a **new Editorial Timing Contract** | platform |
| B-3 | **Re-validate `fcpx_resolve.py` against the new ETC** before any measurement (`DOC-001`) | platform |
| B-4 | Export and designate a **new Approved Viewing Master**, conformant to the millisecond | platform + **Executive** |
| B-5 | One atomic `gen_artifacts.py` run under one `RUN_ID` — seven artifacts | platform |
| B-6 | Re-derive `TIMELINE_REGISTRY`; **submit the new segment ID set for Executive ratification** | platform → **Executive** |
| B-7 | Re-point or retire all **91** cue-index citations; record the method | platform |
| B-8 | Re-derive `VOICE_PRIORITY_MAP`, `MUSIC_OVERLAY_TIMELINE`, `BEHAVIORAL_FINGERPRINT`, `CUE_SHEET*`, `MIE_INPUT_PACKAGE` | platform |
| B-9 | **Executive re-declaration of `EPR-07` and every EPR entry whose `segment_refs` no longer resolve** | **Executive only** |
| B-10 | Archive RE-002 with the RE-001 delta categorized; remedy `RE-ARCHIVE-01`; carry the `D-26` fix | platform |
| B-11 | Re-scope `ESS-001`, `ESS-002`, `ESS-003`; re-prepare `EVS-001` | platform → **Executive** |
| B-12 | Set `RE-001.reference_status: SUPERSEDED` — **without editing anything else in it** | platform |

## B.5 Authoritative under Path B

**After B-1 … B-12 complete — not before:**

- the regenerated seven, at new versions, pinned to the new four hashes
- the re-derived `TIMELINE_REGISTRY` **once the Executive has ratified its segment ID set**
- the re-derived class-T and class-X registries
- `EPR-001` **only after the Executive re-declares the entries that lost their anchors**
- a newly designated Approved Viewing Master
- **class I in full, unchanged** — all doctrine, `EXECUTIVE_RULINGS` v1.5.0, `ADR-009`, every
  `WET-SPEC`, `SOP-06`, the gate standard. **No governance instrument is disturbed by this
  path.** Only measurements are

**During B-1 … B-12 the production has no authoritative timeline artifacts at all.** That
interval is the real cost of Path B and it should be planned for, not discovered.

## B.6 `REFERENCE_ONLY` under Path B

```
08-22 lock FCPXML                 2bf06853…58e7    4846.625 s
08-22 lock SRT ("SRT 2")          89d61f96…a1c6b   2291 cues
P2_LOCK_timing.json (ETC)         e91318a6…010d
Filmage_Editor.mp4 (RE-001 proxy) a53655fc…f47e
Approved Viewing Master           89e911b1…cd46    4846.625 s   <- ceases to be APPROVED
CONDUCTOR_SCORE v1.1.0 · EDITORIAL_SYNCHRONIZATION v1.1.0
CAPTION_REGISTRY 0.2.1 · VISUAL_EVENT_REGISTRY 1.0.1
STEP0_TIMING_CLOSURE · ESS_VALIDATION_REPORT · PRODUCTION_INTELLIGENCE_SEED
VOICE_PRIORITY_MAP · MUSIC_OVERLAY_TIMELINE · BEHAVIORAL_FINGERPRINT
CUE_SHEET · CUE_SHEET_v1.1 · MIE_INPUT_PACKAGE · EVS-001
TIMELINE_REGISTRY 1.0.0 · VOICE_OVER_REGISTRY · DOCUMENTARY_PROGRESSION
QUOTE_LIBRARY · ENERGY_CURVE · RIDER · MOTORCYCLE · ORGANIZATION · WHY_I_RIDE · PROMPT
RE-001 (META · SCORECARD · narrative)  -> reference_status: SUPERSEDED, contents untouched
```

**`CUSTODY_ALERT_001`, `DAY2_PARENT_FORENSIC_AUDIT`, `PR-001`, `IR-001`, `IR-002` and the four
ESS PDRs are class H — historical records, neither authoritative nor `REFERENCE_ONLY`. They
remain exactly as written under every path.**

---

# PATH C — the 08-24 Cut becomes a separate deliverable

*Two productions. Two locks. Two registry sets. Neither contaminates the other.*

## C.1 Operational consequences

**Registry impact**

| | effect |
|---|---|
| **Alpha RoundUp Part 2** (08-22) | **untouched.** Identical to Path A: every registry, every version, every hash pin stands |
| **the new production** (08-24) | **a complete second registry set is created from zero.** It shares no identifiers with the first. It has its own `production_id`, its own four input hashes, its own ETC, its own Approved Viewing Master entry, its own `TIMELINE_REGISTRY` with its own segment IDs |
| `APPROVED_VIEWING_MASTER` | **schema exercise.** The register is written `productions:` as a list but holds one entry. Path C is the first time it carries two, and the rule *"exactly ONE entry per production may carry status APPROVED"* becomes load-bearing rather than theoretical |

**Regeneration impact.** Nothing regenerates for Part 2. Everything **generates** for the new
production — the same seven-artifact atomic run, but as a first execution rather than a
regeneration, and gated on the same prerequisites Path B needs: new ETC, re-validated resolver,
designated master.

**Custody implications**

- `SOP-06 B2` **does not fire for Part 2** — its picture did not change. It fires as `A1` for
  the new production, which begins its own lifecycle at Phase A.
- `RE-001` stays `ACTIVE` and keeps describing Part 2. The new production gets its own reference
  execution when it reaches one.
- **The Parts have an obvious home**: three deliverables of the new production, or the new
  production *is* the three Parts with a Parent assembly. **That question is Executive.**
- **A new custody obligation appears that neither A nor B creates:** every future work order must
  now name *which production* it addresses. The platform has no mechanism for that today — every
  path in the repository is `intelligence/p2/…`.

**Downstream artifact effects.** Part 2's downstream is untouched: `ESS-001/002/003`,
`EVS-001`, `EPR-001`, `CONDUCTOR_SCORE`, the gate — all continue. The new production has no
downstream yet, and **`GATE-2026-08-22-MIE-DOWNSTREAM` does not apply to it** (`scope:
PRODUCTION`, `subject: … for Alpha RoundUp Part 2`). It would need its own gate.

## C.2 Risks

| # | risk |
|---|---|
| **C-R1** | **Permanent duplication.** Two registry sets, two locks, two masters, two gates, two DWRs — maintained in parallel for as long as both exist. This is the only path with an *ongoing* cost rather than a one-time one |
| **C-R2** | **Cross-contamination is now possible and nothing prevents it.** Two productions share riders, quotes, locations, organizations and 3 min 27 s of identical picture. A citation that omits its production is ambiguous — and **`APPROVED_VIEWING_MASTER` is the only artifact in the intelligence layer that names its production at all.** Every registry identifies itself by `registry_id` alone; the sole production discriminator anywhere else is the `p2` in the directory path |
| **C-R3** | **`intelligence/p2/` becomes a misleading namespace** the moment a second production exists under it |
| **C-R4** | **The three Parts may belong to neither.** If the Parts are the actual deliverable, C creates a *third* level — Parts of a Parent of a separate production — and the audit shows the Parts are not byte-slices of the Parent: each adds a 73.8 s head and a 15–20 s tail that exist in no Parent |
| **C-R5** | **Deferring the real question.** If the 08-24 cut is in fact the successor picture, C registers a successor as a sibling — and the divergence compounds with every further edit |
| **C-R6** | **`EXECUTIVE_RULINGS` and all doctrine are written production-agnostic but were exercised against one production.** Their scope is untested across two |

## C.3 Benefits

| # | benefit |
|---|---|
| **C-B1** | **Nothing is lost on either side.** Part 2's record stands intact *and* the 08-24 material becomes governed rather than reference. It is the only path where both are true |
| **C-B2** | **No regeneration of existing artifacts, and no `SOP-06 B2` void event for Part 2** |
| **C-B3** | **`EPR-07` keeps its anchor.** `S19` exists in Part 2 and always will; the new production declares its own beats from a clean start with no re-keying |
| **C-B4** | **The 91 cue-index citations never re-point.** They keep pointing at the GT-2 stream they were extracted from |
| **C-B5** | **The Parts get a governed parent** without voiding anything |
| **C-B6** | **It exercises the platform's multi-production design** — `production_id`, `scope: PRODUCTION` gates, per-production registers — which is designed but never tested. If a second production is coming regardless, this is where the design is proven |
| **C-B7** | **Reversible in one direction.** A later ruling can promote the separate production to *the* production; it cannot easily un-split two productions that have accrued independent history |

## C.4 Required follow-on actions

| # | action | owner |
|---|---|---|
| C-1 | **Name the new production and assign a `production_id`** | **Executive only** |
| C-2 | ~~Rule whether the deliverable is the Parent assembly, the three Parts, or both~~ — **ANSWERED 2026-08-26**: the three Parts are the distribution deliverables (D4); the Parent is an assembly artifact (D5) | **Executive — done** |
| C-3 | Declare a namespace convention for two productions; decide whether `intelligence/p2/` is renamed or the new production is sited beside it | platform → **Executive** |
| C-4 | Run `SOP-06 Phase A` for the new production: export, `GATE-1` audit, hash, ETC | production + platform |
| C-5 | Re-validate `fcpx_resolve.py` against the new ETC (`DOC-001`) | platform |
| C-6 | Designate an Approved Viewing Master for the new production; add a second `productions:` entry | platform + **Executive** |
| C-7 | First `gen_artifacts.py` execution for the new production | platform |
| C-8 | Author the new production's `TIMELINE_REGISTRY` and segment ID set | platform → **Executive** |
| C-9 | Issue a new Execution Gate scoped to the new production | **Executive** |
| C-10 | Record in `APPROVED_VIEWING_MASTER` that two productions share `00:00:00 – 00:03:27.208` identically, so the overlap is never read as an error | platform |
| C-11 | Amend `CUSTODY_ALERT_001` §1 for the resolved Part 1 identification | platform |

## C.5 Authoritative under Path C

**Two disjoint sets.**

*Alpha RoundUp Part 2 (08-22)* — everything currently authoritative, unchanged. Identical to
§A.5.

*The new production (08-24)* — nothing yet. Its artifacts become authoritative as C-4 … C-8
complete, each pinned to its own four hashes.

*Shared across both* — **all of class I.** Doctrine, `EXECUTIVE_RULINGS`, `ADR-009`, the
`WET-SPEC` family, `SOP-06`, `DWR-001`, `WET-SPEC-GATE-001`. **These are production-agnostic by
construction and govern both.**

## C.6 `REFERENCE_ONLY` under Path C

**Neither cut is `REFERENCE_ONLY`.** Both are authoritative for their own production. What
becomes `REFERENCE_ONLY` is only what already was:

```
the six existing reference_only renders in APPROVED_VIEWING_MASTER (unchanged)
+ any 08-24-lineage render that is NON_CONFORMANT to the NEW production's lock
+ PARENT m4a 4b43968a… / PARENT SRT 80a8ed25…  -- pending C-2, since the ANALYSIS-folder
  Parent is a re-encode of the 08-24 cut at the same runtime but a different hash, and only
  one of the two may be the new production's source
```

**`DAY2_PARENT_FORENSIC_AUDIT` changes status under C alone:** its §0.1 caveat — *"describes the
08-24 lineage, not the governed production"* — becomes obsolete, because under C the 08-24
lineage *is* a governed production. **The document does not need rewriting; its caveat needs a
dated annotation.**

---

## 7 · Cross-path comparison — facts only

**No column is weighted. No total is computed. No path is scored.**

| dimension | **A** | **B** | **C** |
|---|---|---|---|
| artifacts regenerated | 0 | 7 machine + ~12 by hand | 0 existing; 7 generated new |
| registries re-derived | 0 | ~11 | 0 existing; ~11 authored new |
| cue-index citations re-pointed | 0 | **91** | 0 |
| Executive re-declaration required | none | **`EPR-07` + any unresolved refs** | new production's beats, from zero |
| `SOP-06 B2` void event | no | **yes** | no (new production starts at A1) |
| new ETC required | no | **yes** | **yes** |
| resolver re-validation required | no | **yes** | **yes** |
| new Approved Viewing Master required | no | **yes** | **yes** |
| `RE-001` status | `ACTIVE` | `SUPERSEDED` | `ACTIVE` |
| `RE-ARCHIVE-01` urgency | deferred | **immediate** | deferred |
| `ESS-002` / `EVS-001` | proceed now | re-scope, re-prepare | proceed now |
| gate `GATE-2026-08-22-MIE-DOWNSTREAM` | unchanged | re-scoped | unchanged; second gate needed |
| interval with no authoritative timeline | none | **B-1 … B-12** | none for Part 2 |
| cost profile | one-time, small | one-time, large | one-time medium + **ongoing** |
| status of the three Parts | ~~reference extracts~~ | ~~extracts of the production~~ | ~~requires C-2 ruling~~ |
| ↳ **overtaken 2026-08-26** | **`DISTRIBUTION_DELIVERABLES` under all three paths (D4).** The row above was written before the Order and is struck rather than deleted. **What this implies for each path is custody precedence, which the Order reserves — it is not derived here** | | |
| namespace change required | no | no | **yes** |
| ease of later reversal | reverses to B or C at that path's cost | re-ruling costs a second full rebuild | promotes to single production easily; **un-splitting is hard** |

---

## 8 · What this brief cannot tell you

**This section exists because a decision package that presents only what is known invites a
ruling made on less than the Executive actually needs.**

### 8.1 Two questions the platform does not hold, either of which changes the decision

| | question | why it changes things |
|---|---|---|
| **Q1** | **Does a cut later than 2026-08-24 exist, or is one planned?** | Every path assumes the pair is `{08-22, 08-24}`. If the picture is still moving, **A** rules on a stale pair, **B** buys a full rebuild that a third cut invalidates, and **C** registers a sibling that will need a third. **The platform cannot observe editorial intent** — it can only hash what is on disk today |
| **Q2** | **What are the three Parts *for*?** | Each ships with a `-Cover.jpg`, a distribution-shaped asset. If the Parts are the actual audience deliverable, then the Parent is an assembly master and the 08-22 lock is a different product — which is not the same question as *"which cut is the production"* |

### `Q2` — **CLOSED** by Executive Order, 2026-08-26

```yaml
answers_recorded:
  Q2_purpose_of_the_three_parts: >
    The three Parts constitute the authoritative public distribution
    deliverables for Alpha RoundUp 2026 Day 2.

production_identity:
  three_parts_status: DISTRIBUTION_DELIVERABLES
```

**Executive facts declared with it:** Day 2 Part 1 is **the published public release**; Parts 2
and 3 are **scheduled public YouTube Premieres**; the ≈80-minute Parent timeline is an
**assembly artifact** used in creating the serialized releases; and the governed record **shall
explicitly distinguish assembly assets from public distribution assets.**

**The Order states these establish the role of each asset only, and do not determine production
lineage, custody precedence, or regeneration authority. No further consequence is drawn here.**

### `Q1` — **OPEN**, reserved to a separate Executive ruling

The Order expressly reserves it. **One half of it has observable evidence and one half does not,
and the difference matters:**

- **On disk:** no FCPXML later than **2026-08-24 17:14** exists anywhere in the tree. That is an
  observation about *exported artifacts*, made 2026-08-26.
- **Not on disk:** the editing application's live library is not in this tree, so *"the latest
  export"* and *"the latest edit"* are different claims. File modification times are not
  authorship evidence — a copy can carry or reset one.
- **Not observable at all:** whether a later cut is *planned*. **That is Executive knowledge and
  the platform holds none of it.**

### 8.2 The framing carries an assumption worth making explicit

The three paths are constructed as **one production slot with two candidates.** That framing is
the Executive's to keep or discard, but it is a framing, and the forensic audit produced evidence
that sits awkwardly inside it:

> The 08-24 lineage is not an isolated file. It is **a Parent with three tiled extracts, cover
> art, and a coherent internal structure** — a 73.800 s standardised opening on each Part, a
> 15–20 s tail on each, no internal edits anywhere. **That is the shape of a distribution
> product, not of a working export.**

**This is stated as an observation, not as an argument for any path.** It is equally consistent
with **B** (the production was re-cut for release and the Parts are its delivery form) and with
**C** (a distinct three-part deliverable was built from a distinct assembly). **It is least
consistent with the description of the 08-24 file as a working export** — but "least consistent"
is not "excluded", and Path A remains fully available: a team can produce a polished three-part
export from a working cut and still hold the 08-22 lock as the production.

> **Annotation, 2026-08-26 — the uncertainty in the paragraph above is closed; the framing
> question is not.** The Executive Order declares the three Parts to be the authoritative public
> distribution deliverables (D4) and the Parent an assembly artifact (D5), and further declares
> that **Part 1 is already published** and Parts 2 and 3 are **scheduled Premieres** (D1–D3).
> The paragraph's *"if the Parts are the actual audience deliverable"* is therefore no longer a
> conditional. **What that means for which cut is the production is custody precedence, which the
> Order expressly reserves. It is not inferred here, and the three paths in §4–§6 stand exactly
> as accepted.**
>
> Two facts are additionally recorded, without consequence drawn:
>
> - **The three Parts exist as full 4K picture renders** — `1648.200 s` · `1669.033 s` ·
>   `1567.000 s`, all 3840×2160 at **30/1 fps**, against the production's 24/1 — measured
>   2026-08-26. A `75.875 s` trailer and a thumbnail named *"Part 1 of 3"* exist alongside them.
> - **An eighth 4K viewing-master candidate exists and is not in `APPROVED_VIEWING_MASTER`:**
>   `ALPHA ROUND UP Day 2 Part 2/Alpha RoudUp Part 2.m4v`, 3840×2160, 24/1, **4689.500 s**,
>   11.80 GB, dated 2026-08-24. **Its filename is identical to the Approved Viewing Master's.**
>   Registering it would alter a governed registry, which the Order suspends; it is recorded here
>   instead.

### 8.3 What is being spent while the ruling is open

Since 2026-08-22, **six commits and seventeen documents** have entered the record, all pinned to
the 08-22 lock: `EPR-001` and its validator, `VPD-001`, `VOICE_PRIORITY_MAP`,
`MUSIC_OVERLAY_TIMELINE`, `BEHAVIORAL_FINGERPRINT`, `EVS-001`, `CUSTODY_ALERT_001`, `PR-001`,
`IR-001`, `IR-002`, the forensic audit, and the `ER-001…ER-004` amendments.

**The accretion is not neutral between the paths.** Under **A** and **C** all of it stands; under
**B** the timecode-bearing members of that set are rebuilt. **This is not a reason to hurry** —
a ruling made early on Q1 and Q2 unknowns is worse than a ruling made late on known answers.
It is stated so the cost of the open interval is visible rather than silent.

### 8.4 One thing that is true under all three paths

**The 08-24 lineage currently has no custody status at all.** That is what allowed a work order
to reach it and be executed against it before anyone noticed which film it described. Whatever
§5 rules, the operational fix is the same: **the lineage acquires a status.**
`REFERENCE_ONLY` (A), production (B), or separate production (C) — **all three close that hole,
and no third option leaves it open.**

---

## 9 · Decision record — to be completed by the Executive

*Two fields are now filled. **Both were transcribed verbatim from the Executive Order of
2026-08-26** — they are the Executive's own words, not the platform's. Every other field remains
blank, and the platform has not pre-filled, suggested, inferred, or defaulted any of them, and
will not.*

```yaml
ruling_id: CUSTODY_ALERT_001-RULING
authority: Executive Producer / Chairman
date:

path_selected:                    # A | B | C | other      -- NOT SELECTED
rationale:                        # Executive custody

answers_recorded:
  Q1_later_cut_exists:            # yes | no | unknown     -- OPEN, reserved
  Q2_purpose_of_the_three_parts: >                         # CLOSED 2026-08-26
    The three Parts constitute the authoritative public distribution
    deliverables for Alpha RoundUp 2026 Day 2.

production_identity:
  governed_production:
  08_24_lineage_status:           # REFERENCE_ONLY | PRODUCTION | SEPARATE_PRODUCTION
  three_parts_status: DISTRIBUTION_DELIVERABLES            # declared 2026-08-26
  parent_timeline_role: >                                  # declared 2026-08-26
    Assembly artifact utilized in the creation of the serialized releases.

record_distinction_required: >                             # declared 2026-08-26 (D6)
  The governed record shall explicitly distinguish assembly assets
  (internal editorial lineage) from public distribution assets
  (released deliverables).

authorised_follow_on_actions: []  # from A.4 / B.4 / C.4
deferred_follow_on_actions: []

effective_immediately:            # true | false
review_by:
```

**Suspended until `Q1` is adjudicated:** path selection · registry regeneration · registry
re-keying · modification of custody precedence · alteration of any governed registry · platform
inference of custody implications · downstream governance changes.

---

## 10 · Provenance of this brief

| item | value |
|---|---|
| custody | `ANALYSIS ONLY` |
| evidence base | `CUSTODY_ALERT_001` · `DAY2_PARENT_FORENSIC_AUDIT` · `APPROVED_VIEWING_MASTER` v1.0.0 · `DOWNSTREAM_AUTHORIZATION_GATE` v1.3.0 · `RE-001_META` · `SOP-06` · `EXECUTIVE_RULINGS` v1.5.0 · `TIMELINE_REGISTRY` v1.0.0 · `EMOTIONAL_PROGRESSION_REGISTRY` v1.1.0 · repository survey of 186 tracked `.yaml`/`.md`/`.json` documents |
| verification pass | every count, version and hash re-queried against the repository after drafting; **five figures were wrong in the draft and were corrected** — the hash-citation count (32 → **31**), the out-of-range artifact count (six → **eight**), the scope of the 29 time-bearing artifacts, the claim that no artifact names its production, and the provenance of the three MIE generators |
| method | every artifact name, version, hash, count and span cited here was read from the repository or from a hashed asset during preparation — **none was recalled** |
| changes made at issue | **none.** No code, no registry, no commit |
| changes made at `AMENDMENT 1` | this document only. **No registry, no artifact, no regeneration, no path selection.** `EXECUTIVE_RULINGS.yaml`, `APPROVED_VIEWING_MASTER.yaml`, `DOWNSTREAM_AUTHORIZATION_GATE.yaml`, `DEFERRED_WORK_REGISTER.yaml`, `RE-001` and every artifact under `intelligence/p2/` were **not touched** |
| recommendation | **none given, and none implied by ordering, emphasis, or omission** |

*The three paths are each consistent with the platform's rules. Which is true is a production
fact only the Executive holds.*
