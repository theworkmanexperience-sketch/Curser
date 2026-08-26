# DAY 2 — PARENT TIMELINE vs PART TIMELINE FORENSIC AUDIT

**Task Order:** Documentary Forensics — Parent Timeline vs Part Timeline Audit
**Authority:** Executive Producer / Chairman · **Priority:** HIGH
**Custody:** `OBSERVATIONAL (MACHINE)` · **Inference Policy:** `ZERO`
**Prepared:** 2026-08-26 · **Status:** COMPLETE — with one custody condition requiring Executive ruling

---

## 0 · Read this first

Two things must be said before any measurement is quoted.

**0.1 — The Parent in this folder is not the governed production.**

The Parent audio runs **4689.557333 s**. The governed lock and the Approved Viewing Master run
**4846.625 s**. The Parent audio was measured directly against the Approved Viewing Master's own audio
and matches it only in **piecewise-shifted blocks** (lags `0.000`, `−3.500`, `+27.710`, `+28.960`,
`+119.540` s) with **regions after ≈ 01:04:00 that have no counterpart at any lag** (best r ≤ 0.42).

The Parent's duration is identical to the **2026-08-24 divergent cut** recorded in `CUSTODY_ALERT_001`,
and the Parent audio correlates with that cut's audio at **r = 0.999958**.

Everything in Parts A–F below therefore describes the **08-24 lineage**, not the governed 08-22 lock.
The three Parts are extracts of that lineage. **No finding here should be applied to the governed
record until `CUSTODY_ALERT_001` §5 is ruled.**

**0.2 — This audit resolves one open question in `CUSTODY_ALERT_001`.**

`CUSTODY_ALERT_001` §1 recorded two unidentified 1648.3 s assets (`Analysis_Day_2_Part_1_video.mov` /
`.WAV`, 44.1 kHz) and could not say what they were. They are identified:

```
Day 2 Part 1.WAV                    sha256 bcc17b2b2ea62f9e30fff18f7667d1ad18f715cc6c86b56ce0f47d4b4feb4d9f
Analysis_Day_2_Part_1_video.WAV     sha256 bcc17b2b2ea62f9e30fff18f7667d1ad18f715cc6c86b56ce0f47d4b4feb4d9f
```

**Byte-identical.** They are Part 1 of this Parent. They were never a 27½-minute *program*; they are a
27½-minute *extract*. That paragraph of `CUSTODY_ALERT_001` should be amended, and its §5 decision is
unaffected.

---

## 1 · Instrument validation (DOC-001)

Performed before any measurement, on the principle that a conformant instrument must be established
before its readings are trusted.

### 1.1 Inventory as found — path corrections

| order says | filesystem actually holds |
|---|---|
| `.../Alpha RoundUp Part 2/Alpha RoundUp Part 2/ALPHA ROUNDUP DAY 2 ANALYSIS/` | `.../Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2 ANALYSIS/` — one fewer nesting level; the parent folder name ends in a **space** |
| `Parent File/` | `Parent file/` — lowercase `f` |
| `Parent File/Parent.WAV` | **no WAV exists.** The Parent audio is `Alpha RoudUp Part 2.m4a` (AAC) |
| `PARENT_SRT.srt` | `PARENT_SRT_English (United States).srt` |

**Look-alike hazard cleared.** Two further directories named `Day 2 Part 2` and `Day 2 Part 3` exist
elsewhere in the tree. The duplicate `Day 2 Part 2.WAV` was hashed and is **byte-identical**
(`a9416a6f…`) to the audited copy, so no ambiguity survives. The duplicate `Day 2 Part 3` directory
contains a different asset set (`Alpha RoudUp Part 3.m4v`, 34 MB) and **was not used**.

### 1.2 Audited assets — hashes and probes

