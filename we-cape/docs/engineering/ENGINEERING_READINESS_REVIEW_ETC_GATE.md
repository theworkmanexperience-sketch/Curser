# ENGINEERING READINESS REVIEW — ETC GATE

**Instrument:** Engineering Readiness Review
**Subject:** Readiness to proceed to atomic regeneration upon receipt of an authoritative 08-24 Editorial Timing Contract
**Production:** Alpha RoundUp 2026 — Day 2 Episodic Trilogy (08-24 lineage), `AR2-0824`
**Date:** 2026-08-29
**Repository state reviewed:** `cfae47d` (HEAD, pushed)
**Custody:** `OBSERVATIONAL (MACHINE)`
**Inference policy:** `ZERO`
**Authority:** none claimed. This review directs no execution, authorizes no regeneration, and alters no Executive declaration, registry, or governed artifact.

---

## 0 · Headline

| Question | Answer |
|---|---|
| **Q1** — Is the current implementation capable of regeneration once an authoritative 08-24 ETC exists? | **NO** |
| **Q2** — Is the missing ETC the single gating dependency? | **NO** — eleven blockers are ETC-independent |
| **Q3** — What constitutes an acceptable 08-24 ETC? | §3, eight acceptance criteria |
| **Q4** — Exact remaining execution sequence after an ETC is supplied? | §4, sixteen gates |
| **Q5** — `ECR-GEN-002` before or after ETC availability? | **BEFORE**, and it is the critical path |

**The finding that changes the shape of this question:** the platform's ETC validator does not work. It was never able to perform the comparison the ETC exists to enable. This was measured against the 08-22 ETC — which the platform *does* hold — during this review. An 08-24 ETC delivered today would arrive at a gate that cannot open.

---

## 1 · Q1 — Is the implementation capable of regeneration once an authoritative 08-24 ETC exists?

### **NO.**

Four findings are independently sufficient to answer NO. Each is reproducible from the committed repository.

---

### 1.1 · The ETC validator is defective — it has never performed the comparison it claims

`fcpx_resolve.py` builds its comparison set as:

```python
mine_spine = [x for x in rows if x['depth'] == 0]        # line 106
...
for a, b in zip(etc_spine, mine_spine):                   # line 109
```

The Editorial Timing Contract's `spine` array **excludes transitions**. The resolver's `depth == 0` set **includes them**. The two lists are then paired positionally by `zip`, so the comparison desynchronises at the first transition and never re-synchronises.

**Measured this session, committed code, committed inputs:**

```
$ python3 fcpx_resolve.py inputs/Info.fcpxml inputs/P2_LOCK_timing.json out.json

etc_spine_n           : 191
resolved_spine_n      : 214
spine_offset_matches  : 1
```

**One match out of 191.**

The same data, with transitions excluded from the resolver set:

```
resolver depth-0 by tag : asset-clip 180 · transition 23 · clip 8 · gap 3   = 214
ETC spine by tag        : asset-clip 180 ·                clip 8 · gap 3   = 191
depth-0 excluding transitions                                              = 191

MATCHES excluding transitions: 191 / 191   (tolerance 0.0005 s on offset and duration)
```

The chain **does** agree exactly. The committed validator cannot show it.

**Two consequences, and the second is the serious one.**

**(a)** The `191 / 191` figure that appears in `STEP0_TIMING_CLOSURE.md`, `ESS_VALIDATION_REPORT.md`, and `PRODUCTION_INTELLIGENCE_SEED.yaml` is a **hard-coded string literal** in the generator (`gen_artifacts_v2.py` lines 219, 280, 1000, 1018, 1207), not a value read from any validation run. `git log` shows `fcpx_resolve.py` has existed in two commits (`8f70dee`, `cfae47d`) and `mine_spine` was constructed identically in both. **No committed code has ever produced the number 191/191.** The measurement is true — this review reproduced it — but the governed artifacts assert it without a producer. That is the same defect class as the ad-hoc figures recorded in `DAY2_PARENT_FORENSIC_AUDIT.md` §9.

