# EVS-001 — Executive Viewing Session: how Road Soul breathes with the edit
## Governance Status
Document Type: **Executive Viewing Session — Brief** · Version **1.2** · Status: **PREPARED 2026-08-22 — SESSION NOT YET HELD**
Date: 2026-08-22 · Authority: Executive Producer · Resolves: `PDR-2026-08-22-ESS-002` (VCONF-02, D-15, D-19, SLF-02)
Precedent: `ELS-001` (Executive Listening Session) · Session class: **EVS** — picture + sound + editorial pacing
**v1.0 → v1.1:** scope narrowed by Executive direction. The session answers **one question**.
**v1.1 → v1.2:** an editorial-resolution viewing master was located, validated against the lock and
approved (`DOC-001` Amendment 1). **The session now runs on the 4K master, not the proxy.** The
§5 limitation *"no editorial-resolution viewing master exists"* is **RETIRED**.
Reporting conformance: `WET-SPEC-REPORT-001` v1.1 — component metrics and objective percentages below;
**the Executive Verdict is deliberately blank. It is the output of the session.**

| field | value |
|---|---|
| **Purpose** | **Is the proposed musical boundary (00:29:10.000) correct?** Nothing more |
| **Media span** | `00:27:10 – 00:33:30` of the locked cut (380 s), with two close passes |
| **Deliverable** | One boundary: option A/B/C/D + a timecode to the frame + whether it sits on a cut |
| **Expected duration** | **~13 minutes** — Passes 1, 2 and 3. Passes 4 and 5 are optional reference |
| **Register** | `intelligence/p2/registries/APPROVED_VIEWING_MASTER.yaml` — exactly one APPROVED per production |
| **Viewing master** | `Alpha RoudUp Part 2.m4v` · 3840×2160 · **4846.625000 s, exact to the lock** · sha `89e911b1…f8cd46` |
| **Processing Status** | `READY` — master validated, measurements corroborated on two instruments, verdict blank |

---

## 0. Scope — one question, by Executive direction

> *"ESS-002 should answer one question. Is the proposed musical boundary correct? Nothing more.
> Everything involving actual music waits until CUE-03 exists."* — Executive direction, 2026-08-22

**The question:** at which timecode does CUE-03 ESCORT_ANTHEM end?

**Why the narrowing was necessary.** There is no CUE-03. No MOTION-family cue has been generated; the
lock's only WE CAPE-added score asset is `KICKSTANDS UP v1` at `00:00:00.000–00:01:16.417`. The entire
27:10–33:30 region is unscored and will be unscored during the viewing. Two of the five questions
originally posed asked you to observe a cue that does not exist — and the dependency was circular,
since ESS-002 blocks the Pass 3 work that would produce it.

| original question | status in v1.1 |
|---|---|
| Does the ride feel **sustained**? | **IN SCOPE** — Pass 1 and Pass 2 |
| Does the cue **overstay**? | **STRUCK** → registered against `PDR-<date>-CUE-03` |
| Does the cue **exit naturally**? | **STRUCK** → registered against `PDR-<date>-CUE-03` |
| Does production sound become **stronger after the exit**? | **IN SCOPE** — already measured, §3.1 |
| Does the audience feel the **deceleration**? | **IN SCOPE** — already measured, §3.2 |

The struck questions are **registered, not discarded** — `ESS-002` Amendment 2 §A2.3 carries them
forward as a written obligation on the cue PDR, together with a third that the measurements raised:
*is the `LEAD` behaviour state achievable over this span's production audio?* (§3.1 — the span runs at
−3.17 dB, the loudest sustained level in the region).

**And the boundary you set is a hypothesis, not a lock.** `PDR-<date>-CUE-03` holds an explicit
licence to move it if the composed cue demands it — provided it records why. The governance value is
not that the boundary never moves; it is that it never moves silently.

## 1. What you are watching, and what the picture actually does

The FCPXML's primary spine, `00:27:25` to `00:32:00` — every shot, authoritative (resolver validated
191/191 against the ETC):

