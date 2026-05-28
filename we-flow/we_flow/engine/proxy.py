"""
engine/proxy.py — Phase 1-E: Proxy Generation (Stage 6)

Generates H.264 720p proxy files from classified camera files.
Written to PROXIES/ in the output root.
SHA-256 based skip: only retranscode if source changed.
All metadata stripped via -map_metadata -1.
"""

import json
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# Extensions that never have a video stream — skip without calling ffprobe
_NON_VIDEO_EXTENSIONS = frozenset({
    '.jpg', '.jpeg', '.png', '.gif', '.heic', '.heif',
    '.raw', '.arw', '.cr2', '.cr3', '.nef', '.dng',
    '.wav', '.mp3', '.aif', '.aiff', '.m4a', '.flac', '.ogg',
    '.pdf', '.docx', '.doc', '.srt', '.aaf', '.edl', '.fcpxml',
    '.txt', '.xml', '.csv', '.json', '.zip', '.rar', '.7z',
})


@dataclass
class ProxyResult:
    source_path: Path
    proxy_path:  Optional[Path]
    source_sha256: str
    status: str          # transcoded | skipped_unchanged | skipped_no_video | failed
    reason: Optional[str] = None
    elapsed_s: Optional[float] = None
    proxy_size_bytes: Optional[int] = None


