# CF-001 — CAPTION STREAM EVIDENCE REVIEW

**Prepared under:** Executive direction, *CF-001 Caption Stream Determination*, Executive Producer / Chairman, 2026-08-30
**Prepared by:** Governance Compliance Auditor · **Custody:** `MACHINE` · **Authority:** NONE
**Mode:** READ-ONLY. No caption stream, registry, citation, script or artifact was modified. No commit made. **No determination is made.**
**Measured at:** repository `2b7f055` · volume `WE_CAPE_OUTPUT` as mounted 2026-08-30

> **This review supplies evidence for a determination. It does not make one.** Where the evidence supports a conclusion it says so; where it does not, it refuses.

---

# 0 · HEADLINE

```
Candidate streams on the volume        8 distinct  ·  17 files
CF-001 tested                          4 of 8      ·  4 excludable on cue count
Streams with a governed FCPXML pairing 1 of 8      ·  89d61f96 only
Streams bound into governed artifacts  89d61f96: 19    c13df1f4: 0
Five Executive criteria                89d61f96 favoured on 5 of 5
```

> ## THE EVIDENCE DOES NOT SUPPORT ANY OF THE THREE ENUMERATED OUTCOMES AS WRITTEN
>
> **All three assume the defect lies in the declaration.** The evidence points the other way: **the declared stream is the one with lineage, custody and authority, and the citation indices were derived from a superseded pre-lock export of a different project.**
>
> **That is a fourth outcome — Outcome D — and it is set out at §7 alongside the three.**

---

# 1 · COMPLETE STREAM CENSUS — 8 DISTINCT, 17 FILES

**Every `.srt` on every mounted volume, hashed.** `[E]`

| sha256[:8] | cues | bytes | `<font>` tags | copies | identity |
|---|---|---|---|---|---|
| **`89d61f96`** | 2,291 | 140,526 | 0 | 2 | **GT-2 — declared source** |
| **`c13df1f4`** | 2,290 | 206,655 | 2,290 | 3 | **Part 2 SRT — measured match** |
| `2a16dd70` | 2,036 | 184,616 | 2,036 | 2 | analysis cut |
| `80a8ed25` | 5,664 | 350,300 | 0 | 2 | PARENT |
| `c057fccf` | 909 | 57,398 | 0 | 2 | Day 2 Part 1 |
| `65a313bc` | 767 | 49,085 | 0 | 2 | Day 2 Part 2 |
| `96bbee5d` | 400 | 24,705 | 0 | 2 | Day 2 Part 3 |
| `c78ac4c3` | 824 | 78,519 | 824 | 2 | 2026-07-29 snapshot |

**`CF-001` tested four streams and described them as *"every candidate caption stream on the volume."* There are eight.** The census was incomplete. `[E]`

**The four untested streams are excludable, on evidence rather than assumption.** `CF-001` records the analysis cut (2,036 cues) resolving only **76 of 82** citations — so at least six cited indices exceed 2,036. **A stream of 909, 824, 767 or 400 cues cannot resolve a citation indexed above its own length.** All four fall far below. **They are excluded by arithmetic, and the exclusion is now on the record rather than assumed.** `[E]`

**Two credible candidates remain: `89d61f96` and `c13df1f4`.**

---

# 2 · PROVENANCE — THE FCPXML PAIRING

**The decisive structural evidence, and `CF-001` did not have it.** Each SRT sits beside an FCP project bundle. **Pairing them by directory and stem resolves which editorial timeline each stream came out of.** `[E]`

| directory | FCP project | project sha256[:8] | SRT in that directory |
|---|---|---|---|
| `XML retry/Thursday Aug 20th/Final Data Source Files/` | `Alpha RoudUp Part 2.fcpxmld` | **`2bf06853`** | **`89d61f96`** |
| `XML retry/Thursday Aug 20th/` | `SRT PART 2.fcpxmld` | `7f243ddc` | `c13df1f4` |
| `Alpha RoundUp Part 2 /` | `Part 2 SRT .fcpxmld` | `91488774` | `c13df1f4` |
| `SPRINT3A_WORK/inputs/` | `Info.fcpxml` = **`2bf06853`** | **`2bf06853`** | `lock_srt2.srt` = **`89d61f96`** |