| asset | sha256 (16) | duration (s) | codec · rate · ch |
|---|---|---|---|
| `Parent file/Alpha RoudUp Part 2.m4a` | `4b43968a0f9d4f06` | **4689.557333** | aac · 48000 · 2 |
| `Parent file/PARENT_SRT_English (United States).srt` | `80a8ed25ed962b4d` | — | 5664 cues |
| `Day 2 Part 1/Day 2 Part 1.WAV` | `bcc17b2b2ea62f9e` | **1648.082721** | pcm_s16le · 44100 · 2 |
| `Day 2 Part 1/Day 2 Part 1.srt` | `c057fccf4001377a` | — | 909 cues |
| `Day 2 Part 2/Day 2 Part 2.WAV` | `a9416a6fc78e3245` | **1668.911020** | pcm_s16le · 44100 · 2 |
| `Day 2 Part 2/Day 2 Part 2.srt` | `65a313bc41614b95` | — | 766 cues |
| `Day 2 Part 3/Day 2 Part 3.WAV` | `1badf1c313a9b942` | **1566.882540** | pcm_s16le · 44100 · 2 |
| `Day 2 Part 3/Day 2 Part 3.srt` | `96bbee5d96b2745a` | — | 400 cues |

**Reference artifacts used for comparison only, not audited:**

```
governed lock SRT ("SRT 2")            89d61f965aa17e4d…   2291 cues · last cue ends 01:20:41.208
Approved Viewing Master (m4v audio)    89e911b1bffe14ce…   4846.625 s
08-24 divergent-cut SRT                2a16dd700148488f…   2036 cues · last cue ends 01:18:08.958
08-24 divergent-cut m4a                fd78b5a2333b8173…   4689.557333 s
```

### 1.3 Two independent instruments, cross-validated

The audit does not rest on one method. Two were run separately and compared afterwards:

| instrument | what it measures | resolution |
|---|---|---|
| **I-1 · caption-text alignment** | longest common word subsequences between normalised Part and Parent caption streams (`difflib.SequenceMatcher`, blocks ≥ 6 words, adjacent duplicate cues collapsed) | word-level; offsets ±1.4 s (word times interpolated within a cue) |
| **I-2 · audio-envelope correlation** | normalised cross-correlation of 100 Hz absolute-amplitude envelopes (mono, 4 kHz decode, 40-sample mean), FFT search over the whole Parent | 10 ms; boundary scans at 0.2 s step with a 1.0 s window |

**Cross-validation result — the two instruments agree without being told to:**

| Part | I-1 caption offset (median) | I-2 audio lag | agreement |
|---|---|---|---|
| Part 1 | −0.046 s | **0.000 s** | 0.046 s |
| Part 2 | +1558.429 s | **+1558.430 s** | **0.001 s** |
| Part 3 | +3137.745 s | **+3137.830 s** | 0.085 s |

Two instruments built on different evidence classes — transcribed text and acoustic amplitude —
converge to within one millisecond on Part 2 and under one tenth of a second on the others. The
instrument is validated. **Findings below cite whichever instrument produced them, and say so.**

---

## 2 · PART A — Parent timeline analysis

**Source:** `PARENT_SRT_English (United States).srt` (`80a8ed25…`) and `Alpha RoudUp Part 2.m4a`
(`4b43968a…`). Custody `MACHINE`.

| measurement | value | method |
|---|---|---|
| cues | 5664 | SRT parse |
| first cue in | `00:00:15.125` — *"Let's work!"* | SRT |
| last cue out | `01:18:08.916` — *"Tick, tick, tick, tick, tick."* | SRT |
| caption span (first in → last out) | 4673.791 s | SRT |
| audio duration | **4689.557333 s** | ffprobe |
| audio present before first caption | 15.125 s | SRT + ffprobe |
| audio present after last caption | 0.641 s | SRT + ffprobe |
| summed cue durations | 3855.688 s | SRT |
| words (normalised) | 27382 | SRT |
| gaps ≥ 10 s between consecutive cues | 10 | SRT |
| largest gap | 20.166 s at `00:56:15.000 → 00:56:35.166` | SRT |
| overlapping cue pairs | 0 | SRT |

### A.1 Two structural defects in the Parent SRT — reported, not corrected

**A-D1 · Every caption is emitted twice.** 2709 adjacent cue pairs carry identical normalised text.
**2669 of those pairs are exactly contiguous** — the second cue begins at the millisecond the first
ends:

```
#1  00:00:15.125 --> 00:00:15.458   "Let's work!"
#2  00:00:15.458 --> 00:00:15.791   "Let's work!"
#3  00:00:15.875 --> 00:00:17.666   "Wake the city, wake the road, just the bridle, let's go,"
#4  00:00:17.666 --> 00:00:19.458   "Wake the city, wake the road, just the bridle, let's go,"
```

