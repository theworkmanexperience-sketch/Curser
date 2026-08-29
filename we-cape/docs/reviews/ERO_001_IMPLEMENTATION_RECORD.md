# ERO-001 — IMPLEMENTATION RECORD

**Instrument:** Engineering Implementation Record
**Order:** EXECUTIVE RESOLUTION ORDER ERO-001 — Narrative Boundary Resolution & Regeneration Scope
**Order date:** 2026-08-28 · **Application:** BINDING
**Implemented:** 2026-08-29
**Custody:** `IMPLEMENTATION / CODEBASE ONLY`
**Repository state at start:** `57c9ed1`

---

## 0 · Disposition

| Order clause | Status |
|---|---|
| §1 — `B-14` segment boundary resolution | **IMPLEMENTED** and enforced by `G-13` |
| §2 — `B-6` regeneration target scope | **IMPLEMENTED** and enforced by `G-12` |
| §3 — engineering authorisation limits | **OBSERVED** — §5 |
| §4 — post-condition | **UNCHANGED** — no regeneration performed or authorised |

```
Conformance suite      22 PASS · 0 FAIL   (was 16 · 0)
Runtime guards         14                 (was 12)
Generator output       BYTE-IDENTICAL to the pre-ERO-001 run
```

**One new condition is raised: `B-16` (§6).** ERO-001 §2 grants episodes their scoring
"exclusively through governed timeline slicing," and no such mechanism exists. The
prohibition is enforced; the permission is not yet implemented.

---

## 1 · §1 — the boundary is determinate

The Order gives two clauses that had to be shown to resolve to a single instant before
anything could be enforced.

```
S12  organizer_honors_and_silence   3124.000 - 3236.000
S13  group_photo                    3230.000 - 3275.000
                                    └──── 6.000 s ────┘
```

| Order clause | resolves to | from |
|---|---|---|
| "EPR-05 maintains … authority **through the visual conclusion of S12**" | **3236.000 s** | S12's declared end |
| "EPR-06 begins at the **editorial completion of that transition**" | **3236.000 s** | the end of the overlap span, which is S12's end |

Both clauses land on the same instant. **The boundary is determinate at 3236.000 s** and
required no interpretation, no midpoint, and no engineering choice.

Recorded as `GNB-001`:

```
id                              GNB-001
authority                       ERO-001 §1
classification                  INTENTIONAL_NARRATIVE_TRANSITION
span                            3230.000 - 3236.000 s   (6.000 s)
retained                        true
authority_beat_through_span     EPR-05          through 3236.000 s
successor_beat                  EPR-06          begins  3236.000 s
interpolation                   PROHIBITED
intermediate_state              PROHIBITED
engineering_obligation          PRESERVE
```

`span_start_s`, `span_end_s` and `overlap_s` are **derived from the segment registry**
by `apply_ero001.py`, not typed. The script stops if a declared overlap magnitude
disagrees with the registry-derived one.

### 1.1 · `G-13` — the guard that matters

`G-13` asserts, on every run, that the governed boundary still describes the data it
governs, and — the clause with teeth — that **the overlap is still there**.

An Executive determination about an anomaly can be destroyed by fixing the anomaly. A
later hand "tidying" S12/S13 into adjacency would delete ERO-001 §1 without touching a
governance document, and before this guard nothing would have noticed.

| test | injected change | result |
|---|---|---|
| `E18` | S13 moved to 3236.0 — the overlap "corrected" away | **STOP** at `G-08b` · exit 2 · **0 files written** |
| `E19` | overlap removed from the data **and** from `declared_segment_overlaps`, leaving only the governance record | **STOP** at `G-13` · exit 2 · **0 files** |

`E19` is the realistic failure. Someone fixes the data, updates the mechanical
declaration to match, and the only thing left standing is the record of what the
Executive decided. `G-13` refuses the run:

```
GNB-001 governs the S12/S13 boundary but no matching declared overlap exists
```

### 1.2 · One clause of `G-13` is defence-in-depth, not proven

`G-13` also refuses a third segment intersecting the governed span. In a start-ordered
registry any such segment necessarily overlaps its neighbour, so `G-08b` fires first
and the `G-13` clause is unreachable in practice. It is retained because the ordering
assumption could change; **it is not claimed as tested.**

---

## 2 · §2 — canonical timeline scope

`regeneration_scope` recorded in the context:

```
mode                                        CANONICAL_EDITORIAL_TIMELINE
conductor_scores_per_run                    1
narrative_progressions_per_run              1
episode_specific_emotional_progressions     PROHIBITED
episode_derivation                          GOVERNED_TIMELINE_SLICING
path_b_architecture                         UNMODIFIED
```

