# W.E. C.A.P.E. — Technical Specification
## Production Intelligence Platform · v1.0 · Contract-Grade
**Workman Experience Technologies LLC — Confidential**
**Status: Platform Phase 2 (in progress) · W.E. C.A.P.E. CAPTURE Phase 1 (in progress)**

---

## 0. About This Document

### 0.1 Purpose
This is the authoritative technical specification for the **W.E. C.A.P.E. Production
Intelligence Platform** and its first product, **W.E. C.A.P.E. CAPTURE**. It defines the
principles, interfaces, and requirements that govern all platform development. It is
suitable for two audiences without modification:

- **Internal development governance** — the binding reference for what may and may not be
  built, and how.
- **External contractor engagement** — a self-contained specification a qualified vendor
  can read, run, and extend against, without access to tribal knowledge.

### 0.2 How to read it — the platform / product split
The document is deliberately split so that shared platform law is never entangled with
product detail:

- **PART I — PLATFORM (W.E. C.A.P.E.)** is **binding on every product** the platform ever
  ships (CAPTURE, ARCHIVE, PULSE, EVALUATE). A requirement in Part I applies to CAPTURE
  and to every future product equally.
- **PART II — W.E. C.A.P.E. CAPTURE** applies **only to the first product**. It inherits
  all of Part I and adds CAPTURE-specific requirements on top.

Where Part II must deviate from a Part I default, it does so explicitly and with
justification (see §21, Documented Deviations). Silent deviation is non-compliant.

### 0.3 Normative language
The key words **MUST**, **MUST NOT**, **SHALL**, **SHOULD**, **MAY**, and **REQUIRED** are
used per RFC 2119. **🔒 LOCKED** marks a decision that MUST NOT be changed by any
implementation without prior written approval from the Client.

### 0.4 Source of truth
This specification is derived from the implemented reference system in the repository
(`~/Curser/we-cape/`, canonical package `wecape/`). Where this document and the code
disagree, that is a defect to be reconciled — the code is not licensed to drift from these
principles. Companion living documents are normative by reference: `CLAUDE.md` (build
context), `SECURITY_RISK_ANALYSIS.md`, `SPEC_Additive_Ingest_Found_Footage.md`,
`SPEC_Production_Health_Report.md`, and `UI_Dashboard_Design_Guidelines_v2.md`.

---

# PART I — PLATFORM (W.E. C.A.P.E.)
*Binding on every product. CAPTURE and all future products inherit this Part in full.*

## 1. Platform Overview & Product Hierarchy

### 1.1 What W.E. C.A.P.E. is
**W.E. C.A.P.E.** (Content Asset Production Ecosystem) is a **local-first, deterministic
production intelligence platform** for independent content creators and studios. It ingests,
organizes, audits, and — over its roadmap — reasons about production media, while keeping
the creator's machine the source of truth and the creator the owner of all data.

The platform brand leads. **W.E. C.A.P.E. is announced before W.E. C.A.P.E. CAPTURE ships**,
and CAPTURE is described as "the first product from W.E. C.A.P.E."

### 1.2 Module architecture
`C.A.P.E.` names the four production-intelligence modules:

| Module | Role | Tagline | Status |
|---|---|---|---|
| **CAPTURE** | Automated multi-camera ingest, scaffold, proxy | *Capture every moment. Miss nothing.* | First product — in build |
| **ARCHIVE** | Storage intelligence, cross-project dedup, lineage | *Every frame. Forever.* | Future (J5) |
| **PULSE** | Production health & operational intelligence | *The heartbeat of production.* | Future (J4) |
| **EVALUATE** | Editorial/quality intelligence, content→insight | *Turn content into intelligence.* | Future (J3–J4) |

### 1.3 Entity & brand separation
| Entity | Owns |
|---|---|
| **Workman Experience Technologies LLC** | The W.E. C.A.P.E. platform IP, all products, and future technology IP |
| **The Workman Experience, LLC** | The creator brand — content, media/press, merchandise, sponsorships, independent content IP |

