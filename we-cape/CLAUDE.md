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
Local:   ~/Curser/we-cape/
Package: wecape/ (canonical). we_capture/ retained only as deprecated CLI shim.
Commit:  04d3910 — Measures 2+4 implemented (pre-audit baseline)
Tests:   225/225 passing (207 prior + 3 camera-model + 15 annotations layer)
Entry:   python -m wecape   (config: wecape/config.yaml, profiles: wecape/profiles/)
Phase 1: COMPLETE
Phase 2: IN PROGRESS (registry live, Measures 1-5, hwaccel, rebrand complete,
         namespace migration COMPLETE, PipelineStage seam real — see Audit Remediation)
```

### Audit Remediation — June 23, 2026 (not yet committed)
```
See CODEBASE_AUDIT_2026-06-23.md for the full audit. Changes applied:
 #1 PipelineStage made real      wecape/capture/stages.py + core/stage.run_stages
 #1b pipeline.py REWIRED         run() now routes through run_stages() by default
                                 (pipeline.engine: stages|legacy; legacy = rollback).
                                 7 production stages extracted to _stage_* methods.
                                 Equivalence validated: legacy==stages output on
                                 synthetic 1080p multicam footage (2 groups, 7 proxies);
                                 in-suite guard test_engine_equivalence.py.
                                 AI hooks: disabled _NullIntelligenceStage (P6).
 #2 write_content preserves      INSERT..ON CONFLICT DO UPDATE w/ COALESCE (P5 now true)
 #3 empty-run guard              reader filter file_count>0 + finalize prunes empty runs
 #4 strict audit mode            registry.strict:true aborts run if audit unwritable (P3)
 #5 migration finished           tests -> wecape/tests/, config+profiles -> wecape/,
                                 entry -> python -m wecape, ProfileLoader path bug fixed
 #6 schema v2 migration          runs.we_forge_version -> we_cape_version (auto, lossless)
 #7 housekeeping                 .weflow->.wecape, junk files -> .trash_junk/, governance doc
 #8 CLI fixes (real-footage)     --proxy now works without --profile (was silently
                                 ignored); added --engine stages|legacy flag.
 REAL-FOOTAGE VALIDATION PASSED  6-file DJI shoot: legacy==stages output (TREES
                                 IDENTICAL), proxy stage 5t/1s/0f, 0 errors.
                                 Caveat: real MULTICAM grouping still untested
                                 (validation card was single-camera).
Verify: python3 -m pytest wecape/tests/ -q   (pytest-free: python run_tests.py)
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
- **P5 Registry Continuity** — non-destructive: content enrichment is never overwritten or nulled (field-preserving upsert); only empty no-op runs are pruned
- **P6 Staged Intelligence** — AI features never foundational to core pipeline
- **P7 Creator Data Sovereignty** — creator owns all production data

---

## Current Package Structure (actual, as of 2026-06-23 audit)

