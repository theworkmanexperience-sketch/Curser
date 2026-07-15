from __future__ import annotations
"""
W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Timestamp Extraction Engine
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
    # Datetime pattern for .SRT sidecar parsing.
    # Source of truth: scripts/srt_telemetry.py (_DT_RE) — duplicated here
    # deliberately: the engine must not import from scripts/ (tooling layer).
    _SRT_DT_RE = re.compile(
        r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})")

    def _extract_dji_telemetry(self, file_path):
        """
        LIVE (opt-in) — DJI .SRT sidecar timestamp source.

        Reads the FIRST record-time datetime from '<name>.SRT' written
        alongside the clip by DJI Action/Osmo cameras. This is the most
        drift-free timestamp available and addresses the camera clock skew
        behind the §7 grouping-window deviation.

        OPT-IN: only called when config timestamp.enable_srt_telemetry is
        true (default false). When the gate is off, default grouping
        behavior is byte-identical to the validated baseline.

        Datetime ONLY — no GPS parsing, no telemetry.db writes in this
        path (D1: location PII stays out of the deterministic engine;
        full-fidelity telemetry lives in scripts/srt_telemetry.py).

        Returns (unix_timestamp: float, 'dji_srt_sidecar') on success,
        (None, None) otherwise. Never raises.
        """
        try:
            # Sidecar naming: exact-stem match, either extension case
            for ext in ('.SRT', '.srt'):
                sidecar = file_path.with_suffix(ext)
                if sidecar.exists() and sidecar != file_path:
                    break
            else:
                return None, None

            # Read only the head — first datetime is the record start
            with open(sidecar, 'r', errors='ignore') as f:
                head = f.read(8192)

            m = self._SRT_DT_RE.search(head)
            if not m:
                return None, None

            dt = datetime(*(int(g) for g in m.groups()))
            return dt.timestamp(), 'dji_srt_sidecar'
        except Exception:
            return None, None


    def __init__(self, camera_offsets: dict | None = None,
                 enable_srt_telemetry: bool = False):
        self.camera_offsets = camera_offsets or {}
        # Opt-in gate for .SRT sidecar timestamps (default OFF —
        # preserves validated baseline grouping behavior)
        self.enable_srt_telemetry = enable_srt_telemetry

    def extract(self, file_path: Path, camera_source: Optional[str] = None) -> TimestampResult:
        # Opt-in: .SRT sidecar — most drift-free source when present
        if self.enable_srt_telemetry:
            ts, method = self._extract_dji_telemetry(file_path)
            if ts is not None:
                result = TimestampResult(
                    unix_timestamp=ts, method=method,
                    fallback_level=0, confidence='high',
                    raw_value='srt_sidecar')
                return self._apply_offset(result, camera_source)

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

    _ffprobe_missing_warned: bool = False

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
        except FileNotFoundError:
            if not TimestampExtractor._ffprobe_missing_warned:
                print(
                    "\n  ⚠ ffprobe not found — multicam grouping disabled.\n"
                    "    Install FFmpeg 6.0+ to enable: https://ffmpeg.org/download.html\n"
                )
                TimestampExtractor._ffprobe_missing_warned = True
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