Platform technology IP and creator-brand IP MUST remain distinct. Product code, registry
data, and specifications belong to the technology entity.

## 2. Architectural Principles (P1–P7) — 🔒 LOCKED

These seven principles are the platform's constitution. Every product, stage, and feature
MUST satisfy them. They are non-negotiable without written approval.

- **P1 — Determinism.** Identical input + identical configuration MUST produce identical
  output, on every run and every machine. No stage may introduce nondeterminism (wall-clock
  ordering, hash-map iteration, unseeded randomness).
- **P2 — Privacy by Design.** The local processing engine MUST make **zero network calls**.
  Privacy is the default, not a setting. (Enforced in CI — see §6.2.)
- **P3 — Auditability.** Every run MUST produce a complete, tamper-evident manifest of what
  it did. No silent decisions.
- **P4 — Extensibility Without Coupling.** New capability is added as new stages/adapters;
  a new stage MUST NOT modify or depend on the internals of an existing stage.
- **P5 — Registry Continuity.** The registry is non-destructive. Content enrichment MUST
  NOT be overwritten or nulled (field-preserving upsert); only empty no-op runs are pruned.
- **P6 — Staged Intelligence.** AI is additive and never foundational. AI features MUST NOT
  be required for the core pipeline to function; v1 of any product ships zero AI.
- **P7 — Creator Data Sovereignty.** The creator owns all production data. No data leaves
  the machine by default — ever. Any egress is explicit, opt-in, and creator-controlled.

## 3. Locked Architecture Decisions — 🔒 LOCKED

| Decision | Commitment |
|---|---|
| Platform brand leads | W.E. C.A.P.E. announced before CAPTURE ships |
| Local-first core | The creator machine is always the source of truth |
| Cloud is optional | No data leaves the machine by default |
| In-house core | CAPTURE, and future EDIT/ARCHIVE cores, are built internally |
| Open API from J3 | Internal extension seams now; public API at J3 |
| Registry from day one | Every stage writes to a local SQLite registry |
| AI is additive | v1 ships zero AI features (P6) |
| Compliance first-class | Auditability is built into every stage (P3) |
| Post-quantum readiness | CRYSTALS-Kyber for any future CloudSyncAdapter at J3 |

## 4. Shared Platform Interfaces (Normative)

All products MUST build on these shared contracts. They are the platform's extension
surface and become the **public extension API at J3**.

### 4.1 PipelineStage (the universal stage contract) — 🔒 LOCKED
Every unit of processing — current or future, first-party or third-party — MUST implement
`PipelineStage` (`wecape/core/stage.py`):

```python
class PipelineStage(ABC):
    stage_id: str
    stage_version: str
    stage_description: str
    def validate_input(self, context: StageContext): ...
    def execute(self, context: StageContext) -> StageResult: ...
    def on_error(self, error: Exception, context: StageContext) -> dict: ...
    def write_registry(self, result, context) -> None:  # mandatory, not overrideable
        context.registry_writer.write_stage_result(...)
```

**Stage rules (MUST):** stages MUST NOT import from other stages; MUST write to the registry
only via the injected `registry_writer`; MUST NOT make network calls; MUST be idempotent
(re-execution on the same input+config is a safe no-op or byte-identical result).

`StageContext` injects `registry_writer` and `sync_adapter` — never imported directly — so
stages remain decoupled (P4) and testable.

### 4.2 SyncAdapter (egress is pluggable and off by default)
Any data leaving the machine MUST pass through a `SyncAdapter` (`wecape/core/sync.py`). The
v1 default is `LocalOnlySyncAdapter` — **every method is a safe no-op with zero network
calls** (P2/P7). LAN and cloud adapters are future, opt-in, and MUST be explicitly selected.