```
wecape/                 ← CANONICAL package (all source + tests live here)
├── __main__.py         ← `python -m wecape` entry
├── config.yaml         ← canonical config (moved from we_capture/)
├── profiles/           ← default.yaml, ryderz.yaml, google_drive.yaml (moved here;
│                          ProfileLoader resolves wecape/profiles — fixed June 23)
├── core/
│   ├── stage.py        ← PipelineStage ABC + run_stages() driver (NEW)
│   ├── sync.py         ← SyncAdapter ABC + LocalOnlySyncAdapter
│   ├── manifest.py     ← RunManifest (JSON+HTML+XML); field now we_cape_version
│   ├── errors.py       ← error taxonomy incl. RegistryAuditError (NEW)
│   └── config.py       ← centralized config: load/profile-merge/overrides/validate (NEW)
├── registry/           ← schema.py (v2 + migrate()), writer.py, reader.py
├── capture/            ← the working pipeline (NOT wecape/flow/)
│   ├── pipeline.py     ← orchestrator (calls components directly today)
│   ├── classifier.py grouper.py variants.py output.py audit.py proxy.py profile.py
│   ├── timestamp.py    ← _extract_dji_telemetry stub (still unintegrated, no tests)
│   ├── stages.py       ← PipelineStage adapters: Archive/Classify/Group/Variant/Proxy (NEW)
│   └── main.py         ← canonical CLI implementation
├── archive/            ← Stage 0.5 (detector/extractor/validator/repair/quarantine/manifest/stage)
├── flow/ sync/ api/ intelligence/   ← EMPTY namespace stubs (__init__ only; future)
└── tests/              ← 188 tests, must stay green (run: python -m pytest wecape/tests/)

we_capture/             ← DEPRECATED. Only main.py (shim) + run_tests.py (shim) remain.
                          Empty leftover dir we_capture/profiles/ could not be unlinked
                          on the working mount; safe to `rmdir` locally.

scripts/                ← ops tooling (NOT the engine)
├── dashboard.py        ← W.E. C.A.P.E. Production Dashboard: local, read-only (mode=ro),
│                          zero-CDN/zero-network self-contained HTML over the registry.
│                          Per-shoot cards (Tier 1 registry + Tier 2 shoot-folder), processing
│                          rates/breakdown, explainability (from LOGS), period pie charts, and
│                          annotations (reads annotations.db mode=ro — see below).
│                          Reference impl of UI_Dashboard_Design_Guidelines_v2.md.
│                          Docs: scripts/README_dashboard.md  ·  Run: python3 scripts/dashboard.py
├── annotations.py      ← Annotations store + CLI (2026-06-30). Human notes on shoots (target=run_id)
│                          and clips (target=content SHA) in a SEPARATE ~/.wecape/annotations.db —
│                          deliberately OUT of the deterministic registry (P1: engine output vs.
│                          mutable human notes stay separated). CRUD + tags + soft-delete (archive/
│                          restore/--hard); `targets` reads the registry ro to list valid run_ids/SHAs.
│                          stdlib-only, zero-network. Dashboard reads it ro and renders (card + table +
│                          Annotations section). annotations.db is NOT regenerable — back it up.
├── fcpxml_export.py    ← FCPXML export bridge (2026-06-30). CAPTURE multicam GROUPS -> one FCP
│                          multicam clip per group (each camera = an angle), placed by the
│                          corrected-timestamp delta; ungrouped single-camera clips ride along as
│                          ordinary Event clips (whole shoot in FCP; --groups-only to omit).
│                          Event items in CAPTURE-time order; clip names timestamp-prefixed so FCP
│                          Name-sort = chronological across cameras (--no-timestamp-prefix to omit).
│                          Clips tagged with <keyword> (Camera: <model>, Shoot: <date>) -> FCP Keyword
│                          Collections (per-camera / per-date sidebar grouping, no scrolling). Pipeline
│                          now persists content.corrected_timestamp for accurate export times.
│                          Angles labeled '<camera> - NN' (one per clip, chronological); multicam clips
│                          'Multicam NN'; every clip carries a Notes field (cam/shot/file/run/shoot)
│                          + videoRole=<camera> (FCP Roles: organize/filter/color the timeline by camera).
│                          Emits a format-matched starter <project> (empty timeline at the dominant
│                          resolution/fps) so FCP lands ready-to-edit, no setup prompt (--no-project omits).
│                          v1 = TIMESTAMP alignment (±s), NOT waveform —
│                          FCP 'Synchronize Clips' (or J3) locks audio (CAPTURE groups / FCP syncs).
│                          Assets carry original + proxy media-reps (FCP proxy workflow); proxies
│                          joined by SHA across runs (P5 upsert preserves them, so a no-proxy
│                          re-CAPTURE still links them). ffprobe formats + registry fallback;
│                          FCPXML 1.9 (FCP + Resolve). --stills <folder> adds images as still assets
│                          in a 'Stills' Keyword Collection (Additive-Ingest spec). Read-only.
│                          Docs: scripts/README_fcpxml.md · SPEC_Additive_Ingest_Found_Footage.md
├── capture_to_fcp.sh   ← one-command handoff (2026-06-30): CAPTURE -> fcpxml_export -> `open`
│                          the .fcpxml on FCP's import sheet. Detects the new run_id (summary line
│                          / newest registry row), passes extra args to wecape. STOPS at the one
│                          click FCP needs — never UI-scripts the import (no API; editor's call).
│                          Docs: scripts/README_fcpxml.md + SOP_fcpxml_import.md
├── export_wizard.py + wecape_export.command  ← novice-friendly guided export (2026-07-01):
│                          double-click the .command -> numbered shoot menu -> pick a number ->
│                          auto-detects the source Photos folder for stills (or drag one in); warns if
│                          the shoot's drive is offline -> runs fcpxml_export -> opens FCP + a
│                          'Next Steps in FCP' one-pager (scripts/next_steps_fcp.html) so the guidance
│                          is on screen at handoff. No run IDs/paths to type. One-time: chmod +x .command.
├── new_shoot.py        ← New Shoot orchestration CORE (2026-07-03). Phase 0 -> FCP front door:
│                          headless, unit-tested spine that chains verified offload -> CAPTURE ->
│                          FCPXML export -> open FCP behind ONE flow. Writes a shoot.yaml MANIFEST
│                          (name/date/location/trusted_clock) that feeds keywords + Production Health;
│                          pre-flight space check (+10% headroom) BEFORE any copy; per-step audit
│                          JSONL (_new_shoot_session.jsonl, P3); idempotent (offload resumes by hash,
│                          CAPTURE skips by SHA). Card detection (detect) GUESSES camera (high=name /
│                          medium=filenames / low=you choose via --card MOUNT=CAMERA) — an unlabeled
│                          card is NEVER silently offloaded. CLI: detect · plan (dry-run) · run. Every
│                          step still runnable standalone (thin wrapper — not the only path). GUI skin
│                          (PyWebView, license-clean; NOT PySimpleGUI which is now paid). stdlib-only,
│                          zero-network, read-only on cards. run_new_shoot emits an optional
│                          progress(stage,detail) callback (headless no-op when omitted).
│                          FOOTAGE-FIRST IDENTITY (2026-07-05): detect no longer trusts the volume
│                          NAME — it calls camera_identity to resolve the body from the footage
│                          (metadata serial > filename brand), demotes the mount name to a weak hint,
│                          and flags `conflict` when the label contradicts the footage. Fixes the
│                          card-label trap (SanDisk "DJIAction6" holds Action 5 Pro). Docs: README_new_shoot.md
├── camera_identity.py + cameras.yaml  ← Footage-first camera identity (2026-07-05). The volume label
│                          LIES (verified: "DJIAction6" card = Action 5 Pro), so identity is derived
│                          from the footage: metadata serial→registry (authoritative), else filename
│                          brand (reliable; DJI stays ambiguous→confirm), else the card name as a WEAK
│                          hint only. A label that contradicts the footage = CONFLICT → stop + confirm
│                          (the "never trust a MIS-labeled card" rule). Confidence INVERTED (name-only
│                          = low). cameras.yaml = serial→label registry seeded with the 3 verified
│                          bodies; add a camera by pasting its serial. exiftool reader is tolerant +
│                          injectable (finalize serial tags once the on-card probe runs). stdlib,
│                          zero-network, read-only. Confirmation-style prompts (novice
│                          confirms a fact, never guesses "5 or 6?"). ERROR TAXONOMY +
│                          PROVENANCE (2026-07-05): each result carries a named status
│                          (verified/conflict/ambiguous/label_only/unknown); new_shoot persists
│                          HOW each camera_id was derived (identified_by + identity_status) into
│                          shoot.yaml AND the session audit JSONL, and flags a human override
│                          (status=overridden) — P3 traceability / ISO-9001-style process control.
├── probe_camera.py     ← Camera discovery / onboarding tool (2026-07-05). Point it at a file/
│                          folder/card → fingerprint (structure, identity, time drift-free-vs-clock,
│                          telemetry STREAMS flagged) + coverage verdict (does identify() resolve it,
│                          is it in cameras.yaml, what's the gap) + PASTE-READY cameras.yaml stub &
│                          FAMILY_PATTERNS line. Smarter label (canonical / brand+code / "Unknown
│                          <Brand> - TODO"). Read-only by default; --add is the only writer (opt-in,
│                          never guesses). Boundaries: FLAGS djmd/gpmf telemetry, does NOT decode it;
│                          not a transcode tester; no engine coupling. Injectable exiftool/ffprobe →
│                          fully unit-tested (10 tests) without either tool. Docs: scripts/README_probe.md
├── new_shoot_gui.py + .html + .command  ← PyWebView SKIN over the new_shoot core (2026-07-03).
│                          BSD PyWebView (NOT PySimpleGUI, now paid); ONE dependency; macOS system
│                          WebView; reuses dashboard/cheat-sheet design. ZERO orchestration logic —
│                          Api bridge just calls detect_cards/build_preview/run_new_shoot. Window:
│                          Detect cards (footage-first STATUS badge + camera dropdown) -> details ->
│                          destinations -> Preview plan (writes nothing) -> Start (threaded, streams live
│                          log via the progress callback; opens FCP + Next-Steps). IDENTITY UI (2026-07-05):
│                          badge is driven by identity_status (conflict=red + a why-line, verified=green,
│                          ambiguous/label_only=confirm); a name/footage CONFLICT must be explicitly
│                          acknowledged at Start; the run payload carries identity provenance through so
│                          overrides are audited (JS syntax-checked; the VISUAL pass still runs on the Mac).
│                          build_preview/do_run unit-tested pywebview-free. Install: pip3 install
│                          pywebview. Everything still doable from CLI. Docs: README_new_shoot.md
├── offload_cards.py    ← Verified card offload — the Hedge-style FRONT END (2026-06-30). Card ->
│                          <dest>/<shoot>/<camera>/ per-camera folders (+ optional 2nd dest), every
│                          copy SHA-256-verified vs source (mismatch = hard fail, not silent),
│                          resumable, JSON manifest, NEVER deletes the card. Two copies satisfied
│                          BEFORE CAPTURE (Principle #1). offload -> CAPTURE.
│                          SHOOT MANIFEST (2026-07-04): --trusted-clock/--shoot-date/--location/
│                          --event/--notes write a shoot.yaml beside the footage at offload (the one
│                          moment the operator is present, per SPEC §3/§10). Each card's camera is
│                          merged into cameras: [...] (offloading all cards builds the list); scalars
│                          overwrite; idempotent per camera. trusted_clock is what upgrades the Health
│                          Report from "likely" to definitively-named culprit — no GPS needed.
│                          Docs: README_offload.md
├── reconcile.py        ← Footage reconciliation / coverage audit (2026-07-01). Cross-checks footage
│                          folders vs the registry: PROCESSED / UNPROCESSED (gap) / DUPLICATE (byte-
│                          identical, reclaimable). quick (filename+size) or --hash (SHA-256, definitive).
│                          Read-only, stdlib. Answers "is every file accounted for?"
├── srt_telemetry.py    ← .SRT sidecar telemetry (2026-07-03). Parses DJI/Osmo .SRT sidecars for
│                          drift-free record-time + GPS; stores in a SEPARATE ~/.wecape/telemetry.db
│                          (NOT the deterministic registry — P1/PII, like annotations.db), keyed by
│                          clip content SHA. Skips non-telemetry caption .SRT (no datetime). scan/show/
│                          list CLI. GPS full-fidelity locally, hashed on egress (D1). Read-only, stdlib.
│                          Feeds the Health Report's authoritative clock. Docs: SPEC_SRT_Telemetry.md
├── health_report.py    ← Production Health Report / postmortem (2026-07-03). Reads the registry
│                          READ-ONLY; explains a shoot honestly: 0-files-lost, per-camera clock health,
│                          the cure + a *labelled simulation* of the projected gain. Two clock signals:
│                          intra-camera spread (one camera contradicting its own dates → some clips
│                          wrong-dated — the provable, roll-time-immune signal; caught real O-SIX
│                          Insta360 7/48 clips at 2018) and inter-camera skew (whole clock off).
│                          Honesty guardrails TESTED: no "% sync accuracy" ever; names a culprit only
│                          on a ≥1-day (provable) offset or with a trusted_clock/telemetry reference,
│                          else "likely" + outlier only. Upgrades automatically when a shoot.yaml
│                          trusted_clock or telemetry.db (.SRT GPS) is present. stdlib, zero-network.
│                          DELIVERY (2026-07-04): standalone <run>_health.md (--out); INTO the run's
│                          LOGS/summary.md (--append-summary, idempotent delimited block, NO engine
│                          coupling — P4); and a compact 🩺 Health row on each dashboard shoot card
│                          (dashboard.py reuses health_report.build_report_data, read-only).
│                          TRUSTED-CLOCK PROMPT (2026-07-04): when NO ground truth is present but a
│                          clock disagreement is detected, the report tells the creator to add
│                          `trusted_clock: <agreeing camera>` to shoot.yaml (suggests a camera that
│                          AGREES, never the outlier) — turning the "likely" gap into an actionable
│                          habit. Suppressed once a manifest/telemetry reference exists.
│                          Spec: SPEC_Production_Health_Report.md
├── mirror_verify.sh + restore_test.sh  ← Backup PRIMITIVES (2026-07-05, for the storage
│                          3-2-1 remediation — see STORAGE_RISK_AND_BACKUP_PLAN.md). mirror_verify:
│                          SHA-256 verified folder->folder copy, ADDITIVE (never deletes), dry-run
│                          default, --go copy+verify, --verify-only (bit-rot check rsync misses).
│                          restore_test: canary restore from a local mirror OR rclone remote ->
│                          scratch -> checksum vs live source, logs PASS/FAIL to RESTORE_TESTS.md
│                          (also an rclone-crypt passphrase-recovery drill). Topology-agnostic
│                          (path args), macOS bash-3.2 safe, handles spaces. 5 subprocess tests
│                          incl. corruption detection. Run: chmod +x once, then dry-run before --go.
├── backup_footage.sh + com.wecape.footagebackup.plist + backup_sources.txt  ← Footage 3-2-1
│                          orchestrator (2026-07-05). Verified mirror of a priority-folder LIST ->
│                          target drive + offsite (rclone crypt) + restore drill, reusing
│                          mirror_verify/restore_test. GUARD: refuses to write unless the target is a
│                          real, WRITABLE, MOUNTED volume — never the boot disk (unmounted-target stray
│                          trap), never a read-only TM disk (Got My BackUP). Dry-run default; --go /
│                          --offsite / --restore-test. plist = weekly scheduled template (safe when the
│                          drive is absent — guard refuses + logs). Repoint --target to the ≥12TB drive
│                          when it arrives. 5 subprocess tests incl. the boot-volume refusal.
│                          VERIFIED TOPOLOGY (2026-07-05): disk13 (one 20TB USB enclosure) holds 10TB
│                          originals + Holder Mac (legal) + old timemachine = the SPOF; originals had
│                          ZERO backup; G-DRIVE SSD (disk6) is APFS-container-CORRUPT (won't mount).
│                          Legal docs now 3-2-1'd (WE_CAPE_OUTPUT + gcrypt). See STORAGE_RISK_AND_BACKUP_PLAN.md.
├── backup_holder_mac.sh + com.wecape.holdermacbackup.plist + com.wecape.registrybackup.plist
│                          ← asset-protection: 4.6TB Holder Mac (weekly) + ~/.wecape 3-2-1 (internal
│                          staging + offsite rclone copy + external mirror; daily via --registry-only).
│                          SQLite online .backup + integrity check. Docs: README_backup.md
└── organize_iphone_backup.sh   ← iPhone originals organizer/verifier (README_iphone.md)
```

