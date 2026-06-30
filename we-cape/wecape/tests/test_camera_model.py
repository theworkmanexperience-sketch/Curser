"""
Camera-model folder detection (DJI Osmo Action 5 vs 6) + distinct-source grouping.

Footage organized in per-camera folders ("DJI ACTION 5/6", "Insta360 X5") must
resolve to the specific body, so two distinct DJI cameras are distinct multicam
sources (§7) — previously both collapsed to "DJI" (dead camera_folder_patterns).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.capture.classifier import FileClassifier
from wecape.capture.grouper import MulticamGrouper

CFG = {
    "classification": {
        "camera_sources": {
            "DJI": {"extensions": [".mp4"], "patterns": ["^DJI_"]},
            "Insta360": {"extensions": [".mp4", ".insv"], "patterns": ["^VID_"]},
        },
        "camera_folder_patterns": [
            {"camera_model": "DJI Osmo Action 5", "pattern": "DJI ACTION 5"},
            {"camera_model": "DJI Osmo Action 6", "pattern": "DJI ACTION 6"},
            {"camera_model": "Insta360 X5", "pattern": "Insta360 X5"},
        ],
    },
    "grouping": {"window_seconds": 15, "min_cameras": 2},
}


def test_folder_identifies_specific_body():
    fc = FileClassifier(CFG)
    assert fc.classify(Path("/src/DJI ACTION 5/DJI_0001.MP4")).camera_source == "DJI Osmo Action 5"
    assert fc.classify(Path("/src/DJI ACTION 6/DJI_0002.MP4")).camera_source == "DJI Osmo Action 6"
    assert fc.classify(Path("/src/Insta360 X5/VID_0003.mp4")).camera_source == "Insta360 X5"


def test_no_folder_falls_back_to_family():
    fc = FileClassifier(CFG)
    # No per-camera folder -> unchanged behavior (family from filename pattern).
    assert fc.classify(Path("/src/loose/DJI_0009.MP4")).camera_source == "DJI"


def test_two_dji_bodies_now_form_a_group():
    fc = FileClassifier(CFG)
    files = [fc.classify(Path("/src/DJI ACTION 5/DJI_0001.MP4")),
             fc.classify(Path("/src/DJI ACTION 6/DJI_0002.MP4"))]
    for f in files:
        f.timestamp = 1000.0  # same moment
    res = MulticamGrouper(CFG).group(files)
    assert len(res.groups) == 1, "two distinct DJI bodies should now form a multicam group"
    assert res.groups[0].source_count == 2
