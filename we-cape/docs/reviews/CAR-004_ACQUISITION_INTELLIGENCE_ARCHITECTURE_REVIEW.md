# CAR-004 — Acquisition Intelligence Architecture Review
## Governance Status
Document Type: Collaborative Architecture Review — Package · Status: **OPEN — AWAITING ENGINEERING REVIEW**
Date opened: 2026-08-22 · Authority: Executive Producer · Predecessor: CAR-003 (CLOSED)
CAR number assigned on convening per CAR-001 Rev A amendment A1.
**Implementation is not authorized.** CAR wraps the review · ADR records the decision · the Work Order
executes it.
Independence disclosure (CAR-001 A4): this package was drafted by the same party that executed
Sprint 3A and CAR-003. Compensating controls: every current-state claim is sourced to a file, a line
or reproducible `ffprobe` output; no proposal is recommended for construction; Executive review and a
required ADR stand between this package and any build.

**Amendment 2 (2026-08-22).** The Executive Ruling on `DWR-010` — *extend GAP-03* — landed while this
package was open and **resolves review question 7 before review begins**. Candidate S-5 is rewritten,
Q7 is closed, and the ruling is now normative as `WET-SPEC-REPORT-001 v1.0`. **Appendix B** applies it
to this production as a worked example.

---

## 1. Executive Summary
The Executive Team has directed that Capture Intelligence be reviewed as architecture rather than
appended to a hygiene review, and reframed at a level above cameras:

> **Capture Intelligence becomes one module. Acquisition Intelligence becomes the architecture.**

The reframe is correct and the evidence supports it. WE CAPE already acquires far more than video:
FCPXML, SRT, GPX, offload manifests, stills, contributed clips, release metadata, proclamation
documents, prompts and generation records all move through the platform today under separate,
uncoordinated handling. *Capture* names the camera path. *Acquisition* names what the platform
actually does.

This package establishes current state from evidence, answers the Executive Question, and frames the
decisions the review must make. **It proposes no architecture.** §6 offers candidate shapes for the
reviewers to argue with, explicitly marked as options, not recommendations.

---

## 2. Review Mission
Review and standardize the WE CAPE **Acquisition Intelligence Layer**, of which Capture Intelligence
is the first and best-evidenced module. Determine what becomes constitutional, what remains
implementation, and what should not be built.

## 3. Scope (as directed)
**In scope:** capture devices (current · future · supported · unsupported) · device profiles
(capabilities · metadata · limitations) · capture modes (interview · ride · 360 · aerial · body ·
static · walking · drone · time-lapse) · metadata (GPS · heading · altitude · IMU · orientation ·
time · lens · frame rate · codec · audio) · whether `CAPTURE_DEVICE_REGISTRY` becomes constitutional ·
whether every production emits `PRODUCTION_CAPTURE_PROFILE.yaml` · asset relationships
(device → clips → edits → final utilization) · dashboard surfacing · new production-intelligence
metrics · a Capture Readiness Score.

**Explicitly out of scope for this review:** implementation · storage internals (PRS-001, deferred) ·
any change to the frozen four-engine constitution · any change to picture lock.

---

## 4. Current State — established by evidence, not recollection
Full device evidence in **Appendix A**. Summary of what exists today:

### 4.1 What is already built
| capability | where | state |
|---|---|---|
| Camera identity from footage, not labels | `scripts/camera_identity.py`, `scripts/probe_camera.py`, `cameras.yaml` | **Production-proven** — the card labelled `DJIAction6` holds Action 5 Pro footage; content-based correction caught it |
| Timestamp fallback chain (filename → metadata → file_stat), levels + confidence | `wecape/capture/timestamp.py` | LOCKED (§5) |
| Embedded timecode extraction | `wecape/capture/proxy.py::_get_timecode()` | Built — **consumed only to re-stamp proxies** |
| Telemetry-stream detection | `scripts/probe_camera.py::stream_signals()` | Built — **nothing consumes the result** |
| SRT sidecar telemetry (GPS + drift-free time) into a separate `telemetry.db` | `scripts/srt_telemetry.py`, `SPEC_SRT_Telemetry.md` | BUILT · gated `false` · **no `.SRT` data exists in this production** |
| Per-card offload manifests | `_offload_manifest.json` (tool · version · created · source · camera · shoot · destinations · files · summary) | Written per card, **not aggregated** |
| Proxy generation with timecode preservation | `wecape/capture/proxy.py` | Built — **ignores camera-native `.LRF`/`.lrv` proxies already on the card** |
| Grouping / multicam engine | `wecape/capture/grouper.py` | Suite-validated, **never production-used for an edit** (GAP-05, DWR-020) |
| Local read-only dashboard | `scripts/dashboard.py` → `wecape_dashboard.html` | Prototype; reads the capture registry only |
| Reconcile audit | `scripts/reconcile.py` | Built; ungoverned |