> Reality check vs the "Target Package Structure" below: working code went to
> `wecape/capture/`, **not** `wecape/flow/`. `flow/ sync/ api/ intelligence/` are
> still empty. `SyncAdapter`/`LocalOnly` live in `core/sync.py`, not `sync/local.py`.
> Treat the Target block as aspirational, not built.

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
    we_cape_version     TEXT NOT NULL,   -- v2 rename from we_forge_version (auto-migrated)
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
    source_clip             TEXT,    -- v3: derivation lineage — source stem a select derives from
    source_clip_sha         TEXT,    -- v3: source clip SHA-256 (if in run) — pins lineage to content
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

### Derivation Lineage & Select Naming Convention (schema v3, 2026-06-29)
```
Problem: §3/§8 LOCKED variant detection treats indexed (1),(2) as duplicate
         variants. A creator using (N) for CURATED SELECTS (segments cut from a
         long source) gets them flagged as variants — spec-correct, but wrong
         intent. Spec collision, not a bug (files are always preserved).

CONVENTION (adopt going forward): name curated selects
         <source_stem>_sel<NN>   e.g.  VID_20260314_093040_00_006_sel01.mp4
  - '_sel<NN>' is OUTSIDE all reserved variant patterns -> stays standalone.
  - KEEP the YYYYMMDD_HHMMSS block so §5 filename-timestamp parsing still works.
  - Rename BEFORE CAPTURE ingest (keeps proxy<->original relink + registry clean).

LINEAGE (schema v3): wecape/capture/derivation.py + lineage config records, per
  select, content.source_clip (source stem) and source_clip_sha (source SHA-256
  if the source is in the run). SEPARATE from variant detection — 'derived from',
  not 'duplicate'. Additive, opt-in (lineage.enabled, default true; no-op for
  non-_sel names). Feeds W.E. ARCHIVE (J5) cross-project lineage.
  Query example:  SELECT filename FROM content WHERE source_clip = '<stem>';
  Validated end-to-end 2026-06-29 (selects -> source_clip + source_clip_sha).
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
- UI layer (packaged / signed app) — after performance gate passes.
  NOTE: a read-only dashboard PROTOTYPE now exists (scripts/dashboard.py, gate passed) — a
  window over the registry, not the shippable app. Docs: scripts/README_dashboard.md +
  UI_Dashboard_Design_Guidelines_v2.md.

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
  - Samsung 990 PRO 4TB (ZikeDrive Z666 TB4): INSTALLED 2026-07-03 — primary NVMe
    (WE_CAPE_OUTPUT). Connected directly to Mac Studio TB4 port (NOT the StarTech dock).
    Enables proxy_generation.workers: 4 (config already set); ~3,098 MB/s confirmed.
```

