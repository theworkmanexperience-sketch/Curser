# Road Soul™ Phase 3 Transition — Work Order Status
**Issued:** Chairman, 2026-08-22 · **Reported by:** Music Systems Engineer · **Date:** 2026-08-22
**Conformance:** ER-001 (no ranking, no recommendation, no preference) · ER-003 (mechanics precede meaning)

| task | status | artifact |
|---|---|---|
| **1 · VOICE_PRIORITY_MAP** | **DELIVERED** | `intelligence/p2/mie/VOICE_PRIORITY_MAP.yaml` v1.0.0 |
| **2 · Music Overlay Timeline** | **DELIVERED** | `intelligence/p2/mie/MUSIC_OVERLAY_TIMELINE.yaml` v1.0.0 |
| **3 · Executive Music Brief, CUE-03** | **BLOCKED — 6 items** | §3 below |
| **4 · Prepare candidate generation + validation** | **PARTIAL** | §4 below |

---

## 1 · VOICE_PRIORITY_MAP — delivered

Documentary-wide, 0.5 s grid, run-length encoded to **759 spans**. Every behaviour cites the law it
comes from; none is invented.

| required behaviour | spans | total | share of lock | law |
|---|---|---|---|---|
| `DUCK` | 372 | 2782.0 s | 57.4% | Yield Law (−18 dB under dialogue, CONVERSATION) |
| `LEAD` | 88 | 757.0 s | 15.6% | family signature — MOTION / CELEBRATION |
| `FLOOR` | 3 | 587.5 s | 12.1% | silence law (ESS-004 ruling) |
| `SUSTAIN` | 285 | 280.0 s | 5.8% | family signature — CONVERSATION / REFLECTION / LEGACY |
| `UNCOVERED` | 11 | 440.1 s | 9.1% | no governed cue region specifies behaviour |

Speech: **2291 SRT cues · 3359.5 s · 69.3% of the lock.** Occupancy evaluated at each slot's
midpoint — expanding cue in/outs to slot boundaries would widen 2291 cues by up to a grid step each
and inflate coverage systematically.

### Speech occupancy inside every governed region

| cue | family | dur | speech | speech-free | longest free window | **VO reserved** |
|---|---|---|---|---|---|---|
| CUE-01 | REFLECTION | 73 s | 53.1% | 34 s | 13.0 s | 0.5 s |
| CUE-02a | CONVERSATION | 519 s | 88.5% | 60 s | 3.0 s | 0.5 s |
| CUE-02b | CONVERSATION | 495 s | 89.0% | 54 s | 4.5 s | 0 |
| CUE-02c | CONVERSATION | 497 s | 93.9% | 30 s | 4.5 s | 0.5 s |
| **CUE-03** | **MOTION** | **90 s** | **58.0%** | **38 s** | **34.0 s** | **90.5 s — the entire cue** |
| SIL-01 | — | 429 s | 82.8% | 74 s | 9.0 s | 0 |
| CUE-04 | CONVERSATION | 785 s | 92.2% | 62 s | 5.0 s | 0 |
| SIL-02 | — | 105 s | 71.6% | 30 s | 10.0 s | 0 |
| CUE-05 | REFLECTION | 45 s | 46.2% | 24 s | 15.0 s | 0 |
| CUE-06 | REFLECTION | 48 s | 86.6% | 6 s | 6.5 s | 48.5 s |
| **CUE-07** | **MOTION** | **153 s** | **0.7%** | **152 s** | **152.5 s** | **0** |
| CUE-08 | CELEBRATION | 485 s | 91.9% | 40 s | 3.0 s | 0 |
| CUE-09a | CELEBRATION | 305 s | 24.4% | 231 s | 45.5 s | 0 |
| CUE-09b | CELEBRATION | 310 s | 4.5% | 296 s | 208.0 s | 0 |
| CUE-10 | LEGACY | 62 s | 84.0% | 10 s | 5.5 s | 62.5 s |

### F1 — CUE-03 is entirely inside a host-VO segment, and VO02 ends at 00:29:10.000

`VOICE_OVER_REGISTRY` v0.1.0 records `VO02 · ride_narration · 27:02–29:10 · vo_candidate:
lead-in-to-civic`. **CUE-03 (27:40–29:10) sits wholly inside it. VO overlap: 90.5 s of a 90 s cue.**

`VO02` **ends at exactly 00:29:10.000** — the CUE-03 out point that ESS-002 exists to adjudicate,
and the point I reported as having *"no picture event, no audio event."* Both of those statements
remain true. **A third artifact places a boundary there, and it is a speech boundary.**

That is a factual candidate explanation for why the cue-sheet boundary sits 18.250 s inside a
66.708 s take: it may never have been a picture boundary. **Whether it should govern the music is
Executive judgement and is not assessed here.**

This registry was not consulted during the ESS-002 measurement work. Recorded as a second instance
of the ER-003 failure class, in the same session.

### F2 — the two MOTION cues have opposite voice conditions

| | CUE-03 | CUE-07 |
|---|---|---|
| speech coverage | **58.0%** | **0.7%** |
| longest speech-free window | 34.0 s | **152.5 s of 153 s** |
| VO reserved | **100% of the cue** | 0 |

Both carry the same family signature — `ENTER · LEAD · DUCK · REBUILD · HANDOFF`. **`LEAD` and
`DUCK` therefore describe materially different obligations in the family's only two members.**
Measurement bearing directly on `DWR-041`; no conclusion drawn.

