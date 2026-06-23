"""W.E. C.A.P.E. CAPTURE — Stage 0.5: Archive & Compression Intelligence
Normalization gate, integrity gate, and forensic recovery gate.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .detector import ArchiveDetector, DetectionResult, PHASE1_FORMATS
from .validator import ArchiveValidator, ValidationResult
from .extractor import ArchiveExtractor, ExtractionResult
from .repair import ArchiveRepair, RepairResult
from .quarantine import Quarantine, QuarantineRecord
from .manifest import ArchiveManifest, ArchiveManifestEntry, compute_sha256


@dataclass
class Stage05Result:
    files_scanned: int
    archives_detected: int
    files_extracted: list
    files_quarantined: list
    partial_downloads: list
    recursive_containers: list
    phase1_formats: list
    errors: list
    manifest_path: Optional[Path]
    archive_summary: dict


class ArchiveIntelligenceStage:

    def __init__(self, config: dict, output_root: Path):
        self.config = config
        self.output_root = output_root
        ae_cfg = config.get('archive_engine', {})
        self.enabled: bool = ae_cfg.get('enabled', False)
        self.attempt_repair: bool = ae_cfg.get('repair', {}).get('attempt_repair', True)
        self.supported_formats: set = set(ae_cfg.get('supported_formats', [
            '.zip', '.gz', '.tar', '.tar.gz', '.tgz'
        ]))
        self.detector  = ArchiveDetector()
        self.validator = ArchiveValidator(config)
        self.extractor = ArchiveExtractor(config)
        self.repair    = ArchiveRepair()
        self.quarantine_handler = Quarantine(config, output_root)
        self.staging_dir = output_root / 'ARCHIVE_EXTRACTED'

    def process(self, raw_files: list, run_id: str,
                logs_dir: Path) -> tuple:
        # Stage 0.5 Archive Intelligence is Phase 1 gated.
        # Disabled by default to preserve locked v4.1 retail determinism.
        # When disabled: returns input list unchanged, zero side effects.
        if not self.enabled:
            return raw_files, Stage05Result(
                files_scanned=len(raw_files), archives_detected=0,
                files_extracted=[], files_quarantined=[],
                partial_downloads=[], recursive_containers=[],
                phase1_formats=[], errors=[],
                manifest_path=None, archive_summary={},
            )

        manifest = ArchiveManifest(run_id, logs_dir)
        result = Stage05Result(
            files_scanned=len(raw_files), archives_detected=0,
            files_extracted=[], files_quarantined=[],
            partial_downloads=[], recursive_containers=[],
            phase1_formats=[], errors=[],
            manifest_path=None, archive_summary={},
        )

        final_files: list = []

        for file_path in raw_files:
            try:
                detection = self.detector.detect(file_path)

                if not detection.is_archive and not detection.is_partial_download:
                    final_files.append(file_path)
                    continue

                result.archives_detected += 1
                entry = self._process_single(file_path, detection, manifest, result)
                manifest.add(entry)
                final_files.append(file_path)

            except Exception as e:
                result.errors.append(f'Stage 0.5 error on {file_path.name}: {e}')
                final_files.append(file_path)

        final_files.extend(result.files_extracted)
        result.manifest_path = manifest.flush()
        result.archive_summary = manifest.summary()

        return final_files, result

    def _process_single(self, path: Path, detection: DetectionResult,
                        manifest: ArchiveManifest,
                        result: Stage05Result) -> ArchiveManifestEntry:
        sha256 = compute_sha256(path)

        if detection.is_partial_download:
            result.partial_downloads.append(path)
            q = self.quarantine_handler.quarantine(
                path, reason='PARTIAL_DOWNLOAD', status='PARTIAL_DOWNLOAD',
                details='Incomplete browser or network download')
            result.files_quarantined.append(path)
            return self._make_entry(path, detection, None, None, None, q, sha256, manifest)

        if detection.is_recursive_container:
            result.recursive_containers.append(path)
            q = self.quarantine_handler.quarantine(
                path, reason='RECURSIVE_CONTAINER', status='RECURSIVE_CONTAINER',
                details='macOS .cpgz recursive extraction loop halted')
            result.files_quarantined.append(path)
            return self._make_entry(path, detection, None, None, None, q, sha256, manifest)

        if detection.is_phase1_format:
            result.phase1_formats.append(path)
            q = self.quarantine_handler.quarantine(
                path, reason='PHASE1_FORMAT', status='PHASE1_FORMAT',
                details=f'Format {detection.detected_type!r} requires Phase 1 tooling')
            result.files_quarantined.append(path)
            return self._make_entry(path, detection, None, None, None, q, sha256, manifest)

        detected_type = detection.detected_type
        fmt_ext = f'.{detected_type}' if detected_type else detection.extension_claimed
        if detected_type == 'tar.gz':
            fmt_ext = '.tar.gz'

        if detected_type not in ('zip', 'gz', 'tar', 'tar.gz') and fmt_ext not in self.supported_formats:
            q = self.quarantine_handler.quarantine(
                path, reason='UNSUPPORTED_FORMAT', status='UNSUPPORTED',
                details=f'Format {fmt_ext!r} not in Phase 0 supported formats')
            result.files_quarantined.append(path)
            return self._make_entry(path, detection, None, None, None, q, sha256, manifest)

        validation = self.validator.validate(detection)

        if validation.status == 'ENCRYPTED':
            q = self.quarantine_handler.quarantine(
                path, reason='ENCRYPTED', status='ENCRYPTED',
                details='Password-protected archive — zero-UI pipeline; quarantined')
            result.files_quarantined.append(path)
            return self._make_entry(path, detection, validation, None, None, q, sha256, manifest)

        if validation.status == 'OVERSIZED':
            q = self.quarantine_handler.quarantine(
                path, reason='OVERSIZED', status='OVERSIZED',
                details='; '.join(validation.warnings))
            result.files_quarantined.append(path)
            return self._make_entry(path, detection, validation, None, None, q, sha256, manifest)

        repair_result = None
        if validation.status == 'CORRUPTED':
            if self.attempt_repair:
                repair_dir = self.staging_dir / f'REPAIR_{path.stem}'
                repair_result = self.repair.attempt_repair(path, detected_type, repair_dir)
                if repair_result.repair_succeeded:
                    result.files_extracted.extend(repair_result.recovered_files)
                    return self._make_entry(path, detection, validation, repair_result,
                                            None, None, sha256, manifest,
                                            extracted_files=repair_result.recovered_files,
                                            extract_path=repair_dir)
                else:
                    q = self.quarantine_handler.quarantine(
                        path, reason='CORRUPTED', status='CORRUPTED',
                        details=f'Repair failed: {repair_result.error_message}')
                    result.files_quarantined.append(path)
                    return self._make_entry(path, detection, validation, repair_result,
                                            None, q, sha256, manifest)
            else:
                q = self.quarantine_handler.quarantine(
                    path, reason='CORRUPTED', status='CORRUPTED',
                    details='Corrupt; repair disabled in config')
                result.files_quarantined.append(path)
                return self._make_entry(path, detection, validation, None, None, q, sha256, manifest)

        if validation.is_extractable and detected_type:
            extract_dir = self.staging_dir / path.stem
            extraction = self.extractor.extract(path, extract_dir, detected_type, depth=0)
            if extraction.success and extraction.extracted_files:
                # Post-extraction scan: quarantine nested partial downloads
                # Extracted files bypass Stage 0.5 entry — check them here
                clean_extracted = []
                for xf in extraction.extracted_files:
                    try:
                        xd = self.detector.detect(xf)
                        if xd.is_partial_download:
                            self.quarantine_handler.quarantine(
                                xf,
                                reason='PARTIAL_DOWNLOAD_EXTRACTED',
                                status='PARTIAL_DOWNLOAD',
                                details=f'Partial download found inside archive {path.name}')
                            result.files_quarantined.append(xf)
                        else:
                            clean_extracted.append(xf)
                    except Exception:
                        clean_extracted.append(xf)
                result.files_extracted.extend(clean_extracted)
                return self._make_entry(path, detection, validation, repair_result,
                                        extraction, None, sha256, manifest,
                                        extracted_files=clean_extracted,
                                        extract_path=extraction.extraction_dir)
            else:
                q = self.quarantine_handler.quarantine(
                    path, reason='EXTRACTION_FAILED', status=validation.status,
                    details=extraction.error_message or 'Extraction produced no files')
                result.files_quarantined.append(path)
                return self._make_entry(path, detection, validation, repair_result,
                                        extraction, q, sha256, manifest)

        q = self.quarantine_handler.quarantine(
            path, reason='UNKNOWN',
            status=validation.status if validation else 'UNKNOWN',
            details='Not extractable; no matching action')
        result.files_quarantined.append(path)
        return self._make_entry(path, detection, validation, None, None, q, sha256, manifest)

    def _make_entry(self, path, detection, validation, repair,
                    extraction, quarantine, sha256, manifest,
                    extracted_files=None, extract_path=None):
        errors, warnings = [], []
        if validation and validation.error_message:
            errors.append(f'Validation: {validation.error_message}')
        if repair and repair.error_message:
            errors.append(f'Repair: {repair.error_message}')
        if extraction and extraction.error_message:
            errors.append(f'Extraction: {extraction.error_message}')
        if extraction:
            warnings.extend(extraction.warnings)
        if validation:
            warnings.extend(validation.warnings)
        if repair:
            warnings.extend(repair.notes)

        extracted = extracted_files or (extraction.extracted_files if extraction else [])
        ext_bytes = extraction.total_bytes_written if extraction else 0
        ext_path = str(extract_path) if extract_path else (
            str(extraction.extraction_dir) if extraction else None)

        return ArchiveManifestEntry(
            run_id=manifest.run_id,
            archive_original=str(path),
            archive_original_name=path.name,
            archive_claimed_extension=detection.extension_claimed,
            archive_detected_type=detection.detected_type,
            archive_extension_mismatch=detection.extension_mismatch,
            archive_detection_method=detection.detection_method,
            archive_detection_confidence=detection.confidence,
            archive_validation_status=validation.status if validation else 'UNVALIDATED',
            archive_repaired=bool(repair and repair.repair_succeeded),
            archive_repair_notes=repair.notes if repair else [],
            archive_checksum_sha256=sha256,
            archive_extract_path=ext_path,
            archive_extracted_file_count=len(extracted),
            archive_extracted_bytes=ext_bytes,
            archive_nested_depth=extraction.depth if extraction else 0,
            archive_quarantined=quarantine is not None,
            archive_quarantine_path=str(quarantine.quarantine_path) if quarantine else None,
            archive_quarantine_reason=quarantine.reason if quarantine else None,
            archive_is_partial_download=detection.is_partial_download,
            archive_is_recursive_container=detection.is_recursive_container,
            archive_is_phase1_format=detection.is_phase1_format,
            archive_errors=errors,
            archive_warnings=warnings,
            processed_at=manifest.now(),
        )
