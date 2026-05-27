"""W.E. FLOW — Archive Validator (Stage 0.5)"""

import gzip
import zipfile
import tarfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .detector import DetectionResult


@dataclass
class ValidationResult:
    path: Path
    detected_type: Optional[str]
    status: str
    is_extractable: bool
    is_encrypted: bool
    total_uncompressed_bytes: int
    entry_count: int
    bad_entries: list
    warnings: list
    error_message: Optional[str]


class ArchiveValidator:

    def __init__(self, config: dict):
        ae = config.get('archive_engine', {})
        limits = ae.get('size_limits', {})
        self.max_single_gb: float = limits.get('max_single_file_extracted_gb', 10.0)
        self.max_total_gb: float = limits.get('max_total_extracted_gb', 50.0)

    def validate(self, detection: DetectionResult) -> ValidationResult:
        t = detection.detected_type
        path = detection.path
        if t == 'zip':
            return self._validate_zip(path)
        elif t in ('gz', 'tar.gz'):
            return self._validate_gz(path, t)
        elif t == 'tar':
            return self._validate_tar(path)
        else:
            return ValidationResult(
                path=path, detected_type=t, status='UNKNOWN',
                is_extractable=False, is_encrypted=False,
                total_uncompressed_bytes=0, entry_count=0,
                bad_entries=[], warnings=[f'No validator for: {t}'],
                error_message=f'Unsupported type: {t}',
            )

    def _validate_zip(self, path: Path) -> ValidationResult:
        warnings, bad_entries = [], []
        total_bytes, entry_count = 0, 0
        is_encrypted = False
        try:
            with zipfile.ZipFile(str(path), 'r') as zf:
                bad = zf.testzip()
                infos = zf.infolist()
                entry_count = len(infos)
                for info in infos:
                    total_bytes += info.file_size
                    if info.flag_bits & 0x1:
                        is_encrypted = True
                    if info.file_size > self.max_single_gb * 1024**3:
                        warnings.append(f'{info.filename!r} exceeds {self.max_single_gb}GB')
                if bad:
                    bad_entries.append(bad)
        except zipfile.BadZipFile as e:
            return ValidationResult(path=path, detected_type='zip', status='CORRUPTED',
                is_extractable=False, is_encrypted=False,
                total_uncompressed_bytes=0, entry_count=0,
                bad_entries=[], warnings=[], error_message=str(e))
        except Exception as e:
            return ValidationResult(path=path, detected_type='zip', status='CORRUPTED',
                is_extractable=False, is_encrypted=False,
                total_uncompressed_bytes=0, entry_count=0,
                bad_entries=[], warnings=[], error_message=str(e))
        if is_encrypted:
            return ValidationResult(path=path, detected_type='zip', status='ENCRYPTED',
                is_extractable=False, is_encrypted=True,
                total_uncompressed_bytes=total_bytes, entry_count=entry_count,
                bad_entries=[], warnings=warnings, error_message=None)
        if total_bytes > self.max_total_gb * 1024**3:
            warnings.append(f'Total {total_bytes/1024**3:.1f}GB exceeds {self.max_total_gb}GB limit')
            return ValidationResult(path=path, detected_type='zip', status='OVERSIZED',
                is_extractable=False, is_encrypted=False,
                total_uncompressed_bytes=total_bytes, entry_count=entry_count,
                bad_entries=bad_entries, warnings=warnings, error_message=None)
        if bad_entries:
            return ValidationResult(path=path, detected_type='zip', status='PARTIAL',
                is_extractable=True, is_encrypted=False,
                total_uncompressed_bytes=total_bytes, entry_count=entry_count,
                bad_entries=bad_entries, warnings=warnings, error_message=None)
        return ValidationResult(path=path, detected_type='zip', status='COMPLETE',
            is_extractable=True, is_encrypted=False,
            total_uncompressed_bytes=total_bytes, entry_count=entry_count,
            bad_entries=[], warnings=warnings, error_message=None)

    def _validate_gz(self, path: Path, detected_type: str) -> ValidationResult:
        try:
            with gzip.open(str(path), 'rb') as gz:
                total_bytes = 0
                while True:
                    data = gz.read(65536)
                    if not data:
                        break
                    total_bytes += len(data)
                    if total_bytes > self.max_total_gb * 1024**3:
                        return ValidationResult(
                            path=path, detected_type=detected_type, status='OVERSIZED',
                            is_extractable=False, is_encrypted=False,
                            total_uncompressed_bytes=total_bytes, entry_count=0,
                            bad_entries=[], warnings=[f'Exceeds {self.max_total_gb}GB'],
                            error_message=None)
        except (gzip.BadGzipFile, OSError, EOFError) as e:
            return ValidationResult(path=path, detected_type=detected_type, status='CORRUPTED',
                is_extractable=False, is_encrypted=False,
                total_uncompressed_bytes=0, entry_count=0,
                bad_entries=[], warnings=[], error_message=str(e))
        return ValidationResult(path=path, detected_type=detected_type, status='COMPLETE',
            is_extractable=True, is_encrypted=False,
            total_uncompressed_bytes=total_bytes, entry_count=1,
            bad_entries=[], warnings=[], error_message=None)

    def _validate_tar(self, path: Path) -> ValidationResult:
        total_bytes, entry_count = 0, 0
        warnings = []
        try:
            with tarfile.open(str(path), 'r:*') as tf:
                for member in tf.getmembers():
                    entry_count += 1
                    total_bytes += member.size
                    if member.size > self.max_single_gb * 1024**3:
                        warnings.append(f'{member.name!r} exceeds {self.max_single_gb}GB')
        except tarfile.TarError as e:
            return ValidationResult(path=path, detected_type='tar', status='CORRUPTED',
                is_extractable=False, is_encrypted=False,
                total_uncompressed_bytes=0, entry_count=0,
                bad_entries=[], warnings=[], error_message=str(e))
        if total_bytes > self.max_total_gb * 1024**3:
            warnings.append(f'Total exceeds {self.max_total_gb}GB')
            return ValidationResult(path=path, detected_type='tar', status='OVERSIZED',
                is_extractable=False, is_encrypted=False,
                total_uncompressed_bytes=total_bytes, entry_count=entry_count,
                bad_entries=[], warnings=warnings, error_message=None)
        return ValidationResult(path=path, detected_type='tar', status='COMPLETE',
            is_extractable=True, is_encrypted=False,
            total_uncompressed_bytes=total_bytes, entry_count=entry_count,
            bad_entries=[], warnings=warnings, error_message=None)
