#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Footage Reconciliation / Coverage Audit  (ops tooling, read-only)

Cross-references footage folders against the CAPTURE registry to answer, with proof:
  • PROCESSED   — the file's content is in the registry (CAPTURE ingested it).
  • UNPROCESSED — a coverage gap: footage present on disk but never processed.
  • DUPLICATE   — byte-identical content in more than one place (reclaimable space).
  • (orphans)   — registry files not found in any scanned folder (moved/deleted originals).

Read-only on the registry. stdlib only. Zero network.

Modes:
  quick (default): match by filename (+ size) — fast first pass.
  --hash:          SHA-256 every file — definitive, and finds byte-identical duplicates.

Usage:
  python3 scripts/reconcile.py \\
      --folder "/Volumes/10TB/O-SIX RYDERZ /O-SIX RYDERZ MC Community Service/DJI ACTION 5" \\
      --folder ".../DJI ACTION 6" --folder ".../Insta360 X5" \\
      --folder ".../DCIM_Sat_3-21_Insta360" --hash
"""

import argparse
import hashlib
import sqlite3
from collections import defaultdict
from pathlib import Path

DEFAULT_DB = Path.home() / ".wecape" / "registry" / "wecape.db"
VIDEO_EXT = {".mp4", ".mov", ".mxf", ".avi", ".mkv", ".insv", ".lrv", ".360", ".braw", ".r3d"}
CHUNK = 8 * 1024 * 1024


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(CHUNK), b""):
            h.update(b)
    return h.hexdigest()


def human(n):
    n = float(n or 0)
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or u == "TB":
            return f"{n:.1f} {u}"
        n /= 1024


def load_registry(db):
    uri = f"file:{Path(db).resolve().as_posix()}?mode=ro"
    c = sqlite3.connect(uri, uri=True)
    c.row_factory = sqlite3.Row
    by_sha, by_name = {}, defaultdict(list)
    try:
        for r in c.execute("SELECT id, filename, original_path, proxy_path, file_size_bytes FROM content"):
            d = dict(r)
            by_sha[d["id"]] = d
            if d.get("filename"):
                by_name[d["filename"]].append(d)
    finally:
        c.close()
    return by_sha, by_name


def is_processed_quick(path, size, by_name):
    """Filename (+ size when known) match against the registry."""
    for c in by_name.get(path.name, []):
        s = c.get("file_size_bytes")
        if s in (None, 0, size):
            return True
    return False


def walk(folder, exts):
    for p in sorted(Path(folder).rglob("*")):
        if p.is_file() and p.suffix.lower() in exts and not p.name.startswith("._"):
            yield p


def reconcile(folders, by_sha, by_name, exts, use_hash):
    files = []
    sha_locations = defaultdict(list)
    for folder in folders:
        fp = Path(folder)
        if not fp.exists():
            print(f"⚠ folder not found: {folder}")
            continue
        for p in walk(fp, exts):
            size = p.stat().st_size
            rec = {"path": p, "folder": folder, "size": size, "processed": False, "sha": None}
            if use_hash:
                sh = sha256(p)
                rec["sha"] = sh
                rec["processed"] = sh in by_sha
                sha_locations[sh].append(p)
            else:
                rec["processed"] = is_processed_quick(p, size, by_name)
            files.append(rec)
    return files, sha_locations


def main(argv=None):
    ap = argparse.ArgumentParser(description="Reconcile footage folders against the CAPTURE registry.")
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--folder", action="append", required=True, help="folder to audit (repeatable)")
    ap.add_argument("--hash", action="store_true", help="SHA-256 every file (definitive; finds byte-identical dups)")
    ap.add_argument("--ext", help="comma-separated extensions (default: common video)")
    args = ap.parse_args(argv)

    if not args.db.exists():
        raise SystemExit(f"registry not found: {args.db}")
    exts = ({"." + e.strip().lower().lstrip(".") for e in args.ext.split(",")} if args.ext else VIDEO_EXT)
    by_sha, by_name = load_registry(args.db)

    files, sha_locations = reconcile(args.folder, by_sha, by_name, exts, args.hash)

    print("=" * 68)
    print(f"  Reconciliation ({'SHA-256' if args.hash else 'filename+size'} mode) · {args.db}")
    print("=" * 68)

    by_folder = defaultdict(lambda: [0, 0, 0])   # files, processed, bytes
    for r in files:
        b = by_folder[r["folder"]]
        b[0] += 1
        b[1] += 1 if r["processed"] else 0
        b[2] += r["size"]
    for folder, (n, proc, sz) in by_folder.items():
        flag = "" if proc == n else f"  ← {n - proc} UNPROCESSED"
        print(f"\n  {folder}\n    {n} video · {human(sz)} · processed {proc}/{n}{flag}")

    gaps = [r for r in files if not r["processed"]]
    print(f"\n  ── UNPROCESSED (coverage gap): {len(gaps)} file(s) ──")
    for r in gaps[:40]:
        print(f"    {r['path'].name}  ({human(r['size'])})  · {r['folder']}")
    if len(gaps) > 40:
        print(f"    … +{len(gaps) - 40} more")

    if args.hash:
        dups = {s: ps for s, ps in sha_locations.items() if len(ps) > 1}
        waste = sum((len(ps) - 1) * ps[0].stat().st_size for ps in dups.values())
        print(f"\n  ── DUPLICATES (byte-identical): {len(dups)} file(s) copied >1× · ~{human(waste)} reclaimable ──")
        for s, ps in list(dups.items())[:20]:
            print(f"    {ps[0].name}  ×{len(ps)}")
            for p in ps:
                print(f"        {p}")

    total = sum(r["size"] for r in files)
    print("\n" + "-" * 68)
    print(f"  {len(files)} video files · {human(total)} · "
          f"processed {sum(1 for r in files if r['processed'])} · unprocessed {len(gaps)}")
    if args.hash:
        print(f"  {len({r['sha'] for r in files})} unique by content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
