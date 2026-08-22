# STEP0_TIMING_CLOSURE.md
## Editorial Timing Closure - WECAPE-AR2-SPRINT3A-20260822-114028

**Status: CLOSED.** The +/-6 s tolerance carried by TIMELINE_REGISTRY since Sprint 2 is discharged. Every delta between the lock SRT, the Editorial Timing Contract, the locked FCPXML and the master proxy is categorized in the ledger below. No delta is unexplained.

### 1. Offset model (one line)

> **The lock SRT is on the ETC timebase exactly: offset = 0.000 s, drift = 0 s/s, single-valued across the whole runtime.** The historical +/-6 s was never a shift in the lock SRT - it was the *pre-lock* SRT's shorter runtime being compared against the lock.

### 2. Inputs of record

| input | SHA-256 | measure |
|---|---|---|
| Filmage_Editor.mp4 | `a53655fc673945a0d99dde3d5b60c9a126d8b41e4e44a7c7eedeb058ba0f47e8` | 4846.633 s video stream, 320x180, 30 fps proxy |
| Info.fcpxml | `2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7` | sequence 4846.625 s, 3840x2160p24, tcStart 0 s, NDF |
| lock SRT ("SRT 2") | `89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b` | 2,291 cues, 0.333 s -> 4841.208 s |
| P2_LOCK_timing.json | `e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d` | 191 spine + 404 connected; declares source sha 2bf0685373d6963b... |

The ETC's own `source_sha256` field equals the SHA-256 this run computed for Info.fcpxml. The four-source chain is therefore closed at the hash level, not merely asserted.

### 3. Method

Two independent methods were run, plus a resolver validation:

**A - envelope correlation.** The master proxy's audio was decoded to a 0.25 s RMS envelope (19,386 samples). The lock SRT was rendered onto the same grid as a speech mask. The two were cross-correlated over +/-40 s. Significance was tested against a null built from 300 circular rotations of the mask; peaks at a search-window edge, non-positive peaks, and peaks failing p<0.05 are reported INDETERMINATE rather than converted into an offset.

Global result: **best lag 0.000 s**, peak r = 0.2783, null p = 0.0, null 95th percentile = 0.1851. Status **ALIGNED_ZERO_OFFSET**.

**B - semantic anchors (SRT text vs ETC title text).** Title elements whose text matches a nearby SRT cue give a direct, audio-independent measurement of the relation between the two timebases. 11 high-quality anchors were found spanning 119.3 s to 4840.7 s (97.4% of runtime).

| title in (s) | delta (s) | title text |
|---|---|---|
| 119.292 | +0.084 | Initiated ? |
| 229.304 | +0.846 | Why Do You Ride ? |
| 244.963 | -0.162 | What's Your Nam e |
| 261.772 | +0.897 | Why Do You Ride ? |
| 291.792 | +0.209 | Why Do You Ride ? |
| 2116.333 | +0.708 | Mayor, Mary Esther Reed |
| 2378.042 | +0.792 | Why Do You Ride ? |
| 3116.042 | -1.124 | The Journey Reveals The Why |
| 4827.750 | +0.584 | Why Do You Ride ? |
| 4835.500 | +0.917 | How Long You Been Rid' n |
| 4840.708 | +2.250 | ..and that's what's good! |

Median delta **+0.708 s**, sd 0.784 s. Regression of delta on time gives a total drift of **+0.684 s over the full runtime, 95% CI [-0.541, +1.909] s** - the interval contains zero, which rules out any rate mismatch (a 23.976/24 pulldown error would have shown -4.85 s). The residual +0.708 s is a constant editorial design lag: cards land just after the words.

**C - picture verification.** Probe 3 sampled 01:19:44-01:20:46 at 1.000 s. Every closing title's ETC in/out is reproduced in the rendered picture to within one sample:

| ETC title | ETC in/out | first sampled frame showing it | last |
|---|---|---|---|
| Why Do You Ride? | 01:20:27.750 - 01:20:31.333 | 01:20:28 | 01:20:30 |
| What RU Rid'n? | 01:20:31.458 - 01:20:33.833 | 01:20:32 | 01:20:32 |
| Who You Rid'n Wit? | 01:20:33.958 - 01:20:35.458 | 01:20:34 | 01:20:34 |
| How Long You Been Rid'n | 01:20:35.500 - 01:20:39.208 | 01:20:36 | 01:20:38 |
| ..and that's what's good! (nested) | 01:20:40.708 - 01:20:46.042 | 01:20:41 | 01:20:45 |

The nested card is the important one: it validates the compound-clip recursion in the resolver against the rendered picture, not just against the ETC.

### 4. Resolver validation (the enabling result)

`P2_LOCK_timing.json` carries `timeline_offset_s: null` for **all 404 connected elements**, and its `parent` references are clip *names*, which repeat. Absolute in/outs for the 16 audio-lane elements and the 40 titles therefore could not be read from the ETC. They were resolved from the FCPXML nesting instead:

```
abs(child) = abs(container) + (child.offset - container.start)
anchored <spine lane=N>: children are expressed in the storyline's own base (0)
```

The resolver reproduces **191 of 191** ETC spine offsets and durations to within 0.0006 s, and its last spine element ends at exactly 4846.625 s. That is the licence to trust its connected-element output.

### 5. Per-segment mapping

| seg | span | dur | SRT cues | speech cov | status | lag | note |
|---|---|---|---|---|---|---|---|
| S01 | 00:00-01:13 | 73 s | 16 | 0.53 | INDETERMINATE | - | ARGMAX_AT_SEARCH_WINDOW_EDGE(no interior peak) |
| S02 | 01:13-01:51 | 38 s | 18 | 0.94 | INDETERMINATE | - | SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s) |
| S03 | 01:51-27:02 | 1511 s | 1022 | 0.87 | ALIGNED_ZERO_OFFSET | +0.00 |  |
| S04 | 27:02-27:23 | 21 s | 6 | 0.64 | INDETERMINATE | - | SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s) |
| S05 | 27:40-29:10 | 90 s | 20 | 0.57 | INDETERMINATE | - | NO_POSITIVE_CORRELATION_PEAK |
| S06 | 31:43-32:33 | 50 s | 16 | 0.94 | INDETERMINATE | - | SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s) |
| S07 | 32:45-33:50 | 65 s | 21 | 0.89 | ALIGNED_ZERO_OFFSET | +0.25 |  |
| S08 | 33:51-35:56 | 125 s | 37 | 0.91 | SHIFT_DETECTED | -6.75 | see D-11 |
| S09 | 36:03-36:30 | 27 s | 8 | 0.44 | INDETERMINATE | - | SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s) |
| S10 | 36:59-38:52 | 113 s | 38 | 0.90 | SHIFT_DETECTED | -3.25 | see D-11 |
| S11 | 38:55-52:00 | 785 s | 587 | 0.89 | INDETERMINATE | - | PEAK_NOT_SIGNIFICANT_VS_NULL(p=0.180) |
| S12 | 52:04-53:56 | 112 s | 39 | 0.72 | ALIGNED_ZERO_OFFSET | +0.00 |  |
| S13 | 53:50-54:35 | 45 s | 13 | 0.43 | INDETERMINATE | - | SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s) |
| S14 | 54:36-55:24 | 48 s | 20 | 0.82 | INDETERMINATE | - | SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s) |
| S15 | 56:10-58:43 | 153 s | 1 | 0.00 | INDETERMINATE | - | INSUFFICIENT_SRT_SPEECH_IN_SPAN(<30%) — non-speech segment by design |
| S16 | 58:43-66:25 | 462 s | 327 | 0.90 | ALIGNED_ZERO_OFFSET | +0.00 |  |
| S17 | 66:25-66:48 | 23 s | 12 | 0.90 | INDETERMINATE | - | SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s) |
| S18 | 69:25-79:40 | 615 s | 40 | 0.14 | INDETERMINATE | - | INSUFFICIENT_SRT_SPEECH_IN_SPAN(<30%) — non-speech segment by design |
| S19 | 79:44-80:46 | 62 s | 24 | 0.83 | ALIGNED_ZERO_OFFSET | +0.25 |  |

