"""Phase 1-E — Proxy Generation Tests"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))
import os; os.environ['WECAPE_TEST_MODE'] = '1'

from wecape.capture.proxy import ProxyGenerator, ProxyResult
from wecape.capture.classifier import ClassifiedFile

# ── Helpers ───────────────────────────────────────────────────────────────────

BASE_CONFIG = {
    'proxy_generation': {
        'enabled': True,
        'target_files': 'camera_only',
        'resolution': '720p',
        'bitrate_mbps': 1.5,
        'encoder': 'libx264',
        'preset': 'fast',
        'output_folder': 'PROXIES',
        'skip_unchanged': True,
    }
}

def _cf(name, classification='camera', size=1_000_000):
    """Create a minimal ClassifiedFile for testing."""
    cf = MagicMock(spec=ClassifiedFile)
    cf.path = Path(f'/fake/input/{name}')
    cf.classification = classification
    cf.file_size = size
    return cf

def _gen(config=None):
    return ProxyGenerator(config or BASE_CONFIG)


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_enabled_flag(tmp_path):
    g = ProxyGenerator({'proxy_generation': {'enabled': True}})
    assert g.enabled is True

def test_disabled_flag(tmp_path):
    g = ProxyGenerator({'proxy_generation': {'enabled': False}})
    assert g.enabled is False

def test_enabled_default_is_false(tmp_path):
    g = ProxyGenerator({})
    assert g.enabled is False

def test_camera_only_filter(tmp_path):
    g = _gen()
    files = [_cf('a.mp4', 'camera'), _cf('b.mp4', 'generic'), _cf('c.mp4', 'reference')]
    eligible = g._get_eligible(files)
    assert len(eligible) == 1
    assert eligible[0].path.name == 'a.mp4'

def test_camera_and_generic_filter(tmp_path):
    cfg = {**BASE_CONFIG, 'proxy_generation': {**BASE_CONFIG['proxy_generation'],
           'target_files': 'camera_and_generic'}}
    g = _gen(cfg)
    files = [_cf('a.mp4', 'camera'), _cf('b.mp4', 'generic'), _cf('c.mp4', 'reference')]
    eligible = g._get_eligible(files)
    assert len(eligible) == 2

def test_non_video_extension_skipped(tmp_path):
    g = _gen()
    cf = _cf('photo.jpg', 'camera')
    sha_map = {cf.path: 'sha256:abc'}
    with patch.object(g, '_has_video_stream', return_value=False):
        result = g.generate([cf], tmp_path, tmp_path / 'tmp', sha_map)
    assert result['skipped'] == 1
    assert result['transcoded'] == 0
    assert result['results'][0].status == 'skipped_no_video'

def test_sha256_unchanged_skip(tmp_path):
    g = _gen()
    cf = _cf('clip.mp4', 'camera')
    sha = 'sha256:deadbeef'
    sha_map = {cf.path: sha}
    # Pre-populate registry
    proxy_dir = tmp_path / 'PROXIES'
    proxy_dir.mkdir()
    registry = {sha: {'proxy_path': str(proxy_dir / 'clip.mp4'), 'proxied_at': '2026-01-01'}}
    (proxy_dir / '.proxy_registry.json').write_text(json.dumps(registry))

    with patch.object(g, '_has_video_stream', return_value=True):
        result = g.generate([cf], tmp_path, tmp_path / 'tmp', sha_map)
    assert result['skipped'] == 1
    assert result['results'][0].status == 'skipped_unchanged'

def test_new_file_transcoded(tmp_path):
    g = _gen()
    cf = _cf('new_clip.mp4', 'camera')
    sha = 'sha256:newfile'
    sha_map = {cf.path: sha}
    (tmp_path / 'tmp').mkdir(exist_ok=True)

    fake_result = ProxyResult(
        source_path=cf.path,
        proxy_path=tmp_path / 'PROXIES' / 'new_clip.mp4',
        source_sha256=sha,
        status='transcoded',
        elapsed_s=1.5,
        proxy_size_bytes=5_000_000,
    )
    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', return_value=fake_result):
        result = g.generate([cf], tmp_path, tmp_path / 'tmp', sha_map)
    assert result['transcoded'] == 1
    assert result['skipped'] == 0

def test_registry_written_after_transcode(tmp_path):
    g = _gen()
    cf = _cf('reg_clip.mp4', 'camera')
    sha = 'sha256:regtest'
    sha_map = {cf.path: sha}
    proxy_path = tmp_path / 'PROXIES' / 'reg_clip.mp4'
    (tmp_path / 'tmp').mkdir(exist_ok=True)

    fake_result = ProxyResult(
        source_path=cf.path, proxy_path=proxy_path,
        source_sha256=sha, status='transcoded',
        elapsed_s=1.0, proxy_size_bytes=1_000_000,
    )
    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', return_value=fake_result):
        g.generate([cf], tmp_path, tmp_path / 'tmp', sha_map)

    registry_path = tmp_path / 'PROXIES' / '.proxy_registry.json'
    assert registry_path.exists()
    registry = json.loads(registry_path.read_text())
    assert sha in registry

def test_ffmpeg_failure_logged_as_failed(tmp_path):
    g = _gen()
    cf = _cf('bad_clip.mp4', 'camera')
    sha = 'sha256:badfile'
    sha_map = {cf.path: sha}
    (tmp_path / 'tmp').mkdir(exist_ok=True)

    fake_result = ProxyResult(
        source_path=cf.path, proxy_path=None,
        source_sha256=sha, status='failed',
        reason='ffmpeg_error: codec not found',
    )
    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', return_value=fake_result):
        result = g.generate([cf], tmp_path, tmp_path / 'tmp', sha_map)
    assert result['failed'] == 1
    assert result['transcoded'] == 0

def test_failed_does_not_stop_run(tmp_path):
    """A failed proxy must not halt processing of remaining files."""
    g = _gen()
    cf1 = _cf('bad.mp4', 'camera')
    cf2 = _cf('good.mp4', 'camera')
    sha_map = {cf1.path: 'sha256:bad', cf2.path: 'sha256:good'}
    (tmp_path / 'tmp').mkdir(exist_ok=True)

    def fake_transcode(source, proxy_path, tmp_dir, sha):
        if 'bad' in source.name:
            return ProxyResult(source, None, sha, 'failed', reason='timeout')
        return ProxyResult(source, proxy_path, sha, 'transcoded',
                           elapsed_s=1.0, proxy_size_bytes=1_000_000)

    with patch.object(g, '_has_video_stream', return_value=True), \
         patch.object(g, '_transcode', side_effect=fake_transcode):
        result = g.generate([cf1, cf2], tmp_path, tmp_path / 'tmp', sha_map)
    assert result['failed'] == 1
    assert result['transcoded'] == 1

def test_registry_load_missing_file(tmp_path):
    g = _gen()
    registry = g._load_registry(tmp_path / 'PROXIES')
    assert registry == {}

def test_registry_load_corrupt_json(tmp_path):
    proxy_dir = tmp_path / 'PROXIES'
    proxy_dir.mkdir()
    (proxy_dir / '.proxy_registry.json').write_text('NOT JSON{{')
    g = _gen()
    registry = g._load_registry(proxy_dir)
    assert registry == {}

def test_proxy_output_folder_created(tmp_path):
    g = _gen()
    cf = _cf('clip.mp4', 'camera')
    sha_map = {cf.path: 'sha256:abc'}
    with patch.object(g, '_has_video_stream', return_value=False):
        g.generate([cf], tmp_path, tmp_path / 'tmp', sha_map)
    assert (tmp_path / 'PROXIES').exists()


if __name__ == '__main__':
    tests = [
        test_enabled_flag, test_disabled_flag, test_enabled_default_is_false,
        test_camera_only_filter, test_camera_and_generic_filter,
        test_non_video_extension_skipped, test_sha256_unchanged_skip,
        test_new_file_transcoded, test_registry_written_after_transcode,
        test_ffmpeg_failure_logged_as_failed, test_failed_does_not_stop_run,
        test_registry_load_missing_file, test_registry_load_corrupt_json,
        test_proxy_output_folder_created,
    ]
    passed = failed = 0
    for fn in tests:
        with tempfile.TemporaryDirectory() as td:
            try:
                fn(Path(td)); passed += 1; print(f'  ✓ {fn.__name__}')
            except Exception as e:
                failed += 1; print(f'  ✗ {fn.__name__}: {e}')
    print(f"\n{'='*50}\n{passed}/{passed+failed} passed")
