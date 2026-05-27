"""W.E. FLOW — Archive Detector (Stage 0.5)
Magic byte detection — never trusts file extensions.
"""

import io
import gzip
import zipfile
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

MAGIC_SIGNATURES = [
    (0,   b'PK\x03\x04',          'zip',    'ZIP archive (standard)'),
    (0,   b'PK\x05\x06',          'zip',    'ZIP archive (empty)'),
    (0,   b'PK\x07\x08',          'zip',    'ZIP archive (spanned)'),
    (0,   b'\x1f\x8b',            'gz',     'GNU gzip compressed'),
    (0,   b'BZh',                  'bz2',    'bzip2 compressed'),
    (0,   b'\xfd7zXZ\x00',         'xz',     'XZ compressed'),
    (0,   b'7z\xbc\xaf\x27\x1c',  '7z',     '7-Zip archive'),
    (0,   b'Rar!\x1a\x07\x00',    'rar',    'RAR archive v1.5+'),
    (0,   b'Rar!\x1a\x07\x01\x00','rar',    'RAR archive v5.0+'),
    (257, b'ustar\x00',           'tar',    'POSIX tar archive'),
    (257, b'ustar  \x00',         'tar',    'GNU tar archive'),
]

PARTIAL_DOWNLOAD_MARKERS = {
    '.crdownload', '.part', '.download', '.tmp', '.partial', '.aria2', '.!ut',
}

PHASE1_FORMATS = {'7z', 'rar', 'bz2', 'xz'}

ARCHIVE_EXTENSIONS = {
    '.zip', '.gz', '.tar', '.tgz', '.bz2', '.xz', '.7z', '.rar',
    '.tar.gz', '.tar.bz2', '.tar.xz', '.cpgz',
    '.z01', '.z02', '.001', '.002',
}

RECURSIVE_CONTAINER_EXTENSIONS = {'.cpgz'}


@dataclass
class DetectionResult:
    path: Path
    extension_claimed: str
    detected_type: Optional[str]
    is_archive: bool
    is_partial_download: bool
    is_recursive_container: bool
    is_phase1_format: bool
    extension_mismatch: bool
    detection_method: str
    confidence: str
    description: str
    suggested_extension: Optional[str]


class ArchiveDetector:

    def detect(self, file_path: Path) -> DetectionResult:
        ext = file_path.suffix.lower()
        stem_ext = self._compound_extension(file_path)

        # Handle Chrome duplicate naming: "file.crdownload 2", "file.crdownload 3"
        import re as _re
        clean_ext = _re.sub(r'\s+\d+$', '', ext)
        if (ext in PARTIAL_DOWNLOAD_MARKERS or
                clean_ext in PARTIAL_DOWNLOAD_MARKERS or
                any(str(file_path).lower().endswith(m)
                    for m in PARTIAL_DOWNLOAD_MARKERS)):
            return DetectionResult(
                path=file_path, extension_claimed=ext, detected_type=None,
                is_archive=False, is_partial_download=True,
                is_recursive_container=False, is_phase1_format=False,
                extension_mismatch=False, detection_method='extension_marker',
                confidence='high', description='Partial / incomplete download',
                suggested_extension=None,
            )

        if ext in RECURSIVE_CONTAINER_EXTENSIONS:
            return DetectionResult(
                path=file_path, extension_claimed=ext, detected_type='cpgz',
                is_archive=True, is_partial_download=False,
                is_recursive_container=True, is_phase1_format=False,
                extension_mismatch=False, detection_method='extension_marker',
                confidence='high', description='macOS recursive container (.cpgz loop risk)',
                suggested_extension=None,
            )

        is_claimed_archive = (ext in ARCHIVE_EXTENSIONS or stem_ext in ARCHIVE_EXTENSIONS)
        detected_type, method, description, confidence = self._detect_by_magic(file_path)

        if detected_type is None and not is_claimed_archive:
            return DetectionResult(
                path=file_path, extension_claimed=ext, detected_type=None,
                is_archive=False, is_partial_download=False,
                is_recursive_container=False, is_phase1_format=False,
                extension_mismatch=False, detection_method='none',
                confidence='high', description='Not an archive',
                suggested_extension=None,
            )

        claimed_type = self._type_from_extension(stem_ext or ext)
        mismatch = (detected_type is not None and
                    claimed_type is not None and
                    detected_type != claimed_type)
        is_phase1 = detected_type in PHASE1_FORMATS if detected_type else False
        is_archive = detected_type is not None or is_claimed_archive
        suggested = self._extension_for_type(detected_type) if mismatch else None

        return DetectionResult(
            path=file_path, extension_claimed=ext, detected_type=detected_type,
            is_archive=is_archive, is_partial_download=False,
            is_recursive_container=False, is_phase1_format=is_phase1,
            extension_mismatch=mismatch, detection_method=method,
            confidence=confidence, description=description or f'Archive: {detected_type}',
            suggested_extension=suggested,
        )

    def _detect_by_magic(self, path: Path) -> tuple:
        try:
            with open(path, 'rb') as f:
                header = f.read(512)
            for offset, magic, dtype, desc in MAGIC_SIGNATURES:
                if len(header) > offset and header[offset:offset + len(magic)] == magic:
                    if dtype == 'tar' and not self._is_valid_tar(path):
                        continue
                    if dtype == 'gz':
                        if self._gz_contains_tar(path):
                            return 'tar.gz', 'magic_bytes', 'GZ-compressed TAR', 'high'
                    return dtype, 'magic_bytes', desc, 'high'
            return self._structural_probe(path)
        except (OSError, PermissionError):
            return None, 'none', 'File unreadable', 'low'

    def _structural_probe(self, path: Path) -> tuple:
        try:
            if zipfile.is_zipfile(str(path)):
                return 'zip', 'structural_probe', 'ZIP (structural probe)', 'medium'
        except Exception:
            pass
        try:
            if tarfile.is_tarfile(str(path)):
                return 'tar', 'structural_probe', 'TAR (structural probe)', 'medium'
        except Exception:
            pass
        return None, 'none', 'Not a recognized archive', 'low'

    def _is_valid_tar(self, path: Path) -> bool:
        try:
            return tarfile.is_tarfile(str(path))
        except Exception:
            return False

    def _gz_contains_tar(self, path: Path) -> bool:
        try:
            with gzip.open(path, 'rb') as gz:
                sample = gz.read(512)
            if len(sample) >= 265 and sample[257:262] in (b'ustar', b'ustar'):
                return True
            try:
                with tarfile.open(fileobj=io.BytesIO(sample)):
                    return True
            except Exception:
                pass
        except Exception:
            pass
        return False

    @staticmethod
    def _compound_extension(path: Path) -> str:
        name = path.name.lower()
        for compound in ('.tar.gz', '.tar.bz2', '.tar.xz'):
            if name.endswith(compound):
                return compound
        return path.suffix.lower()

    @staticmethod
    def _type_from_extension(ext: str) -> Optional[str]:
        return {'.zip':'zip','.gz':'gz','.tar':'tar','.tar.gz':'tar.gz',
                '.tgz':'tar.gz','.bz2':'bz2','.xz':'xz','.7z':'7z','.rar':'rar'}.get(ext)

    @staticmethod
    def _extension_for_type(detected: Optional[str]) -> Optional[str]:
        return {
            'zip':'.zip','gz':'.gz','tar':'.tar','tar.gz':'.tar.gz',
            'bz2':'.bz2','xz':'.xz','7z':'.7z','rar':'.rar',
        }.get(detected or '')
