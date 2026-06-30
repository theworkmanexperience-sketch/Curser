"""
W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — File Classification Engine
§6 File Classification Engine (LOCKED)

Classification order:
  1. Camera source patterns (filename regex + extension)
  2. Audio field recorder patterns → Camera-Audio (§6 final spec)
  3. Audio embedded metadata → Camera-Audio
  4. Reference extension list
  5. Default → Generic

Audio rule (§6 LOCKED — v4.1 ENHANCED final):
  - Audio files matching field_recorder_patterns → Camera-Audio
  - Audio files with camera model in embedded metadata → Camera-Audio
  - All other audio → Generic (NEVER Reference)
  - Reference is reserved for editorial assets (.srt, .edl, .xml, .pdf)
"""

import re
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


AUDIO_EXTENSIONS = {'.wav', '.bwf', '.aiff', '.aif', '.mp3', '.m4a', '.flac', '.ogg'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.mxf', '.avi', '.mkv', '.braw',
                    '.insv', '.r3d', '.lrv', '.wmv', '.webm'}


@dataclass
class ClassifiedFile:
    path: Path
    classification: str            # 'camera' | 'camera_audio' | 'generic' | 'reference'
    camera_source: Optional[str]
    detection_method: str
    classification_note: str = ''  # §11 edge-case annotations
    timestamp: Optional[float] = None
    timestamp_method: Optional[str] = None
    timestamp_fallback_level: int = 0
    timestamp_confidence: str = 'high'
    file_size: int = 0
    file_hash: Optional[str] = None

    @property
    def is_camera(self) -> bool:
        return self.classification in ('camera', 'camera_audio')

    @property
    def is_generic(self) -> bool:
        return self.classification == 'generic'

    @property
    def is_reference(self) -> bool:
        return self.classification == 'reference'

    @property
    def is_audio(self) -> bool:
        return self.classification == 'camera_audio'


