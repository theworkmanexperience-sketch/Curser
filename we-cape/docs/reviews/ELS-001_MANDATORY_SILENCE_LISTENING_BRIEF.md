# ELS-001 — Executive Listening Session: the semantics of `MANDATORY_SILENCE`
## Governance Status
Document Type: Executive Listening Session — Brief · Status: **SESSION HELD 2026-08-22 — FINDING RECORDED, RULING PENDING**
Date: 2026-08-22 · Authority: Executive Producer · Resolves: `PDR-2026-08-22-ESS-004` (SLF-01, D-18)
Reporting conformance: `WET-SPEC-REPORT-001` v1.1 — component metrics and objective percentages are
supplied below; **the Executive Verdict is deliberately blank. It is the output of the session.**

| field | value |
|---|---|
| **Purpose** | Determine the semantic meaning of `MANDATORY_SILENCE` for the WE CAPE platform |
| **Media span** | `00:33:37.708 – 00:34:39.667` (61.958 s) of the locked cut |
| **Deliverable** | One Executive ruling |
| **Expected duration** | ~5 minutes including discussion |
| **Processing Status** | `READY` — media, controls and measurements are all in place |

---

## 1. Why this is 62 seconds of listening and a platform rule
The span is one audio element. The ruling is a definition, and it propagates:

`CONDUCTOR_SCORE` silence behaviour (SIL-01 · SIL-02 · R46 carve-out) → `CUE-03` and `CUE-04`
approach/return states → MIE pass gates → cue validation → every future documentary's silence law →
production automation that has to decide, without a human, whether a given element belongs in a
silence zone.

Getting it right once costs five minutes. Getting it wrong costs it in every production that follows.

---

## 2. **A correction to the PDR before you rule — the question is not binary**
`PDR-2026-08-22-ESS-004` framed the ruling as *no score* **or** *no sound*. That framing is
insufficient, and I would rather say so before the session than discover it after.

The element is **a contributed video's own audio track**. If what is on it is music that was playing
*in the scene* — a PA, a car system, a band — then it is **diegetic** music, and neither option covers
it cleanly:

- *"No score"* permits it — it is not score, it is location sound.
- *"No sound"* forbids it — along with engine noise, wind and room tone.

Film practice has distinguished these for a century. The covenant's own words are the test:

> *"Exists as absence — the town's own words … must carry their full civic weight **unassisted**."*

Diegetic music is genuinely arguable both ways. It is *not* an assist the edit added; it *is* something
competing with the speech. **That is the question the session should actually answer**, and it needs
three options, not two.

---

## 3. What to listen for
Play `00:33:37.708 – 00:34:39.667`. Underneath the proclamation reading, decide which you hear:

| what you hear | classification |
|---|---|
| A composed bed — sustained chords, instrumentation, an arrangement placed by an editor | **NON-DIEGETIC SCORE** |
| Music that was audibly playing at the location — a PA, a vehicle system, a live band, with room acoustics | **DIEGETIC / SOURCE MUSIC** |
| Engines, wind, crowd, road, room tone — no musical pitch content | **PRODUCTION SOUND** |
| Nothing distinguishable under the speech | **INAUDIBLE — element may be muted or gain-floored** |

The last row is a real possibility and worth checking first: an element can be present on a lane and
mixed to silence. **§4 indicates it is not**, but confirm it with your ears before ruling on it.

---

## 4. Component metrics — objective, no classification
Measured on the master proxy at 22.05 kHz mono. Three-way comparison so each number reads against a
known reference rather than an absolute threshold.

- **TARGET** — `00:33:37.708–00:34:39.667`, the element inside SIL-01
- **CONTROL-MUSIC** — `00:00:02.000–00:01:03.958`, `KICKSTANDS UP v1`, the lock's only score asset
- **CONTROL-SPEECH** — `00:35:20.000–00:36:21.958`, inside SIL-01, **no audio-lane element present**

| measure | TARGET | CONTROL-MUSIC | CONTROL-SPEECH | reads as |
|---|---:|---:|---:|---|
| RMS (dBFS) | −11.34 | −4.84 | −10.82 | target sits at speech-control level |
| Level range p95−p5 (dB) | **7.89** | 13.03 | 24.10 | **target is the steadiest of the three** |
| Frames >25 dB below peak | **0.0 %** | 0.1 % | 4.1 % | **target never drops out** |
| Spectral flatness (low = tonal) | **0.1524** | 0.4567 | 0.2882 | **target is the most tonal of the three** |
| Spectral centroid (Hz) | **261** | 310 | 742 | target sits near the music control, far from speech |
| Energy 80–250 Hz | **26.59 %** | 23.63 % | **3.87 %** | **~6.9× the low-frequency energy of the speech-only control** |
| Energy 1–4 kHz (speech band) | 1.21 % | 2.06 % | 10.75 % | speech band is a small share of a low-heavy mix |
| Beat periodicity (0–1) | **0.0403** | 0.7042 | 0.5875 | **no periodic beat detected in the target** |
| Implied BPM at that peak | 51.7 | 69.8 | 184.6 | meaningless where periodicity is near zero |

