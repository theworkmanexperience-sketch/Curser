#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Export Wizard  (novice-friendly, interactive)

A guided front end for scripts/fcpxml_export.py: pick your shoot from a numbered
list, optionally add a stills folder (just drag it into the window), and it runs
the export and opens Final Cut Pro's import sheet — no run IDs or long paths to type.

Advanced users: call fcpxml_export.py directly for --media / --fps / --groups-only.

Run it:   double-click `wecape_export.command`, or:  python3 scripts/export_wizard.py
"""

import os
import shutil
import sqlite3
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXPORT = REPO / "scripts" / "fcpxml_export.py"
DB = Path(os.environ.get("WECAPE_DB", str(Path.home() / ".wecape" / "registry" / "wecape.db")))


def load_runs():
    if not DB.exists():
        return []
    uri = f"file:{DB.resolve().as_posix()}?mode=ro"
    c = sqlite3.connect(uri, uri=True)
    c.row_factory = sqlite3.Row
    try:
        # SELECT * so a schema variant never breaks the picker; fields read via .get().
        return [dict(r) for r in c.execute(
            "SELECT * FROM runs WHERE file_count > 0 ORDER BY timestamp DESC")]
    except sqlite3.Error:
        return []
    finally:
        c.close()


def _ask(prompt, default=""):
    try:
        v = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        v = ""
    return v or default


def _clean_path(raw):
    """A path dragged into Terminal arrives shell-escaped/quoted — normalize it."""
    p = raw.strip().strip("'\"")
    return p.replace("\\", "")          # drop escape backslashes (mac paths have none)


def main():
    print("\n  W.E. C.A.P.E. — Export to Final Cut Pro")
    print("  " + "=" * 44)

    runs = load_runs()
    if not runs:
        print(f"\n  No shoots found in the registry ({DB}).")
        print("  Run a CAPTURE first, then come back.\n")
        return 1

    print("\n  Your shoots (newest first):\n")
    shown = runs[:20]
    for i, r in enumerate(shown, 1):
        name = Path(r["output_path"] or "").name or r["id"]
        print(f"    {i:>2}. {name}   ({r['file_count']} files · {(r['timestamp'] or '')[:10]})")

    sel = _ask(f"\n  Pick a shoot [1-{len(shown)}], or Return for 1: ", "1")
    try:
        run = shown[int(sel) - 1]
        assert int(sel) >= 1
    except Exception:
        print("  That wasn't a valid choice — nothing exported.\n")
        return 1
    run_id = run["id"]
    name = Path(run["output_path"] or "").name or run_id
    out_dir, src_dir = run.get("output_path") or "", run.get("source_path") or ""

    # Drive check — the shoot's output folder must be connected to export.
    if out_dir and not Path(out_dir).is_dir():
        print(f"\n  ⚠  This shoot's folder isn't connected:\n        {out_dir}")
        print("     Plug in the drive (WE_CAPE_OUTPUT, and 10TB for full-res originals), then retry.")
        if not _ask("     Continue anyway? [y/N]: ", "n").lower().startswith("y"):
            return 1

    # Stills — auto-detect a 'Photos' folder in the source, else offer to drag one in.
    extra = []
    auto = next((Path(src_dir) / "Photos" for _ in [0]
                 if src_dir and (Path(src_dir) / "Photos").is_dir()), None)
    if auto:
        if _ask(f"\n  Found a Photos folder — include those stills?\n        {auto}\n     [Y/n]: ",
                "y").lower().startswith("y"):
            extra += ["--stills", str(auto)]
    elif _ask("\n  Include still photos / screenshots? [y/N]: ", "n").lower().startswith("y"):
        folder = _clean_path(_ask("  Drag the Photos folder into this window and press Return: "))
        if folder:
            extra += ["--stills", folder]

    out = Path.home() / "Desktop" / f"{name}_multicam.fcpxml"
    print(f"\n  Exporting '{name}'…\n")
    rc = subprocess.run(
        ["python3", str(EXPORT), "--run", run_id, "--db", str(DB), "--out", str(out)] + extra
    ).returncode
    if rc != 0:
        print("\n  ✗ Export didn't finish — see the messages above.\n")
        return rc

    print(f"\n  ✓ Saved to your Desktop: {out.name}")
    if out.exists() and shutil.which("open"):
        subprocess.run(["open", str(out)])
        print("  ✓ Opening Final Cut Pro — confirm the import sheet (Replace · Keep SDR).")
    else:
        print(f"  In Final Cut Pro: File ▸ Import ▸ XML…  →  {out}")

    cheat = REPO / "scripts" / "next_steps_fcp.html"     # the novice one-pager
    if cheat.exists() and shutil.which("open"):
        subprocess.run(["open", str(cheat)])
        print("  ✓ A 'Next Steps in Final Cut' guide opened in your browser — just follow it.")
    print("\n  ── To see everything FIRST-shot → LAST-shot ─────────────────")
    print("     1. In the FCP browser, switch to List view (the list icon, top-left).")
    print("     2. Click the 'Name' column header  (or  Sort By ▸ Name ▸ Ascending).")
    print("     Every clip & photo is time-stamped, so Name order IS capture order.")
    print("     FCP remembers this — you set it once, per library.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