---

## 2 · MUSIC_OVERLAY_TIMELINE — delivered

**16 regions · 11 uncovered gaps · 25 transitions.** Covered 4401.0 s; uncovered 445.6 s (9.1%).

### F3 — 21 of 25 transitions pass through an uncovered gap

Only **4** are `CUE_TO_CUE`: 02a→02b, 02b→02c, 07→08, 09a→09b.

**Neither silence zone is entered from or exited to a cue.** SIL-01 is preceded by `GAP-03`
(29:10–31:43) and followed by `GAP-04`. SIL-02 likewise.

Consequence, stated as measurement: the silence law assigns `APPROACH` and `RETURN` to govern *"the
shape of the exit and the re-entry either side"* of a conducted silence. **In the lock as it stands,
neither state has a cue to approach from or return to** — both boundaries face an unscored gap.

This bears directly on ESS-002 option B. Extending CUE-03 to 31:43 would create the platform's
**only** direct `CUE → MANDATORY_SILENCE` transition and give `APPROACH` something to attach to.
**Recorded as a consequence of an option, not as an argument for it.**

---

## 3 · Executive Music Brief for CUE-03 — BLOCKED

Six items. Four are missing inputs, one is a naming conflict, one is a governance gate. **None is
engineering's to resolve.**

| # | blocker | detail |
|---|---|---|
| **B1** | **`VPD-001` Voice Priority Doctrine does not exist** | Named as a required input. A repository-wide search returns nothing — no file, no reference, no draft. The doctrine has never been written |
| **B2** | **No Executive Palette exists — for any family** | ER-002 Clarification 2: palettes are Executive-owned; the platform **may not author or extend one**. `DWR-044` records that none has been authored. The brief cannot cite what does not exist, and cannot create it |
| **B3** | **Name conflict: "WE PULLING UP" vs `ESCORT_ANTHEM`** | `CUE_SHEET v1.1` (ARCHITECTURE APPROVED, Chairman 2026-08-21) names CUE-03 `ESCORT_ANTHEM`. "WE PULLING UP" appears nowhere in the repository. Rename of the approved entry, or a different cue? |
| **B4** | **CUE-03's boundary is undispositioned** | ESS-002 is OPEN; EVS-001 unheld; card blank. Entry and Handoff requirements are boundary-dependent — writing them now would presume the disposition |
| **B5** | **"Yield" is not in the behaviour vocabulary** | The ten states are `ENTER SUSTAIN DUCK REBUILD HANDOFF LEAD BREATHE APPROACH FLOOR RETURN`. *Yield* is the name of a **law**, not a state, and the state that enacts it is `DUCK`. Requesting "Entry, Yield, Rebuild, Handoff" either means `ENTER DUCK REBUILD HANDOFF` — or introduces an eleventh state, which is `RSB-AUDIT-001` gap **G2** |
| **B6** | **The gate is CLOSED and names CUE-03 explicitly** | `GATE-2026-08-22-MIE-DOWNSTREAM` blocks `MIE_PASS_3_MOTION`, `CUE-03`, `SIL-01_APPROACH`. Three PDRs remain open; `unblock_condition` states *"partial disposition does not partially open this gate"* |

**Tasks 1, 2 and 4 sit outside the gate** — they are derivations of governed artifacts, not MIE
generation. **Task 3 sits inside it.** Opening the gate, or issuing a carve-out, is an Executive act.

### What can be prepared for the brief without any of the above
A brief *skeleton* citing only what is already governed: CUE-03's family, its behaviour-state
signature, its reason-for-existing from the cue sheet, its measured voice condition (§1), and its
transition context (§2) — with `palette`, `voice_priority_doctrine`, `boundary` and `cue_name`
carried as explicit `AWAITING_EXECUTIVE_INPUT` fields rather than filled with defaults. **Say the
word and it takes an hour. It is not started, because a brief with four invented fields is worse
than no brief.**

---

## 4 · Prepare for candidate generation and validation — PARTIAL

**Buildable now, no blockers** — these validate a delivered candidate against governed criteria and
require no palette, no doctrine and no boundary:

| validator | criterion (ER-001) | method |
|---|---|---|
| duck depth | `ducking_compliance` | measured level under dialogue vs bed level, EBU R128 |
| rebuild budget | `timing_behaviour` | return-to-bed time vs the span's measured `budget_s` |
| silence-covenant tail | `silence_covenant_compliance` | energy inside a silence zone attributable to added score |
| placement | `placement_conformity` | candidate in/out vs the governed cue boundary, to the frame |
| breathe ceiling | `behavioural_state_conformity` | inter-answer gain vs `max_gain_db` |

**Not buildable** — `transition_conformity` and `registry_consistency` both need the boundary
(B4); palette conformity needs a palette (B2) **and** a closed term vocabulary (`EC-N1`, unruled).

Reports will emit the mandated shape — `criterion · status · evidence · measurement · method` —
with **no counts, totals, percentages or aggregates** (ER-001, Executive Clarification 1).

---

## Session state, unchanged

```
pass_1                 ACTIVE
boundary_declared      false
observation_card       BLANK
disposition_inference  FORBIDDEN
```

Nothing in this report bears on the ESS-002 boundary question. **F1 and F3 are measurements that a
disposition may weigh; neither is an argument.**
