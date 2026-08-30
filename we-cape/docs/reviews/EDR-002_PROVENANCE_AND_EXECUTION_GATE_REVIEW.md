# EDR-002 — PROVENANCE RESOLUTION & EXECUTION GATE ARCHITECTURE

**Issued under:** EXECUTIVE REVIEW ORDER EDR-002, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. No registry, caption stream, runtime component or generator was modified. No commit was made. **CF-001 is not resolved and no authoritative stream is chosen.**
**Measured at:** repository HEAD `1552e42` · `WE_CAPE_OUTPUT` volume, live
**Companion:** `EXECUTION_GATE_ARCHITECTURE_ASSESSMENT.md` — Objectives 2 and 3 in full

---

# 0 · SUMMARY

| objective | conclusion |
|---|---|
| **1** Classify CF-001 | **PROVENANCE DEFECT that meets the threshold of a REPOSITORY INTEGRITY EVENT** — the actual source has no identity in the repository at all |
| **2** Gate A / Gate B | **MODEL VALIDATED. RUNTIME CANNOT EXPRESS IT.** Gate A has no representable state today |
| **3** Namespace separation | **REQUIRED.** Experimental artifacts would be indistinguishable from governed ones in three specific places |
| **4** ECR-003 dependency graph | **CONFIRMED, with one revision** — `G-3` and `G-4` are not downstream of CF-001. **ED-004 correctly stays outside the chain** |
| **5** Provenance as a class | **EVIDENCE SUPPORTS THE DISTINCTION** — four instances, none caught by any instrument |

---

# 1 · OBJECTIVE 1 — CLASSIFYING CF-001

## 1.1 · The measurement that settles the class

```
89d61f96…   GT-2, the DECLARED source          appears  70 times across the repository
c13df1f4…   the MEASURED source                appears   0 times
```

`89d61f96` is bound into `CAPTION_REGISTRY.yaml` · `VOICE_PRIORITY_MAP.yaml` · `BEHAVIORAL_FINGERPRINT.yaml` · `AR2-0822.context.json` · `AR2-0822.observations.json` · `CONDUCTOR_SCORE.yaml` · `VISUAL_EVENT_REGISTRY.yaml` · `EDITORIAL_SYNCHRONIZATION.yaml` · `EXECUTION_LOG.md`, and stands as **input #3 of RE-001's four authoritative production artifacts.**

**`c13df1f4` is named nowhere. Not hashed, not registered, not declared, not mentioned.** `[E]`

## 1.2 · What that means, stated precisely

**The repository contains two governed populations resting on two different caption streams.**

| population | stream | status |
|---|---|---|
| **Generated intelligence** — Conductor Score, Visual Event Registry, Editorial Synchronization, Voice Priority Map, Behavioral Fingerprint, Caption Registry | **GT-2 `89d61f96`** | hash-bound in every artifact header; the four-source chain is closed in both directions |
| **Knowledge registries** — the 91 citations in Rider, Motorcycle, Organization, Prompt | **`c13df1f4`** | **the file has no custody record of any kind** |

**The four-source chain is sound.** RE-001's closure — the ETC's `source_sha256` equalling input #2 — remains true, and this review found nothing wrong with it. **The knowledge registries simply sit outside it.**

## 1.3 · Classification, against the Order's four candidates

| candidate | assessment |
|---|---|
| **Specification gap** | **PARTIAL and secondary.** No instrument requires a registry to bind its stream by hash. Real, but it describes the *absence of a control*, not the *condition* |
| **Engineering defect** | **NO.** No code behaved incorrectly. Nothing parsed wrongly, nothing computed wrongly, no guard failed to do what it was written to do. **There is no code to fix** |
| **Provenance defect** | **YES — this is the primary class.** The declared origin of 91 governed citations is not their actual origin |
| **Repository integrity event** | **THRESHOLD MET, and by one specific property** — §1.4 |

## 1.4 · Why it crosses into an integrity event

A mislabelled artifact whose true source is registered elsewhere is a provenance defect and is correctable by pointing at the right record.

**Here there is no right record to point at.** `c13df1f4` has never been hashed into any governed instrument. **The repository cannot currently produce the identity of a file that ninety-one governed citations depend on** — it can only produce the identity of a file they do not use.

**That is the property that distinguishes this from a labelling error.** It is not that the record is wrong; it is that for this dependency, **there is no record.**

## 1.5 · What is NOT compromised, and this matters

**The facts are probably sound.** The names, affiliations and quotes are internally consistent with `c13df1f4` — four of four tested name-matches confirm it. **The extraction appears correct; only its declared origin is wrong.**

