"""W.E. FLOW — Archive Extractor (Stage 0.5)
Deterministic isolated extraction. Originals never deleted.
"""

import gzip
import tarfile
import zipfile
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ExtractionResult:
    source_path: Path
    extraction_dir: Path
    extracted_files: list
    failed_entries: list
    total_bytes_written: int
    nested_archives: list
    depth: int
    success: bool
    error_message: Optional[str]
    warnings: list = field(default_factory=list)


class ArchiveExtractor:

    def __init__(self, config: dict):
        ae = config.get('archive_engine', {})
        ext_cfg = ae.get('extraction', {})
        self.max_depth: int = ext_cfg.get('max_nesting_depth', 3)
        self.overwrite: bool = ext_cfg.get('overwrite_existing', False)

    def extract(self, archive_path: Path, output_root: Path,
                detected_type: str, depth: int = 0) -> ExtractionResult:
        if depth >= self.max_depth:
            return ExtractionResult(
                source_path=archive_path, extraction_dir=output_root,
                extracted_files=[], failed_entries=[],
                total_bytes_written=0, nested_archives=[],
                depth=depth, success=False,
                error_message=f'Max nesting depth ({self.max_depth}) exceeded',
            )
        extract_dir = self._isolated_dir(output_root, archive_path.stem)
        try:
            if detected_type == 'zip':
                return self._extract_zip(archive_path, extract_dir, depth)
            elif detected_type == 'tar.gz':
                return self._extract_tar_generic(archive_path, extract_dir, depth, 'r:gz')
            elif detected_type == 'tar':
                return self._extract_tar_generic(archive_path, extract_dir, depth, 'r:*')
            elif detected_type == 'gz':
                return self._extract_gz(archive_path, extract_dir, depth)
            else:
                return ExtractionResult(
                    source_path=archive_path, extraction_dir=extract_dir,
                    extracted_files=[], failed_entries=[],
                    total_bytes_written=0, nested_archives=[],
                    depth=depth, success=False,
                    error_message=f'No extractor for type: {detected_type}',
                )
        except Exception as e:
            return ExtractionResult(
                source_path=archive_path, extraction_dir=extract_dir,
                extracted_files=[], failed_entries=[],
                total_bytes_written=0, nested_archives=[],
                depth=depth, success=False, error_message=str(e),
            )

    def _extract_zip(self, src: Path, dest: Path, depth: int) -> ExtractionResult:
        extracted, failed, nested = [], [], []
        total_bytes = 0
        warnings = []
        with zipfile.ZipFile(str(src), 'r') as zf:
            for info in zf.infolist():
                safe_name = self._safe_member_name(info.filename)
                if safe_name is None:
                    warnings.append(f'Rejected unsafe path: {info.filename!r}')
                    failed.append(info.filename)
                    continue
                # Filter macOS resource forks (__MACOSX/ and ._* files)
                if (safe_name.startswith('__MACOSX/') or
                        '/__MACOSX/' in safe_name or
                        Path(safe_name).name.startswith('._')):
                    continue
                target = dest / safe_name
                target.parent.mkdir(parents=True, exist_ok=True)
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target = self._safe_dest(target)
                try:
                    with zf.open(info) as src_f, open(target, 'wb') as dst_f:
                        shutil.copyfileobj(src_f, dst_f)
                    total_bytes += target.stat().st_size
                    extracted.append(target)
                    if self._is_archive(target):
                        nested.append(target)
                except Exception as e:
                    failed.append(info.filename)
                    warnings.append(f'Failed {info.filename!r}: {e}')
        return ExtractionResult(
            source_path=src, extraction_dir=dest,
            extracted_files=extracted, failed_entries=failed,
            total_bytes_written=total_bytes, nested_archives=nested,
            depth=depth, success=len(extracted) > 0,
            error_message=None if not failed else f'{len(failed)} entries failed',
            warnings=warnings,
        )

    def _extract_tar_generic(self, src: Path, dest: Path,
                              depth: int, mode: str) -> ExtractionResult:
        extracted, failed, nested = [], [], []
        total_bytes = 0
        warnings = []
        try:
            with tarfile.open(str(src), mode) as tf:
                for member in tf.getmembers():
                    safe_name = self._safe_member_name(member.name)
                    if safe_name is None:
                        warnings.append(f'Rejected unsafe path: {member.name!r}')
                        failed.append(member.name)
                        continue
                    if member.isdir():
                        (dest / safe_name).mkdir(parents=True, exist_ok=True)
                        continue
                    if not member.isfile():
                        continue
                    target = self._safe_dest(dest / safe_name)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        f = tf.extractfile(member)
                        if f is None:
                            continue
                        with open(target, 'wb') as out:
                            shutil.copyfileobj(f, out)
                        total_bytes += target.stat().st_size
                        extracted.append(target)
                        if self._is_archive(target):
                            nested.append(target)
                    except Exception as e:
                        failed.append(member.name)
                        warnings.append(f'Failed {member.name!r}: {e}')
        except tarfile.TarError as e:
            return ExtractionResult(
                source_path=src, extraction_dir=dest,
                extracted_files=extracted, failed_entries=failed,
                total_bytes_written=total_bytes, nested_archives=nested,
                depth=depth, success=len(extracted) > 0,
                error_message=str(e), warnings=warnings,
            )
        return ExtractionResult(
            source_path=src, extraction_dir=dest,
            extracted_files=extracted, failed_entries=failed,
            total_bytes_written=total_bytes, nested_archives=nested,
            depth=depth, success=len(extracted) > 0,
            error_message=None if not failed else f'{len(failed)} members failed',
            warnings=warnings,
        )

    def _extract_gz(self, src: Path, dest: Path, depth: int) -> ExtractionResult:
        out_name = src.stem if src.stem else 'decompressed'
        target = self._safe_dest(dest / out_name)
        dest.mkdir(parents=True, exist_ok=True)
        try:
            with gzip.open(str(src), 'rb') as gz, open(target, 'wb') as out:
                shutil.copyfileobj(gz, out)
            total_bytes = target.stat().st_size
            nested = [target] if self._is_archive(target) else []
            return ExtractionResult(
                source_path=src, extraction_dir=dest,
                extracted_files=[target], failed_entries=[],
                total_bytes_written=total_bytes, nested_archives=nested,
                depth=depth, success=True, error_message=None,
            )
        except Exception as e:
            return ExtractionResult(
                source_path=src, extraction_dir=dest,
                extracted_files=[], failed_entries=[src.name],
                total_bytes_written=0, nested_archives=[],
                depth=depth, success=False, error_message=str(e),
            )

    def _isolated_dir(self, root: Path, stem: str) -> Path:
        safe_stem = ''.join(c if c.isalnum() or c in '-_.' else '_' for c in stem)[:64]
        candidate = root / safe_stem
        if not candidate.exists():
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
        i = 1
        while True:
            candidate = root / f'{safe_stem}_{i}'
            if not candidate.exists():
                candidate.mkdir(parents=True, exist_ok=True)
                return candidate
            i += 1

    def _safe_dest(self, path: Path) -> Path:
        if not path.exists():
            return path
        stem, suffix = path.stem, path.suffix
        i = 1
        while True:
            candidate = path.parent / f'{stem}_{i}{suffix}'
            if not candidate.exists():
                return candidate
            i += 1

    @staticmethod
    def _safe_member_name(name: str) -> Optional[str]:
        parts = name.replace('\\', '/').split('/')
        safe_parts = []
        for part in parts:
            if part in ('', '.'):
                continue
            if part == '..':
                return None
            if part.startswith('/'):
                return None
            safe_parts.append(part)
        if not safe_parts:
            return None
        return '/'.join(safe_parts)

    @staticmethod
    def _is_archive(path: Path) -> bool:
        ARCHIVE_EXTS = {'.zip','.gz','.tar','.tgz','.bz2','.xz','.7z','.rar'}
        ext = path.suffix.lower()
        name = path.name.lower()
        for compound in ('.tar.gz', '.tar.bz2', '.tar.xz'):
            if name.endswith(compound):
                return True
        return ext in ARCHIVE_EXTS
