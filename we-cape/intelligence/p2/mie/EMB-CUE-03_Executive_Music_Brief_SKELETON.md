# EMB-CUE-03 — Executive Music Brief · **SKELETON**
## CUE-03 · `ESCORT_ANTHEM` · working title *"WE PULLING UP"*

**Status:** `SKELETON — NOT A BRIEF.` Executive-owned fields are marked `AWAITING_EXECUTIVE_INPUT`
and are **not** filled with defaults.
**Authorized:** Executive, 2026-08-22, Phase 3 Continuation communiqué item 6
**Prepared by:** Music Systems Engineer · **Custody:** `MACHINE`
**Conformance:** ER-001 · ER-002 (no palette authored or extended) · ER-003 · `VPD-001` v0.1

> **Gate notice.** `GATE-2026-08-22-MIE-DOWNSTREAM` is **CLOSED** and names `CUE-03`,
> `MIE_PASS_3_MOTION` and `SIL-01_APPROACH` explicitly. This skeleton is a derivation of governed
> artifacts, not MIE generation. **No candidate may be generated against it while the gate is
> closed.**

---

## 1 · Identity — per Executive disposition item 4

| field | value | source |
|---|---|---|
| Canonical Cue ID | `CUE-03` | `CUE_SHEET v1.1` |
| Official Cue Sheet Name | `ESCORT_ANTHEM` | `CUE_SHEET v1.1` (ARCHITECTURE APPROVED, Chairman, 2026-08-21) |
| Creative Working Title | *"WE PULLING UP"* | Executive, 2026-08-22 |
| Road Soul Family | **MOTION** | `CONDUCTOR_SCORE` v1.1.0 |
| Energy target | **5** | `CUE_SHEET v1.1` |
| Pass | 3 | `CUE_SHEET v1.1` — gated behind the Conversation family gate |

**Blocker B3 closed.** The three names are now distinguished rather than conflated: the canonical ID
is what artifacts cite, the cue-sheet name is what the approved architecture holds, and the working
title is Executive creative language. **Only the ID and the sheet name appear in generated
artifacts;** the working title is carried here and in the PDR.

---

## 2 · Narrative purpose — governed, verbatim

> *"Exists to transition arrival into shared momentum"* — `CONDUCTOR_SCORE` v1.1.0

> *"Exists to transition the audience from arrival into shared momentum before the community story
> begins — the film's first full statement of unity in motion."* — `CUE_SHEET v1.1`

**Nothing added.** Any expansion of narrative purpose is Executive language, not engineering's.

---

## 3 · Boundaries — **UNRESOLVED**

| field | value |
|---|---|
| Cue-sheet span | `00:27:40.000 – 00:29:10.000` · 90.0 s · timebase CLOSED |
| **Governing boundary** | **`AWAITING_EXECUTIVE_INPUT`** — `PDR-2026-08-22-ESS-002` is OPEN |

`ESS-002` is narrowed to one question: *is the proposed musical boundary correct?* `EVS-001` is
prepared and **unheld**; the observation card is blank. **Entry and Handoff requirements below are
written against the cue-sheet span and are provisional until the boundary is dispositioned.**

**Measured context for the boundary, from the record, no conclusion drawn:**

- `27:40.792` is a cut. The cue-sheet in-point sits **0.792 s** before it — the only boundary in the
  region near a picture event.
- `29:10.000` sits **18.250 s** inside a **66.708 s** take. No cut. No audio level event
  (**+0.556 dB**, below the ~1 dB JND).
- `VO02 · ride_narration` **ends at exactly `29:10.000`.** The boundary coincides with a **speech**
  boundary, not a picture one (`VOICE_PRIORITY_MAP` F1).

---

## 4 · Voice condition — measured, `VOICE_PRIORITY_MAP` v1.0.0

| measurement | value |
|---|---|
| SRT cues in span | 20 |
| Speech coverage | **58.0%** |
| Speech-free total | 38 s |
| **Longest speech-free window** | **34.0 s** (`00:28:11.208 – 00:28:44.875`) |
| Inter-cue gaps | 17 · median **0.084 s** · p10 **0.042 s** |
| **Host-VO reserved** | **90.5 s — the entire cue lies inside `VO02`** |

