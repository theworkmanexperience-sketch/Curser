"""Phase 1-C — Config Profile System Tests"""

import sys, tempfile, yaml
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import os; os.environ['WE_FLOW_TEST_MODE'] = '1'

from engine.profile import ProfileLoader, deep_merge

BASE_CONFIG = {
    'pipeline': {'file_operation': 'symlink', 'enable_duplicate_content_detection': False},
    'grouping': {'window_seconds': 5, 'min_cameras': 2, 'camera_offsets': {'DJI': 0}},
    'classification': {'camera_folder_patterns': [], 'generic_filename_prefixes': ['Screenshot']},
    'archive_engine': {'enabled': False},
    'performance': {'max_workers': 8},
}

def _write_profile(directory, name, data):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f'{name}.yaml'
    path.write_text(yaml.dump(data))
    return path

def test_deep_merge_preserves_unoverridden_keys(tmp_path):
    base = {'a': 1, 'b': {'x': 10, 'y': 20}}
    result = deep_merge(base, {'b': {'x': 99}})
    assert result['a'] == 1
    assert result['b']['x'] == 99
    assert result['b']['y'] == 20

def test_deep_merge_adds_new_keys(tmp_path):
    result = deep_merge({'a': 1}, {'b': 2})
    assert result['a'] == 1 and result['b'] == 2

def test_deep_merge_list_replaced_not_merged(tmp_path):
    result = deep_merge({'p': ['A', 'B']}, {'p': ['C']})
    assert result['p'] == ['C']

def test_profile_loads_from_system_dir(tmp_path):
    sd = tmp_path / 'profiles'
    _write_profile(sd, 'tc', {'profile_name': 'tc', 'grouping': {'window_seconds': 20}})
    loader = ProfileLoader()
    loader.system_dir = sd
    loader.user_dir = tmp_path / 'up'
    result = loader.load('tc', BASE_CONFIG)
    assert result['grouping']['window_seconds'] == 20
    assert result['grouping']['min_cameras'] == 2

def test_user_profile_overrides_system(tmp_path):
    sd, ud = tmp_path / 'profiles', tmp_path / 'user'
    _write_profile(sd, 'cx', {'profile_name': 'cx', 'grouping': {'window_seconds': 10}})
    _write_profile(ud, 'cx', {'profile_name': 'cx', 'grouping': {'window_seconds': 30}})
    loader = ProfileLoader()
    loader.system_dir = sd
    loader.user_dir = ud
    assert loader.load('cx', BASE_CONFIG)['grouping']['window_seconds'] == 30

def test_missing_profile_raises(tmp_path):
    loader = ProfileLoader()
    loader.system_dir = tmp_path / 'p'
    loader.user_dir = tmp_path / 'u'
    try:
        loader.load('nope', BASE_CONFIG)
        assert False
    except FileNotFoundError as e:
        assert 'nope' in str(e)

def test_metadata_stripped_before_merge(tmp_path):
    sd = tmp_path / 'profiles'
    _write_profile(sd, 'mt', {
        'profile_name': 'mt', 'profile_version': '2.0',
        'client': 'X', 'description': 'Y', 'created': '2026',
        'grouping': {'window_seconds': 25},
    })
    loader = ProfileLoader()
    loader.system_dir = sd
    loader.user_dir = tmp_path / 'u'
    result = loader.load('mt', BASE_CONFIG)
    assert 'profile_name' not in result
    assert result['grouping']['window_seconds'] == 25

def test_google_drive_profile_enables_archive_engine(tmp_path):
    sd = tmp_path / 'profiles'
    _write_profile(sd, 'gd', {'profile_name': 'gd',
        'archive_engine': {'enabled': True}, 'pipeline': {'file_operation': 'copy'}})
    loader = ProfileLoader()
    loader.system_dir = sd
    loader.user_dir = tmp_path / 'u'
    result = loader.load('gd', BASE_CONFIG)
    assert result['archive_engine']['enabled'] is True
    assert result['pipeline']['file_operation'] == 'copy'

def test_ryderz_profile_sets_window(tmp_path):
    sd = tmp_path / 'profiles'
    _write_profile(sd, 'rz', {'profile_name': 'rz',
        'grouping': {'window_seconds': 15}, 'pipeline': {'file_operation': 'symlink'}})
    loader = ProfileLoader()
    loader.system_dir = sd
    loader.user_dir = tmp_path / 'u'
    result = loader.load('rz', BASE_CONFIG)
    assert result['grouping']['window_seconds'] == 15

def test_active_profile_metadata_in_config(tmp_path):
    sd = tmp_path / 'profiles'
    _write_profile(sd, 'ac', {'profile_name': 'ac', 'client': 'Acme', 'profile_version': '1.2'})
    loader = ProfileLoader()
    loader.system_dir = sd
    loader.user_dir = tmp_path / 'u'
    result = loader.load('ac', BASE_CONFIG)
    assert result['_active_profile']['client'] == 'Acme'
    assert result['_active_profile']['version'] == '1.2'

def test_list_profiles_returns_all(tmp_path):
    sd = tmp_path / 'profiles'
    _write_profile(sd, 'a', {'profile_name': 'a', 'client': 'A'})
    _write_profile(sd, 'b', {'profile_name': 'b', 'client': 'B'})
    loader = ProfileLoader()
    loader.system_dir = sd
    loader.user_dir = tmp_path / 'u'
    names = [p['name'] for p in loader.list_profiles()]
    assert 'a' in names and 'b' in names

if __name__ == '__main__':
    tests = [test_deep_merge_preserves_unoverridden_keys, test_deep_merge_adds_new_keys,
             test_deep_merge_list_replaced_not_merged, test_profile_loads_from_system_dir,
             test_user_profile_overrides_system, test_missing_profile_raises,
             test_metadata_stripped_before_merge, test_google_drive_profile_enables_archive_engine,
             test_ryderz_profile_sets_window, test_active_profile_metadata_in_config,
             test_list_profiles_returns_all]
    passed, failed = [], []
    for fn in tests:
        with tempfile.TemporaryDirectory() as td:
            try:
                fn(Path(td)); passed.append(fn.__name__); print(f'  ✓ {fn.__name__}')
            except Exception as e:
                failed.append(fn.__name__); print(f'  ✗ {fn.__name__}: {e}')
    print(f"\n{'='*50}\n{len(passed)}/{len(passed)+len(failed)} passed")
