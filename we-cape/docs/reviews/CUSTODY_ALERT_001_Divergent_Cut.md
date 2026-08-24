# CUSTODY ALERT 001 — a second cut of Part 2 exists, and it is not the governed lock
**Raised:** Music Systems Engineer, 2026-08-24 · **For:** Executive Producer / Chairman · **Priority: HIGH**
**Occasion:** instrument validation for the seven-prompt analysis work order
**Status of the work order:** **NOT EXECUTED.** Reason below.

---

## 0. Summary

The folder named in the work order contains a **different edit of Alpha RoundUp Part 2**, dated
**2026-08-24** — two days after the lock. It diverges from the governed cut at **00:03:27.208** and
runs **157.125 seconds shorter**.

The folder also contains **three assets of three different durations**. They are not one production's
assets.

Producing a *"definitive production fingerprint"* over these inputs would have yielded a
confident-looking document describing **no actual program**. Per `DOC-001` — *validate the instrument
by conformance before trusting its fidelity* — nothing was measured.

---

## 1. What is in the folder, measured

| asset | duration | resolution / audio | vs governed lock 4846.625 s |
|---|---|---|---|
| `Info.fcpxml` (inside `.fcpxmld`) | **4689.500 s** | 3840×2160p24 · 136 assets | **−157.125 s** |
| `Alpha RoudUp Part 2.m4a` | **4689.557 s** | AAC 48 kHz stereo | −157.068 s — **agrees with the fcpxml** |
| `…_SRT_English (United States).srt` | last cue **01:18:08.958** · **2036 cues** | — | governed SRT has **2291** cues |
| `Analysis_Day_2_Part_1_video-custom-1.mov` | **1648.292 s** | 854×480 · 30 fps · 44.1 kHz | **−3198.3 s — 27.5 min, not 80** |
| `Analysis_Day_2_Part_1_video.WAV` | **1648.083 s** | PCM s16le 44.1 kHz | −3198.5 s |

**Hashes — neither matches the governed Primary Source:**

```
fcpxml   found 1ab3d12f0dd150c63907a4b2e4bac4253baf8100910dfda74daa3a5378b6b4d2
      governed 2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7

SRT      found 2a16dd700148488fc4d103f91a93421e0d88b35cbce0463c3cbd915fbbc33869
      governed 89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b
```

**Three durations in one folder — 4689.5 s, 4689.6 s, 1648.3 s.** The `.mov` and `.WAV` are a
27½-minute program; their filename says `Day_2_Part_1`. They are 30 fps / 44.1 kHz against the
production's 24 fps / 48 kHz. **Whatever they are, they are not this cut.**

---

## 2. The finding that matters — this is a re-edit, not a trim

Run through the **validated** resolver (`fcpx_resolve.py`, 191/191 against the ETC):

| | analysis cut | governed lock | delta |
|---|---|---|---|
| sequence duration | 4689.500 s | 4846.625 s | **−157.125 s** |
| primary-spine elements | **201** | 191 | **+10** |
| all resolved elements | 1096 | 1025 | +71 |
| titles | **65** | 57 | **+8** |
| transitions | 178 | 180 | −2 |

**It is shorter and has more elements. That is not a tail trim.**

### Where they part company

The two cuts are **identical to the millisecond for the first 26 primary-spine elements — 0 s to
00:03:27.208.** Then:

```
index 26   governed  00:03:27.208   HO11YWOOD_GP
           analysis  00:03:36.041   028 · 06-26 10:59:30 · DJI      delta +9.833 s
```

**Everything after 00:03:27 is a different edit.**

### Consequences visible immediately

| governed timecode | governed content | same timecode in the analysis cut |
|---|---|---|
| `00:27:40.792` — CUE-03 in, and a cut | `011 · 10:27:16 · X5` starts | the same shot starts at **`00:27:44.292`** — **+3.500 s** |
| `00:52:04.000` — SIL-02 in | `043 · 12:50:16 · DJI` | **`049 · 13:40:39 · DJI` — a different clip entirely** |

The escort sequence still exists and has **moved**. By 52 minutes the drift is large enough that a
silence-zone boundary lands on unrelated material.

---

## 3. What this means for the governed record

**If the 2026-08-24 cut is the intended production**, then every artifact built to date describes a
superseded edit:

| artifact | status if the new cut governs |
|---|---|
| `RE-001` four input hashes | no longer describe the production |
| `CONDUCTOR_SCORE` v1.1.0 · `EDITORIAL_SYNCHRONIZATION` v1.1.0 | every boundary past 00:03:27 is wrong |
| `CAPTION_REGISTRY` 0.2.1 · `VISUAL_EVENT_REGISTRY` 1.0.1 | positions wrong; **8 titles unaccounted for** |
| `VOICE_PRIORITY_MAP` · `MUSIC_OVERLAY_TIMELINE` · `BEHAVIORAL_FINGERPRINT` | built today, all against the old cut |
| `APPROVED_VIEWING_MASTER` (4846.625 s) | the approved master is the **old** cut |
| **`ESS-002` — the boundary at `00:29:10.000`** | **the question may not exist in the new cut** |
| `EVS-001` | prepared against a superseded picture |
| Silence zones SIL-01 / SIL-02 / R46 | timecodes shift; SIL-02 already lands elsewhere |

