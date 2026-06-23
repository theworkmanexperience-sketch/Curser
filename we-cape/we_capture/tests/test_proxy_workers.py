"""
Phase 2 — proxy_workers tests.

Tests parallel execution, thread-safe registry writes,
preflight scan, and unique temp path collision prevention.
All tests use mocked ffmpeg/ffprobe — no real media required.
"""

import json
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

from wecape.capture.proxy import ProxyGenerator, ProxyResult
from wecape.capture.classifier import ClassifiedFile

# ── Helpers ──────────────────────────────────────────────────────────────────

def _cf(name, classification='camera'):
    cf = MagicMock(spec=ClassifiedFile)
    cf.path = Path(f'/fake/input/{name}')
    cf.classification = classification
    return cf


def _gen(workers=1, preflight=False, extra_cfg=None):
    cfg = {
        'proxy_generation': {
            'enabled': True,
            'target_files': 'camera_only',
            'resolution': '720p',
            'bitrate_mbps': 1.5,
            'encoder': 'libx264',
            'preset': 'fast',
            'output_folder': 'PROXIES',
            'skip_unchanged': True,
            'workers': workers,
            'preflight': preflight,
            **(extra_cfg or {}),
        }
    }
    return ProxyGenerator(cfg)


def _fake_transcode(source, proxy_path, tmp_path, sha):
    """Mock _transcode that succeeds immediately."""
    return ProxyResult(
        source_path=source,
        proxy_path=proxy_path,
        source_sha256=sha,
        status='transcoded',
        elapsed_s=0.1,
        proxy_size_bytes=1_000_000,
    )


# ── Config ────────────────────────────────────────────────────────────────────

def test_workers_default_is_one():
    g = ProxyGenerator({'proxy_generation': {}})
    assert g._workers == 1


def test_workers_set_from_config():
    g = _gen(workers=4)
    assert g._workers == 4


def test_workers_clamped_to_minimum_one():
    g = _gen(workers=0)
    assert g._workers == 1


def test_preflight_default_is_false():
    g = ProxyGenerator({'proxy_generation': {}})
    assert g._preflight is False


def test_preflight_set_from_config():
    g = _gen(preflight=True)
    assert g._preflight is True


def test_registry_lock_exists():
    g = _gen()
    assert hasattr(g, '_registry_lock')
    assert isinstance(g._registry_lock, type(threading.Lock()))


# ── Parallel execution ────────────────────────────────────────────────────────

def test_parallel_workers_transcodes_all_files(tmp_path):
    """All files are transcoded when workers=4."""
    g = _gen(workers=4)
    files = [_cf(f'clip_{i}.mp4') for i in range(8)]
    # Shas must differ within first 8 chars (that's the prefix used for temp paths)
    sha_map = {cf.path: f'{i:08x}aabbccdd' for i, cf in enumerate(files)}
    (tmp_path / 'tmp').mkdir()

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=_fake_transcode):
        result = g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    assert result['transcoded'] == 8
    assert result['failed'] == 0
    assert result['skipped'] == 0


def test_parallel_workers_handles_mixed_results(tmp_path):
    """Failed files are counted correctly in parallel mode."""
    g = _gen(workers=4)
    files = [_cf(f'clip_{i}.mp4') for i in range(6)]
    # Shas must differ within first 8 chars (that's the prefix used for temp paths)
    sha_map = {cf.path: f'{i:08x}aabbccdd' for i, cf in enumerate(files)}
    (tmp_path / 'tmp').mkdir()

    def mixed_transcode(source, proxy_path, tmp_path_, sha):
        if 'clip_0' in source.name or 'clip_2' in source.name:
            return ProxyResult(source, None, sha, 'failed', reason='timeout')
        return _fake_transcode(source, proxy_path, tmp_path_, sha)

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=mixed_transcode):
        result = g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    assert result['failed'] == 2
    assert result['transcoded'] == 4


def test_parallel_total_results_count_matches_eligible(tmp_path):
    """Total results (transcoded + skipped + failed) == eligible."""
    g = _gen(workers=4)
    files = [_cf(f'clip_{i}.mp4') for i in range(5)] + [_cf('photo.jpg')]
    # Shas must differ within first 8 chars (that's the prefix used for temp paths)
    sha_map = {cf.path: f'{i:08x}aabbccdd' for i, cf in enumerate(files)}
    (tmp_path / 'tmp').mkdir()

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=_fake_transcode):
        result = g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    total = result['transcoded'] + result['skipped'] + result['failed']
    assert total == result['eligible']


def test_parallel_registry_written_for_all_transcoded(tmp_path):
    """Registry contains entry for every successfully transcoded file."""
    g = _gen(workers=4)
    n_files = 8
    files = [_cf(f'clip_{i}.mp4') for i in range(n_files)]
    # Shas must differ within first 8 chars (that's the prefix used for temp paths)
    sha_map = {cf.path: f'{i:08x}aabbccdd' for i, cf in enumerate(files)}
    (tmp_path / 'tmp').mkdir()

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=_fake_transcode):
        g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    registry_path = tmp_path / 'PROXIES' / '.proxy_registry.json'
    assert registry_path.exists()
    registry = json.loads(registry_path.read_text())
    assert len(registry) == n_files


