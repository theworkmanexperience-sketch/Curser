# CAR-004 Appendix A — Capture Capability Matrix
## Governance Status
Document Type: CAR Appendix — Evidence · Status: FOR EXECUTIVE REVIEW · Date: 2026-08-22
Method: `ffprobe` against **actual Alpha RoundUp 2026 source media** on `WE_CAPE_OUTPUT`, plus code
reading of `wecape/capture/` and `scripts/`. Every cell is observed, not recalled.
**Amendment 1 (2026-08-22, pre-commit).** The first draft of this appendix asserted that *"no drone
material exists in this production."* The Executive Producer identified drone footage at
`~/Desktop/Drone`. Access was granted, the files were probed, and §A.5 replaces that claim. The
corrected finding is stronger than the original — see A.5-a.

**Limits declared:** `exiftool` was not available in the execution environment, so EXIF-only fields
(lens, serial, IMU orientation) are marked `UNVERIFIED` rather than guessed. Proprietary telemetry
payloads were detected but **not decoded** — presence is evidence, content is not.

---

## A.1 Devices — three registers, three different answers
| device | in `cameras.yaml` | in this production's SOURCES | in the Part 2 lock (FCPXML) | discussed by Executive |
|---|:--:|:--:|:--:|:--:|
| DJI Osmo Action 6 | ✅ `AC006` | ✅ 46 MP4 + 46 LRF | ✅ (as `DJI`) | ✅ |
| DJI Osmo Action 5 Pro | ✅ `AC004` | ✅ DCIM/DJI_001 | ✅ (as `DJI`) | ✅ |
| Insta360 X5 | ✅ | ✅ DCIM/Camera01 | ✅ **2,553.9 s — 53% of the film** | ✅ |
| OM System OM-1 | ❌ **absent** | ✅ 13 MOV + 2 ORF + 2 JPG | ✅ 75.7 s | ✅ |
| Insta360 X3 | ❌ | ❌ | ❌ | ✅ |
| Insta360 GO 3 | ❌ | ❌ | ❌ | ✅ |
| DJI Drone | ❌ | ❌ **not in SOURCES** | ❌ | ✅ — material found **outside governed custody**, see §A.5 |
| GoPro | ❌ | ❌ | ❌ | ✅ — a GoPro `version.txt` was found in the same uncustodied folder, see §A.5 |
| iPhone | ❌ | ❌ (stills exist, source unconfirmed) | — | ✅ |
| DJI Mic | ❌ | ❌ | ❌ | ✅ |

**Finding A.1-a — the registry is missing a device that shipped in the film.** OM System OM-1 opens the
locked cut (spine element 1, `005 · OM1 · P6250014.MOV`) and is not in `cameras.yaml`. The registry
that calls itself *"the SOURCE OF TRUTH for which physical body recorded a card"* covers 3 of the 4
bodies actually used.

**Finding A.1-b (amended) — no drone material exists in this production's *governed* sources.** No
drone folder in SOURCES, no drone in `cameras.yaml`, and no drone clip in the locked FCPXML. Drone-
labelled material does exist on the operator's Desktop, entirely outside custody — §A.5. The
`DJI`-named clips *in the lock* still resolve to Action bodies, which retrospectively confirms the
Sprint 3A refusal to read *"DJI"* as *"drone"* (RE-001, `VISUAL_EVENT_REGISTRY`
`camera_device_families_from_etc`). The aerial-looking shot at 00:33:00 (`VE-016`, confidence MEDIUM)
still has **no drone source within governed custody** to attribute it to, and the uncustodied clip
does not supply one — it is not in the lock and predates the shoot by two and a half years.

---

