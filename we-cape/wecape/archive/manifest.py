"""W.E. C.A.P.E. CAPTURE — Archive Checksum & Manifest (Stage 0.5)"""

import hashlib
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def compute_sha256(path: Path, chunk_size_mb: int = 64) -> str:
    sha256 = hashlib.sha256()
    chunk = chunk_size_mb * 1024 * 1024
    try:
        with open(path, 'rb') as f:
            while True:
                data = f.read(chunk)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except (OSError, IOError):
        return ''


@dataclass
class ArchiveManifestEntry:
    run_id: str
    archive_original: str
    archive_original_name: str
    archive_claimed_extension: str
    archive_detected_type: Optional[str]
    archive_extension_mismatch: bool
    archive_detection_method: str
    archive_detection_confidence: str
    archive_validation_status: str
    archive_repaired: bool
    archive_repair_notes: list
    archive_checksum_sha256: str
    archive_extract_path: Optional[str]
    archive_extracted_file_count: int
    archive_extracted_bytes: int
    archive_nested_depth: int
    archive_quarantined: bool
    archive_quarantine_path: Optional[str]
    archive_quarantine_reason: Optional[str]
    archive_is_partial_download: bool
    archive_is_recursive_container: bool
    archive_is_phase1_format: bool
    archive_errors: list
    archive_warnings: list
    processed_at: str


class ArchiveManifest:
    def __init__(self, run_id: str, logs_dir: Path):
        self.run_id = run_id
        self.logs_dir = logs_dir
        self._entries: list = []

    def add(self, entry: ArchiveManifestEntry):
        self._entries.append(entry)

    def flush(self) -> Path:
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        path = self.logs_dir / f'{self.run_id}_archive.json'
        doc = {
            'run_id': self.run_id,
            'log_type': 'archive',
            'entry_count': len(self._entries),
            'entries': [asdict(e) for e in self._entries],
        }
        path.write_text(json.dumps(doc, indent=2, default=str))
        return path

    def summary(self) -> dict:
        return {
            'archives_detected': len(self._entries),
            'archives_extracted': sum(1 for e in self._entries if e.archive_extracted_file_count > 0),
            'archives_quarantined': sum(1 for e in self._entries if e.archive_quarantined),
            'archives_repaired': sum(1 for e in self._entries if e.archive_repaired),
            'partial_downloads_detected': sum(1 for e in self._entries if e.archive_is_partial_download),
            'recursive_containers_detected': sum(1 for e in self._entries if e.archive_is_recursive_container),
            'phase1_formats_detected': sum(1 for e in self._entries if e.archive_is_phase1_format),
        }

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()