### Camera Hardware Identity — canonical (2026-07-04, from on-camera Device/Camera Info)
```
Body                | Device Name          | Serial          | FW (device / camera)     | Canonical label
--------------------|----------------------|-----------------|--------------------------|------------------
DJI Osmo Action 6   | OsmoAction6-84CB     | 9KRXNC800BGX5N  | 01.04.14.02 / 10.00.34.29| DJI ACTION 6
DJI Osmo Action 5 Pro| OsmoAction5ProA715  | 82JXN4500BW1VE  | 01.06.01.04 / 10.00.16.13| DJI ACTION 5
Insta360 X5         | Insta360 X5          | IAHEA2503SK8FE  | cam v1.11.6 / MCU v1.2.5 | Insta360 X5
                    |                      |                 | (HW 520)                 |
Note: the camera self-reports "OsmoAction6" (no "Pro"); our label "DJI ACTION 5" == the
Action 5 **Pro** (DJI ships only the Pro variant of the 5). Both DJIs are GPS-for-Action
capable; the X5 is not (see SPEC_SRT_Telemetry / GPS review).

EMBEDDED MODEL CODE (exiftool probe 2026-07-05, RESOLVED): DJI files carry NO plain
Serial tag; the body is in the Category tag's `model_name:AC0NN` token — the strongest
DJI signal. DJI's codes are OFFSET from the marketing name:
    AC003 = Osmo Action 4  ·  AC004 = Osmo Action 5 Pro  ·  AC006 = Osmo Action 6
  WEDDING card    -> AC006 = Action 6      (confirmed)
  DJIAction6 card -> AC004 = Action 5 Pro  (confirmed: camera self-reports "OsmoAction5ProA715"
                     + it's the only non-Action-6 DJI in the kit; NOT an Action 4).
Both mapped in cameras.yaml → identity is now footage-authoritative for all 3 bodies.
The DJIAction6 card now resolves to Action 5 Pro AND flags a conflict vs its volume name.
Unmapped codes (e.g. AC003) still defer to "confirm which body" — never a mislabel.
SCOPING: the WEDDING and DJIAction6 SanDisk cards are STANDALONE (a wedding shoot / a
single-camera reliability test) — NEITHER is part of the O-SIX RYDERZ MC Community
Service production run (that footage is in the 10TB O-SIX per-camera folders). They
were just handy probes to read each BODY's model code; the codes are kit-wide, so
O-SIX DJI footage carries the same AC004 (5 Pro) / AC006 (6).
O-SIX SPLIT FOOTAGE-VERIFIED (2026-07-05): probed /Volumes/10TB/O-SIX RYDERZ MC
Community Service — every clip in DJI ACTION 5/ reports AC004 (10 clips, = registry
Action 5 count) and every clip in DJI ACTION 6/ reports AC006. Folders match the
embedded codes → the WEF_20260630 camera split is authoritative, no mislabels.
(Minor, benign: the Action 6 folder holds 20 .MP4 vs 19 ingested camera_id records —
one variant/dup not ingested; and the Insta360 X5 folder's 49 .MP4 are NOT the raw
.insv the 48 records came from. Run reconcile.py if exact accounting is wanted.)

⚠ CARD-LABEL TRAP (verified 2026-07-04): the SanDisk VOLUME NAMES are misleading —
they do NOT match their contents. OFFLOAD BY CONTENT, NOT BY LABEL:
  SanDisk "WEDDING"    -> holds DJI Osmo Action 6 footage   -> --camera "DJI ACTION 6"
  SanDisk "DJIAction6" -> holds DJI Osmo Action 5 Pro footage -> --camera "DJI ACTION 5"  (NOT 6!)
Consequence: new_shoot `detect` guesses camera from the MOUNT NAME (high-confidence path),
so it would confidently MIS-label both of these. Any past run that trusted the "DJIAction6"
label (e.g. reliability run #2) recorded the wrong camera_id — re-verify/re-CAPTURE if that
footage matters. FIX DIRECTION: identify the body from the FOOTAGE (embedded model/serial
via exiftool) or a serial→label registry, not the volume label. Until then: pass --camera
explicitly and ignore the SanDisk names.
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

- All 225 tests must pass before any commit merges
- New features require tests before merge
- `python3 -m pytest wecape/tests/ -q` is the current gate (all tests now live in wecape/tests/)
- Pytest-free acceptance subset: `python run_tests.py` (repo root; §17 suite only)
- Namespace reorganization COMPLETE — imports verified, 225/225 passing

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
          NOTE (2026): "DJI(29)" lumped BOTH bodies. Real kit = Insta360 X5 +
          DJI Osmo Action 5 + DJI Osmo Action 6 (no GoPro). VALIDATED 2026-06-30
          (WEF_20260630_125435_06980D): re-CAPTURE split DJI(29) -> Osmo 6 (19) +
          Osmo 5 (10); Insta360 X5 (48) unchanged; camera_id now persisted. Groups
          stayed 2 (both DJI bodies overlapped WITH the Insta360, not DJI-only) —
          correct for this shoot.
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
3. DJI telemetry timestamp — FUTURE ENHANCEMENT (deferred by decision 2026-06-24).
   Stub cleaned to an honest no-op placeholder; intended design (parse '<name>.SRT'
   sidecar for drift-free time, opt-in/default-off) documented in timestamp.py.
   .SRT stays classified as reference for now. Would let ±15s window (§7) shrink.
4. Windows platform support
5. Executive Summary update
6. core/config.py — DONE 2026-06-24 (centralized config layer; main.py + pipeline use it)

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

## Hardware — Samsung 990 PRO NVMe (INSTALLED 2026-07-03)

Samsung 990 PRO 4TB + ZikeDrive Z666 TB4 (~$410) — PURCHASED + INSTALLED.
Connected DIRECTLY to Mac Studio TB4 port (NOT the StarTech dock). ~3,098 MB/s.
config.yaml already set: proxy_generation.workers: 4 (no change needed).
CONFIRMED 2026-07-04 on installed hardware: 48.8 min / 0.62 min/proxy / 0 errors
(run WEF_20260704_022704_099669, USB source → NVMe output) — well under the <90 min
gate. workers=4 + VTB hwaccel effective on the real drive (was previously anticipatory).


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
| Production (rewired/stages) | USB HDD | 4 | VTB hwaccel | 51.9 min | 0.66 min/proxy | PASS |
| NVMe-confirm (installed drive) | USB→NVMe | 4 | VTB hwaccel | 48.8 min | 0.62 min/proxy | PASS |

Production run: WEF_20260622_221150_204D47
Output: /Volumes/WE_CAPE_OUTPUT/O-SIX_RYDERZ_MC/Community_Service_2024/
Source: /Volumes/10TB/O-SIX RYDERZ MC Community Service (USB)
Note: USB source adds ~16 min vs NVMe source — gate met on both

Production run (rewired engine): WEF_20260624_001707_C5A8AB — June 24, 2026
Engine:  stages — run() routed through run_stages(). FIRST production-scale
         validation of the rewired orchestrator (see Audit Remediation #1b).
Output:  /Volumes/WE_CAPE_OUTPUT/O-SIX_RYDERZ_MC/Community_Service_2026/
Source:  /Volumes/10TB/O-SIX RYDERZ MC Community Service (USB)
Result:  95 files | 2 groups | 23 variants | 4 diagnostics | 0 errors | Proxies 79t/0s/0f
Runtime: 3111.68s = 51.9 min — on-benchmark vs June 22 (49.9 min); hwaccel confirmed active.
         (Pre-flight's ~138m line was the software-decode comparison, not the actual path.)
Validation: reproduced MG-02 ground truth (2 groups, 23 variants, 4 diagnostics).
         95 real files vs MG-02's 103 = the same 95 + 8 .crdownload partial-download
         artifacts that are absent from this (cleaner) source copy. 0 proxy failures,
         including every Insta360 .insv. Rewired engine matches the proven pipeline
         at production scale.

### Reliability Runs (real-world usage — "ten runs prove reliability")
```
#1  O-SIX RYDERZ MC Community Service  — WEF_20260624_001707_C5A8AB (above)
    Multicam (Insta360 X5 + DJI Action 5/6). 95 files, 2 groups, 23 variants,
    79 proxies, 0 errors. Reproduced MG-02 ground truth on the rewired engine.

