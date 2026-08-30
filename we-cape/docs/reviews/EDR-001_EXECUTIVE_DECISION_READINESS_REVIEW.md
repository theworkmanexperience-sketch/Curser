# EDR-001 — EXECUTIVE DECISION READINESS REVIEW

**Issued under:** EXECUTIVE REVIEW ORDER EDR-001, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. No registry, runtime component, intelligence artifact or presentation artifact was modified. No commit was made. **No Executive Determination is made, inferred, substituted or defaulted.**
**Measured at:** repository HEAD `1552e42` · `WE_CAPE_OUTPUT` volume, live

---

# 0 · READINESS AT A GLANCE

| # | determination | status | the binding constraint |
|---|---|---|---|
| **ED-002** | Token Normalization Standard | **NOT READY** | **No governing artifact defines any of the eight required elements. Zero.** |
| **ED-003** | Picture Lock Designation | **READY WITH CONDITIONS** | Three facts only the Executive holds |
| **ED-004** | Caption Collapse Rule | **READY WITH CONDITIONS** | Four conditions; one of them is ED-002 |
| **ED-005** | Master Picture Designation | **NOT READY** | **Conformance inverts on ED-003, and a required comparison has never been performed** |
| **ED-006** | Generator Lock Release | **NOT READY** | 1 of 8 prerequisites satisfied |

**And the finding that matters most for sequencing: the generator lock's actual release condition is two items, not eight — and both reduce to a single unanswered question.** §6.3.

---

# 1 · METHOD

Each determination was assessed by searching the repository for the evidence it requires, not by carrying forward a prior review's conclusion. **Where a prior review is cited, its claim was re-measured.** One such re-measurement produced `ERRATUM 1` to CIA-001 and is reflected here.

**No determination receives READY unless the required evidence exists in the repository.** Absence is recorded as absence.

**Missing evidence and unresolved policy are held apart throughout.** They have different remedies: missing evidence is engineering work; unresolved policy is an Executive act. Conflating them is how a checklist starts passing rows it should not.

---

# 2 · ED-002 · TOKEN NORMALIZATION STANDARD

## 2.1 · Required evidence, searched element by element

| required element | governing artifact found |
|---|---|
| Unicode normalization (`NFC` / `NFKC` / `NFD`) | **NONE — 0 files** |
| Case handling (`casefold`, `lowercase` as a rule) | **NONE — 0 files** |
| Whitespace normalization | **NONE — 0 files** |
| Punctuation handling | **NONE** |
| Hyphenation | **NONE** |
| Numeral handling | **NONE** |
| Speaker attribution / speaker labels | **NONE — 0 files** |
| Token boundary rules | **NONE — 0 files** |

**Eight required elements. Zero governing artifacts.** `[E]`

## 2.2 · The three near-hits, examined and excluded

| hit | why it is not a specification |
|---|---|
| `WET-SPEC-DIE-001_v0.2.md` line 49 — *"**no normalization**, no inference at extraction"* | **This is a prohibition, not a standard.** It forbids normalizing at extraction. It defines nothing about how tokens are formed, and it arguably points the other way — the 91 citations were extracted from **raw** text |
| `DAY2_PARENT_FORENSIC_AUDIT.md` line 207 — *"normalised (lowercase, punctuation stripped, adjacent duplicate cues collapsed), matched as word…"* | **A method note inside one audit.** Class H — a record of how one measurement was taken, true of when written. **It governs nothing and was never issued as a standard** |
| `CAPE-BRIEF-20260813` line 392 — `- hyphen` | A bullet in an unrelated list |

**The closest thing to a tokenization rule in this repository is a parenthetical inside a forensic audit.** It is also, not coincidentally, the exact normalization under which CCR-001 measured its 0.12 % convergence — which means **the strongest evidence for the caption invariant rests on a normalization that no instrument governs.**

## 2.3 · Status

```
ED-002   NOT READY
```

**This is missing evidence, not unresolved policy.** No amount of Executive deliberation produces a tokenization standard from a repository that contains none — the specification has to be written first, and writing it is engineering work that is not authorized here.

**This corrects the row proposed in the Chairman's draft checklist**, which marked ED-002 `✅ Tokenization decisions defined`. **Verified: they are not defined.** CCR-001 and CIA-001 `R-3` both said so, and re-measurement confirms it.

---

# 3 · ED-003 · PICTURE LOCK DESIGNATION

## 3.1 · Evidence

