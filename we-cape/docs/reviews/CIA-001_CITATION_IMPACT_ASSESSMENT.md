# CIA-001 — CITATION IMPACT ASSESSMENT

**Issued under:** EXECUTIVE REVIEW ORDER CIA-001, Executive Producer / Chairman
**Custody:** `MACHINE` · **Authority:** NONE · **Implementation:** NONE
**Mode:** READ-ONLY. No registry, citation, cue, identifier, runtime component, intelligence artifact or presentation asset was modified. No commit was made.
**Measured at:** repository HEAD `1552e42` · `WE_CAPE_OUTPUT` volume, live

---

# 0 · THE FINDING THAT CHANGES THE QUESTION

**The 91 governed citations do not point at the stream the Caption Collapse Rule would govern.**

```
the 91 citations target      GT-2 canonical SRT        89d61f96…   2,291 cues
the collapse rule targets    PARENT assembly SRT       80a8ed25…   5,664 cues
```

These are different files, different lineages, different hashes, and — measured below — **different defect profiles.** `INGESTION_MANIFEST.yaml` declares `DOUBLED_CUES` on `assembly_captions`, which is the PARENT stream. **GT-2 does not carry that defect.**

**Declaring the Caption Collapse Rule as currently scoped changes zero of the 91 citations.**

The impact is not on what exists. It is on what the rule *unblocks*: an un-ingested assembly asset with no governed consumers today.

**This inverts the premise in the Order's Context section, and the rest of this assessment is written against the measurement rather than the premise.**

---

# 1 · CITATION CENSUS

> ### ERRATUM 2 — issued 2026-08-30 · **the *Current target* column below is WRONG**
>
> **Measured during `ECR-003A` tolerance work: the 91 citations do not resolve against GT-2 `89d61f96…`. They resolve against `Part 2 SRT` `c13df1f4…`.** Timing: median offset **+0.125 s** against `c13df1f4` versus **+16.479 s** against GT-2. Text: **4 of 4 tested name-matches confirm `c13df1f4`, 0 of 4 confirm GT-2.**
>
> **Read every *Current target: GT-2* cell below as `DISPUTED — see CF-001`.**
>
> **What does NOT change:** §0's conclusion. The collapse rule targets PARENT `80a8ed25…`; `c13df1f4` is censused at 39 duplicate runs, 12.2 % abutting, 0 zero-length and **does not carry the defect either.** **Zero of 91 citations are affected by ED-004** — the conclusion is unchanged and rests on firmer ground. `CF-001` is a provenance conflict, not a collapse-impact finding, and its disposition is Executive.

## 1.1 · Complete inventory

**91 citations. 91 distinct cue indices. Zero duplicates. Zero out of range.** `[E]`

| registry | artifact | citations | index range | current target | proposed target | status |
|---|---|---|---|---|---|---|
| `RIDER_REGISTRY.yaml` | `intelligence/p2/registries/` | **80** | 31 – 2284 | GT-2 `89d61f96…` | **unchanged** | **UNAFFECTED** |
| `MOTORCYCLE_REGISTRY.yaml` | `intelligence/p2/registries/` | **6** | within 1 – 2291 | GT-2 `89d61f96…` | **unchanged** | **UNAFFECTED** |
| `ORGANIZATION_REGISTRY.yaml` | `intelligence/p2/registries/` | **3** | within 1 – 2291 | GT-2 `89d61f96…` | **unchanged** | **UNAFFECTED** |
| `PROMPT_REGISTRY.yaml` | `intelligence/p2/registries/` | **2** | within 1 – 2291 | GT-2 `89d61f96…` | **unchanged** | **UNAFFECTED** |
| **total** | | **91** | **31 – 2284** | | | **91 UNAFFECTED** |

**Citation form**, measured from `RIDER_REGISTRY.yaml`:

```yaml
- {id: R01, name: Clutch, affil: "road captain, 9th roundup", cue: "#31 01:51", conf: MEDIUM, …}
- {id: R02, name: Hollywood, affil: "president [org UNCONF]",  cue: "#46 02:16", conf: MEDIUM}
```

**Most citations are a compound: a cue index *and* a timecode.** That second field is load-bearing and §4.2 returns to it — **including a correction: 82 of 91 carry it, not all 91.**

**Provenance is declared in the registry header**, `RIDER_REGISTRY.yaml` line 4:

> `source: canonical SRT GT-2 (founding extraction of record 2026-08-20)`

**The registry names a stream — and names the wrong one.** All 91 citations were extracted on 2026-08-20 and have never been re-pointed. **Measurement shows the extraction source was `c13df1f4…`, not the GT-2 the header declares. See `CF-001`.**

## 1.2 · No generated identifiers

Per the Order's Explicit Prohibitions, **no collapsed identifier was generated.** The *Proposed target* column reads *unchanged* because that is the measured answer under the rule's declared scope, not because a table was withheld.

**One tension in the Order is recorded rather than resolved:** Objective 1 requires a *Proposed target* column while the Prohibitions forbid generating collapsed identifiers. Under the actual scope the two do not conflict. **Under the counterfactual in §4 they would**, so §4 reports shift *magnitudes and counts* and emits no identifier table.

---

# 2 · WHY GT-2 IS NOT AFFECTED — THE MEASUREMENT

Four caption streams were censused with one instrument.

| stream | cues | collapsed | duplicate runs | run lengths | **abutting** | zero-length |
|---|---|---|---|---|---|---|
| **PARENT `80a8ed25`** — the collapse target | **5,664** | **2,962** | **2,612** | `{2: 2569, 4: 42, 8: 1}` | **98.7 %** | **29** |
| **GT-2 `89d61f96`** — the 91 citations | **2,291** | 2,247 | **41** | `{2: 39, 3: 1, 4: 1}` | **13.6 %** | **0** |
| analysis-cut `2a16dd70` — 08-24 context | 2,036 | 2,001 | 33 | `{2: 32, 4: 1}` | 45.7 % | 0 |
| Part 2 SRT `c13df1f4` | 2,290 | 2,249 | 39 | `{2: 38, 4: 1}` | 12.2 % | 0 |

**The two profiles are not the same phenomenon.** `[E]`

**PARENT: 2,612 duplicate runs, 98.7 % abutting, lengths strictly powers of two.** Mechanical re-issue — one utterance's span tiled by copies at cut points.

**GT-2: 41 duplicate runs, 13.6 % abutting, including a run of 3.** Eighty-six percent are *separated in time*, and a run of length 3 does not fit a doubling process at all. **These read as genuine repeated speech — someone said the same words twice, minutes apart.** A collapse rule tuned to the PARENT defect would, if applied to GT-2, merge real repetitions into single utterances.

**That is the strongest argument in this assessment for keeping the rule's scope bound to a named stream hash.**

---

# 3 · REGISTRY & ARTIFACT IMPACT

## 3.1 · Dependency classification

| artifact | class | basis |
|---|---|---|
| `RIDER_REGISTRY.yaml` (80) · `MOTORCYCLE_REGISTRY.yaml` (6) · `ORGANIZATION_REGISTRY.yaml` (3) · `PROMPT_REGISTRY.yaml` (2) | **DIRECT — on GT-2** | carry `#NNNN` bound to `89d61f96…` |
| `AR2-0822.context.json` | **DIRECT — on GT-2** | declares `sha.srt 89d61f96…`, `srt.cues 2291` |
| `AR2-0824.context.json` | **DIRECT — on the analysis cut** | declares `sha.srt 2a16dd70…`, `srt.cues 2036` |
| `build_context.py` | **DIRECT — on any stream it is pointed at** | §6.1 |
| `INGESTION_MANIFEST.yaml` → `assembly_captions` | **DIRECT — on PARENT** | the only artifact naming `80a8ed25…`; `ingestion_status: AWAITING_INGESTION` |
| `DAY2_PARENT_FORENSIC_AUDIT.md` (5 `#NNNN`) | **INDIRECT** | historical measurement record; class H — *never re-pointed, true of when written* |
| `CAPTION_REGISTRY.yaml` | **INDIRECT** | binds to the FCPXML `2bf06853…` for title text and positions, **not to cue indices** |
| `VOICE_OVER_REGISTRY.yaml` | **INDIRECT** | *"host-speech boundaries observed in GT-2"* — observational, no `#NNNN` |
| `EXECUTIVE_DECISION_BRIEF_CUSTODY_ALERT_001.md` · `DEPENDENCY_INVENTORY.md` | **INDIRECT** | describe the citation set; class H |
| Presentation artifacts — Gamma MASTER / BUILD, Executive Edition | **NO DEPENDENCY** | the single `#NNNN` in each is `cue #136`, quoted inside one specimen registry record as an illustration |
| Runtime guards `G-01`…`G-13` | **NO DEPENDENCY on cue index** | `G-09` asserts cue *geometry*, never cue *identity* — §6.2 |
| `gen_artifacts.py` / `gen_artifacts_v2.py` | **NO DEPENDENCY on cue index** | consume timecodes and the ETC, not `#NNNN` |
| `fcpx_resolve.py` · `etc_extract.py` | **NO DEPENDENCY** | FCPXML and ETC only; captions never enter |

