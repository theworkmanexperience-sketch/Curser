"""
Acceptance tests for §17 Test 2: Variant detection + linking.
Covers indexed, suffix, duplicate-keyword, and orphan variant (§3.x Option B).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from wecape.capture.classifier import ClassifiedFile
from wecape.capture.variants import VariantDetector

CONFIG = {
    'variant_detection': {
        'indexed_pattern': r'[\(\[](\d+)[\)\]]',
        'suffix_patterns': ['_v\\d+', '_edit', '_final'],
        'duplicate_keywords': ['copy', 'final', 'backup'],
        'parent_selection': 'largest_file',
    }
}


def make_cf(name: str, size: int = 1000, ts: float = 0.0) -> ClassifiedFile:
    return ClassifiedFile(
        path=Path(f'/fake/{name}'), classification='camera',
        camera_source='DJI', detection_method='test',
        file_size=size, timestamp=ts,
    )


def test_indexed_variants_linked(tmp_path):
    detector = VariantDetector(CONFIG)
    files = [
        make_cf('clip.mp4', size=5000),
        make_cf('clip (1).mp4', size=1000),
        make_cf('clip (2).mp4', size=900),
    ]
    groups, standalone = detector.detect(files)
    assert len(groups) == 1
    assert groups[0].parent.path.name == 'clip.mp4'
    assert len(groups[0].children) == 2


def test_suffix_variants_linked(tmp_path):
    detector = VariantDetector(CONFIG)
    files = [
        make_cf('interview.mp4', size=8000),
        make_cf('interview_v2.mp4', size=7000),
        make_cf('interview_final.mp4', size=6000),
    ]
    groups, standalone = detector.detect(files)
    assert len(groups) == 1
    assert groups[0].parent.path.name == 'interview.mp4'


def test_orphan_variant_becomes_standalone(tmp_path):
    """§3.x Option B: variant with no base → standalone + classification_note."""
    detector = VariantDetector(CONFIG)
    files = [make_cf('drone_edit.mp4', size=3000)]
    groups, standalone = detector.detect(files)
    assert len(groups) == 0
    assert len(standalone) == 1
    assert standalone[0].classification_note == 'variant_pattern_no_base_found'


def test_no_parent_id_written_for_orphan(tmp_path):
    """§3.x Option B: no parent_id field populated."""
    detector = VariantDetector(CONFIG)
    files = [make_cf('scene_final.mp4', size=2000)]
    groups, standalone = detector.detect(files)
    orphan = standalone[0]
    assert not hasattr(orphan, 'parent_id') or getattr(orphan, 'parent_id', 'UNSET') == 'UNSET'
