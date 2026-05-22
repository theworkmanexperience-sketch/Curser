"""
W.E. FLOW / W.E. FORGE — Pipeline Orchestrator v4.1 ENHANCED
§§2–4: System Flow + System Locks

Stages (sequential, deterministic):
  0. Ingest       — Discover + hash all files (parallel, §14 up to 50GB each)
  1. Classify     — Camera | Camera-Audio | Generic | Reference (§6)
  2. Timestamp    — Extract via §5 fallback chain; flag low-confidence
  3. Group        — Multicam grouping, camera + camera_audio eligible (§7)
  4. Variants     — Parent-child detection, orphan → standalone (§8, §3.x)
  5. Output       — Write locked directory structure (§10)
  6. Audit        — Flush all five mandatory log streams (§12)

§3 Locks enforced:
  - Deterministic logic at every decision point
  - ALL files ingested, none dropped
  - No AI, no scene detection, no UI
  - Zero manual preprocessing
  - Idempotency: re-runs detect existing output files and skip (§17 Test 6)
"""

import uuid
import time
import traceback
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

from .classifier import FileClassifier, ClassifiedFile
from .timestamp import TimestampExtractor
from .grouper import MulticamGrouper, GroupingResult
from .variants import VariantDetector, VariantGroup
from .output import OutputBuilder
from .audit import AuditLogger


SKIP_NAMES = {'.DS_Store', 'Thumbs.db', 'desktop.ini', '.gitkeep', '.gitignore'}
SKIP_PREFIXES = {'.', '~'}


