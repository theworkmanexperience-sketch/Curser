# VPD-001 — Voice Priority Doctrine
## Governance Status
Document Type: **Doctrine (governed artifact)** · Status: **v0.2 — TRANSCRIPTION + Executive Dispositions**
Authorized: Executive, 2026-08-22, Phase 3 Continuation communiqué item 2
Instruction of record: *"VPD-001 is hereby authorized as a governed artifact using the
Executive-approved language developed during this session. **Engineering shall transcribe only. No
synthesis or expansion.**"*
Prepared by: Music Systems Engineer · Custody: `MACHINE` transcription of `EXECUTIVE`-custody sources

**v0.1 → v0.2:** Executive Dispositions of 2026-08-22 (EMB-CUE-03 Continuation) recorded at §5.
Three of the four `AWAITING_EXECUTIVE_INPUT` fields are resolved; two new questions are raised.

> **This document contains no engineering-authored doctrine.** Every provision below is quoted
> verbatim from a governed artifact or an Executive statement, with its citation. Where the record is
> silent, §3 says so and marks the field `AWAITING_EXECUTIVE_INPUT` rather than filling it.

---

## 1. The transcribed provisions

### P1 — The Yield Law
**Source:** `CONDUCTOR_SCORE.yaml` v1.1.0 → `global_behaviour_law.yield_law`, carried forward from
`CUE-02A_SPEC` (Pass 1, 2026-08-21)

> *"Any cue whose family is CONVERSATION is a bed under speech and must yield. Ducking target −18 dB
> under dialogue, carried forward from CUE-02A_SPEC, which is the only PDR-adjacent figure in
> evidence. Between answers a bed may breathe upward no more than +3 dB and must return before the
> next question lands. Fail condition: at −18 dB under two minutes of gauntlet audio, any word
> requiring effort fails the candidate regardless of musical merit."*

**Relation expressed:** music yields to speech. **Scope as written:** CONVERSATION family.

### P2 — The Speech Band Rule
**Source:** `CONDUCTOR_SCORE.yaml` v1.1.0 → `global_behaviour_law.speech_band_rule`

> *"keep approximately 1–4 kHz uncluttered in every cue that runs under speech"*

**Scope as written:** every cue that runs under speech — not family-limited.

### P3 — The VO Rule
**Source:** `CONDUCTOR_SCORE.yaml` v1.1.0 → `global_behaviour_law.vo_rule`

> *"Voice-over windows (VOICE_OVER_REGISTRY VO01–VO04) duck like dialogue. VO is excluded by the
> Director's Notes from every silence zone, so no cue needs to plan for VO inside SIL-01, SIL-02 or
> the R46 carve-out."*

**Relation expressed:** VO receives the **same** treatment as dialogue. *Like*, not *above* or
*below*.

### P4 — VO Placement Boundaries
**Source:** `VOICE_OVER_REGISTRY.yaml` v0.1.0 → `vo_placement_boundaries`, per Director's Notes

> *"silence zones (S12, R46, proclamations) EXCLUDED from VO per Director's Notes"*

### P5 — The Silence Law, as ruled
**Source:** Executive Ruling ESS-004, Executive Producer, 2026-08-22 (session ELS-001)

> *"`MANDATORY_SILENCE` is hereby defined as prohibiting WE CAPE-added non-diegetic score only.
> Existing production audio — including speech, ambience, engine noise, wind, and any source audio
> captured as part of the documentary record — shall remain permissible unless otherwise directed by
> an Executive PDR."*

**Relation expressed:** in a silence zone, **voice is permitted and added score is not.** This is the
only provision in the record that resolves a music-versus-voice contest by rule rather than by level.

### P6 — Why the conversation beds exist
**Source:** `CUE_SHEET v1.1`, CUE-02a `reason` (ARCHITECTURE APPROVED, Chairman, 2026-08-21)

> *"Exists to yield — hold a floor under 45 voices so listening feels effortless and no answer
> competes with music."*

### P7 — Why the civic silence exists
**Source:** `CUE_SHEET v1.1`, SIL-01 `reason` (ARCHITECTURE APPROVED, Chairman, 2026-08-21)

> *"Exists as absence — the town's own words (librarian, council, two proclamations, a first ride)
> must carry their full civic weight unassisted."*

### P8 — Doctrine and mechanism are different layers
**Source:** Executive, 2026-08-22, Phase 3 Continuation communiqué item 5