**(b)** `resolved_spine_n` and `etc_spine_n` are both recorded and **never compared**. `zip` truncates to the shorter list without raising. An ETC containing fewer spine entries than the timeline holds would validate against its own prefix and report a clean match on the portion it covers, while the uncovered tail is never examined and never reported as uncovered. Under the standing **NO SILENT RECOVERY** constraint this is a defect, not a limitation: the condition is neither stopped on nor classified.

**Bearing on Q1:** the ETC gate is the first gate the 08-24 lineage must pass, and the gate's mechanism is broken in a direction that produces a *false negative* (1/191 on data that agrees perfectly). An operator seeing that output has two options — halt on a fault that does not exist, or override the validator. Both are worse than not running it.

---

### 1.2 · There is no `AR2-0824.observations.json`

The generator's `--observations` input is mandatory and carries thirteen observation classes:

```
segments · cues · visual_events · not_observed · delta_ledger · audio_sources
progressions · energy · voice_over · offset_model · anchors · die_v · provenance
```

`intelligence/p2/ess/context/` contains `AR2-0822.context.json`, `AR2-0822.observations.json`, and `AR2-0824.context.json`.

**There is no 08-24 observations file, and no partial one.** The generator cannot start.

This is not a formatting gap. Every one of those thirteen classes is a Stage-3 `OBSERVATION` product under **ER-004**, derived from the 08-24 picture and audio. None has been derived. The ETC does not contain any of them and cannot supply any of them.

---

### 1.3 · Two observation producers do not exist, and the input they would need is not designated

Recorded as `T12` in the conformance report and unchanged since:

| Missing input | Consumer | Observation classes it produces |
|---|---|---|
| `video_obs_2fps.npy` | `die_v_observables.py` | `visual_events`, `not_observed`, `die_v` |
| `audio_rms_0p25.npy` | `step0_offset.py` | `offset_model`, `anchors` |

No committed script produces either file. For 08-22 both classes were **reconstructed from the published artifacts** — stated in the observations file's own provenance:

```json
"offset_model/anchors": "RECONSTRUCTED from base/STEP0_TIMING_CLOSURE.md -
   step0_offset.py needs audio_rms_0p25.npy and no producer for it exists in the repository",
"die_v.thresholds": "RECONSTRUCTED from base/VISUAL_EVENT_REGISTRY.yaml -
   die_v_observables.py needs video_obs_2fps.npy and no producer for it exists in the repository"
```

Reconstruction from published output is available for 08-22 because 08-22 has published output. **For 08-24 there is nothing to reconstruct from.** The only route is forward derivation, and forward derivation needs a proxy.

`AR2-0824.context.json` declares:

```json
"proxy": { "name": "NOT_DESIGNATED", "video_duration_s": null,
           "container_duration_s": null, "resolution": "NOT_DESIGNATED", "fps": null },
"sha": { "mp4": "NOT_DESIGNATED", ... }
```

**No 08-24 proxy is designated.** Two of the four source hashes in the four-source chain are absent — the ETC is one, the MP4 is the other. The ETC is the one under discussion; the MP4 is not, and is equally required.

---

### 1.4 · The generator still writes 08-22 constants into all seven artifacts

`ECR-GEN-001` `T9` reported *"no 08-22 constants — 0 across 10 classes"*. That result stands as scoped and the scope was insufficient. `T9` tested the ten classes that feed **computation** — `SHA`, runtime lock, git commit, `RUN_ID`, segments, cues, visual events, delta ledger, not-observed set, source roots. It did not test literals written **directly into output text**, because output text was assumed to be derived from the tested classes. It is not, everywhere.

**Measured on `gen_artifacts_v2.py` at `cfae47d`: 47 lines carry 08-22 production literals.** Distribution by output artifact:

| Output artifact | writer | lines carrying 08-22 literals |
|---|---|---|
| `STEP0_TIMING_CLOSURE.md` | `L` | 8 |
| `CAPTION_REGISTRY.yaml` | `C` | 3 |
| `VISUAL_EVENT_REGISTRY.yaml` | `V` | 4 |
| `EDITORIAL_SYNCHRONIZATION.yaml` | `S` | 1 |
| `CONDUCTOR_SCORE.yaml` | `K` | 1 |
| `ESS_VALIDATION_REPORT.md` | `R` | 8 |
| `PRODUCTION_INTELLIGENCE_SEED.yaml` | `P` | 8 |
| continuation strings / comments | — | 14 |