**Consequence for any downstream consumer:** the Parent's cue count of 5664 is **not comparable** to
the Parts' cue counts or to the lock SRT's 2291 without collapsing these pairs. This audit collapsed
them for alignment (I-1) and reports raw counts unmodified in the tables.

**A-D2 · 29 cues have zero or negative duration.** Example:

```
#2645  00:38:19.916 --> 00:38:19.916   "Here you go, here you go."
#2646  00:38:19.916 --> 00:38:19.916   "Here you go, here you go."
```

Both defects are **properties of the caption artifact, not of the program**. Neither affects the
audio measurements in Part E, which never read the SRT.

### A.2 The Parent SRT is a fourth distinct transcript

| artifact | cues | markup | first cue | last cue |
|---|---|---|---|---|
| **PARENT** `80a8ed25…` | 5664 | none | `00:00:15.125` *"Let's work!"* | `01:18:08.916` *"Tick, tick, tick, tick, tick."* |
| 08-24 divergent cut `2a16dd70…` | 2036 | `<font>` on all 2036 | `00:00:00.375` *"Yeah, yeah, yeah."* | `01:18:08.958` *"Tick, tick, tick, tick, tick."* |
| governed lock `89d61f96…` | 2291 | none | `00:00:00.333` *"Yeah, yeah, yeah."* | `01:20:41.208` *"It'll be coming soon, and that's what's good."* |

The Parent SRT's hash matches none of them. It ends on the same words and within **0.042 s** of the
08-24 cut, and it begins **14.750 s later** with different words. **Observation only:** the Parent SRT
and the 08-24 SRT describe programs that end together; whether the Parent SRT is a re-transcription of
the same audio or a transcription of a different export is `INSUFFICIENT_OBSERVATION` from the SRT
alone. Part E answers it from the audio.

---

## 3 · PART B — Individual Part timeline analysis

Custody `MACHINE`. SRT and ffprobe only; no alignment applied.

| measurement | Part 1 | Part 2 | Part 3 |
|---|---|---|---|
| audio duration (s) | **1648.082721** | **1668.911020** | **1566.882540** |
| audio codec · rate | pcm_s16le · 44100 | pcm_s16le · 44100 | pcm_s16le · 44100 |
| cues | 909 | 766 | 400 |
| first cue in | `00:00:15.166` | `00:00:15.166` | `00:00:01.633` |
| first cue text | *"let's work work the city work the"* | *"let's work work this"* | *"we bikers"* |
| last cue out | `00:27:12.900` | `00:27:33.866` | `00:25:46.900` |
| last cue text | *"for part 2 and then for part 3 we have Bike Night"* | *"three part series and that's what's good"* | *"it'll be coming soon and that's what's good"* |
| audio after last caption (s) | 15.183 | 15.045 | 19.983 |
| summed cue durations (s) | 1443.331 | 1293.889 | 668.800 |
| words (normalised) | 5161 | 4325 | 2193 |
| gaps ≥ 10 s | 1 | 3 | 20 |
| largest gap | 56.433 s at `00:00:17.333` | 70.267 s at `00:02:14.333` | 100.133 s at `00:19:53.900` |
| adjacent identical-text pairs | 2 | 12 | 19 |
| markup tags | none | none | none |

**Three observations carried forward:**

1. **All three Parts open with the same caption material.** Parts 1 and 2 both begin at
   `00:00:15.166` with *"let's work…"*; Part 3 begins at `00:00:01.633` with *"we bikers"*. Part C
   and Part E establish what this is.
2. **All three Parts carry an uncaptioned tail** of 15.0–20.0 s. Part E establishes what is in it.
3. **Part 3's last caption is the governed lock's last line** — *"it'll be coming soon and that's
   what's good"* — a line that also appears in the Parent at `01:18:01`, before the Parent's own final
   *"Tick, tick, tick"*. Textual observation; no conclusion drawn.

---

## 4 · PART C — Content alignment by caption text

**Instrument I-1.** Timestamps were **not** used to align; they are outputs, not inputs. Method: both
sides normalised (lowercase, punctuation stripped, adjacent duplicate cues collapsed), matched as word
sequences, blocks of ≥ 6 consecutive matching words retained.