`G-12` enforces it:

- the scope must be declared as `CANONICAL_EDITORIAL_TIMELINE` — an undeclared or
  different scope is not the run the Order authorises
- the observation bundle may not carry `episode_progressions`, `episodes`,
  `episode_emotional_progressions` or `per_episode_progressions`
- the narrative progression must be a single ordered, non-overlapping cover — one
  authoritative progression cannot contain competing spans
- any declared `episode_slices` must fall inside the canonical timeline and may not
  carry `progressions`, `emotional_progression`, `epr` or `beats` of their own

| test | injected change | result |
|---|---|---|
| `E20` | `episode_progressions` added to the bundle | **STOP** at `G-12` · exit 2 · **0 files** |
| `E21` | `regeneration_scope` removed from the context | **STOP** at `G-12` · exit 2 · **0 files** |
| `E22` | — | exactly **1** Conductor Score emitted per run |

### 2.1 · §2 required no generator restructuring

The generator already emitted one artifact set for one `production_id`. What ERO-001 §2
changed is not the capability but the **constraint**: the alternative architectures the
Readiness Review enumerated under `B-6` — per-episode artifact sets, or a Parent plus
three episode sets — are now closed, and a run that attempts one stops.

`B-6` is closed as an open Executive question.

---

## 3 · Output neutrality

The 08-22 fixture regenerated with `--run-id pinned`, before and after ERO-001:

```
STEP0_TIMING_CLOSURE.md            IDENTICAL
CAPTION_REGISTRY.yaml              IDENTICAL
VISUAL_EVENT_REGISTRY.yaml         IDENTICAL
EDITORIAL_SYNCHRONIZATION.yaml     IDENTICAL
CONDUCTOR_SCORE.yaml               IDENTICAL
ESS_VALIDATION_REPORT.md           IDENTICAL
PRODUCTION_INTELLIGENCE_SEED.yaml  IDENTICAL
```

**All seven byte-identical.** ERO-001's implementation adds refusal, not content. No
emitted value changed, which is the evidence that no Executive narrative declaration
was altered by implementing this Order.

---

## 4 · Where the determination was recorded, and where it was not

| location | written? | why |
|---|---|---|
| `AR2-0822.context.json` | **yes** | the only place a runtime guard can read on every run |
| `runtime_guards.py` `G-12`, `G-13` | **yes** | enforcement |
| `EMOTIONAL_PROGRESSION_REGISTRY.yaml` | **no** | §3 prohibits altering Executive narrative declarations, emotional progression values and ratified themes |
| observation bundle `progressions` | **no** | see §4.1 |

### 4.1 · Why the boundary is not in `progressions`

The generator reads `OBS_DS['progressions']` — `P1 ARRIVAL`, `P2 GAUNTLET_ONE`,
`P3 RIDE_AND_TOWN`, `P4 GAUNTLET_TWO_HONORS`, `P5 BIKE_NIGHT_WRAP`. Those are
**documentary** progressions. The governed span 3230–3236 sits wholly inside `P4` and
does not touch a documentary boundary.

`EPR-05` and `EPR-06` are **emotional** beats on a different axis. Writing an emotional
boundary into the documentary progression would breach **Invariant A** — documentary
intent shall never prescribe musical implementation, and observational measurement
shall never prescribe documentary intent. The two axes stay separate, and the
generator's own output is unchanged as a result (§3).

### 4.2 · The context is not a governance record

`GNB-001` lives in an **engineering input**. That is where the guards can read it, and
it is not where an Executive determination belongs for the long term. A context file
carries no governance standing: it is rebuilt by `build_context.py` on every run, it is
not versioned as a registry, and it is not covered by the CAR → ADR → SPEC → PDR → ER
hierarchy.

**Giving ERO-001 §1 durable governance standing — in `EPR-001`, in a registry, or in a
new instrument — is a separate act requiring separate authority, and this Order does
not grant it.** Until then the determination is enforced but not filed.

---

## 5 · §3 — engineering authorisation, compliance

| §3 prohibits | what was done |
|---|---|
| altering Executive narrative declarations | none altered; `EMOTIONAL_PROGRESSION_REGISTRY.yaml` was neither opened for writing nor read by the generator |
| altering emotional progression values | none written anywhere; `EPR-05`/`EPR-06` appear only as identifiers inside `GNB-001` |
| altering ratified themes | untouched |
| implementing beyond generator conformance | two guards, one transcription script, six tests; no capability added, no artifact regenerated |

Additionally: **`apply_ero001.py` authors nothing.** Every value it writes is either
quoted verbatim from the Order or derived from the segment registry, and each derivation
is recorded in the entry beside the value it produced.