## 3.2 · The decisive structural fact

**The PARENT stream has no governed consumers today.** `[E]`

```
80a8ed25…  referenced by   INGESTION_MANIFEST.yaml   assembly_captions
                            DAY2_PARENT_FORENSIC_AUDIT.md   (measurement record)
           referenced by   NO context file
           referenced by   NO registry citation
           consumed by     NO generator, NO guard, NO governed artifact
           ingestion_status  AWAITING_INGESTION
```

**Nothing downstream depends on it, because nothing has ingested it.** The rule governs an asset at the threshold, and that is the safest possible moment to govern one.

---

# 4 · STRUCTURAL STABILITY

## 4.1 · Representation versus semantics

| property | changes under collapse? | class |
|---|---|---|
| **Cue numbering** | **YES** — indices shift for every cue after the first duplicate run | **REPRESENTATION** |
| **Cue count** | **YES** — 5,664 → 2,962 on PARENT | **REPRESENTATION** |
| **Cue identity** | **YES — and it is not recoverable** | **REPRESENTATION** |
| **Cue ordering** | **NO** — order is preserved; collapse merges neighbours, never reorders | invariant |
| **Transcript identity** | **NO** — CCR-001: 10,209 → 5,145 against an independent 5,151, **0.12 %** | **SEMANTIC — preserved** |
| **Timing identity** | **NO** — a collapsed run spans `[first.start, last.end]`; the covered union is unchanged | invariant |
| **Registry identity** | **NO** — registry ids `R01`…, artifact names and file hashes are untouched by a caption rule | invariant |

**Collapse is a representation change, not a semantic one.** Everything it alters is an artifact of how the picture was cut. Everything it preserves is what was said and when.

## 4.2 · The compound citation is a partial safety net

> ### ERRATUM 1 — issued post-delivery, correcting this section
>
> **This section originally stated that every citation carries a timecode. That is false, and the error was mine.** Re-measured across all four registries:
>
> ```
> RIDER_REGISTRY.yaml         80 citations   80 with timecode    0 without
> PROMPT_REGISTRY.yaml         2 citations    2 with timecode    0 without
> MOTORCYCLE_REGISTRY.yaml     6 citations    0 with timecode    6 WITHOUT
> ORGANIZATION_REGISTRY.yaml   3 citations    0 with timecode    3 WITHOUT
>                             ──                                 ──
>                             91              82                  9
> ```
>
> **82 of 91 carry a timecode. Nine do not.** The nine appear in list-form and bare-cue entries that use a different citation shape:
>
> ```yaml
> MOTORCYCLE_REGISTRY   harley-davidson:        cues: ["#280","#776","#1420","#1471","#2031"]
> MOTORCYCLE_REGISTRY   vrod_2003_anniversary:  cue:  "#2029"
> ORGANIZATION_REGISTRY ORG03 Buffalo Soldiers: cues: ["#303","#1047"]
> ORGANIZATION_REGISTRY CIV02 Nissan Motor Co.: cue:  "#1148"
> ```
>
> **Consequence, and it makes the risk worse rather than better.** `R-1` said a wrong cue index is caught by nothing. For 82 citations a validator can at least be built. **For these nine there is no second field to check against at all — they are structurally unvalidatable in their present form**, and they are the citations that bind a make, a model and an organisation to a moment in the film. **This is a finding, not a footnote, and it belongs to `R-1`.**

Most citations carry **an index and a timecode** — `"#31 01:51"`. `[E]`

**The index is fragile: it always resolves and never errors.** `DEPENDENCY_INVENTORY.md` §3 states the danger exactly:

> *"A wrong timecode is caught by a bounds check. A wrong cue index is caught by nothing. It always resolves, it never errors, and the result is a confident misattribution of a quote or a rider to a person who did not say it."*

**The timecode is the durable half.** Under collapse the timecode of the cited utterance does not move — a collapsed run begins where its first member began. **So 82 of the 91 citations already carry the field needed to verify or rebuild an index. Nine do not.**

**This is not a proposal.** It is an observation that the migration risk in §5 is lower than the index-only framing suggests **for 82 citations**, because those were written with both fields at the founding extraction — and **unchanged for the remaining nine**, which have no second field.

---

# 5 · RE-POINTING STRATEGY

## 5.1 · Under the rule's actual scope

**No re-pointing is required. Zero citations change.** The migration is empty.

## 5.2 · Counterfactual — if the rule were extended to GT-2

Reported because the Executive should know the cost of a scope decision *before* making it, not after. **Magnitudes and counts only; no identifiers generated.**

```
citations resolvable in GT-2 (1…2291)          91 of 91
citations out of range                          0
citations that would keep their index           0
citations that would shift                     91
   shift magnitude                             min 1 · max 44 · mean 19.4

distinct targets from 91 distinct sources      91
COLLISIONS — two citations onto one cue         0        ← the map is INJECTIVE

cited cues sitting INSIDE a duplicate run       5        ← all in RIDER_REGISTRY
```

**Can every citation be deterministically re-pointed? 86 of 91, yes. 5, no.**

**The 86** sit outside every duplicate run. Their new index is a pure function of the collapse — one target each, no collisions, fully deterministic, machine-verifiable against the timecode each citation already carries.

**The 5 require Executive review**, and the reason is precise rather than procedural. A cited cue *inside* a duplicate run means the citation named one member of a run whose members are about to become one cue. **The platform cannot know whether the citation meant that member specifically or the utterance as a whole** — and under `EPR-001 §2.3` and the standing no-silent-recovery rule it must not guess. All five are in `RIDER_REGISTRY.yaml`, which is the registry where a wrong index misattributes a person's words.

**Zero collisions across the whole set is the strong result.** An injective map means no citation would silently merge with another — the failure mode that would be invisible.

---

# 6 · RUNTIME IMPACT

## 6.1 · One component stops. It is designed to.

`build_context.py`, lines 121–125:

```python
if paths['srt']:
    cues = count_srt_cues(paths['srt'])
    dec  = (ctx.get('srt') or {}).get('cues')
    if dec is not None and dec != cues:
        stop('declared srt.cues (%s) does not equal the measured cue count (%d)' % (dec, cues))
```

**Declaring the rule and collapsing a stream changes its cue count, and any context declaring the old count STOPS.** `[E]`

| context | declared | measured today | status |
|---|---|---|---|
| `AR2-0822` | `srt.cues 2291` on `89d61f96…` | 2,291 | **agrees** |
| `AR2-0824` | `srt.cues 2036` on `2a16dd70…` | 2,036 | **agrees** |
| PARENT `80a8ed25…` | **not declared in any context** | 5,664 | **no context to break** |

**This is correct fail-shut behaviour and it is the platform's single best protection here.** A collapse applied without updating the declaration cannot silently propagate — the context refuses to build. **It is also the reason the rule and the context declaration must be issued together.**

## 6.2 · Runtime guards — no cue-identity dependency

`G-09` asserts cue **geometry**, never cue **identity**:

```
G-09  cue registry   ordered, non-overlapping, in range
```

Its three predicates were simulated against every stream, before and after collapse:

| stream | ends-before-start | overlapping | out of range | zero-length | **G-09** |
|---|---|---|---|---|---|
| PARENT, as it stands | 0 | 0 | 0 | 29 | **PASS** |
| PARENT, collapsed | 0 | 0 | 0 | 13 | **PASS** |
| GT-2, as it stands | 0 | 0 | 0 | 0 | **PASS** |
| GT-2, collapsed | 0 | 0 | 0 | 0 | **PASS** |

**No guard fires before or after collapse, on any stream.** `[E]`

**One precision worth recording.** The manifest's second declared defect, `NONPOSITIVE_DURATION_CUES`, is **29 zero-length cues — `end == start` — and zero inverted cues.** `G-09` tests `end < start`, so **zero-length cues pass it invisibly.** Collapse reduces them from 29 to 13 by absorbing those inside duplicate runs. **Thirteen survive any collapse rule and remain undispositioned.**