### 4.3 Registry (the shared data spine) — 🔒 LOCKED
Every product reads and writes one local SQLite registry at `~/.wecape/registry/wecape.db`.
Four required tables: `runs`, `content`, `preferences`, `schema_version` (current schema
**v3**, migrations automatic and lossless). The registry MUST:

- record every run and every content item, keyed by **content SHA-256**;
- apply **field-preserving upsert** — `col = COALESCE(excluded.col, existing.col)` so new
  non-null enrichment wins and existing enrichment is never nulled (P5);
- exclude empty runs (`file_count = 0`) from aggregate queries and prune them on finalize;
- carry derivation lineage (`source_clip`, `source_clip_sha`) for curated selects (schema v3).

The registry is the trust anchor for auditability (P3) and the substrate future products
(ARCHIVE, EVALUATE) query. It is created day one, before those products exist.

### 4.4 RunManifest (tri-format audit record)
Every run MUST emit a `RunManifest` in machine-readable (JSON), human-readable (HTML), and
interchange (XML) forms. The manifest field is `we_cape_version` (auto-migrated from the
legacy `we_forge_version`, schema v2).

## 5. Data Governance & Sovereignty

- **Local-first, air-gap capable.** The core engine MUST function with no network, no cloud
  dependency, no telemetry, no analytics, and no callbacks (P2/P7).
- **PII is hashed, never logged in plaintext.** All path fields in audit logs MUST store the
  SHA-256 of the path string, not the path. Any GPS/location data MUST be hashed in logs.
- **Creator ownership.** All registry and production data belong to the creator (P7). Egress
  is explicit and creator-controlled; the default posture leaks nothing.
- **Human notes are separated from deterministic output.** Mutable human annotations live in
  a separate store (`~/.wecape/annotations.db`), never mixed into the deterministic registry
  (preserves P1: engine output vs. human notes stay distinct).

## 6. Security & Compliance Posture

The platform's living security reference is `SECURITY_RISK_ANALYSIS.md` (threat model,
controls, decision register), normative by reference. Platform-level requirements:

### 6.1 Ordering of risk
For a local-first creator platform the risk order is **data loss → credential exposure →
remote intrusion**. Controls MUST be prioritized in that order; exotic mitigations MUST NOT
precede fundamentals (working backups, key handling, disk encryption).

### 6.2 The zero-network invariant is enforced, not asserted (P2)
A static test MUST fail the build if any network-capable module is imported anywhere in the
engine package (`wecape/`). The only path to an exception is an explicit, code-reviewed
allowlist entry (reserved for a future opt-in cloud adapter). "Zero network" is therefore a
CI-enforced invariant, not a promise.

### 6.3 Auditability & tamper-evidence (P3)
Every run MUST produce complete logs plus a SHA-256 manifest over those logs. Re-verification
of the manifest MUST detect any post-hoc modification.

### 6.4 Credential & egress hygiene
Credentials (cloud tokens, signing keys) live outside the repository and outside any
backed-up path; any offsite copy of registry/notes MUST be encrypted (client-side).
Inventory and rotation are tracked in `CREDENTIAL_INVENTORY.md`.

## 7. Platform Roadmap & Juncture Map

AI capability is layered in over **junctures J1–J5**, each additive (P6) and never required
by the core:

| Juncture | Capability | Hardware delta | Product surface |
|---|---|---|---|
| **J1** | Camera AI identification | none | CAPTURE — removes setup friction |
| **J2** | Shot-quality scoring + content tagging | ANE (free on M1+) | CAPTURE/EVALUATE |
| **J3** | Audio temporal alignment; **public API**; cloud adapter | 32 GB RAM rec. | EVALUATE + platform API |
| **J4** | Highlight detection + rough-cut XML | M1 Pro rec. | PULSE / editorial |
| **J5** | Cross-project registry + lineage at scale | NVMe + storage | ARCHIVE |

