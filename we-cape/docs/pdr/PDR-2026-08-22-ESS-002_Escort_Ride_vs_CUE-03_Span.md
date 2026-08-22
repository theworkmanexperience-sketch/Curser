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

---

# Amendment 1 — 2026-08-22: two findings that arrived after this PDR was written

Two things changed since the Options section above was drafted. Neither is a new opinion; both are
measurements or rulings, and both bear directly on which option is defensible. **The four options
stand. What follows corrects the reasoning attached to them.**

## A1.1 — The ESS-004 ruling removes "silence" from this problem entirely

`MANDATORY_SILENCE` is now defined (Executive Disposition ESS-004, 2026-08-22) as prohibiting
**WE CAPE-added non-diegetic score only.** Existing production audio — engines, wind, ambience,
speech — is permitted.

**Measured consequence.** The primary spine from `00:27:30` to `00:40:00` is **unbroken
camera-original footage**: 37 consecutive `asset-clip` elements, zero gaps, every one carrying its
own audio. There is no point in the 153-second "unscored" span, and no point inside SIL-01, at which
the film is acoustically silent.

| region | span | primary-spine coverage | audible content under the ruling |
|---|---|---|---|
| CUE-03 as specified | 27:40–29:10 | continuous | score **+** production audio |
| the gap | 29:10–31:43 | continuous | production audio (engines, wind, road) |
| SIL-01 | 31:43–38:52 | continuous | production audio + civic speech |

**This reframes Option A.** Option A was written as *"deliberate air."* It is not air. It is
**engines** — 153 seconds of a motorcycle column on a public road, carrying itself. That is a
materially stronger editorial position than "the anthem withdraws and nothing happens," and it is
the position the cut already takes.

**And it reframes Option B's stated virtue.** B was justified by the anthem *"handing directly to
silence."* Under the ruling there is no silence to hand to. B now means: score stops, engines
continue, unchanged. The handoff B was designed to create is already what the gap does — without
four minutes of energy-5 cue to sustain first.

## A1.2 — New measurement: **no cue-sheet boundary in this region lands on a cut**

Measured against the locked FCPXML's primary spine (resolver validated 191/191 against the ETC;
source SHA `2bf06853…3858e7`):

| boundary | timecode | host shot at that instant | prev cut | next cut | on a cut? |
|---|---|---|---|---|---|
| CUE-03 in | 00:27:40.000 | `028 · 10:59:30 · DJI` | −14.208 s | **+0.792 s** | **NO** (near) |
| CUE-03 out | 00:29:10.000 | `013 · 10:27:18 · X5` | −18.250 s | +48.458 s | **NO** |
| SIL-01 in | 00:31:43.000 | `016 · 10:27:19 · X5` | −50.458 s | +12.417 s | **NO** |
| SIL-01 out | 00:38:52.000 | `017 · 10:43:36 · X5` | −74.000 s | +4.292 s | **NO** |
| R46 in | 00:39:07.000 | `018 · 10:47:32 · X5` | −8.375 s | +51.250 s | **NO** |

Only CUE-03's **in** point is near a cut (0.792 s, ~19 frames). Every other boundary sits mid-take,
some by nearly a minute. The pattern is consistent with the cue sheet's spans having been set from
approximate timecode rather than against the cut list — which is normal at architecture stage, and is
exactly what this PDR exists to resolve.

**Consequence for Option B.** B's argument was that the cue *"lands its resolve exactly on the SIL-01
boundary."* That is true on the **timeline** and false in the **picture**: 00:31:43.000 falls 50.5 s
into a 62.9 s continuous take. A four-minute energy-5 cue would resolve to floor with nothing on
screen to mask the event — the most exposed possible place to end a cue. If B is chosen, its out
point should move to a cut. The nearest candidates are **00:31:55.417** (+12.4 s, the cut to `014`)
and **00:30:52.542** (−50.5 s).

**Consequence for Option C.** The same measurement is C's strongest argument. A separate CUE-03b can
take its **in** point at a cut without touching approved CUE-03 at all. `00:29:58.458` — the cut into
`NOTOR1OUS_CARAVAN_1_` — is 48.5 s after the cue sheet's 29:10 and is a real picture event.

**Consequence for Option A.** A is unaffected. It is the only option that needs no boundary.

## A1.3 — Cut density: the gap is editorially *calmer* than the cue

| span | duration | cuts | mean shot length |
|---|---|---|---|
| CUE-03 as specified (27:40–29:10) | 90 s | 7 | **12.86 s** |
| the gap (29:10–31:43) | 153 s | 4 | **38.25 s** |
| SIL-01 (31:43–38:52) | 429 s | 21 | 20.43 s |

The gap is cut **three times slower** than the cue it follows. Whatever was intended, the picture in
that 153 seconds decelerates — it does not sustain. **This argues against B on its own terms:**
holding energy 5 across material that visibly slows down asks the music to contradict the edit. It
argues *for* A (the deceleration is the point) or for a **low-energy** C (a de-escalation cue that
follows the picture down), and it is evidence that Option C's energy value should not inherit
CUE-03's 5.

## A1.4 — What this Amendment does not resolve, and will not