**`SOP-06 B2`:** *any picture change during Phase B voids the lock and requires re-export and
re-audit.* The gate's own `sop06_placement.caution` records this. **This is a Phase-B custody event,
not an analysis request.**

---

## 4. What I did not do, and why

The work order asked for a *"definitive production fingerprint"* and six further reports. **None was
produced.** A fingerprint computed over a folder holding three durations and two unrecognised hashes
would be precise, confident and meaningless — the exact failure mode the Approved Viewing Master
register was created to prevent, appearing for the **third time today**:

1. seven candidate viewing masters, three of them 4K look-alikes, only one lock-conformant;
2. a shot list labelled *"every shot, authoritative"* that showed 214 of 1025 elements;
3. **this.**

**Nothing here is a judgement about which cut is correct.** That is entirely the Executive's.

---

## 5. The decision required — three paths

| | if… | then |
|---|---|---|
| **A** | the **2026-08-22 lock** (4846.625 s) remains the production | the 08-24 folder is a working export and must be marked `REFERENCE_ONLY` in `APPROVED_VIEWING_MASTER`. Everything stands. The work order can run against the **governed** assets |
| **B** | the **2026-08-24 cut** (4689.500 s) is the production | the lock is void per SOP-06 B2. Re-export, re-audit, re-hash, and **regenerate every derived artifact**. `RE-001` becomes a historical baseline of a superseded cut — which is exactly what a Reference Execution is *for*. ESS-002 and EVS-001 are re-scoped to the new picture |
| **C** | the 08-24 cut is a **different deliverable** (analysis edit, festival cut, Part 1 assembly) | it is registered as a separate production with its own lock, hashes and registries. Neither contaminates the other |

**No recommendation.** All three are consistent with the platform's rules; which is true is a
production fact only you hold.

---

## 6. On the seven prompts themselves — three need instruments the platform does not have

Independent of which cut wins. Raised now so it is not discovered mid-report.

| prompt | status | note |
|---|---|---|
| **1 · Production fingerprint** | **runnable today** on governed assets | items 1–16 are already computed: 1025 elements, 180 transitions in 8 kinds (166 Cross Dissolve, mean 0.889 s), 109 storylines, 57 titles, 478 asset-clips. Shot statistics exist per cue in `BEHAVIORAL_FINGERPRINT` |
| **2 · Editorial segmentation** | **largely delivered** | `MUSIC_OVERLAY_TIMELINE` + `TIMELINE_REGISTRY`. *People* and *Location* come from `RIDER_REGISTRY` / `LOCATION_REGISTRY`, where most entries are `UNCONFIRMED` — that status must survive into any segment table |
| **3 · Voice map** | **partly blocked** | speech vs non-speech is measured (`VOICE_PRIORITY_MAP`). **Applause, crowd reaction, engine-only and room ambience require an audio classifier the platform has never built or validated.** Under DOC-001 its output is ineligible for custody until it reproduces a known-good result |
| **4 · Copyright exposure** | **blocked** | requires music detection **and** source attribution (PA vs stereo vs radio). No validated instrument exists. This one carries legal weight: **an unvalidated classifier asserting "copyrighted music may exist here" is a liability claim with no evidence behind it.** It should not be produced by guess |
| **5 · Visual energy** | **partly blocked** | cut density and frame-difference energy exist. **Camera motion needs optical flow**; DIE-V has neither optical flow nor resolution — 64×36 at 2 fps on a 320×180 proxy. Motorcycle and people density need object detection, which is also absent, and *people density* brushes the standing no-biometrics constraint |
| **6 · Editorial backbone** | **runnable today** | purpose-change points are derivable from the primary spine, `TIMELINE_REGISTRY` activities, speech density and graphic density. *"Interview begins/ends"* is the one field needing care: it is an **editorial classification**, not an FCPXML fact |
| **7 · Music opportunity map** | **largely delivered** | `MUSIC_OVERLAY_TIMELINE` uncovered regions + `VOICE_PRIORITY_MAP` behaviour spans already answer most fields. *"Legally"* depends on prompt 4 |

**Four of seven can be produced now against the governed lock. Three need instruments that must be
built and validated first — and prompt 4 should not be attempted at all until it can cite evidence.**

---

## 7. Recommended next action

**Rule on §5 first.** Everything else — the seven prompts, ESS-002, EVS-001, the gate, CUE-03 —
depends on which cut is the production. Measuring before that is answered risks producing a large,
authoritative body of work about a film that is no longer being made.

```
pass_1                 ACTIVE
boundary_declared      false
observation_card       BLANK
disposition_inference  FORBIDDEN
cut_in_force           AWAITING_EXECUTIVE_DISPOSITION
```