### 4.2 What is decided and deferred
`DWR-014` DJI/Insta360 telemetry parser (deferred with an explicit trigger) · `DWR-015` camera identity
multi-layer system (*"foundational, not polish"*) · `DWR-016` bring `cameras.yaml` under governance ·
`DWR-017` SRT telemetry validation tests · `DWR-021` packaged dashboard.

### 4.3 What is missing
No acquisition-side registry is governed · no `PRODUCTION_CAPTURE_PROFILE` exists · no capture-mode
vocabulary exists anywhere in the corpus · non-video acquisitions (GPX, documents, contributed media,
stills) have no common handling · the intelligence layer has **zero custody rows** against 726 camera
rows (GD-12).

**And material enters the building without meeting any of it.** During this review the Executive
Producer identified drone footage at `~/Desktop/Drone`. It was probed (Appendix A §A.5): five files,
89 MB, never offloaded through `offload_cards.py`, no manifest, no registry row, no hash, no shoot
association. Its folder name, its filename convention and its own `version.txt` identify three
different devices. Its video is an FFmpeg re-encode with all camera metadata already destroyed.

That single folder is the clearest statement of the problem this review exists to solve: **the gap is
not capability, it is custody at the moment of acquisition.**

---

## 5. THE EXECUTIVE QUESTION
> *"What metadata can WE CAPE leverage today with little or no additional engineering?"*

Answered in four tiers by **cost**, each item sourced. The headline: **the highest-value items are
already extracted by code that runs today — they are simply not consumed by anything.**

### TIER 0 — Already extracted. Not consumed. Cost: wiring, not building.
| # | metadata | already read by | not consumed by | what it would unlock |
|---|---|---|---|---|
| 0.1 | **Embedded timecode** (present on Action 6, Action 5 Pro, OM-1 — and on the `.LRF` proxies) | `proxy.py::_get_timecode()` | the timestamp chain, the grouper, chronology, FCPXML export | A **stronger sync signal than filename or `creation_time`** — timecode is what the camera thought the time was, frame-accurately. Today it is read and thrown away except for proxy re-stamping |
| 0.2 | **Telemetry-stream presence + handler name** | `probe_camera.py::stream_signals()` | anything downstream | *Which clips carry GPS/IMU* becomes answerable **without decoding a single byte** of proprietary payload |
| 0.3 | **Offload manifests** (`tool·version·created·source·camera·shoot·destinations·files·summary`) | `scripts/offload_cards.py` | production intelligence, dashboard, utilization | A complete acquisition ledger per production already exists on disk, unaggregated |

### TIER 1 — One `ffprobe` call away. No new dependency, no new format knowledge.
Codec · resolution · frame rate · duration · audio codec/channels/sample-rate · stream count · data-stream
handler names · **drop-frame vs non-drop-frame** (free — it is the `;` vs `:` in the timecode string).

Immediate metrics available from these alone: conform burden per production (this one has **four frame
rates and two timecode conventions** into a 24p sequence) · capture diversity · source-audio quality
(the OM-1 is the only **PCM** source in the kit; everything else is AAC) · resolution/aspect mix ·
device utilization by duration.

### TIER 2 — Built, but needs a *setting* or a *flag*, not engineering.
SRT sidecar telemetry: the code exists and is gated `false`. **This production wrote zero `.SRT`
files** despite `cameras.yaml` recording `gps_for_action: true` for both DJI bodies. The gap is
operational, not architectural — see Appendix A §A.3.

### TIER 3 — Genuine engineering. Not "little or no".
Decoding the `CAM meta` / `DJI meta` binary streams (GPS, IMU, heading, altitude) — this is
`DWR-014`, deferred with a trigger, and it must handle **two different handler names for the same
payload across two bodies of the same brand** (A.2-b). Insta360 `.insv` telemetry is proprietary and
not surfaced by `ffprobe` at all.

### The honest summary
> **Tiers 0 and 1 are almost entirely free, and they are where the production-intelligence value is.
> Tier 3 is where the excitement is. They are not the same tier.**

