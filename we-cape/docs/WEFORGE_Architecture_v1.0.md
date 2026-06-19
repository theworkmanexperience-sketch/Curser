# W.E. C.A.P.E. — Technical Architecture Document
## Version 1.0 | Confidential | NDA Required

**Classification:** Confidential — Shared under executed NDA with prjctlazrus.com  
**Prepared by:** Workman Experience Media  
**Document status:** Architecture Lock — Foundational decisions recorded as binding principles

---

> *"W.E. C.A.P.E. at J5 is a production intelligence platform with 2+ years of creator data  
> and AI layers across the entire pre-edit workflow.  
> That's not a $1.275B conversation — that's a different number."*

---

## Table of Contents

- [Part I: Platform Foundation](#part-i-platform-foundation)
- [Part II: Product Architecture](#part-ii-product-architecture)
- [Part III: Core Technical Architecture](#part-iii-core-technical-architecture)
- [Part IV: Intelligence Stack — Junctures 1–5](#part-iv-intelligence-stack--junctures-15)
- [Part V: Build Roadmap](#part-v-build-roadmap)
- [Part VI: Competitive Landscape](#part-vi-competitive-landscape)
- [Part VII: Acquisition Narrative](#part-vii-acquisition-narrative)

---

# PART I: PLATFORM FOUNDATION

## 1. Executive Overview

W.E. C.A.P.E. is a Production Intelligence Platform for independent video creators and small production companies. It combines automated media ingest, multi-camera temporal alignment, AI-assisted content analysis, and a persistent production registry into a single local-first platform.

W.E. C.A.P.E. CAPTURE is the first product from W.E. C.A.P.E. — an automated ingest, scaffold, and proxy generation tool that replaces four separate workflow tools with a single command. W.E. C.A.P.E. CAPTURE is the proof of concept that earns the platform narrative.

The platform is designed along a five-juncture AI intelligence roadmap. At Juncture 1, W.E. C.A.P.E. is a faster, smarter ingest tool. At Juncture 5, it is the only platform that owns production intelligence for the independent creator — a persistent AI trained on a creator's entire production history, operating locally, with no footage ever leaving the creator's machine without explicit consent.

**The market gap W.E. C.A.P.E. fills:**  
Adobe owns the cloud. Apple owns the edit. Blackmagic owns color. Nobody owns pre-edit ingest intelligence for independent creators at scale. W.E. C.A.P.E. owns that gap.

---

## 2. Platform Vision

### 2.1 Mission Statement

> Give independent video creators the production intelligence infrastructure previously available only to high-budget productions — locally, privately, and affordably.

### 2.2 Platform Promise

Every creator using W.E. C.A.P.E. operates under three guarantees:

1. **Your footage never leaves your machine** without your explicit action
2. **Your production history is yours** — portable, inspectable, and deletable at any time
3. **The platform gets smarter with every run** — not by sending data to a server, but by learning your production style locally

### 2.3 Locked Platform Decisions

The following decisions are architectural commitments. They are not subject to revision without a full platform review:

| Decision | Commitment | Rationale |
|----------|------------|-----------|
| **Brand leads** | W.E. C.A.P.E. is announced before W.E. C.A.P.E. CAPTURE ships | Platform narrative must precede product launch |
| **Local-first core** | Creator machine is always the source of truth | Privacy, speed, cost, and trust |
| **Cloud is optional** | No data leaves the machine by default | Legally, ethically, and competitively non-negotiable |
| **In-house core** | W.E. C.A.P.E. CAPTURE, W.E. EDIT, W.E. ARCHIVE built internally | Vision and quality bar cannot be licensed |
| **Open API from J2/J3** | Extension points designed at J1; published at J3 | Ecosystem requires early seam design |
| **Registry from day one** | Every run writes to local SQLite registry | The registry is the long-term product asset |
| **AI is additive** | v1 ships zero AI features | Core workflow proves market fit before AI |
| **Compliance first-class** | Auditability built into every stage | Not bolted on — architecturally required |

---

## 3. Architectural Principles

These principles govern every engineering decision across all junctures:

### P1 — Determinism
Given identical input and configuration, W.E. C.A.P.E. produces identical output. Every stage is reproducible, testable, and verifiable. No randomness, no network calls, no environmental dependencies in the core pipeline.

### P2 — Privacy by Design
The local engine is architecturally incapable of making network calls. Cloud features are implemented as optional adapters that the local engine invokes through a defined interface — never directly. This guarantee is verifiable by code inspection.

### P3 — Auditability
Every pipeline run produces a complete manifest documenting every decision, every file processed, every error encountered, and every stage result. Manifests are machine-readable (JSON), human-readable (HTML), and NLE-compatible (FCPXML/DaVinci XML).

### P4 — Extensibility Without Coupling
Every pipeline stage implements a common interface. New stages — including all AI features at J1–J5 — are added without modifying existing stages. Third-party extensions use the same interface as internal stages.

### P5 — Registry Continuity
The local registry is append-only by default. Historical production data is never overwritten. Deletion is explicit and logged. The registry is the platform's most valuable long-term asset.

### P6 — Staged Intelligence
AI features are never foundational to the core pipeline. The pipeline functions completely without any AI stage. AI stages are enhancements that run after the core workflow succeeds.

### P7 — Creator Data Sovereignty
Creators own their production data. The registry schema is open and documented. Export is always available. The platform never monetizes creator data without explicit consent and compensation.

---

# PART II: PRODUCT ARCHITECTURE

## 4. W.E. C.A.P.E. Platform Structure

```
W.E. C.A.P.E. — The Production Intelligence Platform
│
├── PRODUCTS
│   ├── W.E. C.A.P.E. CAPTURE        ← Ingest, scaffold, proxy (shipping)
│   ├── W.E. EDIT        ← Editorial intelligence (J4 roadmap)
│   ├── W.E. ARCHIVE     ← Storage + retrieval intelligence (J5 roadmap)
│   └── W.E. API         ← Third-party extension layer (J3 roadmap)
│
├── INTELLIGENCE STACK
│   ├── Camera Intelligence      ← J1
│   ├── Content Intelligence     ← J2
│   ├── Temporal Intelligence    ← J3
│   ├── Editorial Intelligence   ← J4
│   └── Production Intelligence  ← J5
│
├── DATA LAYER
│   ├── Local Registry (SQLite)
│   ├── Run Manifests
│   ├── Content Fingerprints
│   └── Production History
│
└── EXTENSION LAYER
    ├── Internal Plugin Interface (J1)
    ├── Public Extension API (J3)
    └── NLE Integration Adapters (J4)
```

---

## 5. W.E. C.A.P.E. CAPTURE — Product Specification

### 5.1 Definition

W.E. C.A.P.E. CAPTURE is an automated multi-camera ingest, scaffold, and proxy generation tool. It ingests raw footage from any combination of cameras, corrects corrupted metadata, organizes footage into a structured scaffold, generates editorial proxies, and produces a complete audit manifest — in a single automated run.

### 5.2 Core Capabilities (v1 Shipping)

| Capability | Description | Status |
|------------|-------------|--------|
| Multi-camera ingest | Processes GoPro, DJI, Insta360, iPhone, DSLR simultaneously | ✅ Production |
| Archive Intelligence | Handles corrupted timestamps, duplicate filenames, bad metadata | ✅ Production |
| Scaffold generation | Date/camera/type organized output structure | ✅ Production |
| Proxy generation | ffmpeg-based, hardware-accelerated on Apple Silicon | ✅ Production |
| Config profile system | Per-client, per-shoot-type configuration | ✅ Production |
| Audit manifest | Complete run documentation | ✅ Production |
| Diagnostic reporting | Error classification and resolution guidance | ✅ Production |
| Registry writes | Every run written to local SQLite | J1 Architecture |
| Parallel proxy workers | 4-worker concurrent transcoding | Phase 2 |
| Pre-flight estimation | ffprobe duration scan before processing | Phase 2 |

### 5.3 Production Baseline

Validated against O-SIX RYDERZ MC client dataset:

```
Files processed:    103
Camera groups:      2
Variants detected:  23
Errors:             0
Diagnostics:        4
Proxies generated:  77 transcoded / 2 skipped / 0 failed
Runtime (v1):       8.9 hours (single worker, USB HDD source)
Runtime (v2 est.):  45-60 minutes (4 workers, NVMe source)
Test coverage:      95/95 passing
```

### 5.4 Camera Compatibility Matrix

| Camera Family | Status | Timestamp Handling |
|---------------|--------|--------------------|
| GoPro Hero 9-13 | ✅ Validated | FAT32 epoch correction |
| DJI Action 5/6 | ✅ Validated | UTC offset handling |
| Insta360 X3/X5 | ✅ Validated | INSV container |
| iPhone (iOS) | ✅ Validated | HEIF/MOV |
| Nikon DSLR | ✅ Validated | Standard EXIF |
| Sony A7/FX/ZV | Phase 2 | XAVC metadata |
| Canon Cinema/R | Phase 2 | MXF extraction |
| Panasonic S5/GH | Phase 2 | XMP sidecar |
| DJI Drones | Phase 2 | Drone vs action differentiation |
| Blackmagic BRAW | J4 roadmap | Requires Blackmagic SDK |
| RED R3D | J5 roadmap | Requires RED SDK |

---

## 6. Future Products

### 6.1 W.E. EDIT (J4 Roadmap)

Editorial intelligence layer. Receives scaffold and proxy output from W.E. C.A.P.E. CAPTURE and produces:
- Shot quality rankings
- Highlight reel recommendations
- Rough cut XML for Final Cut Pro and DaVinci Resolve
- Audio-based moment detection

**Technical dependency:** W.E. EDIT is a collection of pipeline stages operating on the same registry as W.E. C.A.P.E. CAPTURE. No separate data layer required.

### 6.2 W.E. ARCHIVE (J5 Roadmap)

Storage intelligence layer. Manages the full lifecycle of production assets:
- Cross-project content deduplication
- Retrieval by content similarity (not filename)
- Footage reuse recommendations across projects
- Cold storage integration (Google Drive, AWS Glacier, LTO)

**Technical dependency:** W.E. ARCHIVE queries the production registry built by W.E. C.A.P.E. CAPTURE from day one. Users who have run W.E. C.A.P.E. CAPTURE for 18 months have 18 months of archive intelligence on day one of W.E. ARCHIVE.

### 6.3 W.E. API (J3 Roadmap)

Public extension layer exposing the W.E. C.A.P.E. pipeline interface to third-party developers:
- Custom camera metadata parsers
- Specialized content classifiers
- NLE-specific export formats
- Custom scaffold templates
- Webhook integrations

**Technical dependency:** Internal seams designed at J1. Publication at J3 requires documentation and versioning, not refactoring.

---

# PART III: CORE TECHNICAL ARCHITECTURE

## 7. Package Structure and Module Boundaries

### 7.1 Top-Level Namespace

The package namespace is reorganized from `we_capture/` to `wecape/` before v1 ships. This is the last point at which renaming is cost-free.

```
wecape/
│
├── core/                    ← Shared across all W.E. C.A.P.E. products
│   ├── __init__.py
│   ├── stage.py             ← PipelineStage abstract interface
│   ├── context.py           ← StageContext data model
│   ├── sync.py              ← SyncAdapter interface
│   ├── manifest.py          ← RunManifest tri-format
│   ├── config.py            ← Config profile system
│   └── errors.py            ← Error taxonomy and resolution
│
├── registry/                ← The data layer — platform's core asset
│   ├── __init__.py
│   ├── schema.py            ← SQLite schema definitions
│   ├── writer.py            ← Stage result persistence
│   ├── reader.py            ← Query interface
│   └── migrations/          ← Schema version management
│
├── flow/                    ← W.E. C.A.P.E. CAPTURE product
│   ├── __init__.py
│   ├── ingest.py            ← File discovery and validation
│   ├── archive.py           ← Archive Intelligence (Stage 0.5)
│   ├── scaffold.py          ← Directory structure generation
│   ├── proxy.py             ← ffmpeg proxy generation (workers here)
│   ├── audit.py             ← Run manifest generation
│   └── main.py              ← CLI entry point
│
├── intelligence/            ← AI layers — additive, never foundational
│   ├── __init__.py
│   ├── camera.py            ← J1: Camera identification model
│   ├── quality.py           ← J2: Shot quality scoring
│   ├── alignment.py         ← J3: Audio temporal alignment
│   ├── editorial.py         ← J4: Highlight detection
│   └── registry_intel.py   ← J5: Cross-project intelligence
│
├── sync/                    ← Optional sync adapters
│   ├── __init__.py
│   ├── local.py             ← LocalOnlySyncAdapter (v1 default)
│   ├── lan.py               ← LAN sync (v2 — team, no cloud)
│   └── cloud.py             ← CloudSyncAdapter (v3 — optional)
│
└── api/                     ← Extension layer
    ├── __init__.py
    ├── extensions.py        ← Plugin registration system
    ├── contracts.py         ← Public API contracts (v1: internal only)
    └── nle/                 ← NLE integration adapters
        ├── fcpxml.py        ← Final Cut Pro XML
        └── drxml.py         ← DaVinci Resolve XML
```

### 7.2 Module Boundary Rules

These rules are enforced as architectural constraints:

1. `wecape/core/` has zero imports from `wecape/flow/`, `wecape/intelligence/`, or `wecape/sync/cloud/`
2. `wecape/flow/` imports from `wecape/core/` and `wecape/registry/` only
3. `wecape/intelligence/` imports from `wecape/core/` and `wecape/registry/` only
4. `wecape/sync/cloud/` is never imported by `wecape/flow/` directly — only through `wecape/core/sync.py` interface
5. `wecape/api/` imports from `wecape/core/` only — the API is a thin contract layer

---

## 8. Pipeline Stage Interface

Every processing stage in W.E. C.A.P.E. — current and future — implements this interface. This is the extension point that makes the plugin API possible.

```python
# wecape/core/stage.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class StageContext:
    """Passed between stages. Immutable per run."""
    run_id: str                    # UUID generated at run start
    source_path: str               # Absolute path to source footage
    output_path: str               # Absolute path to scaffold output
    profile: dict                  # Config profile for this run
    registry_writer: 'RegistryWriter'  # Injected — never imported directly
    sync_adapter: 'SyncAdapter'    # Injected — LocalOnly by default
    timestamp: datetime            # Run start time (UTC)
    metadata: dict                 # Extensible — stages add keys


@dataclass
class StageResult:
    """Returned by every stage."""
    stage_id: str
    stage_version: str
    success: bool
    files_processed: int
    files_skipped: int
    files_failed: int
    duration_sec: float
    errors: list[dict]
    diagnostics: list[dict]
    metadata: dict                 # Stage-specific output data


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


class PipelineStage(ABC):
    """
    Base interface for every W.E. C.A.P.E. pipeline stage.
    
    This interface is the internal seam that becomes the public
    extension API at J3. Third-party plugins and internal AI stages
    implement identical interfaces.
    
    RULE: Stages must not import from other stages.
    RULE: Stages must write to registry via context.registry_writer only.
    RULE: Stages must not make network calls.
    """
    
    stage_id: str           # Unique identifier: "ingest" | "scaffold" | etc.
    stage_version: str      # Semantic version: "1.0.0"
    stage_description: str  # Human-readable description for UI display
    
    @abstractmethod
    def validate_input(self, context: StageContext) -> ValidationResult:
        """
        Pre-flight check. Called before execute().
        Validates source data, required config, and preconditions.
        Must not modify any files or state.
        """
        pass
    
    @abstractmethod
    def execute(self, context: StageContext) -> StageResult:
        """
        Core processing logic.
        Must write results to context.registry_writer before returning.
        Must be idempotent — safe to re-run on same input.
        """
        pass
    
    @abstractmethod
    def on_error(self, error: Exception, context: StageContext) -> dict:
        """
        Error handler. Returns user-facing resolution guidance.
        Must never raise — always returns a resolution dict.
        """
        pass
    
    def write_registry(self, result: StageResult, context: StageContext) -> None:
        """
        Persist stage results to local registry.
        Called automatically by pipeline runner after execute().
        Not overrideable — registry writes are mandatory.
        """
        context.registry_writer.write_stage_result(
            run_id=context.run_id,
            stage_id=self.stage_id,
            result=result
        )
```

---

## 9. Registry Data Model

### 9.1 Design Principles

- **SQLite** — Python stdlib, zero dependency, portable, queryable
- **JSON columns** for extensible metadata — new AI features add fields without schema migration
- **Append-only** — records are never overwritten; corrections create new records
- **Sync-ready** — schema designed for eventual cloud sync without requiring it
- **Creator-controlled** — full export and deletion always available

### 9.2 Schema Definition

```sql
-- wecape/registry/schema.py

-- RUNS: One record per W.E. C.A.P.E. pipeline execution
CREATE TABLE IF NOT EXISTS runs (
    id                  TEXT PRIMARY KEY,    -- UUID v4
    timestamp           TEXT NOT NULL,       -- ISO 8601 UTC
    we_forge_version    TEXT NOT NULL,       -- Platform version
    we_capture_version     TEXT,                -- W.E. C.A.P.E. CAPTURE version if applicable
    profile_id          TEXT,                -- Config profile identifier
    source_path         TEXT NOT NULL,       -- Absolute source path
    output_path         TEXT NOT NULL,       -- Absolute output path
    file_count          INTEGER DEFAULT 0,
    total_duration_sec  REAL DEFAULT 0.0,    -- Sum of all source file durations
    runtime_sec         REAL DEFAULT 0.0,    -- Wall clock time for run
    stage_sequence      TEXT,                -- JSON: ordered list of stages run
    stage_results       TEXT,                -- JSON: per-stage StageResult objects
    errors              TEXT,                -- JSON: error log
    diagnostics         TEXT,                -- JSON: diagnostic flags
    sync_status         TEXT DEFAULT 'local',-- local | pending | synced
    sync_timestamp      TEXT,                -- When last synced (if ever)
    metadata            TEXT                 -- JSON: extensible run metadata
);

-- CONTENT: One record per processed file across all runs
CREATE TABLE IF NOT EXISTS content (
    id                  TEXT PRIMARY KEY,    -- Content hash (SHA256 → xxHash3 at J3)
    run_id              TEXT NOT NULL REFERENCES runs(id),
    filename            TEXT NOT NULL,
    original_path       TEXT NOT NULL,       -- Source path at ingest time
    scaffold_path       TEXT,                -- Output path after scaffold
    proxy_path          TEXT,                -- Proxy file path
    
    -- Camera metadata (J1: detected, not assumed)
    camera_id           TEXT,                -- Detected camera model
    camera_family       TEXT,                -- GoPro | DJI | Insta360 | iPhone | etc.
    camera_confidence   REAL,                -- J1: AI detection confidence 0.0-1.0
    
    -- Temporal metadata (corrected)
    raw_timestamp       TEXT,                -- Original file timestamp (may be corrupt)
    corrected_timestamp TEXT,                -- Archive Intelligence corrected timestamp
    correction_method   TEXT,                -- How timestamp was corrected
    shoot_date          TEXT,                -- YYYY-MM-DD (corrected)
    
    -- Technical metadata
    duration_sec        REAL,
    codec               TEXT,
    container           TEXT,
    resolution          TEXT,                -- "3840x2160"
    framerate           TEXT,                -- "29.97"
    audio_channels      INTEGER,
    file_size_bytes     INTEGER,
    
    -- AI intelligence fields (populated at respective junctures)
    quality_score       REAL,                -- J2: 0.0-1.0
    content_tags        TEXT,                -- J2: JSON array of tags
    is_highlight        INTEGER DEFAULT 0,   -- J2: Boolean flag
    alignment_offset_ms REAL,               -- J3: Temporal offset in milliseconds
    alignment_confidence REAL,              -- J3: Alignment confidence 0.0-1.0
    highlight_score     REAL,               -- J4: Editorial highlight score 0.0-1.0
    rough_cut_candidate INTEGER DEFAULT 0,  -- J4: Boolean flag
    
    -- Registry tracking
    first_seen          TEXT NOT NULL,       -- ISO 8601: first run this file appeared
    last_seen           TEXT NOT NULL,       -- ISO 8601: most recent run
    appearance_count    INTEGER DEFAULT 1,   -- How many runs have seen this file
    
    metadata            TEXT                 -- JSON: extensible content metadata
);

-- PREFERENCES: Creator preferences learned across runs
CREATE TABLE IF NOT EXISTS preferences (
    key                 TEXT PRIMARY KEY,
    value               TEXT NOT NULL,       -- JSON
    source              TEXT,                -- "user" | "inferred" | "ai"
    confidence          REAL DEFAULT 1.0,    -- For inferred preferences
    updated_at          TEXT NOT NULL        -- ISO 8601
);

-- PROJECTS: Logical groupings of runs (optional, user-defined)
CREATE TABLE IF NOT EXISTS projects (
    id                  TEXT PRIMARY KEY,    -- UUID v4
    name                TEXT NOT NULL,
    client              TEXT,
    shoot_type          TEXT,                -- "event" | "documentary" | "commercial"
    created_at          TEXT NOT NULL,
    completed_at        TEXT,
    metadata            TEXT                 -- JSON
);

-- RUN_PROJECTS: Many-to-many: runs belong to projects
CREATE TABLE IF NOT EXISTS run_projects (
    run_id              TEXT REFERENCES runs(id),
    project_id          TEXT REFERENCES projects(id),
    PRIMARY KEY (run_id, project_id)
);

-- SCHEMA VERSION: Migration tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version             INTEGER PRIMARY KEY,
    applied_at          TEXT NOT NULL,
    description         TEXT
);
```

### 9.3 Registry Growth Projections

| Usage Level | Shoots/Month | Files/Shoot | Registry Growth | 2-Year Size |
|-------------|-------------|-------------|-----------------|-------------|
| Light | 2 | 50 | ~5 MB/month | ~120 MB |
| Moderate | 6 | 100 | ~18 MB/month | ~430 MB |
| Heavy | 12 | 200 | ~72 MB/month | ~1.7 GB |
| Studio | 20 | 300 | ~180 MB/month | ~4.3 GB |

Registry remains query-performant on SQLite up to ~50 GB. NVMe storage recommended for heavy/studio use at J5.

---

## 10. Sync Adapter Interface

The local engine never imports from cloud modules directly. This is the architectural guarantee behind the privacy promise.

```python
# wecape/core/sync.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class SyncManifest:
    run_id: str
    delta_records: list[dict]   # Only changed records
    checksum: str               # Integrity verification


@dataclass  
class SharedLibrary:
    team_id: str
    content_records: list[dict]
    last_updated: str


class SyncAdapter(ABC):
    """
    Interface for all sync implementations.
    
    Local engine ONLY calls methods on this interface.
    Cloud implementation details are never visible to the pipeline.
    
    v1: LocalOnlySyncAdapter (default, does nothing)
    v2: LANSyncAdapter (team sync, no cloud)
    v3: CloudSyncAdapter (optional, explicit user consent)
    """
    
    @abstractmethod
    def is_available(self) -> bool:
        """Can this adapter currently sync? Network check for cloud adapters."""
        pass
    
    @abstractmethod
    def push_run(self, manifest: SyncManifest) -> bool:
        """Persist run data to sync target. Returns success."""
        pass
    
    @abstractmethod
    def push_registry_delta(self, delta: SyncManifest) -> bool:
        """Sync only changed registry records."""
        pass
    
    @abstractmethod
    def pull_shared_library(self, team_id: str) -> Optional[SharedLibrary]:
        """Pull team-shared content library. Returns None if unavailable."""
        pass
    
    @abstractmethod
    def get_sync_status(self) -> dict:
        """Return current sync status for UI display."""
        pass


class LocalOnlySyncAdapter(SyncAdapter):
    """
    Default v1 implementation.
    All methods are safe no-ops.
    Zero network calls. Zero external dependencies.
    """
    
    def is_available(self) -> bool:
        return True   # Always "available" — nothing to check
    
    def push_run(self, manifest: SyncManifest) -> bool:
        return True   # No-op, report success
    
    def push_registry_delta(self, delta: SyncManifest) -> bool:
        return True   # No-op, report success
    
    def pull_shared_library(self, team_id: str) -> Optional[SharedLibrary]:
        return None   # No shared libraries in local-only mode
    
    def get_sync_status(self) -> dict:
        return {"mode": "local", "status": "active", "last_sync": None}
```

---

## 11. Manifest Format Specification

Every run produces a `RunManifest` in three formats simultaneously. The same data object renders to JSON, HTML, and NLE XML without duplication.

```python
# wecape/core/manifest.py

from dataclasses import dataclass, field
from typing import Optional
import json
from datetime import datetime


@dataclass
class RunManifest:
    """
    Single source of truth for a completed pipeline run.
    Three output formats — zero data duplication.
    
    JSON   → Registry, sync, API, developer tools
    HTML   → UI dashboard, human-readable report
    FCPXML → Final Cut Pro timeline import (J4: rough cut)
    DRXML  → DaVinci Resolve media pool import (J4: rough cut)
    """
    
    run_id: str
    timestamp: str
    profile_id: Optional[str]
    source_path: str
    output_path: str
    we_forge_version: str
    
    # Aggregate statistics
    total_files: int
    processed_files: int
    skipped_files: int
    failed_files: int
    total_duration_sec: float
    runtime_sec: float
    
    # Stage results
    stage_results: list[dict]
    errors: list[dict]
    diagnostics: list[dict]
    
    # Content records
    content: list[dict]           # One entry per processed file
    
    # Intelligence results (populated at respective junctures)
    quality_summary: Optional[dict] = None    # J2
    alignment_summary: Optional[dict] = None  # J3
    highlight_summary: Optional[dict] = None  # J4
    
    def to_json(self) -> dict:
        """Machine-readable. Used by registry, sync, and API."""
        return {
            "schema_version": "1.0",
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "platform": "W.E. C.A.P.E.",
            "version": self.we_forge_version,
            "source": self.source_path,
            "output": self.output_path,
            "statistics": {
                "total_files": self.total_files,
                "processed": self.processed_files,
                "skipped": self.skipped_files,
                "failed": self.failed_files,
                "source_duration_sec": self.total_duration_sec,
                "runtime_sec": self.runtime_sec
            },
            "stages": self.stage_results,
            "errors": self.errors,
            "diagnostics": self.diagnostics,
            "content": self.content,
            "intelligence": {
                "quality": self.quality_summary,
                "alignment": self.alignment_summary,
                "highlights": self.highlight_summary
            }
        }
    
    def to_html(self) -> str:
        """Human-readable report. Rendered in UI dashboard."""
        # Template-based HTML generation
        # Stub in v1, fully implemented with UI layer
        raise NotImplementedError("HTML renderer implemented with UI (Phase 3)")
    
    def to_fcpxml(self) -> str:
        """
        Final Cut Pro XML.
        v1: Empty stub — interface exists, implementation at J4.
        J4: Imports scaffold as organized event with proxy references.
        """
        return '<?xml version="1.0" encoding="UTF-8"?><!-- W.E. C.A.P.E. FCPXML stub -->'
    
    def to_drxml(self) -> str:
        """
        DaVinci Resolve XML.
        v1: Empty stub — interface exists, implementation at J4.
        """
        return '<!-- W.E. C.A.P.E. DaVinci XML stub -->'
```

---

## 12. Extension Point Design

### 12.1 Plugin Registration System

```python
# wecape/api/extensions.py

from typing import Type, Dict
from wecape.core.stage import PipelineStage


class ExtensionRegistry:
    """
    Central registry for all pipeline stage extensions.
    
    v1: Used internally only.
    J3: Opened as public API with versioning and validation.
    
    Third-party plugins register stages here.
    W.E. C.A.P.E. products (W.E. EDIT, W.E. ARCHIVE) use the same registry.
    """
    
    _stages: Dict[str, Type[PipelineStage]] = {}
    _stage_order: Dict[str, int] = {}
    
    @classmethod
    def register(
        cls,
        stage_class: Type[PipelineStage],
        insert_after: str = "audit"
    ) -> None:
        """Register a pipeline stage extension."""
        stage_id = stage_class.stage_id
        cls._stages[stage_id] = stage_class
        # Insertion order determines execution sequence
        
    @classmethod
    def get_pipeline(cls, profile: dict) -> list[PipelineStage]:
        """Return ordered list of stages for a given profile."""
        pass
    
    @classmethod
    def validate_extension(cls, stage_class: Type[PipelineStage]) -> bool:
        """Validate extension implements interface correctly."""
        pass


# Built-in stage registration (v1)
# These are the seams that become the public API at J3

from wecape.flow.ingest import IngestStage
from wecape.flow.archive import ArchiveIntelligenceStage
from wecape.flow.scaffold import ScaffoldStage
from wecape.flow.proxy import ProxyStage
from wecape.flow.audit import AuditStage

ExtensionRegistry.register(IngestStage, insert_after=None)
ExtensionRegistry.register(ArchiveIntelligenceStage, insert_after="ingest")
ExtensionRegistry.register(ScaffoldStage, insert_after="archive")
ExtensionRegistry.register(ProxyStage, insert_after="scaffold")
ExtensionRegistry.register(AuditStage, insert_after="proxy")

# AI stages registered separately — not in default pipeline until activated
# ExtensionRegistry.register(CameraIntelligenceStage, insert_after="ingest")  # J1
# ExtensionRegistry.register(QualityScoringStage, insert_after="proxy")       # J2
# ExtensionRegistry.register(AudioAlignmentStage, insert_after="archive")     # J3
# ExtensionRegistry.register(HighlightDetectionStage, insert_after="audit")   # J4
```

---

# PART IV: INTELLIGENCE STACK — JUNCTURES 1–5

## 13. Juncture 1 — Camera Intelligence

**Business goal:** Eliminate manual camera profile configuration. Cameras are identified automatically.

**Technical implementation:**
- Classification model: ~20 MB, bundled in app, runs locally
- Input: File codec, container, resolution, framerate, audio channel count, filename pattern
- Output: Camera family + model identification with confidence score
- Inference time: <100ms per file on CPU, negligible overhead
- Fallback: Unidentified cameras fall back to manual profile selection

**Hardware delta:** Zero. CPU-only inference on startup metadata — no video decoding required.

**Registry impact:** `camera_id`, `camera_family`, `camera_confidence` fields populated in `content` table from v1 forward. All future AI features benefit from clean camera identification.

**User experience:** Camera profile setup is eliminated. Setup time drops from 15 minutes to zero.

**W.E. C.A.P.E. platform value:** Platform accumulates camera fingerprint library across creator community. Rare and new cameras become identifiable faster than any manual approach.

---

## 14. Juncture 2 — Content Intelligence

**Business goal:** Give editors quality context before they open the NLE. Eliminate hours of proxy skimming.

**Technical implementation:**
- Vision model: CLIP or MobileNet variant, ~100 MB bundled
- Input: Sampled frames from proxies (not originals — proxies already exist)
- Analysis: Exposure, focus, motion stability, subject presence, shot type classification
- Output: Quality score (0.0–1.0) + content tags per clip
- Inference: Apple Neural Engine on M1+ (free, already present), CPU fallback
- Processing overhead: +15-20% of proxy generation time

**Hardware delta:** Apple Neural Engine already present on all M1+ chips. No new hardware required. Windows users benefit from any NVIDIA GPU via CUDA.

**Registry impact:** `quality_score`, `content_tags`, `is_highlight` populated in `content` table.

**User experience:** Proxy bins arrive with quality indicators. Editors go directly to the best material.

**Pricing impact:** Justifies W.E. C.A.P.E. CAPTURE upgrade from $99 → $149/year.

**W.E. C.A.P.E. platform value:** Quality scoring model improves with each creator's feedback over time. The platform learns what "good footage" means per creator, per shoot type, per client.

---

## 15. Juncture 3 — Temporal Intelligence

**Business goal:** Eliminate PluralEyes ($199 standalone tool) as a required workflow step. Multi-camera shoots arrive aligned, not raw.

**Technical implementation:**
- Audio fingerprinting: librosa or chromaprint, bundled
- Input: Audio tracks from all cameras in same shoot date group
- Algorithm: Cross-correlation of audio waveforms to detect matching peaks
- Accuracy: ±1-2 frames at 29.97fps
- Fallback: GPS timestamp correlation, then manual offset if no audio match
- Processing time: 10-20 minutes per shoot (acceptable — eliminates 30-60 minutes manual)
- Hardware: CPU-only, 32 GB RAM recommended for 6+ camera shoots

**Hardware delta:** 32 GB RAM strongly recommended. Already recommended for professional video work independently of this feature.

**Registry impact:** `alignment_offset_ms`, `alignment_confidence` populated in `content` table. Alignment data is reusable — once a shoot is aligned, offset is stored permanently.

**User experience:** Multi-camera footage arrives in NLE with cameras pre-synced. Audio alignment is invisible — it just works.

**Pricing impact:** Justifies W.E. C.A.P.E. CAPTURE upgrade to $199/year. Eliminates $199 competitor purchase.

**W.E. C.A.P.E. platform value:** Public API opens at J3. Third-party developers can build custom alignment algorithms, specialized classifier plugins, and NLE-specific export formats. Ecosystem begins.

**Competitive impact:** PluralEyes (Red Giant/Maxon) charges $199 for this single feature as a standalone tool. W.E. C.A.P.E. includes it in the standard ingest run. No other sub-$500 tool offers this capability.

---

## 16. Juncture 4 — Editorial Intelligence

**Business goal:** Deliver a usable rough cut starting point. Reduce editor time on a 3-hour shoot from 6-8 hours to 2-3 hours.

**Technical implementation:**
- Motion analysis: Frame differential scoring for action detection
- Audio energy: RMS analysis for crowd/music/speech peak detection
- Face detection: Lightweight face detection model for coverage identification
- Shot classification: Wide/medium/close-up classification
- Rough cut assembly: XML timeline generation with highest-scoring segments
- Export formats: FCPXML (Final Cut Pro), DaVinci Resolve XML
- Processing time: 30-45 minutes per shoot
- Hardware: Apple Neural Engine heavily utilized. M1 Pro/Max recommended.

**Hardware delta:** First juncture where hardware meaningfully matters. M1 Pro minimum recommended. Windows users benefit significantly from RTX 3060 or better GPU. M1 base Mac processes this feature correctly but slowly.

**Registry impact:** `highlight_score`, `rough_cut_candidate` populated. Rough cut XML written as run artifact.

**User experience:** After a run, editors receive a rough cut XML they can import directly into their NLE as a starting point. The workflow shifts from "editor assembles a cut from nothing" to "editor refines a machine-generated starting point."

**W.E. C.A.P.E. platform value:** W.E. EDIT launches as a distinct product at this juncture — with W.E. C.A.P.E. CAPTURE as the ingest layer and W.E. EDIT as the editorial intelligence layer. Platform narrative fully earned.

**Pricing impact:** Justifies $249-299/year positioning. The tool now touches the editorial phase — not just ingest.

**Acquisition signal:** This is the feature set that attracts acquisition conversations. Adobe, Apple, and Blackmagic are all building editorial AI. W.E. C.A.P.E. has it running locally, privately, at a prosumer price point.

---

## 17. Juncture 5 — Production Intelligence

**Business goal:** Become the single source of production truth for a creator's entire body of work. Enable cross-project intelligence that no competitor can replicate.

**Technical implementation:**
- Cross-project deduplication: Content fingerprint matching across all runs
- Footage reuse recommendations: "You shot similar content on [date] for [client]"
- Production analytics: Camera usage, shoot frequency, duration trends, error patterns
- Content retrieval: Find footage by visual similarity, not filename
- API layer: Full public REST API for third-party integrations
- Team sync: Optional LAN sync for shared team libraries (no cloud required)
- Cloud sync: Optional W.E. C.A.P.E. cloud sync for cross-device continuity

**Hardware delta:** Registry queries on SQLite scale efficiently. NVMe strongly recommended for heavy users with 50+ GB registries. No GPU required for registry operations.

**Registry impact:** The registry IS the product at J5. Cross-project queries span the entire `content` table. The production intelligence layer reads patterns across thousands of runs.

**User experience:** The platform knows the creator's entire production history. It surfaces insights invisible without persistent cross-run data. Reuse recommendations, redundancy alerts, production pattern analysis, and content retrieval by visual similarity all emerge from the registry built silently since v1.

**W.E. C.A.P.E. platform value:** At J5, W.E. C.A.P.E. is no longer a tool. It is a production intelligence platform trained on 2+ years of a creator's work. A new user starting at J5 starts from zero. An existing user starting at v1 has 2 years of production intelligence on day one of J5.

**This is the data moat.** No competitor can replicate a creator's production history. The platform gets more valuable the longer a creator uses it.

**Pricing:** Team/studio pricing at $499-999/seat/year. Enterprise API access as separate tier.

---

# PART V: BUILD ROADMAP

## 18. Phase Definitions and Milestones

### Phase 1 — Core Pipeline (Complete)

```
Status: ✅ Complete
Commit: f2e2cbf (audit.py proxies flush fix)
Tests:  95/95 passing

Delivered:
- Archive Intelligence (Stage 0.5)
- Config Profile System (Phase 1-C)
- Error/Diagnostics (Phase 1-D)
- Proxy Generation (Phase 1-E)
- audit.py proxies flush fix
```

---

### Phase 2 — Performance (Commercial Prerequisite)

```
Status: In progress
Prerequisite for: Any commercial release
Gate: W.E. C.A.P.E. CAPTURE processes 100-file shoot in under 90 minutes

Build items:
- proxy_workers: 4 (parallel transcoding)      Est. 2 weeks
- Pre-flight ffprobe duration estimate          Est. 1 week
- Package namespace reorganization (wecape/)   Est. 1-2 days
- Registry schema v1 (SQLite setup)             Est. 1 week
- PipelineStage interface formalization         Est. 3-4 days
- SyncAdapter interface (LocalOnly)             Est. 2-3 days
- RunManifest tri-format (JSON + HTML stubs)    Est. 3-4 days

Performance target after Phase 2:
- Scaffolding:     27 min → <5 min (NVMe)
- Proxy (100 files): 8.9 hrs → 45-60 min (4 workers + NVMe)
- Total run:       9.5 hrs → <1.5 hrs

Hardware dependency:
- Samsung 990 PRO 4TB + ZikeDrive Z666 enclosure ($410)
- Connected via direct Thunderbolt 4 port (not hub)
```

---

### Phase 3 — Platform Launch

```
Status: Planned (after Phase 2 performance gates pass)
Deliverable: W.E. C.A.P.E. brand + W.E. C.A.P.E. CAPTURE v1 public release

Build items:
- W.E. C.A.P.E. brand identity + weforge.com          Est. 1-2 weeks
- macOS packaging (.dmg, code signed)              Est. 1-2 weeks
- UI Layer (FastAPI + HTML dashboard)              Est. 6-10 weeks
- Windows platform support                         Est. 2-4 weeks
- Error handling (user-facing messages)            Est. 1-2 weeks
- Auto-update system                               Est. 3-5 days
- Licensing (Paddle/LemonSqueezy integration)      Est. 1 week
- Camera compatibility expansion (Sony, Canon)     Est. 2-3 weeks
- J1 Camera Intelligence AI stage                  Est. 2-3 weeks
- Documentation                                    Ongoing

Pricing: $99-149/year
Target: Independent creators, primary avatar
Revenue target: $75,000-149,000 at 500-1,000 users
```

---

### Phase 4 — Intelligence Layer

```
Status: Planned (6-12 months post-launch)
Prerequisite: Proven product-market fit, positive unit economics

Build items:
- J2 Shot Quality Scoring + Content Tagging        Est. 3-4 weeks
- J3 Audio Temporal Alignment                      Est. 4-6 weeks
- Public Extension API v1                          Est. 3-4 weeks
- Developer preview program (10 vetted partners)   Est. ongoing
- LAN sync adapter (team, no cloud)               Est. 2-3 weeks
- W.E. EDIT product launch                        Concurrent with J4
- FCPXML + DaVinci XML manifest implementation    Est. 1-2 weeks

Pricing: $199-299/year
Acquisition signal: Audio alignment at J3 attracts media tool acquirers
Revenue target: $199,000-299,000 at 1,000 users
```

---

### Phase 5 — Platform Scale

```
Status: Planned (18-24 months post-launch)
Prerequisite: J4 complete, API ecosystem established

Build items:
- J4 Highlight Detection + Rough Cut Export        Est. 6-8 weeks
- J5 Cross-Project Content Registry               Est. 6-10 weeks
- W.E. ARCHIVE product launch                     Concurrent with J5
- Optional cloud sync (W.E. C.A.P.E. Cloud)          Est. 8-12 weeks
- Team/enterprise licensing                        Est. 3-4 weeks
- Full public API documentation                    Est. 2-3 weeks
- NLE plugin ecosystem (Premiere, Final Cut)       Partner development

Pricing: $299-999/seat/year
Acquisition conversations: Full platform with production intelligence data
Revenue target: $999,000+ at enterprise scale
```

---

# PART VI: COMPETITIVE LANDSCAPE

## 19. Differentiation Matrix

| Capability | Hedge | ShotPut Pro | Kyno | Silverstack | PluralEyes | W.E. C.A.P.E. v1 | W.E. C.A.P.E. J5 |
|------------|-------|-------------|------|-------------|------------|----------------|----------------|
| Verified copy | ✅ Best | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Multi-camera scaffold | ❌ | ❌ | ❌ | Partial | ❌ | ✅ **Best** | ✅ **Best** |
| Timestamp corruption repair | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **Unique** | ✅ **Unique** |
| Proxy generation | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Archive Intelligence | ❌ | ❌ | Basic | Basic | ❌ | ✅ **Best** | ✅ **Best** |
| Audio temporal alignment | ❌ | ❌ | ❌ | ❌ | ✅ ($199 standalone) | ❌ (J3) | ✅ **Included** |
| Shot quality scoring | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (J2) | ✅ |
| Rough cut export | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (J4) | ✅ |
| Production intelligence | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (J5) | ✅ **Unique** |
| Local-first privacy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Open extension API | ❌ | ❌ | Limited | ❌ | ❌ | ❌ (J3) | ✅ |
| **Price** | **$99/yr** | **$99/yr** | **$149/yr** | **$500-1000/yr** | **$199 once** | **$149/yr** | **$299-999/yr** |
| **Time to editorial-ready** | ~2 hrs | ~2 hrs | ~2 hrs | ~1.5 hrs | N/A | **~1 hr** | **<30 min** |

---

## 20. The Workflow Replacement Argument

**Current creator workflow (4 separate tools, ~2 hours minimum):**

```
Card → Hedge ($99/yr)          → Verified copy
     → Finder (free, manual)   → Manual organization (~60 min)
     → PluralEyes ($199 once)  → Multi-camera alignment
     → Kyno ($149/yr)          → Proxy generation
                                 Total cost: $448/yr + $199 once
                                 Total time: ~2 hours minimum
```

**W.E. C.A.P.E. workflow (one platform, one run):**

```
Card → W.E. C.A.P.E. ($149-299/yr) → Verified + organized + aligned + proxied
                                   Total cost: $149-299/yr
                                   Total time: <1 hour (J3 complete)
```

**At J3, W.E. C.A.P.E. replaces $448/year of tools with a single $199/year platform at half the cost and half the time.**

---

# PART VII: ACQUISITION NARRATIVE

## 21. Market Context

Adobe acquired Frame.io in 2021 for **$1.275 billion**.

Frame.io at acquisition:
- Cloud video collaboration and review platform
- Approximately 300,000 users
- ~$50M ARR
- Zero AI features
- No ingest intelligence
- No production history data
- No local-first processing
- Required cloud upload of all footage

**The $1.275B was for the collaboration layer — not intelligence, not data, not AI.**

---

## 22. W.E. C.A.P.E. at J5 — The Differentiated Position

W.E. C.A.P.E. at full J5 maturity:

| Asset | Description | Frame.io Equivalent |
|-------|-------------|---------------------|
| Production intelligence AI | 5-layer intelligence stack across pre-edit workflow | None at acquisition |
| Local-first architecture | Privacy guarantee Adobe cannot match | Cloud-dependent |
| Creator production data | 2+ years of anonymized production history per user | Review/approval data only |
| Audio temporal alignment | PluralEyes capability included standard | None |
| Editorial rough cut AI | Machine-generated starting points | None |
| Extension API ecosystem | Third-party plugin marketplace | Limited |
| Multi-camera intelligence | Unique capability, no direct competitor | None |

**The acquisition conversation for W.E. C.A.P.E. is not about users or ARR alone — it is about production intelligence infrastructure that cannot be rebuilt from scratch.**

Any acquirer that buys W.E. C.A.P.E. also acquires:
- The only proven multi-camera temporal alignment pipeline for independent creators
- A production intelligence model trained on real creator workflows
- A local-first AI architecture that answers Adobe's cloud-dependency criticism
- An extension ecosystem with third-party camera parsers and NLE integrations
- A creator community that trusts the platform with their production history

**That is not a $1.275B conversation at the same metrics. That is a different valuation framework entirely.**

---

## 23. Staged Value Creation

| Milestone | Platform State | Value Drivers |
|-----------|---------------|---------------|
| Phase 3 launch | W.E. C.A.P.E. v1, 500-1,000 users | Proven PMF, recurring revenue |
| J3 complete | Audio alignment live | PluralEyes competitor + open API |
| J4 complete | Rough cut AI live | Editorial AI, W.E. EDIT launched |
| J5 + 2yr data | Full production intelligence | Acquisition-attractive, unique dataset |

---

## 24. Strategic Principles for the Lifestyle-to-Company Arc

1. **Prove the core before adding intelligence.** W.E. C.A.P.E. CAPTURE v1 ships with zero AI — the workflow proves market fit. AI features prove scale.

2. **Build the data layer from day one.** The registry starts writing at v1. At J5, 2 years of production history is already collected. This advantage cannot be manufactured at acquisition time.

3. **Privacy is the moat, not a constraint.** Local-first architecture is technically verifiable. "Your footage never leaves your machine" is an engineering guarantee, not a marketing claim. This positions W.E. C.A.P.E. against Adobe in a way no cloud-first competitor can match.

4. **The extension API creates the ecosystem before acquisition.** Third-party plugins, NLE integrations, and specialized classifiers built by the community are acquisition assets — not just features.

5. **Platform pricing is earned, not assumed.** W.E. C.A.P.E. launches at $149/year. The price increases as intelligence features ship and are validated by real users. Pricing is locked to demonstrable value.

---

*Document version 1.0 — Architecture Lock*  
*Next review: Phase 2 completion (proxy_workers:4 benchmarked)*  
*Distribution: W.E. C.A.P.E. core team + prjctlazrus.com (under executed NDA)*

---

**W.E. C.A.P.E. — The Production Intelligence Platform**  
*Local-first. Privacy by design. Your footage never leaves your machine without your explicit choice.*

*W.E. C.A.P.E. CAPTURE: The first product from W.E. C.A.P.E..*