**No generated artifact is implicated.** Every artifact carrying a RUN_ID header binds GT-2 by hash and was produced against it. **The two populations did not cross.**

**And the repository behaved well in one respect worth recording:** the compound `#N MM:SS` citation form — which nothing required — is the only reason this was detectable at all. **Without the second field, CF-001 would have been unfindable.**

## 1.6 · Recorded classification

```
CF-001   PROVENANCE DEFECT
         meeting the threshold of a REPOSITORY INTEGRITY EVENT
         by reason of the actual source having no custody record

         NOT an engineering defect — no code behaved incorrectly
         NOT primarily a specification gap — though one enabled it
         Content integrity  NOT SHOWN TO BE COMPROMISED
         Generated artifacts NOT IMPLICATED
```

**Which stream is authoritative is not determined here and must not be inferred from this classification.**

---

# 2 · OBJECTIVES 2 & 3 — SUMMARY

Full assessment in the companion document. The conclusions:

**The Gate A / Gate B model is architecturally correct.** It is the platform's own custody-versus-authority doctrine applied to execution: running a generator is a `MACHINE` act; making its output governed is an `EXECUTIVE` one. **The model resolves the ED-006 contradiction rather than choosing a side.**

**The runtime cannot currently express Gate A.** A Gate-A run today either declares `regeneration_scope.mode: CANONICAL_EDITORIAL_TIMELINE` — in which case `G-12` passes and **the output is indistinguishable from a governed artifact** — or declares anything else, in which case **`G-12` stops the run and Gate A produces nothing.** There is no third state.

**Namespace separation is required, and the distinction breaks in three specific places:** no machine-readable status field on any artifact; a caller-supplied output directory with nothing pinning it away from the governed tree; and a single admissible regeneration mode. **Detail, evidence and the minimum changes are in the companion assessment.**

---

# 3 · OBJECTIVE 4 — THE ECR-003 DEPENDENCY GRAPH

## 3.1 · The proposed sequence — CONFIRMED

```
CF-001
    ↓
Executive Provenance Disposition
    ↓
G-2 Stream Binding
    ↓
G-1 Tolerance
    ↓
ECR-003 Specification Completion
    ↓
ECR-003 Implementation
```

**Confirmed by evidence at each link:**

| link | evidence |
|---|---|
| CF-001 → disposition | The correct stream is an Executive determination. `EPR-001 §2.3` and NO SILENT RECOVERY both forbid the platform choosing |
| disposition → `G-2` | `G-2` asks which stream each registry cites. **The one existing declaration is wrong and the alternative is unregistered** — the answer does not exist until it is declared |
| `G-2` → `G-1` | **Measured: against `c13df1f4` the offsets have IQR 1.021 s and a tolerance is specifiable. Against GT-2 they span 50 s and no tolerance is meaningful.** The tolerance is a function of the stream |
| spec → implementation | Chairman's own sequencing, and CF-001 is the evidence for it: implementing first would have returned `FAILED` on ~77 of 82 and been read as a citation defect |

## 3.2 · One revision — two gaps are not downstream

**`G-3` (fail-closed semantics) and `G-4` (citation grammar) have no dependency on CF-001 and can be specified today.**

`G-3` asks what a `FAILED` verdict does — halt or report. `G-4` asks how the four citation shapes are parsed. **Neither answer changes with the stream.** Holding them behind CF-001 would idle work that is ready.

```
CF-001 ──► Executive Disposition ──► G-2 ──► G-1 ──┐
                                                    ├──► ECR-003 Spec ──► Implementation
G-3  fail-closed semantics  ───────────────────────┤
G-4  citation grammar       ───────────────────────┘
     (specifiable now — no CF-001 dependency)
```

**`G-4` in particular should not wait**, because it is the gap that could make the control reproduce the failure it exists to detect: a parser written for the compound form alone would report *82 of 82 validated* and never mention the nine.

## 3.3 · Should ED-004 remain outside the chain? — CONFIRMED

**Yes, on measured evidence.**

```
ED-004 collapse rule targets   PARENT       80a8ed25   5,664 cues   2,612 dup runs   98.7% abutting
the 91 citations target        Part 2 SRT   c13df1f4   2,290 cues      39 dup runs   12.2% abutting
the registries declare         GT-2         89d61f96   2,291 cues      41 dup runs   13.6% abutting
```

**Three distinct streams. Only one carries the defect, and the citations are not on it under either candidate provenance.** ED-004's zero-impact conclusion holds whether CF-001 resolves to GT-2 or to `c13df1f4`.

**Stated with its own limit:** this holds for every disposition the evidence supports. It would not hold if the Executive declared PARENT the citation authority — which no evidence supports (91 citations max out at index 2,284 against 5,664 cues, at a median offset of −693 s). **The conclusion is robust, not unconditional.**

