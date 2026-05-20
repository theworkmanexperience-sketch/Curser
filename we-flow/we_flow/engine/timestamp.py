from __future__ import annotations
"""
W.E. FLOW / W.E. FORGE — Timestamp Extraction Engine
§5 Detection Priority (LOCKED)

Fallback chain (highest → lowest priority):
  0. Filename parsing
  1. File metadata (ffprobe embedded creation_time)
  2. File creation time (os.stat mtime)

Each result carries fallback_level and a timestamp_confidence rating:
  high   = level 0 or 1 (reliable embedded source)
  low    = level 2 (file-system clock — unreliable after copy/transfer)

When confidence is low, the pipeline logs a WARNING and the group is
flagged. The fallback chain is never bypassed — §5 is LOCKED.
"""

import os
import re
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

FILENAME_TIMESTAMP_PATTERNS = [
    (r'(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})', '%Y%m%d_%H%M%S'),
    (r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})', '%Y-%m-%d_%H-%M-%S'),
    (r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})', '%Y%m%d%H%M%S'),
    (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
    (r'(\d{4})(\d{2})(\d{2})', '%Y%m%d'),
]


@dataclass
class TimestampResult:
    unix_timestamp: float
    method: str
    fallback_level: int       # 0=filename, 1=metadata, 2=file_stat
    confidence: str           # 'high' | 'low'
    raw_value: str


class TimestampExtractor:

    def __init__(self, camera_offsets: dict | None = None):
        self.camera_offsets = camera_offsets or {}

    def extract(self, file_path: Path, camera_source: Optional[str] = None) -> TimestampResult:
        result = self._from_filename(file_path)
        if result:
            return self._apply_offset(result, camera_source)

        result = self._from_ffprobe(file_path)
        if result:
            return self._apply_offset(result, camera_source)

        # Level 2: file-system clock — confidence LOW, WARNING logged by pipeline
        result = self._from_file_stat(file_path)
        return self._apply_offset(result, camera_source)

    def _from_filename(self, file_path: Path) -> Optional[TimestampResult]:
        stem = file_path.stem
        for pattern, fmt in FILENAME_TIMESTAMP_PATTERNS:
            match = re.search(pattern, stem)
            if match:
                raw = match.group(0)
                try:
                    clean = raw.replace('-', '').replace('_', '')
                    fmt_clean = fmt.replace('-', '').replace('_', '')
                    dt = datetime.strptime(clean, fmt_clean).replace(tzinfo=timezone.utc)
                    return TimestampResult(
                        unix_timestamp=dt.timestamp(),
                        method='filename',
                        fallback_level=0,
                        confidence='high',
                        raw_value=raw,
                    )
                except ValueError:
                    continue
        return None

    def _from_ffprobe(self, file_path: Path) -> Optional[TimestampResult]:
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', str(file_path)],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                return None
            data = json.loads(result.stdout)
            tags = data.get('format', {}).get('tags', {})
            for key in ['creation_time', 'date', 'DATE', 'com.apple.quicktime.creationdate']:
                raw = tags.get(key)
                if raw:
                    ts = self._parse_iso(raw)
                    if ts:
                        return TimestampResult(
                            unix_timestamp=ts,
                            method='metadata_creation',
                            fallback_level=1,
                            confidence='high',
                            raw_value=raw,
                        )
        except Exception:
            pass
        return None

    def _from_file_stat(self, file_path: Path) -> TimestampResult:
        mtime = file_path.stat().st_mtime
        return TimestampResult(
            unix_timestamp=mtime,
            method='file_stat_mtime',
            fallback_level=2,
            confidence='low',
            raw_value=datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat(),
        )

    def _apply_offset(self, result: TimestampResult, camera_source: Optional[str]) -> TimestampResult:
        if camera_source and camera_source in self.camera_offsets:
            offset = self.camera_offsets[camera_source]
            if offset != 0:
                result.unix_timestamp += offset
                result.raw_value = f"{result.raw_value} (offset: {offset:+.1f}s)"
        return result

    @staticmethod
    def _parse_iso(raw: str) -> Optional[float]:
        formats = [
            '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S', '%Y/%m/%d %H:%M:%S',
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(raw.strip(), fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.timestamp()
            except ValueError:
                continue
        return None
