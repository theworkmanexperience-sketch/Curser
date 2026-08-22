# ESS_VALIDATION_REPORT.md
## Sprint 3A Validation - WECAPE-AR2-SPRINT3A-20260822-114028

**Verdict: PASS with three CONFLICTED observations and two items escalated for human adjudication.** No delta is uncategorized. No music was generated. No biometric identification was performed. No inferred value was silently substituted for a missing one.

### 1. Four-source chain

| link | test | result |
|---|---|---|
| FCPXML -> ETC | ETC `source_sha256` vs computed SHA-256 of Info.fcpxml | **MATCH** `2bf0685373d6963bc151b982...` |
| FCPXML -> ETC | resolver reproduces ETC spine offsets and durations | **191 / 191** within 0.0006 s |
| FCPXML -> lock | last spine element out-point vs sequence duration | **4846.625 s = 4846.625 s** |
| SRT -> ETC | envelope correlation, null-tested | **offset 0.000 s**, p = 0.0 vs null |
| SRT -> FCPXML | 11 semantic title/cue anchors over 97.4% of runtime | median **+0.708 s** constant, drift CI contains 0 |
| ETC -> picture | 5 title in/outs vs rendered frames at 1.000 s | **5 / 5** within one sample |
| proxy -> lock | container duration vs sequence | 4846.633 s vs 4846.625 s (**D-05**) |

The chain is closed at the hash level in both directions: the ETC names the FCPXML hash this run computed, and the resolver built from that FCPXML reproduces the ETC's own numbers exactly. Neither artifact is being taken on trust.

### 2. Step 0 closure evidence

- Offset model: **0.000 s, single-valued, no drift.** Two independent methods agree; a third (picture verification) confirms at frame level.

- Drift bound: **+0.684 s over 4846.625 s, 95% CI [-0.541, +1.909] s.** Zero is inside the interval; a 23.976/24 rate error (-4.85 s) is far outside it.

- The +/-6 s tolerance is discharged. Its origin is identified: the *pre-lock* SRT ran to 01:20:40 against a 01:20:46.625 lock. The lock SRT itself was never shifted.

- Enabling result: the ETC publishes `timeline_offset_s: null` for all 404 connected elements, so the 16 audio elements and 40 titles had to be resolved from FCPXML nesting. The resolver earned the right to be believed by reproducing all 191 spine offsets first.

### 3. Probe results (fixture validation before registry custody)

| probe | window | expectation | result | what was actually observed |
|---|---|---|---|---|
| P1 | 00:27:40-00:29:10 | mass-ride / escort motion | **PASS** | staging-lot mount-up, column departure, two-abreast public-road formation, marked police vehicle and officer at an intersection at 00:29:06 |
| P2 | 00:52:04-00:53:49 | static crowd / ceremony | **PASS** | interior hall, podium with venue plate, US flag and standards, framed plaques presented and raised, line of recipients, wide seated banquet room |
| P3 | 01:19:44-end | riding + night | **PASS** | night formation riding, helmet POV, lit portico arrival, closing card run; five closing title in/outs reproduced in picture |

P3 did double duty. Because the closing cards are legible in the rendered frames, it is simultaneously the night/riding fixture and the frame-accuracy evidence for Step 0 - including for a title nested inside a compound clip, which is the case the resolver was most likely to get wrong.

### 4. Coverage reconciliation

**Events vs runtime**

| measure | value |
|---|---|
| runtime | 4846.625 s |
| DIE-V events emitted | 39 |
| instrument-derived events | 4 (illumination runs, 100% of runtime) |
| observation-derived events | 35 |
| survey frames extracted | 1616 at 3.000 s (100% of runtime) |
| contact sheets built / read in full | 54 / 20 |
| probe frames extracted | 258 at 1.000 s |
| explicit NOT_OBSERVED declarations | 5 |

**Sync rows vs spine**

