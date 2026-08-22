# PDR-2026-08-22-ESS-002 — Escort ride duration vs CUE-03 ESCORT_ANTHEM span
## Governance Status
Document Type: Production Decision Record · Status: **OPEN — AWAITING EXECUTIVE DISPOSITION** · Date: 2026-08-22
Authority: Executive Producer · Origin: Final Executive Disposition, Sprint 3A (2026-08-22), item 2
Reference Execution: RE-001 · Conflict ID: **VCONF-02** · Related delta: **D-15**
Boundary: ADRs govern the platform · PDRs govern productions.

## Question
`CUE-03 ESCORT_ANTHEM` is specified **00:27:40–00:29:10 (90 s)**. The mass ride is on screen
continuously from **00:28:15 to approximately 00:33:00**. Roughly **150 seconds of escort ride carries
no cue**, and the film's "first full statement of unity in motion" ends while the ride is still running.
Does the cue extend, does a new cue take the remainder, or does the silence after 00:29:10 stand?

## Evidence
| kind | value |
|---|---|
| Cue sheet | `CUE-03 ESCORT_ANTHEM, family MOTION, pass 3, span "27:40-29:10", energy 5` (CUE_SHEET v1.1) |
| Registry | `S05 span "27:40-29:10" activity: escort_ride vehicles: [motorcycles-mass] note: police tribute` |
| Observation | `VE-013` MASS_RIDE_PUBLIC_ROAD, **00:28:15 → ~00:33:00**, continuous two-abreast formation, POV from inside the column, confidence HIGH |
| Observation | `VE-014` LAW_ENFORCEMENT_ESCORT_PRESENCE — marked police vehicles / officer at intersections at **00:29:06, 00:30:03, 00:30:21, 00:30:51, 00:31:33, 00:31:48**, confidence HIGH |
| Structural | next cue-sheet entry after CUE-03 is `SIL-01` at **00:31:43**. The span 00:29:10–00:31:43 (**153 s**) carries neither cue nor conducted silence (delta D-19) |
| Structural | SIL-01 therefore **opens over moving ride footage**, not over civic speech (finding SLF-02) |
| Source | `Filmage_Editor.mp4` SHA-256 `a53655fc…0f47e8` |

## Why this was not auto-resolved
The cue sheet is ARCHITECTURE APPROVED (Chairman, 2026-08-21) and registries outrank visual
observation. Extending a cue is a musical-intent decision, not a measurement.

## The real shape of the problem
Three facts have to be held together, and they conflict pairwise:
1. The ride runs to ~00:33:00.
2. The cue ends at 00:29:10.
3. Mandatory silence begins at 00:31:43 — **while the ride is still on screen**.

So the 153 s gap is not simply "unscored"; it is bounded on the right by a covenant that cannot move
without reopening the silence law. Any option that extends CUE-03 past 00:31:43 is not a cue decision,
it is a silence-law decision.

## Options
**A — Cue stands. The 153 s is deliberate air.** The anthem makes its statement and withdraws, leaving
engine noise to carry the ride into the town's silence. Defensible and possibly the original intent —
but if so it is nowhere written down, and the Conductor's Score currently records it as an uncovered
span rather than an intended one. Choosing A should include recording *why*.

**B — Extend CUE-03 to 00:31:43.** Cue runs 27:40–31:43 (243 s), landing its resolve exactly on the
SIL-01 boundary. Musically coherent: the anthem carries the whole ride and hands directly to silence.
Cost: CUE-03 becomes the film's second-longest cue and its energy-5 profile must sustain 4 minutes;
the APPROACH state into SIL-01 has to bring energy 5 to absolute floor in 6 s.

**C — New cue CUE-03b for 00:29:10–00:31:43.** Preserves the approved CUE-03 verbatim and gives the
run-out its own behaviour (de-escalation into the civic zone). Cost: a new cue ID in an approved sheet,
and a Pass-3 addition.

**D — Move the S05 boundary only, leave music alone.** Corrects the registry to match the observed ride
without changing the score. Honest about the picture; leaves the 153 s musically unaddressed.

## Downstream impact
- Regenerates on decision: `EDITORIAL_SYNCHRONIZATION.yaml`, `CONDUCTOR_SCORE.yaml`.
- Option B or C changes `CONDUCTOR_SCORE.uncovered_spans` and the SIL-01 APPROACH state.
- Options B and C are Pass 3 (MOTION) work and cannot proceed before the Conversation family gate.
- No effect on Step 0 or any timing claim.

## Blocks
Downstream MIE Pass 3 (MOTION family). Also touches SIL-01's approach behaviour, so it should be
dispositioned **together with `PDR-2026-08-22-ESS-004`**, which concerns the interior of the same
silence zone.

## Decision
> _To be recorded by the Executive Producer._

**Selected option:** ☐ A ☐ B ☐ C ☐ D ☐ Other: ______
**If A — recorded rationale for the intended air:** ______
**Rationale:** ______
**Dispositioned by / date:** ______