**What MUST NOT be built ahead of its juncture:** public API before J3; cloud sync while
`LocalOnlySyncAdapter` is the v1 default; any AI feature in a product's v1; downstream
products (ARCHIVE/PULSE/EVALUATE) before CAPTURE has earned them and the registry holds the
data they require.

---

# PART II — W.E. C.A.P.E. CAPTURE (First Product)
*Inherits all of Part I. Adds the product-specific requirements below.*

## 8. CAPTURE Overview & Scope

**W.E. C.A.P.E. CAPTURE** is a deterministic multi-camera **ingest, scaffold, and proxy**
engine: it takes an unorganized folder (or offloaded cards) of footage from mixed cameras
and produces a classified, grouped, variant-aware, audited output tree plus edit-ready
proxies — with a complete registry record and manifest.

- **Phase 0 (complete):** deterministic ingest, classification, grouping, variant detection,
  metadata output, five-stream logging, tamper-evident manifest.
- **Phase 1 (in progress):** proxy generation, pre-flight estimation, performance
  parallelism, GPS metadata extraction, grouping-accuracy validation.
- **What CAPTURE replaces:** the manual stack of Hedge (offload) + Finder organization +
  PluralEyes (sync) + Kyno (review) — as one deterministic, auditable pipeline.

CAPTURE ships **zero AI** in v1 (P6). Its intelligence is deterministic.

## 9. System Flow — 🔒 LOCKED (sequential, auditable)

The pipeline is deterministic and sequential; each stage produces auditable output before
the next begins. No stage may be skipped or reordered.

```
Stage 0  Pre-flight    disk-space check · first-run EULA acceptance · PII filename scan ·
                       operator attestation (tty-guarded, CI-safe) · SHA-256 of input path
Stage 1  Ingest        parallel discovery (default 8 workers) · streaming SHA-256 per file
                       (50 GB+ safe) · optional duplicate-content detection
Stage 2  Timestamp     Level 0 filename → Level 1 ffprobe creation_time → Level 2 mtime (§10)
Stage 3  Classify      generic prefixes → reference folders → generic folders → camera
                       patterns → audio field recorder → reference ext → default generic
Stage 4  Group         UTC window (§12) · SHA-256 group IDs · per-camera offset correction
Stage 5  Variants      indexed/suffix/keyword patterns · parent selection · orphan promotion
Stage 6  Output        locked directory structure (§14) · symlink | copy | move
Stage 7  Audit close   five log streams flushed · SHA-256 manifest written
```

The stage seam is real: `run()` routes through `run_stages()` by default
(`pipeline.engine: stages`), with a `legacy` mode retained only as rollback. The two engines
are equivalence-validated on real multicam footage.

## 10. Detection Priority — 🔒 LOCKED (timestamp fallback chain)

Timestamp resolution MUST attempt higher-priority methods first and MUST NOT leave any file
without a resolvable timestamp:

```
Level 0  filename parse         confidence: high   (DJI, Insta360, GoPro, iPhone, OM System)
Level 1  ffprobe creation_time  confidence: high   (UTC from container metadata)
Level 2  file_stat_mtime        confidence: low    (flagged; file processed, never blocked)
```

A Level-2 resolution MUST be processed (not blocked) and logged with `timestamp_confidence:
low` and a WARNING event; its grouping eligibility is flagged `low_confidence: true`.

## 11. File Classification Engine — 🔒 LOCKED (four categories)

Every ingested file MUST be classified into exactly one of: **Camera**, **Camera-Audio**,
**Generic**, or **Reference**. Classification is deterministic and config-driven. **All files
MUST be ingested; no file may be dropped or ignored.**

**Recognized camera sources** (filename patterns → source; extensions):