**`2bf06853` is the picture lock.** `CAPTION_REGISTRY.yaml` names it verbatim as an authoritative input:

> `Alpha RoudUp Part 2.fcpxmld/Info.fcpxml   2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7`

**Therefore:** `[E]`

- **`89d61f96` is the caption export of the picture-lock project**, sharing its directory and its filename stem, and adopted into `SPRINT3A_WORK/inputs/` as **`lock_srt2.srt`** beside `Info.fcpxml` = `2bf06853`. **The pair is complete and internally consistent.**
- **`c13df1f4` is the caption export of two different projects** — `7f243ddc` and `91488774` — **neither of which is the picture lock, and neither of which is named as an authoritative input by any governed artifact.**

## 2.1 · Chronology

**Modification times, with the caution this program has applied before: a copy time is not a creation time.** `[E]` · the inference drawn from them is marked `[P]`

```
c13df1f4   2026-08-19 20:50    Alpha RoundUp Part 2 /Part 2 SRT _SRT_...
c13df1f4   2026-08-19 21:19    Alpha RoundUp Part 2 /Part 2 SRT  - SD 480p_srtCaptionSuffix_...
c13df1f4   2026-08-20 13:27    XML retry/Thursday Aug 20th/SRT PART 2_SRT_...
89d61f96   2026-08-21 00:39    XML retry/Thursday Aug 20th/Final Data Source Files/...
89d61f96   2026-08-22 11:41    SPRINT3A_WORK/inputs/lock_srt2.srt
```

**`RIDER_REGISTRY.yaml` declares `run: {date: 2026-08-21, … source: canonical SRT GT-2 (founding extraction of record 2026-08-20)}`.**

**On 2026-08-20, no copy of `89d61f96` is observable at any path.** The earliest is 2026-08-21 00:39. **`c13df1f4` is the only Part 2 caption stream observable on the declared extraction date.** `[E]`

**Inference, marked as such:** the founding extraction read the only Part 2 SRT then present — `c13df1f4` — and the declaration was written the following day naming the lock-paired stream that had by then superseded it. **`[P]` — no copy of `89d61f96` with an earlier timestamp was found, but absence at these paths is not proof of non-existence elsewhere.**

---

# 3 · REPOSITORY AUTHORITY — 19 AGAINST 0

**Every committed file referencing each hash, classified by whether it *binds* the stream or merely *discusses* it.** `[E]`

## 3.1 · `89d61f96` — 30 files, of which 19 bind

| binding artifact | what it binds |
|---|---|
| `intelligence/p2/registries/CAPTION_REGISTRY.yaml` | **a registry** — declares it an authoritative input |
| `intelligence/p2/ess/context/AR2-0822.context.json` | **the governed context declaration** |
| `intelligence/p2/ess/context/AR2-0822.observations.json` | governed observations |
| `intelligence/p2/ess/CONDUCTOR_SCORE.yaml` | generated governed artifact |
| `intelligence/p2/ess/EDITORIAL_SYNCHRONIZATION.yaml` | generated governed artifact |
| `intelligence/p2/ess/VISUAL_EVENT_REGISTRY.yaml` | generated governed artifact |
| `intelligence/p2/ess/PRODUCTION_INTELLIGENCE_SEED.yaml` | the seed |
| `intelligence/p2/mie/BEHAVIORAL_FINGERPRINT.yaml` · `VOICE_PRIORITY_MAP.yaml` | MIE artifacts |
| `intelligence/p2/ess/scripts/gen_artifacts.py` | **hard-coded generator input** |
| `intelligence/p2/ess/scripts/conformance_suite.py` · `verification.diff` | conformance |
| `intelligence/p2/mie/scripts/behavioral_fingerprint.py` · `voice_priority_map.py` | MIE generators |
| `docs/rulings/EXECUTIVE_RULINGS.yaml` | **an Executive ruling** |
| `docs/doctrine/VPD-001_Voice_Priority_Doctrine.md` | **doctrine** |
| `docs/reference_executions/RE-001_WECAPE-AR2-SPRINT3A.md` | **the Reference Execution baseline** |
| `intelligence/p2/ess/EXECUTION_LOG.md` · `STEP0_TIMING_CLOSURE.md` | execution record |

