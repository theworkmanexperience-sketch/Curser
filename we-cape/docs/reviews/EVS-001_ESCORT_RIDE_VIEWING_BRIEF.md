# EVS-001 — Executive Viewing Session: how Road Soul breathes with the edit
## Governance Status
Document Type: **Executive Viewing Session — Brief** · Version **1.1** · Status: **PREPARED 2026-08-22 — SESSION NOT YET HELD**
Date: 2026-08-22 · Authority: Executive Producer · Resolves: `PDR-2026-08-22-ESS-002` (VCONF-02, D-15, D-19, SLF-02)
Precedent: `ELS-001` (Executive Listening Session) · Session class: **EVS** — picture + sound + editorial pacing
**v1.0 → v1.1:** scope narrowed by Executive direction 2026-08-22 (`ESS-002` Amendment 2). The session
now answers **one question**. Two questions are struck and registered against `PDR-<date>-CUE-03`.
Reporting conformance: `WET-SPEC-REPORT-001` v1.1 — component metrics and objective percentages below;
**the Executive Verdict is deliberately blank. It is the output of the session.**

| field | value |
|---|---|
| **Purpose** | **Is the proposed musical boundary (00:29:10.000) correct?** Nothing more |
| **Media span** | `00:27:10 – 00:33:30` of the locked cut (380 s), with two close passes |
| **Deliverable** | One boundary: option A/B/C/D + a timecode to the frame + whether it sits on a cut |
| **Expected duration** | **~13 minutes** — Passes 1, 2 and 3. Passes 4 and 5 are optional reference |
| **Processing Status** | `READY` — media cut, measurements complete, verdict blank |

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

| # | file | span | duration | required? | watch for |
|---|---|---|---|---|---|
| **1** | `PASS1_clean_27-10_to_33-30.mp4` | 27:10–33:30 | 380 s | **required** | **Nothing in particular. Watch it as an audience.** One question afterwards: **where did the music's job end?** Note the timecode only after it finishes |
| **2** | `PASS2_muted_27-10_to_33-30.mp4` | 27:10–33:30 | 380 s | **required** | **Muted.** Does the sequence still sustain with no sound at all? This separates *edit* pacing from *engine* pacing — and the boundary is a picture decision, so this is the pass that most directly answers it |
| **3** | `PASS3_boundary_28-40_to_30-30.mp4` | 28:40–30:30 | 110 s | **required** | The proposed boundary at **29:10**, in context. It sits 18.25 s into a 66.7 s shot. **Does anything happen there?** If nothing does, 29:10 is not a boundary — it is a number |
| 4 | `PASS4_sil01_31-10_to_32-30.mp4` | 31:10–32:30 | 80 s | optional | The SIL-01 boundary at 31:43, 50.5 s into a 62.9 s shot. Where the mix's own large level event lives (§3.1). Watch if you are considering option B |
| 5 | `PASS5_marked_reference_27-10_to_33-30.mp4` | 27:10–33:30 | 380 s | **last, if at all** | Burned-in timecode and zone labels. **Reference only.** Use it to convert a Pass-1 instinct into a timecode |

**Preferred instrument: Final Cut Pro, on the timeline itself.** These files are 320×180 — the only
full-length Part 2 render that exists is a proxy (§5). For *pacing* that is sufficient, because pacing
is a property of time and the cut points are exact. For anything about how the image *looks*, it is
not. Watch Pass 1 in FCP at full resolution if you can; use these files for Passes 2–5, for
repeatability, and for watching away from the machine.

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

| limitation | effect on this session |
|---|---|
| **No editorial-resolution viewing master exists.** The only full-length Part 2 renders are 320×180: `Filmage_Editor.mp4` (4846.747 s, lock-conformant to 0.122 s) and `Reduced_Part_2.mp4` (4850.810 s — **4.19 s longer, NOT lock-conformant; do not use it**) | Pacing judgements are **unaffected** — cut points are exact and time is exact. Judgements about the *image* (composition, grade, detail) are **not supported**. Do not rule on anything image-quality-dependent from these files |
| The proxy carries a watermark | Cosmetic; does not affect timing |
| Audio is a 44.1 kHz AAC stereo mixdown | Adequate for relative level and for "what is audible." **Not** adequate for mix decisions — duck depth, EQ, final level all belong to a later pass |
| Frame-difference energy is computed at 64×36, 2 fps | It is a coarse motion proxy. It ranks regions reliably; it does not measure camera movement as such |
| §3 audio figures are **total mix energy** | They do not isolate engines from speech from wind |
| No CUE-03 exists | §0 |

---

## 6. Executive Verdict
### 6.1 Viewing findings — TO BE RECORDED
**Pass 1 (clean, as an audience).** Where did the music's job end? `______`
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

All five cut from `Filmage_Editor.mp4` SHA `a53655fc673945a0d99dde3d5b60c9a126d8b41e4e44a7c7eedeb058ba0f47e8`.
Measurements: `intelligence/p2/ess/scripts/evs001_measure.py` · source series
`SPRINT3A_WORK/audio_rms_0p25.npy`, `video_obs_2fps.npy`.
