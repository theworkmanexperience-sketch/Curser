"""
Acceptance tests for §17 Test 3: Multicam grouping.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.classifier import ClassifiedFile
from engine.grouper import MulticamGrouper

CONFIG = {
    'grouping': {'window_seconds': 5, 'min_cameras': 2, 'camera_offsets': {}},
    'output': {'group_id_prefix': 'MCG'},
}


def make_cf(name: str, source: str, ts: float) -> ClassifiedFile:
    return ClassifiedFile(
        path=Path(f'/fake/{name}'), classification='camera',
        camera_source=source, detection_method='test',
        file_size=1000, timestamp=ts,
    )


def test_two_sources_within_window_form_group(tmp_path):
    grouper = MulticamGrouper(CONFIG)
    files = [
        make_cf('dji.mp4', 'DJI', 1000.0),
        make_cf('iphone.mov', 'iPhone', 1003.0),
    ]
    result = grouper.group(files)
    assert len(result.groups) == 1
    assert len(result.ungrouped) == 0


def test_single_source_does_not_group(tmp_path):
    grouper = MulticamGrouper(CONFIG)
    files = [make_cf('dji_a.mp4', 'DJI', 1000.0), make_cf('dji_b.mp4', 'DJI', 1002.0)]
    result = grouper.group(files)
    assert len(result.groups) == 0
    assert len(result.ungrouped) == 2


def test_outside_window_does_not_group(tmp_path):
    grouper = MulticamGrouper(CONFIG)
    files = [make_cf('dji.mp4', 'DJI', 1000.0), make_cf('iphone.mov', 'iPhone', 1010.0)]
    result = grouper.group(files)
    assert len(result.groups) == 0


def test_no_duplicate_group_membership(tmp_path):
    """§7 LOCKED: a file may not belong to more than one group."""
    grouper = MulticamGrouper(CONFIG)
    files = [
        make_cf('dji.mp4', 'DJI', 1000.0),
        make_cf('iphone.mov', 'iPhone', 1002.0),
        make_cf('gopro.mp4', 'GoPro', 1003.0),
    ]
    result = grouper.group(files)
    all_assigned = [str(f.path) for g in result.groups for f in g.files]
    assert len(all_assigned) == len(set(all_assigned))


def test_three_sources_form_one_group(tmp_path):
    grouper = MulticamGrouper(CONFIG)
    files = [
        make_cf('dji.mp4', 'DJI', 1000.0),
        make_cf('iphone.mov', 'iPhone', 1001.0),
        make_cf('gopro.mp4', 'GoPro', 1004.0),
    ]
    result = grouper.group(files)
    assert len(result.groups) == 1
    assert result.groups[0].file_count == 3