**Two production-audio elements must be sat under, not replaced** — both `KEEP_CANDIDATE`,
`HUMAN_PDR_REQUIRED`:

| element | span | classification |
|---|---|---|
| `Map traavel to Smyrna Event Center-10` | 27:40.792 – 28:12.147 | `PRODUCTION_ORIGINAL_MEDIA_AUDIO` |
| `Map traavel to Smyrna Event Center-8` | 28:44.708 – 29:11.681 | `PRODUCTION_ORIGINAL_MEDIA_AUDIO` |

> *"the route-map animation audio … a music cue must sit under it, not replace it"* —
> `CONDUCTOR_SCORE` v1.1.0, reconciliation basis

**Consequence, stated as measurement:** the cue's only substantial speech-free window — 34.0 s —
falls **between** the two map elements. The cue is constrained on three layers simultaneously:
interview speech (58%), route-map production audio (both ends), and a reserved host-VO window (all
of it).

---

## 5 · Voice Priority Doctrine — `VPD-001` v0.1

| provision | applies to CUE-03? | effect |
|---|---|---|
| **P1** Yield Law, −18 dB | **NO as written** — scoped to CONVERSATION | CUE-03 is MOTION |
| **P2** Speech band 1–4 kHz uncluttered | **YES** — "every cue that runs under speech" | binding |
| **P3** VO ducks like dialogue | **YES** — `VO02` covers the cue | binding |
| **P4/P5** silence-zone exclusions | **NO** — CUE-03 is outside every silence zone | — |
| **P8** `YIELD` is doctrine, `DUCK` the mechanism | **YES** | the cue's `DUCK` state enacts it |
| **P9** *"support orientation rather than lead"* | **`AWAITING_EXECUTIVE_INPUT`** | issued for `00:27:10`, which is **30 s before** this cue starts. Whether it governs CUE-03 is not stated and is not inferred |

**Open question carried from `VPD-001` §3.3, material to this cue:** CUE-03's `DUCK` sidechain names
*"voice-over and any diegetic announcement only."* **It does not name interview speech** — which
occupies 58.0% of the cue. Whether this bed ducks to interview speech at all is unstated.

---

## 6 · Behavioral sequence — governed, verbatim from `CONDUCTOR_SCORE` v1.1.0

MOTION family signature: `ENTER · LEAD · DUCK · REBUILD · HANDOFF`

| state | specification as recorded | class |
|---|---|---|
| **ENTER** | *"enter under picture on a movement, not on a cut; ≤2 s"* | ≤2 s is **Type A**; "on a movement, not on a cut" is **Type C** |
| **LEAD** | *"music carries the span; ambient engine and crowd sound sit under it but must remain audible"* | **Type B** — audibility is a relation between two signals |
| **DUCK** | `target_db: -12` · `sidechain: voice-over and any diegetic announcement only` | **Type A** |
| **REBUILD** | `budget_s: 0.042` | **Type A** — the span's measured p10 inter-cue gap |
| **HANDOFF** | *"resolve on the last phrase before the boundary; do not fade under the following cue's entry"* | **Type B** |

**Transition out, as recorded:** *"Crossfade at a phrase boundary unless the next entry is a
conducted silence, in which case the APPROACH state governs and nothing may tail across the
boundary."*

**Measured note on the handoff:** CUE-03 does **not** currently hand off to a cue or to a silence. It
hands off to `GAP-03` (`29:10 – 31:43`, uncovered). **21 of 25 transitions in the lock pass through
an uncovered gap; neither silence zone is entered from a cue** (`MUSIC_OVERLAY_TIMELINE` F3). The
`HANDOFF` specification above has no defined destination until `ESS-002` is dispositioned.

---

## 7 · Palette — **NOT SUPPLIED, AND NOT INFERRED**