| Source | Key patterns | Extensions |
|---|---|---|
| DJI | `^DJI_`, `^DJI\d`, `DJI_\d{4}` | `.mp4 .mov .jpg .dng` |
| Insta360 | `^ISD_`, `^VID_`, `_00_\d+\.insv`, `^PRO_VID` | `.insv .insp .mp4 .jpg` |
| iPhone | `^IMG_\d{4}`, `^MOV_\d{4}`, `^RPReplay` | `.mov .mp4 .heic` (video only for camera) |
| GoPro | `^GOPR\d+`, `^G[HXLP]\d{6}` | `.mp4 .lrv .thm` |
| Sony | `^C\d{3}S\d{4}`, `^CLIP\d+`, `^M2U\d+` | `.mxf .mp4 .mov` |
| Canon | `^MVI_\d+`, `^_MG_\d+` | `.mov .mp4 .cr3` |
| Blackmagic | `^Blackmagic_`, `^BMPCC` | `.braw .mp4 .mov` |
| OM System | `^P\d{7}`, `^P[A-C]\d{6}` | `.mov .mp4 .orf` |

**Per-body distinction (§12 sources):** where footage is in a per-camera folder, the specific
physical body is resolved (e.g. *DJI Osmo Action 5* vs *Action 6*, *Insta360 X5*,
*OM System OM-1*), because a physical camera equals a grouping source. `camera_id` MUST be
persisted to the registry.

**Camera-Audio:** field-recorder files (Zoom, Sound Devices, Tascam — configurable
`field_recorder_patterns`) are `camera_audio` and eligible for multicam *association* by
timestamp; other audio is `generic` unless container metadata identifies it as production
camera audio. Audio is NEVER classified as Reference.

## 12. Multicam Grouping Engine — 🔒 LOCKED

- **Eligibility:** only Camera (and associated Camera-Audio) files group. A valid group
  REQUIRES ≥ 2 distinct camera **sources** (not merely 2 files).
- **Window:** ±N seconds UTC. RFQ-locked default is **5s**; production is calibrated to
  **15s** — a documented, field-validated deviation (see §21).
- **Group ID:** SHA-256 of the sorted member-path list — deterministic across runs (P1).
- **Per-camera clock offset:** configurable UTC offsets correct known clock skew *before*
  grouping; the fallback chain is never bypassed to compensate.
- **Membership:** a file MUST NOT belong to more than one group. All conflict resolution MUST
  be deterministic (closest timestamp, then alphabetical filename tiebreak).
- **Output:** `MULTICAM/MCG_{sha256_prefix}.json` per group.

## 13. Variant Detection & Derivation Lineage — 🔒 LOCKED

- **Patterns:** Indexed `(1) [2]`; Suffix `_v2 _edit _final _export _rev1`; Keyword
  `copy final backup duplicate`.
- **Parent selection (configurable, uniform per run):** `largest_file` (default) |
  `lowest_index` | `earliest_timestamp`.
- **Orphan rule (LOCKED):** a variant pattern with no matching base file is reclassified as
  standalone; the variants object is NOT populated; log `variant_pattern_no_base_found`.
- **Curated selects & lineage (schema v3):** selects named `<source_stem>_sel<NN>` are treated
  as *derivations*, not duplicates. `content.source_clip` / `source_clip_sha` record lineage
  (opt-in, additive) — feeding ARCHIVE (J5) cross-project lineage.

## 14. Output Structure & Metadata Schema — 🔒 LOCKED

**Directory structure:** `CAMERA/DATE/SOURCE`, `REFERENCES/` (at project root, not inside
date folders), `MULTICAM/`, `LOGS/`, and `PROXIES/`. Multi-day shoots MUST separate files by
resolved calendar date. `{run_id}_index.json` is written at the project root as the single
machine-readable summary.

**Index JSON** (`{run_id}_index.json`) records: `run_id`, `input_path_hash`, timestamps,
`files_discovered/processed/filtered`, `camera/generic/reference/error_files`,
`groups_formed`, `variant_groups`, `throughput_gb_hr`.

**Multicam group JSON** records `group_id`, `window_seconds`, and per-member
`{path_hash, source, timestamp, confidence}` — paths hashed, never plaintext.

## 15. Logging & Audit — 🔒 LOCKED (five streams + manifest)

