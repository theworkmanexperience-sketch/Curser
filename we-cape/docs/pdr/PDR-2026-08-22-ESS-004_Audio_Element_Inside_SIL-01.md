# PDR-2026-08-22-ESS-004 — Audio element inside SIL-01 (silence-law integrity)
## Governance Status
Document Type: Production Decision Record · Status: **OPEN — AWAITING EXECUTIVE DISPOSITION** · Date: 2026-08-22
Authority: Executive Producer · Origin: Final Executive Disposition, Sprint 3A (2026-08-22), item 2
Reference Execution: RE-001 · Finding ID: **SLF-01** · Related deltas: **D-18**, **D-22**
Boundary: ADRs govern the platform · PDRs govern productions.
**This is the highest-consequence of the four. It touches the covenant.**

## Question
The audio-lane element **`NOTOR1OUS_CARAVAN_2_`** occupies **00:33:37.708 – 00:34:39.667** — 61.958 s
lying **entirely inside SIL-01 CIVIC_SILENCE (00:31:43 – 00:38:52)**. Is this a breach of the silence
law, permitted diegetic audio, or something to be removed?

## Evidence
| kind | value |
|---|---|
| Element | `NOTOR1OUS_CARAVAN_2_`, lane −1, in **00:33:37.708**, out **00:34:39.667**, duration **61.958 s** |
| Provenance | FCPXML asset `r95`, `media-rep src = file:///Volumes/10TB/AlphaRoundUp_2026/CONTRIBUTED/Videos_Alpha RoundUp/NOTOR1OUS_CARAVAN_2_.mp4` — a **contributed video's audio**, `hasVideo=1 hasAudio=1` |
| Contrast | the only element in the timeline sourced from `/Soundtrack/` is `KICKSTANDS UP v1.wav` (00:00:00.000–00:01:16.417). By path provenance, `NOTOR1OUS_CARAVAN_2_` is **not a score asset** |
| Covenant | `SIL-01 CIVIC_SILENCE, mode: MANDATORY_SILENCE, reason: "Exists as absence — the town's own words (librarian, council, two proclamations, a first ride) must carry their full civic weight unassisted"` (CUE_SHEET v1.1) |
| Picture at that moment | spine clip 015 (proclamation footage); SRT cues 1137–1142 are the town proclamation being read ("And whereas…") |
| **Not determined** | **whether the element's audio content is musical.** Its source volume `/Volumes/10TB` was not mounted for RE-001 (delta D-22), so the media was never inspected |
| Also relevant | a compound clip named `Mark S. Tillman (GP)_CARAVAN` sits on the spine at 00:36:00–00:36:49 — the same contributed material appears in picture ~2.5 min *after* this audio placement |

## Why this was not auto-resolved
RE-001 classified this **UNCERTAIN** and escalated rather than judging it. Three reasons, all of which
still hold:
1. **The content was never heard.** Calling it a silence-law breach would have been an inference about
   audio nobody in the run listened to.
2. **Provenance cuts the other way.** It is contributed source audio, not score. The covenant forbids
   *music* over the civic zone; whether it forbids a contributed clip's own sound is a reading of the
   covenant, not a measurement against it.
3. **It may be intentional.** Audio arriving ~2.5 min before its picture is a recognised editorial
   device (audio pre-lap). This could be craft, not leakage.

## What must happen before this can be decided
**A human has to listen to 00:33:37.708 – 00:34:39.667 in the locked cut.** That is a 62-second task
and it collapses most of the ambiguity. RE-001 could not do it: `rm`-blocked sandbox, offline source
volume, and — more importantly — classifying audio as "musical" is exactly the kind of judgement the
no-silent-recovery constraint exists to prevent an implementation from making alone.

## Options
**A — Permitted diegetic audio; covenant intact.** If the content is the caravan's own ambience/engine
sound, SIL-01 means *no score*, not *no sound*, and nothing changes. Record the reading explicitly so
the covenant's scope is written down rather than assumed.

**B — Breach; remove or move the element.** If the content is musical, it violates SIL-01 as written.
Remedies: remove; move it out of the zone; or re-cut so its picture and audio coincide.

**C — Amend the covenant.** Carve out contributed-source audio from SIL-01 explicitly. **Not
recommended without deliberate intent** — SIL-01's stated reason is that the town's words carry
"unassisted", and a carve-out weakens the strongest editorial commitment in the cue sheet.

**D — Defer pending audio inspection.** Formally record that the decision is blocked on a 62-second
listen, with a named owner.

## Downstream impact
- Regenerates on decision: `CONDUCTOR_SCORE.yaml` (SIL-01 behaviour states, reconciliation verdict for
  this element), `EDITORIAL_SYNCHRONIZATION.yaml`.