| in | duration | shot |
|---|---|---|
| 27:25.792 | 15.000 s | `028 · 10:59:30 · DJI` |
| **27:40.792** | 28.333 s | `011 · 10:27:16 · X5` ← **CUE-03 in, 0.792 s earlier, is the only boundary in this region that sits at a cut** |
| 28:09.125 | 3.667 s | `013 · X5` |
| 28:12.792 | 2.083 s | `013 · X5` |
| 28:14.875 | 3.125 s | `013 · X5` |
| 28:18.000 | 4.292 s | `013 · X5` |
| 28:22.292 | 29.458 s | `013 · X5` |
| **28:51.750** | **66.708 s** | `013 · X5` ← the longest shot in the region. **CUE-03's out point (29:10) falls 18.25 s inside it** |
| 29:58.458 | 3.458 s | `NOTOR1OUS_CARAVAN_1_` |
| 30:01.917 | 43.542 s | `016 · X5` |
| 30:45.458 | 7.083 s | `016 · X5` |
| **30:52.542** | **62.875 s** | `016 · X5` ← **SIL-01's in point (31:43) falls 50.458 s inside it** |
| 31:55.417 | 18.000 s | `014 · X5` |

**The shape in one sentence:** a burst of short cuts from 28:09 to 28:22, then the edit stops cutting —
66.7 s, then 43.5 s, then 62.9 s. The picture enters "let it ride" mode at **28:51.750**, nineteen
seconds *before* the cue sheet asks the music to leave.

---

## 2. The viewing passes — three required, two optional, in this order for a reason

Clean before marked, sound before silence-comparison, whole before close. Markers and measurements
anchor perception; they come *after* the judgement, not before it (DOC-001: validate the instrument
before the measurement — here, the instrument is you, and priming is the contamination).

### The instrument — approved 2026-08-22

```
Alpha RoundUp Part 2 /XML retry/Thursday Aug 20th/Alpha RoudUp Part 2.m4v
3840x2160 h264 · 24/1 fps NDF · AAC 48 kHz stereo · 12,199,752,138 bytes
duration 4846.625000 s — EXACT match to the editorial lock
sha256   89e911b1bffe14cefe330f8e4270d467dc06393b622143350ca42de8dbf8cd46
```

**Play it directly. Nothing needs to be cut.** The master's timeline *is* the lock's timeline, so every
timecode below is a position you can type into the transport.

> **Do not substitute a different render.** Six other candidates exist on the volume and **three of
> them are also 12 GB, also 3840×2160, and almost identically named** — and are **not** lock-conformant
> (`+1.500 s`, `+15.208 s`, `+22.000 s`). Verify the file you open reports **4846.625000 s** before you
> start. `DOC-001` Amendment 1 §A1.2 carries the full table.

| # | pass | play from → to | duration | required? | watch for |
|---|---|---|---|---|---|
| **1** | **clean, whole** | **27:10 → 33:30** | 380 s | **required** | **Nothing in particular. Watch it as an audience.** One question afterwards: **where did the music's job end?** Note the timecode only after it finishes |
| **2** | **muted, whole** | **27:10 → 33:30**, sound off | 380 s | **required** | Does the sequence still sustain with no sound at all? This separates *edit* pacing from *engine* pacing — and the boundary is a picture decision, so this is the pass that answers it most directly |
| **3** | **the boundary** | **28:40 → 30:30** | 110 s | **required** | The proposed boundary at **29:10**, in context. It sits 18.250 s into a 66.708 s shot. **Does the picture declare a musical transition there?** If it does not, 29:10 is a spreadsheet value, not an editorial event |
| 4 | the silence boundary | 31:10 → 32:30 | 80 s | optional | SIL-01 opens at 31:43, 50.458 s into a 62.875 s shot. Where the mix's own large level event lives (§3.1). Watch if you are weighing option B |
| 5 | marked reference | `PASS5_marked_reference_27-10_to_33-30.mp4` | 380 s | **last, if at all** | The only pass that stays on the proxy — it carries burned-in timecode and zone labels, which is exactly why it must not be watched first. **Reference only.** Use it to convert a Pass-1 instinct into a timecode |