```yaml
palette:                 AWAITING_EXECUTIVE_INPUT
palette_reference:       AWAITING_EXECUTIVE_INPUT   # Road Soul MOTION, once issued
list_closure:            AWAITING_EXECUTIVE_INPUT   # CLOSED or OPEN (EC-N1, unruled)
```

ER-002 Clarification 2: **Palette is layer 4 and Executive-owned. The platform may reference a
palette; it may not author, extend, add terms to, or infer one.** No palette has been issued for any
family (`DWR-044`).

**`CONDUCTOR_SCORE` carries `inherited_expressive_guidance` for MOTION**, preserved verbatim under
the Option C ruling and marked `normative: false`, `authored_by: NOT_THE_PLATFORM`,
`status: AWAITING_EXECUTIVE_PALETTE_RATIFICATION`. **It is deliberately not reproduced here**, so
that this skeleton cannot be mistaken for supplying a palette.

---

## 8 · Generation targets — **BLOCKED**

```yaml
candidate_count:         AWAITING_EXECUTIVE_INPUT
minimum_usable_length:   AWAITING_EXECUTIVE_INPUT
creative_prompt:         EXECUTIVE_PRODUCER_OR_COMPOSER_ONLY   # ER-002: the platform shall not
                                                               # author, optimize or select one
gate_state:              CLOSED    # GATE-2026-08-22-MIE-DOWNSTREAM
```

**Nothing may be generated until the gate opens.** The gate opens only when all four PDRs are
dispositioned; `ESS-004` is done, three remain.

---

## 9 · What this skeleton would need to become a brief

| # | needed | owner | status |
|---|---|---|---|
| 1 | ESS-002 boundary disposition | Executive | `EVS-001` prepared, unheld |
| 2 | Road Soul **MOTION** palette | Executive | none issued for any family |
| 3 | `VPD-001` §3.3 — voice priority order and collision resolution | Executive | four fields open |
| 4 | Whether P9 governs CUE-03 | Executive | issued 30 s earlier, scope unstated |
| 5 | Whether a MOTION bed ducks to interview speech | Executive | sidechain names VO only |
| 6 | Gate open, or a carve-out | Executive | three PDRs open |
| 7 | Creative prompt | Executive Producer / Composer | ER-002 forbids platform authorship |

**Seven items. All seven are Executive. None is engineering's to resolve, and none has been filled
with a default.**

---

## 10 · Validators ready on gate-open — task 4

Emitting `criterion · status · evidence · measurement · method`, **no counts, totals, percentages or
aggregates** (ER-001, Executive Clarification 1):

| criterion | testable now | method |
|---|---|---|
| `ducking_compliance` | **yes** | level under VO/announcement vs bed, target −12 dB, EBU R128 |
| `timing_behaviour` (rebuild) | **yes** | return-to-bed time vs `budget_s` 0.042 |
| `silence_covenant_compliance` | **yes** | provenance test — added score inside a zone (ESS-004) |
| `placement_conformity` | **on disposition** | candidate in/out vs the governing boundary, to the frame |
| `behavioural_state_conformity` | **partial** | Type A criteria only; ENTER's "not a downbeat" is Type C |
| `transition_conformity` | **blocked** | no defined destination until ESS-002 closes (§6) |
| `registry_consistency` | **blocked** | boundary-dependent |
| palette conformity | **blocked** | no palette (§7); no closed term vocabulary (`EC-N1`) |

---

```
pass_1                 ACTIVE
boundary_declared      false
observation_card       BLANK
disposition_inference  FORBIDDEN
```

*Skeleton prepared 2026-08-22. No doctrine created. No palette authored. No prompt written. No
candidate ranked. Sources: `CONDUCTOR_SCORE.yaml` v1.1.0 · `CUE_SHEET v1.1` · `VPD-001` v0.1 ·
`VOICE_PRIORITY_MAP.yaml` v1.0.0 · `MUSIC_OVERLAY_TIMELINE.yaml` v1.0.0 ·
`EXECUTIVE_RULINGS.yaml` v1.5.0.*
