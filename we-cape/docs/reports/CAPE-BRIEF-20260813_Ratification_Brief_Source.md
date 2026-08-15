# W.E. C.A.P.E.™ RATIFICATION REVIEW

## Purpose

This document presents the recommendations we propose to **ratify as architectural principles for W.E. C.A.P.E.™ (Creator Asset Production Ecosystem)** following:

- production experience with `AlphaRoundUp_2026`;
- the Part 1 / Part 2 chrono-SET workflow;
- Claude's technical assessment of the proposed Final Cut Pro correlation architecture;
- observed Final Cut Pro timestamp behavior;
- DJI camera-body identification testing;
- subsequent architectural review.

Treat these as **proposed CAPE specification decisions**, not merely workflow tips.

Please review them critically before ratification. Identify any contradiction with existing CAPE ADRs, schemas, findings F1–F5, custody rules, lineage requirements, or production-proven behavior.

---

# I. FUNDAMENTAL ARCHITECTURAL MODEL

We recommend that CAPE explicitly distinguish three layers:

## Layer 1 — SOURCE TRUTH

The original captured media and its custody/provenance record.

Original assets are evidence.

They are not modified merely to make an NLE easier to organize.

## Layer 2 — CAPE TRUTH

The CAPE registry/catalog contains CAPE's authoritative interpretation of each asset:

- asset identity;
- original filename/path;
- cryptographic identity;
- camera identity;
- temporal normalization;
- provenance;
- lineage;
- SET/scene relationships;
- evidence;
- confidence;
- rights state;
- other production metadata.

CAPE may derive conclusions from source evidence, but the derivation must remain distinguishable from the underlying evidence.

## Layer 3 — EDITORIAL PRESENTATION

Final Cut Pro is an editorial interface consuming CAPE-derived organization.

FCP clip names, keywords, collections, Camera Name, Camera Angle, roles, FCPXML, etc. are **presentation/editorial metadata**.

They must not become the sole authoritative record of CAPE asset identity or chronology.

### Proposed principle

> **Final Cut Pro is the editorial interface; the CAPE registry is the organizational authority; immutable source media remains the evidentiary foundation.**

---

# II. ORIGINAL-ASSET IMMUTABILITY

## RATIFY

CAPE must never rename original captured media merely for organizational convenience.

Example original:

`DJI_20260626125016_0024_D.MP4`

remains:

`DJI_20260626125016_0024_D.MP4`

CAPE should likewise avoid modifying original embedded timestamps, metadata, or file contents to "correct" them.

Corrections belong in the registry/presentation layer.

### Reasons

Renaming originals can jeopardize or complicate:

- lineage;
- parent-stem matching;
- custody verification;
- archive reconciliation;
- re-offload comparison;
- FCP relinking;
- camera-card structures;
- external applications;
- future forensic/recovery work.

### Proposed principle

> **CAPE adapts its catalog to the source. CAPE does not alter the source to fit its catalog.**

---

# III. ORIGINAL FILENAME PRESERVATION

## RATIFY

Every asset record must retain the original camera-generated filename.

Recommended minimum:

`original_filename`

`original_path`

`asset_id`

The original filename remains an important lineage and provenance attribute even when CAPE presents a different human-readable name inside FCP.

---

# IV. STABLE ASSET IDENTITY

## RATIFY

Every asset should receive a stable CAPE asset identifier independent of:

- filename;
- card;
- folder;
- FCP Event;
- FCP Library;
- camera-generated sequence number.

Where the existing registry already uses SHA-256 as asset identity, retain that architecture unless there is a compelling reason to introduce a separate logical UUID.

CAPE must distinguish:

**content identity**

from:

**human-readable naming**

from:

**physical storage location**

---

# V. CAMERA BODY IS NOT CARD IDENTITY

## RATIFY

A removable SD/SanDisk card is a storage/provenance object, **not camera identity**.

A novice may:

1. use a card in DJI5;
2. remove it;
3. insert it into DJI6;
4. continue shooting;
5. later offload all material together.

Therefore CAPE must determine camera identity independently of the card.

