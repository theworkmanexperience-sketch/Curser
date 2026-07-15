"""
Backup primitives (scripts/mirror_verify.sh, scripts/restore_test.sh).

These are the topology-agnostic building blocks of the storage 3-2-1 remediation.
The point of both is trust: a copy/backup is only real if its bytes are proven, so the
tests assert not just the happy path but that CORRUPTION is caught (a verify that can't
fail is worthless). Run the real scripts via bash on temp dirs.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "scripts"


def _run(script, *args):
    return subprocess.run(["bash", str(_SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True)


def _tree(root):
    (root / "DJI ACTION 6").mkdir(parents=True)      # spaces in path on purpose
    (root / "DJI ACTION 6" / "DJI_0001.MP4").write_bytes(b"clip-one" * 100)
    (root / "DJI ACTION 6" / "DJI_0002.MP4").write_bytes(b"clip-two" * 100)
    (root / "Insta360 X5").mkdir()
    (root / "Insta360 X5" / "VID_0001.insv").write_bytes(b"insta" * 50)


# ── mirror_verify ────────────────────────────────────────────────────────────
def test_mirror_copies_and_verifies():
    with tempfile.TemporaryDirectory() as t:
        src, dst = Path(t) / "src", Path(t) / "dst"
        _tree(src)
        r = _run("mirror_verify.sh", src, dst, "--go")
        assert r.returncode == 0, r.stdout + r.stderr
        assert (dst / "DJI ACTION 6" / "DJI_0001.MP4").read_bytes() == (src / "DJI ACTION 6" / "DJI_0001.MP4").read_bytes()
        assert "every file verified" in r.stdout


def test_mirror_dry_run_writes_nothing():
    with tempfile.TemporaryDirectory() as t:
        src, dst = Path(t) / "src", Path(t) / "dst"
        _tree(src)
        r = _run("mirror_verify.sh", src, dst)          # no --go
        assert r.returncode == 0 and not dst.exists()
        assert "dry-run" in r.stdout.lower()


def test_mirror_verify_only_catches_bitrot():
    with tempfile.TemporaryDirectory() as t:
        src, dst = Path(t) / "src", Path(t) / "dst"
        _tree(src)
        assert _run("mirror_verify.sh", src, dst, "--go").returncode == 0
        # silently corrupt a byte in the DEST copy (rsync-invisible bit-rot)
        bad = dst / "DJI ACTION 6" / "DJI_0001.MP4"
        b = bytearray(bad.read_bytes()); b[0] ^= 0xFF; bad.write_bytes(bytes(b))
        r = _run("mirror_verify.sh", src, dst, "--verify-only")
        assert r.returncode == 1 and "MISMATCH" in r.stdout


# ── restore_test ─────────────────────────────────────────────────────────────
def test_restore_drill_passes_and_logs():
    with tempfile.TemporaryDirectory() as t:
        src, backup, scratch = Path(t) / "src", Path(t) / "backup", Path(t) / "scratch"
        log = Path(t) / "RESTORE_TESTS.md"
        _tree(src)
        assert _run("mirror_verify.sh", src, backup, "--go").returncode == 0
        r = _run("restore_test.sh", "--source", src, "--backup", backup,
                 "--scratch", scratch, "--log", log, "--sample", 3)
        assert r.returncode == 0, r.stdout + r.stderr
        text = log.read_text()
        assert "| PASS |" in text and "Restore Tests" in text


def test_restore_drill_fails_on_bad_backup():
    with tempfile.TemporaryDirectory() as t:
        src, backup, scratch = Path(t) / "src", Path(t) / "backup", Path(t) / "scratch"
        log = Path(t) / "RESTORE_TESTS.md"
        _tree(src)
        _run("mirror_verify.sh", src, backup, "--go")
        # corrupt the backup copy — the drill must catch it, not rubber-stamp it
        bad = backup / "DJI ACTION 6" / "DJI_0001.MP4"
        bad.write_bytes(b"corrupted")
        r = _run("restore_test.sh", "--source", src, "--backup", backup,
                 "--scratch", scratch, "--log", log, "--sample", 3)
        assert r.returncode == 1
        assert "| FAIL |" in log.read_text()