## 6.3 · Everything else

| component | impact |
|---|---|
| `gen_artifacts.py` / `_v2.py` | **none** — consume the ETC and timecodes, never `#NNNN`. Also under RUN_ID lock |
| `fcpx_resolve.py` · `etc_extract.py` | **none** — FCPXML and ETC only |
| `runtime_guards.py` `G-01`–`G-13` | **none** on identity; `G-09` geometry unaffected |
| `traceability_scan.py` | **none** — scans production-identifying literals, not cue indices |
| `conformance_suite.py` / `ecr_gen_002_suite.py` | **none measured** — no `#NNNN` assertions |
| `epr_validate.py` | **none** — segment-keyed (`S01`…`S19`), a different binding class |
| Presentation generation | **none** — no derived figure depends on a cue count |
| Registry validation | **no cue-index validator exists** — §7, risk `R-1` |

---

# 7 · RISK ASSESSMENT

## Critical

**`R-1` · There is no automated detector for a wrong cue index.**
*Description.* A stale `#NNNN` always resolves and never errors. `DEPENDENCY_INVENTORY.md` calls this *"the highest-severity item in the inventory"* and records that **it has no automated detection.** This risk exists **today**, independent of the rule.
*Likelihood.* Certain, if any citation is ever re-pointed by hand.
*Impact.* Confident misattribution of a quote or a rider to a person who did not say it.
*Mitigation, recommended not implemented.* **82 of 91 citations already carry a timecode (§4.2). A validator checking index against timecode would convert a silent failure into a caught one for those 82 and requires no new data.** The remaining **nine have no second field and cannot be validated in their present form** — a validator should report them as `UNVALIDATABLE` rather than pass them, and whether to give them timecodes is an Executive matter, not an engineering one. This is the single highest-value engineering item this assessment found, and it is worth doing whether or not the rule is declared.

## Moderate

**`R-2` · Scope creep from PARENT onto GT-2.**
*Description.* A rule declared without a stream hash could later be read as applying to GT-2, whose 41 duplicate runs are 86 % non-abutting and include a run of 3 — **genuine repeated speech, not the defect** (§2).
*Likelihood.* Moderate, if scope is declared by defect name rather than by hash.
*Impact.* 91 citations invalidated at once, and real repetitions silently merged.
*Mitigation.* **Declare the rule against `80a8ed25…` by hash.** Any extension becomes a separate, visible determination.

**`R-3` · Tokenization is undeclared.**
*Description.* CCR-001's 0.12 % convergence was measured under lowercase, punctuation-stripped, whitespace-split tokenization. **Case, punctuation, hyphenation, numerals and speaker labels each move the count, and none is declared anywhere in the repository.**
*Likelihood.* Certain — every implementer picks something.
*Impact.* The rule is not reproducible; two correct implementations disagree.
*Mitigation.* Declare tokenization in the same instrument as the rule.

**`R-4` · The two declared defects are coupled.**
*Description.* Thirteen zero-length cues survive collapse (§6.2) and pass `G-09` invisibly.
*Likelihood.* Certain.
*Impact.* `NONPOSITIVE_DURATION_CUES` remains open after the rule is declared, and the manifest's ingestion precondition is only half discharged.
*Mitigation.* Disposition both defects in one instrument, or state explicitly that the second remains open.

## Low

**`R-5` · The run of 8.** One caption in PARENT was re-issued eight times. Any rule should be checked against that case, not against the 2,569 pairs.

**`R-6` · Historical records must not be re-pointed.** The 5 `#NNNN` in `DAY2_PARENT_FORENSIC_AUDIT.md` are class H — true of when written. Re-pointing them would falsify a measurement record.

**`R-7` · Presentation artifacts carry `cue #136` as an illustration.** Not a governed citation. If GT-2 were ever collapsed, the specimen would become inconsistent with the registry it illustrates. Cosmetic; recorded for completeness.

---

# 8 · BACKWARD COMPATIBILITY

**Evaluated, not implemented. Recommended in order of fit to this repository's existing patterns.**

