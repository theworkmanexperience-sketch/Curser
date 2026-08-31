# ED-003 — PICTURE LOCK DESIGNATION

## `` I S S U E D ``

**Class:** Executive Determination
**Issued by:** Executive Producer / Chairman · **Date of issuance:** 2026-08-31
**Authorized for execution under:** EXECUTIVE ORDER `EO-WET-EXEC-019` — *Authorization for Issuance and Repository Custody of ED-003*
**Drafted under:** EXECUTIVE DIRECTION — *ED-003 Draft Authorization*, 2026-08-31 · **Drafting channel:** Governance Compliance Auditor, `Authority: NONE`
**Custody:** `MACHINE` · **Authority:** **EXECUTIVE**

> **This determination is issued and in force.**
>
> **Picture Lock designation is effected by this instrument and by no other.** `EO-WET-EXEC-019` authorized its issuance and custody; **it does not contain the designation, which resides exclusively here at §2.1.**
>
> **The drafting channel holds `Authority: NONE` and did not designate a Picture Lock.** That act is the Executive Producer / Chairman's and is exercised by the issuance of this determination.

---

# 1 · THE DESIGNATED ARTIFACT

| | |
|---|---|
| **SHA-256** | `d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80` |
| **Path** | `WE_CAPE_OUTPUT/AlphaRoundUp_2026/Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2 ANALYSIS/Corrected Video Analysis Files/Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` |
| **Bytes** | 7,264,164 |
| **Sequence duration** | `225096000/48000s` = **4689.500 s** · `tcFormat` `NDF` · `format` `r1` · `tcStart` `0s` |
| **Internal project name** | `Alpha RoudUp Part 2` |
| **Lineage** | 08-24 |

**Two properties of the artifact are recorded rather than normalized**, per `PLR-001` §1.1:

- **The container is a `.fcpxmld` bundle**, not a flat `.fcpxml`. The FCPXML is `Info.fcpxml` inside it.
- **The project name is misspelled `Alpha RoudUp`** — missing the `n` — **in the FCPXML's own `<project name>` attribute.** This is a property of the edit, not a filesystem accident. **A future search on the correct spelling will not find this file.**

**Accompanying artifacts in the same directory, recorded for identification and not designated by this determination:**

```
Alpha RoudUp Part 2.mov                         ff34278fe1f47f67…
Alpha RoudUp Part 2_SRT_English (US).srt        d93d86a1b7cd99c9…
```

---

# 2 · EXECUTIVE DETERMINATIONS

**Four, and no others.**

## 2.1 · Designation

**The FCPXML identified at §1, SHA-256 `d82c2c3ec0f788cf…`, is designated the governed Picture Lock for the 08-24 lineage.**

## 2.2 · Freeze

**The designated editorial timeline is frozen as the engineering baseline for all subsequent governance determinations.** Its sequence duration of **4689.500 s** is the governing editorial lock for the 08-24 lineage.

## 2.3 · New governed editorial lineage

**This designation establishes the beginning of a new governed editorial lineage.** The 08-24 lineage originates here.

## 2.4 · What this determination does not do

**Stated as determinations, not as commentary.**

| | |
|---|---|
| Determine `CF-001` | **NO** — the citation provenance conflict remains `UNRESOLVED — REQUIRES EXECUTIVE DETERMINATION` |
| Determine `ED-004` | **NO** — the caption collapse rule remains undeclared |
| Designate the Master Picture (`ED-005`) | **NO** — §4 |
| Authorize implementation | **NO** |
| Release `ED-006` | **NO** — the `RUN_ID` lock state remains a documented contradiction |
| Alter caption authority | **NO** — no caption stream is designated, and none is disturbed |
| Perform the `SOP-06` export | **NO** — Qualifier 2 |

---

# 3 · ENGINEERING QUALIFIERS

> **These are accepted engineering facts accompanying the Executive designation. They are not Executive determinations, and they are permanent parts of this instrument.**

## Qualifier 1 — Editorial gaps

**The designated timeline contains five editorial gaps at spine depth 0.**

**Verified against the designated artifact, not carried from its predecessor:** `[E]`

```
d82c2c3e   designated       depth-0 children 225   gaps 5
1ab3d12f   PLR-001 candidate depth-0 children 225   gaps 5
2bf06853   08-22 assembly    depth-0 children 214   gaps 3
```

**The designated timeline carries two more depth-0 gaps than the superseded 08-22 assembly.** A gap in a spine is a span with no primary picture.

**By issuing this determination the Executive acknowledges this editorial reality without assigning engineering interpretation beyond the measured evidence.** **No engineering conclusion is drawn as to whether five gaps is consistent with a locked picture; that judgement is editorial and is not made here.** `[O]`

## Qualifier 2 — `SOP-06` export

**Picture Lock designation and `SOP-06` conformant export are separate governance acts.**

**Issuing this determination does not create the conformant Picture Lock export.** The designated artifact is a project bundle in an analysis folder; it is not named `P2_LOCK_<date>.fcpxml` and it does not reside in `XML/`. `[E]`

**Execution of `SOP-06` Step A1 remains a separate, future, Executive-authorized activity, and will necessarily produce a new exported artifact with a different SHA-256 from the one designated here.**

## Qualifier 3 — New lineage

