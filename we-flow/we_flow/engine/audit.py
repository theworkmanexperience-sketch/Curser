"""
W.E. FLOW / W.E. FORGE — Logging & Audit Engine
§12: Five mandatory log streams (LOCKED)

1. ingest_log        — all files received + SHA-256 hashes
2. classification_log — per-file classification decisions
3. grouping_log      — multicam grouping trace
4. variant_log       — parent-child linkage records
5. error_log         — errors, skips, fallbacks
"""

import hashlib
import json
import logging
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class AuditLogger:

    def __init__(self, run_id: str, log_dir: Path, log_format: str = 'json'):
        self.run_id = run_id
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._ingest: list[dict] = []
        self._classification: list[dict] = []
        self._grouping: list[dict] = []
        self._variants: list[dict] = []
        self._errors: list[dict] = []

        self._logger = logging.getLogger(f'weflow.{run_id}')
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(message)s'))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def log_ingest(self, file_path: Path, file_size: int, file_hash: Optional[str] = None):
        entry = self._base(file_path)
        entry.update({'event': 'ingest', 'file_size_bytes': file_size,
                      'file_hash_sha256': file_hash})
        self._ingest.append(entry)

    def log_classification(self, file_path: Path, classification: str,
                           camera_source: Optional[str], method: str,
                           timestamp_used: Optional[float],
                           timestamp_fallback_level: int,
                           timestamp_confidence: str = 'high'):
        entry = self._base(file_path)
        entry.update({
            'event': 'classification',
            'classification': classification,
            'camera_source': camera_source,
            'detection_method': method,
            'timestamp_unix': timestamp_used,
            'timestamp_fallback_level': timestamp_fallback_level,
            'timestamp_confidence': timestamp_confidence,
        })
        self._classification.append(entry)

    def log_grouping(self, group_id: str, files: list[Path],
                     anchor_timestamp: float, timestamp_deltas: dict,
                     conflict_resolved: bool = False,
                     conflict_note: Optional[str] = None):
        entry = {
            'run_id': self.run_id, 'event': 'grouping',
            'logged_at': self._now(), 'group_id': group_id,
            'file_count': len(files),
            'filenames': [f.name for f in files],
            'file_path_hashes': [self._path_hash(f) for f in files],
            'anchor_timestamp_unix': anchor_timestamp,
            'timestamp_deltas_seconds': timestamp_deltas,
            'conflict_resolved': conflict_resolved,
            'conflict_note': conflict_note,
        }
        self._grouping.append(entry)

    def log_ungrouped(self, file_path: Path, reason: str):
        entry = self._base(file_path)
        entry.update({'event': 'ungrouped_camera', 'reason': reason})
        self._grouping.append(entry)
        self._logger.warning(f'[UNGROUPED] {file_path.name}: {reason}')

    def log_variant(self, parent_path: Path, child_path: Path,
                    detection_method: str, match_pattern: str):
        self._variants.append({
            'run_id': self.run_id, 'event': 'variant_link',
            'logged_at': self._now(),
            'parent_filename': parent_path.name,
            'parent_path_hash': self._path_hash(parent_path),
            'child_filename': child_path.name,
            'child_path_hash': self._path_hash(child_path),
            'detection_method': detection_method, 'match_pattern': match_pattern,
        })

    def log_error(self, file_path: Optional[Path], error_type: str,
                  message: str, recoverable: bool = True,
                  exception: Optional[Exception] = None):
        entry = {
            'run_id': self.run_id, 'event': 'error',
            'logged_at': self._now(),
            'filename': file_path.name if file_path else None,
            'file_path_hash': self._path_hash(file_path) if file_path else None,
            'error_type': error_type, 'message': message,
            'recoverable': recoverable,
            'traceback': traceback.format_exc() if exception else None,
        }
        self._errors.append(entry)
        level = self._logger.warning if recoverable else self._logger.error
        level(f"[{'SKIP' if recoverable else 'ERROR'}] {error_type}: {message}")

    def log_fallback(self, file_path: Path, from_method: str,
                     to_method: str, reason: str):
        self.log_error(
            file_path=file_path, error_type='fallback',
            message=f"Timestamp: '{from_method}' → '{to_method}': {reason}",
            recoverable=True,
        )

    def flush(self) -> dict[str, Path]:
        written = {}
        streams = {
            'ingest': self._ingest,
            'classification': self._classification,
            'grouping': self._grouping,
            'variants': self._variants,
            'errors': self._errors,
        }
        for name, entries in streams.items():
            path = self.log_dir / f'{self.run_id}_{name}.json'
            path.write_text(json.dumps(
                {'run_id': self.run_id, 'log_type': name, 'entries': entries},
                indent=2, default=str,
            ))
            written[name] = path

        manifest = {
            'run_id': self.run_id,
            'generated_at': self._now(),
            'log_hashes': {
                name: {
                    'filename': path.name,
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                }
                for name, path in written.items()
            },
        }
        manifest_path = self.log_dir / f'{self.run_id}_manifest.json'
        manifest_path.write_text(json.dumps(manifest, indent=2))
        written['manifest'] = manifest_path
        return written

    def summary(self) -> dict:
        real_errors = [e for e in self._errors if e.get('error_type') != 'fallback']
        fallbacks = [e for e in self._errors if e.get('error_type') == 'fallback']
        return {
            'files_ingested': len(self._ingest),
            'files_classified': len(self._classification),
            'multicam_groups_formed': len(
                [e for e in self._grouping if e.get('event') == 'grouping']
            ),
            'variants_detected': len(self._variants),
            'errors': len(real_errors),
            'fallbacks': len(fallbacks),
            'ungrouped_camera_files': len(
                [e for e in self._grouping if e.get('event') == 'ungrouped_camera']
            ),
        }

    def _base(self, file_path: Path) -> dict:
        return {
            'run_id': self.run_id,
            'logged_at': self._now(),
            'filename': file_path.name,
            'file_path_hash': self._path_hash(file_path),
        }

    @staticmethod
    def _path_hash(path: Path) -> str:
        return 'sha256:' + hashlib.sha256(str(path).encode()).hexdigest()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