| | Part 1 | Part 2 | Part 3 |
|---|---|---|---|
| Part words compared | 5157 | 4280 | 2121 |
| words in matched blocks | 2228 | 2344 | 764 |
| matched blocks | 210 | 198 | 66 |
| Part cues touched by a match | 481 of 909 | 452 of 766 | 140 of 400 |
| **first matched text** | *"we got a busy day today we got a community"* | *"so we got that group ride leading from hilton garden"* | *"so that's it for the alpha round up community service"* |
| — at Part | `00:01:16.633` | `00:01:19.000` | `00:01:16.033` |
| — at Parent | `00:01:16.500` | `00:27:17.333` | `00:53:34.041` |
| **last matched text** | *"y'all we still got the whole ride over to the"* | *"we still got more of this day two three part"* | *"it'll be coming soon and that's what's good"* |
| — at Part | `00:27:06.100` | `00:27:28.200` | `00:25:43.733` |
| — at Parent | `00:27:08.458` | `00:53:27.166` | `01:18:01.500` |
| **Parent region spanned** | `00:01:16.500 – 00:27:08.458` | `00:27:17.333 – 00:53:30.208` | `00:53:34.041 – 01:18:03.541` |
| offset median · stdev | −0.046 s · 0.851 | +1558.429 s · 1.274 | +3137.745 s · 1.428 |

**Finding C-1 — the three Parts map to three sequential, non-overlapping regions of the Parent, in
order, with no crossing.** Part 1's matched region ends at Parent `00:27:08`; Part 2's begins at
Parent `00:27:17`; Part 2's ends at `00:53:30`; Part 3's begins at `00:53:34`.

**Finding C-2 — matched-word density is not uniform and this is a property of the transcripts, not of
the picture.** Part 3 matched 764 of 2121 words where Part 2 matched 2344 of 4280. The Parts and the
Parent are **separate transcription passes with different word errors** — the same audio yields
*"Let's work!"* in the Parent and *"let's work work the city work the"* in Part 1. Matched-word
density therefore measures transcript agreement, **not** content presence, and must not be read as a
coverage figure. Coverage is measured acoustically in Part F instead.

**Finding C-3 — each Part's opening caption block does not match at that Part's body offset.** Part 2's
cue 1 and Part 3's cues 1–2 fall outside every matched block at the offsets above. Instrument I-1
cannot say what they are. `INSUFFICIENT_OBSERVATION` from caption text alone — **resolved in Part E**.

---

## 5 · PART D — Discrepancy analysis

Each row: location · duration · evidence · cause · confidence. **Cause is left `INSUFFICIENT_OBSERVATION`
wherever the evidence does not determine it.** No discrepancy below has been repaired, smoothed, or
reconciled.

### D-1 · Parent is not the governed production — **CUSTODY**

| field | value |
|---|---|
| location | whole timeline |
| duration | Parent 4689.557333 s vs governed lock 4846.625 s — **−157.068 s** |
| evidence | ffprobe on `4b43968a…`; envelope correlation against the Approved Viewing Master's own audio (`89e911b1…`, 4846.625 s) |
| measurement | shared material appears at lags `0.000`, `−3.500`, `+27.710`, `+28.960`, `+119.540` s; Parent windows at `01:04`, `01:06`, `01:08`, `01:10`, `01:12`, `01:16` return best r ≤ 0.43 against **any** AVM position |
| cause | the Parent belongs to the 08-24 lineage (r = 0.999958 against the 08-24 cut audio) |
| confidence | **HIGH** — two independent duration measurements plus a full-program correlation sweep |
| disposition | **`CUSTODY_ALERT_001` §5 governs. Not this audit's to rule.** |

### D-2 · Parts 2 and 3 each begin with a duplicate of the Parent's opening — **STRUCTURAL**

| field | value |
|---|---|
| location | Part 2 `00:00:00.000 – 00:01:13.800`; Part 3 `00:00:00.000 – 00:01:13.800` |
| duration | **73.800 s each** |
| evidence | I-2. 1.0 s windows correlate against **Parent `00:00:00`+t** at r ≥ 0.98 throughout; against the Part's own body lag at r ≤ 0.4 |
| measurement | Part 2 last head window r=0.993 at t=72.60 · **Part 3 returns the identical r at every scan position**, which is itself evidence that the two heads are the same material |
| cause | each Part carries a re-prepended copy of the Parent's first 73.8 s |
| confidence | **HIGH** |