Every run MUST emit all five streams plus a manifest, with **all path fields SHA-256-hashed**:

| Stream | Content |
|---|---|
| `_ingest.json` | per file: path hash, size, mtime, content SHA-256 (if enabled) |
| `_classification.json` | per file: classification, camera_source, detection_method, size |
| `_grouping.json` | groups + members + confidence; ungrouped camera files with reason |
| `_variants.json` | variant groups, parent rationale, orphan-promotion events |
| `_errors.json` | per error: path hash, stage, error_type, message |
| `_manifest.json` | SHA-256 of each of the five streams (tamper evidence) |

Strict audit mode (`registry.strict: true`) MUST abort the run if audit output cannot be
written (guarantees P3).

## 16. Edge-Case Matrix — 🔒 LOCKED (zero silent failure)

Every case MUST be handled deterministically without crash or data loss:

| Case | Required behavior |
|---|---|
| Zero-byte file | ingested, classified by extension/pattern, logged |
| Corrupt media | logged to errors stream with reason; pipeline continues |
| Special chars / Unicode / spaces | processed correctly; no crash |
| Read-only volume | symlink created; copy/move failure logged as error |
| Duplicate content (SHA-256) | flagged in ingest; second instance not re-processed |
| Output drive below min free | pre-flight blocks with clear error |
| System drive as output (copy, >10 GB) | pre-flight blocks with explicit warning |
| `ffprobe` not on PATH | warning; grouping skipped; pipeline continues |
| Re-run same input+output | idempotent — identical index JSON; no `_1` artifacts |
| Multi-day shoot | files separated by calendar date |
| Partial/corrupt downloads (`.crdownload/.part/.tmp`) | quarantined by the archive stage before ingest |

## 17. Configuration System

Configuration is **YAML only** (`wecape/config.yaml` + `wecape/profiles/`) — no database, no
external service. A centralized config layer handles load, profile-merge, override, and
validation. All LOCKED parameters are surfaced as config with LOCKED defaults; changing a
default requires the deviation process in §21.

## 18. Performance Requirements

Throughput floors on reference hardware (parallel; proxy time excluded from ingest floors):

| Tier | Dataset | Floor | Memory |
|---|---|---|---|
| Novice | 100 GB | ≥ 50 GB/hr | ≤ 16 GB |
| Pro | 500 GB | ≥ 120 GB/hr | ≤ 32 GB |
| Studio | 1 TB | ≥ 80 GB/hr | ≤ 64 GB |

**Proxy-generation gate:** a 79-proxy production shoot MUST complete in **< 90 minutes**.
Validated: hardware-accelerated VideoToolbox at 4 workers completes the reference set in
**34 minutes** (MG-04) and full production runs in **~50 minutes** (see Appendix B). The
engine MUST support ≥ 8 concurrent workers.

## 19. CAPTURE Toolchain (Operations Layer — distinct from the engine)

The following ship with CAPTURE as **operations tooling**. They are **read-only or additive
around** the deterministic engine and MUST NOT alter its determinism (P1) or its zero-network
guarantee (P2). Each is independently runnable; none is the only path.

