# CLAUDE.md — W.E. C.A.P.E. / W.E. C.A.P.E. CAPTURE Build Context
## Version 2.0 | Updated June 8, 2026

## What This Project Is

**W.E. C.A.P.E.** is The Workman Experience's Production Intelligence Platform.
**W.E. C.A.P.E. CAPTURE** is the first product — automated multi-camera ingest, scaffold, and proxy generation.

Platform brand leads. W.E. C.A.P.E. is announced before W.E. C.A.P.E. CAPTURE ships.
W.E. C.A.P.E. CAPTURE is described as "the first product from W.E. C.A.P.E.."

---

## Repository State

```
Repo:    github.com:theworkmanexperience-sketch/Curser.git
Local:   ~/Curser/we-flow/
Package: we_capture/ (target: wecape/ — see Phase 2)
Commit:  04d3910 — Measures 2+4 implemented
Tests:   171/171 passing
Phase 1: COMPLETE
Phase 2: IN PROGRESS (registry live, Measures 1-4, hwaccel, rebrand complete)
```

### Production Baseline (O-SIX RYDERZ MC — validated)
```
Files: 103 | Groups: 2 | Variants: 23
Proxies: 77 transcoded / 2 skipped / 0 failed
Errors: 0 | Runtime: 8.9 hours (USB HDD, 1 worker)
Target:  <90 minutes (NVMe, 4 workers) — Phase 2 gate
```

---

## Locked Architecture Decisions

These are non-negotiable. Do not modify without explicit instruction.

| Decision | Commitment |
|----------|------------|
| Platform brand leads | W.E. C.A.P.E. announced before W.E. C.A.P.E. CAPTURE ships |
| Local-first core | Creator machine is always source of truth |
| Cloud is optional | No data leaves machine by default — ever |
| In-house core | W.E. C.A.P.E. CAPTURE, W.E. EDIT, W.E. ARCHIVE built internally |
| Open API from J3 | Internal seams now, public API at J3 |
| Registry from day one | Every stage writes to local SQLite registry |
| AI is additive | v1 ships zero AI features |
| Compliance first-class | Auditability built into every stage |
| Post-quantum crypto | CRYSTALS-Kyber for CloudSyncAdapter at J3 |

### Architectural Principles (P1-P7)
- **P1 Determinism** — identical input + config = identical output, always
- **P2 Privacy by Design** — local engine cannot make network calls
- **P3 Auditability** — every run produces a complete manifest
- **P4 Extensibility Without Coupling** — new stages never modify existing stages
- **P5 Registry Continuity** — registry is append-only, never overwritten
- **P6 Staged Intelligence** — AI features never foundational to core pipeline
- **P7 Creator Data Sovereignty** — creator owns all production data

---

## Current Package Structure

```
we_capture/
├── archive_engine/     ← Archive Intelligence (Stage 0.5)
│   ├── detector.py
│   ├── extractor.py
│   ├── manifest.py
│   ├── quarantine.py
│   ├── repair.py
│   ├── stage.py
│   └── validator.py
├── engine/             ← Core pipeline
│   ├── audit.py
│   ├── classifier.py
│   ├── grouper.py
│   ├── output.py
│   ├── pipeline.py
│   ├── profile.py
│   ├── proxy.py        ← JSON registry today, SQLite at Phase 2
│   ├── timestamp.py    ← _extract_dji_telemetry stub (unintegrated, no tests yet)
│   └── variants.py
├── profiles/
│   ├── default.yaml
│   ├── ryderz.yaml
│   └── google_drive.yaml
├── tests/              ← 95 tests, must stay green
└── main.py
```

---

## Target Package Structure (Phase 2)

```
wecape/
├── core/               ← Shared across all W.E. C.A.P.E. products
│   ├── stage.py        ← PipelineStage ABC
│   ├── sync.py         ← SyncAdapter ABC + LocalOnlySyncAdapter
│   ├── manifest.py     ← RunManifest (JSON + HTML + XML stubs)
│   ├── config.py       ← Config profile system
│   └── errors.py       ← Error taxonomy
├── registry/           ← SQLite data layer
│   ├── schema.py       ← Table definitions
│   ├── writer.py       ← Stage result persistence
│   └── reader.py       ← Query interface
├── flow/               ← W.E. C.A.P.E. CAPTURE product
│   ├── ingest.py
│   ├── archive.py      ← Archive Intelligence
│   ├── scaffold.py
│   ├── proxy.py        ← proxy_workers:4 lands here
│   ├── audit.py
│   └── main.py
├── intelligence/       ← AI stages (J1-J5, not yet built)
│   ├── camera.py       ← J1
│   ├── quality.py      ← J2
│   ├── alignment.py    ← J3
│   └── editorial.py    ← J4
├── sync/               ← Sync adapters
│   ├── local.py        ← LocalOnlySyncAdapter (v1 default, no-op)
│   ├── lan.py          ← v2
│   └── cloud.py        ← v3, optional
└── api/                ← Extension layer
    ├── extensions.py
    └── contracts.py
```

