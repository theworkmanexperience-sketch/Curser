"""
Footage 3-2-1 orchestrator (scripts/backup_footage.sh).

The point of this script is a SAFE, verified, repeatable backup. The most important
test is the GUARD: it must REFUSE to write to the boot volume (the unmounted-target
"stray folder" trap) rather than silently filling the system disk. Also covers the
verified-mirror happy path, restore-drill integration, and dry-run writing nothing.

The guard refuses any target on '/' unless WECAPE_TEST_ALLOW_ROOT=1 — so the refusal
test runs WITHOUT that env, and the happy-path tests set it (sandbox temp dirs are all
on '/').
"""

import os
import subprocess
from pathlib import Path
import tempfile

_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"


def _run(*args, allow_root=False):
    env = dict(os.environ)
    if allow_root:
        env["WECAPE_TEST_ALLOW_ROOT"] = "1"
    return subprocess.run(["bash", str(_SCRIPTS / "backup_footage.sh"), *map(str, args)],
                          capture_output=True, text=True, env=env)


def _shoot(root, name="O-SIX Community Service"):
    d = root / name
    (d / "DJI ACTION 6").mkdir(parents=True)
    (d / "DJI ACTION 6" / "DJI_0001.MP4").write_bytes(b"m" * 500)
    (d / "DJI ACTION 6" / "DJI_0002.MP4").write_bytes(b"n" * 500)
    return d


# ── THE GUARD (most important) ───────────────────────────────────────────────
def test_guard_refuses_boot_volume_target():
    # A target directly under '/' (its mount point resolves to the boot volume) must be
    # REFUSED with a non-zero exit and NOTHING written — the unmounted-drive safety net.
    # (No WECAPE_TEST_ALLOW_ROOT here so the guard actually fires.)
    stray = f"/wecape_no_such_backup_target_{os.getpid()}"
    with tempfile.TemporaryDirectory() as t:
        src = _shoot(Path(t))
        r = _run("--target", stray, "--source", str(src), "--go")
        assert r.returncode == 3
        assert "REFUSING" in r.stdout and "BOOT volume" in r.stdout
        assert not Path(stray).exists()                      # never created under /


def test_offsite_without_remote_is_refused():
    # --offsite with NO --remote would silently upload nothing (the footgun that bit us
    # twice). It must fail LOUDLY (exit 2) before any copy happens, naming --remote.
    with tempfile.TemporaryDirectory() as t:
        src = _shoot(Path(t)); target = Path(t) / "target"
        r = _run("--target", str(target), "--source", str(src), "--go", "--offsite",
                 allow_root=True)
        assert r.returncode == 2, r.stdout + r.stderr
        assert "REFUSING" in r.stdout and "--remote" in r.stdout
        assert not target.exists()                           # nothing written


def test_dry_run_writes_nothing():
    with tempfile.TemporaryDirectory() as t:
        src = _shoot(Path(t)); target = Path(t) / "target"
        r = _run("--target", str(target), "--source", str(src), allow_root=True)   # no --go
        assert r.returncode == 0 and not target.exists()
        assert "DRY-RUN" in r.stdout


# ── happy path (guard bypassed for the sandbox's on-'/' temp dirs) ────────────
def test_execute_mirrors_and_verifies():
    with tempfile.TemporaryDirectory() as t:
        src = _shoot(Path(t)); target = Path(t) / "target"
        log = Path(t) / "backup.log"
        r = _run("--target", str(target), "--source", str(src), "--go", "--log", str(log),
                 allow_root=True)
        assert r.returncode == 0, r.stdout + r.stderr
        dst = target / "O-SIX Community Service" / "DJI ACTION 6" / "DJI_0001.MP4"
        assert dst.read_bytes() == (src / "DJI ACTION 6" / "DJI_0001.MP4").read_bytes()
        assert "backup complete" in r.stdout


def test_restore_test_integration_logs_pass():
    with tempfile.TemporaryDirectory() as t:
        src = _shoot(Path(t)); target = Path(t) / "target"
        log = Path(t) / "backup.log"
        r = _run("--target", str(target), "--source", str(src), "--go", "--restore-test",
                 "--log", str(log), allow_root=True)
        assert r.returncode == 0, r.stdout + r.stderr
        assert (Path(t) / "RESTORE_TESTS.md").read_text().count("| PASS |") >= 1


def test_list_file_is_read():
    with tempfile.TemporaryDirectory() as t:
        src = _shoot(Path(t)); target = Path(t) / "target"
        listing = Path(t) / "sources.txt"
        listing.write_text(f"# priority\n{src}\n\n# a comment line\n")
        r = _run("--target", str(target), "--list", str(listing), "--go",
                 "--log", str(Path(t) / "b.log"), allow_root=True)
        assert r.returncode == 0 and (target / "O-SIX Community Service").exists()
