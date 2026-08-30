# CF-001 — CITATION PROVENANCE CONFLICT

**Raised:** Platform Architect, during EDR-001 follow-up measurement · **For:** Executive Producer / Chairman
**Priority: CRITICAL** · **Custody:** `MACHINE` · **Authority:** NONE
**Mode:** READ-ONLY. Nothing modified, nothing committed, no determination made.
**Occasion:** measuring the `G-1` time tolerance for `ECR-003A`, as the Chairman proposed.

> ## THE 91 GOVERNED CITATIONS DO NOT RESOLVE AGAINST THE STREAM THEY DECLARE
>
> `RIDER_REGISTRY.yaml` declares its source as **GT-2 `89d61f96…`**.
> Measured, the citations resolve against **`Part 2 SRT` `c13df1f4…`** — a different file.
>
> **`R-1` is not a hypothetical risk. It has already occurred, and nothing detected it.**

---

# 1 · HOW THIS SURFACED

The Chairman directed that `G-1` — the undefined time tolerance — be resolved before implementing `ECR-003`. **Measuring the tolerance required resolving each citation's index against the declared stream and comparing to its recorded timecode.** The expected result was a tight distribution around zero, from which a tolerance could be specified.

**The distribution was not tight.**

```
offset = cue_start(GT-2) − cited timecode,  n = 82 compound citations

  min  −6.834 s      max  +43.250 s      mean  +15.749 s      median  +16.479 s
  within ±2 s:  5 of 82
```

A tolerance cannot be specified for a 50-second spread. **The premise was wrong, not the measurement.**

---

# 2 · THE MEASUREMENT

Every candidate caption stream on the volume, tested against the same 82 compound citations.

| stream | cues | resolvable | truncation-consistent | within ±2 s | median offset | IQR |
|---|---|---|---|---|---|---|
| **GT-2 `89d61f96`** — *declared source* | 2,291 | 82 | **0** | **5** | **+16.479 s** | 18.114 |
| **`Part 2 SRT` `c13df1f4`** | 2,290 | 82 | **47** | **80** | **+0.125 s** | **1.021** |
| analysis-cut `2a16dd70` | 2,036 | 76 | 0 | 0 | +41.979 s | 68.771 |
| PARENT `80a8ed25` | 5,664 | 82 | 0 | 0 | −693.312 s | 1215.677 |

**`c13df1f4` matches. Nothing else is close.** Median offset **+0.125 s**, IQR **1.021 s**, **80 of 82 within ±2 s**. `[E]`

---

# 3 · CONFIRMED BY TEXT — FOUR FOR FOUR

Offsets could in principle be a timing artefact. **Text cannot.** Each citation names a person; the cue it points at either says that name or does not.

| registry entry | cites | **`c13df1f4` #N** | GT-2 `89d61f96` #N |
|---|---|---|---|
| `R01` **Clutch** — *road captain, 9th roundup* | `#31 01:51` | **`"Clutch."`** ✓ | `"We're gonna have some good cigars."` ✗ |
| `R02` **Hollywood** — *president [org UNCONF]* | `#46 02:16` | **`"Hey, my name is Hollywood."`** ✓ | `"I serve as the vice president."` ✗ |
| `R03` **Mark Tillman** — *general president, 20+ yrs* | `#60 02:45` | **`"My name is Mark Tillman."`** ✓ | `"I'm gonna make it happen."` ✗ |
| `R05` **Rose** — *06 Riders* | `#95 04:08` | **`"Rose?"`** ✓ | `"What's your name?"` ✗ |

**Four tested. Four match `c13df1f4`. Four fail GT-2.** `[E]`

**This is not a tolerance question, an off-by-one, or a rounding convention. The registries cite a different file than the one they name.**

---

# 4 · WHY NOTHING CAUGHT IT

The two streams differ by **one cue** — 2,291 against 2,290 — and diverge from **index 7**:

```
index 7   GT-2 `89d61f96`   29.125 s   "go, go, go, I said,"
          Part 2 SRT        32.500 s   <font color="#ffffff">Fuck that, fully loade…
```

**Every index in both files resolves.** Cite `#60` against either and you get a cue. One of them is Mark Tillman introducing himself; the other is an unrelated line 2.75 seconds earlier. **No bounds check fires. No parser errors. No guard exists.**

This is precisely the mechanism the repository's own dependency inventory named:

> *"A wrong timecode is caught by a bounds check. **A wrong cue index is caught by nothing. It always resolves, it never errors**, and the result is a confident misattribution of a quote or a rider to a person who did not say it."*