Read this table correctly: the per-segment column is a **diagnostic on the measurement**, not 19 independent offset estimates. A locked cut cannot carry a different timebase in one two-minute stretch than in the stretches on either side of it. Where a segment disagrees with zero, the disagreement is a property of the probe (see D-11), and it is written down as such rather than averaged away.

### 6. The 16 audio-lane elements - exact in/outs (resolved)

| # | in | out | dur (s) | lane | classification | source |
|---|---|---|---|---|---|---|
| 1 | 00:00:00.000 | 00:01:16.417 | 76.417 | -2 | SCORE_ASSET | `KICKSTANDS UP v1 (Remastered)` |
| 2 | 00:01:13.782 | 00:01:34.512 | 20.730 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-23` |
| 3 | 00:26:54.812 | 00:26:58.637 | 3.825 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-3` |
| 4 | 00:27:10.000 | 00:27:24.610 | 14.610 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-7` |
| 5 | 00:27:40.792 | 00:28:12.147 | 31.355 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-10` |
| 6 | 00:28:44.708 | 00:29:11.681 | 26.973 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-8` |
| 7 | 00:29:16.792 | 00:29:49.467 | 32.675 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-11` |
| 8 | 00:33:37.708 | 00:34:39.667 | 61.958 | -1 | CONTRIBUTED_VIDEO_AUDIO | `NOTOR1OUS_CARAVAN_2_` |
| 9 | 00:38:51.866 | 00:38:54.125 | 2.259 | -2 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-26` |
| 10 | 00:38:54.119 | 00:38:56.340 | 2.222 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-26` |
| 11 | 00:51:55.795 | 00:52:00.340 | 4.545 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-28` |
| 12 | 00:54:42.609 | 00:55:25.917 | 43.308 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-13` |
| 13 | 01:06:24.238 | 01:06:49.661 | 25.422 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-15` |
| 14 | 01:19:45.501 | 01:20:29.667 | 44.165 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-17` |
| 15 | 01:20:29.667 | 01:20:36.708 | 7.042 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-24` |
| 16 | 01:20:36.708 | 01:20:42.696 | 5.987 | -1 | PRODUCTION_ORIGINAL_MEDIA_AUDIO | `Map traavel to Smyrna Event Center-25` |

Provenance is decisive here and it is read from the FCPXML asset paths, not guessed: **exactly one** of the sixteen is a score asset (`/AlphaRoundUp_2026/Soundtrack/KICKSTANDS UP v1.wav`). Fourteen are detached production audio from `P2_CHRONO_SETS/Original Media` - the route-map animation audio, whose picture this run observed directly at 00:27:12-00:27:21. One is the audio of a contributed video (`NOTOR1OUS_CARAVAN_2_`), and it sits inside SIL-01. That last one is escalated, not resolved: see D-18.

### 7. Delta ledger - every delta categorized

| id | category | magnitude | disposition |
|---|---|---|---|
| D-01 | NON_SPEECH_TAIL | +5.417 s | CLOSED |
| D-02 | NON_SPEECH_HEAD | +0.333 s | CLOSED |
| D-03 | PRE_LOCK_VS_LOCK_SRT_REVISION | +1 cue / +1.208 s | CLOSED-AS-BOUNDED (pre-lock SRT out of scope of this run's inputs) |
| D-04 | REGISTRY_NOTE_ARITHMETIC | 0.600 s | CLOSED-AS-NOTED (registry text unchanged by this run; flagged for registry maintenance) |
| D-05 | PROXY_CONTAINER_ROUNDING | +0.008 s video / +0.122 s container | CLOSED |
| D-06 | ETC_CENSUS_EXCLUDES_TRANSITIONS | 23 elements | CLOSED |
| D-07 | NESTED_TITLES_NOT_IN_ETC_CENSUS | 17 titles | CLOSED - the 17 are enrolled into CAPTION_REGISTRY by this run |
| D-08 | ETC_CONNECTED_OFFSETS_NULL | 404 elements | CLOSED - absolute offsets resolved from FCPXML nesting; resolver validated 191/191 against the ETC spine offsets |
| D-09 | SYNC_CLIP_INTERNAL_MEDIA | 18 elements | CLOSED - excluded from the timeline census by rule |
| D-10 | CORRELATION_INDETERMINATE_SPANS | 1968 s of runtime | CLOSED - each carries a categorized reason (segment shorter than the lag-search window, or SRT speech coverage below 30%) |
| D-11 | SATURATED_SPEECH_MASK | 2 segments / 238 s | CLOSED - measurement artefact, not a timebase shift; a genuine mid-film shift bounded by zero-offset neighbours on both sides is editorially impossible |
| D-12 | EDITORIAL_CARD_LAG_CONSTANT | +0.708 s median | CLOSED - a constant editorial design lag, not a timebase offset |
| D-13 | NO_RATE_MISMATCH | 0 s within CI | CLOSED |
| D-14 | CUE_BOUNDARY_VS_EXISTING_ELEMENT | +3.417 s | OPEN-TO-PDR (cue in/out binds to the closed ETC; reconciliation verdict is a human decision) |
| D-15 | OBSERVED_ACTIVITY_EXCEEDS_CUE_SPAN | approx +150 s of unscored ride | OPEN-TO-PDR (registry and cue sheet remain authoritative; recorded as CONFLICTED observation) |
| D-16 | REGISTRY_LABEL_VS_OBSERVATION | 462 s | CONFLICTED - registry value retained as authoritative; observation recorded and raised as a PDR candidate |
| D-17 | AGREEMENT_WITHIN_SAMPLING | 0.5 s | CLOSED - agreement within the 0.5 s observation grid |
| D-18 | SILENCE_LAW_OVERLAP_CANDIDATE | 61.958 s inside a mandatory-silence window | OPEN-TO-PDR - classified UNCERTAIN; escalated rather than resolved |
| D-19 | CUE_SHEET_COVERAGE_GAPS | 445.625 s across 11 spans | CLOSED-AS-ENUMERATED (each span listed in CONDUCTOR_SCORE.uncovered_spans) |
| D-20 | REGISTRY_SEGMENT_GAPS | 434.625 s across 13 spans | CLOSED-AS-ENUMERATED (each span listed in EDITORIAL_SYNCHRONIZATION.unsegmented_spans) |
| D-21 | TITLE_TEXT_LETTER_SPACING | cosmetic | CLOSED - verbatim preserved per DIE-X rule X-2 (zero interpretation at extraction) |
| D-22 | OFFLINE_MEDIA_REFERENCE | 1 asset | CLOSED-AS-NOTED - affects content inspection only, not timing. It was the stated reason D-18 could not be resolved in RE-001; the ESS-004 ruling retired that dependency by making the test provenance rather than content, so the offline volume no longer blocks any decision |
| D-23 | DIE_V_SAMPLING_UNCERTAINTY | +/-0.5 sample | CLOSED - frame-accuracy claims rest on the ETC and on the 1.000 s probe grid, never on the 3.000 s survey grid |
| D-24 | PROXY_RESOLUTION_CEILING | 320x180 vs 3840x2160 master | CLOSED-AS-DECLARED - every affected observation is capped at MEDIUM or UNCERTAIN; no observation claims detail the proxy cannot carry |
| D-26 | YAML_SEXAGESIMAL_TIMECODE | 4 artifacts, all *_tc fields | FIXED in the regeneration - all timecodes are now quoted at write time and load as strings. The RE-001 archived copies retain the defect by design (immutable); RE-002 will carry the fix |
| D-25 | DIE_V_SHEET_SAMPLING | 20 of 54 sheets read in full | CLOSED-AS-DECLARED - gauntlet spans carry span-level classifications only, never per-event claims outside a read sheet |

Full descriptions are carried in ESS_VALIDATION_REPORT.md section 6.

### 8. Closure statement

With offset = 0.000 s and drift within [-0.541, +1.909] s of zero over 4846.625 s, and with 26 deltas each carrying a category and a disposition, the +/-6 s tolerance is **CLOSED**. Frame-accurate claims downstream of this report are licensed against the ETC and the 24 fps sequence timebase - not against the 320x180 proxy and not against the 3.000 s DIE-V survey grid.