| measure | value |
|---|---|
| ESS rows | 32 |
| registry segments covered | 19 of 19 |
| runtime inside a registry segment | 4418.000 s (91.2%) |
| runtime unsegmented | 434.625 s (9.0%) across 13 spans (D-20) |
| spine story elements | 191 (ETC) / 214 incl. transitions (FCPXML) (D-06) |

**Cues vs spine**

| measure | value |
|---|---|
| cues + silences scored | 15 |
| runtime under a cue or conducted silence | 4401.000 s (90.8%) |
| runtime uncovered | 445.625 s (9.2%) across 11 spans (D-19) |
| existing audio-lane elements reconciled | 16 of 16 |
| of which score assets | 1 |
| of which detached production audio | 14 |
| of which contributed-video audio | 1 (escalated) |
| caption elements enrolled | 57 (40 ETC-census + 17 newly enrolled) |

### 5. Conflict ledger

| id | registry value | observation | state | resolution |
|---|---|---|---|---|
| VCONF-01 | TIMELINE_REGISTRY S16 labelled `bike_night_arrivals` (00:58:43-01:06:25) | span is bright daylight; mean luma 130.7; sustained night onset measured at 01:06:24.5 | **CONFLICTED** | registry authoritative; PDR candidate |
| VCONF-02 | S05 / CUE-03 escort ride 00:27:40-00:29:10 (90 s) | mass ride observed continuously 00:28:15 to approx 00:33:00; escort presence to 00:31:48 | **CONFLICTED** | registry authoritative; PDR candidate |
| VCONF-03 | CAPTION_REGISTRY policy: rider lower-thirds at 75 first-cues | the lock contains zero rider lower-thirds; on-screen naming is reserved for civic speakers | **CONFLICTED** | policy line marked SUPERSEDED-BY-EVIDENCE; adding them stays a human decision |
| SLF-01 | SIL-01 is mandatory silence 00:31:43-00:38:52 | audio-lane element NOTOR1OUS_CARAVAN_2_ occupies 00:33:37.708-00:34:39.667 inside it | **UNCERTAIN** | escalated, not resolved - contributed-video audio, content undetermined, source media offline (D-18, D-22) |
| SLF-02 | SIL-01 framed as civic silence | the zone opens over continuous ride footage, not over speech | **OBSERVATION** | named for the conductor; no registry change |

Three conflicts, one escalation, one framing note. In every case the registry value stands and the observation is recorded beside it. That is the whole point of DIE-V being a module rather than an authority.

### 6. Delta ledger - full descriptions

Every measurable difference found anywhere in this run, with a category and a disposition. An uncategorized delta would be a failure of this sprint; there are none.

**D-01 - NON_SPEECH_TAIL** *(magnitude: +5.417 s)*  
Lock runtime 4846.625 s vs last lock-SRT cue end 4841.208 s. The tail is the closing card over the final shot; no speech exists to transcribe.  
*Disposition:* CLOSED

**D-02 - NON_SPEECH_HEAD** *(magnitude: +0.333 s)*  
First lock-SRT cue starts at 0.333 s, not 0.000 s.  
*Disposition:* CLOSED

