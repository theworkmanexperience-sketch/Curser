# W.E. FLOW / W.E. FORGE — Phase 1 Planning
**Phase 0 Status:** ✅ COMPLETE & GREEN (commit 940cb62)  
**Date:** 2026-05-25

## Phase 1 Goals
Activate advanced capabilities on top of the locked deterministic Phase 0 core while maintaining zero breaking changes.

### Core Pillars of Phase 1
1. **Archive Intelligence Activation** (Stage 0.5)
2. **DJI / Insta360 Telemetry Parser** (GPS + accurate creation_time)
3. **Config / Profile-Based Workflows**
4. **Performance Optimization & Scaling**
5. **Enhanced Logging & Observability**

## Prioritized Features & Tasks

### 1. Archive Intelligence Activation (Highest Priority)
- Enable `archive_engine.enabled: true` via feature flag
- Integrate Stage 0.5 into main pipeline (magic-byte detection, repair, quarantine)
- Add new output folders: `QUARANTINE/`, `ARCHIVE_EXTRACTED/`
- Update acceptance tests to include archive scenarios
- Add config validation for Phase 1 formats (.7z, .rar, etc.)

### 2. DJI / Insta360 Telemetry Parser (PI-04)
- Parse proprietary CAM meta binary stream via ffprobe + custom parser
- Extract GPS coordinates, accurate creation_time, camera model
- Update timestamp fallback chain to prefer telemetry data
- Add GPS redaction option in logs for privacy compliance

### 3. Config / Profile-Based Workflows
- Support multiple named profiles in `config.yaml` (e.g. "novice", "pro", "studio")
- Add `--profile` CLI flag
- Dynamic workflow selection (symlink vs copy vs move, proxy settings, etc.)
- Profile inheritance and overrides

### 4. Performance Optimization
- Parallel processing (configurable `max_workers`)
- Checkpointing / resumable runs
- Memory usage optimization for large shoots (>500 GB)
- Benchmark targets:
  - Studio tier: ≥ 80 GB/hr on Apple Silicon
  - Pro tier: ≥ 120 GB/hr

### 5. Enhanced Logging & Idempotency
- Structured observability (Prometheus metrics scaffold)
- Detailed performance telemetry per stage
- Stronger idempotency guarantees with checkpoint files

## Implementation Order (Recommended)
1. Archive activation (quick win, already built)
2. DJI telemetry parser + GPS handling
3. Config profile system
4. Performance & parallelism
5. Enhanced logging & observability

## Acceptance Criteria for Phase 1
- All new features behind feature flags (zero impact on Phase 0)
- 100% backward compatibility with v4.1 Phase 0 behavior
- New tests covering archive scenarios and DJI files
- Updated compliance delta showing PI-04 and MG-03 closed

**Next Immediate Step:**  
Activate Archive Intelligence safely (toggle the feature flag and run regression tests).

Would you like me to generate the commands for **Step 1 (Archive Activation)** right now?