class FileClassifier:

    def __init__(self, config: dict):
        cls_cfg = config.get('classification', {})
        audio_cfg = config.get('audio_classification', {})

        self._reference_extensions: set[str] = {
            ext.lower() for ext in cls_cfg.get('reference_extensions', [])
        }
        self._compiled_camera: dict[str, list[re.Pattern]] = {}
        self._camera_extensions: dict[str, set[str]] = {}
        for source, rules in cls_cfg.get('camera_sources', {}).items():
            self._compiled_camera[source] = [
                re.compile(p, re.IGNORECASE) for p in rules.get('patterns', [])
            ]
            self._camera_extensions[source] = {
                ext.lower() for ext in rules.get('extensions', [])
            }

        # Audio field recorder patterns (§6 final spec)
        self._field_recorder_patterns: list[re.Pattern] = [
            re.compile(p, re.IGNORECASE)
            for p in audio_cfg.get('field_recorder_patterns', [])
        ]
        self._audio_default = audio_cfg.get('default_classification', 'generic')

        self._generic_filename_prefixes: list[str] = cls_cfg.get(
            'generic_filename_prefixes', []
        )
        self._generic_filename_substrings: list[str] = cls_cfg.get(
            'generic_filename_substrings', []
        )

        # Folder-based classification patterns (case-insensitive substring match on path parts)
        self._reference_folder_patterns: list[str] = [
            p.lower() for p in cls_cfg.get('reference_folder_patterns', [])
        ]
        self._generic_folder_patterns: list[str] = [
            p.lower() for p in cls_cfg.get('generic_folder_patterns', [])
        ]
        # Camera-model folder patterns (e.g. "DJI ACTION 6" -> "DJI Osmo Action 6").
        # Used to distinguish physical bodies (Osmo Action 5 vs 6) as separate
        # multicam sources when footage is organized in per-camera folders.
        self._camera_folder_patterns: list[dict] = cls_cfg.get('camera_folder_patterns', [])

        # Duplicate detection
        self._dedup_enabled: bool = config.get('pipeline', {}).get(
            'enable_duplicate_content_detection', False
        )

    def classify(self, file_path: Path) -> ClassifiedFile:
        ext = file_path.suffix.lower()
        filename = file_path.name
        size = self._safe_size(file_path)

        # 0. Generic filename override — force generic regardless of extension
        if any(filename.startswith(p) for p in self._generic_filename_prefixes):
            return ClassifiedFile(
                path=file_path, classification='generic',
                camera_source=None, detection_method='generic_filename_prefix',
                file_size=size,
            )

        # 0a. Generic filename substring match (e.g. VID_..._screenshot.jpg)
        if any(p in filename for p in self._generic_filename_substrings):
            return ClassifiedFile(
                path=file_path, classification='generic',
                camera_source=None, detection_method='generic_filename_substring',
                file_size=size,
            )

        # 0b. Folder-based classification — reference/generic by parent folder name
        folder_class = self._match_folder(file_path)
        if folder_class == 'reference':
            return ClassifiedFile(
                path=file_path, classification='reference',
                camera_source=None, detection_method='reference_folder_pattern',
                file_size=size,
            )
        if folder_class == 'generic':
            return ClassifiedFile(
                path=file_path, classification='generic',
                camera_source=None, detection_method='generic_folder_pattern',
                file_size=size,
            )

        # 1. Camera video/image source detection
        camera_source, method = self._detect_camera(filename, ext)
        if camera_source:
            # Refine to the specific body (e.g. "DJI Osmo Action 6") when footage
            # lives in a per-camera folder, so distinct physical cameras are
            # distinct multicam sources (§7).
            folder_model = self._match_camera_folder(file_path)
            if folder_model:
                camera_source, method = folder_model, 'camera_folder_pattern'
            return ClassifiedFile(
                path=file_path, classification='camera',
                camera_source=camera_source, detection_method=method, file_size=size,
            )

        # 2. Audio classification (§6 LOCKED — Generic default, Camera-Audio via patterns)
        if ext in AUDIO_EXTENSIONS:
            return self._classify_audio(file_path, filename, size)

        # 3. Reference files (editorial assets only)
        if ext in self._reference_extensions:
            return ClassifiedFile(
                path=file_path, classification='reference',
                camera_source=None, detection_method='extension_match', file_size=size,
            )

        # 4. Default: Generic
        return ClassifiedFile(
            path=file_path, classification='generic',
            camera_source=None, detection_method='default_generic', file_size=size,
        )

    def classify_batch(self, file_paths: list[Path]) -> list[ClassifiedFile]:
        return [self.classify(p) for p in file_paths]

    def compute_hash(self, file_path: Path, chunk_size_mb: int = 64) -> str:
        """
        Streaming SHA-256 — handles 50GB+ files without loading into memory.
        chunk_size_mb configurable via performance.hash_chunk_size_mb.
        """
        sha256 = hashlib.sha256()
        chunk = chunk_size_mb * 1024 * 1024
        try:
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(chunk)
                    if not data:
                        break
                    sha256.update(data)
            return sha256.hexdigest()
        except (OSError, IOError):
            return ''

    # ------------------------------------------------------------------ #
    # Audio classification                                                 #
    # ------------------------------------------------------------------ #

    def _classify_audio(self, file_path: Path, filename: str, size: int) -> ClassifiedFile:
        """
        §6 Audio rule (LOCKED):
        1. Match field_recorder_patterns → Camera-Audio
        2. Embedded metadata identifies camera model → Camera-Audio
        3. Default → Generic (NEVER Reference)
        """
        # Path 1: filename pattern matching (primarily, §6)
        for pattern in self._field_recorder_patterns:
            if pattern.search(filename):
                return ClassifiedFile(
                    path=file_path, classification='camera_audio',
                    camera_source='FieldRecorder',
                    detection_method=f'field_recorder_pattern:{pattern.pattern}',
                    file_size=size,
                )

        # Path 2: embedded metadata (camera model in EXIF/QuickTime)
        camera_from_meta = self._audio_camera_from_metadata(file_path)
        if camera_from_meta:
            return ClassifiedFile(
                path=file_path, classification='camera_audio',
                camera_source=camera_from_meta,
                detection_method='embedded_metadata_camera_model',
                file_size=size,
            )

        # Default: Generic (§6 — audio is never Reference)
        return ClassifiedFile(
            path=file_path, classification='generic',
            camera_source=None, detection_method='audio_default_generic',
            file_size=size,
        )

    def _audio_camera_from_metadata(self, file_path: Path) -> Optional[str]:
        """Check ffprobe metadata for camera model identifiers in audio files."""
        try:
            import subprocess, json
            result = subprocess.run(
                ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', str(file_path)],
                capture_output=True, text=True, timeout=15,
            )
            if result.returncode != 0:
                return None
            tags = json.loads(result.stdout).get('format', {}).get('tags', {})
            model = tags.get('com.apple.quicktime.model', '') or tags.get('make', '') or tags.get('model', '')
            camera_keywords = ['dji', 'insta360', 'iphone', 'gopro', 'sony', 'canon', 'blackmagic']
            model_lower = model.lower()
            for kw in camera_keywords:
                if kw in model_lower:
                    return model
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------ #
    # Camera detection                                                     #
    # ------------------------------------------------------------------ #

    def _detect_camera(self, filename: str, ext: str) -> tuple[Optional[str], str]:
        all_cam_exts: set[str] = set()
        for exts in self._camera_extensions.values():
            all_cam_exts.update(exts)

        # Pass 1: pattern + extension match
        for source, patterns in self._compiled_camera.items():
            if ext not in self._camera_extensions.get(source, set()):
                continue
            for pattern in patterns:
                if pattern.search(filename):
                    return source, f'filename_pattern:{pattern.pattern}'

        # Pass 2: extension-only for video files (Unknown_Camera)
        if ext in VIDEO_EXTENSIONS and ext not in self._reference_extensions:
            return 'Unknown_Camera', 'extension_only'

        return None, ''

    def _match_folder(self, file_path: Path) -> Optional[str]:
        """Return 'reference' or 'generic' if a parent folder matches a configured pattern."""
        parts_lower = [p.lower() for p in file_path.parts[:-1]]
        for part in parts_lower:
            for pattern in self._reference_folder_patterns:
                if pattern in part:
                    return 'reference'
            for pattern in self._generic_folder_patterns:
                if pattern in part:
                    return 'generic'
        return None

    @staticmethod
    def _safe_size(file_path: Path) -> int:
        try:
            return file_path.stat().st_size
        except OSError:
            return 0

    def _match_camera_folder(self, file_path: Path) -> Optional[str]:
        """Return camera_model if a parent folder matches a configured pattern."""
        parts_lower = [p.lower() for p in file_path.parts[:-1]]
        for entry in self._camera_folder_patterns:
            pattern = str(entry.get('pattern', '')).lower()
            camera_model = entry.get('camera_model')
            if not camera_model:
                continue
            for part in parts_lower:
                if pattern in part:
                    return camera_model
        return None