**ED-004 therefore remains outside the ECR-003 chain and is not blocked by CF-001.** Its own four conditions still stand, and condition 2 — tokenization — is still blocked on ED-002.

---

# 4 · OBJECTIVE 5 — PROVENANCE AS A DISTINCT CLASS

**The Order asks only whether repository evidence supports the distinction. It does. No standard is created and no instrument is renamed.**

## 4.1 · The evidence — four instances, one shape

| # | instance | declared | actual | detected by |
|---|---|---|---|---|
| 1 | **`191/191`** | a measurement | **a hard-coded string; no committed code ever produced it** | a human reading `git log` |
| 2 | **The ETC producer** | a first-class governed artifact class with four consumers | **no producer in version control** | a human asking where the file came from |
| 3 | **`CF-001`** | citations sourced from GT-2 | **`c13df1f4`, unregistered** | a human measuring a tolerance for a different purpose |
| 4 | **`V-2` / `S19`** | a validated segment reference | **resolved against a superseded registry version, and passing** | the workbook's own author, in prose |

**Zero of four were detected by an instrument. Four of four were found by a person asking a question.** `[E]`

## 4.2 · Why the distinction is real and not merely descriptive

**An implementation failure is caught by testing the code. A provenance failure is not — because the code is correct.**

In all four instances every component behaved exactly as written. The parser parsed, the index resolved, the validator validated, the report reported. **There was no bug to find.** What was wrong was the relationship between an artifact and its declared origin — a property no unit test expresses, because it is not a property of any single component.

**They also differ in remedy.** An implementation defect is fixed by an engineer. **A provenance defect cannot be fixed by an engineer**, because determining which of two conflicting records is true is a custody question. Every one of the four terminated in a human decision, and CF-001 has terminated in one again.

**And they differ in detection cost.** An implementation defect surfaces at the next run. **A provenance defect can persist indefinitely** — `191/191` stood for three months; CF-001 stood for ten days across four reviews that each looked directly at the citations without seeing it, including two of mine.

## 4.3 · Conclusion

```
Does repository evidence support distinguishing provenance failures
from implementation failures?

YES — on four instances, a shared failure shape, a shared detection
      profile of zero, and a categorically different remedy.
```

**Whether to create a class, and what to call it, is not determined here.** The Order forbids it and the observation stands without it.

**One property worth carrying into whatever instrument eventually addresses this:** every instance was found because *some* second signal existed — a git history, a consumer with no producer, a timecode beside an index, an author's own prose. **The four detections were luck riding on redundancy.** A control that survives this class is one that requires the second signal rather than hoping for it.

---

# 5 · WHAT THIS REVIEW DOES NOT ESTABLISH

- **Which caption stream is authoritative.** Prohibited, and not inferable from anything here.
- **Whether the 9 timecode-less citations share `c13df1f4`'s provenance.** **Untestable by any available method.** They may be correct, may not, and nothing in the repository can say.
- **Whether any downstream consumer ever resolved a citation against the wrong stream.** Not measured. §1.2 shows the two populations did not cross *in generated artifacts*; human reading is not measurable.
- **Whether Gate A / Gate B should be adopted.** The model is validated as sound; adoption is an Executive act.
- **The correctness of the 91 citations' content.** Four were verified by name match. **Seventy-eight compound citations remain unverified**, and that is what ECR-003 exists to do.

---

# 6 · CERTIFICATION

```
CF-001 classification       PROVENANCE DEFECT · integrity-event threshold met
                            declared stream appears 70×  ·  actual stream appears 0×
Engineering defect          NO — no code behaved incorrectly
Content compromised         NOT SHOWN — extraction consistent with the measured stream
Generated artifacts         NOT IMPLICATED — all bind GT-2 by hash

Gate A / Gate B model       VALIDATED as architecture
Gate A runtime expression   ABSENT — no representable state exists
Namespace separation        REQUIRED — 3 break points, companion document

Dependency graph            CONFIRMED with one revision
                            G-3 and G-4 are NOT downstream of CF-001
ED-004 outside the chain    CONFIRMED on measured evidence, with its limit stated

Provenance as a class       EVIDENCE SUPPORTS THE DISTINCTION
                            4 instances · 0 detected by an instrument

CF-001 resolved             NO
Authoritative stream chosen NO
Determinations made         NONE
Standards created           NONE
Commits                     NONE
```

---

*Prepared under EDR-002. Custody: MACHINE. Authority: NONE. No registry, caption stream, runtime component, generator or source file was modified. No commit was made. CF-001 remains unresolved, no authoritative caption stream is chosen, no gate is implemented, and no governance standard is created.*