### Standard body codes currently proposed

`X5` — Insta360 X5

`OM1` — OM System OM-1 Mark II

`DJI5` — DJI Osmo Action 5 Pro

`DJI6` — DJI Osmo Action 6

Body codes should remain short, stable, machine-safe, and human-readable.

---

# VI. CAMERA IDENTITY REQUIRES PROVENANCE

## RATIFY WITH REFINEMENT

Do not store only:

`camera_body_code = DJI5`

Store how CAPE reached that conclusion.

Recommended fields:

`camera_body_code`

`camera_unit_serial`

`camera_id_source`

`camera_id_confidence`

Potential `camera_id_source` values could include:

- custody_manifest
- source_offload_job
- serial_metadata
- model_metadata
- embedded_metadata
- filename_signature
- operator_declaration
- inferred
- unknown

### Proposed evidence precedence

Prefer approximately:

**verified custody/offload provenance**

→ **unique camera serial/unit metadata**

→ **embedded model metadata**

→ **known camera-specific signature**

→ **operator declaration**

→ **inference**

→ **UNKNOWN**

Do not silently convert weak inference into asserted fact.

---

# VII. DJI5/DJI6 FINDING MUST INFORM THE DESIGN

## RATIFY AS A REQUIREMENT

Production testing showed that body identity cannot be assumed to exist in easily accessible metadata.

For the tested 31 DJI clips:

- Spotlight acquisition-model lookup returned UNKNOWN;
- the registry contained generic DJI family identity or null identity;
- therefore make/family identification was insufficient to distinguish the two physical DJI camera types.

This means CAPE requires a **camera-identity resolution mechanism**, not merely a metadata lookup.

The current custody/offload structure may provide stronger evidence because the per-camera source/offload job can establish provenance even when the media itself exposes inadequate model metadata.

However:

> **Filesystem inode relationships may be useful evidence during the current implementation but should not become CAPE's universal long-term identity model.**

Persist the resolved provenance into the registry.

---

# VIII. CANONICAL EVENT TIME

## RATIFY

CAPE should establish its own canonical event-time field rather than blindly accepting an NLE or filesystem timestamp.

Proposed conceptual field:

`cape_capture_time`

This represents CAPE's best-supported estimate of when capture occurred in the event's real-world chronology.

Conceptually:

**raw timestamp**

+ **timestamp source**

+ **declared timezone**

+ **DST interpretation**

+ **known camera offset**

+ **other temporal evidence**

→ **CAPE canonical event time**

Recommended supporting fields include:

`capture_ts_raw`

`capture_ts_utc`

`tz_offset`

`ts_source`

`ts_confidence`

`per_camera_clock_offset`

`cape_capture_time`

Exact schema names should align with existing F1/F2 work rather than duplicate established fields.

---

# IX. FCP `CONTENT CREATED` IS NOT TEMPORAL AUTHORITY

## RATIFY

Final Cut Pro's:

`Group Clips By > Content Created`

must **not** be treated as CAPE's primary chronological authority.

Production evidence from `AlphaRoundUp_2026` showed that clips could appear according to card-offload/filesystem dates rather than actual event chronology.

Additional risks include:

- filesystem birthtime;
- copy dates;
- naive local timestamps;
- timezone interpretation;
- DST;
- metadata lost during an ingest path;
- camera-specific timestamp semantics.

### Therefore

`Content Created` may remain:

- informational;
- diagnostic;
- a secondary browser view.

It must not override CAPE-normalized chronology.

---

# X. CHRONOLOGY SHOULD BE CARRIED INTO FCP PRESENTATION

## RATIFY

CAPE should calculate chronology before Final Cut organization and carry that chronology into a reliably sortable presentation field.

The current proven mechanism is the **FCP browser clip name**.

Example display name:

`043 · 06-26 12:50:16 · DJI5 · DJI_20260626125016_0024_D`

This communicates:

- sequence;
- CAPE-normalized event date/time;
- camera body;
- original source identity.

The richer FCP display name does **not** imply renaming the physical source file.

### Primary chronological browser operation