**All seven artifacts are affected.** Representative instances:

| Line | Literal written | Correct 08-24 value |
|---|---|---|
| 1206 | `etc_elements_resolved: 1025` | 1096 *(measured this session)* |
| 1205 | `srt_cues_parsed: 2291` | 2036 *(present in context as `srt.cues`, unused)* |
| 1172 | `spine_elements: 191, connected_elements: 404` | 201 spine excl. transitions; connected census unestablished |
| 1165–1171 | `bytes: 399320021` / `4479627` / `140526` / `183116` | four different files |
| 1165–1171 | `Filmage_Editor.mp4` · `Info.fcpxml` · `P2_LOCK_timing.json` | `NOT_DESIGNATED` · `Info_analysiscut.fcpxml` · `NOT_PRODUCED` |
| 477 | `declared_lock_tc: "01:20:46:14"` | 08-24 lock is 4689.5 s |
| 1189 | `runtime_processed_tc: "01:20:46.625"` | 4689.5 s |
| 201, 209, 379, 385, 1022, 1028 | picture-verification probe windows and their results | probes never run on 08-24 |

`PRODUCTION_INTELLIGENCE_SEED.yaml` is the worst case: these are not prose, they are **machine-readable YAML fields** that downstream consumers read as measurements. A regeneration run today would emit a seed asserting 2291 cues and 1025 resolved elements for a film that has 2036 and 1096.

Note the failure mode: the generator **would not error**. It would run to completion and emit seven well-formed, hash-stamped, correctly-structured artifacts describing the wrong film. This is `R-4`'s signature — *wrong film, right format, no error* — reappearing in a second, independent place.

---

## 2 · Q2 — Is the missing ETC the single gating dependency?

### **NO.** The ETC is one of twelve blockers, and it is not the binding one.

**Blocker register.** Column `ETC?` states whether the blocker would still exist the moment an authoritative 08-24 ETC is delivered.

| # | Blocker | Class | Severity | Still blocking after ETC arrives? |
|---|---|---|---|---|
| **B-1** | ETC validator compares against the wrong set; `zip` truncates without assertion | implementation defect | **BLOCKING** | **YES** — the ETC cannot be validated |
| **B-2** | No `AR2-0824.observations.json` | missing input | **BLOCKING** | **YES** |
| **B-3** | No producer for `video_obs_2fps.npy` / `audio_rms_0p25.npy` | missing producer | **BLOCKING** | **YES** |
| **B-4** | 47 residual 08-22 literals across all seven artifacts | implementation defect | **BLOCKING** | **YES** |
| **B-5** | Segment set is 08-22 seconds; `segment_authority_status: SUPERSEDED_PENDING_REDERIVATION`; `EPR-001` binds beats to `S01…S18` | governance + input | **BLOCKING** | **YES** — requires Executive ratification |
| **B-6** | Path B regeneration target undefined — Parent assembly artifact, or three episodic deliverables, or both | **architectural, unresolved** | **BLOCKING** | **YES** — requires an Executive Order |
| **B-7** | No 08-24 proxy designated; `sha.mp4: NOT_DESIGNATED` | missing input | **BLOCKING** | **YES** |
| **B-8** | `git_commit: AWAITING_INGESTION` in the 08-24 context | missing input | **BLOCKING** | **YES** |
| **B-9** | `R-4` — no `production_id` cross-check between `--context` and `--observations` | residual risk | **HIGH** | **YES** |
| **B-10** | `T11` — committed `CONDUCTOR_SCORE.yaml` (`1464e335`) ≠ generator output (`fc481954`) | repository drift | **PROCEDURAL** | **YES** — corrupts the regression baseline |
| **B-11** | **ETC `NOT_PRODUCED`** | missing input | **BLOCKING** | *n/a — this is the ETC* |
| **B-12** | `GE-6` — three ESS PDRs OPEN; `GATE-2026-08-22-MIE-DOWNSTREAM` CLOSED | procedural | **PROCEDURAL** | **YES** |

