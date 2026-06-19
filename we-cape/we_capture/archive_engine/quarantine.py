"""W.E. C.A.P.E. CAPTURE — Quarantine Handler (Stage 0.5)"""
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class QuarantineRecord:
    original_path: Path
    quarantine_path: Path
    reason: str
    status: str
    details: str
    preserved: bool

class Quarantine:
    def __init__(self, config: dict, output_root: Path):
        qdir = config.get('archive_engine', {}).get('quarantine', {}).get('quarantine_dir', 'QUARANTINE')
        self.quarantine_dir = output_root / qdir
        # Lazy mkdir — not created until first quarantine() call

    def quarantine(self, path: Path, reason: str,
                   status: str, details: str = '') -> QuarantineRecord:
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        dest = self._safe_dest(path)
        shutil.copy2(str(path), dest)
        return QuarantineRecord(
            original_path=path, quarantine_path=dest,
            reason=reason, status=status, details=details, preserved=True,
        )

    def _safe_dest(self, path: Path) -> Path:
        dest = self.quarantine_dir / path.name
        if not dest.exists():
            return dest
        stem, suffix = path.stem, path.suffix
        i = 1
        while True:
            candidate = self.quarantine_dir / f'{stem}_{i}{suffix}'
            if not candidate.exists():
                return candidate
            i += 1
