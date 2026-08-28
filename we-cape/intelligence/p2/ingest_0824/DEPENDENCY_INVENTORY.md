# DEPENDENCY INVENTORY — what Path B must traverse

**State:** `PREPARED_NOT_EXECUTED` · **Prepared:** 2026-08-28 · **Custody:** `MACHINE`
**Authority:** `EXECUTIVE ORDER — CUSTODY_ALERT_001 FINAL DISPOSITION & WORKBOOK GENERATION` §2.5
**Source of the classification:** `EXECUTIVE_DECISION_BRIEF_CUSTODY_ALERT_001.md` §2, measured
from the repository 2026-08-26 and re-checked 2026-08-28.

**This is an inventory, not a work order.** Nothing listed has been re-derived, re-pointed, or
regenerated.

---

## 1 · Classes

| class | binding | count | disposition under Path B |
|---|---|---|---|
| **T** — timecode-bound | values are positions in one specific edit | 21 artifacts | **all require re-derivation** |
| **X** — SRT-cue-index-bound | cite `#NNNN` positions in the GT-2 caption stream | 4 registries, **91 citations** | **all require re-pointing or retirement** |
| **S** — segment-keyed | survive iff the `S01…S19` ID set survives | 3 artifacts | **survive if the ID set is ratified unchanged; `EPR-07` already does not** |
| **I** — cut-independent | doctrine, rulings, specs, standards | ~25 documents | **unaffected. No governance instrument is disturbed by Path B** |
| **H** — historical by design | records of a moment | 10 documents | **never re-pointed. They remain true of when they were written** |

---

## 2 · Class T — timecode-bound

Ordered by the count of time-bearing values each carries.

| artifact | time values | regeneration route |
|---|---|---|
| `mie/VOICE_PRIORITY_MAP.yaml` | 1564 | `mie/scripts/voice_priority_map.py` |
| `ess/VISUAL_EVENT_REGISTRY.yaml` | 206 | **`gen_artifacts.py`** |
| `ess/CONDUCTOR_SCORE.yaml` | 121 | **`gen_artifacts.py`** |
| `registries/CAPTION_REGISTRY.yaml` | 115 | **`gen_artifacts.py`** |
| `ess/EDITORIAL_SYNCHRONIZATION.yaml` | 105 | **`gen_artifacts.py`** |
| `ess/STEP0_TIMING_CLOSURE.md` | 94 | **`gen_artifacts.py`** |
| `mie/MUSIC_OVERLAY_TIMELINE.yaml` | 85 | `mie/scripts/music_overlay_timeline.py` |
| `mie/CUE_SHEET.yaml` + `CUE_SHEET_v1.1.yaml` | 64 | **no generator — hand-authored** |
| `registries/TIMELINE_REGISTRY.yaml` | 41 | **no generator — hand-authored** |
| `ess/ESS_VALIDATION_REPORT.md` | 38 | **`gen_artifacts.py`** |
| `mie/BEHAVIORAL_FINGERPRINT.yaml` | 30 | `mie/scripts/behavioral_fingerprint.py` |
| `ess/EXECUTION_LOG.md` | 21 | **historical — do not re-point** |
| `mie/EMB-CUE-03_…_SKELETON.md` | 14 | **no generator** |
| `registries/QUOTE_LIBRARY.yaml` | 13 | **no generator** |
| `registries/DOCUMENTARY_PROGRESSION.yaml` | 10 | **no generator** |
| `mie/PHASE3_TRANSITION_WORK_ORDER_STATUS.md` | 9 | **historical** |
| `registries/VOICE_OVER_REGISTRY.yaml` | 8 | **no generator** |
| `registries/WHY_I_RIDE_REGISTRY.yaml` | 66 (`t:` fields) | **no generator** |
| `registries/RIDER_REGISTRY.yaml` | 80 (`cue:` fields) | **no generator — also class X** |
| `ess/PRODUCTION_INTELLIGENCE_SEED.yaml` | 2 | **`gen_artifacts.py`** |
| `MIE_INPUT_PACKAGE.yaml` | 2 | **no generator** |
| `registries/APPROVED_VIEWING_MASTER.yaml` | 4 | hand-maintained register |

### 2.1 The regeneration boundary