**All eleven non-ETC blockers survive the ETC's arrival.** The ETC is a necessary input. It is not the constraint.

### 2.1 · `B-6` is the blocker no amount of engineering resolves

The Executive Order of 2026-08-26 established that the three Parts are `DISTRIBUTION_DELIVERABLES` and the Parent is an **assembly artifact**. Path B — Episodic Production Architecture — was ratified on 2026-08-28.

`gen_artifacts_v2.py` emits **one artifact set for one `production_id`**. `AR2-0824.context.json` describes the Parent: `runtime_s: 4689.5`, one FCPXML, one SRT.

No Order states what atomic regeneration targets. Three readings are each defensible from the record:

1. **The Parent only** — the assembly artifact gets an ESS artifact set; the episodes inherit by reference.
2. **The three episodes only** — the distribution deliverables get artifact sets; the Parent is scaffolding and is not a governed product.
3. **All four** — one Parent set plus three episode sets, with a defined relationship between them.

Each implies a different `--context`/`--observations` pairing, a different segment set, a different `RUN_ID` scheme, and — under reading 2 or 3 — **a generator that does not currently exist**, because nothing in the codebase produces per-episode artifact sets or relates them to a parent.

Engineering cannot select among these. `DOC-CAND-001` — *the platform prepares decisions; it does not make artistic ones* — and the standing prohibition on inferring Executive intent both apply. **This is reported as an open Executive question, not as an engineering task.**

Scoping `ECR-GEN-002` before `B-6` is answered risks building the wrong generator correctly.

### 2.2 · `B-5` has a dependency the register does not show

`EPR-001` is ratified at v1.13.0 and binds six beats to segment references `S01…S18`. Those references are 08-22 segment identifiers on 08-22 seconds. The registry itself carries `segment_authority_status: SUPERSEDED_PENDING_REDERIVATION`.

Re-deriving the 08-24 segment set will produce boundaries that are not the 08-22 boundaries — the forensic audit measured a 73.800 s re-prepended opening on two of three Parts and 15.0–19.6 s uncaptioned tails, so the runtimes differ by 157.125 s in total. **The re-derived segments will not map one-to-one onto `S01…S18`.**

At that point one of two things is true, and only the Executive can say which:

- the ratified `EPR-001` beat structure **survives** re-derivation and is re-bound to new segment IDs, or
- the beat structure was authored against a superseded segmentation and requires **Executive re-authoring**.

The platform must not choose. `EPR-001` order §2.3 — *the platform SHALL NOT author, populate, infer, extend, suggest, or default ANY EPR-001 value* — governs the re-binding as much as the original authoring.

**This is the single largest schedule risk in the register and it is not an engineering task.**

---

## 3 · Q3 — What constitutes an acceptable 08-24 ETC

*Acceptance criteria only. Not how to build it. Not who builds it.*

Derived from the 08-22 ETC's actual schema (`P2_LOCK_timing.json`, 183 116 bytes) and from what `fcpx_resolve.py` and `gen_artifacts_v2.py` actually consume.

**For regeneration to begin, the 08-24 Editorial Timing Contract must contain:**

### `ETC-A1` — `source`
Absolute path of the FCPXML the contract was exported from.

### `ETC-A2` — `source_sha256`
SHA-256 of that FCPXML. **Must equal exactly:**

```
1ab3d12f0dd150c63907a4b2e4bac4253baf8100910dfda74daa3a5378b6b4d2
```

This is the hash the platform computed for `analysis_cut/Info_analysiscut.fcpxml`. Any other value means the ETC describes a different export. **Inequality is a STOP condition, not a warning.**

### `ETC-A3` — `sequence`
An object carrying:

| field | requirement |
|---|---|
| `duration_s` | **must equal `4689.5` exactly** |
| `format_ref` | format element id |
| `declared_lock` | lock timecode as a string, at 24/1 NDF |

### `ETC-A4` — `spine`
An array, **in timeline order**, of every primary-spine element **excluding transitions**.

**Expected length: `201`** — measured this session from `Info_analysiscut.fcpxml` (225 elements at depth 0, of which 24 are transitions; the remainder is 188 `asset-clip` + 8 `clip` + 5 `gap`).

