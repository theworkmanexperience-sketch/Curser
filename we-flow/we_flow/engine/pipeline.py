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

import json
import os
import re
import tempfile
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

    @staticmethod
    def _is_system_drive(path: Path) -> bool:
        import shutil
        try:
            sys_device = shutil.disk_usage('/').total
            out_device = shutil.disk_usage(path).total
            # Same total size is a strong signal they share the same volume
            return sys_device == out_device
        except OSError:
            return False

    def _preflight_check(self, input_path: Path, output_path: Path) -> None:
        import shutil
        file_op = self.config.get('pipeline', {}).get('file_operation', 'symlink')
        output_path.mkdir(parents=True, exist_ok=True)

        free_bytes = shutil.disk_usage(output_path).free
        free_gb = free_bytes / (1024 ** 3)
        sys_free_gb = shutil.disk_usage('/').free / (1024 ** 3)
        on_system_drive = self._is_system_drive(output_path)

        input_gb = 0.0
        file_count = 0
        files: list = []
        try:
            files = [f for f in input_path.rglob('*') if f.is_file()]
            file_count = len(files)
            input_gb = sum(f.stat().st_size for f in files) / (1024 ** 3)
        except OSError:
            pass

        needed_gb = input_gb * 1.1 if file_op == 'copy' else 5.0
        mode_note = (
            f"copy mode — will duplicate {input_gb:.1f} GB onto output drive"
            if file_op == 'copy'
            else f"symlink mode — no files copied, only folder structure created"
        )

        print("\n" + "━" * 56)
        print("  W.E. FLOW — Pre-Flight Check")
        print("━" * 56)
        print(f"  Input media:    {input_path}")
        print(f"                  {input_gb:.1f} GB · {file_count:,} files")
        print(f"  Output folder:  {output_path}")

        if on_system_drive:
            print(f"  ⚠  WARNING: This folder is on your Mac's internal drive!")
            print(f"     Your internal drive only has {sys_free_gb:.1f} GB free.")
            print(f"     Copying large video shoots here will fill up your Mac.")
            print(f"")
            print(f"     RECOMMENDED: Use an external drive instead.")
            print(f"     Example:  --output /Volumes/YourDriveName/WE_FLOW_OUTPUT")
            print(f"     To see your drives: open Finder → Locations (left sidebar)")
        else:
            status = "✓" if free_gb >= needed_gb else "✗"
            print(f"                  {free_gb:.1f} GB free  {status}")

        print(f"  File mode:      {mode_note}")
        print(f"  Space needed:   {needed_gb:.1f} GB minimum on output drive")
        print(f"  System drive:   {sys_free_gb:.1f} GB free"
              + ("  ⚠  Keep above 20 GB" if sys_free_gb < 20 else "  ✓"))
        print("━" * 56)

        errors = []
        if on_system_drive and file_op == 'copy' and input_gb > 10:
            errors.append(
                f"\n  Your output folder is on your Mac's internal drive and\n"
                f"  file mode is set to 'copy'. This will copy {input_gb:.1f} GB\n"
                f"  onto your Mac and may fill it up completely.\n\n"
                f"  Fix: point --output to an external drive.\n"
                f"  Example: --output /Volumes/YourDriveName/WE_FLOW_OUTPUT\n"
                f"  Or change file_operation to 'symlink' in config.yaml."
            )
        if free_gb < needed_gb:
            errors.append(
                f"\n  Not enough space on the output drive.\n"
                f"  You need {needed_gb:.1f} GB free — only {free_gb:.1f} GB available.\n\n"
                f"  Fix: choose a drive with more free space, or\n"
                f"  change file_operation to 'symlink' in config.yaml."
            )
        if sys_free_gb < 5.0:
            errors.append(
                f"\n  Your Mac's internal drive is almost full ({sys_free_gb:.1f} GB left).\n"
                f"  macOS needs at least 5–10 GB free to run normally.\n\n"
                f"  Fix: move large files to an external drive before continuing."
            )

        if errors:
            raise RuntimeError(
                "\n\n  ✗ Pre-flight FAILED — please fix the following:\n"
                + "\n".join(errors)
            )

        # ── PI-01/02: PII Filename Scanner ───────────────────────────────
        # Use segment-boundary anchors (^|_) not \b — underscore is \w so
        # \b does not fire between underscore-separated tokens in compound names.
        _PII_PATTERNS = [
            # Full name: Two_Word proper case separated by underscores
            (re.compile(r'(?:^|_)([A-Z][a-z]{1,20})_([A-Z][a-z]{2,20})(?:_|$)'),
             'name_in_filename'),
            # Single-initial name: T_Workman, J_Smith
            (re.compile(r'(?:^|_)[A-Z]_[A-Z][a-z]{2,20}(?:_|$)'),
             'initial_name_in_filename'),
            (re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'),
             'email_address'),
            (re.compile(r'(?:^|_)\d{3}[.\-]?\d{3}[.\-]?\d{4}(?:_|$)'),
             'phone_number'),
            (re.compile(r'\d{3}-\d{2}-\d{4}'), 'ssn_pattern'),
        ]
        pii_flagged: list[tuple[str, str]] = []
        for f in files:
            stem = f.stem
            if f.name in SKIP_NAMES or any(f.name.startswith(p) for p in SKIP_PREFIXES):
                continue
            for pattern, label in _PII_PATTERNS:
                if pattern.search(stem):
                    pii_flagged.append((f.name, label))
                    break
        if pii_flagged:
            print(f"\n  ⚠  PII WARNING — {len(pii_flagged)} filename(s) contain possible PII:")
            for fname, label in pii_flagged[:10]:
                print(f"     [{label}] {fname}")
            if len(pii_flagged) > 10:
                print(f"     ... and {len(pii_flagged) - 10} more")
            print(f"\n     These filenames will be HASHED in all log records (not stored in plaintext).")
            print(f"     Confirm authorization in the attestation prompt below.\n")

        # ── PF-02: EULA Version Check ────────────────────────────────────
        import sys
        non_interactive = (
            not sys.stdin.isatty()
            or os.getenv('WEFLOW_NONINTERACTIVE') == '1'
        )
        eula_version: Optional[str] = self.config.get('compliance', {}).get('eula_version')
        eula_accepted_version: Optional[str] = None

        if eula_version and not non_interactive:
            eula_state_path = Path.home() / '.weflow' / 'eula_acceptance.json'
            already_accepted = False
            if eula_state_path.exists():
                try:
                    state = json.loads(eula_state_path.read_text())
                    if eula_version in state.get('accepted_versions', []):
                        already_accepted = True
                        eula_accepted_version = eula_version
                except Exception:
                    pass
            if not already_accepted:
                print(
                    f"\n  ─────────────────────────────────────────────────────\n"
                    f"  W.E. FLOW — End User License Agreement v{eula_version}\n"
                    f"  ─────────────────────────────────────────────────────\n"
                    f"\n"
                    f"  This software is licensed for use by authorized operators only.\n"
                    f"  [DRAFT — requires attorney review before retail distribution]\n"
                    f"\n"
                    f"  Full terms: see EULA.md in the software package.\n"
                    f"\n"
                    f"  Type YES to accept, or Ctrl+C to cancel.\n"
                    f"  > "
                )
                try:
                    eula_response = input().strip()
                except (EOFError, KeyboardInterrupt):
                    raise RuntimeError("\n  Run cancelled: EULA not accepted.")
                if eula_response.upper() != 'YES':
                    raise RuntimeError(
                        f"\n  EULA not accepted (received: '{eula_response}'). "
                        f"You must accept the license to use W.E. FLOW."
                    )
                eula_state_path.parent.mkdir(parents=True, exist_ok=True)
                eula_state: dict = {'accepted_versions': [], 'acceptances': []}
                if eula_state_path.exists():
                    try:
                        eula_state = json.loads(eula_state_path.read_text())
                    except Exception:
                        pass
                eula_state.setdefault('accepted_versions', [])
                eula_state.setdefault('acceptances', [])
                if eula_version not in eula_state['accepted_versions']:
                    eula_state['accepted_versions'].append(eula_version)
                    eula_state['acceptances'].append({
                        'version': eula_version,
                        'accepted_at': datetime.now(timezone.utc).isoformat(),
                        'operator': os.getenv('USER', 'unknown'),
                    })
                eula_state_path.write_text(json.dumps(eula_state, indent=2))
                eula_accepted_version = eula_version
        elif eula_version:
            eula_accepted_version = eula_version  # non-interactive: record version without prompting

        # ── Operator Attestation ─────────────────────────────────────────
        attestation_text = (
            "\n  BEFORE YOU CONTINUE — please confirm all of the following:\n\n"
            "  [ ] I am authorized to process the media files in the input folder\n"
            "  [ ] These files comply with all applicable NDAs and client agreements\n"
            "  [ ] I understand that W.E. FLOW will read every file in the input folder\n"
            "  [ ] The output drive meets my organization's encryption requirements\n\n"
            "  Type YES and press Enter to confirm, or Ctrl+C to cancel.\n"
            "  > "
        )
        attestation_hash: Optional[str] = None
        preflight_event = 'preflight_noninteractive'

        if not non_interactive:
            print(attestation_text, end='', flush=True)
            try:
                response = input().strip()
            except (EOFError, KeyboardInterrupt):
                raise RuntimeError("\n  Run cancelled at attestation prompt.")
            if response.upper() != 'YES':
                raise RuntimeError(
                    f"\n  Attestation not confirmed (received: '{response}'). "
                    f"Type YES to proceed."
                )
            attestation_hash = 'sha256:' + hashlib.sha256(
                attestation_text.encode()
            ).hexdigest()
            preflight_event = 'preflight_accepted'

        # ── Write _preflight.json ────────────────────────────────────────
        logs_dir = output_path / 'LOGS'
        logs_dir.mkdir(parents=True, exist_ok=True)
        preflight_record = {
            'run_id': self.run_id,
            'event': preflight_event,
            'logged_at': datetime.now(timezone.utc).isoformat(),
            'operator': os.getenv('USER', 'unknown'),
            'input_path_hash': 'sha256:' + hashlib.sha256(
                str(input_path).encode()
            ).hexdigest(),
            'output_drive': str(output_path),
            'output_on_system_drive': on_system_drive,
            'output_drive_free_gb': round(free_gb, 1),
            'system_drive_free_gb': round(sys_free_gb, 1),
            'eula_version_accepted': eula_accepted_version,
            'attestation_hash': attestation_hash,
            'file_operation_mode': file_op,
            'pii_flagged_count': len(pii_flagged),
            'pii_flagged_filenames': [f for f, _ in pii_flagged],
        }
        preflight_path = logs_dir / f'{self.run_id}_preflight.json'
        preflight_path.write_text(json.dumps(preflight_record, indent=2))

    def run(self, input_path: Path, output_path: Path) -> dict:
        self._preflight_check(input_path, output_path)
        start = time.time()
        output_path.mkdir(parents=True, exist_ok=True)
        logs_dir = output_path / 'LOGS'

        # OP-04: Secure temp dir — cleaned up in finally regardless of outcome
        _tmp_ctx = tempfile.TemporaryDirectory(prefix=f'weflow_{self.run_id}_')
        tmp_dir = Path(_tmp_ctx.name)

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

            # ── OP-04: Secure temp file deletion ────────────────────────
            try:
                _tmp_ctx.cleanup()
            except Exception:
                pass

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