**Final Cut Pro on the timeline is equally valid for Passes 1–4** and is preferable if you want to
scrub. The proxy cuts in `SPRINT3A_WORK/evs001/` remain for watching away from the machine; they are
now a **convenience, not the instrument.**

---

## 3. Component metrics — measured, not interpreted

Audio: full-mix RMS, 0.25 s grid, from `Filmage_Editor.mp4` (SHA `a53655fc…0f47e8`). Video:
frame-difference energy from the 2 fps observable series. Cuts: FCPXML primary spine (authoritative).

| region | dur | audio RMS | motion | cuts | mean shot |
|---|---|---|---|---|---|
| pre-roll 26:00–27:40 | 100 s | −8.22 dB | 31.22 | 3 | 33.33 s |
| **CUE-03 as specified** 27:40–29:10 | 90 s | **−3.69 dB** | 22.80 | 7 | **12.86 s** |
| **the gap** 29:10–31:43 | 153 s | **−3.17 dB** | 18.84 | 4 | **38.25 s** |
| SIL-01 first 77 s 31:43–33:00 | 77 s | **−10.82 dB** | 16.60 | 4 | 19.25 s |
| SIL-01 remainder 33:00–38:52 | 352 s | −12.76 dB | 19.03 | 17 | 20.71 s |

### 3.1 "Does production sound become stronger after the boundary?"
**Measured answer: no. It does not change at all.**

- across CUE-03's out point: **−3.6925 dB → −3.1675 dB = +0.525 dB.** Below the ~1 dB just-noticeable
  difference for broadband level. **There is no audio event at 29:10.**
- across SIL-01's in point: **−3.1675 dB → −10.8150 dB = −7.648 dB.** Large, and unmistakable by ear.

**The mix already performs an exit — at 31:43, not at 29:10.** Thirty-second walk:

| window | audio RMS | motion | cuts/min | |
|---|---|---|---|---|
| 27:00–27:30 | −10.57 dB | 29.48 | 4 | |
| 27:30–28:00 | −6.85 dB | 21.27 | 2 | ← CUE-03 in |
| 28:00–28:30 | −3.61 dB | 27.58 | 10 | |
| 28:30–29:00 | −2.67 dB | 20.61 | 2 | |
| 29:00–29:30 | −2.50 dB | 22.82 | 0 | ← CUE-03 out — **the loudest window in the region** |
| 29:30–30:00 | −2.71 dB | 17.83 | 2 | |
| 30:00–30:30 | −3.40 dB | 19.98 | 2 | |
| 30:30–31:00 | −3.21 dB | 16.51 | 4 | |
| 31:00–31:30 | −3.54 dB | 16.33 | 0 | |
| 31:30–32:00 | −4.43 dB | 23.02 | 2 | ← SIL-01 in |
| 32:00–32:30 | **−12.82 dB** | 11.48 | 2 | **the drop** |
| 32:30–33:00 | −14.39 dB | 18.14 | 4 | |

Two things worth carrying into the room. **The production mix rises ~7 dB from 27:00 to 28:00** — the
ride arriving — so part of CUE-03's stated job, *"transition the audience into shared momentum,"* the
production audio already does. And **CUE-03 is scheduled to exit at the loudest moment in the region**
(−2.50 dB, 29:00–29:30). Music leaving at the exact point the film is at its fullest is a legitimate
choice, but it should be a chosen one.

**One consequence for the deferred cue PDR, raised here because the measurement raises it.**
`CONDUCTOR_SCORE` assigns CUE-03 the behaviour state **`LEAD`** — *"music carries the span; ambient
engine and crowd sound sit under it but must remain audible."* Over a span whose production audio
already runs at **−3.17 dB, the loudest sustained level in the region**, `LEAD` is a demanding ask:
the music must sit above engines that the ESS-004 ruling now guarantees will stay. That is not a
boundary question and is out of scope today — it is registered as the third deferred question in
`ESS-002` §A2.3.