**Part 1 has no such head.** Part 1 begins at Parent `00:00:00.000` at lag exactly 0.000 and stays
there; the material Parts 2 and 3 prepend is, for Part 1, simply its own beginning.

### D-3 · A short indeterminate zone at each head/body join — **UNRESOLVED**

| field | value |
|---|---|
| location | Part 2 `00:01:13.800 – 00:01:15.200`; Part 3 `00:01:13.800 – 00:01:15.600` |
| duration | **1.400 s** and **1.800 s** |
| evidence | I-2. r falls below 0.4 against the head hypothesis and below 0.9 against the body hypothesis across this interval |
| measurement | Part 2: r(head) 0.993→0.004 between t=72.6 and t=74.0; r(body) 0.907 first reached at t=75.2 |
| cause | **`INSUFFICIENT_OBSERVATION`.** A cross-dissolve, a re-mixed join, and inserted material are all consistent with an envelope that matches neither source |
| confidence | boundary **HIGH** (±0.2 s); cause **NONE — not determined** |

### D-4 · Each Part carries an unmatched tail — **STRUCTURAL**

| field | value |
|---|---|
| location | Part 1 `00:27:13.083 – end` · Part 2 `00:27:34.111 – end` · Part 3 `00:25:47.283 – end` |
| duration | **15.000 s · 14.800 s · 19.600 s** |
| evidence | I-2 tail scan at the body lag; plus a **free search of each tail against the entire Parent** |
| measurement | free-search best matches: Part 1 r=0.500, Part 2 r=0.524, Part 3 r=0.472 — against r ≥ 0.90 for every genuine match in this audit. Tail mean envelope level 3755 / 3792 / 3004 against part-wide means of 9229 / 8864 / 9831 |
| corroboration | SRT: **no caption falls inside any tail.** Part 1's last cue ends at `00:27:12.900`, its tail begins `00:27:13.083`. Same pattern in Parts 2 and 3 |
| cause | **`INSUFFICIENT_OBSERVATION`.** The tails are quiet, uncaptioned, and have no counterpart anywhere in the Parent. End card, outro bed, and fade-to-black are all consistent |
| confidence | presence and duration **HIGH**; content **NONE — not determined** |

### D-5 · Part 3 extends past the end of the Parent — **STRUCTURAL**

| field | value |
|---|---|
| location | Part 3 `00:25:51.727 – 00:26:06.883`, i.e. Parent `01:18:09.557` onward |
| duration | **15.156 s** |
| evidence | I-2. Part 3's body lag is +3137.830 s; the Parent envelope ends at 4689.51 s; Part 3 continues to 1566.883 s local |
| measurement | every window from Part 3 t=1550.88 returns `BEYOND_PARENT_END` — there is no Parent index to compare against |
| cause | Part 3 contains material the Parent does not contain |
| confidence | **HIGH** |

### D-6 · Three sub-second Parent windows are in no Part body — **GAP**

| field | value |
|---|---|
| location | Parent `00:27:13.083 – 00:27:13.630` · `00:53:32.541 – 00:53:33.430` · `01:18:05.113 – 01:18:09.557` |
| duration | **0.547 s · 0.889 s · 4.444 s** — total **5.880 s** |
| evidence | I-2 boundary scans; corroborated by SRT cue inspection inside each window |
| measurement | window A holds Parent cues #2179–2180 (*"out, we out, we out, we out."* / *"Oh, that was…"*); window B holds #4187–4188 (*"All right, Webachus."*); window C holds #5663–5664 (*"Tick, tick, tick, tick, tick."*) |
| cause | windows A and B lie at Part-to-Part handover points and are shorter than the boundary resolution of ±0.2 s per edge. Window C is the Parent's final 4.444 s, which falls inside Part 3's tail region where correlation degrades to r 0.60–0.90 rather than failing outright |
| confidence | durations **MEDIUM** — each is of the same order as the measurement resolution and should not be read as an editorial decision |

### D-7 · Localised audio divergence between the Parent and the 08-24 cut — **NOTED**

