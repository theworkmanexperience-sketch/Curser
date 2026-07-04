#!/usr/bin/env python3
"""
W.E. C.A.P.E. — .SRT Sidecar Telemetry  (Phase 1: GPS + drift-free time)

DJI/Osmo cameras drop a `.SRT` subtitle sidecar next to each clip carrying, per
timecode, the camera's real record-time datetime and (when a GPS lock exists) GPS
coordinates. This read-only post-processor parses those sidecars and stores the
result in a SEPARATE telemetry store — NOT the deterministic registry.

Why separate (see SPEC_SRT_Telemetry.md §5): telemetry is enrichment, not pipeline
truth (P1); GPS is location PII kept full-fidelity only in this creator-owned local
store (P7) and hashed/omitted on egress (D1). It joins the registry read-only by the
clip's content SHA-256. Telemetry is regenerable from the .SRT files.

CLI:
  python3 scripts/srt_telemetry.py scan  <folder|.SRT> [more…]   # parse + store
  python3 scripts/srt_telemetry.py show  <content_sha|key>       # one clip
  python3 scripts/srt_telemetry.py list  [--limit N]             # all clips

stdlib only · zero network · never mutates footage.
"""

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

PARSER_VERSION = "1"
TELEMETRY_DB = Path.home() / ".wecape" / "telemetry.db"
REGISTRY_DB = Path.home() / ".wecape" / "registry" / "wecape.db"
VIDEO_EXTS = (".mp4", ".mov", ".m4v", ".insv", ".avi", ".mkv")
CHUNK = 8 * 1024 * 1024

# ── tolerant parse patterns (format varies by model/firmware) ────────────────
_DT_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})")
_LAT_RE = re.compile(r"latitude\s*[:=]\s*(-?\d+\.\d+)", re.I)
_LON_RE = re.compile(r"longitude\s*[:=]\s*(-?\d+\.\d+)", re.I)
_ALT_RE = re.compile(r"(?:abs_alt|altitude)\s*[:=]?\s*(-?\d+\.?\d*)", re.I)
# Paren form (some DJI drones): GPS(longitude,latitude,altitude) — NOTE the order
# is lon,lat and is firmware-dependent; labeled form above is authoritative and is
# what Osmo Action 5/6 emit. Validate paren order against real footage before trust.
_GPS_PAREN = re.compile(r"GPS\s*\(?\s*(-?\d+\.\d+)[,\s]+(-?\d+\.\d+)", re.I)


def parse_srt(text):
    """Pure, tolerant parse. Returns start/end record-time (camera-LOCAL wall clock,
    not UTC), a representative GPS fix (or None), and how many samples were seen.
    MUST NOT fail a clip that has time but no GPS."""
    times = [f"{y}-{mo}-{d}T{h}:{mi}:{s}"
             for (y, mo, d, h, mi, s) in _DT_RE.findall(text)]
    lat = lon = alt = None
    for line in text.splitlines():
        if lat is None:
            la, lo = _LAT_RE.search(line), _LON_RE.search(line)
            if la and lo:
                lat, lon = float(la.group(1)), float(lo.group(1))
            else:
                g = _GPS_PAREN.search(line)
                if g:                                  # GPS(lon, lat, …)
                    lon, lat = float(g.group(1)), float(g.group(2))
        if alt is None:
            a = _ALT_RE.search(line)
            if a:
                try:
                    alt = float(a.group(1))
                except ValueError:
                    pass
        if lat is not None and alt is not None:
            break
    if lat is not None and not (-90 <= lat <= 90 and -180 <= lon <= 180):
        lat = lon = None                               # reject an impossible fix
    return {"start_time": times[0] if times else None,
            "end_time": times[-1] if times else None,
            "gps_lat": lat, "gps_lon": lon, "gps_alt": alt,
            "sample_count": len(times)}


# ── I/O edges ────────────────────────────────────────────────────────────────
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(CHUNK), b""):
            h.update(b)
    return h.hexdigest()


def _path_hash(path):
    return "sha256:" + hashlib.sha256(str(path).encode()).hexdigest()


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_sibling_video(srt_path):
    """The video clip next to the .SRT (same stem), case-insensitive."""
    srt_path = Path(srt_path)
    stem = srt_path.stem.lower()
    try:
        for f in srt_path.parent.iterdir():
            if f.is_file() and f.suffix.lower() in VIDEO_EXTS and f.stem.lower() == stem:
                return f
    except OSError:
        pass
    return None


def lookup_run_id(content_sha, registry=REGISTRY_DB):
    reg = Path(registry)
    if not content_sha or not reg.exists():
        return None
    try:
        con = sqlite3.connect(f"file:{reg.resolve().as_posix()}?mode=ro", uri=True)
        row = con.execute("SELECT run_id FROM content WHERE id=? LIMIT 1", (content_sha,)).fetchone()
        con.close()
        return row[0] if row else None
    except sqlite3.Error:
        return None


def _db(path=TELEMETRY_DB):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(path))
    con.execute("""CREATE TABLE IF NOT EXISTS telemetry(
        key TEXT PRIMARY KEY, content_sha TEXT, run_id TEXT, srt_path_hash TEXT,
        start_time TEXT, end_time TEXT, gps_lat REAL, gps_lon REAL, gps_alt REAL,
        sample_count INTEGER, parser_version TEXT, updated_at TEXT)""")
    con.execute("CREATE INDEX IF NOT EXISTS ix_sha ON telemetry(content_sha)")
    return con