*Caveat, stated plainly:* this is **total mix energy**, not "engine energy." Speech, wind, engines and
the contributed clip are all in it. It measures whether the film gets louder or quieter, not what is
making the sound.

### 3.2 "Sustained?" and "does the audience feel the deceleration?"
**Measured answer: the deceleration is real, and it is in the *cutting*, not the *motion*.**

| | CUE-03 span | the gap | change |
|---|---|---|---|
| mean shot length | 12.857 s | 38.250 s | **2.975× longer** |
| frame-difference energy | 22.799 | 18.839 | 0.826× — barely moves |

The edit slows by a factor of three. What is *inside* the frame keeps moving at almost the same rate.
**The ride does not decelerate. The cutting stops interrupting it.** That is a meaningfully different
thing from "the sequence winds down," and Pass 2 (muted) is the test of which one you actually feel.

The gap's two halves are near-identical (−2.90 vs −3.44 dB; 19.98 vs 17.70 motion; 38.25 s mean shot
in both), so there is no measurable internal event in the 153 s to hang a boundary on. Any boundary
inside the gap will be a **musical** choice, not a response to something in the picture.

---

## 4. Candidate boundaries, with what each costs

Every cue-sheet boundary in this region except CUE-03's in point sits mid-take (ESS-002 Amendment 1).
If a boundary moves, these are the real picture events available:

| timecode | what it is | distance from 29:10 | note |
|---|---|---|---|
| **29:58.458** | cut into `NOTOR1OUS_CARAVAN_1_` | +48.5 s | the only cut in the gap's first half; a genuine picture event |
| **30:01.917** | cut into `016 · X5` | +51.9 s | 3.5 s later; the pair reads as one event |
| **30:45.458** | cut within `016` | +95.5 s | |
| **30:52.542** | cut into the 62.9 s take | +102.5 s | last cut before SIL-01 |
| **31:55.417** | cut into `014 · X5` | +165.4 s | **12.4 s *after* SIL-01 opens** — the nearest cut to the silence boundary |
| 29:10.000 | *the cue sheet's value* | 0 | 18.25 s into a 66.7 s shot; **no picture event, no audio event** |

---

## 5. Instrument limitations — declared before use, not after

**Retired in v1.2:** *"No editorial-resolution viewing master exists."* It did exist; it had not been
located. It is now validated, hashed and approved (`DOC-001` Amendment 1).

| limitation | status |
|---|---|
| ~~No editorial-resolution master~~ | **RETIRED.** 3840×2160, 4846.625000 s, exact to the lock |
| ~~Audio is a 44.1 kHz proxy mixdown~~ | **RETIRED for viewing.** The master carries AAC 48 kHz stereo |
| **Six other renders exist and three are 4K look-alikes that are NOT lock-conformant** | **LIVE — the one real hazard.** Verify 4846.625000 s before starting |
| §3 metrics were computed on the proxy series | **CORROBORATED, not superseded** — see below |
| §3 audio figures are **total mix energy** | **LIVE.** They measure whether the film gets louder or quieter, never what is making the sound |
| Frame-difference energy is computed at 64×36, 2 fps | **LIVE.** A coarse motion proxy: it ranks regions reliably, it does not measure camera movement |
| No CUE-03 exists | **LIVE.** §0 |

### 5.1 Two instruments, one answer
`DOC-001` requires that a cheap independent check be taken rather than assumed. The §3 region metrics
were recomputed from the 4K master's 48 kHz audio and compared with the proxy figures:

| measurement | from the **master** | from the proxy | agreement |
|---|---|---|---|
| across CUE-03 out (29:10) | **+0.5565 dB** | +0.5251 dB | **0.031 dB** |
| across SIL-01 in (31:43) | **−7.6244 dB** | −7.6476 dB | **0.023 dB** |

A 320×180 / 44.1 kHz proxy and a 3840×2160 / 48 kHz master agree to within **0.03 dB** on both deltas
that carry the finding. **The verdicts are unchanged and now rest on two independent instruments:** no
audible event at 29:10 (below the ~1 dB JND); a large audible event at 31:43.