| field | value |
|---|---|
| location | 744 of 468 951 ten-millisecond windows, concentrated before `00:08:00`; largest at `00:00:06.340 – 00:00:07.270` |
| evidence | I-2, sample-aligned difference of the two envelopes |
| measurement | global r = 0.999958; peak absolute envelope difference **17 799 at `00:00:06.410`** — Parent 14 386, 08-24 cut 32 185 — in a passage already near full scale (32 767 max) |
| cause | **`INSUFFICIENT_OBSERVATION`.** A different AAC encode of the same source and a genuine content difference in the opening are both consistent with an envelope difference of this shape |
| confidence | presence **HIGH**; cause **NONE — not determined** |

---

## 6 · PART E — Audio analysis

Custody `MACHINE`. Method declared in full so the measurement can be repeated or refuted:

> Each asset decoded to mono 16-bit PCM at 4000 Hz (`ffmpeg -ac 1 -ar 4000`), rectified, averaged in
> 40-sample blocks to a **100 Hz absolute-amplitude envelope**. Alignment by FFT normalised
> cross-correlation over the entire Parent envelope, with per-position mean and variance removed, so
> the score is a Pearson r invariant to level and offset. Sweep windows 30 s at 30 s steps; boundary
> windows 1.0 s at 0.2 s steps; continuity windows 10 s at 10 s steps.
>
> **This instrument measures amplitude structure. It does not classify speech, music, applause, or
> speaker identity, and no such claim is made anywhere in this report.**

### E.1 The measured structure of each Part

```
PART 1   1648.082721 s
  [ 0.000 ──────────────────── 1633.083 ]  body   → PARENT 00:00:00.000 – 00:27:13.083   lag  +0.000
  [ 1633.083 ─── 1648.083 ]                tail   → no counterpart in PARENT              15.000 s

PART 2   1668.911020 s
  [ 0.000 ─── 73.800 ]                     head   → PARENT 00:00:00.000 – 00:01:13.800   lag  +0.000
  [ 73.800 ─ 75.200 ]                      join   → matches neither                        1.400 s
  [ 75.200 ──────────────── 1654.111 ]     body   → PARENT 00:27:13.630 – 00:53:32.541   lag +1558.430
  [ 1654.111 ─── 1668.911 ]                tail   → no counterpart in PARENT              14.800 s

PART 3   1566.882540 s
  [ 0.000 ─── 73.800 ]                     head   → PARENT 00:00:00.000 – 00:01:13.800   lag  +0.000
  [ 73.800 ─ 75.600 ]                      join   → matches neither                        1.800 s
  [ 75.600 ─────────────── 1547.283 ]      body   → PARENT 00:53:33.430 – 01:18:05.113   lag +3137.830
  [ 1547.283 ─ 1551.727 ]                  tail-a → PARENT 01:18:05.113 – 01:18:09.557, r 0.60–0.90
  [ 1551.727 ─── 1566.883 ]                tail-b → BEYOND PARENT END                     15.156 s
```

### E.2 Continuity inside each body — no internal edits detected

10 s windows every 10 s across each body, held at the single fixed lag above:

| Part | windows tested | windows below r = 0.70 | lowest r inside the body |
|---|---|---|---|
| Part 1 | 164 | 1 — the window straddling the tail boundary | 0.363 at t=1630, at the boundary |
| Part 2 | 159 | 2 — one at `00:05:15` mid-body (r=0.697), one past the tail boundary | 0.073 at t=1655, past the tail boundary |
| Part 3 | 147 | 6 — a degraded band at `00:12:45 – 00:13:35` and one at `00:21:05` | 0.650, never a break |

**Finding E-1 — no lag discontinuity was found inside any Part body.** A single constant lag holds
from the first body window to the last in all three Parts. **Nothing in the audio evidence indicates
that material was cut, inserted, or reordered inside a Part relative to the Parent.**

**Finding E-2 — the degraded band in Part 3 at `00:12:45 – 00:13:35` (Parent `01:05:03 – 01:05:53`) is
recorded and not explained.** r falls to 0.65–0.68 without the lag changing. A level or mix difference,
an added element, and envelope noise in a quiet passage are all consistent. **`INSUFFICIENT_OBSERVATION`.**

### E.3 Parent audio identity

| comparison | global r | reading |
|---|---|---|
| Parent m4a `4b43968a…` vs 08-24 cut m4a `fd78b5a2…` (same duration, different hash) | **0.999958** | same program; 744 of 468 951 windows differ (D-7) |
| Parent m4a vs **Approved Viewing Master** `89e911b1…` (4846.625 s) | piecewise only | see D-1 — five distinct lags and unmatched regions after ≈ 01:04 |