## 3.2 · `c13df1f4` — 6 files, of which **0 bind**

`PROGRAM_EXECUTION_ROADMAP_v2` · `CF-001` · `CIA-001` · `ECR-003` · `EDR-002` · `ED-CAM-001`

**All six are reviews or reports. All six were written on or after 2026-08-30. All six exist to describe this conflict.** `[E]`

> **`c13df1f4` is bound by no registry, no context declaration, no script, no generated artifact, no ruling, no doctrine and no Reference Execution. Its entire presence in the governed corpus is commentary about its own anomaly.**

---

# 4 · CONTENT — THE TWO STREAMS ARE DIFFERENT TRANSCRIPTIONS

**`CF-001` §3 reported four citations matching `c13df1f4` and failing GT-2, and concluded the registries cite a different file than they name. That is correct. It did not test whether the named file contains the same material. It does.** `[E]`

| registry entry | cited index | index in `c13df1f4` | **index in GT-2** | present in GT-2? |
|---|---|---|---|---|
| `R01` Clutch | `#31` | 31 | **#34** — `"Clutch."` | **yes** |
| `R02` Hollywood | `#46` | 46 | **#49** — `"Hey, my name is Hollywood."` | **yes** |
| `R03` Mark Tillman | `#60` | 60 | **#63** — `"My name is Mark Tillman."` | **yes** |
| `R05` Rose | `#95` | 95 | **#96** — `"Rose?"` | **yes** |

**All four utterances exist in GT-2, at indices offset by +3, +3, +3 and +1.** The offset is **not constant**, so no single shift re-points the citations. `[E]`

## 4.1 · But the streams are not the same transcript

**Normalized to text only — markup, indices and timecodes stripped:** `[E]`

```
GT-2        2,291 lines   59,158 text bytes
c13df1f4    2,290 lines   58,913 text bytes

identical lines            1,161
unique to GT-2             1,130
unique to c13df1f4         1,129
```

**Roughly half of all lines differ in wording.** Samples:

| `c13df1f4` | GT-2 |
|---|---|
| `06 Riders, MC, Baltimore Mallet, baby.` | `06 Riders, MC, Baltimore Mallard, baby.` |
| `04, uh, 04, uh, VTX, 1300.` | `04, 04, BTX, 1300.` |
| `06 riding.` | `06 rider.` |

**These are two independent transcriptions of the same audio** — same runtime (`01:20:38` → `01:20:41` vs `01:20:40`), same speakers, same content, different wording decisions and different cue boundaries. **Not two segmentations of one transcript.** `[E]`

**Which transcription is more accurate is an editorial judgment about audio, not a repository measurement. This review does not make it and cannot.** `[O]`

## 4.2 · What a stream change would cost the registries

**15 rider names tested against both streams.** `[E]`

```
present in both                14 of 15
absent from GT-2                1 of 15   ·  "Slow-mo"  (R23)
absent from both                1         ·  "Buckeye"  (R07)
```

- **`R23` "Slow-mo" does not appear in GT-2 at all.** `RIDER_REGISTRY` records `note: names are verbatim-of-transcript`. **Under GT-2 that name is not verbatim of anything.**
- **`R07` "Buckeye" appears in neither stream** — an independent open question this review surfaces and does not resolve. `[O]`
- **`R09`'s affiliation wording differs**: `Baltimore Mallet` (`c13df1f4`) against `Baltimore Mallard` (GT-2). The registry records `Baltimore [UNCONF]` and quotes neither, so this entry is unaffected.

---

# 5 · THE FIVE EXECUTIVE CRITERIA