---

## Registry Schema — SQLite (Phase 2)

Location: `~/.wecape/registry/wecape.db`

### Four Required Tables

```sql
CREATE TABLE IF NOT EXISTS runs (
    id                  TEXT PRIMARY KEY,
    timestamp           TEXT NOT NULL,
    we_forge_version    TEXT NOT NULL,
    profile_id          TEXT,
    source_path         TEXT NOT NULL,
    output_path         TEXT NOT NULL,
    file_count          INTEGER DEFAULT 0,
    total_duration_sec  REAL DEFAULT 0.0,
    runtime_sec         REAL DEFAULT 0.0,
    stage_results       TEXT,
    errors              TEXT,
    diagnostics         TEXT,
    sync_status         TEXT DEFAULT 'local',
    metadata            TEXT
);

CREATE TABLE IF NOT EXISTS content (
    id                      TEXT PRIMARY KEY,
    run_id                  TEXT REFERENCES runs(id),
    filename                TEXT NOT NULL,
    original_path           TEXT NOT NULL,
    scaffold_path           TEXT,
    proxy_path              TEXT,
    camera_id               TEXT,
    camera_family           TEXT,
    corrected_timestamp     TEXT,
    shoot_date              TEXT,
    duration_sec            REAL,
    codec                   TEXT,
    resolution              TEXT,
    file_size_bytes         INTEGER,
    quality_score           REAL,
    content_tags            TEXT,
    alignment_offset_ms     REAL,
    highlight_score         REAL,
    model_version           TEXT,
    embedding_model_version TEXT,
    embedding_vector_dims   INTEGER,
    content_type            TEXT DEFAULT 'original',
    first_seen              TEXT NOT NULL,
    last_seen               TEXT NOT NULL,
    metadata                TEXT
);

CREATE TABLE IF NOT EXISTS preferences (
    key         TEXT PRIMARY KEY,
    value       TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL,
    description TEXT
);
```

---

## PipelineStage Interface (Phase 2)

Every stage — current and future — implements this. This becomes the public extension API at J3.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StageContext:
    run_id: str
    source_path: str
    output_path: str
    profile: dict
    registry_writer: object   # injected — never imported directly
    sync_adapter: object      # injected — LocalOnly by default
    timestamp: datetime
    metadata: dict


@dataclass
class StageResult:
    stage_id: str
    stage_version: str
    success: bool
    files_processed: int
    files_skipped: int
    files_failed: int
    duration_sec: float
    errors: list
    diagnostics: list
    metadata: dict


class PipelineStage(ABC):
    stage_id: str
    stage_version: str
    stage_description: str

    @abstractmethod
    def validate_input(self, context: StageContext): pass

    @abstractmethod
    def execute(self, context: StageContext) -> StageResult: pass

    @abstractmethod
    def on_error(self, error: Exception, context: StageContext) -> dict: pass

    def write_registry(self, result: StageResult, context: StageContext) -> None:
        # Mandatory — not overrideable
        context.registry_writer.write_stage_result(
            run_id=context.run_id,
            stage_id=self.stage_id,
            result=result
        )
```

**Stage Rules:**
- Stages NEVER import from other stages
- Stages write to registry via `context.registry_writer` only
- Stages NEVER make network calls
- Stages must be idempotent

---

## SyncAdapter Interface (Phase 2)

```python
from abc import ABC, abstractmethod


class SyncAdapter(ABC):
    @abstractmethod
    def is_available(self) -> bool: pass

    @abstractmethod
    def push_run(self, manifest) -> bool: pass

    @abstractmethod
    def push_registry_delta(self, delta) -> bool: pass

    @abstractmethod
    def pull_shared_library(self, team_id): pass

    @abstractmethod
    def get_sync_status(self) -> dict: pass


class LocalOnlySyncAdapter(SyncAdapter):
    """Default v1. All methods are safe no-ops. Zero network calls."""
    def is_available(self) -> bool: return True
    def push_run(self, manifest) -> bool: return True
    def push_registry_delta(self, delta) -> bool: return True
    def pull_shared_library(self, team_id): return None
    def get_sync_status(self) -> dict:
        return {"mode": "local", "status": "active", "last_sync": None}