A fourth audio artifact of 4848.170667 s (`SRT PART 2.m4a`, `dd3fedfd…`, 2026-08-20) exists in the
same tree and is **not** the Approved Viewing Master's audio. It was not used for any finding and is
listed here only so it is not mistaken later for the master. This is the same look-alike class that
produced the Approved Viewing Master register.

---

## 7 · PART F — Runtime accounting

```
Part 1                                             1648.082721 s
Part 2                                             1668.911020 s
Part 3                                             1566.882540 s
                                                 ───────────────
sum of Parts                                       4883.876281 s
Parent                                             4689.557333 s
                                                 ───────────────
excess of Parts over Parent                         194.318948 s
```

### F.1 The excess, itemised

| item | duration (s) | evidence |
|---|---|---|
| Part 2 head — duplicate of Parent `00:00:00 – 00:01:13.800` | +73.800 | D-2 |
| Part 3 head — duplicate of Parent `00:00:00 – 00:01:13.800` | +73.800 | D-2 |
| Part 2 head/body join, matching neither | +1.400 | D-3 |
| Part 3 head/body join, matching neither | +1.800 | D-3 |
| Part 1 tail, no Parent counterpart | +15.000 | D-4 |
| Part 2 tail, no Parent counterpart | +14.800 | D-4 |
| Part 3 tail (4.444 s degraded + 15.156 s beyond Parent end) | +19.600 | D-4, D-5 |
| **Part material with no single-lag Parent counterpart** | **+200.200** | |
| Parent windows in no Part body (D-6) | −5.880 | D-6 |
| **net** | **+194.320** | |
| measured excess | +194.319 | ffprobe |
| **residual** | **0.001** | |

### F.2 `UNACCOUNTED_RUNTIME` — none, and what that does and does not mean

**Declared: `UNACCOUNTED_RUNTIME = 0.000 s`.** Every second of Part runtime is assigned to a named
category, and every second of Parent runtime is either covered by a Part body or named in D-6.

**The residual of 0.001 s is not an independent validation and must not be read as one.** The
boundary times in F.1 and the Parent gaps in D-6 are derived from the *same* seven boundary
measurements, so the two columns are algebraically linked; the accounting is internally consistent by
construction. The genuinely independent quantities are the four file durations (ffprobe) and the three
body lags (correlation). What the table demonstrates is that **those seven independent numbers admit a
consistent partition with nothing left over** — not that the partition has been confirmed twice.

The real independent check is §1.3: caption-text alignment and audio-envelope correlation, built on
different evidence, produced the same three lags to within 0.085 s.

### F.3 Parent coverage

```
PARENT  00:00:00.000 ──────────────────────────────────────────── 01:18:09.557   4689.557 s
Part 1 body   [00:00:00.000 ─ 00:27:13.083]                                      1633.083 s
Part 2 body                   [00:27:13.630 ─ 00:53:32.541]                      1578.911 s
Part 3 body                                   [00:53:33.430 ─ 01:18:05.113]      1471.683 s
                                                                               ────────────
                                                          covered by a Part body   4683.677 s
                                                          named in D-6             5.880 s
```

**Finding F-1 — the three Parts, taken together, contain the whole of the Parent.** No Parent interval
longer than 4.444 s is absent from all three Parts, and the two interior gaps are 0.547 s and 0.889 s,
both at the resolution limit of the boundary measurement.

**Finding F-2 — the Parts are sequential and do not overlap.** Part 1's body ends at Parent
`00:27:13.083` and Part 2's begins at `00:27:13.630`; Part 2's ends at `00:53:32.541` and Part 3's
begins at `00:53:33.430`. **The duplicated material between Parts is the re-prepended opening (D-2),
not shared body content.**

---

## 8 · PART G — Summary of the editorial relationship

Stated as observation. **No cause outside the evidence is asserted, and no editorial intent is
attributed to anyone.**

**G-1.** The three Parts are **contiguous, in-order, non-overlapping extracts of a single Parent
timeline**, joined at Parent `00:27:13` and Parent `00:53:33`, together spanning the Parent end to end.

