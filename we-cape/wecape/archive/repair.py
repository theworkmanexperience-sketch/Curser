"""W.E. C.A.P.E. CAPTURE — Archive Repair Engine (Stage 0.5)"""

import gzip
import tarfile
import zipfile
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class RepairResult:
    path: Path
    detected_type: Optional[str]
    repair_attempted: bool
    repair_succeeded: bool
    recovered_files: list
    unrecoverable_entries: list
    error_message: Optional[str]
    notes: list = field(default_factory=list)


class ArchiveRepair:

    def attempt_repair(self, path: Path, detected_type: Optional[str],
                       recovery_dir: Path) -> RepairResult:
        recovery_dir.mkdir(parents=True, exist_ok=True)
        if detected_type == 'zip':
            return self._repair_zip(path, recovery_dir)
        elif detected_type in ('tar', 'tar.gz'):
            return self._repair_tar(path, recovery_dir, detected_type)
        elif detected_type == 'gz':
            return self._repair_gz(path, recovery_dir)
        else:
            return RepairResult(
                path=path, detected_type=detected_type,
                repair_attempted=False, repair_succeeded=False,
                recovered_files=[], unrecoverable_entries=[],
                error_message=f'No repair strategy for type: {detected_type}',
                notes=['Repair not attempted'],
            )

    def _repair_zip(self, path: Path, dest: Path) -> RepairResult:
        recovered, unrecoverable = [], []
        notes = ['ZIP repair: entry-by-entry extraction with bad entry skip']
        try:
            with zipfile.ZipFile(str(path), 'r') as zf:
                for info in zf.infolist():
                    try:
                        target = dest / info.filename
                        target.parent.mkdir(parents=True, exist_ok=True)
                        if not info.is_dir():
                            with zf.open(info) as src, open(target, 'wb') as dst:
                                shutil.copyfileobj(src, dst)
                            recovered.append(target)
                    except Exception as e:
                        unrecoverable.append(f'{info.filename}: {e}')
        except Exception as e:
            return RepairResult(path=path, detected_type='zip',
                repair_attempted=True, repair_succeeded=len(recovered) > 0,
                recovered_files=recovered, unrecoverable_entries=unrecoverable,
                error_message=str(e), notes=notes)
        return RepairResult(path=path, detected_type='zip',
            repair_attempted=True, repair_succeeded=len(recovered) > 0,
            recovered_files=recovered, unrecoverable_entries=unrecoverable,
            error_message=None, notes=notes)

    def _repair_tar(self, path: Path, dest: Path, detected_type: str) -> RepairResult:
        recovered, unrecoverable = [], []
        mode = 'r:gz' if detected_type == 'tar.gz' else 'r:*'
        notes = ['TAR repair: member-by-member extraction, errorlevel=0']
        try:
            with tarfile.open(str(path), mode, errorlevel=0) as tf:
                for member in tf.getmembers():
                    if not member.isfile():
                        continue
                    try:
                        target = dest / member.name
                        target.parent.mkdir(parents=True, exist_ok=True)
                        f = tf.extractfile(member)
                        if f:
                            with open(target, 'wb') as out:
                                shutil.copyfileobj(f, out)
                            recovered.append(target)
                    except Exception as e:
                        unrecoverable.append(f'{member.name}: {e}')
        except Exception as e:
            return RepairResult(path=path, detected_type=detected_type,
                repair_attempted=True, repair_succeeded=len(recovered) > 0,
                recovered_files=recovered, unrecoverable_entries=unrecoverable,
                error_message=str(e), notes=notes)
        return RepairResult(path=path, detected_type=detected_type,
            repair_attempted=True, repair_succeeded=len(recovered) > 0,
            recovered_files=recovered, unrecoverable_entries=unrecoverable,
            error_message=None, notes=notes)

    def _repair_gz(self, path: Path, dest: Path) -> RepairResult:
        out_name = path.stem or 'recovered'
        target = dest / out_name
        notes = ['GZ repair: partial decompression to truncation point']
        recovered_bytes = 0
        try:
            with gzip.open(str(path), 'rb') as gz, open(target, 'wb') as out:
                while True:
                    try:
                        chunk = gz.read(65536)
                        if not chunk:
                            break
                        out.write(chunk)
                        recovered_bytes += len(chunk)
                    except (EOFError, gzip.BadGzipFile):
                        notes.append(f'Truncation after {recovered_bytes:,} bytes')
                        break
        except Exception as e:
            return RepairResult(path=path, detected_type='gz',
                repair_attempted=True, repair_succeeded=recovered_bytes > 0,
                recovered_files=[target] if recovered_bytes > 0 else [],
                unrecoverable_entries=[], error_message=str(e), notes=notes)
        return RepairResult(path=path, detected_type='gz',
            repair_attempted=True, repair_succeeded=recovered_bytes > 0,
            recovered_files=[target] if recovered_bytes > 0 else [],
            unrecoverable_entries=[], error_message=None, notes=notes)
