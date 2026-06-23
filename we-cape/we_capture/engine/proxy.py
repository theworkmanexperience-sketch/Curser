"""
engine/proxy.py — Phase 1-E: Proxy Generation (Stage 6)

Generates H.264 720p proxy files from classified camera files.
Written to PROXIES/ in the output root.
SHA-256 based skip: only retranscode if source changed.
All metadata stripped via -map_metadata -1.

Phase 2 additions:
  workers:   parallel ffmpeg processes (default 1 — set 4 for NVMe storage)
  preflight: ffprobe duration scan before transcoding starts
"""

import concurrent.futures
import json
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


_NON_VIDEO_EXTENSIONS = frozenset({
    '.jpg', '.jpeg', '.png', '.gif', '.heic', '.heif',
    '.raw', '.arw', '.cr2', '.cr3', '.nef', '.dng',
    '.wav', '.mp3', '.aif', '.aiff', '.m4a', '.flac', '.ogg',
    '.pdf', '.docx', '.doc', '.srt', '.aaf', '.edl', '.fcpxml',
    '.txt', '.xml', '.csv', '.json', '.zip', '.rar', '.7z',
})


@dataclass
class ProxyResult:
    source_path:    Path
    proxy_path:     Optional[Path]
    source_sha256:  str
    status:         str     # transcoded | skipped_unchanged | skipped_no_video | failed
    reason:         Optional[str] = None
    elapsed_s:      Optional[float] = None
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
        self._workers        = max(1, int(cfg.get('workers', 1)))      # NEW Phase 2
        self._preflight      = bool(cfg.get('preflight', False))       # NEW Phase 2
        self.ffmpeg_cmd      = ffmpeg_cmd
        self.ffprobe_cmd     = ffprobe_cmd
        self._registry_lock  = threading.Lock()                        # NEW Phase 2

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

        # Pre-flight: scan source durations and estimate runtime before first transcode
        if self._preflight and eligible:
            self._run_preflight(eligible)

        transcoded = skipped = failed = 0
        results:      list[ProxyResult] = []
        to_transcode: list[tuple]       = []  # (cf, src_sha, proxy_path)

        # Resolve all skips upfront — no ffmpeg needed, fast
        for cf in eligible:
            src_sha    = sha_map.get(cf.path, '')
            proxy_path = proxy_dir / (Path(cf.path.stem).with_suffix('.mp4').name)

            if cf.path.suffix.lower() in _NON_VIDEO_EXTENSIONS:
                print(f"  {cf.path.name} → skip (no video stream)")
                results.append(ProxyResult(cf.path, None, src_sha,
                                           'skipped_no_video', 'no_video_stream'))
                skipped += 1
                continue

            if not self._has_video_stream(cf.path):
                print(f"  {cf.path.name} → skip (no video stream)")
                results.append(ProxyResult(cf.path, None, src_sha,
                                           'skipped_no_video', 'no_video_stream'))
                skipped += 1
                continue

            if self._skip_unchanged and src_sha and src_sha in registry:
                print(f"  {cf.path.name} → skip (unchanged)")
                results.append(ProxyResult(cf.path, proxy_path, src_sha,
                                           'skipped_unchanged', 'sha256_match'))
                skipped += 1
                continue

            to_transcode.append((cf, src_sha, proxy_path))

        total = len(to_transcode)

        # ── Measure 2: Pre-run proxy count summary ───────────────────────────
        # Show operator exactly what will happen before first ffmpeg call.
        # Counts are final — all skips resolved, to_transcode is the real list.
        already_proxied = sum(1 for r in results if r.status == 'skipped_unchanged')
        no_video        = sum(1 for r in results if r.status == 'skipped_no_video')
        import os as _os, sys as _sys

        print(f"\n  ── Proxy Run Summary ──────────────────────────────────────")
        print(f"  Eligible:         {len(eligible):>4}")
        print(f"  Already proxied:  {already_proxied:>4}  (SHA registry match — will skip)")
        print(f"  No video stream:  {no_video:>4}  (audio/ref files — will skip)")
        print(f"  To transcode:     {total:>4}  (will run ffmpeg)")
        print(f"  ────────────────────────────────────────────────────────────")

        _non_interactive = (
            not _sys.stdin.isatty()
            or _os.getenv('WECAPE_NONINTERACTIVE') == '1'
        )

        if total == 0:
            print(f"  Nothing to transcode — all files already proxied or skipped.\n")
        elif not _non_interactive:
            print(f"  Proceed with transcoding? Press Enter to continue or Ctrl+C to cancel.")
            print(f"  > ", end='', flush=True)
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                raise RuntimeError("\n  Proxy run cancelled at Measure 2 confirmation.")
        else:
            print(f"  Non-interactive mode — proceeding automatically.\n")
        # ── End Measure 2 ─────────────────────────────────────────────────────

        # ── Measure 4: Smoke test — transcode one file before full run ─────
        # If the first file fails, abort before wasting hours on a broken config.
        # Only runs when total > 1 (single-file runs skip — they ARE the smoke test).
        if total > 1:
            _smoke_cf, _smoke_sha, _smoke_proxy = to_transcode[0]
            _smoke_tmp = tmp_dir / f"_smoketest_{_smoke_sha[:8]}_{_smoke_proxy.name}"
            print(f"  Smoke test [{_smoke_cf.path.name}]...", end='', flush=True)
            _smoke_result = self._transcode(
                _smoke_cf.path, _smoke_proxy, _smoke_tmp, _smoke_sha
            )
            if _smoke_result.status == 'transcoded':
                _smoke_mb = (_smoke_result.proxy_size_bytes or 0) / 1_048_576
                print(f" ✓ ({_smoke_mb:.0f} MB, {_smoke_result.elapsed_s:.1f}s)")
                # Register smoke test result — it counts as transcoded
                with self._registry_lock:
                    _reg = self._load_registry(proxy_dir)
                    _reg[_smoke_sha] = {
                        'proxy_path': str(_smoke_proxy),
                        'proxied_at': _now(),
                    }
                    self._save_registry(proxy_dir, _reg)
                results.append(_smoke_result)
                transcoded += 1
                to_transcode = to_transcode[1:]  # remove smoke test file from queue
                total = len(to_transcode)
            else:
                # Distinguish config failures (abort) from file failures (warn + continue)
                # Config failures: ffmpeg_not_found, encoder_error
                # File failures:   timeout, corrupt source — log and continue
                _config_failures = {'ffmpeg_not_found', 'encoder_error'}
                _is_config_failure = any(
                    tag in (_smoke_result.reason or '')
                    for tag in _config_failures
                )
                if _is_config_failure:
                    print(f" ✗ FAILED — {_smoke_result.reason}")
                    raise RuntimeError(
                        f"\n\n  ✗ Smoke test FAILED — configuration error: "
                        f"{_smoke_cf.path.name}"
                        f"\n  Reason: {_smoke_result.reason}"
                        f"\n  Aborting before full {total}-file run."
                        f"\n  Check ffmpeg installation and encoder config."
                    )
                else:
                    # File-level failure — warn but do not abort
                    print(f" ⚠ ({_smoke_result.reason}) — file issue, continuing run")
                    results.append(_smoke_result)
                    failed += 1
                    to_transcode = to_transcode[1:]
                    total = len(to_transcode)
        # ── End Measure 4 ────────────────────────────────────────────────────

        # ── Measure 5: Heartbeat state ────────────────────────────────────
        # Emits periodic progress in serial path (parallel already logs per-file)
        # Fires every 5 minutes when run has been active > 5 minutes
        import time as _time
        _run_start      = _time.time()
        _last_heartbeat = [_run_start]
        _heartbeat_interval = 300  # seconds (5 minutes)
        # ── End Measure 5 state ───────────────────────────────────────────────

        if self._workers <= 1 or total <= 1:
            # ── Serial path — original behavior, backward compatible ──────────
            for i, (cf, src_sha, proxy_path) in enumerate(to_transcode, 1):
                # Unique tmp path — safe even in serial, prevents stale file collisions
                unique_tmp = tmp_dir / f"_tmp_{src_sha[:8]}_{proxy_path.name}"
                print(f"  [{i}/{total}] {cf.path.name} → transcoding...",
                      end='', flush=True)
                result = self._transcode(cf.path, proxy_path, unique_tmp, src_sha)

                if result.status == 'transcoded':
                    with self._registry_lock:
                        reg = self._load_registry(proxy_dir)
                        reg[src_sha] = {
                            'proxy_path': str(proxy_path),
                            'proxied_at': _now(),
                        }
                        self._save_registry(proxy_dir, reg)
                    mb = (result.proxy_size_bytes or 0) / 1_048_576
                    print(f" done ({mb:.0f} MB, {result.elapsed_s:.1f}s)")
                    transcoded += 1
                else:
                    print(f" FAILED: {result.reason}")
                    failed += 1
                results.append(result)

                # ── Measure 5: Serial heartbeat ───────────────────────────────
                _now_t   = _time.time()
                _elapsed = _now_t - _run_start
                _since   = _now_t - _last_heartbeat[0]
                if _elapsed > _heartbeat_interval and _since > _heartbeat_interval:
                    _pct       = int((i / total) * 100)
                    _rate      = _elapsed / i
                    _remaining = max(0, _rate * (total - i))
                    print(
                        f"  [HEARTBEAT] {i}/{total} files ({_pct}%) | "
                        f"elapsed: {int(_elapsed/60)}m | "
                        f"est. remaining: {int(_remaining/60)}m"
                    )
                    _last_heartbeat[0] = _now_t
                # ── End Measure 5 serial ──────────────────────────────────────

        else:
            # ── Parallel path — workers > 1 ───────────────────────────────────
            print(f"  → parallel transcoding ({self._workers} workers)")
            completed = [0]
            count_lock = threading.Lock()

            def _transcode_one(args: tuple) -> ProxyResult:
                cf, src_sha, proxy_path = args
                # sha prefix in temp name prevents collision:
                # GoPro FAT32 reset produces duplicate filenames across cameras
                unique_tmp = tmp_dir / f"_tmp_{src_sha[:8]}_{proxy_path.name}"
                result = self._transcode(cf.path, proxy_path, unique_tmp, src_sha)

                with count_lock:
                    completed[0] += 1
                    n = completed[0]

                if result.status == 'transcoded':
                    with self._registry_lock:
                        reg = self._load_registry(proxy_dir)
                        reg[src_sha] = {
                            'proxy_path': str(proxy_path),
                            'proxied_at': _now(),
                        }
                        self._save_registry(proxy_dir, reg)
                    mb = (result.proxy_size_bytes or 0) / 1_048_576
                    print(f"  [{n}/{total}] {cf.path.name} "
                          f"→ done ({mb:.0f} MB, {result.elapsed_s:.1f}s)")
                else:
                    print(f"  [{n}/{total}] {cf.path.name} → FAILED: {result.reason}")

                return result

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self._workers
            ) as executor:
                for result in executor.map(_transcode_one, to_transcode):
                    if result.status == 'transcoded':
                        transcoded += 1
                    else:
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
        source:     Path,
        proxy_path: Path,
        tmp_path:   Path,   # unique temp FILE path — not a directory
        src_sha:    str,
    ) -> ProxyResult:
        """
        Transcode source to proxy via ffmpeg.
        tmp_path is a unique file path per call — safe for parallel execution.
        Falls back from h264_videotoolbox to libx264 on encoder failure.
        """
        tmp_proxy = tmp_path
        cmd = self._build_cmd(source, tmp_proxy)
        try:
            t0 = time.time()
            r  = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            elapsed = time.time() - t0

            if r.returncode != 0:
                if self._encoder == 'h264_videotoolbox' and tmp_proxy.exists():
                    tmp_proxy.unlink()
                if self._encoder == 'h264_videotoolbox':
                    cmd2 = self._build_cmd(source, tmp_proxy, force_libx264=True)
                    r2 = subprocess.run(cmd2, capture_output=True, text=True,
                                        timeout=7200)
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
        # Hardware decode: keeps frames in GPU memory, pipes to h264_videotoolbox encoder.
        # ffmpeg silently falls back to software decode if source codec unsupported.
        hwaccel_flags = ['-hwaccel', 'videotoolbox'] if encoder == 'h264_videotoolbox' else []
        base = [self.ffmpeg_cmd] + hwaccel_flags + [
            '-i', str(source),
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

    def _run_preflight(self, eligible: list) -> None:
        """
        Scan all eligible files via ffprobe before transcoding starts.
        Reports total source duration and estimated runtime at current workers.
        Empirical baseline: USB HDD 1 worker = ~10x realtime (Phase 1 validated).
        """
        print("  Pre-flight: scanning source durations...")
        total_sec = 0.0
        scanned   = 0
        for cf in eligible:
            dur = self._get_file_duration(cf.path)
            if dur:
                total_sec += dur
                scanned += 1

        if total_sec == 0:
            print(f"  Pre-flight: {len(eligible)} files (duration unavailable)")
            return

        hours = total_sec / 3600
        n = len(eligible)
        # Empirically validated rates (h264_videotoolbox, software decode):
        # USB HDD 1 worker:  ~7.0 min/proxy  (MG-02 validated — 79 proxies / 9.08h)
        # USB HDD 4 workers: ~2.7 min/proxy  (MG-03a validated — 79 proxies / 3.56h)
        # NVMe 4 workers:    ~2.3 min/proxy  (MG-03b validated — 79 proxies / 3.07h)
        # NVMe 4w + hwaccel: ~0.43 min/proxy  (MG-04 validated — 79 proxies / 34 min)
        # Source: NVMe, workers: 4, encoder: h264_videotoolbox + hwaccel videotoolbox
        est_usb_min   = n * 7.0 / self._workers
        est_nvme_min  = n * 2.3 / self._workers   # software decode (no hwaccel)
        est_hwaccel_min = n * 1.7 / self._workers  # hwaccel decode (MG-04 validated)
        if self._encoder == 'h264_videotoolbox':
            print(
                f"  Pre-flight: {scanned}/{n} files scanned, "
                f"{hours:.1f}h source duration\n"
                f"  Estimated: ~{est_usb_min:.0f}m (USB/{self._workers}w) · "
                f"~{est_nvme_min:.0f}m (NVMe/sw/{self._workers}w) · "
                f"~{est_hwaccel_min:.0f}m (NVMe/hwaccel/{self._workers}w)"
            )
        else:
            print(
                f"  Pre-flight: {scanned}/{n} files scanned, "
                f"{hours:.1f}h source duration\n"
                f"  Estimated: ~{est_usb_min:.0f}m (USB/{self._workers}w) · "
                f"~{est_nvme_min:.0f}m (NVMe/{self._workers}w)"
            )

    def _get_file_duration(self, file_path: Path) -> Optional[float]:
        """Return duration in seconds via ffprobe, or None on failure."""
        try:
            r = subprocess.run(
                [self.ffprobe_cmd, '-v', 'quiet', '-print_format', 'json',
                 '-show_format', str(file_path)],
                capture_output=True, text=True, timeout=15,
            )
            if r.returncode != 0:
                return None
            dur = float(json.loads(r.stdout).get('format', {}).get('duration', 0))
            return dur if dur > 0 else None
        except Exception:
            return None

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