#2  DJIAction6 card (single-camera)    — June 24-25, 2026
    Source: DJIAction6 NTFS card -> copied to WE_CAPE_OUTPUT/DJIAction6_2026/_source
    Output: /Volumes/WE_CAPE_OUTPUT/DJIAction6_2026/
    Files:  157 (39 video .MP4 + ~118 DJI sidecars: .LRV/.SRT/.THM)
    Result: 0 groups (single camera — correct) | 0 variants | 0 errors | 1 diagnostic
    Proxies: 39 transcoded (run 1, WEF_20260624_215037_BC0C7F)
    IDEMPOTENCY PROVEN: re-run (WEF_20260625_013821_E5FEF7) completed in 54.66s,
    skipped all 39 by SHA registry match, 0 re-transcodes, 0 errors. Re-running a
    processed shoot is safe and ~25x faster than the original transcode pass.
    Note: .SRT telemetry sidecars present on card -> real test data for the
    deferred DJI-telemetry enhancement (backlog #3).

#3  O-SIX camera re-CAPTURE (per-body split) — WEF_20260630_125435_06980D, June 30 2026
    FIRST run after the camera_folder_patterns fix. Source per-camera folders
    (DJI ACTION 5/ · DJI ACTION 6/ · Insta360 X5/) now resolve to the specific body.
    Files: 95 | Groups: 2 | Variants: 23 | Errors: 0 | Diagnostics: 4 (no-proxy validation).
    Split CONFIRMED in registry: DJI Osmo Action 6 (19) + DJI Osmo Action 5 (10) =
    the old lumped DJI(29) EXACTLY; Insta360 X5 (48) unchanged; camera_id now persisted
    (was null). Groups held at 2 (NOT a regression): both DJI bodies overlapped WITH the
    Insta360, joining existing groups as a 3rd source rather than forming DJI-only groups.
    New validated camera-identity baseline. Proxies unaffected (split is metadata, not
    pixels) — no re-transcode needed for the existing 79-proxy edit set.

#4  O-SIX NVMe confirmation — WEF_20260704_022704_099669, July 4 2026
    FIRST benchmark on the INSTALLED Samsung 990 PRO NVMe (ZikeDrive Z666, direct
    TB4 Receptacle 1, 40 Gb/s USB4 — verified NOT behind the StarTech dock).
    Source: /Volumes/10TB O-SIX (USB) -> Output: WE_CAPE_OUTPUT/O-SIX_NVMe_confirm (NVMe).
    Files: 95 | Groups: 2 | Variants: 23 | Errors: 0 | Diagnostics: 4 | Proxies 79t/0s/0f.
    Runtime: 2926s = 48.8 min (0.62 min/proxy) — on-benchmark vs June 22/24 (49.9/51.9),
    well under the <90 min gate. Confirms workers=4 + VTB hwaccel effective on real
    installed hardware (config was previously anticipatory). Ran via scripts/benchmark_run.sh.
```

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
  STATUS (2026-06-23): NOW ENFORCED IN CODE.
    - reader.list_runs() / get_aggregate_stats() exclude file_count=0 by default
      (pass include_empty=True for raw history)
    - writer.finalize_run() prunes a run that finalizes with 0 files
  The historical WEF_20260622_020843_66257B row in the live DB should be deleted
  once (DELETE FROM runs WHERE file_count=0); new empty runs no longer persist.

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

### Camera Identification — per-body distinction (2026-06-29)
Actual kit:         Insta360 X5 + DJI Osmo Action 5 + DJI Osmo Action 6. No GoPro
                    (GoPro is a supported-but-unused config pattern; it appeared
                    only in synthetic test fixtures, never real footage).
Bug fixed:          camera_folder_patterns was DEAD CODE — the config read sat after
                    a `return` inside the static _safe_size(), and _match_camera_folder()
                    was never called. So every DJI body collapsed to a generic "DJI"
                    and the Osmo 5/6 distinction did nothing.
Fix:                read moved to __init__; _match_camera_folder() now called in
                    classify(). When footage is in a per-camera folder
                    ("DJI ACTION 5/6", "Insta360 X5"), camera_source resolves to the
                    specific body. camera_id now persisted to the registry.
Decision (2026-06-29): two DJI bodies are DISTINCT §7 grouping sources (a physical
                    camera = an angle). More correct — two DJI cameras rolling the
                    same moment now form a group (previously did not).
Re-validate:        existing runs (O-SIX, MG-02) were processed pre-fix (both DJI as
                    one source). Re-CAPTURE to apply.
Validated:          2026-06-30, run WEF_20260630_125435_06980D (O-SIX, no-proxy).
                    Split DJI(29) -> Osmo Action 6 (19) + Osmo Action 5 (10) [exact
                    match to the lumped 29]; Insta360 X5 (48) unchanged; camera_id
                    persisted. Groups held at 2 — the two DJI bodies overlapped WITH
                    the Insta360 (joined existing groups as a 3rd source), so no new
                    DJI-only groups formed. Correct for this shoot; future DJI-only
                    overlapping moments will now group.
Status:             Correctness fix + intentional deviation from the lumped baseline.

### Stage 0.5 Archive Engine — Enabled (intentional deviation)
RFQ LOCKED spec:    archive_engine disabled by default (Phase-1 gated, v4.1 retail determinism)
Production config:  archive_engine.enabled: true
Justification:      Acts as a production safeguard — quarantines partial/corrupt
                    downloads (.crdownload/.part/.tmp) and handles archives before
                    they reach the pipeline. Caused zero harm in the June 24
                    production run (95 files, 0 errors); would have caught the 8
                    .crdownload artifacts that polluted the MG-02 baseline.
Decision:           2026-06-24 — keep enabled as an intentional production safeguard.
Status:             Documented deviation — defensible, validated, intentional.

### Proxy timecode for FCP proxy workflow (2026-06-30)
Problem:   proxies were re-encoded with `-map_metadata -1` -> started at TC 00:00:00,
           while DJI/Insta360 originals carry time-of-day timecode. FCP then rejected
           the CAPTURE proxies on FCPXML import: "proxy media incompatible … no shared
           media range" (clips showed "Missing Proxy"; originals imported fine).
Fix:       wecape/capture/proxy.py — _get_timecode() reads the source timecode (ffprobe
           format/stream tags) and _build_cmd re-stamps it via `ffmpeg -timecode <TC>`
           so proxy and original share a timecode range. Config toggle
           proxy_generation.embed_source_timecode (default true).
Apply:     requires RE-TRANSCODE — existing proxies predate the fix. Re-run the proxy
           stage (--proxy) to regenerate FCP-compatible proxies.
Validated: cmd construction + 4 new tests (261/261). TRUE proof is an FCP re-import
           after re-transcode (couldn't run ffmpeg/FCP in the build env).

### RFQ Tests 1-5 — PASS
All five tests covered by existing test suite.
Test 3 variant patterns (copy/final/backup) confirmed implemented in variants.py.

### Test 6 Quantitative Thresholds — CLOSED July 14, 2026
Status:             DEFINED + IMPLEMENTED (commit 2a3220e).
                    RFQ is self-issued; thresholds defined from validated
                    production data (MG-01 through MG-05):
                    6.1 Ingest 100% | 6.2 Zero errors | 6.3 Logs 5/5 +
                    traceability | 6.4 Proxy >=95% (empirical 100%) |
                    6.5 Classification >=75% named | 6.6 Determinism |
                    6.7 Run ID consistency.
                    RFQ AUDIT COMPLETE — Tests 1-6 ALL PASS. 391/391.


---

## SRT Sidecar Timestamp Source — LIVE (gated) — July 14, 2026

Status:    Implemented b6ef97c. Stub _extract_dji_telemetry is now live.
Gate:      timestamp.enable_srt_telemetry (config.yaml) — DEFAULT FALSE.
           Gate off = byte-identical to validated baseline (395/395).
Behavior:  When enabled, .SRT sidecar datetime becomes the highest-priority
           timestamp source (fallback_level=0, confidence=high).
           Datetime ONLY — no GPS parsing, no telemetry.db writes in the
           engine path (D1). Full telemetry: scripts/srt_telemetry.py.
Payoff:    Drift-free timestamps address the clock-skew root cause behind
           the §7 grouping-window deviation. Future option: enable gate +
           test grouping at RFQ-original ±5s window on SRT-equipped shoots.
Tests:     wecape/tests/test_srt_timestamp_gate.py — 4 cases
           (present / absent / malformed / gate-off).


---

## Registry Anomalies — July 18-19, 2026 (AlphaRoundUp intake)

WEF_20260718_131502_D3396B  aborted at Measure-2 (126 eligible — LRV
                            misclassification, caught pre-transcode)
WEF_20260719_040129_25F16B  CONTAMINATED: output-inside-input — ingested
                            own prior output (658 files, 39 false groups,
                            62 proxies overwritten by proxies-of-proxies).
                            Output tree deleted+rebuilt; run record stands
                            (append-only). EXCLUDE from analytics.
WEF_20260719_095346_454ACB  aborted at attestation (tty wedge)
WEF_20260719_172839_E82E8A  CLEAN authoritative AlphaRoundUp run:
                            389 files · 1 group · 150/151 proxies ·
                            clip 0023 corrupt-at-source (see shoot.yaml)

## Backlog additions — from AlphaRoundUp intake
1. GUARD: refuse/warn when --output is a child of --input (root cause
   of the contaminated run; five-line check in preflight)
2. Attestation prompt tty/EOF fix — wedged 3x in one session
3. Estimator: duration-based (source_hours x rate / workers) — 27min
   estimate vs 55min actual on X5 run; pre-flight already scans durations
4. offload_cards: write _offload_manifest.json OUTSIDE media tree
   (created phantom 2026-07-18 date folder)
5. offload_cards: probe first file metadata, warn if contradicts
   --camera (card labels lie — Action5Pro/Action6 swap caught by hand)
6. Review .lrf/.thm/.scr classification (DJI sidecars) — .lrv fix
   precedent; verify they route reference, not camera-eligible


## Criterion 2 Baseline — RWP (Riding With Purpose) — FILED 2026-07-21
64 hrs total (55-75 bracket, medium confidence) — curation 12 · review 12 ·
edit 30 · graphics 5 · publish 5. Evidence: CapCut draft lineage (0621 x2,
0706, 0706_FINAL Jul 12, 0706-copy Jul 15 publication master). Measured:
calendar/session structure. Inferred: within-session hours. AlphaRoundUp
target: <=32 hrs. Deliverable 1 of 3 (Board directive) COMPLETE.


## Deliverable 3 — Studio Session #1 — Curation Phase COMPLETE 2026-07-26
X5 curation: 139 exports (93 ProRes .mov + 46 .mp4, 557 GB) + 10 Clip Anchor
GPX + 54 screenshots. MEASURED curation clock: ~38 hrs (34-42) across 5
sessions Jul 22-26, derived from export mtimes. CRITERION-2 FLAG: curation
alone exceeds the 32-hr total target — deep-curation strategy (3.3x RWP
export volume); ratio-based restatement deferred to W.E.I.C.P. post-edit.
GPS CORRECTION: X5 GPS was sparse (anchor-grade), not absent. Telemetry
Correlation Standard adopted as policy (ADR-003 candidate), build deferred.