| # | criterion | `89d61f96` GT-2 | `c13df1f4` |
|---|---|---|---|
| **1** | **Provenance** — unbroken custody chain | **YES.** Paired export of `2bf06853`; adopted as `lock_srt2.srt`; declared in context and registry | **NO.** Export of `7f243ddc` / `91488774`; **no governed artifact records its origin** |
| **2** | **Lineage** — derives from the governed editorial timeline | **YES.** Shares directory and stem with the picture lock | **NO.** Derives from two projects that are not the picture lock |
| **3** | **Repository authority** — bound into governed artifacts | **YES — 19**, including a registry, a ruling, doctrine and `RE-001` | **NO — 0.** Six references, all post-hoc commentary |
| **4** | **Editorial fidelity** — governed work, not an intermediate export | **YES**, on available evidence. Plain text, lock-paired | **WEAKER.** `<font color>` on all 2,290 cues and a sibling named `SD 480p_srtCaptionSuffix` — **markers of a delivery export** `[P]` |
| **5** | **Determinism** — reachable without interpretation | **YES.** Declared in `AR2-0822.context.json`, in registry headers, hard-coded in `gen_artifacts.py` | **NO.** Reachable only by knowing this conflict exists |

**Five of five favour `89d61f96`.** **The single fact favouring `c13df1f4` is that the citation indices resolve against it — which is a fact about how the citations were produced, not about the stream's standing.** `[E]`

---

# 6 · GOVERNED CONSUMERS AND DOWNSTREAM IMPACT

| consumer | binds | effect if GT-2 is affirmed | effect if `c13df1f4` is declared |
|---|---|---|---|
| `CAPTION_REGISTRY.yaml` | GT-2 | none | **declared input becomes false** |
| `AR2-0822.context.json` | GT-2 | none | **governed context becomes false** |
| `gen_artifacts.py` | GT-2, hard-coded | none | **generator input wrong — a code change** |
| `CONDUCTOR_SCORE` · `EDITORIAL_SYNCHRONIZATION` · `VISUAL_EVENT_REGISTRY` | GT-2 | none | **regeneration required under `DOC-002`** |
| `VPD-001` doctrine · `EXECUTIVE_RULINGS.yaml` | GT-2 | none | **doctrine and a ruling cite a superseded stream** |
| `RE-001` Reference Execution | GT-2 | none | **the comparison baseline is invalidated** |
| `RIDER_REGISTRY` + 3 registries, 91 citations | indices from `c13df1f4` | **91 citations require re-derivation; `R23` loses its verbatim name** | none |

**The asymmetry is stark and it is measured, not argued.** `[E]`
**Affirming GT-2 costs a citation re-derivation. Declaring `c13df1f4` invalidates a registry, a context declaration, a generator input, three generated artifacts, a doctrine, an Executive ruling and the Reference Execution baseline.**

---

# 7 · OUTCOME ASSESSMENT

## Outcome A — *the currently declared stream is authoritative; CF-001 closes with no repository correction*

**PARTIALLY SUPPORTED.** The first clause is supported on five of five criteria. **The second is not:** the 91 citations demonstrably index `c13df1f4`, so a correction is required — **to the citations, not to the declaration.** `[E]`

## Outcome B — *a different stream is authoritative; the declaration becomes a provenance defect*

**NOT SUPPORTED.** `c13df1f4` fails provenance, lineage, repository authority and determinism. **Declaring it authoritative would make a registry, a context file, a generator, three artifacts, a doctrine, a ruling and `RE-001` all wrong at once**, to rescue an index binding. `[E]`

## Outcome C — *evidence insufficient; remain UNRESOLVED*

**SUPPORTED FOR ONE SUB-QUESTION AND NOT FOR THE OTHER.**

- **The stream question is answerable.** Five of five criteria, an unbroken FCPXML pairing, and a 19-to-0 authority ratio. `[E]`
- **The remediation question is not.** The two streams are different transcriptions differing on ~half their lines; re-pointing touches **verbatim-of-transcript** content, and `R23`'s name does not exist in GT-2 at all. **Which wording is correct is an editorial judgment on audio the platform cannot make.** `[O]`