| criterion | finding | grade |
|---|---|---|
| **Candidate identity** | `Alpha RoudUp Part 2.fcpxmld/Info.fcpxml` · `1ab3d12f…` · byte-identical to `SPRINT3A_WORK/analysis_cut/Info_analysiscut.fcpxml`. Path confirmed by the Chairman during PLR-001 | `[E]` |
| **Completeness** | One sequence, spine 201, connected 455, duration 4689.500 s. Every ETC input present except `declared_lock`, which **no FCPXML carries** | `[E]` |
| **Stability** | Parses cleanly; duration corroborated by the Parent audio (0.057 s) and the forensic audit (−157.068 s). **Five gaps against the prior lock's three** — flagged, not interpreted | `[E]` / `[O]` |
| **Exclusivity** | **Uncontested.** Every other FCPXML is a single-clip caption carrier, has no sequence, or is `SUPERSEDED_ASSEMBLY` | `[E]` |
| **Lineage** | **MISSING, not broken.** Eight references describe it; none derives from it. Designation starts a clean lineage | `[E]` |

## 3.2 · Remaining unknowns — all Executive, none engineering

**No unresolved engineering question remains.** The three open items are facts only the Executive holds:

1. **No later Day 2 cut exists.** `CUSTODY_ALERT_001` asked exactly this; the recorded answer is `Q1_later_cut_exists: "no"`. **Already answered, and the answer is in the record.**
2. **The five gaps are deliberate and the timing is final.** SOP-06's trigger is *"no further cuts, trims, or re-orders."* Only the editor knows.
3. **This file, or a fresh SOP-06 A1 export.** A1 directs a fresh export named `P2_LOCK_<date>.fcpxml` into `XML/`. **That would be a different artifact with a different hash**, and the ETC would bind to it instead.

**Item 3 is the one that changes downstream work**, because every hash-pinned artifact binds to whichever file is designated.

## 3.3 · Status

```
ED-003   READY WITH CONDITIONS
```

Conditions: items 2 and 3 above. Item 1 is already satisfied by the record.

**This narrows the Chairman's draft row.** `✅ PLR-001 complete` describes the *review*, not the *determination*. PLR-001 recommended **subject to three facts it could not establish** — one of which is now shown to be already answered, leaving two.

---

# 4 · ED-004 · CAPTION COLLAPSE RULE

## 4.1 · Confirmations required by the Order

| required confirmation | verified |
|---|---|
| CCR-001 identified the invariant | **YES** — the merge normal form; forced by the Executive's own declared asymmetry (merge deterministic, split not) and supported at **0.12 %** convergence |
| CIA-001 confirmed the declared scope | **YES** — `INGESTION_MANIFEST` declares `DOUBLED_CUES` on `assembly_captions` = PARENT `80a8ed25…` |
| Zero governed citation impact under current scope | **YES** — the 91 citations target GT-2 `89d61f96…`; **0 of 91 change** |
| CIA-001 conditions fully identified | **YES** — four, all carried below |

## 4.2 · The four conditions, verified as still outstanding

| # | condition | state |
|---|---|---|
| **1** | **Scope the rule by stream hash `80a8ed25…`** | **OUTSTANDING.** GT-2's 41 duplicate runs are **13.6 % abutting and include a run of 3** — genuine repeated speech, not the defect. A rule scoped by defect *name* will eventually be read onto them |
| **2** | **Tokenization dependency** | **OUTSTANDING — and it is ED-002, which is NOT READY.** §2 |
| **3** | **Zero-length cue disposition** | **OUTSTANDING.** `NONPOSITIVE_DURATION_CUES` = 29 zero-length, 0 inverted. Collapse absorbs 16; **13 survive any rule and pass `G-09` invisibly** |
| **4** | **Context declaration dependency** | **OUTSTANDING.** `build_context.py` lines 121–125 stop when a declared `srt.cues` disagrees with measurement. The rule and the declaration must issue together |

## 4.3 · Status

```
ED-004   READY WITH CONDITIONS
```

**The declaration is low-risk and the conditions are not decorative.** Condition 2 is a hard dependency on a determination that is NOT READY — **ED-004 cannot be fully satisfied before ED-002 exists.** It can be *declared* with condition 2 recorded as open, but the rule is not reproducible until tokenization is specified.

**This narrows the Chairman's draft row.** `✅ CCR-001 + CIA-001 complete` swallows four conditions, one of which is blocked.

---

# 5 · ED-005 · MASTER PICTURE DESIGNATION

**This determination is not close, and the reason is structural rather than procedural.**

## 5.1 · What the register actually says about itself

`APPROVED_VIEWING_MASTER.yaml` raises the condition in its own header, unprompted:

> *"The render carrying `approval_status: APPROVED` below is 4846.625 s and is CONFORMANT to the 08-22 assembly — it is therefore **NO LONGER conformant to the governed production**… Until a conformant master of the 08-24 production is exported and designated, **this register names an approved viewing master for a superseded assembly.** Recorded here rather than corrected, per NO SILENT RECOVERY."*

**The register has already declared itself stale and declined to fix it silently.** That is the doctrine working.

## 5.2 · Conformance inverts on ED-003

