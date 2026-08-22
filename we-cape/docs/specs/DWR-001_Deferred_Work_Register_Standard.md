# DWR-001 — Deferred Work Register Standard
Version: 1.0

> **Transcription note.** Filed into governed documentation on 2026-08-22 from the Executive
> Communiqué of the same date. See the numbering note at the end.

## Governance Status
Document Type: Standard · Status: ISSUED · Date: 2026-08-22 · Authority: Executive Office
Initiative: PHI-001

---

# Purpose
The Deferred Work Register (DWR) records ideas that have been intentionally postponed.

Deferred work is not backlog. Deferred work represents conscious Executive decisions.

# Required Fields
Every Deferred Work item shall record:

- DWR Identifier
- Title
- Category
- Origin
- Discussion Reference
- Date Identified
- Reason Deferred
- Executive Context
- Dependencies
- Trigger Event
- Estimated Value
- Estimated Complexity
- Recommended Priority
- Current Status

# Status Values
`Deferred` · `Under Review` · `Ready` · `In Progress` · `Completed` · `Archived` · `Rejected`

# Review Frequency
Deferred Work shall be reviewed during: Platform Hygiene Reviews · Executive Planning ·
Major Releases · CAR Reviews · Version Milestones.

# Principle
A good idea should never disappear because today's priorities are different. Deferred work preserves
institutional memory until the appropriate time for implementation.

# Relationship
| artifact | role |
|---|---|
| CAR | reviews deferred work |
| ADR | records architectural decisions |
| PDR | records production decisions |
| RE | records historical execution baselines |
| DWR | preserves intentionally postponed work |

---

## Executive enhancement adopted at first use (2026-08-22)
Every entry additionally carries a **`class`** field distinguishing:

- **Deferred Decision** — a question still requiring an Executive or Chairman ruling. Blocked on
  *authority*. May not be scheduled as engineering work.
- **Deferred Implementation** — a decision already made and intentionally postponed. Blocked on
  *capacity*. May be scheduled.

Operative rule: **a DECISION entry may never enter a sprint plan.**

## Numbering note raised by the first review (CAR-003)
This standard's document ID (`DWR-001`) occupies the same identifier space as the entries it defines
(`DWR-001`, `DWR-002`, …). CAR-003 recommends renaming the standard to **`WET-SPEC-DWR-001`**,
matching the named-series convention already used by `WET-SPEC-DIE-001` and `WET-SPEC-GATE-001`, which
frees `DWR-NNN` for entries. Recorded rather than silently resolved; the first register was issued
with entry IDs `DWR-001`…`DWR-036` pending this ruling.