def _iter_srt(paths):
    for p in paths:
        p = Path(p)
        if p.is_dir():
            yield from sorted(x for x in p.rglob("*") if x.suffix.lower() == ".srt")
        elif p.suffix.lower() == ".srt":
            yield p


def scan(paths, db=TELEMETRY_DB, registry=REGISTRY_DB, hash_video=True):
    """Parse every .SRT under `paths`, link to its clip's content SHA, upsert to the
    telemetry store. Idempotent (re-scan updates the same key)."""
    con = _db(db)
    n = linked = with_gps = skipped = 0
    for srt in _iter_srt(paths):
        try:
            data = parse_srt(srt.read_text(errors="ignore"))
        except OSError:
            continue
        if data["start_time"] is None:
            skipped += 1              # no camera datetime → a caption/subtitle .SRT, not telemetry
            continue
        vid = find_sibling_video(srt)
        content_sha = sha256_file(vid) if (vid and hash_video) else None
        run_id = lookup_run_id(content_sha, registry)
        key = content_sha or ("srt:" + hashlib.sha256(str(srt).encode()).hexdigest())
        con.execute("""INSERT INTO telemetry
            (key, content_sha, run_id, srt_path_hash, start_time, end_time,
             gps_lat, gps_lon, gps_alt, sample_count, parser_version, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(key) DO UPDATE SET
             content_sha=excluded.content_sha, run_id=excluded.run_id,
             srt_path_hash=excluded.srt_path_hash, start_time=excluded.start_time,
             end_time=excluded.end_time, gps_lat=excluded.gps_lat,
             gps_lon=excluded.gps_lon, gps_alt=excluded.gps_alt,
             sample_count=excluded.sample_count, parser_version=excluded.parser_version,
             updated_at=excluded.updated_at""",
            (key, content_sha, run_id, _path_hash(srt), data["start_time"], data["end_time"],
             data["gps_lat"], data["gps_lon"], data["gps_alt"], data["sample_count"],
             PARSER_VERSION, _now()))
        n += 1
        linked += 1 if content_sha else 0
        with_gps += 1 if data["gps_lat"] is not None else 0
    con.commit()
    con.close()
    return {"srt_files": n, "linked_to_clip": linked, "with_gps": with_gps,
            "skipped_non_telemetry": skipped}


def _fetch(db, where, arg):
    con = _db(db)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(f"SELECT * FROM telemetry {where}", arg)]
    con.close()
    return rows


# ── CLI ──────────────────────────────────────────────────────────────────────
def _cli(argv=None):
    ap = argparse.ArgumentParser(description="W.E. C.A.P.E. — .SRT sidecar telemetry (GPS + drift-free time).")
    ap.add_argument("--db", default=str(TELEMETRY_DB), help="telemetry store (default ~/.wecape/telemetry.db)")
    sub = ap.add_subparsers(dest="cmd")

    sc = sub.add_parser("scan", help="parse .SRT sidecars under folder(s) and store")
    sc.add_argument("paths", nargs="+", help="folders or .SRT files")
    sc.add_argument("--registry", default=str(REGISTRY_DB), help="registry for run_id linkage (read-only)")
    sc.add_argument("--no-hash-video", action="store_true", help="skip hashing sibling clips (no registry link)")

    sh = sub.add_parser("show", help="show one clip's telemetry (by content_sha or key)")
    sh.add_argument("id")

    ls = sub.add_parser("list", help="list stored telemetry")
    ls.add_argument("--limit", type=int, default=50)
    ls.add_argument("--gps-only", action="store_true", help="only rows with a GPS fix")

    args = ap.parse_args(argv)

    if args.cmd == "scan":
        r = scan(args.paths, db=args.db, registry=args.registry, hash_video=not args.no_hash_video)
        print(f"  ✓ {r['srt_files']} telemetry .SRT stored · {r['linked_to_clip']} linked to a clip · "
              f"{r['with_gps']} with GPS · {r['skipped_non_telemetry']} skipped (caption/subtitle)"
              f"  ->  {args.db}")
        return 0

    if args.cmd == "show":
        rows = _fetch(args.db, "WHERE content_sha=? OR key=?", (args.id, args.id))
        if not rows:
            print("  (no telemetry for that id)")
            return 1
        print(json.dumps(rows[0], indent=2))
        return 0

    if args.cmd == "list":
        where = "WHERE gps_lat IS NOT NULL " if args.gps_only else ""
        rows = _fetch(args.db, where + "ORDER BY start_time LIMIT ?", (args.limit,))
        if not rows:
            print("  (telemetry store empty — run 'scan' first)")
            return 0
        for r in rows:
            sha = (r["content_sha"] or r["key"])[:16]
            gps = f"{r['gps_lat']:.5f},{r['gps_lon']:.5f}" if r["gps_lat"] is not None else "no-gps"
            print(f"  {sha}  {r['start_time'] or '?':<19}  {gps:<22}  n={r['sample_count']}")
        print(f"\n  {len(rows)} row(s). GPS shown in full locally (creator-owned; redact on egress — D1).")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