## 6. Executive Verdict

### 6.0 Observation protocol — and an honest limit on it

**The protocol, as directed:**

> *"I would deliberately forget everything we've discussed about 29:10. Watch Pass 1 exactly as an
> audience. When you reach the end, immediately write down: 'The music's job ended at ___'. Write the
> time before opening any notes. Only afterward compare it against 29:10, 31:43, the measured
> transitions, and the cue sheet."*

**Adopted. Write the timecode before reopening this document.** That instruction is the whole
instrument, and it is worth taking literally: close the brief, play from 27:10, and do not consult
anything until a number is on paper.

**The limit that must be recorded with it.** *"Deliberately forget"* is not achievable by intention,
and this session's observer is already primed. Before this protocol was proposed, this brief and the
conversation around it had already supplied:

- that the proposed boundary is `00:29:10.000`;
- that the boundary sits **18.250 s inside a 66.708 s take**, and lands on no cut;
- that the picture *"enters let-it-ride mode at 28:51.750"* — an engineer's phrase, and a leading one;
- that mean shot length rises **2.975×** across the boundary;
- that there is **no audible level event at 29:10** and a **−7.6 dB event at 31:43**.

Priming does not clear on request. **The observation this session produces will therefore be an
INFORMED Executive observation, not an independent one**, and it must be labelled that way in the
disposition. It is still the most valuable thing available — an experienced eye on the actual picture
outranks any measurement here — but it cannot be cited as confirmation of the measurements, because
the measurements are already in the observer.

**If a genuinely independent observation is wanted, it costs one person and six minutes.** Someone who
has read none of this watches 27:10 → 33:30 on the approved master and writes down where the music's
job ended, before being told anything. That is the only way to obtain an uncontaminated data point,
and it would make the Executive's own observation *more* citable rather than less — two observers, one
primed and one not, is a stronger record than either alone. **Recommended, not required, and it should
not delay the session.**

**Whichever is done, the record states what the observer had been exposed to beforehand.** That is the
difference between a governed observation and an anecdote.

### 6.0.1 The predicted outcomes — with a fourth the Executive did not list

| # | outcome | reading |
|---|---|---|
| 1 | stops **near 29:10** | ESS-002 confirmed. The cue sheet's value was an editorial instinct, and it was right |
| 2 | stops **later**, near the long-take transition | ESS-002 shifts. **A governed finding, not a failure** |
| **4** | stops **EARLIER**, near **28:51.750** | **Not in the original list, and it is where the measurements point** — the edit stops cutting 18.25 s *before* the cue is scheduled to leave. If this happens it should not be retro-fitted as "the boundary shifts later" |
| 3 | **no conscious stopping point at all** | The most interesting outcome — it would suggest Road Soul must **yield gradually** rather than end at a discrete boundary. **Also the outcome most vulnerable to the priming above**, since the observer has already been told the picture decelerates rather than cuts. Weight it accordingly, and it is the outcome that most needs the independent second observer |

All four advance the platform. Outcome 3 would be the one that changes the *vocabulary* — a gradual
yield is not `HANDOFF`, and Road Soul does not currently have a word for it.