- If B: the picture lock may need to reopen, invalidating RE-001 input hash 2 for future comparison.
- **Precedent value beyond this element:** whatever is decided defines whether MANDATORY_SILENCE means
  "no score" or "no sound" for the rest of the platform. That definition should be written into the
  silence law once, here.

## Blocks
**All downstream MIE work.** Every cue adjacent to SIL-01 (`CUE-03`, `CUE-04`) inherits its APPROACH
and RETURN behaviour from the zone's definition. Should be dispositioned together with
`PDR-2026-08-22-ESS-002`, which concerns the same zone's left boundary.

## Decision
> _To be recorded by the Executive Producer._

**Audio inspected (00:33:37.708–00:34:39.667):** ☐ yes ☐ no — **by / date:** ______
**Content classified as:** ☐ musical ☐ non-musical diegetic ☐ mixed ☐ other: ______
**Selected option:** ☐ A ☐ B ☐ C ☐ D ☐ Other: ______
**Silence-law scope now reads:** ☐ no score ☐ no sound ☐ other: ______
**Rationale:** ______
**Dispositioned by / date:** ______

---

## Amendment 1 — 2026-08-22 (evidence only; no decision changed)
**Raised by:** implementation, during the Gate Ledger Standard work.
**Effect:** narrows the question. Does not answer it.

SOP-06 Phase A4 (GATE 1 — Timeline Audit) records the CONTRIBUTED custody exception for this
production verbatim as: *"every clip resolves to ORIGINAL or cleared-CONTRIBUTED custody (currently
cleared: **NOTOR1OUS ×2** only)."*

The element in question is therefore **already custody-cleared at GATE 1**. Two consequences:

1. **The element's presence in the timeline is not at issue.** It is one of exactly two cleared
   contributed items in the whole lock. Option B's "remove it" framing should be read as *remove it
   from this window*, never as *it should not be here*.
2. **The open question is narrower than first stated.** It is only whether the audio *content* is
   musical for silence-law purposes — which is still resolved by the 62-second listen, and which still
   sets the platform-wide reading of MANDATORY_SILENCE.

Options A–D stand unchanged. Status remains **OPEN — AWAITING EXECUTIVE DISPOSITION**.

---

## Amendment 2 — 2026-08-22: reframed as an Executive Listening Session; **options corrected**
**Reframe (Executive direction).** This PDR is conducted as **ELS-001 — Executive Listening Session**.
Purpose: determine the semantic meaning of `MANDATORY_SILENCE`. Deliverable: one Executive ruling.
Expected duration ~5 minutes, though the media span is 62 seconds. Brief and evidence:
`docs/reviews/ELS-001_MANDATORY_SILENCE_LISTENING_BRIEF.md`.

**Correction to this PDR's own framing — the question is not binary.**
Options A–D above were built on *no score* versus *no sound*. That is insufficient. The element is a
**contributed video's own audio track**; if its content is music that was playing *in the scene*, it is
**diegetic**, and neither original option covers it. "No score" permits it as location sound; "no
sound" forbids it along with engine noise and room tone. The covenant's test — the town's words
carrying their weight *"unassisted"* — is genuinely arguable in that case.

The ruling therefore requires **three** options, carried in ELS-001 §5:
1. No **non-diegetic** score — diegetic/source audio permitted
2. No **music of any kind**, diegetic or not
3. No sound but the primary speech

Options A–D above remain valid as *dispositions of this element*. The semantic ruling is the new
1/2/3. Raised before the session rather than discovered after it.

**Objective evidence now attached (ELS-001 §4).** A three-way measurement against known controls
establishes one fact and refuses to establish the other:
- The element is **audible** — the target span carries **26.59 %** of total energy in 80–250 Hz against
  **3.87 %** in an otherwise-comparable span of the same silence zone, never drops out, and is the most
  tonal of the three spans. Row "inaudible / muted" is unlikely.
- The measurements **do not classify the content**. Steady, tonal, low-frequency and beatless is equally
  consistent with a musical pad and with engine rumble. No verdict is offered, per
  `WET-SPEC-REPORT-001` and the run's no-silent-recovery constraint.

Status remains **OPEN — AWAITING EXECUTIVE DISPOSITION**.

---

## Amendment 3 — 2026-08-22: Executive Listening Finding (ELS-001). Content determined; diegesis NOT.
**Finding, as issued by the Executive Producer after listening:**

> *"The target span contains a composite production audio bed consisting of multiple audible elements,
> including music/vocals, engine rumble, wind, and speech. The Executive cannot conclude that the
> audible musical content is exclusively editorial (non-diegetic) based on the available proxy."*

