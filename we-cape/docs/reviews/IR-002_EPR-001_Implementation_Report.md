# IR-002 — EPR-001 Implementation Report
**To:** Chairman / Executive Producer · **From:** Platform Architect · **Date:** 2026-08-26
**Re:** Executive Ratification Order & Ingestion Prompt — EPR-001
**Status:** **IMPLEMENTED.** One structural contradiction raised; three definitional questions open.

---

## Consistency review — one contradiction, and it is not blocking today

### I1 — §1.2's operational interpretation cannot currently be satisfied by any cue

The precondition contract, carried forward verbatim, is operationalised as:

> *"A cue cannot generate until both the Executive documentary intent (EPR-001) **and the downstream
> musical responsibility (Behavior layer / Conductor Score)** are available."*

But **§1.3 defers the entire musical-responsibility vocabulary to `WET-SPEC-RSB-001`** — *"No mapping
to the ten conductor behavior states shall be executed today"* — and **§4.3 records that the Behavior
Registry does not yet exist.**

**So the precondition names a prerequisite that has been formally deferred and has no home.** As
written, **no cue can generate until `WET-SPEC-RSB-001` exists.**

**Nothing is blocked today** — `GATE-2026-08-22-MIE-DOWNSTREAM` is CLOSED and blocks all generation
anyway. **It becomes live the moment the gate opens**, and it would then block Pass 1 for a reason
that has nothing to do with Pass 1.

Three readings, none adopted:

| | reading | consequence |
|---|---|---|
| **R1** | **Deliberate.** Generation is intentionally held until `WET-SPEC-RSB-001` exists | coherent, and consistent with the platform's sequencing discipline. It should be *said*, because it moves a dependency onto the critical path |
| **R2** | **`CONDUCTOR_SCORE`'s existing `behaviour_states` satisfy "responsibility" in the interim** | the ten states already say what each cue must do. §1.2's own parenthesis — *"(Behavior layer / Conductor Score)"* — names `CONDUCTOR_SCORE`, which supports this reading |
| **R3** | **The precondition is suspended until the Behavior Registry is extracted** | explicit, and leaves nothing implicit |

**Recorded in EPR-001 as `engineering_note_IR002_I1`, unresolved.**

### Everything else is consistent

No conflict found with `DOC-001`, `DOC-002`, `ER-001`, `ER-003`, `ER-004`, `ESS-002`, `ADR-009`, the
custody model, the regeneration model, or the gate ledger. **Invariant B is strictly stronger than my
R1/R2/R3 readings in `IR-001` — it covers all three at once** and is implemented that way.

---

## What was implemented

### 1 · `EMOTIONAL_PROGRESSION_REGISTRY.yaml` v1.1.0 — **transcribed, not authored**

`intelligence/p2/registries/EMOTIONAL_PROGRESSION_REGISTRY.yaml`

Order §2.3 forbids the platform to author, populate, infer, suggest **or default** any value. Order
§1.1 names `EMOTIONAL_ARC` as the provenance of EPR-001's initial content. **Those two are reconciled
the same way `VPD-001` was:**

| field | what the platform did |
|---|---|
| `beat` · `segment_refs` · `audience_state` | **TRANSCRIBED verbatim** from existing `EXECUTIVE`-custody declarations. `audience_emotion → audience_state` is the order's rename, not a change of value |
| `dramatic_intensity` · `governing_theme` · `editorial_transition` · `executive_notes` | **`AWAITING_EXECUTIVE_INPUT`** on all seven entries — 29 fields. **Not one was defaulted.** No entry received a suggested intensity, and none ever will from this side |

**Seven entries.** Two segments — **`S04` ride_brief** and **`S17` audience_cta** — had no
`EMOTIONAL_ARC` provenance. **No entry was created for them**, because creating one would require
authoring a `beat`. They are reported under `undeclared_segments`, never filled.

One transcription note carried into the file rather than silently normalised: `EPR-05`'s
`audience_state` is **`"Empathy -> Reverence"`** — a two-state value under a schema that appears to
expect one. **Transcribed exactly as declared.** Whether it should be split is Executive.

### 2 · `epr_validate.py` — V-1 … V-6, structure only

`intelligence/p2/registries/scripts/epr_validate.py` · custody `MACHINE`

```
criterion status  measurement
V-1       PASS    7/7 entries carry id, beat and ≥1 segment_ref
V-2       PASS    17/17 segment_refs resolve in TIMELINE_REGISTRY
V-3       PASS    0 prohibited keys; 0 timecode-shaped scalars outside prose
V-4       PASS    file source_class=EXECUTIVE; non-conforming entries: none
V-5       PASS    observed=17 expected=19 percentage=89.47%; undeclared S04, S17
V-6       PASS    declared=7; AWAITING_EXECUTIVE_INPUT=29; out-of-vocabulary intensity: none
```

**On V-6.** The order states content is never validated. The validator therefore performs **exactly
one** content-adjacent check and I want it visible rather than buried: it confirms that
`dramatic_intensity`, **where declared**, is one of the five ratified tokens. That is a *vocabulary*
check — it cannot tell whether the category chosen is right, only whether the word exists in the
ratified set. **If even that is more than the order intends, say so and it comes out.**

