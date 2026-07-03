#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Security environment check  (resolves SECURITY_RISK_ANALYSIS [VERIFY]s)

Audits the RUNTIME facts the analysis document cannot see from source code:
  • D3 — rclone.conf permissions + whether it sits in a backed-up path
  • D4 — FileVault status (internal disk at rest)
  • D2 — whether an offsite *crypt* remote is configured

Read-only, stdlib-only, macOS-aware (degrades gracefully elsewhere). This is an
operator audit, NOT a unit test — a pytest that inspected your real home config
would be flaky and non-portable. The pure logic below is unit-tested; the live
checks are best-effort.

Run:  python3 scripts/security_check.py
"""

import stat
import subprocess
from pathlib import Path

RCLONE_CONF = Path.home() / ".config" / "rclone" / "rclone.conf"
BACKUP_ROOTS = [Path.home() / ".wecape", Path.home() / ".wecape_snapshots"]


# ── pure, unit-tested ────────────────────────────────────────────────────────
def perm_check(path):
    p = Path(path)
    if not p.exists():
        return {"exists": False}
    mode = stat.S_IMODE(p.stat().st_mode)
    return {"exists": True, "mode": oct(mode),
            "owner_only": mode in (0o600, 0o400),
            "group_or_other_readable": bool(mode & 0o077)}


def in_backup_path(path, roots):
    p = Path(path).resolve()
    for r in roots:
        try:
            p.relative_to(Path(r).resolve())
            return True
        except ValueError:
            continue
    return False


# ── best-effort live checks ──────────────────────────────────────────────────
def filevault_on():
    try:
        out = subprocess.run(["fdesetup", "status"], capture_output=True, text=True, timeout=5)
        return ("On" in out.stdout) if out.returncode == 0 else None
    except Exception:
        return None


def crypt_remote_present():
    try:
        out = subprocess.run(["rclone", "listremotes", "--long"],
                             capture_output=True, text=True, timeout=5)
        return ("crypt" in out.stdout.lower()) if out.returncode == 0 else None
    except Exception:
        return None


def main():
    print("\n  W.E. C.A.P.E. — security environment check")
    print("  " + "=" * 44)

    pc = perm_check(RCLONE_CONF)                                       # D3
    if not pc.get("exists"):
        print(f"  [–] rclone.conf not found at {RCLONE_CONF} (offsite not configured yet?)")
    else:
        ok = pc["owner_only"]
        print(f"  [{'✓' if ok else '⚠'}] rclone.conf perms {pc['mode']} — "
              + ("owner-only" if ok else f"GROUP/OTHER READABLE → run: chmod 600 {RCLONE_CONF}"))
        inb = in_backup_path(RCLONE_CONF, BACKUP_ROOTS)
        print(f"  [{'✓' if not inb else '⚠'}] rclone.conf is "
              + ("NOT inside a backed-up path" if not inb else "INSIDE a backed-up path — move it out"))

    fv = filevault_on()                                               # D4
    print(f"  [{'✓' if fv else ('⚠' if fv is False else '–')}] FileVault "
          + ("On" if fv else ("OFF → System Settings ▸ Privacy & Security ▸ FileVault"
                              if fv is False else "status unknown (not macOS / no permission)")))

    cr = crypt_remote_present()                                       # D2
    print(f"  [{'✓' if cr else '–'}] offsite crypt remote "
          + ("configured" if cr else "not detected (recommended for annotations.db — see D2)"))

    print("\n  Environment audit — resolve any ⚠. Full context: SECURITY_RISK_ANALYSIS.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