## A.2 What each device actually emits — observed
| device / file | embedded timecode | DF/NDF | creation_time | video | audio | data streams | handler names |
|---|---|:--:|:--:|---|---|:--:|---|
| Action 6 `.MP4` | `18:45:38:01` | **NDF** | ✅ UTC | HEVC 3840×2880 **25p** | AAC 48k 2ch | **3** | `CAM meta` · `CAM dbgi` · `TimeCodeHandler` |
| Action 6 `.LRF` | `11:48:21:17` | NDF | ✅ | H.264 960×720 23.976p | AAC 48k 2ch | **2** | `CAM meta` · `TimeCodeHandler` |
| Action 5 Pro `.MP4` | `09:39:08;15` | **DF** | ✅ | HEVC 3840×2880 **29.97p** | AAC 48k 2ch | **3** | `DJI meta` · `DJI dbgi` · `TimeCodeHandler` |
| OM-1 `.MOV` | `01:27:35;27` | **DF** | ✅ | H.264 3840×2160 **59.94p** | **PCM s16le** 48k 2ch | 1 | *(unnamed)* |
| Insta360 X5 `.insv` | **NONE** | — | ✅ | HEVC **1920×1920 ×2** (dual fisheye) 29.97p | AAC 48k 2ch | **0** | none |
| Insta360 X5 `.lrv` | NONE | — | ✅ | H.264 1664×832 29.97p | AAC 48k 2ch | 0 | none |
| Contributed `.mov` | NONE | — | ✅ | H.264 460×822 59.94p | AAC 48k 2ch | 0 | none |

### The four findings that matter
**A.2-a — Camera-native proxies carry the telemetry.** The DJI `.LRF` is not merely a small copy: it
carries `CAM meta` **and** a timecode track. Telemetry can be parsed from a 960×720 file instead of a
4K master. Nothing in the platform currently exploits this.

**A.2-b — The two DJI bodies name the same stream differently.** Action 6 emits `CAM meta` / `CAM dbgi`;
Action 5 Pro emits `DJI meta` / `DJI dbgi`. A parser keyed to one string silently misses the other
body's entire telemetry payload — and silently is the dangerous word. This is DOC-001 territory
(*validate the instrument before the measurement*) before a single line of parser is written.

**A.2-c — The kit mixes drop-frame and non-drop-frame timecode.** Action 6 is NDF at 25p; Action 5 Pro
is DF at 29.97; OM-1 is DF at 59.94 — all conforming into a **24p** sequence. Four frame rates and two
timecode conventions in one production. Every clip needs a conform, and DF/NDF mixing is a classic
silent-drift source in multicam sync.

**A.2-d — The dominant camera is the least instrumented.** The Insta360 X5 supplies **53% of the
finished film** and emits **no timecode and no data streams at all**. The platform's richest metadata
sits on the bodies that contribute least; its thinnest sits on the body that carries the documentary.
Any Acquisition Intelligence design that assumes metadata richness scales with screen time is
designing against this production.

---

## A.3 GPS — the finding with the sharpest operational edge
| observation | evidence |
|---|---|
| `cameras.yaml` records `gps_for_action: true` for **both** DJI bodies | `cameras.yaml` |
| `.SRT` sidecars are the GPS carrier for those bodies | `scripts/srt_telemetry.py` docstring; `SPEC_SRT_Telemetry.md` |
| `.SRT` files present in this production's SOURCES | **ZERO** (`find -iname '*.srt'` → 0) |
| SRT telemetry pipeline | **BUILT**, config-gated, default `false` (GAP-02) |

**The whole ride — the centrepiece of the film, 00:28:15 to ~00:33:00 of continuous public-road
formation riding — could have carried a GPS track. It does not.** The capability was built. The
registry records the camera as capable. No file was ever written.

`cameras.yaml` records what the camera **can do**, never what it **was set to do**. That distinction is
the entire argument for a Capture Readiness check, and it cost this production its route telemetry.

**This is the strongest available evidence for the Executive Team's own "Capture Readiness Score"
question, and it is a one-line pre-shoot check, not an architecture.**

---

## A.5 Acquisition outside custody — the `~/Desktop/Drone` finding
Identified by the Executive Producer during review; probed 2026-08-22 with granted access.