The single highest-value item is **0.1 — embedded timecode.** The platform already reads it, on three
of four bodies, including on the tiny proxy files, and currently uses it for nothing but proxy
compatibility.

---

## 6. Candidate shapes for review — **options, not recommendations**
Offered so reviewers have something specific to disagree with. **None is proposed for construction.**

| id | candidate | argument for | argument against |
|---|---|---|---|
| S-1 | `ACQUISITION_REGISTRY` as the constitutional artifact, with `CAPTURE_DEVICE_REGISTRY` as one profile class within it | Matches the Executive reframe; one contract covers video, stills, GPX, documents, contributed media | A registry defined before its second asset class exists risks being shaped entirely by cameras anyway |
| S-2 | `CAPTURE_DEVICE_REGISTRY` constitutional now; acquisition generalized later from evidence | `cameras.yaml` already exists and is production-proven; promoting it is `DWR-016`, a Quick Win | Risks the exact naming/discoverability failure CAR-003 just documented — a second registry culture |
| S-3 | `PRODUCTION_CAPTURE_PROFILE.yaml` emitted per production | Makes capture readiness, conform burden and device utilization measurable per production; feeds the dashboard and the PIR | Another generated artifact to keep regenerate-only (DOC-002); value unproven until a second production exists to compare |
| S-4 | Capture-mode vocabulary (interview · ride · 360 · aerial · body · static · walking · time-lapse) as a governed enum | Sprint 3A's DIE-V invented ad-hoc event classes for exactly these; a shared vocabulary would let capture and editorial intelligence speak | Mode is often *interpretation*, not observation — assigning it at capture risks writing NIE-class judgement into a DIE-class registry (ADR-009 boundary) |
| S-5 | **Acquisition Readiness *Report*** — component metrics → objective percentages → Executive Verdict, per `WET-SPEC-REPORT-001` | A.3 shows one missed setting cost this production its route GPS; **Appendix B** demonstrates the report against real evidence and the verdict is actionable in one sentence | Cost is in the *collection* of component evidence, not the format; needs a decision on whether it is generated per production (`S-3`) or on demand |
| S-6 | Extend the existing dashboard rather than build an Executive Dashboard | R6 accepted in CAR-003; the dashboard exists and honours zero-network | Capture Intelligence may need surfaces the current prototype was not shaped for |

**S-5 is settled in form, open in scope.** The Executive Ruling of 2026-08-22 extended GAP-03: a
Capture Readiness **Score** is prohibited; a Capture Readiness **Report** is the required shape.
`WET-SPEC-REPORT-001 v1.0` is in force and supersedable only by an ADR that explicitly says so. What
remains for this review is *when* the report is produced and *what collects its component evidence* —
not whether it may be a number.

---