def test_parallel_registry_no_data_loss_under_concurrency(tmp_path):
    """
    Registry must not lose entries when multiple workers write simultaneously.
    Simulates write contention by adding a small sleep in transcode mock.
    """
    g = _gen(workers=4)
    n_files = 12
    files = [_cf(f'clip_{i}.mp4') for i in range(n_files)]
    # Shas must differ within first 8 chars (that's the prefix used for temp paths)
    sha_map = {cf.path: f'{i:08x}aabbccdd' for i, cf in enumerate(files)}
    (tmp_path / 'tmp').mkdir()

    def slow_transcode(source, proxy_path, tmp_path_, sha):
        time.sleep(0.01)  # simulate brief transcode time
        return _fake_transcode(source, proxy_path, tmp_path_, sha)

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=slow_transcode):
        result = g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    assert result['transcoded'] == n_files
    registry = json.loads(
        (tmp_path / 'PROXIES' / '.proxy_registry.json').read_text()
    )
    # Every transcoded file must have a registry entry — no lost writes
    assert len(registry) == n_files


# ── Temp path collision prevention ───────────────────────────────────────────

def test_transcode_called_with_unique_tmp_paths(tmp_path):
    """
    Each _transcode call receives a unique tmp_path.
    GoPro FAT32 reset produces GX010001.MP4 on multiple camera cards —
    files have same name but different paths and different SHA256 content.
    Unique sha-prefixed temp paths prevent parallel worker collision.
    """
    g = _gen(workers=4)
    # Same filename, different source directories — real GoPro FAT32 scenario
    files = []
    for i in range(4):
        cf = MagicMock(spec=ClassifiedFile)
        cf.path = Path(f'/fake/card_{i}/GX010001.MP4')  # different cards
        cf.classification = 'camera'
        files.append(cf)
    # Shas must differ within first 8 chars (that's the prefix used for temp paths)
    sha_map = {cf.path: f'{i:08x}aabbccdd' for i, cf in enumerate(files)}
    (tmp_path / 'tmp').mkdir()

    seen_tmp_paths = []
    lock = threading.Lock()

    def capture_tmp(source, proxy_path, tmp_path_, sha):
        with lock:
            seen_tmp_paths.append(tmp_path_)
        return _fake_transcode(source, proxy_path, tmp_path_, sha)

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=capture_tmp):
        g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    # All tmp paths must be unique
    assert len(seen_tmp_paths) == len(set(str(p) for p in seen_tmp_paths))


# ── Preflight scan ────────────────────────────────────────────────────────────

def test_preflight_calls_get_file_duration_for_each_eligible(tmp_path):
    g = _gen(workers=1, preflight=True)
    files = [_cf(f'clip_{i}.mp4') for i in range(5)]
    # Shas must differ within first 8 chars (that's the prefix used for temp paths)
    sha_map = {cf.path: f'{i:08x}aabbccdd' for i, cf in enumerate(files)}
    (tmp_path / 'tmp').mkdir()

    duration_calls = []

    def mock_duration(path):
        duration_calls.append(path)
        return 120.0  # 2 minutes per file

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=_fake_transcode), \
         patch.object(g, '_get_file_duration', side_effect=mock_duration):
        g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    assert len(duration_calls) == 5


def test_preflight_skipped_when_disabled(tmp_path):
    g = _gen(workers=1, preflight=False)
    files = [_cf('clip.mp4')]
    sha_map = {files[0].path: 'sha256:abc'}
    (tmp_path / 'tmp').mkdir()

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=_fake_transcode), \
         patch.object(g, '_get_file_duration') as mock_dur:
        g.generate(files, tmp_path, tmp_path / 'tmp', sha_map)

    mock_dur.assert_not_called()


def test_get_file_duration_returns_none_on_failure():
    g = _gen()
    with patch('subprocess.run', side_effect=Exception('ffprobe not found')):
        result = g._get_file_duration(Path('/fake/file.mp4'))
    assert result is None


def test_get_file_duration_returns_none_for_zero_duration():
    g = _gen()
    import subprocess as sp
    mock_run = MagicMock()
    mock_run.returncode = 0
    mock_run.stdout = '{"format": {"duration": "0"}}'
    with patch('subprocess.run', return_value=mock_run):
        result = g._get_file_duration(Path('/fake/file.mp4'))
    assert result is None


def test_get_file_duration_returns_float_on_success():
    g = _gen()
    mock_run = MagicMock()
    mock_run.returncode = 0
    mock_run.stdout = '{"format": {"duration": "127.5"}}'
    with patch('subprocess.run', return_value=mock_run):
        result = g._get_file_duration(Path('/fake/file.mp4'))
    assert result == 127.5