| approach | assessment |
|---|---|
| **Do nothing — no dual indexing needed** | **RECOMMENDED under the actual scope.** PARENT has no governed consumers (§3.2). There is no old identifier set to remain compatible with |
| **Bind citations by stream hash** | **RECOMMENDED as the durable form.** A citation reading *`#31` in `89d61f96…`* is unambiguous forever. It matches the platform's existing pattern — `CAPTION_REGISTRY` already binds entries to `2bf06853…` per record |
| **Index-plus-timecode verification** | **RECOMMENDED.** The data is already there (§4.2). Cheapest real protection available |
| **Translation table** | Viable if GT-2 is ever collapsed; the map is injective (§5.2). **But a table is a second source of truth and would need its own governance** |
| **Alias mapping** | Not recommended. Aliases make both identifiers valid, which is the opposite of what a silent-failure surface needs |
| **Versioned registries** | Not recommended now. The registries are already versioned by commit, and a parallel scheme adds drift surface without adding safety |
| **Dual indexing inside a record** | Not recommended. Doubles the field a validator must check and doubles the chance of one going stale |

---

# 9 · WHAT THIS ASSESSMENT DOES NOT ESTABLISH

- **Whether the rule should be declared.** Not asked, not answered.
- **Which stream the rule should govern.** Measured as PARENT from the manifest. **If the Executive intends a different stream, every number in §1 and §5.1 changes**, and §5.2 becomes the operative section.
- **Exact invariance.** CCR-001 recorded that no two streams here share a transcription. Unchanged. `[O]`
- **Whether the 5 in-run citations meant a member or the utterance.** Unknowable from the record; that is why they route to Executive review.
- **The correctness of the founding extraction.** All 91 were extracted on 2026-08-20 and never verified against their timecodes. **This assessment did not verify them either** — that is `R-1`'s mitigation, and it is engineering work not authorized here. `[O]`

---

# 10 · RECOMMENDATION

```
READY WITH CONDITIONS
```

**The rule as scoped is low-risk because it governs an asset that nothing consumes.** Zero of 91 citations change. No guard fires. One component — `build_context.py` — stops if a declaration and a stream disagree, which is the behaviour that makes this safe rather than a reason for concern. The migration is empty, and the moment to govern an asset is before it is ingested, not after.

**Four conditions, each traceable to a measurement above:**

1. **Declare the rule against `80a8ed25…` by hash, not by defect name.** GT-2's 41 duplicate runs are a different phenomenon (§2), and scope stated by name will eventually be read onto them.
2. **Declare tokenization in the same instrument.** Without it the rule is not reproducible (`R-3`).
3. **Disposition `NONPOSITIVE_DURATION_CUES` in the same instrument, or state that it remains open.** Thirteen zero-length cues survive collapse and pass `G-09` invisibly (`R-4`).
4. **Issue the rule and the context declaration together.** A collapsed stream with a stale `srt.cues` stops `build_context.py` (§6.1).

**And one item that stands on its own merits.** `R-1` — the absence of any index-against-timecode validator — is the highest-severity item in the repository's own inventory, exists today, and is unaffected by this decision. **82 of 91 citations already carry the timecode needed to check them; nine carry nothing to check against and are structurally unvalidatable as written.** That work is worth authorizing whether the rule is declared or not.

---

```
Citations censused                 91 · 4 registries · 91 distinct indices · 0 out of range
Citations carrying a timecode      82 of 91 · 9 UNVALIDATABLE as written (ERRATUM 1)
Declared vs actual stream          CONFLICT — CF-001 (ERRATUM 2) · declared GT-2, measured c13df1f4
Citation target                    GT-2 89d61f96… · 2,291 cues
Collapse rule target               PARENT 80a8ed25… · 5,664 cues
Citations affected as scoped       0 of 91
Deterministic re-point (if scoped onto GT-2)   86 of 91 · 0 collisions · map injective
Requiring Executive review         5 · all RIDER_REGISTRY · cited inside duplicate runs
Runtime components affected        1 — build_context.py, fail-shut by design
Runtime guards firing              0, before or after collapse, on any stream
Critical risks                     1 — no cue-index validator, pre-existing
Identifiers generated              NONE
Registries modified                NONE
Commits                            NONE
Determinations made                NONE
```

---

*Prepared under CIA-001. Custody: MACHINE. Authority: NONE. No registry, citation, cue, identifier, runtime component, intelligence artifact, presentation asset or source file was modified. No collapsed identifier was generated. No commit was made. ED-004 is not declared here and remains reserved to Executive authority.*