```

---

## Phase 2 Build Sequence

### Track A — Performance (Commercial Launch Gate)
```
1. proxy_workers: 4        ← parallel ffmpeg transcoding (2 weeks)
2. pre-flight ffprobe      ← duration estimate before run starts (1 week)
3. NVMe benchmark          ← validate after hardware arrives
Gate: 100-file shoot completes in under 90 minutes
```

### Track B — Platform Architecture (do in this order)
```
1. wecape/ namespace reorganization  ← FIRST — before proxy_workers:4
2. Registry schema v1 + SQLite setup
3. PipelineStage ABC
4. SyncAdapter (LocalOnly default)
5. RunManifest tri-format (JSON + HTML + XML stubs)
```

### Track C — Platform
```
- weforge.com domain registration
- W.E. C.A.P.E. landing page (before W.E. C.A.P.E. CAPTURE ships)
- Apple Developer account ($99/yr)
- Executive Summary v4.7 → v4.8
- Publish architecture doc to prjctlazrus.com
```

---

## What NOT To Build Yet

- W.E. EDIT (J4) — not until W.E. C.A.P.E. CAPTURE v1 ships and earns it
- W.E. ARCHIVE (J5) — not until registry has 18+ months of data
- W.E. API public (J3) — internal seams only for now
- AI features of any kind — v1 ships zero AI
- Cloud sync — LocalOnlySyncAdapter is v1 default
- UI layer — after performance gate passes

---

## Juncture Map (AI Intelligence Stack)

| Juncture | Feature | Hardware Delta | Pricing Impact |
|----------|---------|---------------|---------------|
| J1 | Camera AI identification | Zero | Eliminates setup friction |
| J2 | Shot quality scoring + content tagging | ANE (free on M1+) | $99→$149/yr |
| J3 | Audio temporal alignment (PluralEyes killer) | 32GB RAM recommended | $149→$199/yr |
| J4 | Highlight detection + rough cut XML | M1 Pro recommended | $199→$299/yr |
| J5 | Cross-project content registry + API | NVMe + storage growth | $499-999/seat/yr |

---

## Hardware Context

```
Machine: Mac Studio M1 Max — 32 GB RAM
Storage:
  - Internal SSD: 414 GB (67% full after cleanup — June 2026)
  - 10TB My Book Duo (RAID 0): active shoots + WE_FLOW_OUTPUT
  - Got My BackUP (5TB WD easystore): Time Machine destination
  - G-DRIVE SSD (4TB): backup archive
  - FreeAgent GoFlex (1TB): corrupted filesystem, DiskWarrior needed
Pending purchase: Samsung 990 PRO 4TB + ZikeDrive Z666 TB4 (~$410)
CRITICAL: Connect NVMe directly to Mac Studio TB4 port — NOT through StarTech dock
```

---

## External Services

```
Google Drive: the.workman.experience@gmail.com (20TB plan)
  - Archive complete: 3.3TB across 6 stage folders
  - rclone configured with custom API client (project: weforge-archive)
  - Stream mode enabled (not Mirror)
