# CAR-004 Appendix B — Acquisition Readiness Report: Alpha RoundUp Part 2
## Governance Status
Document Type: CAR Appendix — Worked Example · Status: FOR EXECUTIVE REVIEW · Date: 2026-08-22
Conforms to: **WET-SPEC-REPORT-001 v1.0** (Component Metrics → Objective Percentages → Executive Verdict)

> **This is a worked example, not a platform artifact.** It demonstrates the reporting standard against
> real evidence so the Executive Team can see the pattern before authorizing anything that produces it.
> No system was built to generate this. Producing it automatically is `S-3`, still under review.

Evidence base: `ffprobe` against Alpha RoundUp 2026 source media · `cameras.yaml` · `wecape/capture/` ·
`scripts/` · RE-001 (`WECAPE-AR2-SPRINT3A-20260822-114028`) · Appendix A.

---

## 1. Component Metrics
| Capability | Available | Enabled | Consumed | Status | Evidence |
|---|:--:|:--:|:--:|---|---|
| Filename timestamp | ✓ | ✓ | ✓ | **PASS** | `timestamp.py` level 0; `DJI_YYYYMMDDHHMMSS`, `VID_YYYYMMDD_HHMMSS` |
| Device clock (`creation_time`) | ✓ | ✓ | ✓ | **PASS** | present on all four device families; `timestamp.py` level 1 |
| Locked FCPXML (editorial contract) | ✓ | ✓ | ✓ | **PASS** | `Info.fcpxml` sha `2bf06853…`; ETC derived from it |
| Canonical SRT (speech) | ✓ | ✓ | ✓ | **PASS** | lock SRT sha `89d61f96…`, 2,291 cues |
| Per-card offload manifests | ✓ | ✓ | ✗ | **OPPORTUNITY** | `_offload_manifest.json` written per card; never aggregated |
| **Embedded timecode** | ✓ *(3 of 4 families)* | ✓ | **✗** | **OPPORTUNITY** | read by `proxy.py::_get_timecode()`; **used only to re-stamp proxies** — not by `timestamp.py`, `grouper.py` or export |
| Telemetry stream (`CAM meta` / `DJI meta`) | ✓ *(DJI only)* | ✓ | **✗** | **OPPORTUNITY** | detected by `probe_camera.py::stream_signals()`; never decoded |
| Camera-native proxies (`.LRF` / `.lrv`) | ✓ | ✓ | **✗** | **OPPORTUNITY** | 46 `.LRF` on the Action 6 card alone, carrying **telemetry *and* timecode**; `proxy.py` transcodes its own instead |
| 4K video master | ✓ | ✓ | **✗** | **OPPORTUNITY** | 3840×2880 / 3840×2160 masters exist in SOURCES; Sprint 3A DIE-V was supplied a **320×180 watermarked proxy** (delta D-24) |
| **GPS (`.SRT` sidecars)** | ✓ *(both DJI bodies capable)* | **✗** | — | **ATTENTION** | `cameras.yaml` records `gps_for_action: true`; `find -iname '*.srt'` → **0 files** |
| SRT telemetry pipeline | ✓ | **✗** *(gated `false`)* | — | **ATTENTION** | GAP-02; `scripts/srt_telemetry.py` built, promotion blocked on 4 unit tests |
| Device registry coverage | ✓ | *partial* | ✓ | **ATTENTION** | `cameras.yaml` holds 3 of the 4 bodies used; **OM-1 absent** — and it opens the locked cut |
| Custody at acquisition | ✓ | **✗** | ✗ | **ATTENTION** | `~/Desktop/Drone`: 5 files, no manifest, no registry row, no hash, no shoot association (Appendix A §A.5) |
| Insta360 X5 timecode | **✗** | — | — | **ABSENT** | `.insv` probe: no timecode track, no data streams. The device emits none |
| Insta360 X5 telemetry | **✗** *(via ffprobe)* | — | — | **ABSENT** | proprietary container; not surfaced. **UNVERIFIED**, not disproven |

**Nothing in this table is BLOCKED.** Every gap is either a setting (ATTENTION) or value already paid
for and not collected (OPPORTUNITY). That distinction is the point of the standard — and it is exactly
what a single number would have destroyed.

## 2. Objective Percentages
Each carries its numerator, denominator and source, per WET-SPEC-REPORT-001 §5.

| Measurement | Value | Numerator / Denominator | Source |
|---|---:|---|---|
| Editorial synchronization coverage | **91.2 %** | 4,421.2 s inside a registry segment / 4,846.625 s | RE-001 `EDITORIAL_SYNCHRONIZATION` |
| Cue + conducted-silence coverage | **90.8 %** | 4,401.0 s / 4,846.625 s | RE-001 `CONDUCTOR_SCORE` |
| Camera attribution by runtime | **91.2 %** | 4,421.2 s attributable to a named body / 4,846.625 s | FCPXML spine; 425.4 s inside compound clips unattributed |
| **Embedded-timecode coverage by runtime** | **38.5 %** | 1,867.3 s (DJI 1,791.6 + OM-1 75.7) / 4,846.625 s | Appendix A §A.2 |
| Telemetry-stream presence by runtime | **37.0 %** | 1,791.6 s (DJI only) / 4,846.625 s | Appendix A §A.2 |
| Device registry coverage | **75.0 %** | 3 bodies registered / 4 bodies used | `cameras.yaml` vs SOURCES + lock |
| **GPS coverage** | **0.0 %** | 0 `.SRT` sidecars / 46+ DJI clips | `find -iname '*.srt'` |
| Timing-delta categorization | **100 %** | 25 categorized / 25 logged | RE-001 `ESS_VALIDATION_REPORT` |
| Fixture probes passed | **100 %** | 3 / 3 | RE-001 |

**No composite. No average of the above.** Nine measurements, nine denominators, nine sources.

## 3. Executive Verdict
> **Ready for high-confidence editorial synchronization. Acquisition telemetry is available but
> uncollected — enable GPS-for-Action and consume embedded timecode before the next production.**

## 4. What the verdict is based on, stated plainly
The editorial chain is sound: the four-source hash chain closed, the offset model is zero with no
drift, and 91.2 % of runtime sits inside a governed segment. Synchronization is not at risk.

The **acquisition** chain is where the value is sitting unclaimed. Timecode is read today and thrown
away. Telemetry is detected today and never decoded. Camera-native proxies carrying both are ignored in
favour of transcoding. The 4K masters existed while the visual pass ran on a 320×180 watermarked proxy.

And the single most costly item is not an engineering gap at all: **the ride — the centrepiece of the
film — could have carried a GPS track, and did not, because a camera setting was off.** The registry
recorded the camera as capable. Capability is not configuration.

## 5. Why this is not "Capture Readiness: 62 %"
A composite of the nine percentages above would land somewhere in the sixties and would be
**actively misleading**: it would average a 0 % that costs nothing to fix next shoot against a 91.2 %
that took a governed sprint to earn, and it would hide the fact that **not one row in §1 is blocked**.

The verdict in §3 is one sentence and it tells a producer exactly what to do on Monday. That is the
whole argument of WET-SPEC-REPORT-001, demonstrated rather than asserted.