Use:

`Sort By > Name`

with ascending order after CAPE normalization.

`Content Created` becomes secondary.

---

# XI. DERIVATIVE FILE NAMING

## RATIFY

When CAPE itself creates a new file—proxy, normalized copy, intermediate, export, generated derivative, etc.—CAPE may control its filename.

Recommended filesystem-safe pattern:

`NNN_YYYYMMDD-HHMMSS_CAM_originalstem.ext`

Example:

`043_20260626-125016_DJI5_DJI_20260626125016_0024_D.MP4`

Use conservative filesystem characters:

- A–Z / a–z
- 0–9
- underscore
- hyphen

Avoid requiring:

- spaces;
- colons;
- middots;
- parentheses;
- automatically generated `(N)` collision suffixes.

Preserve the parent/original relationship in the registry independently of the derivative filename.

---

# XII. CAMERA KEYWORDS SHOULD BE FIRST-CLASS CAPE EDITORIAL METADATA

## RATIFY WITH NAMESPACE REFINEMENT

FCP `Camera Name` is useful where reliable but should not be the sole CAPE mechanism for camera organization.

Body-specific keywords are:

- XML-friendly;
- visible;
- searchable;
- usable as Keyword Collections;
- understandable to novice editors;
- less dependent upon version-specific metadata behavior.

Recommend a namespace:

`CAM_X5`

`CAM_OM1`

`CAM_DJI5`

`CAM_DJI6`

rather than bare:

`X5`

`OM1`

`DJI5`

`DJI6`

This prepares CAPE for additional namespaces such as:

`SET_07`

`LOC_HOTEL`

`EVT_BIKE_NIGHT`

`RIGHTS_ORIGINAL`

etc.

### Proposed rule

**Camera keyword = CAPE editorial organization**

**FCP Camera Name = optional convenience/enhancement**

The registry remains authoritative for actual camera identity.

---

# XIII. TEMPORAL OVERLAP DOES NOT EQUAL SCENE MEMBERSHIP

## RATIFY AS A CORE RULE

This distinction is essential.

If four cameras record at 12:50, they are not necessarily recording the same scene.

Example:

- DJI5 — hotel parking lot
- X5 — motorcycle at gas station
- OM1 — restaurant interior
- DJI6 — rider several blocks away

Perfect timestamp agreement proves temporal coincidence, not spatial or narrative coincidence.

Therefore:

> **Temporal overlap generates a candidate relationship. It does not prove SET/scene membership.**

---

# XIV. SCENE/SET CORRELATION SHOULD BE EVIDENCE-BASED

## RATIFY

Potential evidence classes include:

1. normalized temporal overlap;
2. per-camera sequence/adjacency continuity;
3. known itinerary/schedule;
4. custody/operator assignment;
5. GPS/GPX anchors;
6. audio similarity;
7. visual similarity;
8. spoken-word/contextual similarity;
9. manual markers;
10. human editorial confirmation.

GPS should be considered **corroborating evidence**, not a mandatory prerequisite.

### Important principle

**No GPS does not prevent CAPE correlation.**

---

# XV. CONFIDENCE-SCORED RELATIONSHIPS

## RATIFY

Automatically inferred relationships should carry:

`membership_confidence`

and:

`membership_evidence`

A time-only match should generally remain:

**SUGGESTED**

rather than automatically becoming:

**CONFIRMED**

For automatic SET assignment, CAPE should ideally require multiple independent evidence classes or a sufficiently authoritative single source.

Exact thresholds should remain configurable/empirical rather than being prematurely hard-coded into the architectural principle.

### Human authority

Manual human confirmation should be capable of overriding inferred membership while preserving enough history to explain what CAPE originally proposed.

---

# XVI. REFINED CAPE HIERARCHY

The earlier shorthand was:

**TIME → SET/SCENE → CAMERA**

That remains useful operationally, but it is too simplistic as the architectural model because time itself can require interpretation.

We recommend the deeper model:

# ASSET → EVIDENCE → CANONICAL EVENT TIME → SET/SCENE → CAMERA PERSPECTIVE