### What this settles
| question | status |
|---|---|
| Is the element audible? | **YES** — confirmed by ear and by measurement (26.59% of energy in 80–250 Hz vs 3.87% in the element-free control). The "muted / inaudible" option is struck |
| Does the span contain musical content? | **YES** — music **and vocals** |
| Does it contain non-musical content? | **YES** — engine rumble, wind, speech |
| Is the musical content editorial (non-diegetic)? | **UNDETERMINED on the available proxy** |

### Instrument/ear agreement
Every measurement in ELS-001 §4 is consistent with a composite bed and is explained by it:
low-band energy 26.59% (engine + musical bass), pitch-class concentration 51.1% sitting **between**
the known-score control (69.9%) and the element-free control (38.5%) — dilution by non-musical
sources — and beat periodicity 0.04 against the score control's 0.70, because the musical pulse is
buried under mechanical and ambient content. Two independent methods, one conclusion (DOC-001).

### The consequence the Executive Team should weigh before ruling — **decidability**
The finding does not block a ruling. It blocks *one* of the three:

| definition | applicable to this evidence? | outcome if chosen |
|---|---|---|
| **1 — no non-diegetic score** | **NO.** Requires a diegesis judgement the Executive has expressly declined to make on the proxy | ESS-004 remains OPEN pending `/Volumes/10TB` (delta D-22); the gate stays CLOSED indefinitely |
| **2 — no music of any kind** | **YES.** Music/vocals are audibly present; diegesis is irrelevant to the test | Covenant breached; element disposition follows |
| **3 — no sound but the primary speech** | **YES.** Engine, wind and music are all present | Covenant breached; element disposition follows |

**Definition 1 is not wrong — it is currently unrulable.** It asks a question the platform's own governed
artifacts cannot answer, and would do so again for every future silence-zone element. A definition the
platform cannot adjudicate from the evidence it holds will keep producing UNDETERMINED. That is a
property of the definition, not of this element, and it is the strongest practical argument in the
record for choosing 2 or 3 — or for choosing 1 **and** accepting that silence-zone adjudication
requires camera-original source media on hand, which is a capture-side commitment (see `DWR-032`,
`CAR-004` §5 Tier 3).

### One further observation, raised because it strengthens the case rather than the ruling
The finding names **vocals**. The covenant's stated reason for SIL-01 is that *"the town's own words …
must carry their full civic weight unassisted."* Audible vocals under a civic proclamation are
competing speech, not merely competing music — a materially stronger concern than an instrumental bed,
and one that reads on the covenant's own terms regardless of which definition is adopted.

Status remains **OPEN — AWAITING EXECUTIVE RULING** on definitions 1 / 2 / 3.

---

# EXECUTIVE DISPOSITION — 2026-08-22 · ESS-004 · **CLOSED**

**Authority:** Executive Producer · **Session:** ELS-001 · **Ruling ID:** `ESS-004-RULING`
**Status transition:** OPEN — AWAITING EXECUTIVE RULING → **DISPOSITIONED / CLOSED**

## D.1 The ruling as issued

> ELS-001 confirms that the evaluated span contains a composite production soundscape. The available
> proxy does not conclusively distinguish the provenance of the musical content, and that distinction
> is not required for this ruling.
>
> **`MANDATORY_SILENCE` is hereby defined as prohibiting WE CAPE-added non-diegetic score only.
> Existing production audio — including speech, ambience, engine noise, wind, and any source audio
> captured as part of the documentary record — shall remain permissible unless otherwise directed by
> an Executive PDR.**

**Definition selected:** 1 — no WE CAPE-added non-diegetic score.
**Disposition of the element (`NOTOR1OUS_CARAVAN_2_`, 2017.708–2079.667 s):** **PERMITTED — covenant intact.**
No removal, no move, no re-cut. `SLF-01` → **RESOLVED**.

## D.2 What the ruling changed that the engineering record did not anticipate

The engineering record (Amendment 3, and ELS-001 §6.1) argued that definition 1 was *"currently
unrulable"* because it required a diegesis judgement the proxy could not support. **That argument was
incomplete, and this disposition supersedes it.**

Amendment 3 assumed the test for definition 1 had to be **acoustic** — decide from the sound whether
the music is scored or in-world. On that assumption the conclusion held. The Executive did not accept
the assumption. The ruling relocates the test to **provenance**: an element breaches a silence zone
if and only if **WE CAPE added it as score**. That is not a listening question at all. It is a
question the locked FCPXML already answers, in writing, for every element in the timeline.

The lesson is recorded here because it generalizes: *the engineering record correctly identified that
the question as posed was undecidable, and then wrongly treated the posing as fixed.* A definition
that is undecidable under one test may be trivially decidable under another. Reframing the test is an
Executive prerogative that engineering analysis should surface as an option rather than foreclose.