## 7. Risks & Assumptions
| id | risk | note |
|---|---|---|
| R-1 | **Architecture defined from one production's kit** | Four bodies, one shoot, one genre. X3, GO 3, iPhone and DJI Mic have **zero evidence** anywhere reachable by this review; GoPro and DJI Drone have exactly one uncustodied, re-encoded artefact each (A.5) — enough to prove they are in the building, **not** enough to profile them. Designing profiles for any of these would be speculation, which CAR-003's mission text forbids |
| R-7 | **Designing for camera-original files the platform may never receive** | `DJI_0047.MOV` reached the operator already transcoded (`vendor_id=FFMP`). Tier 3 telemetry parsing is worth nothing against a re-encode. An acquisition layer must decide what it does with material whose metadata was destroyed *before* it arrived |
| R-2 | **Registry proliferation** | ADR-009 named engine proliferation the top governance risk; WET-SPEC-GATE-001 §7 named gate proliferation the same risk in a new costume. Registry proliferation is the third costume |
| R-3 | **Telemetry parsing silently half-working** | Two handler names for one payload (A.2-b). DOC-001 applies before the first parser line |
| R-4 | **Boundary erosion** | Capture modes and readiness scores are close to interpretation. ADR-009 keeps interpretation in NIE via `nie.*` enrichment. An acquisition layer that classifies *meaning* has crossed a frozen line |
| R-5 | **Privacy regression** | GPS is deliberately excluded from the pipeline path and kept in a separate `telemetry.db`, hashed on egress (D1, P7). Any acquisition registry that centralizes metadata must not quietly re-merge location PII |
| R-6 | **Solving for the wrong camera** | The best-instrumented bodies contribute least; the X5 carries 53% of the film with no timecode and no data streams (A.2-d) |
| A-1 | Assumption | `exiftool` is available in normal operation (it was not in this review's environment), so EXIF-tier fields are richer in practice than Appendix A can show |

---

## 8. Engineering Review Questions
1. **Constitutional alignment** — does an Acquisition Intelligence layer sit inside the frozen
   four-engine constitution as DIE-adjacent modules, or does it require an ADR to place it?
2. **Responsibility boundaries** — where does acquisition end and DIE extraction begin? Both read files
   and emit facts.
3. **Registry shape** — S-1 or S-2? One acquisition registry, or a capture registry generalized later?
4. **Constitutionality** — should `CAPTURE_DEVICE_REGISTRY` be constitutional, or is a governed
   extension registry (like `ENERGY_CURVE`) sufficient?
5. **Per-production profile** — does `PRODUCTION_CAPTURE_PROFILE.yaml` earn its regeneration cost?
6. **Mode vocabulary** — is capture mode observation or interpretation? Which engine owns it?
7. ~~**Score** — extend or overturn GAP-03's no-composite-score ruling?~~ **RESOLVED 2026-08-22 by
   Executive Ruling: EXTEND.** See `WET-SPEC-REPORT-001 v1.0`. Residual question for reviewers: what
   collects the component evidence in §1 of Appendix B, and is the report generated per production or
   on demand?
8. **Telemetry sequencing** — parse Tier 3 telemetry, or first exhaust Tiers 0–1 and measure what is
   still missing?
9. **Privacy** — how does a centralized acquisition view preserve the GPS separation D1/P7 guarantees?
10. **Custody at acquisition** — what should happen when material appears outside the offload path
    (A.5)? Is uncustodied material refused, quarantined, or ingested with a reduced-confidence
    provenance class? This is the question the `~/Desktop/Drone` folder actually asks.
11. **Missing capabilities / better alternatives** — what has this package failed to ask?

---

## 9. Requested Deliverables from Engineering Review
Executive assessment · recommended refinements · **GO / HOLD / REJECT** · required ADRs · a work order
if GO · implementation sequence · risks requiring mitigation · an explicit ruling on which of S-1…S-6
are in scope for a first increment.

## 10. Disposition Matrix
| item | Accept | Modify | Reject | Notes |
|---|:--:|:--:|:--:|---|
| Reframe to Acquisition Intelligence, Capture as module 1 | ☐ | ☐ | ☐ | |
| S-1 acquisition-first registry | ☐ | ☐ | ☐ | |
| S-2 capture-first registry | ☐ | ☐ | ☐ | |
| S-3 `PRODUCTION_CAPTURE_PROFILE.yaml` | ☐ | ☐ | ☐ | |
| S-4 capture-mode vocabulary | ☐ | ☐ | ☐ | |
| S-5 Acquisition Readiness **Report** (form settled by ruling; scope open) | ☐ | ☐ | ☐ | `WET-SPEC-REPORT-001` in force |
| S-6 extend existing dashboard | ☐ | ☐ | ☐ | |
| Tier 0 wiring as a first increment | ☐ | ☐ | ☐ | |
| Custody-at-acquisition rule for uncustodied material | ☐ | ☐ | ☐ | raised by A.5 |

## 11. Executive Decision
**Decision:** GO · GO WITH MODIFICATIONS · HOLD · REJECT — `______`
**Rationale:** `______`  **Required ADR:** `______`  **Authority / date:** `______`

## 12. Success Criteria
CAR-004 is complete when independent engineering review is recorded, executive disposition is
recorded, required ADRs exist, implementation authority is explicitly granted or withheld, and every
recommendation traces to documented evidence.

## 13. Lessons Learned
*(To be completed at disposition.)*

## 14. References
`CAR-001` Rev A (standard) · `CAR-003` findings + disposition · `records/dwr/DEFERRED_WORK_REGISTER.yaml`
(DWR-014…017, 021, 032) · `WET-WF-001` Gap Register GAP-02/03/04/05 · `SPEC_SRT_Telemetry.md` ·
`SPEC_Production_Health_Report.md` · `UI_Dashboard_Design_Guidelines_v2.md` ·
`CAPE-RAT-20260813` clauses 9–15 · `ADR-009` (engine boundaries) · `DOC-001`, `DOC-002` ·
**Appendix A — Capture Capability Matrix** · **Appendix B — Acquisition Readiness Report (worked
example under `WET-SPEC-REPORT-001`)** · `WET-SPEC-REPORT-001 v1.0` (Platform Reporting Standard) ·
`DWR-010` (Completed, 2026-08-22).
