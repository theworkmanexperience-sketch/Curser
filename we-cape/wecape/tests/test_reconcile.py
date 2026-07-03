"""
Footage reconciliation / coverage audit (scripts/reconcile.py).

Pins the core: quick mode flags files whose filename isn't in the registry as
UNPROCESSED, and hash mode matches by SHA (processed) and detects byte-identical
duplicates across folders.
"""

import hashlib
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import reconcile as rc          # scripts/reconcile.py


def test_quick_flags_unprocessed_by_filename():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / "f"; d.mkdir()
        (d / "A.mp4").write_bytes(b"a" * 100)
        (d / "B.mp4").write_bytes(b"b" * 200)
        by_name = defaultdict(list)
        by_name["A.mp4"].append({"file_size_bytes": 100})    # A is in the registry, B is not
        files, _ = rc.reconcile([str(d)], {}, by_name, rc.VIDEO_EXT, False)
        state = {f["path"].name: f["processed"] for f in files}
        assert state == {"A.mp4": True, "B.mp4": False}


def test_hash_matches_registry_and_finds_dups():
    with tempfile.TemporaryDirectory() as t:
        d1 = Path(t) / "f1"; d1.mkdir()
        d2 = Path(t) / "f2"; d2.mkdir()
        (d1 / "X.mp4").write_bytes(b"same" * 1000)
        (d2 / "X.mp4").write_bytes(b"same" * 1000)           # byte-identical duplicate
        (d1 / "Y.mp4").write_bytes(b"unique")
        sha_x = hashlib.sha256(b"same" * 1000).hexdigest()
        by_sha = {sha_x: {"filename": "X.mp4"}}
        files, locs = rc.reconcile([str(d1), str(d2)], by_sha, defaultdict(list), rc.VIDEO_EXT, True)
        proc = {f["path"]: f["processed"] for f in files}
        assert all(v for k, v in proc.items() if k.name == "X.mp4")          # X in registry -> processed
        assert not [v for k, v in proc.items() if k.name == "Y.mp4"][0]      # Y not -> gap
        assert len(locs[sha_x]) == 2                                          # X duplicated across folders


def test_non_video_ignored():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / "f"; d.mkdir()
        (d / "clip.mp4").write_bytes(b"v")
        (d / "notes.txt").write_bytes(b"x")
        (d / ".DS_Store").write_bytes(b"x")
        files, _ = rc.reconcile([str(d)], {}, defaultdict(list), rc.VIDEO_EXT, False)
        assert [f["path"].name for f in files] == ["clip.mp4"]
