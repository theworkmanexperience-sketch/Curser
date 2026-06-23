"""
Acceptance tests for §17 Test 1: Classification accuracy.
Tests run against synthetic files — full accuracy test requires benchmark_manifest.json.
"""
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from wecape.capture.classifier import FileClassifier, AUDIO_EXTENSIONS

MINIMAL_CONFIG = {
    'pipeline': {'file_operation': 'copy', 'enable_duplicate_content_detection': False},
    'audio_classification': {
        'field_recorder_patterns': ['^ZOOM\\d*', '^SD_\\d+', '^TASCAM_'],
        'default_classification': 'generic',
    },
    'classification': {
        'camera_sources': {
            'DJI': {'patterns': ['^DJI_'], 'extensions': ['.mp4', '.mov']},
            'iPhone': {'patterns': ['^IMG_\\d{4}'], 'extensions': ['.mov', '.mp4', '.jpg']},
        },
        'reference_extensions': ['.pdf', '.srt', '.edl', '.xml'],
        'generic_video_extensions': ['.mp4', '.mov', '.avi'],
        'generic_image_extensions': ['.png', '.tiff'],
    },
}


def make_file(name: str, tmp_path: Path) -> Path:
    f = tmp_path / name
    f.write_bytes(b'0' * 1024)
    return f


def test_dji_classified_as_camera(tmp_path):
    clf = FileClassifier(MINIMAL_CONFIG)
    f = make_file('DJI_0001.mp4', tmp_path)
    result = clf.classify(f)
    assert result.classification == 'camera'
    assert result.camera_source == 'DJI'


def test_iphone_classified_as_camera(tmp_path):
    clf = FileClassifier(MINIMAL_CONFIG)
    f = make_file('IMG_4321.mov', tmp_path)
    result = clf.classify(f)
    assert result.classification == 'camera'
    assert result.camera_source == 'iPhone'


def test_zoom_audio_classified_as_camera_audio(tmp_path):
    clf = FileClassifier(MINIMAL_CONFIG)
    f = make_file('ZOOM0001.wav', tmp_path)
    result = clf.classify(f)
    assert result.classification == 'camera_audio'


def test_unknown_audio_classified_as_generic(tmp_path):
    """Audio with no field recorder pattern → Generic (§6: never Reference)."""
    clf = FileClassifier(MINIMAL_CONFIG)
    f = make_file('interview_mix.wav', tmp_path)
    result = clf.classify(f)
    assert result.classification == 'generic'
    assert result.classification != 'reference'


def test_srt_classified_as_reference(tmp_path):
    clf = FileClassifier(MINIMAL_CONFIG)
    f = make_file('captions.srt', tmp_path)
    result = clf.classify(f)
    assert result.classification == 'reference'


def test_png_classified_as_generic(tmp_path):
    clf = FileClassifier(MINIMAL_CONFIG)
    f = make_file('thumbnail.png', tmp_path)
    result = clf.classify(f)
    assert result.classification == 'generic'


def test_unknown_video_classified_as_camera(tmp_path):
    """Unknown .mp4 (no pattern match) → Unknown_Camera via extension-only."""
    clf = FileClassifier(MINIMAL_CONFIG)
    f = make_file('clip_001.mp4', tmp_path)
    result = clf.classify(f)
    assert result.classification == 'camera'
    assert result.camera_source == 'Unknown_Camera'