Reason:

CAPE begins with an asset and available evidence.

From evidence it determines:

- probable capture time;
- probable camera identity;
- probable location/context;
- probable SET relationship.

Those derived conclusions should not be confused with immutable source facts.

### Architectural principle

> **CAPE records both conclusions and the evidence used to reach them.**

---

# XVII. CAMERA CLOCK SYNC SHOULD BECOME A PRE-SHOOT SOP

## RATIFY

Add a formal **Camera Clock Sync** procedure to CAPE preflight/SOP-04 or the appropriate existing SOP.

Before production:

1. Select one authoritative clock, preferably a network-synchronized phone.
2. Verify timezone and DST assumptions.
3. Set all camera clocks as closely as practical.
4. Record the authoritative clock display with every camera for approximately 10 seconds.
5. Where practical, include a common audible/visual synchronization event.
6. Record relevant timezone/camera configuration in `shoot.yaml` or the existing shoot manifest.

The filmed clock provides measurable evidence if a camera's internal clock proves inaccurate later.

---

# XVIII. STORE OFFSETS; DO NOT "FIX" ORIGINALS

## RATIFY

When a camera clock is wrong:

Do **not** rewrite the original file's timestamp merely to make it agree with other cameras.

Instead store something equivalent to:

`per_camera_clock_offset`

and apply the correction during CAPE normalization.

Example conceptually:

`raw camera time 12:47:11`

`camera offset +00:02:49`

`CAPE event time 12:50:00`

The raw evidence remains preserved.

---

# XIX. DISCOVERY SYNC AND EDIT SYNC ARE DIFFERENT PROBLEMS

## RATIFY

CAPE timestamp normalization needs enough accuracy to locate candidate media in the same temporal neighborhood.

It does not necessarily need frame-accurate synchronization.

For actual multicamera editing:

- audio waveform synchronization;
- synchronized clips;
- multicam synchronization;
- visual sync markers;

can provide substantially finer alignment.

Therefore:

**CAPE temporal normalization = discovery/correlation**

**FCP audio/multicam synchronization = editorial frame alignment**

Do not unnecessarily require one mechanism to solve both problems.

---

# XX. RECOMMENDED PER-ASSET METADATA MODEL

Subject to reconciliation with the existing registry schema, CAPE should be able to represent:

### Identity

`asset_id`

`original_filename`

`original_path`

`content_hash`

### Camera

`camera_body_code`

`camera_unit_serial`

`camera_family`

`camera_id_source`

`camera_id_confidence`

### Time

`capture_ts_raw`

`capture_ts_utc`

`tz_offset`

`ts_source`

`ts_confidence`

`per_camera_clock_offset`

`cape_capture_time`

### Story Organization

`set_id`

`scene_label`

`membership_confidence`

`membership_evidence`

### Provenance / Lineage

`source_offload_job`

`card_volume_label`

`lineage_parent_asset_id`

`lineage_parent_stem`

### Governance

`rights_class`

and existing Gate-1/consent state as required.

### Optional where known

`operator`

`lens`

`recording_mode`

`resolution`

`frame_rate`

`codec`

`location`

`GPS/GPX relationship`

Do not make optional metadata mandatory for successful ingestion.

---

# XXI. NOVICE-SAFETY PRINCIPLES

## RATIFY

CAPE is specifically intended to reduce the ability of novice operators to damage media organization.

Therefore:

### Originals

Treat originals as effectively read-only after verified offload.

### Organization

Prefer:

- registry records;
- FCPXML;
- keywords;
- collections;
- presentation names;
- reversible relationships;

over filesystem manipulation.

### Automation

Automated conclusions should expose confidence.

### Ambiguity

UNKNOWN is preferable to a confidently wrong value.

### Camera cards

Never assume card = camera.

### Timestamp

Never assume filesystem date = capture date.

### FCP

Never assume an FCP metadata field is authoritative merely because Final Cut displays it.

### Human intervention

Allow simple manual confirmation/correction without requiring the novice to understand the underlying registry architecture.

---