Each entry must carry all nine fields:

```
tag · name · lane · depth · parent · timeline_offset_s · rel_offset_s · duration_s · source_start_s
```

`timeline_offset_s` and `duration_s` must be **non-null, in seconds, absolute to the sequence origin**. These two fields are the entire basis of the validation; a null in either makes the entry unvalidatable.

**Tolerance:** `0.0005 s` on both, per the resolver's comparison.

**Ordering:** the comparison is positional. The array order must match timeline order with no gaps and no re-sorting.

### `ETC-A5` — `connected_elements`
An array of every connected (lane ≠ null) element, same nine-field shape.

`timeline_offset_s` **may be null** — the 08-22 ETC published null for all 404 — provided `rel_offset_s` is populated, since the platform resolves connected elements from FCPXML nesting rather than from the contract.

**Disclosed limitation:** the platform performs **no validation whatsoever** on `connected_elements`. The resolver ignores the array; only its length is recorded, into `AR2-0824.context.json` as `etc.connected`. This class is therefore accepted **on trust**. It is stated here so the Executive knows which part of the contract carries no independent check, not as a criterion the platform can enforce.

### `ETC-A6` — Independence of instrument
The ETC must be produced by the editorial system, or by any instrument **other than `fcpx_resolve.py`**.

`DOC-001` requires the instrument be validated by conformance before its fidelity is trusted. If the ETC is generated from the same parser whose output it is used to check, the agreement is tautological and the validation establishes nothing. The evidentiary value of `ETC-A4` comes entirely from the two instruments being independent.

### `ETC-A7` — Completeness assertion
The contract must be complete for the sequence it names — `len(spine)` must equal the count of non-transition depth-0 elements in the FCPXML at `ETC-A2`.

The platform **cannot currently enforce this** (`B-1`: `zip` truncates silently). Until `B-1` is corrected, `ETC-A7` is an assertion the supplier makes and the platform cannot check.

### `ETC-A8` — Immutability and pinning
On acceptance, the ETC is hashed, and `AR2-0824.context.json` is updated:

```
sha.etc        <- SHA-256 of the accepted contract   (currently "NOT_PRODUCED")
etc.spine      <- len(spine)                          (currently null)
etc.connected  <- len(connected_elements)             (currently null)
source_files.etc <- path                              (currently "NOT_PRODUCED")
```

The contract is thereafter immutable. A revised ETC is a new contract with a new hash and a new `RUN_ID`, not an edit — `DOC-002`, *regenerate, never patch*.

---

### 3.1 · What an acceptable ETC does **not** supply

Stated to prevent the acceptance criteria being read as a readiness gate:

An ETC meeting `ETC-A1…A8` supplies **timeline geometry and one hash-chain link**. It does not supply, and cannot supply:

- any of the thirteen observation classes (`B-2`)
- the proxy or its hash (`B-7`)
- the segment set or its Executive ratification (`B-5`)
- the regeneration target under Path B (`B-6`)
- the ingestion commit (`B-8`)

---

## 4 · Q4 — Exact post-ETC execution sequence

Sixteen gates, `G0`–`G15`. Each states its **owner**, its **precondition**, and its **stop condition**. A gate that cannot report its stop condition is not a gate.

```
  ┌─────────────────────────────────────────────────────────────────┐
  │  G0   PRECONDITIONS CLEARED   (B-1 · B-3 · B-4 · B-6 · B-10)     │
  └────────────────────────────────┬────────────────────────────────┘
                                   ↓
  G1   RECEIVE ETC                     → hash, verify ETC-A1..A8
                                   ↓
  G2   PIN CONTEXT                     → sha.etc, etc.spine, etc.connected,
                                          sha.mp4, git_commit
                                   ↓
  G3   RESOLVE FCPXML                  → fcpx_resolve.py, timeline.json
                                   ↓
  G4   VALIDATE AGAINST ETC            → 201/201 or STOP        [needs B-1]
                                   ↓
  G5   DERIVE CAMERA RUNS              → camera_runs.json
                                   ↓
  G6   PRODUCE OBSERVATION INTERMEDIATES                        [needs B-3, B-7]
                                   ↓
  G7   DERIVE SEGMENT SET              → machine proposal only
                                   ↓
  G8   EXECUTIVE RATIFICATION          → segments + EPR re-binding  [EXECUTIVE]
                                   ↓
  G9   ASSEMBLE OBSERVATIONS           → AR2-0824.observations.json
                                   ↓
  G10  RUNTIME GUARDS                  → production_id, closure, census
                                   ↓
  G11  GENERATE RUN_ID                 → --run-id auto
                                   ↓
  G12  ATOMIC BUILD                    → seven artifacts, scratch tree
                                   ↓
  G13  POST-BUILD VERIFICATION         → residual-literal scan, closure re-check
                                   ↓
  G14  PUBLISH                         → commit to intelligence/p2/ess/
                                   ↓
  G15  EXECUTIVE REVIEW                                          [EXECUTIVE]
```

