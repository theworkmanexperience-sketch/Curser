# W.E. FLOW / W.E. FORGE — Phase 1 Planning

**Phase 0 Status:** ✅ COMPLETE & GREEN (commit `940cb62`)
**Phase 1 Status:** 🔄 IN PROGRESS (commit `4d054e4`)
**Last updated:** 2026-05-27

---

## Phase 1 Goals

Activate advanced capabilities on top of the locked deterministic Phase 0 core
while maintaining zero breaking changes.

---

## Core Pillars — Actual Status

### ✅ Pillar 1: Archive Intelligence Activation (COMPLETE)

**Commit:** `v1.1.1` | **Tests:** 21/21 passing
**Production validated:** `WEF_20260527_140214_182FC2` — 103 files, 6 `.crdownload`
quarantined, 1 `.crdownload.zip` extracted (9 GB nested partial inside)

Delivered:
- Stage 0.5 integrated into main pipeline (feature-flagged, default off)
- Magic-byte detection, repair, and quarantine
- `QUARANTINE/` and `ARCHIVE_EXTRACTED/` output folders
- 21/21 acceptance tests covering archive scenarios
- Production bug fixes (P1–P4):
  - `__MACOSX/` and `._*` macOS resource fork filtering
  - `.crdownload 2` Chrome duplicate naming detection
  - Nested partial download quarantine (post-extraction scan)
  - Files-ingested count corrected to post-Stage-0.5 pool size

Activate via: `--profile google_drive`

---

### ⏸ Pillar 2: DJI / Insta360 Telemetry Parser (DEFERRED — evidence-driven)

**Original plan:** Parse CAM meta binary stream via ffprobe; extract GPS +
accurate `creation_time`; update timestamp fallback chain.

**Decision:** Deferred. Production analysis on Ryderz dataset (103 files, March
2026 shoot) showed the 9 timestamp fallbacks were `.crdownload` partial downloads
and a PDF — not DJI camera files. DJI files with `DJI_YYYYMMDDHHMMSS` naming are
already parsed at `fallback_level=0` from the filename. No DJI file fell back to
`file_stat_mtime` on real client data.

**Revisit when:** A production run shows DJI files at `fallback_level=2`.
**Compliance:** PI-04 remains open. GPS redaction not required until GPS data
is actually extracted.

---

### ✅ Pillar 3: Config / Profile-Based Workflows (COMPLETE)

**Commit:** `4d054e4` | **Tests:** 11/11 passing
**Production validated:** `WEF_20260527_185428_26967E` — profile loaded, baseline held

Delivered:
- `engine/profile.py`: ProfileLoader with `deep_merge()`, instance attributes
  for test isolation, system + user dir resolution
- `profiles/default.yaml`: annotated reference of all overridable keys
- `profiles/ryderz.yaml`: O-SIX RYDERZ client profile (15s window, symlink,
  folder patterns, camera offsets)
- `profiles/google_drive.yaml`: Google Drive delivery profile (archive engine
  on, copy mode)
- `--profile` and `--list-profiles` CLI flags
- Profile resolution order: `config.yaml` → `profiles/{name}.yaml` →
  `~/.weflow/profiles/{name}.yaml` (last wins, deep merge)

Note: Implementation uses separate YAML files in `profiles/`, not named
sections in `config.yaml` as originally planned. This is the correct design.

---

### ✗ Pillar 4: Performance Optimization (NOT STARTED)

Original targets:
- Parallel processing (configurable `max_workers`) — already configurable
- Checkpointing / resumable runs — not built
- Memory optimization for large shoots (>500 GB) — not addressed
- Benchmark: Studio tier ≥ 80 GB/hr on Apple Silicon — not validated

Note: The 712 GB/hr symlink benchmark is not a performance metric — it measures
filesystem metadata creation, not media processing. Proxy generation benchmarks
are the meaningful target and require Phase 1-E (proxy generation) to exist first.

---

### ✗ Pillar 5: Enhanced Logging & Observability (NOT STARTED)

- Prometheus metrics scaffold — not built
- Detailed performance telemetry per stage — not built
- Stronger idempotency guarantees with checkpoint files — not built

---

## Additional Phase 1 Items (Discovered During Build)

These were not in the May 25 plan but are in scope for Phase 1:

| ID | Item | Status | Priority |
|----|------|--------|----------|
| Phase 1-D | Error/diagnostics reporting | Not started | High |
| Phase 1-E | Proxy generation (H.264 720p) | Not started | High |
| — | Screenshot `contains` fix in classifier | Not started | Medium |
| — | Cross-run content registry (SHA-256 per-client) | Not started | Medium |
| — | Audio field recorder classification — verify wiring | Not started | Medium |
| — | Per-camera UTC offset wiring in grouper — verify | Not started | Medium |
| — | `_preflight.json` `output_drive_encrypted` field | Not started | Low |
| — | Hash `pii_flagged_filenames` before storage | Not started | Medium |

---

## Spec Deviations From Phase 0 Design

| Item | Original Spec | Current | Evidence |
|------|--------------|---------|----------|
| Multicam grouping window | ±5s LOCKED (§7) | ±15s default (configurable) | Ryderz dataset: 8s real-world gap |
| Stage numbering | Stages 0–7 (Pre-flight = Stage 0) | Pre-flight unlabeled; Stages 0–6 | Architectural decision |
| Stage order | Timestamp (2) → Classification (3) | Classification (1) → Timestamp (2) | Better design — class before extract |
| Config profiles | Named sections in `config.yaml` | Separate YAML files in `profiles/` | Better design — separation of concerns |

---

## Implementation Order — Revised

1. ✅ Archive Intelligence (complete)
2. ✅ Config Profile System (complete)
3. 🔄 Phase 1-D: Error/diagnostics reporting (next)
4. 🔄 Phase 1-E: Proxy generation
5. ⏸ Performance optimization (after proxy)
6. ⏸ Enhanced logging (after proxy)
7. ⏸ DJI telemetry parser (evidence-driven)

---

## Acceptance Criteria — Updated

- [x] All new features behind feature flags (zero impact on Phase 0)
- [x] 100% backward compatibility with v4.1 Phase 0 behavior
- [x] Archive scenarios covered by tests (21/21)
- [x] Profile system covered by tests (11/11)
- [ ] Proxy generation implemented and tested
- [ ] Error/diagnostics separated in summary output
- [ ] Screenshot classification fix verified
- [ ] Cross-run content registry implemented
- [ ] Updated compliance delta showing PI-04 closed (evidence-driven)
- [ ] MG-03 validated against simultaneous multicam dataset

---

## Test Count

| Suite | Tests | Status |
|-------|-------|--------|
| Phase 0 core | 49 | ✅ Passing |
| Stage 0.5 Archive Intelligence | 21 | ✅ Passing |
| Phase 1-C Config Profile System | 11 | ✅ Passing |
| **Total** | **81** | ✅ **81/81** |

---

*Last updated: 2026-05-27*
*Next update: after Phase 1-D completion*
