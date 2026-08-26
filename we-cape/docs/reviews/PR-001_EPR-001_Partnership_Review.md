# PR-001 — Partnership Review: EPR-001 Integration & Gate 0 Ingestion Strategy
**Requested by:** Executive / Creative Direction · **Reviewed by:** Platform Architect · **Date:** 2026-08-24
**Subject:** proposed `EMOTIONAL_PROGRESSION_REGISTRY.yaml` (EPR-001) as a governed upstream artifact
**Scope:** governance integrity · Gate 0 placement · dependency chain · draft ingestion prompt

---

## Verdict

**EPR-001 is architecturally sound and it should exist. It is not, however, a new artifact — and the
chain it is proposed into contains three nodes that do not.**

| review area | finding |
|---|---|
| **1 · Architectural integrity** | **No irreconcilable conflict.** Six conditions must hold; one is load-bearing and unstated in the proposal |
| **2 · Gate 0** | **Cannot be answered as posed. `Gate 0` does not exist** in the Gate Ledger or anywhere in the repository |
| **3 · Dependency chain** | **Revision recommended.** Three named nodes are absent, and one edge is architecturally wrong |
| **Deliverable** | Draft ingestion prompt at §4, **conditional** on the six conditions |

---

## 0. The finding that reframes the proposal — this artifact already exists

`intelligence/p2/mie/EMOTIONAL_ARC.yaml` · `document_id: DOCUMENTARY_EMOTIONAL_ARC` · **v1.0.0** ·
`class: executive-artifact` — *"the emotional contract binding composer and editor (Chairman
addition, Executive Review)."* It is already cited as a governed reference by `CUE-02A_SPEC`.

```yaml
- {beat: Arrival,     segs: [S01, S02], audience_emotion: Curiosity, music_responsibility: Invite}
- {beat: Interviews,  segs: [S03],      audience_emotion: Listening, music_responsibility: Yield}
- {beat: Brotherhood, segs: [S05],      audience_emotion: Unity,     music_responsibility: Lift}
…
contract: "Every cue decision cites its beat; a cue that cannot name its emotion and
           responsibility does not generate."
```

**The overlap is near-total.** `audience_emotion` **is** the proposed `audience_state`. `beat` and
`segs` are the proposed segmentation. It is already Executive-class.

**This is the fourth instance today of the CAR-003 discoverability pattern** — a capability that
exists under a different name. It is not an argument against EPR-001. It changes what EPR-001 *is*:

> **The proposal is not an addition. It is a SPLIT.**
>
> `EMOTIONAL_ARC` currently couples **what the audience feels** to **what music must do**
> (`music_responsibility`: Invite · Yield · Lift · Support · Celebrate · Resolve).
> **EPR-001's stated purpose is to decouple exactly those two things.**

Recommended framing for the ingestion prompt: EPR-001 **supersedes `EMOTIONAL_ARC` v1.0.0**, taking
its documentary-intent half and adding `dramatic_intensity` and `editorial_transition`. The
`music_responsibility` half moves **downstream** to the Behavior layer, which is where the proposal
already says it belongs.

**Two things must survive the split, or they are lost silently:**

1. **The `contract` clause is a live generation precondition** — *"a cue that cannot name its emotion
   and responsibility does not generate."* If EPR-001 supersedes the arc, that clause is either
   carried forward or explicitly retired. It cannot simply stop existing.
2. **`music_responsibility` is a second, undeclared musical vocabulary** — six terms, entirely
   separate from the ten behaviour states in `CONDUCTOR_SCORE`. The platform has been running two
   vocabularies without knowing it. This is `RSB-AUDIT-001` gap **G2** in a place the audit did not
   look. The split is the moment to declare or reconcile them.

---

## 1 · Architectural Integrity — six conditions

### C1 — **LOAD-BEARING, AND UNSTATED.** EPR-001 must be `EXECUTIVE` custody, and the platform must be barred from populating it

The engagement's standing constraint: *no sentiment or emotion inference beyond governed
observables — classify as `UNCERTAIN` rather than infer.*

A registry named `EMOTIONAL_PROGRESSION` with `audience_state` and `dramatic_intensity` sits directly
on that constraint. **It does not breach it — provided every value is declared, never derived.**

