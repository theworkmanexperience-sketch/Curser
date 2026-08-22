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