## **Outcome D — the declaration is correct and the citations are defective**

**This is what the evidence supports, and it is absent from the three enumerated outcomes, all of which locate the defect in the declaration.** `[E]`

> **GT-2 `89d61f96` is the caption stream of the governed editorial timeline. The 91 citation indices were derived on 2026-08-20 from `c13df1f4` — a pre-lock export of a different project, and the only Part 2 caption stream observable on that date.**
>
> **The provenance defect is real and it runs the other way: not a registry naming the wrong file, but an extraction reading a superseded one and a declaration written afterwards that named the right one.**

**Under Outcome D, `CF-001` closes on the stream and opens a narrower successor on the citations.** The successor is bounded: re-derive 91 indices against GT-2 by text match, and refer the `R23` name and any wording divergence to the editorial channel. **`ED-004` and `ECR-003 G-1` unblock as soon as the stream is fixed** — the tolerance `G-1` needs is measurable against a settled stream.

---

# 8 · WHAT THIS REVIEW DOES NOT ESTABLISH `[O]`

- **Which transcription is more accurate.** Not measurable from the repository. Referred, not judged.
- **The 9 citations without timecodes.** Untestable by any method available here, exactly as `CF-001` recorded.
- **`R07` "Buckeye" appears in neither stream.** Origin unknown. Surfaced, not explained.
- **Whether `89d61f96` existed before 2026-08-21 00:39.** No earlier copy was found; **absence at these paths is not proof of non-existence.** `[P]`
- **Whether any downstream artifact consumed a citation against the wrong stream.** Not measured — outside the scope set.
- **`c13df1f4`'s own origin.** Its two parent projects `7f243ddc` and `91488774` are named by no governed artifact. **The stream the citations came from has no custody record at all** — which is the same failure class as `191/191`, the ETC producer and `GO-001-6`.

---

# 9 · ACCEPTANCE CRITERIA

| # | required demonstration | result |
|---|---|---|
| 1 | every candidate stream identified | **MET** — 8 distinct, 17 files, §1 |
| 2 | complete provenance for each | **MET for both candidates** — §2; six non-candidates excluded on cue count |
| 3 | custody chain documented | **MET** — complete for GT-2; **documented as absent for `c13df1f4`**, §2, §8 |
| 4 | governed consumers enumerated | **MET** — 19 binding vs 0, §3, §6 |
| 5 | downstream impact measured | **MET** — both directions, §6 |
| 6 | recommendation supported solely by repository evidence | **MET** — every claim cites a measurement at `2b7f055` or on the volume |
| 7 | every inference distinguished from observed fact | **MET** — `[E]` evidenced · `[P]` projection · `[O]` open, throughout |

---

# 10 · NO DETERMINATION IS MADE

**Nothing was rewritten, collapsed, migrated, re-pointed, implemented or inferred.** No caption stream was declared authoritative. **The determination is the Chairman's.**

**The standard he set is the one applied:** *the platform does not choose the most likely answer; it chooses the answer the evidence can support — or it refuses to choose.* **On the stream, the evidence supports an answer and this review says so. On the remediation, it does not, and this review refuses.**

---

```
CF-001 EVIDENCE REVIEW                READ-ONLY

Streams censused                      8 distinct  ·  17 files
Credible candidates                   2
Five criteria                         89d61f96 favoured 5 of 5
Governed bindings                     89d61f96: 19   ·   c13df1f4: 0
FCPXML pairing to picture lock        89d61f96 only
Content relationship                  two transcriptions, ~50% wording divergence
Registry names surviving GT-2         14 of 15   ·   R23 "Slow-mo" absent

Outcome A   partially supported       Outcome B   not supported
Outcome C   supported for remediation Outcome D   supported for the stream

Determination made                    NONE
Registries modified                   NONE       Commits   NONE
```

---

*Prepared under Executive direction. Custody: `MACHINE`. Authority: NONE. No caption stream, registry, citation, script, artifact or specification was modified; no stream was declared authoritative; no citation was re-pointed; and no commit was made.*