### Gate detail

| Gate | Action | Owner | Precondition | Stop condition |
|---|---|---|---|---|
| **G0** | Confirm `B-1`, `B-3`, `B-4`, `B-6`, `B-10` are closed | Engineering | `ECR-GEN-002` complete | any still open → do not enter G1 |
| **G1** | Receive ETC; compute SHA-256; check `ETC-A1…A8` | Engineering | ETC delivered | any criterion unmet → **STOP**, report, do not proceed |
| **G2** | Write `sha.etc`, `etc.spine`, `etc.connected`, `source_files.etc`, `sha.mp4`, `git_commit` into `AR2-0824.context.json` | Engineering | G1 | any field still `NOT_DESIGNATED` / `AWAITING_INGESTION` → **STOP** |
| **G3** | `fcpx_resolve.py Info_analysiscut.fcpxml <ETC> timeline_0824.json` | Machine | G2 | parse failure, or `spine_end_s ≠ 4689.5` → **STOP** |
| **G4** | ETC binding validation | Machine | `B-1` corrected | `spine_offset_matches ≠ 201`, **or** `etc_spine_n ≠ resolved_spine_n_excl_transitions`, **or** any `out_of_range` → **STOP** |
| **G5** | `derive_camera_runs.py` → `camera_runs.json` | Machine | G3 | any element unassignable to a known family → classify `UNCERTAIN`, do not infer |
| **G6** | Produce `video_obs_2fps.npy`, `audio_rms_0p25.npy`, then `die_v_observables.py`, `step0_offset.py`, `step0_*.py` | Machine | `B-3` corrected, `B-7` designated proxy | any intermediate unproduceable → **STOP** (do not reconstruct from 08-22) |
| **G7** | Derive candidate segment boundaries from G3/G6 | Machine | G6 | insufficient evidence → `INSUFFICIENT_OBSERVATION`, no inferred boundary |
| **G8** | **Executive ratification of the 08-24 segment set, and disposition of the `EPR-001` beat re-binding** | **EXECUTIVE** | G7 | unratified → **STOP**. The platform shall not bind beats to unratified segments |
| **G9** | Assemble `AR2-0824.observations.json`, thirteen classes, with per-class provenance | Engineering | G8 | any class absent or reconstructed → record `NOT_OBSERVED` / `INSUFFICIENT_OBSERVATION`; do not substitute |
| **G10** | Runtime guards: `context.production_id == observations.production_id`; spine closure equals `sequence.duration_s`; cue count equals `context.srt.cues`; segment span union equals runtime | Machine | `B-9` implemented | any assertion false → **STOP** before any artifact is written |
| **G11** | `--run-id auto` → `WECAPE-AR2-0824-<UTC>` | Machine | G10 | id collides with a recorded run → **STOP** |
| **G12** | `gen_artifacts_v2.py --context … --observations … --derived … --sources … --out <scratch> --run-id auto` | Machine | G11 | non-zero exit → **STOP**; no partial publication |
| **G13** | Scan the seven outputs for residual 08-22 literals; re-verify closure and census against G3/G6 independently of the generator | Engineering | G12 | any 08-22 literal present, or any figure not traceable to an input → **STOP**, return to `ECR-GEN-002` |
| **G14** | Publish the seven artifacts to `intelligence/p2/ess/`; commit; record `RUN_ID`, four input hashes, git commit | Engineering | G13 clean | — |
| **G15** | **Executive validation and disposition** | **EXECUTIVE** | G14 | — |