### 6.1 Viewing findings — TO BE RECORDED
**Pass 1 (clean, as an audience).** Where did the music's job end? `______`
**Written before reopening this brief?** ☐ yes ☐ no · **Observation class:** ☐ INFORMED ☐ INDEPENDENT
**Prior exposure, if INFORMED:** `______` *(§6.0 lists this session's default exposure)*
Did the ride feel sustained through to SIL-01? ☐ yes ☐ no ☐ partly: `______`

**Pass 2 (muted).** With no sound at all, does the sequence still sustain? ☐ yes ☐ no
Is the deceleration in the **edit** or in the **engines**? ☐ edit ☐ engines ☐ both

**Pass 3 (the 29:10 boundary).** Does anything happen at 29:10? ☐ yes ☐ no

### 6.2 Disposition of ESS-002 — the one question
**Is the proposed musical boundary (00:29:10.000) correct?** ☐ yes ☐ no

**Selected option:** ☐ A stands at 29:10 ☐ B extend ☐ C new CUE-03b ☐ D registry only ☐ Other: `______`
**Boundary timecode, to the frame:** `______`
**Does it sit on a cut?** ☐ yes ☐ no — **if no, the recorded reason:** `______`
**If C — in point for CUE-03b and its energy value:** `______`
*(§3.2: inheriting CUE-03's energy 5 is contradicted by a 2.975× drop in cut rate)*
**Rationale:** `______`
**Dispositioned by / date:** `______`

### 6.3 Optional — the behavioral question, if a rule presents itself
Only if watching makes one obvious. **This is not required to disposition ESS-002**, and the session
should not be held open for it.

> *"Let's let ESS-002 teach us how Road Soul breathes with the edit."*

**Candidate behavior:** `______`
*(e.g. "when the cut rate falls by more than 2x, the score yields to production sound and does not
return until the cut rate recovers" — measurable, falsifiable, checkable against every cue in the sheet)*

**Do not promote it to doctrine from this session.** One instance is an observation. **CUE-07
RIDE_PASSAGE (56:10–58:43) is the natural second test** — also MOTION family, also road, also
unscored today. And CUE-07 matters twice over: MOTION currently has only two cues, so CUE-03 and
CUE-07 *are* the entire evidence base for the MOTION grammar (`RSB-AUDIT-001` §4).

## 7. After the session
- ESS-002 dispositioned → `EDITORIAL_SYNCHRONIZATION.yaml` and `CONDUCTOR_SCORE.yaml` **regenerate**
  (DOC-002 — never hand-edited).
- The three deferred questions travel to `PDR-<date>-CUE-03` (`ESS-002` A2.3), which holds a recorded
  licence to move the boundary if the composed cue demands it.
- Gate: 2 of 4 dispositioned; **still CLOSED**. Remaining: ESS-001, ESS-003.
- Any candidate behavior recorded at §6.3 goes to `docs/doctrine/` as a **candidate**, not doctrine,
  with CUE-07 named as its test.

## 8. Session materials
`SPRINT3A_WORK/evs001/` on the media volume:

| file | SHA-256 |
|---|---|
| `PASS1_clean_27-10_to_33-30.mp4` | `a593e49dcc2867ed8c56dc47d8ca99fbdf86af8b19c24bad3974420e46e32b71` |
| `PASS2_muted_27-10_to_33-30.mp4` | `901878c80398559c844a6db9b11331a906e325c9eb40ee330496166bb6a2a5a8` |
| `PASS3_boundary_28-40_to_30-30.mp4` | `51312ab5ce1332cd48acf1c115b83628b295a81fd46c3444a6b82891da25722d` |
| `PASS4_sil01_31-10_to_32-30.mp4` | `5e77a2a8a459eae8a4113ac4523b144398b8d1a16ccda9a74d028c568ba63b2a` |
| `PASS5_marked_reference_27-10_to_33-30.mp4` | `6edcfd7e3c7b736a11c5ae78cb1e7339e8d8c758d904fc5cb486eaca66a159e3` |

All five cut from `Filmage_Editor.mp4` SHA `a53655fc…0f47e8`. **In v1.2 these are a convenience, not
the instrument** — Passes 1–4 run on the approved master; only Pass 5 (marked reference) remains proxy-only.

**Approved viewing master:** `Alpha RoundUp Part 2 /XML retry/Thursday Aug 20th/Alpha RoudUp Part 2.m4v`
· sha256 `89e911b1bffe14cefe330f8e4270d467dc06393b622143350ca42de8dbf8cd46` · 4846.625000 s.

Measurements: `intelligence/p2/ess/scripts/evs001_measure.py` · proxy series
`SPRINT3A_WORK/audio_rms_0p25.npy`, `video_obs_2fps.npy` · master cross-check excerpt
`SPRINT3A_WORK/evs001/master_1550_2350_mono8k.wav` (1550–2350 s, mono 8 kHz, for level comparison only).