---

## 6 · `B-16` — the permission in §2 has no implementation

ERO-001 §2: *"Public distribution episodes derive their scoring exclusively through
governed timeline slicing."*

`G-12` enforces the **prohibition** — no independent episode-specific emotional
progressions. Nothing implements the **permission**. There is no slicing mechanism: no
code takes the canonical Conductor Score and derives an episode's scoring from a span of
it, and no schema describes what a governed slice is beyond the `episode_slices` shape
`G-12` validates if one is ever supplied.

The consequence, stated plainly: under the architecture ERO-001 ratifies, **the three
Path B distribution deliverables have no scoring path today.** They may not have their
own progressions, and the mechanism that would give them scoring from the canonical
timeline does not exist.

This is not a defect in the Order — the Order settled the architecture, which was the
question. It is the next piece of engineering the architecture implies, and it is
raised, not scoped or begun.

---

## 7 · Conformance suite — 22 PASS · 0 FAIL

`E1`–`E16` are unchanged from ECR-GEN-002 and all still pass. New:

| id | test | result | evidence |
|---|---|---|---|
| `E17` | ERO-001 transcribed and enforced on the fixture | **PASS** | scope `CANONICAL_EDITORIAL_TIMELINE`; `GNB-001` S12/S13 3230.000–3236.000 s; EPR-05 through 3236.000; EPR-06 from 3236.000 |
| `E18` | erasing the governed overlap stops the run | **PASS** | `G-08b`, exit 2, 0 files |
| `E19` | a complete tidy-up still stops at the governance record | **PASS** | `G-13`, exit 2, 0 files |
| `E20` | episode-specific emotional progressions stop the run | **PASS** | `G-12`, exit 2, 0 files |
| `E21` | an undeclared regeneration scope stops the run | **PASS** | `G-12`, exit 2, 0 files |
| `E22` | exactly one authoritative Conductor Score per run | **PASS** | 1 emitted |

`E8` now records **14 guards passed** (was 12).

---

## 8 · §4 — post-condition

No production regeneration was performed and none is authorised. The prerequisites
standing before this Order stand after it, less the two it closed:

| prerequisite | state |
|---|---|
| `B-14` segment boundary | **CLOSED** by §1 |
| `B-6` regeneration target | **CLOSED** by §2 |
| authoritative 08-24 ETC | `NOT_PRODUCED` |
| 08-24 observation bundle | `ABSENT` |
| 08-24 proxy designation | `NOT_DESIGNATED` |
| 08-24 ingestion commit | `AWAITING_INGESTION` |
| 08-24 segment set + ratification | pending re-derivation (`B-5`) |
| visual observation producer equivalence | **NOT ESTABLISHED** (`B-3`) |
| `CONDUCTOR_SCORE.yaml` currency | **STALE** — regeneration authority not granted (`T11`) |
| narrative literals in the generator | 280 across 166 lines (`B-13`) |
| governed timeline slicing | **DOES NOT EXIST** (`B-16`, new) |
| durable filing of `GNB-001` | **NOT FILED** — separate authority required (§4.2) |

---

## 9 · Files changed

| path | change |
|---|---|
| `ess/scripts/runtime_guards.py` | `G-12`, `G-13` added; check register updated · 228 → 344 lines |
| `ess/scripts/apply_ero001.py` | **NEW** — transcribes ERO-001; authors nothing |
| `ess/scripts/ecr_gen_002_suite.py` | `E17`–`E22` added |
| `ess/context/AR2-0822.context.json` | `regeneration_scope`, `governed_narrative_boundaries`, `ero_001_transcription` |
| `docs/reviews/ERO_001_IMPLEMENTATION_RECORD.md` | **NEW** — this document |

`EMOTIONAL_PROGRESSION_REGISTRY.yaml`, all governance registries, and all seven governed
artifacts are **unchanged**.

---

## 10 · Standing state

```
B-14 segment boundary             RESOLVED (ERO-001 §1) - enforced by G-13
B-6  regeneration target          RESOLVED (ERO-001 §2) - enforced by G-12
GNB-001 durable filing            NOT FILED - separate authority required
B-16 governed timeline slicing    DOES NOT EXIST - raised, not scoped
runtime guards                    14, fail-fast, 8 negatives proven
conformance suite                 22 PASS / 0 FAIL
generator output                  byte-identical to the pre-ERO-001 run
Engineering Certification         ENGINEERING-CONFORMANT
Production Readiness              NOT YET AUTHORIZED
```

**Prepared for Executive review. No execution is directed by this document.**