**Two gates are Executive and cannot be discharged by engineering: `G8` and `G15`.** `G8` sits in the middle of the sequence, not at the end. Regeneration is not a single unattended run; it halts for an Executive decision at its midpoint.

**One property of this sequence is worth stating plainly:** `G12` — the atomic build itself — is the shortest step in the list. Everything expensive is upstream of it.

---

## 5 · Q5 — Should `ECR-GEN-002` occur before or after ETC availability?

### **BEFORE.** `ECR-GEN-002` is the critical path; the ETC is not.

**Engineering rationale, five points.**

**5.1 · The ETC's only consumer is broken.** `B-1` means an ETC delivered today reaches a validator that reports `1/191`-class results on data that agrees exactly. The ETC would sit unvalidated — or, worse, be validated by an override, which is precisely the silent substitution the standing constraints forbid. **The work that makes the ETC useful must precede the ETC.**

**5.2 · `ECR-GEN-002` has no dependency on the ETC.** Every item in its natural scope is testable against the 08-22 pair, which the platform already holds complete:

| `ECR-GEN-002` scope item | Testable today against 08-22? |
|---|---|
| `B-1` fix `mine_spine` transition filter + assert `etc_spine_n == resolved_spine_n` | **YES** — expected result `191/191`, already measured |
| `B-4` eliminate 47 residual literals | **YES** — regression is byte-equality against the seven `fc481954`-class hashes |
| `B-9` `production_id` cross-check | **YES** — negative test: 0822 context + 0824 observations must raise |
| `B-3` write the two `.npy` producers | **YES** — 08-22 proxy exists; success criterion is reproducing the published `die_v` thresholds and `offset_model` |
| `B-10` resolve the stale `CONDUCTOR_SCORE.yaml` | **YES** — requires regeneration authority, not an ETC |
| extend `T9` to narrative and manifest literals | **YES** |

**Sequencing `ECR-GEN-002` after the ETC would idle the entire scope behind an input none of it needs.**

**5.3 · The 08-22 pair is the only complete regression fixture that will ever exist.** It has four hashed sources, a published artifact set, and a known-good ETC. Once work moves to 08-24 — where the ETC is new, the observations are new, and the segments are unratified — **there is no oracle**. Every `ECR-GEN-002` correction verified after the switch would be verified against output nobody has seen before. The 08-22 fixture is a wasting asset and it should be spent while it is still the *only* thing that can prove a change is behaviour-neutral.

**5.4 · `B-4` is a silent-failure class, and silent failures must be closed before first use, not after.** A regeneration run on 08-24 with `B-4` open produces seven well-formed artifacts asserting 2291 cues and 1025 resolved elements for a film with 2036 and 1096. There is no exception, no exit code, no log line. If those artifacts are published before the residual-literal scan is written, **the defect enters the governed record and `DOC-002` requires a full regeneration to remove it** — which requires another Executive authorization, which the current Order does not grant.

**5.5 · The counter-argument, stated fairly.** Doing `ECR-GEN-002` first means the ETC — once produced — waits. If the ETC has a shelf life, or if the editorial team's availability is the binding constraint, there is a real cost to leaving it on the shelf. **The mitigation is that ETC production and `ECR-GEN-002` are performed by different parties and do not compete for the same resource**, so they can proceed concurrently; what must not happen is *regeneration* being attempted on the ETC's arrival.

**The recommendation is therefore about the order of `regeneration`, not the order of `work`:** commission the ETC now, run `ECR-GEN-002` now, and do not enter `G1` until `G0` is clear.

### 5.1a · One scope item `ECR-GEN-002` must **not** contain

`B-5` (segment re-derivation and `EPR-001` re-binding) and `B-6` (Path B regeneration target) must not be scoped into an engineering change request. Both require Executive declaration. An `ECR` that silently picks a segmentation or a target would be the platform inferring Executive intent — prohibited by the Ratification Order §4 and by `EPR-001` §2.3.

**They are named here as Executive decisions blocking `G8` and `G0` respectively.**

---

## 6 · Executable now vs inherently blocked