## D.3 The test, as now implemented (machine-checkable, no listener required)

Read the `media-rep` source path of each audio-lane element intersecting a silence zone:

| path signature | classification | verdict |
|---|---|---|
| `…/Soundtrack/…` | `SCORE_ASSET` — WE CAPE-added | **BREACH** |
| `…/Original Media/…` (P2_CHRONO_SETS) | `PRODUCTION_ORIGINAL_MEDIA_AUDIO` | PERMITTED |
| contributed video asset | `CONTRIBUTED_VIDEO_AUDIO` | PERMITTED |

This check runs from the locked FCPXML alone. It requires neither the master audio, nor the offline
`/Volumes/10TB` camera originals, nor a human listener — which **retires delta D-22 as a dependency**
for silence-zone adjudication (D-22 itself remains CLOSED-AS-NOTED for content inspection).

## D.4 Result of the regeneration under this definition

| zone | span | intersecting audio elements | breaches | state |
|---|---|---|---|---|
| SIL-01 | 00:31:43.000–00:38:52.000 | 2 — `NOTOR1OUS_CARAVAN_2_` (CONTRIBUTED_VIDEO_AUDIO) · `Map traavel to Smyrna Event Center-26` (PRODUCTION_ORIGINAL_MEDIA_AUDIO) | **0** | INTACT |
| SIL-02 | 00:52:04.000–00:53:49.000 | 0 | **0** | INTACT |
| R46 carve-out | 00:39:07.000–00:39:59.000 | 0 | **0** | INTACT |

**TOTAL BREACHES: 0 · COVENANT: INTACT.** The lock's only WE CAPE-added score asset,
`KICKSTANDS UP v1` (00:00:00.000–00:01:16.417), lies outside every silence zone.

## D.5 The observation that survives the ruling, unresolved

Amendment 3 noted that the finding names **vocals**, and that SIL-01's stated reason is that *"the
town's own words must carry their full civic weight unassisted."* Under this ruling those vocals are
**permitted**, because they are documentary record rather than WE CAPE-added score. The covenant is
intact as written.

This is nonetheless a place where the covenant's **letter** and its **stated intent** can diverge: an
audible vocal under a civic proclamation competes for the audience's attention whatever its
provenance. The ruling's own closing clause — *"unless otherwise directed by an Executive PDR"* — is
the mechanism for closing that gap element by element if the Executive later wishes to. **No such
direction is issued here, and none is implied.** It is recorded so that a future reader does not
mistake silence on the point for absence of the point.

## D.6 Artifacts regenerated under this disposition

Regeneration run `WECAPE-AR2-ESS004-REGEN-20260822-174500`. Per DOC-002 — regenerate, never patch —
no artifact was hand-edited; all outputs come from `intelligence/p2/ess/scripts/gen_artifacts.py`
re-run against the unchanged four authoritative inputs.

| artifact | version | note |
|---|---|---|
| `CONDUCTOR_SCORE.yaml` | 1.0.0 → **1.1.0** | silence law re-encoded as provenance behavior; `silence_law_definition` + `silence_law_compliance` blocks added |
| `EDITORIAL_SYNCHRONIZATION.yaml` | 1.0.0 → **1.1.0** | audio-element provenance classification carried on sync rows |
| `ESS_VALIDATION_REPORT.md` | regenerated | D-18 CLOSED by ruling · D-22 dependency retired · **D-26 added** |
| `PRODUCTION_INTELLIGENCE_SEED.yaml` | regenerated | seed reflects intact covenant |
| `CAPTION_REGISTRY.yaml` | 0.2.0 → **0.2.1** | **serialization only** (D-26); zero content change |
| `VISUAL_EVENT_REGISTRY.yaml` | 1.0.0 → **1.0.1** | **serialization only** (D-26); zero event-content change |

**D-26 — `YAML_SEXAGESIMAL_TIMECODE`:** a defect found *during* this regeneration, unrelated to the
ruling. Under YAML 1.1, a bare `start_tc: 00:31:43.000` parses as the float `1903.0`, not the string
`"00:31:43.000"`. It was present in **every YAML artifact of the RE-001 baseline**. All timecodes are
now quoted at write time. The RE-001 archived copies retain the defect **by design** — an archived
reference execution is immutable, and its scorecard now carries the finding.

## D.7 Gate consequence

`DOWNSTREAM_AUTHORIZATION_GATE.yaml`: ESS-004 → `DISPOSITIONED`. **The gate REMAINS CLOSED.**
Three PDRs — ESS-001, ESS-002, ESS-003 — are still open, and `on_open` requires all four.
Next in the confirmed disposition order: **ESS-002**.

**Ruled by:** Executive Producer · **Date:** 2026-08-22 · **Recorded by:** Implementation Engineer