GitHub: github.com:theworkmanexperience-sketch/Curser.git
Architecture doc: prjctlazrus.com (NDA in place)
Apple Developer account: NOT YET PURCHASED ($99/yr needed for .dmg signing)
```

---

## Future Products (Do Not Build Yet)

### W.E. EDIT (J4)
Editorial intelligence layer — rough cut XML, highlight detection, shot quality rankings.
Technical dependency: same registry and PipelineStage interface as W.E. C.A.P.E. CAPTURE.

### W.E. ARCHIVE (J5)
Storage intelligence layer — cross-project deduplication, visual similarity search, cold storage.
Technical dependency: queries the production registry built by W.E. C.A.P.E. CAPTURE from day one.

### W.E. API (J3)
Public extension layer — custom camera parsers, NLE integrations, webhook support.
Technical dependency: internal seams designed at J1, published at J3.

---

## Test Requirements

- All 95 tests must pass before any commit merges
- New features require tests before merge
- `python3 -m pytest we_capture/tests/ -q` is the current gate
- After wecape/ namespace reorganization: update all imports, verify 95/95 still pass
- Test file location after reorganization: `wecape/tests/`

---

## Competitive Context

W.E. C.A.P.E. CAPTURE replaces: Hedge ($99/yr) + manual Finder org + PluralEyes ($199) + Kyno ($149/yr)
W.E. C.A.P.E. at J5: production intelligence platform with 2+ years creator data + AI across pre-edit workflow.
Adobe paid $1.275B for Frame.io (cloud collaboration, no AI, no ingest intelligence).
W.E. C.A.P.E. at J5 is a different conversation entirely.

---

## MG-02 Results (O-SIX RYDERZ MC Community Service — June 8, 2026)

```
Run ID:   WEF_20260608_120955_289A74
Files:    103 | Groups: 2 | Variants: 23 | Errors: 0 | Diagnostics: 4
Proxies:  79 transcoded | 0 skipped | 0 failed
Runtime:  32,697s = 9.08 hours
Rate:     6.90 min/file (validates MG-01: 6.96 min/file)
Registry: 103 records in ~/.wecape/registry/wecape.db
Cameras:  Insta360(48) DJI(29) unclassified(23)
```

Validated per-file rate: ~7 min/file USB/1w | ~0.75 min/file NVMe/4w (projected)

---

## Backlog — Known Issues (Priority Order)

COMPLETED:
  Measure 1  c35750a  fail fast if ffmpeg/ffprobe missing
  Measure 2  c17795a  proxy count summary
  Measure 3  27c8043  warn when 0 proxies
  Measure 4  04d3910  smoke test first file

PENDING:
1. Measure 5 - progress heartbeat for runs >1 hour
2. wecape/capture migration (Option A) — COMPLETE 083889c
3. _extract_dji_telemetry integration
4. Windows platform support
5. Executive Summary update

---

## Recent Commits

```
27c8043  feat(preflight): Measure 3 — warn when 0 proxies from eligible
62209f2  fix(proxy): pre-flight estimate per-file rate, MG-01 calibrated
c35750a  feat(preflight): Measure 1 — fail fast if ffmpeg/ffprobe missing
9033721  feat(registry): wire RegistryWriter into pipeline
65866a9  docs: add WEFORGE Architecture v1.0 and Phase 2 build log
```

---

## Hardware Pending

Samsung 990 PRO 4TB (~$260) + ZikeDrive Z666 TB4 enclosure (~$150) = ~$410
Connect NVMe DIRECTLY to Mac Studio TB4 port — NOT StarTech dock
After install: config.yaml workers: 1 -> 4
Expected: 9 hours -> ~60 minutes per 79-file shoot


---

## Brand Architecture

### Platform
W.E. C.A.P.E. — Content Asset Production Ecosystem
Capture - Archive - Pulse - Evaluate

### Entity Structure
Workman Experience Technologies LLC  (W.E. C.A.P.E. IP owner)
  W.E. C.A.P.E.
    CAPTURE   current build — we_capture/
    ARCHIVE   J5
    PULSE     J4
    EVALUATE  J3-J4
  Future technology IP

The Workman Experience, LLC  (Creator brand)
  YouTube / Content
  Media & Press credentials
  Merchandise
  Sponsorships
  Independent Content IP

### Module Taglines
CAPTURE  — Capture every moment. Miss nothing.
ARCHIVE  — Every frame. Forever.
PULSE    — The heartbeat of production.
EVALUATE — Turn content into intelligence.

### Registry
Path:   ~/.wecape/registry/wecape.db
Status: LIVE — collecting since June 8, 2026
Data:   MG-02 complete (103 files, 9.08h, 79 proxies)

### Codebase
Repo:      ~/Curser/we-cape/
Namespace: wecape/ (platform) + we_capture/ (CAPTURE module)
Tests:     171/171 passing
Env vars:  WECAPE_TEST_MODE=1 | WECAPE_NONINTERACTIVE=1


---

## Benchmark Results — All Validated Runs

| Run | Source | Workers | Encoder | Runtime | Rate | Gate |
|-----|--------|---------|---------|---------|------|------|
| MG-01 | USB HDD | 1 | VTB sw decode | 8.9h | 6.96 min/proxy | baseline |
| MG-02 | USB HDD | 1 | VTB sw decode | 9.08h | 6.90 min/proxy | fail |
| MG-03a | USB HDD | 4 | VTB sw decode | 3.56h | 2.71 min/proxy | fail |
| MG-03b | NVMe | 4 | VTB sw decode | 3.07h | 2.33 min/proxy | fail |
| MG-04 | NVMe | 4 | VTB hwaccel | 34 min | 0.43 min/proxy | PASS |

Gate: < 90 minutes. Confirmed MG-04 June 22, 2026.

| Production | USB HDD | 4 | VTB hwaccel | 49.9 min | 0.63 min/proxy | PASS |

Production run: WEF_20260622_221150_204D47
Output: /Volumes/WE_CAPE_OUTPUT/O-SIX_RYDERZ_MC/Community_Service_2024/
Source: /Volumes/10TB/O-SIX RYDERZ MC Community Service (USB)
Note: USB source adds ~16 min vs NVMe source — gate met on both

Critical discovery: commit 724bdae declared gate active before any validation.
NVMe delivered 2.96x improvement. Free -hwaccel flag delivered 16x.
Storage was never the bottleneck. Software decoding was.

---

## Pre-Flight Estimates — Validated Rates

| Config | Rate | Source |
|--------|------|--------|
| USB/1w/sw | 7.0 min/proxy | MG-02 validated |
| USB/4w/sw | 2.7 min/proxy | MG-03a validated |
| NVMe/4w/sw | 2.3 min/proxy | MG-03b validated |
| NVMe/4w/hwaccel | 0.43 min/proxy | MG-04 validated |

---

## Measures Implemented

| Measure | Commit | Description |
|---------|--------|-------------|
| 1 | c35750a | Fail fast if ffmpeg/ffprobe missing when proxy enabled |
| 2 | c17795a | Proxy count summary + confirm before transcoding starts |
| 3 | 27c8043 | Warn when 0 proxies generated from eligible files |
| 4 | 04d3910 | Smoke test first file — abort config failures, warn file failures |

Measure 5  4fa19c6  parallel + serial heartbeat every 5 min — validated MG-05

---

## Storage Map — June 22, 2026

| Volume | Size | Used | Free | Notes |
|--------|------|------|------|-------|
| Macintosh HD Data | 414 GB | 314 GB | 77 GB | Correct volume to monitor — fixed d402855 |
| WE_CAPE_OUTPUT NVMe TB4 | 4.0 TB | 256 GB | 3.5 TB | Primary output + source copies |
| 10TB My Book Duo | 10 TB | 9.2 TB | 0.8 TB | Active shoots |
| timemachine | 4.0 TB | 3.9 TB | 0.1 TB | Time Machine — same physical drive as 10TB |
| Got My BackUP | 5.0 TB | 184 GB | 4.8 TB | Underutilized — backs up almost nothing |
| Holder Mac HFS+ | 6.0 TB | 4.6 TB | 1.4 TB | Production content + legal docs — zero backup |
| G-DRIVE SSD | 4.0 TB | unknown | unknown | MG-02 proxies — disconnected June 22 |
| WEDDING NTFS | 512 GB | unknown | unknown | Unverified backup status |
| DJIAction6 NTFS | 256 GB | 157 GB | 99 GB | Unprocessed shoot — needs CAPTURE |
| FreeAgent GoFlex | 1.0 TB | unknown | unknown | Corrupted — DiskWarrior needed |

Critical risks:
  Holder Mac 4.6 TB has zero backup — single HFS+ volume
  disk12 holds timemachine + 10TB + Holder Mac — one failure loses all three
  Got My BackUP has 4.8 TB free but is backing up almost nothing
  G-DRIVE SSD disconnected — MG-02 proxies inaccessible

Pre-flight fix June 22: sys_free_gb was reading OS volume (12 GB)
instead of Data volume (314 GB) since June 8. Fixed in d402855.
All prior pre-flight reports contain incorrect system drive free space.

---

## Known Registry Anomaly

WEF_20260622_020843_66257B: 0 files, 0.0h
  Cause: CAPTURE ran against empty source (rsync still in progress)
  Rule:  All aggregate queries must include WHERE file_count > 0

---

## Rebrand — June 22, 2026 (commit f8c8878)

W.E. FORGE     -> W.E. C.A.P.E.
W.E. FLOW      -> W.E. C.A.P.E. CAPTURE
weforge/       -> wecape/
we_flow/       -> we_capture/
~/.weforge/    -> ~/.wecape/
weforge.db     -> wecape.db
Entity:        Workman Experience Technologies LLC (pending formation)
Domain:        workmanexperience.com/cape (pending build)


---

## RFQ Compliance Notes

### §7 Grouping Window Deviation
RFQ LOCKED spec:    window_seconds: 5
Production config:  window_seconds: 15
Justification:      DJI/Insta360 clock drift is 6-12s in field conditions.
                    At ±5s: 1/3 groups form, 67% of camera files ungrouped.
                    At ±15s: 3/3 groups form, 0% ungrouped.
                    Empirically validated June 22 2026 on Community Service dataset.
                    Deviation is a field calibration, not a spec violation.
Status:             Documented deviation — defensible, validated, intentional.

### Test 6 Quantitative Thresholds
Status:             Cannot be written — RFQ Appendix B not available.
                    Appendix B contains the specific thresholds for Test 6.
                    Request Appendix B from contract holder before filing.