The register defines conformance against `editorial_lock_duration_s`, currently `4846.625` — the **08-22** lock:

> *"CONFORMANT means equality to the millisecond. Anything else is NON_CONFORMANT and is ineligible for any judgement expressed in timecode — **it is not a lower-quality option, it is a different film.**"*

| render | runtime | conformant to 08-22 lock | conformant to the ED-003 candidate (4689.500) |
|---|---|---|---|
| `89e911b1…` — currently **APPROVED** | 4846.625 | **YES** | **NO** |
| `a94569ce…` — currently **REFERENCE_ONLY, hazard HIGH** | 4689.500 | NO (Δ 157.125 s) | **YES, to the millisecond** |

**The two verdicts swap the moment ED-003 is declared.** `[E]`

**ED-005 is therefore strictly downstream of ED-003 and cannot be assessed before it.** Assessing it now would evaluate the candidate against a lock the Executive is about to supersede.

## 5.3 · And duration equality is not sufficient — a required comparison has never been run

Both the register and the ingestion manifest state the same limit in almost the same words:

> `provenance_note`: *"Runtime matches the 2026-08-24 divergent-cut FCPXML to the millisecond. **Whether this render was produced from that FCPXML is NOT asserted — equality of duration is not identity of source, and no comparison of this file's picture against that timeline has been performed.**"*

**This is missing evidence, not unresolved policy.** A picture-against-timeline comparison is a measurement. It has never been performed, it is not authorized here, and **without it, lifting the quarantine would rest on a coincidence of duration** — which the register itself names as the hazard it exists to prevent.

## 5.4 · The hazard is live and specific

> *"the filename is **IDENTICAL** to the Approved Viewing Master's `Alpha RoudUp Part 2.m4v`. Not similar: identical. The two are distinguishable only by directory, size (11,803,856,181 vs 12,199,752,138 bytes), runtime and hash."*

Two 4K h264 files, same codec, same resolution, same frame rate, **same filename**, differing by 157.125 s of picture.

## 5.5 · Status

```
ED-005   NOT READY
```

**Two blockers, of different kinds.** ED-003 must be declared first, because conformance is computed against the lock. And **a picture-to-timeline comparison must be performed** — engineering work, currently unauthorized.

---

# 6 · ED-006 · GENERATOR LOCK RELEASE

## 6.1 · The eight prerequisites named in the Order

| # | prerequisite | state | evidence |
|---|---|---|---|
| 1 | **ETC extractor validated** | **SATISFIED** | Gate satisfied byte-for-byte, `e91318a6…`; committed `1552e42`; 7 of 7 checks pass |
| 2 | Picture Lock designated | **NOT SATISFIED** | ED-003 READY WITH CONDITIONS; no designation exists |
| 3 | Token Normalization declared | **NOT SATISFIED** | ED-002 NOT READY; zero governing artifacts |
| 4 | Caption Collapse Rule declared | **NOT SATISFIED** | ED-004 READY WITH CONDITIONS; not declared |
| 5 | Master Picture designated | **NOT SATISFIED** | ED-005 NOT READY; quarantine stands |
| 6 | **EPR-001 completed** | **NOT SATISFIED** | §6.2 — one open question |
| 7 | **EPR-001 ratified** | **NOT SATISFIED** | no ratification instrument exists |
| 8 | CC-001 chronology disposition declared | **NOT SATISFIED** | `UNRESOLVED — REQUIRES DECLARED DISPOSITION` |

**1 of 8 satisfied.**

## 6.2 · EPR-001 is one question from ratifiable

`EPR_EXECUTIVE_AUTHORING_WORKBOOK.md` states it directly:

> **"ONE thing stands between here and a ratifiable EPR-001:"**
> | **1** | **`EPR-07` disposition** — retire · migrate · survive · hold | Section 4 · Q10 |

Q7 and Q8 were answered 2026-08-29. **Every in-scope segment `S01`–`S18` now carries an intentional Executive disposition, and `V-5` coverage stands at `observed=19 expected=19`.**

What remains is `Q10` — what becomes of the `Ride_Home` beat, whose segment `S19` lies wholly beyond this production's runtime. Four options are on the page and none is checked. **`EPR-06` carries `terminal_beat_status: CONTINGENT_ON_EPR-07_DISPOSITION` and the platform has not classified it either way** — consistent with the refusal already on the record, where converting an inclination into a disposition was declined because *an inclination is not a ruling.*

## 6.3 · The governing instrument names two conditions, not eight

**This distinction is the most consequential thing in this review and it is recorded rather than resolved.**

```
INGESTION_MANIFEST.yaml
  gen_artifacts_py:       LOCKED
  run_id_lock_held_by:    "EXECUTIVE ORDER 2026-08-28 section 4"

release condition, as written in that Order:
  Executive Authoring Workbook complete  AND  EPR-001 formally ratified
```