`V-3` also scans for **timecode-shaped scalars**, since `timecodes` is a prohibited field and a
timecode could otherwise enter through a differently-named key. Prose fields are excluded.

### 3 · `EMOTIONAL_ARC.yaml` — marked superseded, retained, not deleted

Header records: `SUPERSEDED_BY: EPR-001 v1.1.0` · that it remains the provenance · that
`music_responsibility` did **not** transfer and its six terms are deferred to `WET-SPEC-RSB-001` ·
that the contract clause is live in both files with **EPR-001 as the governing copy** · and
`DO NOT EDIT`.

### 4 · Dependency topology — recorded as ratified

```
PRIMARY SOURCES  (immutable — ER-004)
        │
        ▼
Editorial Timing Contract
        │
        ▼
 ┌─────────── OBSERVATIONAL LAYER (MACHINE custody) ────────────┐
 │  Visual Registry · Voice Registry · Caption Registry         │
 └──────────────────────────┬───────────────────────────────────┘
                            ▼
              EDITORIAL_SYNCHRONIZATION      ← 100% observational (§4.1, §4.2)
                            │
   EPR-001 ─────────────────┤   INTERIM edge (§4.3)
   (EXECUTIVE, segment-keyed)│
                            ▼
                     CONDUCTOR_SCORE
                            │
                            ▼
                     Road Soul™ Studio
```

Absent and recorded as such: **Interview Registry** (QW-5, still undone) · **Behavior Registry**
(extraction deferred to `WET-SPEC-RSB-001`) · **Gate 0** (not created, per §4.4).

### 5 · Regeneration sequence — **staged, NOT run**

Order §6, one atomic pass under one `RUN_ID`, **after** the `CUSTODY_ALERT_001` ruling.

**One implementation detail the order's five steps do not cover.** `gen_artifacts.py` emits **seven**
artifacts in a single run, not four: it also produces `CAPTION_REGISTRY`, `VISUAL_EVENT_REGISTRY`,
`STEP0_TIMING_CLOSURE` and `PRODUCTION_INTELLIGENCE_SEED`. An atomic pass therefore regenerates all
seven or the generator must be split.

**Recommendation: regenerate all seven.** Splitting the generator to honour a four-item list would
create two run boundaries where there is now one, and a partial regeneration is exactly the state
`DOC-002` exists to prevent. **Raised rather than assumed — say the word if the list is exhaustive
by intent.**

---

## Three definitional questions

| # | question | why it matters |
|---|---|---|
| **Q1** | **Is the intensity scale ORDERED or merely LABELLED?** Recorded as `AWAITING_EXECUTIVE_INPUT`. Invariant B forbids interpolating *between* levels — it does not say whether one level *outranks* another. If ordered, a consumer may compare beats; if labelled, it may not. **And the plain-English reading is genuinely ambiguous**: "elevated" ordinarily means *raised*, which reads as **below** "high", yet the order lists `HIGH` then `ELEVATED` | decides whether any consumer may sort, compare, or reason about relative intensity |
| **Q2** | **Where is the precondition contract evaluated?** See I1. After the split, EPR-001 holds the emotion and the Behavior layer holds the responsibility — the check now spans two artifacts | it is a generation gate; something has to own it |
| **Q3** | **`registry_version` opens at `1.1.0`.** Implemented exactly as ratified. Noting only that §4.5 makes version increments the regeneration trigger, so the **first** increment after authoring will be `1.2.0` | avoids a later "was 1.1.0 the trigger or the baseline?" |

---

## What must still await `CUSTODY_ALERT_001`

Unchanged from `IR-001` §4, and confirmed by implementation:

**Done today, cut-independent:** EPR-001 exists · validator built and passing · supersession recorded
· topology documented.

**Awaiting the cut ruling:** every `segment_ref → timecode` resolution · the §6 regeneration pass ·
all four (seven) regenerated artifacts · `ESS-002` · `EVS-001`.

### One dependency the order should name

**`TIMELINE_REGISTRY` v1.0.0 is the segment authority and is pinned to the 08-22 lock.** EPR-001
records it as `segment_authority`. Two things follow:

1. **Segment keying is safe only while the ID *set* is stable.** The 08-24 cut carries 10 more primary
   elements and 8 more titles; a re-edit may add or split segments. **`V-2` catches an unresolvable
   `segment_ref` — but `V-2` only reports. It does not say what to do.**
2. `TIMELINE_REGISTRY`'s own `delta_note` still says segment boundaries carry a **±6 s tolerance**
   *"until Sprint lock-SRT reconciliation."* **That reconciliation happened** — Step 0 closed the
   tolerance at offset 0.000 s. The note is stale. It does not affect EPR-001, whose keying uses IDs
   rather than spans, but the segment authority should not carry a superseded caveat.

---

## Summary

**Implemented as ratified.** One structural contradiction (I1), three definitional questions, one
generator-scope detail, one stale note in the segment authority. **No value in EPR-001 was authored,
inferred, suggested or defaulted by the platform** — 29 fields stand empty and will stay that way.

*Nine commits plus this one await `git push origin main`.*