| | permitted | prohibited |
|---|---|---|
| Executive **declares** the intended audience experience | ✅ this is intent, and intent is Executive property | |
| Platform **infers** audience state from luma, cut rate, speech density, or any observable | | ❌ **breaches the standing constraint and ER-003 Layer 3** |

**Condition:** `source_class: EXECUTIVE` on every entry. The platform may **read, cite and validate
structure**. It may **never author, populate, infer, extend, or suggest a value.** This is the same
boundary ER-002 draws for Palette, and it must be written into the ingestion prompt in those words —
the proposal as circulated does not contain it.

### C2 — ER-003: EPR-001 is the platform's **first wholly Layer 3 artifact**

Every existing registry is Layer 1 (timeline mechanics) or Layer 2 (screen presentation). EPR-001 is
Layer 3 — Executive Interpretation — end to end. **That is a genuine architectural first and should
be named as such**, because it establishes the precedent that Layer 3 may have permanent governed
homes rather than living only in rulings and PDRs. Consistent with ER-003, conditional on C1.

### C3 — DOC-001: no conflict, but EPR-001 **can never be validated**, only structurally checked

DOC-001 binds *derived* instruments. EPR-001 derives nothing, so it has no instrument to validate.
The consequence must be stated rather than left implicit: **an EPR entry cannot be right or wrong.**
It can only be *declared* or *absent*. Validation is therefore limited to schema, coverage and
referential integrity — never to content.

### C4 — ER-004 custody: the **fusion hazard**, and it is the real risk

If EPR-001 feeds `EDITORIAL_SYNCHRONIZATION`, that artifact stops being a fusion of *measured* facts
and becomes a blend of measurement and declaration **in the same rows**. Under ER-004 those are
different custody classes and must remain distinguishable.

This is the reasoning behind the dependency revision at §3. **It is the strongest technical objection
in this review**, and it is an objection to one *edge*, not to the artifact.

### C5 — DOC-002: a frequently-edited artifact upstream of a regenerate-only chain is a new operating condition

The four Primary Sources never change. **EPR-001 will change often** — it is creative work in
progress. Placed upstream of `EDITORIAL_SYNCHRONIZATION` → `CONDUCTOR_SCORE`, **every edit fires a
full regeneration cascade.** DOC-002 permits no patching, so there is no cheap path.

**Condition:** EPR-001 carries `registry_version`, and regeneration is triggered by a **version
increment**, not by file mtime. Working edits accumulate; a version bump publishes them. Without this
the platform either regenerates constantly or drifts silently — and drifting silently is the failure
this platform has ruled against since Sprint 3A.

### C6 — ESS-002 and the open cut: **key EPR-001 on segments, not timecodes**

`CUSTODY_ALERT_001` is unresolved: a second cut of Part 2 exists, diverging at `00:03:27.208`.
`ESS-002`'s boundary is open. **Authoring EPR-001 against timecodes now would pin documentary intent
to numbers that may not survive the cut ruling.**

`EMOTIONAL_ARC` already solved this — it keys on **segment IDs (`S01…S19`)**, not timecodes.
**Segment-keyed intent survives a re-edit; timecode-keyed intent does not.** Carry that property
forward. It is the single design decision that lets EPR-001 be authored *before* the cut question is
settled, which is otherwise a hard blocker.

---

## 2 · Gate 0 — the question cannot be answered as posed

**`Gate 0` does not exist.** A repository-wide search returns nothing. The Gate Ledger, discovered by
the `gate_class: EXECUTION_GATE` marker per `WET-SPEC-GATE-001`, contains **exactly one gate**:

```
[CLOSED] GATE-2026-08-22-MIE-DOWNSTREAM   (PROGRESSION/PRODUCTION)   blocking: 3 open of 4
```

Also named-but-absent: **`MIE-PROD-001`** — `GENERATION_PLAN.yaml` records it as *"not yet issued."*
And SOP-06's GATE 1/2/3 are prose-only, never entered in the ledger (`DWR` already flags this).

**I will not place EPR-001 relative to a gate I would have to invent.** Naming its position against
an undefined gate would create the appearance of governance without the substance.

**Recommendation — answer the underlying question instead.** The real question is *when may EPR-001
be authored, and when does it bind?* Those have different answers:

| | answer | reason |
|---|---|---|
| **When may it be authored?** | **Immediately, and before any gate** | it is a declaration of intent, derives nothing, and consumes no evidence. Nothing gates an Executive statement of what the film is for. Keyed on segments (C6), it does not even depend on the cut ruling |
| **When does it bind generation?** | **At the existing MIE gate — no new gate needed** | `GATE-2026-08-22-MIE-DOWNSTREAM` already blocks all generation. Adding a second gate for EPR-001 would be the parallel system `WET-REV-002` forbids |
| **When does it enter the regeneration chain?** | **On its first version increment after the cut is ruled** | before that, its downstream consumers are themselves in question |

**If a `GATE-0` is genuinely wanted**, it should be created properly — a conforming ledger entry with
`gate_class: EXECUTION_GATE`, a stated `unblock_condition`, and a `composition: ADDITIVE` clause — not
referenced into existence. That is a separate decision and I have not made it.

---

## 3 · Dependency Chain — revision recommended

### 3.1 Three nodes in the proposed chain do not exist

| node | status |
|---|---|
| `Interview Registry` | **absent.** This is the omission I self-reported in `CAR-003 §6.1` — `EDITORIAL_SYNCHRONIZATION` never declared it `NOT_CONSUMED`. Remedy is Quick Win **QW-5**, still not done |
| `Behavior Registry` | **absent.** Behaviour currently lives *inside* `CONDUCTOR_SCORE` as `behaviour_states`. Extracting it is a real change, not a wiring diagram |
| `Gate 0` | **absent** (§2) |

**Ratifying EPR-001 "into" this chain would pin it to three nodes that are not there.** Each is a
legitimate future artifact; none can be depended on today.

### 3.2 The edge that is architecturally wrong

```
proposed:   Visual · Voice · Caption · Interview · EPR-001  ──▶  EDITORIAL_SYNCHRONIZATION
```

`ADR-009 §2` defines `EDITORIAL_SYNCHRONIZATION` as *"fusion of things that already exist under
governance … correlation."* Every other input on that line is **observational** — Layer 1/2, `MACHINE`
custody, independently verifiable. **EPR-001 is declarative — Layer 3, `EXECUTIVE` custody, not
verifiable in principle (C3).**

Placing them on the same edge asserts they are the same kind of input. They are not. The consequence
is concrete: **a sync artifact containing declared intent can no longer be independently checked**,
because part of it has no method. That defeats the property that makes it citable.

### 3.3 Recommended chain

```
PRIMARY SOURCES  (immutable — ER-004)
        │
        ▼
Editorial Timing Contract
        │
        ▼
 ┌──────────────── OBSERVATIONAL LAYER ─────────────────┐
 │  Visual Registry · Voice Registry · Caption Registry │   MACHINE custody
 │  Interview Registry            (ER-003 Layer 1 / 2)  │   independently verifiable
 └──────────────────────────┬───────────────────────────┘
                            ▼
              EDITORIAL_SYNCHRONIZATION          ← stays PURELY observational
                            │
                            ▼
   EPR-001 ───────────────▶ Behavior Registry    ← intent meets measurement HERE
   (EXECUTIVE custody,      (both custody classes present, per-field provenance)
    Layer 3, segment-keyed) │
                            ▼
                     CONDUCTOR_SCORE
                            │
                            ▼
                     Road Soul™ Studio
```

**Why this ordering is more auditable — three reasons, each testable:**

1. **`EDITORIAL_SYNCHRONIZATION` stays independently verifiable.** Every row keeps a method. Re-run
   the instruments, get the same artifact. That property dies the moment declared intent enters it.
2. **The custody boundary lands where ER-004 puts it** — at the join between measurement and
   decision, which is exactly where the Behavior layer sits. Intent and measurement meet **once**, in
   a named place, with per-field provenance, rather than diffusing through the pipeline.
3. **It matches what the proposal already says.** The stated purpose is that EPR-001 remains agnostic
   about cue behaviour and that behaviour is *downstream*. Feeding it into the sync layer would place
   it **two levels upstream of its own stated boundary.** The revision does not fight the proposal —
   it enforces it.

**One consequence to accept openly:** this makes the **Behavior Registry a prerequisite**, not an
optional node. Today behaviour lives inside `CONDUCTOR_SCORE`, so until it is extracted, EPR-001's
only consumer is `CONDUCTOR_SCORE` itself. That is workable as an interim edge and should be stated
as interim rather than left ambiguous.