> *"Voice Priority Doctrine governs behavior. 'YIELD' is a narrative doctrine. Existing behavioral
> states (including DUCK) remain implementation mechanisms unless and until Road Soul behavior
> vocabulary is formally revised."*

**Effect on the vocabulary:** `YIELD` is **not** an eleventh behaviour state. It is doctrine; `DUCK`
is the mechanism that enacts it. The ten-state vocabulary is unchanged. This closes blocker **B5**
and does not reopen `RSB-AUDIT-001` gap **G2**.

### P9 — Music and orientation
**Source:** Executive Producer, 2026-08-22, EVS-001 Pass 1, observation at 00:27:10

> *"Map overlay introduces the next riding segment. Audience attention is divided between route
> information and rider staging. **Music should support orientation rather than lead the scene.**"*

**Recorded with its class.** ER-003 Layer 3 — Executive Interpretation. Custody `EXECUTIVE`. It is
the only statement in the record that addresses music priority against a **non-speech** attention
demand. It is transcribed here because it was issued this session; **it is not generalized**, and no
rule is derived from it.

---

## 2. What the transcription establishes

Restatement with citations only. No provision is combined with another to produce a new rule.

| relation | established by | scope as written |
|---|---|---|
| Music yields to speech | P1, P6 | CONVERSATION family (P1); "45 voices" (P6) |
| Music yields to speech in **every** cue, in the speech band | P2 | any cue running under speech |
| VO is treated **as** dialogue | P3 | VO01–VO04 |
| VO is excluded from silence zones | P3, P4 | SIL-01, SIL-02, R46 |
| In a silence zone, voice is permitted and added score is not | P5 | all three conducted silences |
| `YIELD` is doctrine; `DUCK` is its mechanism | P8 | platform-wide |
| Music supports orientation rather than leading | P9 | **one observation, one span, not generalized** |

---

## 3. What the record does NOT establish — and why it matters here

### 3.1 There is no priority order among voices
**The doctrine is named *Voice Priority*. The governed record contains no priority relation between
one voice and another.**

Every provision above orders **music against voice**. None orders **voice against voice**. P3 is
explicit that VO is treated *like* dialogue — which is parity, not precedence. Nothing states what
governs when host VO, interview speech and civic speech occupy the same instant.

Transcription cannot supply this. Assembling one from P1–P9 would be synthesis, which item 2
forbids in the same sentence that authorizes this document.

### 3.2 The collision is not hypothetical — measured
`VOICE_PRIORITY_MAP` v1.0.0, from the lock SRT (`89d61f96…a1c6b`, 2291 cues) against
`VOICE_OVER_REGISTRY` v0.1.0:

| VO window | span | duration | observed speech inside it | |
|---|---|---|---|---|
| VO01 · day_brief | 01:13–01:51 | 38 s | 37.0 s | **97.4%** |
| VO02 · ride_narration | 27:02–29:10 | 128 s | 69.0 s | **53.9%** |
| VO03 · service_wrap | 54:36–55:24 | 48 s | 42.0 s | **87.5%** |
| VO04 · wrap_tease | 79:44–80:46 | 62 s | 52.5 s | **84.7%** |
| **all four** | | **276 s** | **200.5 s** | **72.6%** |

**Every VO candidate window already carries observed speech.** Placing host narration in any of them
puts two voices in the same instant. The collision is **prospective** — no VO has been authored — but
it is present in all four windows, not one.

### 3.3 The fields this document cannot fill