**D-03 - PRE_LOCK_VS_LOCK_SRT_REVISION** *(magnitude: +1 cue / +1.208 s)*  
Founding fixture (WET-SPEC-DIE-001 App. A) records 2,290 cues ending 01:20:40; the lock SRT carries 2,291 cues ending 01:20:41.208. The pre-lock SRT is not among this run's four authoritative inputs, so the single added cue cannot be identified here.  
*Disposition:* CLOSED-AS-BOUNDED (pre-lock SRT out of scope of this run's inputs)

**D-04 - REGISTRY_NOTE_ARITHMETIC** *(magnitude: 0.600 s)*  
TIMELINE_REGISTRY.delta_note states the pre-lock/lock delta as +6.025 s. Lock runtime minus the fixture's stated 01:20:40 end is +6.625 s.  
*Disposition:* CLOSED-AS-NOTED (registry text unchanged by this run; flagged for registry maintenance)

**D-05 - PROXY_CONTAINER_ROUNDING** *(magnitude: +0.008 s video / +0.122 s container)*  
Filmage_Editor.mp4 video stream duration 4846.633 s and container duration 4846.747 s vs sequence 4846.625 s.  
*Disposition:* CLOSED

**D-06 - ETC_CENSUS_EXCLUDES_TRANSITIONS** *(magnitude: 23 elements)*  
FCPXML top-level spine carries 214 story elements; the ETC spine census is 191. The 23-element difference is exactly the transition elements.  
*Disposition:* CLOSED

**D-07 - NESTED_TITLES_NOT_IN_ETC_CENSUS** *(magnitude: 17 titles)*  
FCPXML contains 57 title elements; 40 sit on connected lanes at depth 1 (the ETC census) and 17 are nested inside compound clips.  
*Disposition:* CLOSED - the 17 are enrolled into CAPTION_REGISTRY by this run

**D-08 - ETC_CONNECTED_OFFSETS_NULL** *(magnitude: 404 elements)*  
Every connected element in P2_LOCK_timing.json carries timeline_offset_s: null; only rel_offset_s is present, and parent references are by non-unique name.  
*Disposition:* CLOSED - absolute offsets resolved from FCPXML nesting; resolver validated 191/191 against the ETC spine offsets

**D-09 - SYNC_CLIP_INTERNAL_MEDIA** *(magnitude: 18 elements)*  
18 resolved elements fall outside [0, 4846.625]. All are video/gap/audio components inside synchronized clips using the offset==start idiom; they are media plumbing, not timeline story elements.  
*Disposition:* CLOSED - excluded from the timeline census by rule

**D-10 - CORRELATION_INDETERMINATE_SPANS** *(magnitude: 1968 s of runtime)*  
12 of 19 registry segments cannot yield an independent offset estimate from envelope correlation.  
*Disposition:* CLOSED - each carries a categorized reason (segment shorter than the lag-search window, or SRT speech coverage below 30%)

**D-11 - SATURATED_SPEECH_MASK** *(magnitude: 2 segments / 238 s)*  
S08 and S10 initially returned apparent lags of -6.75 s and -3.25 s. In both spans the ASR emits back-to-back cues with a median inter-cue gap of 0.042 s (one frame at 24 fps), so the speech mask is effectively constant and the correlation surface is a plateau, not a peak.  
*Disposition:* CLOSED - measurement artefact, not a timebase shift; a genuine mid-film shift bounded by zero-offset neighbours on both sides is editorially impossible

**D-12 - EDITORIAL_CARD_LAG_CONSTANT** *(magnitude: +0.708 s median)*  
Across 11 semantic anchors spanning 97.4% of runtime, title cards land a median +0.708 s after the matching spoken phrase begins (sd 0.784 s).  
*Disposition:* CLOSED - a constant editorial design lag, not a timebase offset

**D-13 - NO_RATE_MISMATCH** *(magnitude: 0 s within CI)*  
Regression of anchor delta on time gives a drift of +0.684 s over the full runtime, 95% CI [-0.541, +1.909] s, which contains zero. A 23.976/24 pulldown error would be -4.85 s.  
*Disposition:* CLOSED

**D-14 - CUE_BOUNDARY_VS_EXISTING_ELEMENT** *(magnitude: +3.417 s)*  
CUE-01 is specified 00:00-01:13; the existing score element KICKSTANDS UP v1 occupies 00:00:00.000-00:01:16.417.  
*Disposition:* OPEN-TO-PDR (cue in/out binds to the closed ETC; reconciliation verdict is a human decision)

**D-15 - OBSERVED_ACTIVITY_EXCEEDS_CUE_SPAN** *(magnitude: approx +150 s of unscored ride)*  
CUE-03 ESCORT_ANTHEM is specified 00:27:40-00:29:10 (90 s). The mass ride is observed continuously in picture from 00:28:15 to approximately 00:33:00.  
*Disposition:* OPEN-TO-PDR (registry and cue sheet remain authoritative; recorded as CONFLICTED observation)

**D-16 - REGISTRY_LABEL_VS_OBSERVATION** *(magnitude: 462 s)*  
TIMELINE_REGISTRY S16 (00:58:43-01:06:25) carries the label 'bike_night_arrivals'. Measured mean luma over that span is 130.7 and the picture is bright daylight with blue sky throughout.  
*Disposition:* CONFLICTED - registry value retained as authoritative; observation recorded and raised as a PDR candidate

**D-17 - AGREEMENT_WITHIN_SAMPLING** *(magnitude: 0.5 s)*  
Registry S16/S17 boundary at 3985 s vs instrument-measured sustained night onset at 3984.5 s.  
*Disposition:* CLOSED - agreement within the 0.5 s observation grid

**D-18 - SILENCE_LAW_OVERLAP_CANDIDATE** *(magnitude: 61.958 s inside a mandatory-silence window)*  
Audio-lane element NOTOR1OUS_CARAVAN_2_ occupies 00:33:37.708-00:34:39.667, entirely inside SIL-01 (00:31:43-00:38:52). Its source is a contributed video's audio, not a score asset. Whether its content is musical was NOT determined by this run.  
*Disposition:* OPEN-TO-PDR - classified UNCERTAIN; escalated rather than resolved

**D-19 - CUE_SHEET_COVERAGE_GAPS** *(magnitude: 445.625 s across 11 spans)*  
Spans carrying neither a cue nor a mandatory silence.  
*Disposition:* CLOSED-AS-ENUMERATED (each span listed in CONDUCTOR_SCORE.uncovered_spans)

**D-20 - REGISTRY_SEGMENT_GAPS** *(magnitude: 434.625 s across 13 spans)*  
Runtime not covered by TIMELINE_REGISTRY segments S01-S19.  
*Disposition:* CLOSED-AS-ENUMERATED (each span listed in EDITORIAL_SYNCHRONIZATION.unsegmented_spans)

**D-21 - TITLE_TEXT_LETTER_SPACING** *(magnitude: cosmetic)*  
Title text extracted from FCPXML carries kinetic letter-spacing (for example 'W i n d T h e r a p h y'). Style runs within one text block were concatenated; residual spacing is the designed on-screen treatment and was not normalised.  
*Disposition:* CLOSED - verbatim preserved per DIE-X rule X-2 (zero interpretation at extraction)

**D-22 - OFFLINE_MEDIA_REFERENCE** *(magnitude: 1 asset)*  
FCPXML asset r95 (NOTOR1OUS_CARAVAN_2_) resolves to /Volumes/10TB/..., a volume not mounted for this run.  
*Disposition:* CLOSED-AS-NOTED - affects content inspection only, not timing; recorded as a reason D-18 could not be resolved here

**D-23 - DIE_V_SAMPLING_UNCERTAINTY** *(magnitude: +/-0.5 sample)*  
Contact-sheet evidence timestamps sit on a 3.000 s grid and probe sheets on a 1.000 s grid.  
*Disposition:* CLOSED - frame-accuracy claims rest on the ETC and on the 1.000 s probe grid, never on the 3.000 s survey grid

**D-24 - PROXY_RESOLUTION_CEILING** *(magnitude: 320x180 vs 3840x2160 master)*  
The visual ground truth supplied is a 320x180 proxy carrying a 'Filmage Editor' trial watermark. Formation geometry, flag identification, and camera-motion class are limited by this.  
*Disposition:* CLOSED-AS-DECLARED - every affected observation is capped at MEDIUM or UNCERTAIN; no observation claims detail the proxy cannot carry

**D-25 - DIE_V_SHEET_SAMPLING** *(magnitude: 20 of 54 sheets read in full)*  
54 survey contact sheets were generated at 3.000 s cadence covering 100% of runtime; 20 sheets were read frame-by-frame in full, chosen to cover every non-gauntlet span completely and the two homogeneous interview gauntlets by systematic sample.  
*Disposition:* CLOSED-AS-DECLARED - gauntlet spans carry span-level classifications only, never per-event claims outside a read sheet

### 7. Constitutional compliance

| constraint | evidence |
|---|---|
| No music generated | CONDUCTOR_SCORE declares `music_generated: false`; no audio was synthesised at any point in the run |
| No biometric identification | no face detection or recognition was run. The only person names in any artifact are text read from FCPXML title elements, carried as caption text |
| No sentiment inference | event classes are physical observables only. No emotional, atmospheric or affective term appears as an event class |
| Energy from observables only | ENERGY_CURVE values are carried through from the governed registry; DIE-V contributes luma, colour ratio, frame-difference energy and shot-change density, never an energy judgement |
| Enrichment namespaces untouched | every DIE-V event carries `enrichment: {nie: {}, mie: {}, pie: {}}` empty |
| Registries outrank visual observation | three conflicts recorded; registry value retained in all three |
| No silent recovery | 12 correlation spans reported INDETERMINATE with reasons rather than given inferred offsets; one silence-law item escalated as UNCERTAIN rather than judged; aerial-vs-elevated classified MEDIUM rather than asserted; five explicit NOT_OBSERVED declarations |
| No undocumented assumptions | the proxy-resolution ceiling (D-24) and the sheet-sampling plan (D-25) are declared in the registry itself, not left implicit |
| Frozen documents untouched | only CAPTION_REGISTRY was modified, with the enrichment noted in its header as the work order permits |

### 8. Reproducibility envelope (WET-SPEC-DIE-001 section 3)

| field | value |
|---|---|
| run_id | WECAPE-AR2-SPRINT3A-20260822-114028 |
| specification version | WET-SPEC-DIE-001 v0.2 (frozen tag wet-spec-die-001-v0.2-frozen) |
| architecture | ADR-009 (ACCEPTED) |
| repository commit at launch | ff0c45f77b2fb612606e1d5b8ef86641822e5e4a |
| source grades | FCPXML/ETC: editorial ground truth; SRT: GT-2; proxy: derived visual reference |
| source hashes | all four recorded in every artifact header |
| deterministic | frame extraction, envelope, correlation and null test are seeded (`numpy.random.default_rng(20260822)`); rerunning the scripts on the same hashes reproduces the numbers |
| model-mediated component | contact-sheet observation; fixture-validated on three probes before registry custody per DIE-X rule X-5 |

### 9. What a reviewer should push on

Three things in this report are weaker than they look, and it is better that the Executive Team hears it here than discovers it later:

1. **The envelope correlation is a weak instrument.** Its peak r is 0.278. It is convincing because the peak is at exactly zero and beats a proper null, and because two independent methods agree - not because the correlation itself is strong. On its own it would not close the tolerance.

2. **The visual ground truth is a 320x180 watermarked proxy.** It is sufficient for day/night, riding/static, crowd bands, ceremony/formation and reading burned-in titles. It is not sufficient for formation geometry, flag identification, or separating camera motion from subject motion. If Sprint 4 wants richer visual events, it needs a better proxy, not a better prompt.

3. **Twenty of 54 contact sheets were read in full.** Coverage of the non-gauntlet material is complete; the two interview gauntlets - 38% of runtime - are covered at span level by systematic sample. No per-event claim is made inside an unread sheet, but a reviewer should know the difference.

### 10. Verdict

**PASS.** Step 0 closed. Three artifacts produced under the canonical sync_event schema, each hash-pinned to all four sources. Fifteen cues and three conducted silences encoded as behaviour. Sixteen of sixteen existing audio elements reconciled as candidates. Twenty-five deltas, all categorized. Two items escalated to human adjudication rather than resolved by the implementation.
