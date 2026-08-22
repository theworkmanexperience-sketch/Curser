# PDR-2026-08-22-ESS-001 — TIMELINE_REGISTRY S16: segment label vs observed illumination
## Governance Status
Document Type: Production Decision Record · Status: **OPEN — AWAITING EXECUTIVE DISPOSITION** · Date: 2026-08-22
Authority: Executive Producer · Origin: Final Executive Disposition, Sprint 3A (2026-08-22), item 2
Reference Execution: RE-001 (`WECAPE-AR2-SPRINT3A-20260822-114028`) · Conflict ID: **VCONF-01**
Boundary: ADRs govern the platform · PDRs govern productions.

## Question
TIMELINE_REGISTRY segment **S16 (00:58:43–01:06:25)** carries `activity: bike_night_arrivals`.
The picture in that span is daylight. Does the registry label change, does the segment boundary
change, or does the label stand as an editorial shorthand?

## Evidence
| kind | value |
|---|---|
| Registry value | `S16 span "58:43-66:25" activity: bike_night_arrivals interview_count: 8 participants: [R68-R75]` (TIMELINE_REGISTRY 1.0.0) |
| Instrument measurement | mean luma **130.7** over the span; warm ratio R/B **1.04** (neutral daylight) |
| Instrument measurement | sustained low-light onset at **3984.5 s = 01:06:24.5**, first night sample 01:06:24, last day sample 01:06:21 |
| Observation | bright daylight, blue sky, hotel parking lot: arrivals, machines parked, riders addressing camera (`VE-034` DAYLIGHT_LOT_GATHERING_AND_INTERVIEWS, confidence HIGH) |
| Corroboration | ENERGY_CURVE gives S16 energy 4 "night arrivals, engines + crowd" — same assumption, same span |
| Source | `Filmage_Editor.mp4` SHA-256 `a53655fc…0f47e8` (320×180 proxy — see D-24) |

## What is *not* in dispute
The **boundary** is right. The registry places the S16/S17 edge at 3985 s; the instrument places the
day→night transition at 3984.5 s. Agreement to **0.5 s**, inside the observation grid (delta D-17).
Whoever set that boundary put it in exactly the right place. Only the label disagrees with the picture.

## Why this was not auto-resolved
Registries outrank visual observation (ADR-009). DIE-V recorded CONFLICTED and stopped. A label is also
not obviously a factual claim — "bike night arrivals" may mean *arrivals for bike night*, which happen
in daylight, rather than *arrivals at night*. That is an editorial reading, and reading is not DIE's.

## Options
**A — Label stands; annotate only.** Add a clarifying note to S16 recording that the span is daylight
and that "bike night" names the destination, not the light. Cheapest; preserves every downstream
reference to S16. Risk: the next reader makes the same inference, and MIE cue colour for CUE-08
(`NIGHT_ARRIVALS`, CELEBRATION, 58:43–66:48) may have been chosen against a night image that is not there.

**B — Rename the segment.** e.g. `daylight_gathering_pre_bike_night`. Truthful to picture. Requires
TIMELINE_REGISTRY 1.0.0 → 1.1.0, and CUE-08's name `NIGHT_ARRIVALS` becomes misleading for the first
7 m 42 s of its own span.

**C — Split S16 at the measured transition.** S16a daylight gathering 58:43–01:06:24, S16b night
transition 01:06:24–01:06:48. Most faithful; largest blast radius — segment IDs are referenced by
ENERGY_CURVE, DOCUMENTARY_PROGRESSION, EDITORIAL_SYNCHRONIZATION and the cue sheet.

## Downstream impact
- **CUE-08 `NIGHT_ARRIVALS`** (58:43–66:48, CELEBRATION, energy 4) is written against this span. If the
  first 7 m 42 s is daylight, the cue's visual premise is wrong even though its timecodes are right.
  This is the one place where the label actually reaches the music.
- Regenerates on decision: `EDITORIAL_SYNCHRONIZATION.yaml`, `CONDUCTOR_SCORE.yaml` (both are
  regenerate-on-mismatch, never hand-edited).
- No effect on Step 0, the offset model, or any timing claim.

## Blocks
Downstream MIE Pass 4 (CELEBRATION family) — CUE-08 is a Pass 4 cue.

## Decision
> _To be recorded by the Executive Producer._

**Selected option:** ☐ A ☐ B ☐ C ☐ Other: ______
**Rationale:** ______
**Registry version after decision:** ______
**Dispositioned by / date:** ______