```
machine-regenerable, ONE atomic run      7   gen_artifacts.py
script-assisted, inputs must be re-pinned 3   mie/scripts/*.py
HAND-AUTHORED, NO GENERATOR              ~11
historical, never re-pointed              2
```

**The eleven hand-authored artifacts are the cost centre, and no tool exists for any of them.**

---

## 3 · Class X — the silent-failure surface

| registry | `#NNNN` citations |
|---|---|
| `RIDER_REGISTRY.yaml` | **80** |
| `MOTORCYCLE_REGISTRY.yaml` | 6 |
| `ORGANIZATION_REGISTRY.yaml` | 3 |
| `PROMPT_REGISTRY.yaml` | 2 |
| **total** | **91** |

The governed production's caption stream holds **2036 cues**; the superseded assembly's holds
**2291**. **`#1420` is a different sentence in the two streams.**

> **A wrong timecode is caught by a bounds check. A wrong cue index is caught by nothing.** It
> always resolves, it never errors, and the result is a confident misattribution of a quote or a
> rider to a person who did not say it. **This is the highest-severity item in the inventory and
> it has no automated detection.**

---

## 4 · Class S — segment-keyed

| artifact | status |
|---|---|
| `EMOTIONAL_PROGRESSION_REGISTRY.yaml` (EPR-001) v1.2.0 | **`EPR-07` unresolvable** (`PBC-1`); `S18` boundary out of range (`PBC-2`); no episode assignment (`PBC-3`) |
| `EMOTIONAL_ARC.yaml` | superseded by EPR-001; retained, `DO NOT EDIT` |
| `ENERGY_CURVE.yaml` | keys on `S01…S19`; inherits every consequence above |

**Segment keying was chosen precisely so intent would survive a re-cut. It largely has: 16 of 18
in-scope segments are unaffected as identifiers.** The two that are not are `S18` and `S19`, at
the tail — and `S19` is the one carrying an Executive beat.

---

## 5 · Class I — unaffected

`DOC-001` · `DOC-002` · `DOC-003` · `DOC-SRC-001` · `DOC-CAND-001` · `VPD-001` ·
`EXECUTIVE_RULINGS.yaml` v1.5.0 · `ADR-007` · `ADR-009` · `AIS-001` · every `WET-SPEC-*` ·
`SOP-04/05/06` · `WET-SPEC-GATE-001` · `DWR-001` · `CAR-001/003/004`.

**No governance instrument is disturbed by Path B.** Only measurements are. That is a property of
the architecture, and it is the reason Path B is executable at all.

---

## 6 · Class H — historical, never re-pointed

`RE-001` META · SCORECARD · narrative · `CUSTODY_ALERT_001` · `DAY2_PARENT_FORENSIC_AUDIT` ·
`PR-001` · `IR-001` · `IR-002` · the four `PDR-2026-08-22-ESS-*` · `EVS-001`.

**`RE-001` is the exception that needs an Executive act:** it still reads
`reference_status: ACTIVE` while describing a superseded assembly. Changing that is **not
authorized by any Order to date** (`LC-5`).

---

## 7 · Order of operations, if and when regeneration is authorized

```
IP-1  Editorial Timing Contract for the 08-24 lineage
   -> IP-2  fcpx_resolve.py re-validated against it            (DOC-001: instrument first)
      -> IP-6  segment set re-derived and Executive-ratified
         -> IP-7  episode boundaries assigned                  (unblocks PBC-3)
            -> gen_artifacts.py, ONE atomic run, SEVEN artifacts   (DOC-002: never partial)
               -> mie/scripts/*.py re-derivation
                  -> hand-authored class T
                     -> class X re-pointing, method recorded
                        -> RE-002 archival, RE-ARCHIVE-01 remedy, D-26 fix
```

**Two independent gates sit across this whole chain and neither is opened by the ratification of
Path B:**

- **`GATE-2026-08-22-MIE-DOWNSTREAM`** — `CLOSED`, 3 of 4 blocking PDRs still OPEN
- **`gen_artifacts.py` RUN_ID lock** — held by the 2026-08-28 Order §4 until the Workbook is
  complete and `EPR-001` is ratified

**Nothing in this inventory has been executed.**