---

## 4 · Draft Executive Ingestion Prompt

**Conditional on C1–C6 and the §3 revision.** Not authorization — a draft for the Executive to issue,
amend or reject.

```
════════════════════════════════════════════════════════════════════════════
EXECUTIVE INGESTION PROMPT — EPR-001
Authority: Executive Producer / Chairman        Application: PROSPECTIVE
════════════════════════════════════════════════════════════════════════════

1 · RATIFICATION
EMOTIONAL_PROGRESSION_REGISTRY.yaml (EPR-001) is ratified as a governed
upstream artifact of documentary intent.

It SUPERSEDES EMOTIONAL_ARC.yaml v1.0.0 (DOCUMENTARY_EMOTIONAL_ARC), taking
its documentary-intent content forward and leaving its music_responsibility
column to the Behavior layer.

  1.1  EMOTIONAL_ARC v1.0.0 is retained, marked SUPERSEDED_BY: EPR-001, and
       is NOT deleted. It remains the provenance of EPR-001's initial content.
  1.2  Its `contract` clause — "a cue that cannot name its emotion and
       responsibility does not generate" — is:
           ☐ carried forward into EPR-001 verbatim
           ☐ retired, with the reason recorded
       ONE MUST BE CHOSEN. It is a live generation precondition today.
  1.3  The six music_responsibility terms (Invite · Yield · Lift · Support ·
       Celebrate · Resolve) are a SECOND musical vocabulary alongside the ten
       behaviour states. On transfer to the Behavior layer they are:
           ☐ declared as a distinct vocabulary with a stated relation to the
             ten states
           ☐ mapped onto the ten states, with the mapping recorded
           ☐ deferred to WET-SPEC-RSB-001
       (RSB-AUDIT-001 gap G2.)

2 · CUSTODY — BINDING, AND NOT WAIVABLE BY IMPLEMENTATION CONVENIENCE
  2.1  Every EPR-001 entry carries source_class: EXECUTIVE.
  2.2  The platform MAY read, cite, and validate the STRUCTURE of EPR-001.
  2.3  The platform SHALL NOT author, populate, infer, extend, suggest, or
       default ANY EPR-001 value. An empty field remains empty.
  2.4  No EPR-001 value may be derived from any observable — luma, cut rate,
       speech density, motion energy, or any other measured quantity.
       This preserves the standing constraint against sentiment and emotion
       inference, and ER-003's Layer 3 boundary.
  2.5  Governing invariant, as proposed and adopted:
       DOCUMENTARY INTENT SHALL NEVER PRESCRIBE MUSICAL IMPLEMENTATION.
       Corollary, added on review:
       AND MEASUREMENT SHALL NEVER PRESCRIBE DOCUMENTARY INTENT.

3 · SCHEMA
  registry_id: EMOTIONAL_PROGRESSION_REGISTRY
  registry_version / registry_schema_version        (WET-SPEC-DIE-001 F-2)
  source_class: EXECUTIVE
  supersedes: EMOTIONAL_ARC.yaml v1.0.0
  entries[]:
    id                     stable, immutable
    beat                   narrative beat name
    segment_refs[]         SEGMENT IDs — NOT timecodes (see 4.2)
    dramatic_intensity     Executive-declared
    audience_state         Executive-declared
    editorial_transition   narrative handoff; NO musical execution
    executive_notes        optional documentary intent
  PROHIBITED FIELDS: palette, instrumentation, stems, BPM, harmony, genre,
  prompts, dynamics, cue behaviour, or any field naming a musical means.

4 · KEYING
  4.1  EPR-001 keys on SEGMENT IDENTIFIERS, never on timecodes.
  4.2  Reason: a second cut of Part 2 exists (CUSTODY_ALERT_001) and ESS-002's
       boundary is open. Segment-keyed intent survives a re-edit; timecode-
       keyed intent does not. EMOTIONAL_ARC already keys this way.
  4.3  Timecode resolution is performed DOWNSTREAM, by the consumer, against
       whichever cut is in force — and is never stored in EPR-001.

5 · PLACE IN THE ARCHITECTURE
  5.1  EPR-001 does NOT feed EDITORIAL_SYNCHRONIZATION, which remains PURELY
       observational and independently verifiable (ADR-009 §2).
  5.2  EPR-001 feeds the BEHAVIOR LAYER, where declared intent meets measured
       fact, with per-field provenance (ER-004).
  5.3  INTERIM: the Behavior Registry does not yet exist. Until it does,
       EPR-001's sole consumer is CONDUCTOR_SCORE. This edge is INTERIM and
       is recorded as such.

6 · GATE RELATIONSHIP
  6.1  No new gate is created. "Gate 0" does not exist in the Gate Ledger and
       is not brought into existence by reference.
  6.2  Authoring EPR-001 is UNGATED. It declares intent, derives nothing, and
       consumes no evidence.
  6.3  EPR-001 binds generation through the EXISTING gate,
       GATE-2026-08-22-MIE-DOWNSTREAM. No parallel mechanism (WET-REV-002).
  6.4  EPR-001 enters the regeneration chain on its first version increment
       AFTER the cut question (CUSTODY_ALERT_001) is ruled.

7 · VALIDATION — STRUCTURE ONLY
  V-1  every entry carries an id, a beat, and at least one segment_ref
  V-2  every segment_ref resolves in the governing segment registry
  V-3  no prohibited field (§3) appears anywhere in the file
  V-4  no entry carries source_class other than EXECUTIVE
  V-5  coverage reported as {observed, expected, percentage} over the segment
       set, with missing_data_policy (ER-003 A2.3 / A2.4)
  V-6  CONTENT IS NEVER VALIDATED. An EPR entry cannot be correct or
       incorrect. It can only be declared or absent. (C3)

8 · REGENERATION
  8.1  A version increment of EPR-001 triggers regeneration of every
       downstream governed artifact. DOC-002 — regenerate, never patch.
  8.2  Regeneration is triggered by VERSION INCREMENT, never by file mtime.
       Working edits accumulate; a version bump publishes them. (C5)
  8.3  EPR-001 is a GOVERNED ARTIFACT, not a Primary Source (ER-004 A1).
       Regeneration never alters it.

9 · EXECUTION ORDER — on ratification, and after the cut ruling
       1. EPR-001 authored and version-pinned          (Executive)
       2. VISUAL_EVENT_REGISTRY.yaml                   (regenerate)
       3. EDITORIAL_SYNCHRONIZATION.yaml               (regenerate — WITHOUT
                                                        EPR input, per 5.1)
       4. Behavior Registry                            (INTERIM: skip; the
                                                        artifact does not exist)
       5. CONDUCTOR_SCORE.yaml                         (regenerate — consumes
                                                        EPR-001 directly, 5.3)
       6. ESS_VALIDATION_REPORT.md                     (regenerate; includes
                                                        V-1..V-6 results)
  9.1  Steps 2–6 are one regeneration run under a single RUN_ID.
  9.2  No step may be performed by hand (DOC-002).

10 · WHAT THIS PROMPT DOES NOT AUTHORIZE
  Not composition. Not prompt generation. Not cue realization. Not palette
  authorship. Not movement of the ESS-002 boundary. Not resolution of
  CUSTODY_ALERT_001.
════════════════════════════════════════════════════════════════════════════
```

---

## 5 · What I could not assess, and one custody question

**Could not assess:** whether the intended `dramatic_intensity` scale is ordinal, interval, or
labelled. If it is numeric and later aggregated across beats, it becomes a composite score and falls
under the `DWR-010` prohibition. **If it is numeric, its scale and its non-aggregation should be
stated in §3 of the prompt.** I have not assumed either way.

**One custody question the proposal raises and the platform has no answer for.** The communiqué
records that *Creative Direction (ChatGPT)* contributed the narrative and behavioural framing.
Under ER-003 A2.2 there are three custody classes — `MACHINE` (governed instrumentation), `HUMAN`
(a person), `EXECUTIVE` (the Executive). **A second AI system fits none of them.** It is not the
platform's instrumentation, it is not a person, and it is not the Executive.

Today the answer is clean: **the Executive adopted the framing, so it enters as `EXECUTIVE` custody
and the origin is provenance, not custody.** That works. It is worth recording explicitly, because
the moment a contribution is ingested *without* Executive adoption, the class is genuinely undefined.

**Raised, not decided.** No new class proposed.

---

*Prepared 2026-08-24 by the Platform Architect. Review and draft only — this document authorizes
nothing. Six conditions, one chain revision, three absent nodes, and one superseded artifact.*