class Pipeline:

    def __init__(self, config_path: Path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        prefix = self.config.get('pipeline', {}).get('run_id_prefix', 'WEF')
        self.run_id = (
            f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
            f"_{uuid.uuid4().hex[:6].upper()}"
        )
        offsets = self.config.get('grouping', {}).get('camera_offsets', {})
        self.max_workers: int = self.config.get('performance', {}).get('max_workers', 8)
        self.hash_chunk_mb: int = self.config.get('performance', {}).get('hash_chunk_size_mb', 64)

        self.classifier = FileClassifier(self.config)
        self.ts_extractor = TimestampExtractor(camera_offsets=offsets)
        self.grouper = MulticamGrouper(self.config)
        self.variant_detector = VariantDetector(self.config)

    def _preflight_check(self, input_path: Path, output_path: Path) -> None:
        import shutil
        file_op = self.config.get('pipeline', {}).get('file_operation', 'copy')
        output_path.mkdir(parents=True, exist_ok=True)
        free_bytes = shutil.disk_usage(output_path).free
        free_gb = free_bytes / (1024 ** 3)
        if file_op == 'copy':
            try:
                input_size = sum(f.stat().st_size for f in input_path.rglob('*') if f.is_file())
                input_gb = input_size / (1024 ** 3)
                if free_gb < input_gb * 1.1:
                    raise RuntimeError(
                        f"Pre-flight FAILED: file_operation=copy needs ~{input_gb:.1f} GB free "
                        f"on output drive, only {free_gb:.1f} GB available. "
                        f"Use file_operation=symlink or point --output to a drive with more space."
                    )
            except OSError:
                pass
        if free_gb < 5.0:
            raise RuntimeError(
                f"Pre-flight FAILED: output drive has only {free_gb:.1f} GB free — minimum 5 GB required."
            )

    def run(self, input_path: Path, output_path: Path) -> dict:
        self._preflight_check(input_path, output_path)
        start = time.time()
        output_path.mkdir(parents=True, exist_ok=True)
        logs_dir = output_path / 'LOGS'

        logger = AuditLogger(
            run_id=self.run_id,
            log_dir=logs_dir,
            log_format=self.config.get('logging', {}).get('log_format', 'json'),
        )
        output_builder = OutputBuilder(self.config, output_path)
        all_classified: list[ClassifiedFile] = []
        errors: list[str] = []
        written: dict = {}

        try:
            # ── Stage 0: INGEST ──────────────────────────────────────────
            print(f"\n[{self.run_id}] Stage 0: Ingest — {input_path}")
            raw_files = self._discover_files(input_path)
            print(f"  → {len(raw_files):,} files discovered")

            # Parallel hash + ingest log
            def _ingest_file(fp: Path) -> Optional[ClassifiedFile]:
                try:
                    size = fp.stat().st_size
                    sha = self.classifier.compute_hash(fp, self.hash_chunk_mb)
                    logger.log_ingest(fp, file_size=size, file_hash=sha)
                    return None
                except Exception as e:
                    logger.log_error(fp, 'ingest_error', str(e), recoverable=True)
                    errors.append(f"Ingest: {fp.name}: {e}")
                    return None

            with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                list(ex.map(_ingest_file, raw_files))

            # ── Stage 1: CLASSIFY ────────────────────────────────────────
            print(f"[{self.run_id}] Stage 1: Classification")

            def _classify(fp: Path) -> Optional[ClassifiedFile]:
                try:
                    return self.classifier.classify(fp)
                except Exception as e:
                    logger.log_error(fp, 'classification_error', str(e), recoverable=True)
                    errors.append(f"Classify: {fp.name}: {e}")
                    return None

            with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                results = list(ex.map(_classify, raw_files))

            all_classified = [r for r in results if r is not None]
            cam = sum(1 for f in all_classified if f.is_camera)
            gen = sum(1 for f in all_classified if f.is_generic)
            ref = sum(1 for f in all_classified if f.is_reference)
            print(f"  → {cam} camera | {gen} generic | {ref} reference")

            # ── Stage 2: TIMESTAMP ───────────────────────────────────────
            print(f"[{self.run_id}] Stage 2: Timestamp extraction")
            low_confidence_count = 0

            def _stamp(f: ClassifiedFile) -> ClassifiedFile:
                nonlocal low_confidence_count
                try:
                    r = self.ts_extractor.extract(f.path, f.camera_source)
                    f.timestamp = r.unix_timestamp
                    f.timestamp_method = r.method
                    f.timestamp_fallback_level = r.fallback_level
                    f.timestamp_confidence = r.confidence
                    if r.fallback_level > 0:
                        logger.log_fallback(f.path, 'higher_priority', r.method,
                                            f"fallback_level={r.fallback_level}")
                    if r.confidence == 'low':
                        low_confidence_count += 1
                    logger.log_classification(
                        file_path=f.path,
                        classification=f.classification,
                        camera_source=f.camera_source,
                        method=f.detection_method,
                        timestamp_used=f.timestamp,
                        timestamp_fallback_level=f.timestamp_fallback_level,
                        timestamp_confidence=f.timestamp_confidence,
                    )
                except Exception as e:
                    logger.log_error(f.path, 'timestamp_error', str(e), recoverable=True)
                    f.timestamp = 0.0
                    f.timestamp_confidence = 'low'
                    errors.append(f"Timestamp: {f.path.name}: {e}")
                return f

            with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                all_classified = list(ex.map(_stamp, all_classified))

            if low_confidence_count:
                print(f"  ⚠  WARNING: {low_confidence_count} files resolved via file-system clock "
                      f"(timestamp_confidence=low). Multicam grouping accuracy may be degraded.")
                logger.log_error(None, 'low_confidence_timestamps',
                                 f"{low_confidence_count} files at fallback_level=2",
                                 recoverable=True)

            # ── Stage 3: MULTICAM GROUPING ───────────────────────────────
            print(f"[{self.run_id}] Stage 3: Multicam grouping")
            camera_files = [f for f in all_classified if f.is_camera]
            grouping_result: GroupingResult = self.grouper.group(camera_files)

            for group in grouping_result.groups:
                logger.log_grouping(
                    group_id=group.group_id,
                    files=[f.path for f in group.files],
                    anchor_timestamp=group.anchor_timestamp,
                    timestamp_deltas=group.timestamp_deltas,
                    conflict_resolved=group.conflict_resolved,
                    conflict_note=group.conflict_note,
                )
            for f in grouping_result.ungrouped:
                logger.log_ungrouped(f.path, grouping_result.ungrouped_reasons.get(f.path.name, ''))

            print(f"  → {len(grouping_result.groups)} groups | "
                  f"{len(grouping_result.ungrouped)} ungrouped camera files")

            # ── Stage 4: VARIANT DETECTION ───────────────────────────────
            print(f"[{self.run_id}] Stage 4: Variant detection")
            variant_groups, standalone = self.variant_detector.detect(all_classified)

            for vg in variant_groups:
                for child in vg.children:
                    logger.log_variant(vg.parent.path, child.path,
                                       vg.parent_selection_method, 'stem_base_match')

            # Log orphan variants (classification_note set by detector)
            orphans = [f for f in standalone if f.classification_note == 'variant_pattern_no_base_found']
            for f in orphans:
                logger.log_error(f.path, 'orphan_variant',
                                 'variant_pattern_no_base_found — reclassified as standalone',
                                 recoverable=True)

            print(f"  → {len(variant_groups)} variant groups | "
                  f"{len(orphans)} orphan variants (standalone)")

            # ── Stage 5: OUTPUT ──────────────────────────────────────────
            print(f"[{self.run_id}] Stage 5: Writing output → {output_path}")
            written = output_builder.build(
                run_id=self.run_id,
                all_files=all_classified,
                grouping_result=grouping_result,
                variant_groups=variant_groups,
                standalone_files=standalone,
            )

        except Exception as e:
            logger.log_error(None, 'pipeline_fatal', str(e), recoverable=False, exception=e)
            errors.append(f"FATAL: {e}")
            print(f"\n[FATAL] {e}\n{traceback.format_exc()}")

        finally:
            # ── Stage 6: AUDIT FLUSH (always runs) ──────────────────────
            print(f"[{self.run_id}] Stage 6: Flushing audit logs")
            log_paths = logger.flush()
            summary = logger.summary()
            summary.update({
                'run_id': self.run_id,
                'elapsed_seconds': round(time.time() - start, 2),
                'pipeline_errors': errors,
                'log_files': {k: str(v) for k, v in log_paths.items()},
            })
            report = output_path / 'LOGS' / f'{self.run_id}_summary.md'
            self._write_report(report, summary)

            elapsed = summary.get('elapsed_seconds', 0)
            ingested = summary.get('files_ingested', 0)
            throughput = (ingested / elapsed * 3600) if elapsed > 0 else 0
            print(f"\n✓ {self.run_id} complete in {elapsed}s")
            print(f"  Files: {ingested:,} | Groups: {summary.get('multicam_groups_formed', 0)} | "
                  f"Variants: {summary.get('variants_detected', 0)} | "
                  f"Errors: {summary.get('errors', 0)}")
            print(f"  Report: {report}\n")

        return summary

    # ------------------------------------------------------------------ #
    # File discovery                                                       #
    # ------------------------------------------------------------------ #

    def _discover_files(self, input_path: Path) -> list[Path]:
        if input_path.is_file():
            return [input_path]
        files = []
        for item in sorted(input_path.rglob('*')):
            if not item.is_file():
                continue
            if item.name in SKIP_NAMES:
                continue
            if any(item.name.startswith(p) for p in SKIP_PREFIXES):
                continue
            files.append(item)
        return files

    # ------------------------------------------------------------------ #
    # Human-readable run summary (§18)                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _write_report(path: Path, s: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# W.E. FLOW Run Summary", "",
            f"**Run ID:** `{s.get('run_id')}`  ",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}  ",
            f"**Elapsed:** {s.get('elapsed_seconds', 0)}s  ", "",
            "## Totals", "",
            "| Metric | Value |", "|--------|-------|",
            f"| Files ingested | {s.get('files_ingested', 0):,} |",
            f"| Multicam groups | {s.get('multicam_groups_formed', 0)} |",
            f"| Ungrouped camera files | {s.get('ungrouped_camera_files', 0)} |",
            f"| Variant groups | {s.get('variants_detected', 0)} |",
            f"| Errors | {s.get('errors', 0)} |",
            f"| Fallbacks | {s.get('fallbacks', 0)} |", "",
            "## Errors", "",
        ]
        errs = s.get('pipeline_errors', [])
        lines += [f"- {e}" for e in errs] if errs else ["_None._"]
        lines += ["", "## Log Files", ""]
        for name, p in s.get('log_files', {}).items():
            lines.append(f"- **{name}:** `{p}`")
        path.write_text('\n'.join(lines))