class ProxyGenerator:
    """Stage 6: Proxy generation engine. Injectable ffmpeg/ffprobe for testing."""

    REGISTRY_FILE = '.proxy_registry.json'

    def __init__(
        self,
        config: dict,
        ffmpeg_cmd:  str = 'ffmpeg',
        ffprobe_cmd: str = 'ffprobe',
    ):
        cfg = config.get('proxy_generation', {})
        self._enabled        = cfg.get('enabled', False)
        self._target_files   = cfg.get('target_files', 'camera_only')
        self._height         = int(str(cfg.get('resolution', '720p')).replace('p', ''))
        self._bitrate        = cfg.get('bitrate_mbps', 1.5)
        self._encoder        = cfg.get('encoder', 'h264_videotoolbox')
        self._preset         = cfg.get('preset', 'fast')
        self._output_folder  = cfg.get('output_folder', 'PROXIES')
        self._skip_unchanged = cfg.get('skip_unchanged', True)
        self.ffmpeg_cmd      = ffmpeg_cmd
        self.ffprobe_cmd     = ffprobe_cmd

    @property
    def enabled(self) -> bool:
        return self._enabled

    # ── Public ────────────────────────────────────────────────────────────────

    def generate(
        self,
        classified_files: list,
        output_path: Path,
        tmp_dir: Path,
        sha_map: dict,
    ) -> dict:
        """
        Generate proxies for eligible classified files.
        Returns stats dict: eligible, transcoded, skipped, failed, results.
        """
        proxy_dir = output_path / self._output_folder
        proxy_dir.mkdir(parents=True, exist_ok=True)

        registry = self._load_registry(proxy_dir)
        eligible  = self._get_eligible(classified_files)

        print(f"  → {len(eligible)} files eligible")

        transcoded = skipped = failed = 0
        results: list[ProxyResult] = []

        for i, cf in enumerate(eligible, 1):
            src_sha = sha_map.get(cf.path, '')
            proxy_path = proxy_dir / (Path(cf.path.stem).with_suffix('.mp4').name)

            # Fast path: known non-video extension
            if cf.path.suffix.lower() in _NON_VIDEO_EXTENSIONS:
                print(f"  [{i}/{len(eligible)}] {cf.path.name} → skip (no video stream)")
                results.append(ProxyResult(cf.path, None, src_sha,
                                           'skipped_no_video', 'no_video_stream'))
                skipped += 1
                continue

            # ffprobe check for edge cases
            if not self._has_video_stream(cf.path):
                print(f"  [{i}/{len(eligible)}] {cf.path.name} → skip (no video stream)")
                results.append(ProxyResult(cf.path, None, src_sha,
                                           'skipped_no_video', 'no_video_stream'))
                skipped += 1
                continue

            # SHA-256 unchanged check
            if self._skip_unchanged and src_sha and src_sha in registry:
                print(f"  [{i}/{len(eligible)}] {cf.path.name} → skip (unchanged)")
                results.append(ProxyResult(cf.path, proxy_path, src_sha,
                                           'skipped_unchanged', 'sha256_match'))
                skipped += 1
                continue

            # Transcode
            print(f"  [{i}/{len(eligible)}] {cf.path.name} → transcoding...",
                  end='', flush=True)
            result = self._transcode(cf.path, proxy_path, tmp_dir, src_sha)

            if result.status == 'transcoded':
                registry[src_sha] = {
                    'proxy_path': str(proxy_path),
                    'proxied_at': _now(),
                }
                self._save_registry(proxy_dir, registry)
                mb = (result.proxy_size_bytes or 0) / 1_048_576
                print(f" done ({mb:.0f} MB, {result.elapsed_s:.1f}s)")
                transcoded += 1
            else:
                print(f" FAILED: {result.reason}")
                failed += 1

            results.append(result)

        return {
            'proxy_dir':   str(proxy_dir),
            'eligible':    len(eligible),
            'transcoded':  transcoded,
            'skipped':     skipped,
            'failed':      failed,
            'results':     results,
        }

    # ── Private ───────────────────────────────────────────────────────────────

    def _get_eligible(self, classified_files: list) -> list:
        if self._target_files == 'camera_only':
            return [f for f in classified_files if f.classification == 'camera']
        if self._target_files == 'camera_and_generic':
            return [f for f in classified_files
                    if f.classification in ('camera', 'generic')]
        # all_video — anything not in non-video extensions
        return [f for f in classified_files
                if f.path.suffix.lower() not in _NON_VIDEO_EXTENSIONS]

    def _has_video_stream(self, file_path: Path) -> bool:
        try:
            r = subprocess.run(
                [self.ffprobe_cmd, '-v', 'quiet', '-print_format', 'json',
                 '-show_streams', str(file_path)],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode != 0:
                return False
            streams = json.loads(r.stdout).get('streams', [])
            return any(s.get('codec_type') == 'video' for s in streams)
        except Exception:
            return False

    def _transcode(
        self,
        source: Path,
        proxy_path: Path,
        tmp_dir: Path,
        src_sha: str,
    ) -> ProxyResult:
        tmp_proxy = tmp_dir / proxy_path.name
        cmd = self._build_cmd(source, tmp_proxy)
        try:
            t0 = time.time()
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            elapsed = time.time() - t0

            if r.returncode != 0:
                # If videotoolbox failed, retry with libx264
                if self._encoder == 'h264_videotoolbox' and tmp_proxy.exists():
                    tmp_proxy.unlink()
                if self._encoder == 'h264_videotoolbox':
                    cmd2 = self._build_cmd(source, tmp_proxy, force_libx264=True)
                    r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=7200)
                    if r2.returncode == 0:
                        shutil.move(str(tmp_proxy), str(proxy_path))
                        return ProxyResult(
                            source, proxy_path, src_sha, 'transcoded',
                            elapsed_s=time.time() - t0,
                            proxy_size_bytes=proxy_path.stat().st_size,
                        )
                return ProxyResult(source, None, src_sha, 'failed',
                                   reason=f'ffmpeg_error: {r.stderr[-300:]}')

            shutil.move(str(tmp_proxy), str(proxy_path))
            return ProxyResult(
                source, proxy_path, src_sha, 'transcoded',
                elapsed_s=elapsed,
                proxy_size_bytes=proxy_path.stat().st_size,
            )

        except subprocess.TimeoutExpired:
            if tmp_proxy.exists():
                tmp_proxy.unlink()
            return ProxyResult(source, None, src_sha, 'failed', reason='timeout')
        except Exception as e:
            if tmp_proxy.exists():
                tmp_proxy.unlink()
            return ProxyResult(source, None, src_sha, 'failed', reason=str(e))

    def _build_cmd(self, source: Path, output: Path,
                   force_libx264: bool = False) -> list:
        encoder = 'libx264' if force_libx264 else self._encoder
        base = [
            self.ffmpeg_cmd, '-i', str(source),
            '-vf', f'scale=-2:{self._height}',
            '-c:a', 'aac', '-b:a', '128k',
            '-map_metadata', '-1',
            '-movflags', '+faststart',
            '-y',
        ]
        if encoder == 'h264_videotoolbox':
            return base + ['-c:v', 'h264_videotoolbox',
                           '-b:v', f'{self._bitrate}M', str(output)]
        return base + ['-c:v', 'libx264', '-preset', self._preset,
                       '-b:v', f'{self._bitrate}M', str(output)]

    def _load_registry(self, proxy_dir: Path) -> dict:
        p = proxy_dir / self.REGISTRY_FILE
        if p.exists():
            try:
                return json.loads(p.read_text())
            except Exception:
                return {}
        return {}

    def _save_registry(self, proxy_dir: Path, registry: dict) -> None:
        (proxy_dir / self.REGISTRY_FILE).write_text(
            json.dumps(registry, indent=2)
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