# XXII. CURRENT ALPHAROUNDUP PART 2 PRODUCTION RULE

## RATIFY AS AN OPERATIONAL DECISION, NOT A PERMANENT ARCHITECTURAL RULE

Do not destabilize the current half-completed edit merely to deploy the improved architecture.

During the existing Part 2 edit:

### SAFE

- continue editing;
- resolve DJI5/DJI6 body provenance;
- add body-code keywords to existing browser clips;
- perform registry/schema work outside FCP;
- prepare SOP improvements;
- document findings.

### DO NOT DO MID-EDIT

- rename physical source files;
- regenerate and re-import the entire organizational FCPXML into the active edit merely to obtain new metadata;
- create duplicate browser media unnecessarily;
- undertake architecture-driven restructuring that provides less value than maintaining edit momentum.

### Natural deployment boundary

Use the **Part 2 → Part 3 boundary** to introduce the revised generated metadata/FCPXML architecture.

---

# XXIII. PROPOSED CAPE RATIFICATION PRINCIPLES

Please specifically review the following sixteen statements for ratification:

1. **Original media is immutable.**

2. **Original camera filenames are immutable.**

3. **The CAPE registry is the authoritative organizational/catalog layer.**

4. **Every asset has stable identity independent of filename, storage location, card, or NLE.**

5. **Camera body identity is an asset property, never a removable-card property.**

6. **Camera identity records both its conclusion and its evidence source/confidence.**

7. **Canonical event time is derived by CAPE from evidence rather than blindly inherited from FCP or filesystem timestamps.**

8. **Final Cut Pro `Content Created` is not CAPE's authoritative chronological signal.**

9. **CAPE-normalized FCP clip names provide a sortable human-readable representation of event chronology and camera identity without renaming originals.**

10. **Camera-body keywords are CAPE's primary FCP camera-organization mechanism; `Camera Name` is a secondary convenience when reliable.**

11. **Temporal overlap generates candidate SET/scene relationships; it does not prove scene membership.**

12. **GPS is corroborating evidence rather than required evidence.**

13. **Inferred SET/scene relationships carry evidence and confidence and remain human-confirmable/reversible.**

14. **Camera clock synchronization becomes a formal pre-shoot CAPE procedure.**

15. **Clock corrections are stored as offsets/normalization data; original media timestamps are not rewritten.**

16. **Final Cut Pro is CAPE's editorial interface, not CAPE's metadata authority.**

---

# XXIV. REQUEST TO CLAUDE

Please review this as a proposed **CAPE architecture ratification**, not as general editing advice.

For each of the 16 principles, return one of:

**RATIFY**

**RATIFY WITH MODIFICATION**

**REJECT**

For every modification or rejection:

- explain why;
- cite the existing CAPE finding, ADR, production evidence, registry behavior, or technical limitation that conflicts;
- provide replacement wording suitable for insertion into the formal CAPE specification.

Then separately identify:

### A. Missing Principles
Anything that should be ratified now but is absent.

### B. Schema Conflicts
Anything here that duplicates or conflicts with the existing registry/F1/F2 schema.

### C. F1–F5 Reconciliation
Map these recommendations against the existing findings and identify which findings can now be considered confirmed, mitigated, superseded, or still open.

### D. ADR Impact
Identify which existing ADRs require amendment and whether a new ADR should govern temporal/camera/scene correlation.

### E. SOP Impact
Identify exact additions required to SOP-04 or other existing SOPs, especially Camera Clock Sync.

### F. Implementation Boundary
Separate:
- documentation/spec changes;
- registry/schema changes;
- engine changes;
- FCPXML generator changes;
- current AlphaRoundUp Part 2 manual actions;
- Part 3 deployment changes.

### G. Outstanding Evidence
List any questions that should **not** be ratified yet because production evidence remains insufficient.

### H. Final Ratification Set
Return clean, specification-quality language for the principles you believe should become permanent W.E. C.A.P.E. architecture.

Do not silently assume that earlier CAPE implementation details are correct. Where current production evidence contradicts an earlier design assumption, favor the evidence and explicitly identify the superseded assumption.