| Tool | Role |
|---|---|
| `offload_cards.py` | Verified card offload — checksum-verified two-copy ingest before CAPTURE (Principle #1) |
| `new_shoot.py` (+ GUI) | Headless orchestration: manifest → offload → CAPTURE → FCPXML → Final Cut, with card detection, pre-flight space, audit trail, idempotency |
| `fcpxml_export.py` | FCPXML 1.9 export — multicam clips, chronological naming, per-camera Keyword Collections + Roles, stills, proxy media-reps, starter Project |
| `capture_to_fcp.sh` / `export_wizard.py` | One-command / novice-guided CAPTURE→FCP handoff |
| `dashboard.py` | Local, read-only (`mode=ro`), zero-network HTML window over the registry |
| `annotations.py` | Human notes store (separate `annotations.db`; out of the deterministic registry) |
| `reconcile.py` | Footage coverage audit — PROCESSED / UNPROCESSED / DUPLICATE vs the registry |
| `backup_holder_mac.sh` | 3-2-1 protection for `~/.wecape` (encrypted offsite) + bulk content |
| `security_check.py` | Environment audit for the security controls in `SECURITY_RISK_ANALYSIS.md` |

## 20. Acceptance Criteria

| # | Test | Pass condition |
|---|---|---|
| 1 | Classification accuracy | full acceptance suite green; ≥ 95% known-source accuracy on benchmark |
| 2 | Variant detection | all variant cases pass |
| 3 | Multicam grouping | all grouping cases pass; ≥ 95% accuracy on a simultaneous-recording dataset (Phase 1) |
| 4 | Output structure | tree matches §14 exactly |
| 5 | Comprehensive logging | five streams present every run; manifest re-verifies |
| 6 | Idempotency & robustness | re-run yields byte-identical index JSON; no `_1` artifacts |
| 7 | Performance | meets §18 tier floors within memory ceilings |
| 8 | Compliance metrics | full compliance set passes (with GPS + MG-03 resolved) |

**Current state:** the full engine test suite is green (**300+ tests**, `python3 -m pytest
wecape/tests/ -q`; pytest-free subset `python run_tests.py`). Phase-0 compliance is
**26/28**, gate CONDITIONALLY GREEN; the two open items (GPS extraction PI-04, grouping
accuracy MG-03) are Phase-1 scope. All new features REQUIRE tests before merge.

## 21. Documented Deviations (defensible, validated, intentional)

Deviations from a LOCKED default are permitted only when recorded here with justification.

| Deviation | From → To | Justification |
|---|---|---|
| Grouping window | 5s → **15s** | DJI/Insta360 field clock drift is 6–12s; at ±5s only 1/3 groups formed, at ±15s all 3 formed, 0 ungrouped. Field-validated. |
| Archive engine | disabled → **enabled** | Production safeguard: quarantines partial/corrupt downloads before the pipeline. Zero harm on a 95-file production run. |
| Per-body camera split | lumped DJI → **Osmo 5 / Osmo 6 distinct** | A physical camera is a grouping source; correctness fix, validated (split 29 → 19 + 10 exactly). |
| Proxy timecode | `-map_metadata -1` → **source timecode re-stamped** | FCP requires proxy + original to share a timecode range; fixes "Missing Proxy" on FCPXML import. |
| OM System OM-1 | added as first-class camera | Real kit expansion; classification already supported, front-door plumbing added. |

---

# PART III — ENGAGEMENT & APPENDICES

## 22. Engagement Model (for contractor use)

A vendor engaging against this specification is expected to **read, run, and extend** the
reference implementation — not replace it. The engagement is gated on the acceptance criteria
in §20, not on lines of code.

**Prerequisites.** Vendor personnel MUST execute an NDA and the Data Governance Agreement
before receiving benchmark datasets. Benchmark content is Confidential, authorized for
compliance testing only, MUST NOT be used for model training or public demonstration, and
MUST be deleted within 30 days of contract close.

**Suggested milestones** (commercial terms per vendor quote — not fixed by this document):

| Milestone | Gate |
|---|---|
| M1 — Integration | Full acceptance suite green (incl. any added scope); compliance delta document; code delivered to Client repo |
| M2 — Phase 1 features | GPS extraction + proxy generation implemented with completed Privacy Impact Assessments; MG-03 grouping-accuracy validated on a simultaneous-recording dataset |
| Final — Hardening | Full stress test on Client benchmark; macOS code signing + Apple notarization; attorney-reviewed Privacy Policy / ToS / DPA |

**Definition of done (every deliverable):** deterministic (P1), zero-network in the engine
(P2, CI-enforced), fully audited (P3), tests before merge, and no LOCKED deviation without a
§21 entry.

## Appendix A — Compliance Status Snapshot (at issue)

| Metric group | Status |
|---|---|
| PF-01–06 Pre-flight (attestation, EULA, disk checks, path hashing) | 6/6 PASS |
| AI-01–06 Audit integrity (coverage, completeness, tamper-evidence) | 6/6 PASS |
| PI-01–03 PII detection (scan, warning, hash-only logging) | 3/3 PASS |
| PI-04 GPS extraction | FAIL — Phase 1 (CAM-meta binary parser) |
| CL-01–04 Classification | 4/4 PASS (100% known-source coverage on benchmark) |
| MG-01/02/04 Grouping mechanism & determinism | 3/3 PASS |
| MG-03 Grouping accuracy | CANNOT TEST — Phase 1 dataset needed |
| OP-01–04 Output (idempotency, no system writes, temp cleanup) | 4/4 PASS |
| **TOTAL** | **26/28 — Gate: CONDITIONALLY GREEN** |

## Appendix B — Validated Benchmark & Production Runs

| Run | Source | Workers | Encoder | Runtime | Result |
|---|---|---|---|---|---|
| MG-04 | NVMe | 4 | VTB hwaccel | **34 min** | Proxy gate PASS (< 90 min) |
| Production `WEF_20260622_221150` | USB HDD | 4 | VTB hwaccel | 49.9 min | PASS — 79 proxies, 0 errors |
| Production `WEF_20260624_001707` (stages engine) | USB HDD | 4 | VTB hwaccel | 51.9 min | PASS — 95 files, 2 groups, 23 variants, 79 proxies, 0 errors; reproduced ground truth on the rewired engine |
| Camera-split re-CAPTURE `WEF_20260630_125435` | per-camera folders | — | no-proxy | — | DJI(29) → Osmo 6 (19) + Osmo 5 (10); Insta360 X5 (48) unchanged; `camera_id` persisted |

**Key finding:** storage was never the proxy-gate bottleneck; software decoding was. NVMe
gave a 2.96× improvement; the free `-hwaccel` flag gave ~16×.

## Appendix C — Repository Map & Entry Points

```
wecape/                  canonical package (source + tests)
  __main__.py            `python -m wecape` entry
  config.yaml, profiles/ configuration + run profiles
  core/                  stage.py · sync.py · manifest.py · config.py · errors.py
  registry/              schema.py (v3 + migrate) · writer.py · reader.py
  capture/               pipeline · classifier · grouper · variants · output · audit · proxy · stages
  archive/               Stage 0.5 (detect/extract/validate/repair/quarantine)
  tests/                 300+ tests — the merge gate
scripts/                 operations tooling (NOT the engine) — see §19
```

**Test gate:** `python3 -m pytest wecape/tests/ -q` (pytest-free subset: `python run_tests.py`).
**Registry:** `~/.wecape/registry/wecape.db` (schema v3). **Notes:** `~/.wecape/annotations.db`.

## Appendix D — Normative References & Change Log

**Normative by reference:** `CLAUDE.md` · `SECURITY_RISK_ANALYSIS.md` ·
`CREDENTIAL_INVENTORY.md` · `SPEC_Additive_Ingest_Found_Footage.md` ·
`SPEC_Production_Health_Report.md` · `UI_Dashboard_Design_Guidelines_v2.md` ·
`WE_FLOW_RFQ_v6.md` (predecessor CAPTURE RFQ) · `EXECUTIVE_SUMMARY_v4.7.md`.

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-07-03 | Initial platform + product technical specification. Establishes the Part I (platform) / Part II (CAPTURE) split; supersedes the RFQ-format v6 as the governance reference. |

---
*W.E. C.A.P.E. Technical Specification v1.0 — Workman Experience Technologies LLC — Confidential.*
*Platform principles (Part I) are binding on every product; CAPTURE requirements (Part II)
apply to the first product only. No LOCKED item may change without written approval and a §21 entry.*