```yaml
voice_priority_order:        AWAITING_EXECUTIVE_INPUT
  # candidates present in the lock, from governed registries, unordered:
  #   host_vo            VOICE_OVER_REGISTRY VO01-VO04
  #   interview_speech   lock SRT, rider interviews
  #   civic_speech       lock SRT, proclamations and council (SIL-01)
  #   contributed_audio  CONTRIBUTED assets carrying speech

collision_resolution:        AWAITING_EXECUTIVE_INPUT
  # what governs when two permitted voices occupy the same instant.
  # P3 establishes VO is treated LIKE dialogue. It does not say what happens
  # when VO and dialogue coincide, which the measurement in 3.2 shows they do
  # in 72.6% of every VO window.

yield_scope_beyond_conversation: PARTIALLY_STATED
  # CORRECTED on inspection of the artifact rather than asserted from the law.
  # P1's -18 dB is written for CONVERSATION. CUE-03's own record in
  # CONDUCTOR_SCORE v1.1.0 carries DUCK target_db -12 with sidechain
  # "voice-over and any diegetic announcement only" - so a MOTION figure DOES
  # exist per-cue. What does not exist is a FAMILY-level rule: -12 is recorded
  # for CUE-03 and CUE-07 individually, not as a MOTION law, and no provision
  # states which governs if the two disagree.
  family_level_rule:         AWAITING_EXECUTIVE_INPUT
  # Also unstated: CUE-03's sidechain names "voice-over and any diegetic
  # announcement only" - it does NOT name interview speech, which the
  # measurement shows occupies 58.0% of the cue. Whether a MOTION bed ducks to
  # interview speech at all is unstated.

p9_scope:                    AWAITING_EXECUTIVE_INPUT
  # "Music should support orientation rather than lead the scene" was issued
  # for one span during EVS-001 Pass 1. Whether it is a general doctrine or an
  # observation about 00:27:10 is not stated, and is not inferred here.
```

---

## 4. Status and effect

**v0.1 is a complete transcription of an incomplete record.** It is citable for P1–P9 exactly as
written. It is **not** citable for a priority order, because it contains none.

**Blocker `B1` is closed** to the extent the record allows: `VPD-001` now exists as a governed
artifact and the Executive Music Brief may cite it. **Four fields remain `AWAITING_EXECUTIVE_INPUT`**,
and §3.3 states each one's exact question rather than a default.

**No doctrine was created in producing this document.** Per the Phase 3 Continuation instruction, and
per `DOC-CAND-001`: the platform prepares decisions; it does not make artistic ones.

---
*Transcribed 2026-08-22. Sources: `CONDUCTOR_SCORE.yaml` v1.1.0 · `CUE_SHEET v1.1` ·
`VOICE_OVER_REGISTRY.yaml` v0.1.0 · Executive Ruling ESS-004 · Phase 3 Continuation communiqué ·
EVS-001 Pass 1 observation. Measurement: `VOICE_PRIORITY_MAP.yaml` v1.0.0.*


---

## 5. Executive Dispositions — 2026-08-22, EMB-CUE-03 Continuation

### D1 — Scope confirmed *(resolves §3.1, §3.3 fields 1 and 2)*

> *"VPD-001 scope is confirmed. It governs the relationship between music and spoken communication
> only. It does not determine editorial precedence among simultaneous speech sources."*

**The §3.1 gap is closed by exclusion rather than by filling.** Precedence among voices is not a
missing provision — it is **out of scope**. `voice_priority_order` and `collision_resolution` are
struck from §3.3 and no longer await input.

**One consequence worth stating, and it is not a music question.** The lock has already resolved
speech-versus-speech for every voice it contains — the edit decided who speaks when. **Host VO is
the exception: `VO01–VO04` are not in the lock.** Authoring VO into windows that already carry
72.6% observed speech (§3.2) will create simultaneity the edit never adjudicated. Under D1 that is
an **editorial** decision at VO authoring, not a VPD-001 provision. Recorded so it is not mistaken
for settled.

### D2 — MOTION yields to interviews and narration alike *(resolves §3.3 field 3)*

> *"All Level 1 and Level 2 spoken communication invokes the Voice Priority Doctrine. MOTION cues
> shall yield to interviews and narration alike. Differences in implementation remain an engineering
> concern, not a doctrinal one."*

**The artifact contradicted this and has been corrected at the generator.** `CUE-03`'s `DUCK`
sidechain read *"voice-over and any diegetic announcement only"* — which **excluded interview
speech**, 58.0% of the cue as measured.

```
was : sidechain "voice-over and any diegetic announcement only"
now : sidechain "interviews, narration, voice-over and any diegetic announcement"
      target_db -12  (UNCHANGED — the ruling extended WHAT is yielded to, not BY HOW MUCH)
```

Encoded in `gen_artifacts.py` with `doctrine_ref` and the superseded value retained as
`prior_sidechain`. **The artifact is deliberately not regenerated yet:** `CONDUCTOR_SCORE`
regenerates on the ESS-002 disposition, which precedes gate-open, which precedes any generation.
Regenerating now would be a change to a governed artifact outside a governed trigger.