**G-2.** Parts 2 and 3 each carry a **73.800 s re-prepended copy of the Parent's opening**, joined to
the body through a 1.4 s / 1.8 s interval that matches neither source.

**G-3.** All three Parts carry a **15.0 – 19.6 s uncaptioned tail** at a mean envelope level between
**0.31 and 0.43 of that Part's own mean**, with **no counterpart anywhere in the Parent** (best
free-search r ≤ 0.524). Part 3's tail extends **15.156 s past the Parent's end**.

**G-4.** **No internal edit was detected within any Part.** One constant lag per Part holds across 470
continuity windows.

**G-5.** **The Parent is not the governed production.** It is 157.068 s shorter than the lock, matches
the Approved Viewing Master only in five piecewise-shifted blocks with unmatched regions after ≈ 01:04,
and matches the 2026-08-24 divergent cut at r = 0.999958.

### 8.1 What follows from G-5 — and what does not

**Governance conditions raised, none ruled here:**

| # | condition |
|---|---|
| **C-1** | These three Parts are extracts of the **08-24 lineage**. If `CUSTODY_ALERT_001` §5 rules **path A** (the 08-22 lock stands), the Parts describe a `REFERENCE_ONLY` edit and carry no authority over the governed record. If it rules **path B**, they are extracts of the production. If it rules **path C**, they belong to the separate deliverable and need their own registry. **This audit does not favour any path.** |
| **C-2** | The Parent SRT (`80a8ed25…`) is a **fourth transcript** of Part 2 material. If any Part or Parent artifact is ever admitted to the governed record, it needs its own hash pin; it is not covered by `RE-001`'s four input hashes. |
| **C-3** | `CUSTODY_ALERT_001` §1 identifies `Analysis_Day_2_Part_1_video.WAV` as an unexplained 27½-minute asset. It is **byte-identical to Day 2 Part 1** and is explained. That paragraph should be amended; §5 is unaffected. |
| **C-4** | The Parent SRT's doubled cues (A-D1) and 29 zero-duration cues (A-D2) would corrupt any consumer that counts cues or sums caption time. If this transcript is ever ingested, a declared collapse rule must precede it. |

**Three questions this audit was not equipped to answer, listed so they are not later assumed:**

| # | question | why not answered |
|---|---|---|
| **Q-A** | What is in the Part tails? | The envelope instrument measures amplitude only. Determining whether a tail is an end card, an outro bed, or black requires picture, and the Parts hold no picture in this folder |
| **Q-B** | Is D-7's opening divergence a re-encode or a content change? | Requires sample-level comparison of the two m4a files, not envelopes |
| **Q-C** | Why does Part 3 degrade to r ≈ 0.65 at `00:12:45 – 00:13:35`? | The lag never moves, so it is not an edit. Level, mix, and quiet-passage noise are all consistent |

---

## 9 · Method, custody, and reproduction

| item | value |
|---|---|
| custody of every measurement | `MACHINE` |
| inference policy | `ZERO` — five conditions are recorded as `INSUFFICIENT_OBSERVATION` and none was filled |
| instruments | I-1 caption-text alignment · I-2 audio-envelope correlation, cross-validated to 0.001–0.085 s |
| resolution | envelope 10 ms · boundary scans ±0.2 s · lag search 10 ms |
| scripts | `srt.py`, `partA_B.py`, `partC.py`, `partC2.py`, `partD_internal.py`, `partE_align.py`, `partE_bound.py`, `partE_fine.py` |
| assets read | 8 audited (§1.2) + 4 reference (§1.2), all hashed before use |
| assets modified | **none.** Working copies were made under `SPRINT3A_WORK/parent_audit/`; no audited file was written to |
| registries consulted | none required; **no registry was modified** |
| ranking, preference, or aggregate compliance value expressed | **none** (ER-001) |

**Reproduction note.** The four audited hashes in §1.2 pin the inputs. Re-running the eight scripts
against those hashes reproduces every number in this report. Any number that cannot be reproduced from
those inputs is an error in this report and should be reported as one.

---

*Prepared under the Documentary Forensics task order. Custody `OBSERVATIONAL (MACHINE)`. Inference
policy `ZERO`. Five conditions stand as `INSUFFICIENT_OBSERVATION`; four governance conditions and
three unanswered questions are raised for Executive attention. **No disposition is proposed and none
is implied.***