| observed | evidence |
|---|---|
| 5 files, 89 MB: `DJI_0047.MOV` · `.THM` · `.SCR` · `dji.gis` · `version.txt` | `ls -la ~/Desktop/Drone` |
| `DJI_0047.MOV` — H.264 **1920×1080 30p**, 15.73 s, `creation_time 2023-12-31T23:03:05Z` | `ffprobe` |
| **`vendor_id=FFMP`, `encoder=Lavf56.15.102`** — the file is an **FFmpeg re-encode**, not camera-original | `ffprobe` format tags |
| **No timecode, no data streams, no telemetry** | `ffprobe` |
| `version.txt` reports `"camera type":"HERO11 Black"`, `"camera serial number":"C34713245827 35"`, firmware `H22.01.02.20.00` — a **GoPro** card file | file contents |
| `dji.gis` is 43 MB with a `GIS` magic header — DJI **offline map-tile cache**, not flight telemetry | header inspection + size |
| `DJI_0047` appears **0 times** in the locked FCPXML | `grep` against `Info.fcpxml` |

### What this actually demonstrates
**A.5-a — Acquisition is happening outside governed custody.** This material never passed through
`offload_cards.py`. There is no `_offload_manifest.json`, no registry row, no shoot association, no
hash. It is invisible to every instrument the platform has. **This is the single clearest argument in
this package for an Acquisition Intelligence layer** — not because the platform lacks capability, but
because material can enter the building without meeting any of it.

**A.5-b — The folder's label, its filenames and its metadata disagree three ways.** Folder says
*Drone*. Filenames say *DJI* (Phantom-era `DJI_NNNN` + `.THM` + `.SCR` + `dji.gis` structure).
`version.txt` says *GoPro HERO11 Black*, with a serial. This is exactly the label-versus-content
failure `camera_identity.py` was built to catch — and it went uncaught because the material never
entered the pipeline. **Which device recorded `DJI_0047.MOV` is UNCERTAIN and requires human
confirmation; this review does not assert it.**

**A.5-c — Metadata was destroyed before acquisition.** `vendor_id=FFMP` and `encoder=Lavf56.15.102`
mean this file was transcoded by FFmpeg at some point. Whatever timecode, telemetry or camera tags the
original carried are gone. No parser can recover them. This is a live example of the strongest possible
argument for acquiring **camera-original** files: Tier 3 telemetry parsing is worth nothing against a
re-encode.

**A.5-d — `dji.gis` is a trap.** It is 43 MB, it is named like geographic intelligence, and it is a
map-tile cache for the DJI app. A future Acquisition Intelligence increment that pattern-matches on
file extension would find it, try to parse it as flight data, and either fail loudly or — worse —
succeed at extracting something meaningless. Recorded here so nobody builds that parser.

**A.5-e — Evidence status for GoPro and DJI Drone.** Both move from *"no evidence"* to *"evidence
exists, ungoverned, and insufficient to profile."* One re-encoded clip and one card `version.txt` do
not establish a device profile. They establish that these devices are **in the building** and outside
the registry.

## A.4 Confidence and what this appendix does not claim
| claim class | status |
|---|---|
| Timecode / creation_time / codec / resolution / fps / audio / stream counts / handler names | **OBSERVED** — reproducible with `ffprobe` on the cited files |
| Telemetry stream *presence* | **OBSERVED** |
| Telemetry stream *contents* (GPS, IMU, heading, altitude, orientation) | **NOT DECODED** — presence is not content |
| Lens, serial, exposure, IMU orientation from EXIF | **UNVERIFIED** — `exiftool` unavailable in this environment; `scripts/probe_camera.py` uses it in normal operation |
| Insta360 `.insv` internal telemetry | **UNVERIFIED** — not surfaced by `ffprobe`; proprietary container |
| Devices marked ❌ in A.1 | **NOT PRESENT** in registry, sources or lock — no claim made about their real-world capability |
| Which device recorded `DJI_0047.MOV` | **UNCERTAIN** — folder name, filename convention and `version.txt` disagree; requires human confirmation |
| `dji.gis` contents | **OBSERVED as a `GIS`-header binary of 43 MB**; identified as a map cache by structure and size, **not decoded** |