Cut alignment, audio continuity and cut density are **measurements**. Whether the anthem should carry
the ride or step out of it is a **musical-intent decision** and remains entirely the Executive
Producer's. Nothing above narrows the four options; it corrects three claims attached to them:

| claim as originally written | status after Amendment 1 |
|---|---|
| A = "deliberate air" | **WRONG WORD.** It is 153 s of engines, not absence |
| B = "hands directly to silence" | **NO LONGER TRUE.** There is no silence to hand to |
| B = "resolve lands exactly on the SIL-01 boundary" | **TRUE ON THE TIMELINE, FALSE IN THE PICTURE.** It lands 50.5 s inside a continuous take |

**Status remains OPEN — AWAITING EXECUTIVE DISPOSITION.**

---

## Decision (Amendment 1 revision — replaces the block above)

**Selected option:** ☐ A ☐ B ☐ C ☐ D ☐ Other: ______
**If A — recorded rationale for the intended engine-carry:** ______
**If B or C — out/in point, and whether it moves to a cut:** ______
**If C — energy value for CUE-03b (note A1.3: inheriting 5 is contradicted by the cut density):** ______
**Rationale:** ______
**Dispositioned by / date:** ______



---

# Amendment 2 — 2026-08-22: **SCOPE NARROWED BY EXECUTIVE DIRECTION**

**Direction as issued:**

> *"ESS-002 should answer one question. Is the proposed musical boundary correct? Nothing more.
> Everything involving actual music waits until CUE-03 exists."*

## A2.1 The question this PDR now answers — and only this

> **Is the proposed musical boundary correct?**

Concretely: **at which timecode does CUE-03 ESCORT_ANTHEM end?** The four options A/B/C/D are
unchanged; they are now read strictly as boundary options, stripped of every claim about how music
will behave once it exists.

| in scope | out of scope — deferred to `PDR-<date>-CUE-03` |
|---|---|
| Which option: A / B / C / D | Whether the finished cue overstays |
| The out point, to the frame | Whether the exit gesture reads as natural |
| Whether that point sits on a cut, and if not, why not | Level, duck depth, tail length, reverb decay |
| Whether the picture's deceleration is real and intended | Whether the `LEAD` behavior state is achievable over this production audio |
| If C: the in point for CUE-03b, and its energy value | Whether the chosen boundary survives contact with the composed cue |

## A2.2 Why the scope had to narrow — the circularity, restated

ESS-002 blocks MIE Pass 3. Pass 3 produces CUE-03. CUE-03 is what "does it overstay" needs.
Left as originally written, this PDR could not be dispositioned until the work it blocks had been
done. Narrowing it to the boundary breaks the loop: **placement is decidable from picture; behavior
is not decidable until there is a cue.**

## A2.3 The deferred question — registered, not lost

A question moved out of scope and not written down anywhere is a question that disappears. It is
therefore registered here as a forward obligation on the cue PDR:

```
DEFERRED-FROM: PDR-2026-08-22-ESS-002 (Amendment 2, Executive direction 2026-08-22)
DEFERRED-TO:   PDR-<date>-CUE-03
QUESTIONS:     1. Does the composed CUE-03 overstay its span?
               2. Does its exit read as natural at the boundary set here?
               3. Is the LEAD behaviour state achievable over this span's production audio?
                  (measured at -3.17 dB mean across the gap - see EVS-001 section 3.1)
LICENCE:       The cue PDR MAY move the boundary set here, provided it records why.
               See A2.4. A boundary is a hypothesis with a rationale, not a lock.
```

## A2.4 The risk this narrowing creates, stated so it is not discovered later

Deciding placement before composition is disciplined. It is also a **bet**: that the correct boundary
can be known before the music that has to land on it exists.

That bet is usually good and occasionally wrong. A composer working the span may find the natural
resolve is fourteen seconds later than the ruled boundary — not because the ruling was careless, but
because a musical phrase has a length that no picture measurement predicts.

**The failure mode is not blur. It is premature freezing** — treating a boundary ruled at EVS-001 as
immovable because it is now in a governed artifact, and bending the music to fit a number.

**The mitigation is stated above and is not optional:** `PDR-<date>-CUE-03` holds an explicit licence
to move this boundary **if it records why**. The governance value is not that the boundary never
changes. It is that it never changes *silently* — the same property `DOC-002` gives derived
artifacts, applied to a decision.

## A2.5 Session

`EVS-001` (`docs/reviews/EVS-001_ESCORT_RIDE_VIEWING_BRIEF.md`), revised to v1.1 under this
narrowing: the two unanswerable questions are struck from the session, and the passes are retargeted
onto the boundary question alone.

**Status remains OPEN — AWAITING EXECUTIVE DISPOSITION**, now on one question.

---

## Decision (Amendment 2 revision — supersedes all decision blocks above)

**Is the proposed musical boundary (00:29:10.000) correct?** ☐ yes ☐ no

**Selected option:** ☐ A cue stands at 29:10 ☐ B extend ☐ C new CUE-03b ☐ D registry only ☐ Other: ______
**Boundary timecode, to the frame:** ______
**Does it sit on a cut?** ☐ yes ☐ no — **if no, the recorded reason:** ______
**If C — in point for CUE-03b, and its energy value:** ______
**Rationale:** ______
**Dispositioned by / date:** ______