**Designation of this Picture Lock establishes the beginning of a new governed editorial lineage. Accordingly:**

- **No existing governed artifact inherits authority from this designation.**
- **All downstream governed artifacts shall be regenerated from the newly designated Picture Lock.**
- **No prior generated artifact shall be treated as an authoritative descendant of this lineage.**

**The measured basis:** `PLR-001` §4 records that **every governed artifact in the repository traces to the 08-22 assembly, not to this lineage** — *"Eight references, and every one describes the candidate rather than deriving from it. No registry entry, no timecode-bound artifact, no governed output has this file as its upstream."* `[E]`

**This lineage therefore begins with zero governed descendants, and that is a starting condition rather than a defect.**

---

# 4 · RELATIONSHIP TO `ED-005`

**This determination satisfies the Picture Lock prerequisite for `ED-005` — Master Picture Designation. It does not unblock `ED-005`.**

`EDR-001` records `ED-005` as **`NOT READY`**, because *"conformance inverts on `ED-003`, and a required comparison has never been performed."* `[E]`

**`ED-005` continues to require its own evidence, including the comparison between the designated Picture Lock and the candidate viewing master, which has not been performed.** **One prerequisite is removed. The determination is not completed.**

**And one consequence recorded in advance rather than discovered later:** `CAM-002` §3.2 holds that the 08-22 assembly and the 08-24 lineage are **the same production**, so a subsequent 08-24 master designation **supersedes the current viewing master**. **`ED-005` will therefore be a designation and a supersession, and should issue as one instrument.** `[E]`

---

# 5 · PRESERVATION OF THE GOVERNANCE BOUNDARY

**Engineering evidence identifies and evaluates candidate timelines. Executive authority alone establishes Picture Lock.**

**Nothing within `CF-001B` shall be interpreted as granting canonical status to the corrected analysis lineage.** `CF-001B` certifies **engineering fidelity** — that the corrected FCPXML is a complete and reliable representation of its own analysis project, and that its SRT export is faithful though lossy. **It confers no governing standing on that lineage, and the Chairman's Acceptance Memorandum accompanying it says so in terms.** `[E]`

**Authority arrives with this determination and from no other source.**

---

# 6 · EVIDENTIARY BASIS

| instrument | contribution | custody |
|---|---|---|
| `PLR-001_PICTURE_LOCK_REVIEW.md` | candidate identification · the `.fcpxmld` and spelling anomalies · gap count · `SOP-06` A1 separateness · zero downstream derivation | committed `2b7f055` |
| `CF-001B_CORRECTED_ANALYSIS_ARTIFACT_REVIEW.md` | engineering characterisation of the designated artifact — 4689.500 s, structure preserved, +4 nested asset-clips, 1 rewritten lower third | committed `d4f6135` |
| `CUSTODY_ALERT_001` Amendment 1 | `08_22_assembly_lock_status: SUPERSEDED_ASSEMBLY`, ratified 2026-08-28 — the 08-22 assembly cannot be the 08-24 lock | committed |
| `EDR-001` §6 | `ED-003` `READY WITH CONDITIONS`; the conditions are Executive facts, not engineering deficiencies | committed `2b7f055` |
| Live measurement, 2026-08-31 | full SHA-256; depth-0 gap verification on the designated artifact | this determination |

**One point of candour about the candidate set.** `PLR-001`'s exclusivity finding — that the candidate was the only complete, non-superseded Day 2 timeline — **was measured at repository `1552e42`, before the corrected artifacts existed.** Re-measured on 2026-08-31 there are **two** such timelines: `1ab3d12f` and `d82c2c3e`, identical in duration and depth-0 structure, differing by four nested asset-clips and one lower-third text. `[E]`

**The candidate set contained two qualifying timelines at the time of determination. This determination designates `d82c2c3e` as the governed Picture Lock after consideration of those qualifying candidates. The alternative is recorded so that the designation is visible as a deliberate Executive choice rather than as the absence of one.**

---

# 7 · STATUS

```
ED-003 — PICTURE LOCK DESIGNATION                    I S S U E D

Issued                     2026-08-31   ·   Executive Producer / Chairman
Authorized under           EO-WET-EXEC-019
Designated artifact        d82c2c3ec0f788cf…      4689.500 s
Lineage                    08-24 — begins here
Executive determinations   4
Engineering qualifiers     3   ·   permanent, not determinations

Designation in force       YES
CF-001                     UNRESOLVED
ED-004                     undeclared
ED-005                     prerequisite satisfied, determination NOT complete
ED-006                     unchanged
SOP-06 export              NOT performed
Implementation             NOT AUTHORIZED
Caption authority          UNCHANGED
```

---

*Issued by the Executive Producer / Chairman on 2026-08-31, authorized for execution and custody under EXECUTIVE ORDER `EO-WET-EXEC-019`. Drafted by the Governance Compliance Auditor under EXECUTIVE DIRECTION — ED-003 Draft Authorization; the drafting channel held `Authority: NONE` and designated nothing. Custody: `MACHINE`. **Authority: EXECUTIVE.***

***The Picture Lock designation is effected by this determination at §2.1 and resides nowhere else.** No caption stream was designated, no `SOP-06` export performed, no implementation authorized, no generated artifact modified, and no determination other than the four at §2 was made.*