**Term flagged, not guessed.** *"Level 1 and Level 2 spoken communication"* has no definition in the
record. The platform's only Levels are ER-003's three observation layers — Timeline Mechanics,
Screen Presentation, Executive Interpretation — which classify **how an observation entered the
record**, not kinds of speech. The operative clause (*"interviews and narration alike"*) is
unambiguous and has been implemented; the taxonomy term is recorded as
`AWAITING_EXECUTIVE_INPUT` and nothing has been inferred from it.

### D3 — P9 applies to every cue *(resolves §3.3 field 4, and raises a new question)*

> *"P9 applies to every Road Soul cue, including CUE-03."*

**Recorded.** And it produces a collision that should be surfaced before composition, not after.

P9 says music should **support orientation rather than lead the scene.** `LEAD` is a behaviour state
specified as *"music carries the span"*, and it is in the signature of every MOTION and CELEBRATION
cue. **Applied without condition, P9 and `LEAD` say opposite things.**

**Measured, `BEHAVIORAL_FINGERPRINT` v1.0.0 — where orientation elements actually occur:**

| | orientation-bearing share of span |
|---|---|
| CUE-01 · CUE-10 · CUE-06 | 100.0% · 98.4% · 87.5% |
| **CUE-03** (MOTION) | **64.4%** |
| CUE-04 · CUE-02c · CUE-08 | 11.6% · 6.9% · 5.7% |
| **CUE-07** (MOTION) · CUE-09a · CUE-09b · CUE-02b · CUE-05 | **0.0% — five cues** |

**10 of 15 cues carry orientation elements. Five carry none.** The two MOTION cues sit at opposite
ends — CUE-03 at 64.4%, CUE-07 at **0.0%** — and both carry `LEAD`.

**CUE-07 is the test case.** It runs 153 s with **0.7% speech, no titles, no map elements, no
graphic overlays, and a 152.5-second speech-free window.** Applied unconditionally, P9 instructs the
music to support orientation across a span containing nothing to orient to.

Two readings, neither adopted:

| | reading | consequence |
|---|---|---|
| **R1** | P9 binds **wherever an orientation element is present** | compatible with `LEAD` elsewhere; CUE-03 bound, CUE-07 not |
| **R2** | P9 binds **unconditionally** | `LEAD` is superseded wherever it applies — which is a **revision of the behaviour vocabulary**, and **P8 holds the vocabulary unchanged "unless and until formally revised"** |

**R2 cannot be adopted silently without contradicting P8.** No state has been altered.

```yaml
p9_scope_within_a_cue:   AWAITING_EXECUTIVE_INPUT   # R1 conditional, or R2 unconditional
p9_vs_lead:              AWAITING_EXECUTIVE_INPUT   # if R2, LEAD requires formal revision (P8)
```

### D4–D7 — recorded, no engineering action beyond compliance

| | disposition | effect here |
|---|---|---|
| **D4** | No gate carve-out. Skeleton may mature; no composition, prompt or realization | `EMB-CUE-03` remains a SKELETON. Nothing generated |
| **D5** | Palette stays Executive-owned and `AWAITING_EXECUTIVE_INPUT` | §7 of the skeleton unchanged; nothing inferred |
| **D6** | ESS-002 retains the boundary. No inference, no provisional movement | every artifact continues to cite `00:29:10.000` as the **cue-sheet** value with the boundary marked unresolved |
| **D7** | Preserve measured transitions as **fingerprints, not arguments** | `BEHAVIORAL_FINGERPRINT.yaml` v1.0.0 — 15 cues, every row a measurement with a method, no row recommending anything |

---

## 6. Status after v0.2

| field | v0.1 | v0.2 |
|---|---|---|
| `voice_priority_order` | awaiting | **STRUCK — out of scope (D1)** |
| `collision_resolution` | awaiting | **STRUCK — out of scope (D1)**, with the VO-authoring note above |
| `yield_scope_beyond_conversation` | partially stated | **RESOLVED (D2)** — MOTION yields to interviews and narration; family-level rule still open |
| `p9_scope` | awaiting | **RESOLVED (D3)** — applies to every cue |
| `level_1_2_taxonomy` | — | **NEW — awaiting** (D2) |
| `p9_scope_within_a_cue` / `p9_vs_lead` | — | **NEW — awaiting** (D3) |

**Two closed by ruling, one closed by exclusion, three raised.** No doctrine was created in producing
this version.
