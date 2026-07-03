"""
Security environment check (scripts/security_check.py) — pure-logic unit tests.

Only the portable, deterministic core is tested here (permission math + path
containment). The live checks (FileVault, rclone) are environment-specific and
best-effort by design, so they are NOT asserted in the suite.
"""

import os
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import security_check as sc          # scripts/security_check.py


def test_perm_check_flags_owner_only():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        p = Path(f.name)
    try:
        os.chmod(p, 0o600)
        r = sc.perm_check(p)
        assert r["owner_only"] and not r["group_or_other_readable"]
    finally:
        p.unlink()


def test_perm_check_flags_group_other_readable():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        p = Path(f.name)
    try:
        os.chmod(p, 0o644)
        r = sc.perm_check(p)
        assert not r["owner_only"] and r["group_or_other_readable"]
    finally:
        p.unlink()


def test_perm_check_missing_file():
    assert sc.perm_check("/no/such/file/here") == {"exists": False}


def test_in_backup_path_true_and_false():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t) / "wecape"; root.mkdir()
        inside = root / "sub" / "x.conf"; inside.parent.mkdir(); inside.write_text("x")
        outside = Path(t) / "elsewhere.conf"; outside.write_text("x")
        assert sc.in_backup_path(inside, [root])
        assert not sc.in_backup_path(outside, [root])