### 4.1 The one thing these numbers establish
> **Something substantial and low-frequency is present under the proclamation in the target span that
> is absent from the otherwise-comparable span of the same silence zone.** 26.59 % versus 3.87 % of
> total energy in 80–250 Hz, with the target never dropping out and showing the most tonal spectrum of
> the three.

The element is **audible**. It is not muted. Row 4 of §3 is unlikely.

### 4.2 What these numbers do **not** establish
- **They do not classify the content.** Steady, tonal, low-frequency, no beat is equally consistent
  with a sustained musical pad **and** with motorcycle engine rumble. The measurement cannot separate
  them; a human ear separates them instantly. That is why this is a listening session.
- **The element cannot be isolated.** All figures describe the **mixed** program audio. The element's
  own track is not separable from the proclamation in the locked master.
- **Source audio was never inspected.** `/Volumes/10TB/.../NOTOR1OUS_CARAVAN_2_.mp4` remains offline
  (delta D-22). These measurements are of the mix, not of the element.
- **The proxy is lossy** (AAC, from a 320×180 export). Low-frequency energy ratios are robust to that;
  fine timbral judgement is not.

---

## 5. Ruling options
| # | ruling — `MANDATORY_SILENCE` means… | permits | forbids | consequence |
|---|---|---|---|---|
| **1** | **No non-diegetic score** | location sound, engines, room tone, **diegetic music** | composed beds placed by the edit | Closest to film convention. Most permissive. Requires every future silence-zone element to be adjudicated for diegesis — a judgement automation cannot make alone |
| **2** | **No music of any kind**, diegetic or not | engines, wind, crowd, room tone | anything with musical pitch content | Machine-checkable in principle. May forbid material that is genuinely part of the town's own record |
| **3** | **No sound but the primary speech** | nothing else | all layered elements | Strictest reading of *"unassisted"*. Would forbid engine and ambience beds the film may rely on elsewhere |

**Precedent note:** whichever is chosen becomes the definition for `SIL-01`, `SIL-02`, the `R46`
carve-out, and every silence zone in every future production. Option 1 is the most editorially
faithful and the least automatable; option 2 is the most automatable and may be editorially blunt.

---

## 6. Executive Verdict
### 6.1 Listening finding — RECORDED 2026-08-22
> *"The target span contains a composite production audio bed consisting of multiple audible elements,
> including music/vocals, engine rumble, wind, and speech. The Executive cannot conclude that the
> audible musical content is exclusively editorial (non-diegetic) based on the available proxy."*

**Content heard:** ☒ music **and vocals** ☒ production sound (engine, wind) ☒ speech
☐ ~~inaudible~~ (struck) · diegesis: **UNDETERMINED on the proxy**

**Decidability note:** definition 1 cannot be applied to this finding — it requires the diegesis
judgement the Executive declined to make. Definitions 2 and 3 can. See PDR Amendment 3.

### 6.2 Ruling — PENDING
**`MANDATORY_SILENCE` shall mean:** ☐ 1 no non-diegetic score ☐ 2 no music of any kind ☐ 3 no sound but speech ☐ other: ______
**Disposition of this element:** ☐ permitted, covenant intact ☐ remove ☐ move out of the zone ☐ re-cut so picture and audio coincide
**Rationale:** ______
**Ruled by / date:** ______

---

## 7. After the ruling
Confirmed disposition order — the silence decision informs the escort-ride discussion:

```
ESS-004  →  ESS-002  →  ESS-001  →  ESS-003
```

On ruling, `CONDUCTOR_SCORE.yaml` and `EDITORIAL_SYNCHRONIZATION.yaml` **regenerate** from the disposed
values (DOC-002 — never hand-edited), and the run is archived as **RE-002** with its delta against
RE-001 categorized. The gate's `on_open.required_actions` already specifies this; the mechanism is
armed and waiting on four decisions.

## 8. Session materials
`SPRINT3A_WORK/ess004/target.wav` · `control_music.wav` · `control_speech.wav` (62 s each, on the
media volume) · measurements `out/ess004_measurements.json` · script
`intelligence/p2/ess/scripts/ess004_measure.py`.