**The two files are also distinguishable on sight, and that distinction was available the whole time.** `c13df1f4` carries `<font color="#ffffff">` markup; GT-2 is plain text. **No instrument was looking.**

---

# 5 · WHAT IS AND IS NOT ESTABLISHED

## Established `[E]`

- The 82 compound citations resolve against `c13df1f4`, by timing and by text.
- `RIDER_REGISTRY.yaml` line 4 declares `source: canonical SRT GT-2 (founding extraction of record 2026-08-20)`.
- `AR2-0822.context.json` declares the governed stream as `sha.srt 89d61f96…`, `srt.cues 2291`.
- The declared stream and the actual stream are different files.

## NOT established — and these matter `[O]`

- **Which stream is *correct*.** It is possible the registries are right and the context declaration is wrong; possible the reverse; possible both were true at different moments on 2026-08-20. **This review does not adjudicate that and must not.**
- **The status of the 9 citations without timecodes.** They cannot be tested by this method at all. **They may or may not share the same provenance**, and there is no way to tell from the record.
- **Whether any downstream artifact consumed a citation against the wrong stream.** Not measured here.
- **Whether the registry content is wrong.** **It probably is not.** The names, affiliations and quotes were extracted *from* `c13df1f4` and are internally consistent with it. **The defect is in the declared provenance, not necessarily in the facts.** That distinction is important and should not be lost: this is a labelling failure, and the extraction may be entirely sound.

---

# 6 · CONSEQUENCES FOR WORK IN FLIGHT

| instrument | effect |
|---|---|
| **`CIA-001` §1** | *Current target: GT-2* is **wrong** for all 91 rows → **ERRATUM 2 issued** |
| **`CIA-001` §0 conclusion** | **UNCHANGED and now stronger.** The collapse rule targets PARENT `80a8ed25`. The citations target `c13df1f4` — censused at 39 duplicate runs, 12.2 % abutting, 0 zero-length: **it does not carry the defect either.** *Zero of 91 affected* still holds |
| **`ED-004` readiness** | **UNCHANGED.** READY WITH CONDITIONS |
| **`ECR-003` `G-2`** | **Upgraded from a gap to a defect.** Stream binding was *unspecified* for three registries and **specified incorrectly for the fourth** |
| **`ECR-003` `G-1`** | **Cannot be resolved until `CF-001` is dispositioned.** Against `c13df1f4` the distribution is tight and a tolerance is specifiable; against GT-2 it is meaningless. **The tolerance depends on which stream the Executive declares authoritative** |
| **`ECR-003A`** | **The Chairman's sequencing was correct and this is the evidence for it.** Implementing `ECR-003` against the declared stream would have returned `FAILED` on ~77 of 82 citations and the failure would have been read as a citation defect rather than a provenance defect |

---

# 7 · WHAT THIS DOES NOT AUTHORIZE

**Nothing.** No registry was modified. No citation was re-pointed. No stream was re-declared. No validator was built or run beyond the measurement reported here, which resolved indices to compare them and adjudicated nothing.

**The disposition of `CF-001` is an Executive determination.** The available dispositions are visible from the evidence and are listed without preference:

- the registries' declared source is corrected to `c13df1f4`;
- the citations are re-pointed to GT-2 — **which would change the text every citation resolves to**;
- both streams are declared, with each registry bound to its own by hash;
- the conflict is held open and recorded while the question is investigated further.

**The platform will not choose.** Under `NO SILENT RECOVERY` and `EPR-001 §2.3` this is recorded as an explicit unresolved conflict.

---

```
CONFLICT                  CF-001
class                     declared provenance ≠ actual provenance
population                91 citations · 4 registries · 82 testable, 9 untestable
declared stream           GT-2                89d61f96…   2,291 cues
measured stream           Part 2 SRT          c13df1f4…   2,290 cues
evidence                  timing: median +0.125 s vs +16.479 s
                          text:   4 of 4 name matches vs 0 of 4
divergence begins         index 7
detected by               nothing — first observed 2026-08-30 during G-1 measurement

DISPOSITION               UNRESOLVED — REQUIRES EXECUTIVE DETERMINATION
silent reconciliation     PROHIBITED and not performed
registries modified       NONE
commits                   NONE
```

---

*Raised under EDR-001 follow-up. Custody: MACHINE. Authority: NONE. No registry, citation, caption stream, runtime component or source file was modified. No commit was made. No determination is made, and the correct stream is not asserted.*
