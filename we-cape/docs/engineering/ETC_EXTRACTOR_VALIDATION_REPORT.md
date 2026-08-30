# ETC EXTRACTOR — IMPLEMENTATION & VALIDATION REPORT

**Issued under:** EXECUTIVE AUTHORIZATION ED-001A, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE
**Deliverable:** `intelligence/p2/ess/scripts/etc_extract.py`

> # ACCEPTANCE GATE — SATISFIED
> **The extractor regenerates the surviving 08-22 Editorial Timing Contract byte-for-byte.**
>
> ```
> regenerated   e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d
> reference     e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d
> bytes         183,116 == 183,116
> ```
>
> Per ED-001A §6, **this authorization is now concluded.** No further engineering authority is implied and none is assumed.

---

# 1 · THE GAP THIS CLOSES

**The missing ETC producer was not feature creep. It was an architectural gap that broke an existing contract.**

*(That formulation is the Chairman's, recorded here as his. It does not appear in my Phase 1 record — my wording there was narrower, and the sentence quoted back to me was not mine. I am not accepting authorship of it. It states the boundary better than my version did, and it carries more weight as an Executive formulation than it would as an engineering one.)*

Before this work:

```
P2_LOCK_timing.json      first-class governed artifact class (PDR-2026-08-20-ETC-001)
committed consumers      fcpx_resolve.py · build_context.py · gen_artifacts.py · gen_artifacts_v2.py
committed producer       NONE — no file, no git history, no writer anywhere in the repository
documents citing it      10
```

After: the producer exists, is committed, is deterministic, and has been proved against the only reference that could prove it.

---

# 2 · WHAT THE CONTRACT ACTUALLY IS

Derived from the surviving artifact, not from documentation. Four structural rules were recovered, each confirmed by exact census match.

| rule | evidence |
|---|---|
| **`spine`** = depth-0 children of the first `<spine>`, **excluding `transition`** | Raw spine has 214 children: 180 asset-clip · 23 transition · 8 clip · 3 gap. The contract's spine is **191 = 180 + 8 + 3**. Transitions are structurally present and contractually absent |
| **Nested `<spine>` subtrees are not traversed at all** | Descending them yields 545 connected elements. Not descending them yields **exactly 404**, with every per-tag and per-depth count matching. Secondary-storyline contents are outside the contract |
| **Only timeline-bearing tags are emitted** — `asset-clip`, `clip`, `gap`, `title`, `audio`, `video` | Decoration (`conform-rate`, `timeMap`, `adjust-*`, `keyword`, `filter-*`, `marker`, `param`, `data`, `audio-channel-source`) is neither emitted nor descended |
| **Depth-0 carries `timeline_offset_s`; depth ≥ 1 carries `rel_offset_s`** | Mutually exclusive in every one of the 595 rows |

**The transition exclusion is the same fact that produced the B-1 defect.** `fcpx_resolve.py` originally compared the ETC's 191 spine entries against 214 raw depth-0 children positionally and scored `1/191`. The contract had always excluded transitions; the resolver had not. **The producer now makes that rule explicit in the code that creates the artifact, rather than leaving it as a convention the consumer had to guess.**

## 2.1 · Census reconciliation against the governing PDR

| | PDR-2026-08-20-ETC-001 declares | regenerated |
|---|---|---|
| spine | 191 — asset-clips 180 · clips 8 · gaps 3 | **191 — 180 · 8 · 3** |
| connected | 404 — asset-clips 247 · video 18 · audio 30 · titles 40 · clips 39 · gaps 30 | **404 — 247 · 18 · 30 · 40 · 39 · 30** |
| sequence duration | 4846.625 s | **4846.625 s** |
| source sha256 | `2bf0685373…` | **`2bf0685373…`** |

**Every published figure reproduced from the FCPXML.** The PDR's numbers were correct and are now derivable rather than asserted.

---

# 3 · TWO SERIALISATION FACTS THAT ARE PART OF THE ARTIFACT

Byte equality forced these into the open. Both were undocumented anywhere.

| | |
|---|---|
| **A missing `name` serialises as `""`, a missing `lane` as `null`** | Five elements carry an empty-string name; zero carry a null name; 238 carry a null lane. Treating both alike costs 2 bytes per element |
| **The artifact has NO trailing newline** | It ends at its closing brace |

Together these were the entire 11-byte gap between a structurally perfect result and a passing gate — 5 × 2 bytes, plus 1.

**This is the argument for byte equality as the criterion.** A structural or field-level comparison would have passed a producer that emits a different artifact. The gate caught what a semantic test would have waved through, which is exactly why ED-001A §3 permits no alternative.

---

# 4 · VALIDATION

| # | check | result |
|---|---|---|
| **V1** | Determinism — three consecutive runs | **PASS** · 3 runs, 1 distinct hash |
| **V2** | The extractor never reads the artifact it must reproduce | **PASS** · no reference to `P2_LOCK_timing` anywhere in the source |
| **V3** | Source-identity guard fires on a wrong hash | **PASS** · `STOP FAILED_SOURCE_IDENTITY`, **exit 2, zero files written** |
| **V4** | Multi-sequence input stops | **PASS** · exit 1, zero files written |
| **V5** | `declared_lock` is never invented | **PASS** · `null` when not supplied |
| **V6** | Census matches the governing PDR | **PASS** · §2.1 |
| **V7** | Gate re-confirmed after every edit | **PASS** · `e91318a6…` |

**V2 is the check that matters most.** A producer that reads its own target would pass the gate and prove nothing. The extractor takes one input — the FCPXML — and the reference artifact is never opened.

## 4.1 · Fail-shut behaviour

Consistent with the platform's existing guard architecture: **every stop writes zero files.** A failed run leaves no partial artifact to be mistaken for a good one.

---

# 5 · DECLARED, NOT DERIVED

Two fields are parameters and the tool refuses to invent either.

| field | why |
|---|---|
| `sequence.declared_lock` | **`01:20:46:14` does not appear anywhere in the FCPXML** — verified by direct search. It is a human declaration, reconciled against the parsed duration by the PDR. Omitted, it is emitted as `null` |
| `source` | The path recorded in the contract. The 08-22 artifact records a `/Volumes/...` path that is not this session's mount point |

**The tool will not default a lock timecode.** An empty field remains empty.

---

# 6 · SCOPE — WHAT WAS AND WAS NOT DONE

Per ED-001A §4.

| authorized | done |
|---|---|
| Implement the ETC extractor | yes |
| Validate against the existing 08-22 artifact | yes — §4 |
| Document validation results | this report |
| Correct defects required to satisfy the gate | yes — two, §3 |

| excluded | observed |
|---|---|
| Enhancement of the ETC specification | **none.** The format is reproduced exactly, including both quirks in §3 |
| Changes to doctrine | none |
| Changes to governed artifact formats | none |
| New production features | none |
| Optimization unrelated to the gate | none |

## 6.1 · The extractor has not been pointed at anything else

Per ED-001A §3, and now per §6:

```
08-24 lineage        NOT PROCESSED
Alpha RoundUp Day 3  NOT PROCESSED
any new production   NOT PROCESSED
```

**It has been run against exactly one input: the 08-22 picture-locked FCPXML `2bf0685373…`.**

## 6.2 · Executive determinations — untouched

None of the five reserved determinations was inferred, substituted or defaulted: the 08-24 picture-lock designation, the caption collapse rule, the master picture designation, EPR-001 completion or ratification, and release of the generator lock. **The generator lock remains held.**

---

# 7 · ONE OBSERVATION, RECORDED NOT ACTED ON

**The 08-22 ETC was reproducible, which means the artifact governing three months of downstream work was in fact derivable from its declared source all along.** That is the good outcome — the artifact was true. It was simply unverifiable, because nothing that could check it existed.

**What remains unknown is whether the original producer worked this way.** This extractor reproduces the *output* byte-for-byte. It is not evidence about the *method* that first produced it, and no such claim is made. What the repository now has is a producer whose method is inspectable, which it did not have before.

---

# 8 · CERTIFICATION

```
Deliverable                  intelligence/p2/ess/scripts/etc_extract.py
Dependencies                 stdlib only · no network · read-only on input

ACCEPTANCE GATE              SATISFIED
  regenerated                e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d
  reference                  e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d
  bytes                      183,116 == 183,116
  alternative criteria used  NONE

Validation checks            7 of 7 PASS
Determinism                  3 runs, 1 hash
Fail-shut                    confirmed — every stop writes 0 files
Spec enhanced                NO
Doctrine changed             NO
Formats changed              NO
Lineages processed           1 — the 08-22 validation corpus only
Executive determinations     0 inferred, 0 substituted, 0 defaulted
Generator lock               STILL HELD

ED-001A authorization        CONCLUDED per section 6
```

---

*Prepared under ED-001A. Custody: MACHINE. Authority: NONE. No registry, generator, specification, doctrine, Executive Order, narrative declaration, production artifact, or source file was modified. The 08-22 Editorial Timing Contract on the output volume was read and not written.*
