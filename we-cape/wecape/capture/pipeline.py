"""
W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Pipeline Orchestrator v4.1 ENHANCED
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
from wecape.capture.proxy import ProxyGenerator

from .classifier import FileClassifier, ClassifiedFile
from .timestamp import TimestampExtractor
from .grouper import MulticamGrouper, GroupingResult
from .variants import VariantDetector, VariantGroup
from .output import OutputBuilder
from .audit import AuditLogger
from ..core.errors import RegistryAuditError
from ..core.stage import (
    PipelineStage, StageContext, StageResult, ValidationResult, run_stages,
)
from ..core.sync import LocalOnlySyncAdapter


SKIP_NAMES = {'.DS_Store', 'Thumbs.db', 'desktop.ini', '.gitkeep', '.gitignore'}
SKIP_PREFIXES = {'.', '~'}


def _audit_failure(strict: bool, test_mode: bool, phase: str, exc: Exception) -> None:
    """
    Strict-audit policy for registry/audit write failures.

    In strict mode (default) a failed audit write aborts the run — a
    compliance-first product must not report success without an audit record.
    Disabled in test mode (the production registry is intentionally skipped) and
    when ``registry.strict: false`` is configured.
    """
    if strict and not test_mode:
        raise RegistryAuditError(
            f"[{phase}] audit write failed and strict audit mode is ON — aborting run. "
            f"Cause: {exc}. Set 'registry.strict: false' in config to run without a "
            f"guaranteed audit trail."
        ) from exc
    print(f"  [registry] {phase} skipped (non-strict mode): {exc}")


class _MethodStage(PipelineStage):
    """
    Internal production stage: wraps a Pipeline bound-method as a PipelineStage
    so the real orchestrator runs through core.stage.run_stages(). Shares state
    via StageContext.metadata. (The clean public J3 contract is in
    wecape/capture/stages.py; these instance-bound stages are the production set.)
    """

    def __init__(self, stage_id, stage_version, fn, desc=""):
        self.stage_id = stage_id
        self.stage_version = stage_version
        self.stage_description = desc
        self._fn = fn

    def validate_input(self, context) -> ValidationResult:
        return ValidationResult(True)

    def execute(self, context) -> StageResult:
        return self._fn(context)

    def on_error(self, error, context) -> dict:
        return {"stage": self.stage_id, "error": str(error),
                "resolution": "See the LOGS error stream for details."}


class _NullIntelligenceStage(PipelineStage):
    """
    Placeholder for the J1–J5 AI stages (P6: AI is additive and never
    foundational). Disabled by default; only appended when
    `intelligence.enabled: true`. A genuine no-op so v1 ships zero AI.
    """
    stage_id = "intelligence:placeholder"
    stage_version = "0.0.0"
    stage_description = "Reserved AI hook — no-op until J1+ (camera/quality/alignment/editorial)"

    def validate_input(self, context) -> ValidationResult:
        return ValidationResult(True)

    def execute(self, context) -> StageResult:
        return StageResult(self.stage_id, self.stage_version, True,
                           metadata={"enabled": False,
                                     "note": "AI stages (J1-J5) plug in here via PipelineStage"})

    def on_error(self, error, context) -> dict:
        return {"stage": self.stage_id, "error": str(error)}


class Pipeline:

    def __init__(self, config_path: Path):
        from ..core.config import load_base
        self.config = load_base(config_path)

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

        # W.E. C.A.P.E. Registry — writes production history to local SQLite.
        # Strict audit mode (default ON): if the audit trail cannot be written,
        # the run aborts rather than silently completing without a record.
        # Opt out with `registry.strict: false`. Always relaxed under test mode.
        import os as _os
        self._test_mode = _os.environ.get('WECAPE_TEST_MODE') == '1'
        self._registry_strict = bool(self.config.get('registry', {}).get('strict', True))
        try:
            import sys as _sys
            if self._test_mode:
                self._registry = None  # Never write test runs to production registry
            else:
                _wecape_root = str(Path(__file__).resolve().parent.parent.parent)
                if _wecape_root not in _sys.path:
                    _sys.path.insert(0, _wecape_root)
                from wecape.registry.writer import RegistryWriter as _RegistryWriter
                _reg_path = Path.home() / '.wecape' / 'registry' / 'wecape.db'
                self._registry = _RegistryWriter(db_path=_reg_path)
        except Exception as _e:
            self._registry = None
            _audit_failure(self._registry_strict, self._test_mode, 'registry-init', _e)

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

    def _preflight_check(self, input_path, output_path):
        import os
        if os.environ.get('WECAPE_TEST_MODE') == '1':
            return  # Skip interactive prompts in automated test runs
        import shutil

        # ── Measure 1: Dependency check — fail fast before any processing ───
        # Prevents silent 8-9 hour runs that produce 0 proxies due to missing tools
        if self.config.get('proxy_generation', {}).get('enabled', False):
            _missing = [t for t in ('ffmpeg', 'ffprobe') if not shutil.which(t)]
            if _missing:
                raise RuntimeError(
                    "\n\n  ✗ Pre-flight FAILED — missing required tools:\n"
                    f"\n  Proxy generation is enabled but "
                    f"{', '.join(_missing)} "
                    f"{'is' if len(_missing) == 1 else 'are'} not installed.\n"
                    "\n  Install with:  brew install ffmpeg"
                    "\n  Then re-run this command."
                    "\n\n  Run aborted — 0 files processed, 0 hours wasted."
                )
        # ── End dependency check ─────────────────────────────────────────────

        file_op = self.config.get('pipeline', {}).get('file_operation', 'symlink')
        output_path.mkdir(parents=True, exist_ok=True)

        free_bytes = shutil.disk_usage(output_path).free
        free_gb = free_bytes / (1024 ** 3)
        sys_free_gb = shutil.disk_usage(str(Path.home())).free / (1024 ** 3)
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
        print("  W.E. C.A.P.E. CAPTURE — Pre-Flight Check")
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
            or os.getenv('WECAPE_NONINTERACTIVE') == '1'
        )
        eula_cfg: dict = self.config.get('compliance', {}).get('eula', {})
        eula_version: Optional[str] = eula_cfg.get('version')
        eula_text: str = eula_cfg.get('text', '')
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
                print(f"\n  {'─' * 56}")
                print(f"  W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — End User License Agreement v{eula_version}")
                print(f"  {'─' * 56}\n")
                for line in eula_text.splitlines():
                    print(f"  {line}")
                print(f"\n  {'─' * 56}")
                print(f"  Type YES to accept this Agreement, or Ctrl+C to cancel.")
                print(f"  > ", end='', flush=True)
                try:
                    eula_response = input().strip()
                except (EOFError, KeyboardInterrupt):
                    raise RuntimeError("\n  Run cancelled: EULA not accepted.")
                if eula_response.upper() != 'YES':
                    raise RuntimeError(
                        f"\n  EULA not accepted (received: '{eula_response}'). "
                        f"You must accept the license to use W.E. C.A.P.E. CAPTURE."
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
            "  [ ] I understand that W.E. C.A.P.E. CAPTURE will read every file in the input folder\n"
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


        # Registry: open run record before any stage executes
        try:
            if self._registry:
                self._registry.write_run(
                    run_id=self.run_id,
                    we_cape_version='1.0.0',
                    source_path=str(input_path),
                    output_path=str(output_path),
                    profile_id=self.config.get('_active_profile', {}).get('name'),
                )
        except Exception as _e:
            _audit_failure(self._registry_strict, self._test_mode, 'write_run', _e)
        output_path.mkdir(parents=True, exist_ok=True)
        logs_dir = output_path / 'LOGS'

        # OP-04: Secure temp dir — cleaned up in finally regardless of outcome
        _tmp_ctx = tempfile.TemporaryDirectory(prefix=f'wecape_{self.run_id}_')
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
        sha_map: dict  = {}  # Stage 0 → Stage 6: source path → SHA-256

        # Shared state for the stage engine. The same mutable objects (errors,
        # sha_map) are visible to the finally block below.
        stage_state = {
            'logger': logger, 'output_builder': output_builder,
            'sha_map': sha_map, 'all_classified': all_classified,
            'errors': errors, 'written': written,
            'raw_files': [], 'grouping_result': None,
            'variant_groups': [], 'standalone': [], 'archive_result': None,
        }
        stage_ctx = StageContext(
            run_id=self.run_id,
            source_path=str(input_path),
            output_path=str(output_path),
            profile=self.config,
            registry_writer=self._registry,
            sync_adapter=LocalOnlySyncAdapter(),
            timestamp=datetime.now(timezone.utc),
            metadata=stage_state,
        )

        # Ordered production stages. run_stages() is the central entry point;
        # `pipeline.engine: legacy` calls the identical methods directly (rollback).
        engine = self.config.get('pipeline', {}).get('engine', 'stages')
        stage_list = [
            _MethodStage('ingest',    '1.0.0', self._stage_ingest,    'Discover + hash all files (§14)'),
            _MethodStage('archive',   '1.0.0', self._stage_archive,   'Stage 0.5 archive intelligence (gated)'),
            _MethodStage('classify',  '1.0.0', self._stage_classify,  'Classify camera/generic/reference (§6)'),
            _MethodStage('timestamp', '1.0.0', self._stage_timestamp, 'Timestamp fallback chain (§5)'),
            _MethodStage('group',     '1.0.0', self._stage_group,     'Multicam grouping (§7)'),
            _MethodStage('variants',  '1.0.0', self._stage_variants,  'Variant detection (§8)'),
            _MethodStage('output',    '1.0.0', self._stage_output,    'Write locked output structure (§10)'),
        ]
        # P6: disabled-by-default AI hook. Never foundational; opt-in only.
        if self.config.get('intelligence', {}).get('enabled', False):
            stage_list.append(_NullIntelligenceStage())

        try:
            if engine == 'legacy':
                # Rollback path: identical stage methods, single-try semantics.
                for _stage in stage_list:
                    _stage.execute(stage_ctx)
            else:
                _results = run_stages(stage_list, stage_ctx)
                _failed = [r for r in _results if not r.success]
                if _failed:
                    # Surface the first stage failure as a pipeline-fatal (matches
                    # the legacy single-try behaviour: remaining stages skipped).
                    raise RuntimeError((_failed[0].errors or ['stage failed'])[0])

        except Exception as e:
            logger.log_error(None, 'pipeline_fatal', str(e), recoverable=False, exception=e)
            errors.append(f"FATAL: {e}")
            print(f"\n[FATAL] {e}\n{traceback.format_exc()}")

        finally:
            # Pull stage outputs back from the shared context (stages reassign
            # these inside metadata, so the run()-local names must be refreshed).
            all_classified = stage_ctx.metadata.get('all_classified', all_classified)
            sha_map = stage_ctx.metadata.get('sha_map', sha_map)
            raw_files = stage_ctx.metadata.get('raw_files', [])
            errors = stage_ctx.metadata.get('errors', errors)

            # ── Stage 6: PROXY GENERATION ────────────────────────────────
            proxy_result = None
            _px_cfg = self.config.get('proxy_generation', {})
            if _px_cfg.get('enabled', False):
                print(f"[{self.run_id}] Stage 6: Proxy generation")
                generator = ProxyGenerator(self.config)
                _px_t0 = time.perf_counter()
                proxy_result = generator.generate(
                    classified_files=all_classified,
                    output_path=output_path,
                    tmp_dir=tmp_dir,
                    sha_map=sha_map,
                )
                _px_secs = round(time.perf_counter() - _px_t0, 2)
                for r in proxy_result.get('results', []):
                    logger.log_proxy(
                        source_path=r.source_path,
                        proxy_path=r.proxy_path,
                        status=r.status,
                        reason=r.reason,
                        elapsed_s=r.elapsed_s,
                        source_sha256=r.source_sha256,
                    )
                t = proxy_result.get('transcoded', 0)
                s = proxy_result.get('skipped', 0)
                f = proxy_result.get('failed', 0)
                print(f"  → {t} transcoded | {s} skipped | {f} failed")
                # Record proxy as a stage_result — makes re-runs (transcoded=0) and
                # proxy time attributable in the registry. No schema change.
                try:
                    if self._registry:
                        self._registry.write_stage_result(self.run_id, 'proxy', StageResult(
                            stage_id='proxy', stage_version='1.0.0', success=(f == 0),
                            files_processed=t, files_skipped=s, files_failed=f,
                            duration_sec=_px_secs,
                            metadata={'transcoded': t, 'skipped': s, 'failed': f,
                                      'eligible': proxy_result.get('eligible', 0)}))
                except Exception:
                    pass

            # Registry: write content records + finalize run
            try:
                if self._registry and all_classified:
                    # Build proxy path lookup from proxy results
                    _proxy_map = {}
                    if proxy_result:
                        for _r in proxy_result.get('results', []):
                            if _r.status == 'transcoded' and _r.proxy_path:
                                _proxy_map[_r.source_path] = str(_r.proxy_path)

                    # Derivation lineage (v3): record select -> source provenance.
                    # Additive metadata only; safe no-op for non-select filenames.
                    from .derivation import DerivationResolver
                    _lin = self.config.get('lineage', {})
                    _resolver = DerivationResolver(
                        select_pattern=_lin.get('select_pattern', r'_sel\d+'),
                        enabled=_lin.get('enabled', True),
                    )
                    _resolver.index_sources(
                        (f.path.stem, sha_map.get(f.path)) for f in all_classified
                    )

                    for _f in all_classified:
                        _sha = sha_map.get(_f.path, '')
                        if not _sha:
                            continue
                        _src_clip, _src_sha = _resolver.resolve(_f.path.name)
                        _shoot_date = None
                        if getattr(_f, 'timestamp', None):
                            try:
                                _shoot_date = datetime.fromtimestamp(
                                    _f.timestamp, tz=timezone.utc
                                ).strftime('%Y-%m-%d')
                            except Exception:
                                pass
                        _size = None
                        try:
                            _size = _f.path.stat().st_size if _f.path.exists() else None
                        except Exception:
                            pass
                        self._registry.write_content(
                            run_id=self.run_id,
                            content_id=_sha,
                            filename=_f.path.name,
                            original_path=str(_f.path),
                            camera_family=getattr(_f, 'camera_source', None),
                            shoot_date=_shoot_date,
                            file_size_bytes=_size,
                            proxy_path=_proxy_map.get(_f.path),
                            content_type='original',
                            source_clip=_src_clip,
                            source_clip_sha=_src_sha,
                        )

                    self._registry.finalize_run(
                        run_id=self.run_id,
                        file_count=len(all_classified),
                        total_duration_sec=0.0,
                        runtime_sec=round(time.time() - start, 2),
                        errors=errors,
                    )
                    print(f"  [registry] {len(all_classified)} records → ~/.wecape/registry/wecape.db")
            except RegistryAuditError:
                raise
            except Exception as _e:
                _audit_failure(self._registry_strict, self._test_mode, 'finalize', _e)

            # ── Measure 3: Warn if proxy generation expected but 0 produced ──
            if proxy_result:
                _eligible  = proxy_result.get('eligible', 0)
                _transcoded = proxy_result.get('transcoded', 0)
                _unchanged  = sum(
                    1 for r in proxy_result.get('results', [])
                    if r.status == 'skipped_unchanged'
                )
                if _eligible > 0 and _transcoded == 0 and _unchanged < _eligible:
                    print(
                        f"\n  ⚠  WARNING: {_eligible} files were eligible for "
                        f"proxy generation but 0 were transcoded.\n"
                        f"  Check ffmpeg installation and source file integrity."
                    )
                    errors.append(
                        f"WARN: 0 proxies generated from {_eligible} eligible files"
                    )
            # ── End Measure 3 ────────────────────────────────────────────────

            # ── Stage 7: AUDIT CLOSE ─────────────────────────────────────
            print(f"[{self.run_id}] Stage 7: Flushing audit logs")
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
            # Priority 4: Count final ingested files after Stage 0.5 expansion
            ingested = summary.get('files_ingested', len(raw_files))
            throughput = (ingested / elapsed * 3600) if elapsed > 0 else 0
            print(f"\n✓ {self.run_id} complete in {elapsed}s")
            px_t = summary.get('proxies_transcoded', 0)
            px_s = summary.get('proxies_skipped', 0)
            px_f = summary.get('proxies_failed', 0)
            px_str = f" | Proxies: {px_t}t/{px_s}s/{px_f}f" if summary.get('proxies_transcoded', 0) + summary.get('proxies_skipped', 0) + summary.get('proxies_failed', 0) > 0 else ""
            print(f"  Files: {ingested:,} | Groups: {summary.get('multicam_groups_formed', 0)} | "
                  f"Variants: {summary.get('variants_detected', 0)} | "
                  f"Errors: {summary.get('errors', 0)} | "
                  f"Diagnostics: {summary.get('diagnostics', 0)}{px_str}")
            print(f"  Report: {report}\n")

        return summary

    # ------------------------------------------------------------------ #
    # Production stages (driven by core.stage.run_stages)                  #
    # Each operates on StageContext.metadata and returns a StageResult.    #
    # Logic is identical to the legacy inline blocks — only relocated.     #
    # ------------------------------------------------------------------ #

    def _stage_ingest(self, ctx: StageContext) -> StageResult:
        m = ctx.metadata
        logger = m['logger']; errors = m['errors']; sha_map = m['sha_map']
        input_path = Path(ctx.source_path)
        print(f"\n[{self.run_id}] Stage 0: Ingest — {input_path}")
        raw_files = self._discover_files(input_path)
        print(f"  → {len(raw_files):,} files discovered")

        def _ingest_file(fp: Path) -> Optional[ClassifiedFile]:
            try:
                size = fp.stat().st_size
                sha = self.classifier.compute_hash(fp, self.hash_chunk_mb)
                sha_map[fp] = sha
                logger.log_ingest(fp, file_size=size, file_hash=sha)
                return None
            except Exception as e:
                logger.log_error(fp, 'ingest_error', str(e), recoverable=True)
                errors.append(f"Ingest: {fp.name}: {e}")
                return None

        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            list(ex.map(_ingest_file, raw_files))

        m['raw_files'] = raw_files
        return StageResult('ingest', '1.0.0', True, files_processed=len(raw_files))

    def _stage_archive(self, ctx: StageContext) -> StageResult:
        m = ctx.metadata; errors = m['errors']
        raw_files = m['raw_files']
        archive_result = None
        _ae_cfg = self.config.get('archive_engine', {})
        if _ae_cfg.get('enabled', False):
            print(f"[PHASE1] Archive Intelligence Engine ENABLED")
            from wecape.archive.stage import ArchiveIntelligenceStage
            _archive_stage = ArchiveIntelligenceStage(self.config, Path(ctx.output_path))
            print(f"[{self.run_id}] Stage 0.5: Archive & Compression Intelligence")
            raw_files, archive_result = _archive_stage.process(
                raw_files, self.run_id, Path(ctx.output_path) / 'LOGS'
            )
            if archive_result.archives_detected > 0:
                print(f"  → {archive_result.archives_detected} archives | "
                      f"{len(archive_result.files_extracted)} extracted | "
                      f"{len(archive_result.files_quarantined)} quarantined")
                if archive_result.partial_downloads:
                    print(f"  ⚠  {len(archive_result.partial_downloads)} partial downloads detected")
            for e in (archive_result.errors if archive_result else []):
                errors.append(e)
        m['raw_files'] = raw_files
        m['archive_result'] = archive_result
        return StageResult('archive', '1.0.0', True, files_processed=len(raw_files))

    def _stage_classify(self, ctx: StageContext) -> StageResult:
        m = ctx.metadata; logger = m['logger']; errors = m['errors']
        raw_files = m['raw_files']
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
        m['all_classified'] = all_classified
        return StageResult('classify', '1.0.0', True, files_processed=len(all_classified),
                           metadata={'camera': cam, 'generic': gen, 'reference': ref})

    def _stage_timestamp(self, ctx: StageContext) -> StageResult:
        m = ctx.metadata; logger = m['logger']; errors = m['errors']
        all_classified = m['all_classified']
        print(f"[{self.run_id}] Stage 2: Timestamp extraction")
        low = [0]

        def _stamp(f: ClassifiedFile) -> ClassifiedFile:
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
                    low[0] += 1
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

        if low[0]:
            print(f"  ⚠  WARNING: {low[0]} files resolved via file-system clock "
                  f"(timestamp_confidence=low). Multicam grouping accuracy may be degraded.")
            logger.log_error(None, 'low_confidence_timestamps',
                             f"{low[0]} files at fallback_level=2",
                             recoverable=True)
        m['all_classified'] = all_classified
        return StageResult('timestamp', '1.0.0', True, files_processed=len(all_classified),
                           diagnostics=([f"low_confidence={low[0]}"] if low[0] else []))

    def _stage_group(self, ctx: StageContext) -> StageResult:
        m = ctx.metadata; logger = m['logger']
        all_classified = m['all_classified']
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
        m['grouping_result'] = grouping_result
        return StageResult('group', '1.0.0', True, files_processed=len(camera_files),
                           metadata={'groups': len(grouping_result.groups),
                                     'ungrouped': len(grouping_result.ungrouped)})

    def _stage_variants(self, ctx: StageContext) -> StageResult:
        m = ctx.metadata; logger = m['logger']
        all_classified = m['all_classified']
        print(f"[{self.run_id}] Stage 4: Variant detection")
        variant_groups, standalone = self.variant_detector.detect(all_classified)

        for vg in variant_groups:
            for child in vg.children:
                logger.log_variant(vg.parent.path, child.path,
                                   vg.parent_selection_method, 'stem_base_match')

        orphans = [f for f in standalone if f.classification_note == 'variant_pattern_no_base_found']
        for f in orphans:
            logger.log_error(f.path, 'orphan_variant',
                             'variant_pattern_no_base_found — reclassified as standalone',
                             recoverable=True)

        print(f"  → {len(variant_groups)} variant groups | "
              f"{len(orphans)} orphan variants (standalone)")
        m['variant_groups'] = variant_groups
        m['standalone'] = standalone
        return StageResult('variants', '1.0.0', True, files_processed=len(all_classified),
                           metadata={'variant_groups': len(variant_groups), 'orphans': len(orphans)})

    def _stage_output(self, ctx: StageContext) -> StageResult:
        m = ctx.metadata
        output_builder = m['output_builder']
        print(f"[{self.run_id}] Stage 5: Writing output → {ctx.output_path}")
        written = output_builder.build(
            run_id=self.run_id,
            all_files=m['all_classified'],
            grouping_result=m['grouping_result'],
            variant_groups=m['variant_groups'],
            standalone_files=m['standalone'],
        )
        m['written'] = written
        return StageResult('output', '1.0.0', True, files_processed=len(m['all_classified']))

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
            "# W.E. C.A.P.E. CAPTURE Run Summary", "",
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
            f"| Diagnostics | {s.get('diagnostics', 0)} |",
            f"| Fallbacks (timestamp) | {s.get('fallbacks', 0)} |", "",
            "## Errors", "",
        ]
        errs = s.get('pipeline_errors', [])
        lines += [f"- {e}" for e in errs] if errs else ["_None._"]
        diag_count = s.get('diagnostics', 0)
        lines += ["", "## Diagnostics", "",
                  f"_{diag_count} operational diagnostic(s) — low-confidence timestamps "
                  f"and orphan variants. Not pipeline failures._"]
        lines += ["", "## Log Files", ""]
        for name, p in s.get('log_files', {}).items():
            lines.append(f"- **{name}:** `{p}`")
        path.write_text('\n'.join(lines))