**The Order that holds the lock names prerequisites 6 and 7. It does not name 1, 2, 3, 4, 5 or 8.**

The eight-item list in EDR-001 is broader than the instrument in force. **That is entirely the Chairman's prerogative — an Executive may hold a lock to a higher standard than the Order that set it.** But the two should not be confused, because they imply very different paths:

| | prerequisites | shortest path |
|---|---|---|
| **As the governing Order stands** | 6 and 7 | **Answer `Q10` → complete the Workbook → ratify EPR-001 → the lock releases** |
| **As EDR-001 lists them** | all 8 | ED-002 must first be *written*, ED-005 needs a comparison that has never been run |

**Under the Order in force, the generator lock is one question away.** Under the eight-item list it is a program.

**Which standard applies is an Executive determination and is not made here.**

## 6.4 · Status

```
ED-006   NOT READY
```

Under either standard. The difference is how far from ready.

---

# 7 · A CROSS-CUTTING FINDING — TWO SILENT-FAILURE SURFACES, NOT ONE

CIA-001 recorded `R-1`: a wrong cue index always resolves and never errors. **This review found a second instance of the identical pattern, and it is already live.**

`EPR_EXECUTIVE_AUTHORING_WORKBOOK.md` §4, on the `S19` reference:

> *"**`V-2` does not detect this.** It resolves `S19` against `TIMELINE_REGISTRY` v1.0.0 — **the superseded assembly's authority** — and passes. **The validator will keep reporting this entry as sound.**"*

| surface | mechanism | detection today |
|---|---|---|
| **`R-1`** cue index | a stale `#NNNN` resolves against the wrong stream and returns a confident wrong answer | **none** |
| **`V-2`** segment reference | a stale `S19` resolves against a **superseded registry version** and passes | **none** |

**Both are validators that succeed against the wrong authority.** Neither is caused by the determinations under review, and neither is fixed by them. **ECR-003 addresses the first. The second has no proposed control** and is recorded here so it is not lost.

---

# 8 · DEPENDENCY ORDER

Derived from the evidence above, not proposed as a plan.

```
ED-002  Token Normalization ─────────► ED-004 condition 2
        (blocked: must be WRITTEN — no artifact exists)

ED-003  Picture Lock ────────────────► ED-005  (conformance is computed
        (2 Executive facts)                     against the lock, and the
                                                verdicts INVERT)
                                     └─► picture-to-timeline comparison
                                         (unperformed measurement)

ED-004  Caption Collapse ────────────► depends on ED-002
        (4 conditions)

Q10 ──► Workbook complete ──► EPR-001 ratified ──► ED-006 under the Order in force
        (one unanswered question — independent of every determination above)

CC-001  chronology disposition ──────► independent; nothing blocks it but a ruling
```

**Q10 sits on no other determination's critical path, and no other determination sits on it.** It is the only item in this review that is both fully in the Executive's hands and unblocked by anything.

---

# 9 · WHAT THIS REVIEW DOES NOT ESTABLISH

- **Whether any determination should be made.** Not asked, not answered.
- **Whether the eight-item ED-006 standard or the two-item Order standard governs.** §6.3 — Executive.
- **Whether the five gaps in the ED-003 candidate are deliberate.** Editorial; unknowable from the repository.
- **Whether the quarantined render was produced from the candidate FCPXML.** The comparison has never been run (§5.3).
- **Whether the 91 citations are correct.** All were extracted 2026-08-20 and **have never been verified against their timecodes.** Unchanged by this review. `[O]`

---

# 10 · CERTIFICATION

```
ED-002  Token Normalization     NOT READY                 0 of 8 elements specified
ED-003  Picture Lock            READY WITH CONDITIONS     2 Executive facts outstanding
ED-004  Caption Collapse Rule   READY WITH CONDITIONS     4 conditions, 1 blocked on ED-002
ED-005  Master Picture          NOT READY                 downstream of ED-003 +
                                                          an unperformed comparison
ED-006  Generator Lock          NOT READY                 1 of 8 · or 0 of 2 under the
                                                          Order actually in force

Draft checklist rows corrected   3   ED-002 ✅→NOT READY · ED-003 and ED-004 ✅→WITH CONDITIONS
Rows added                       2   EPR-001 completion/ratification · CC-001 disposition
Silent-failure surfaces found    2   R-1 cue index · V-2 superseded segment authority

Determinations made              NONE
Engineering authorized           NONE
Registries modified              NONE
Commits                          NONE
```

---

*Prepared under EDR-001. Custody: MACHINE. Authority: NONE. No registry, runtime component, intelligence artifact, presentation artifact or source file was modified. No commit was made. No Picture Lock, Caption Collapse Rule, Master Picture or Generator Lock release was declared, and none is implied.*