### 6.1 · Executable before an authoritative 08-24 ETC exists

| Work | Blocker closed | Verifiable against |
|---|---|---|
| Correct `fcpx_resolve.py` spine comparison; add the count assertion | `B-1` | 08-22 pair → `191/191` |
| Remove the 47 residual 08-22 literals; route every emitted figure through `--context` / `--observations` | `B-4` | byte-equality on all seven 08-22 artifacts |
| Implement the `production_id` cross-check and closure guards | `B-9` | negative tests on mismatched pairs |
| Write producers for `video_obs_2fps.npy` and `audio_rms_0p25.npy` | `B-3` | reproduce published 08-22 `die_v` / `offset_model` |
| Extend `T9` to narrative and manifest literal classes | test-scope gap | re-run on 08-22 |
| Add `T3`/`T4` execution against the **08-22** ETC (never previously run) | test-scope gap | the pair already held |
| Designate and hash the 08-24 proxy; record the ingestion commit | `B-7`, `B-8` | context completeness |
| Resolve `T11` — regenerate or supersede `CONDUCTOR_SCORE.yaml` | `B-10` | requires **Executive regeneration authority** |
| Derive 08-24 timeline, camera runs, SRT census | — | already done this session; ETC-free |
| Draft the 08-24 candidate segment set as a **machine proposal** | prepares `B-5` | proposal only; no authority claimed |

### 6.2 · Inherently blocked until an authoritative ETC exists

| Work | Why the ETC is irreplaceable |
|---|---|
| `G4` ETC binding validation (`T3`) | the ETC is the second instrument; `DOC-001` requires two |
| `G4` segment binding against validated geometry (`T4`) | depends on `T3` |
| Closing the four-source hash chain | `sha.etc` has no substitute |
| Any frame-accurate claim in a published 08-24 artifact | the licence for frame-accuracy is the ETC agreement, per `STEP0_TIMING_CLOSURE` |
| `G14` publication | an artifact set with `etc_validation: NOT_VALIDATED` is not a governed product |

### 6.3 · Blocked by Executive declaration, not by engineering and not by the ETC

| Decision | Blocks |
|---|---|
| **Path B regeneration target** — Parent, three episodes, or both | `G0`; the scope of `ECR-GEN-002` |
| **08-24 segment set ratification** | `G8` |
| **`EPR-001` beat re-binding disposition** after re-segmentation | `G8` |
| **Regeneration authority for `T11`** | `B-10` |
| **`ER-005` Editorial Lineage Classification** (proposed, undrafted) | pre-execution lineage checks |

---

## 7 · What this review did not do

Enumerated against the standing prohibitions.

- **No governed artifact was regenerated.** `fcpx_resolve.py` was executed twice, read-only, with output written to session scratch (`~/rr/`). No repository file was modified.
- **No Executive declaration, `EPR` field, or registry was read for modification or altered.**
- **No Executive intent was inferred.** `B-5` and `B-6` are reported as open Executive questions with the readings enumerated and none selected.
- **No missing value was populated or defaulted.** `NOT_DESIGNATED`, `NOT_PRODUCED`, and `AWAITING_INGESTION` are reported as they stand.
- **No defect was silently repaired.** `B-1` is diagnosed with the exact line and the exact corrected expression, and left uncorrected — correcting a governed instrument is engineering work requiring its own change request.
- **No compliance aggregate, score, ranking, or readiness percentage is stated.** Q1 is answered NO on four independently sufficient findings, not on a tally.

---

## 8 · Standing state after this review

```
ETC (08-24)                       NOT_PRODUCED
ETC validator                     DEFECTIVE - B-1, diagnosed, uncorrected
08-24 observations                ABSENT
08-24 proxy                       NOT_DESIGNATED
08-24 segment authority           SUPERSEDED_PENDING_REDERIVATION
Path B regeneration target        UNDECLARED
generator residual literals       47 lines, all seven artifacts
production_id guard               NOT IMPLEMENTED
CONDUCTOR_SCORE.yaml              STALE - regeneration authority not granted
atomic regeneration               NOT READY - B-1..B-12
```

**Prepared for Executive review. No execution is directed by this document.**
