#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Verified Card Offload  (the Hedge-style front end)

Pulls a camera card into the per-camera folder structure CAPTURE expects, with
**checksum-verified** copies and an optional **second destination** — so "no asset
exists until it exists in two locations" (Principle #1) is true the moment offload
finishes, before CAPTURE ever runs.

What it does:
  • copies every file from the card to  <dest>/<shoot>/<camera>/…  (preserving the
    card's subfolders), and to <dest2>/… too if given;
  • verifies EACH copy by SHA-256 against the source (re-reads the written file —
    a copy that didn't land byte-for-byte is a hard failure, not a silent pass);
  • is resumable: a file already present with a matching hash is skipped;
  • writes a JSON manifest (every file + hash + verification result);
  • NEVER deletes or modifies the card. You format it yourself, only after the
    summary says every file verified in every destination.

The <camera> label should match CAPTURE's camera_folder_patterns so the body is
identified downstream: "DJI ACTION 5", "DJI ACTION 6", "Insta360 X5".

Usage:
  python3 scripts/offload_cards.py --source /Volumes/DJIAction6 \\
      --camera "DJI ACTION 6" --shoot "O-SIX_2026" \\
      --dest "/Volumes/10TB" --dest2 "/Volumes/Got My BackUP/cards"
  python3 scripts/offload_cards.py --source /Volumes/CARD --camera "Insta360 X5" \\
      --shoot Wedding_2026 --dest /Volumes/10TB --dry-run

stdlib only · zero network · read-only on the source.
"""

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

KNOWN_CAMERAS = ("DJI ACTION 5", "DJI ACTION 6", "Insta360 X5", "OM System OM-1")

# ── shoot manifest (shoot.yaml) — human context for the Production Health Report ──
# Written at offload (the one moment the operator is present), travels with the
# footage, read by health_report.py at report time. Influences report FRAMING only,
# never pipeline output (P1). stdlib-only mini-YAML — matches the SPEC §3 shape and
# health_report.load_trusted_clock's line parser.
MANIFEST_NAME = "shoot.yaml"
_MANIFEST_ORDER = ["shoot_name", "shoot_date", "location", "event",
                   "cameras", "trusted_clock", "notes"]


def parse_manifest(text):
    """Tolerant mini-YAML → dict. Only the flat `key: value` + `cameras: [a, b]`
    shapes this tool writes; unknown lines are ignored."""
    data = {}
    for line in (text or "").splitlines():
        m = re.match(r"\s*([A-Za-z_]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
        if key == "cameras":
            inner = val.strip().lstrip("[").rstrip("]")
            data["cameras"] = [c.strip().strip('"').strip("'")
                               for c in inner.split(",") if c.strip()]
        elif val:
            data[key] = val
    return data


def render_manifest(data):
    lines = ["# W.E. C.A.P.E. shoot manifest — human context for the Production Health Report.",
             "# Optional; influences report framing only, never pipeline output (P1)."]
    for key in _MANIFEST_ORDER:
        if key == "cameras":
            cams = data.get("cameras") or []
            if cams:
                lines.append("cameras: [" + ", ".join(cams) + "]")
        elif data.get(key):
            lines.append(f"{key}: {data[key]}")
    return "\n".join(lines) + "\n"


def merge_manifest(existing_text, updates):
    """Merge new fields into an existing manifest (idempotent per camera): scalar
    fields overwrite when provided; the current camera is appended to `cameras` so
    offloading each card in turn builds up the full camera list."""
    data = parse_manifest(existing_text)
    camera = updates.pop("_camera", None)
    for k, v in updates.items():
        if v:
            data[k] = v
    if camera:
        cams = data.get("cameras") or []
        if camera not in cams:
            cams.append(camera)
        data["cameras"] = cams
    return render_manifest(data)


def write_shoot_manifest(shoot_root, camera, fields):
    """Create/update <shoot_root>/shoot.yaml, folding in this camera + fields."""
    path = Path(shoot_root) / MANIFEST_NAME
    existing = path.read_text() if path.exists() else ""
    updates = dict(fields)
    updates["_camera"] = camera
    path.write_text(merge_manifest(existing, updates))
    return path
CRUFT_NAMES = {".DS_Store"}
CRUFT_DIRS = {".Spotlight-V100", ".Trashes", ".fseventsd",
              ".DocumentRevisions-V100", ".TemporaryItems"}
CHUNK = 8 * 1024 * 1024


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def human(n):
    n = float(n or 0)
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or u == "TB":
            return f"{n:.1f} {u}"
        n /= 1024


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def is_cruft(p: Path):
    if p.name in CRUFT_NAMES or p.name.startswith("._"):
        return True
    return any(part in CRUFT_DIRS for part in p.parts)


def list_source(root: Path, exts):
    if root.is_file():
        return root.parent, [root]
    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or is_cruft(p):
            continue
        if exts and p.suffix.lower().lstrip(".") not in exts:
            continue
        files.append(p)
    return root, files


def copy_verify(src, dst, src_hash):
    """Copy src->dst (mkdir parents) and verify dst hash == src_hash. Returns (ok, dst_hash, skipped)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size == src.stat().st_size:
        if sha256(dst) == src_hash:                 # already there & verified -> resume-skip
            return True, src_hash, True
    shutil.copy2(src, dst)
    dh = sha256(dst)
    return (dh == src_hash), dh, False


def main(argv=None):
    ap = argparse.ArgumentParser(description="Verified camera-card offload into CAPTURE's per-camera folders.")
    ap.add_argument("--source", required=True, help="card mount or folder (read-only)")
    ap.add_argument("--camera", required=True, help='per-camera label, e.g. "DJI ACTION 6"')
    ap.add_argument("--shoot", required=True, help="shoot name (top folder under each destination)")
    ap.add_argument("--dest", required=True, help="primary destination root (e.g. /Volumes/10TB)")
    ap.add_argument("--dest2", help="optional second destination root (true two-copy safety)")
    ap.add_argument("--ext", help="comma-separated extension allowlist (default: copy everything)")
    ap.add_argument("--dry-run", action="store_true", help="show what would copy; write nothing")
    # ── shoot manifest fields (all optional) — written to shoot.yaml beside the footage ──
    ap.add_argument("--trusted-clock",
                    help='the camera whose clock is authoritative (e.g. "DJI Osmo Action 6"); '
                         "lets the Health Report name the culprit definitively")
    ap.add_argument("--shoot-date", help="the true shoot date, if known (YYYY-MM-DD)")
    ap.add_argument("--location", help="free-text location (e.g. 'Kansas City, MO')")
    ap.add_argument("--event", help="free-text event name")
    ap.add_argument("--notes", help="free-text notes (e.g. 'Insta360 clock was not reset')")
    args = ap.parse_args(argv)

    manifest_fields = {"shoot_name": args.shoot, "shoot_date": args.shoot_date,
                       "location": args.location, "event": args.event,
                       "trusted_clock": args.trusted_clock, "notes": args.notes}
    want_manifest = any(v for k, v in manifest_fields.items() if k != "shoot_name")

    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"✗ source not found: {source}")
    if not any(k.lower() in args.camera.lower() for k in KNOWN_CAMERAS):
        print(f"⚠ camera label {args.camera!r} matches none of {KNOWN_CAMERAS} — "
              f"CAPTURE may not resolve the specific body. Continuing anyway.")

    exts = None
    if args.ext:
        exts = {e.strip().lower().lstrip(".") for e in args.ext.split(",") if e.strip()}

    root, files = list_source(source, exts)
    if not files:
        raise SystemExit(f"✗ no files to offload under {source}")

    roots = [Path(args.dest)] + ([Path(args.dest2)] if args.dest2 else [])
    for r in roots:
        if not r.exists():
            raise SystemExit(f"✗ destination drive not mounted: {r}")
    dests = [r / args.shoot / args.camera for r in roots]

    total_bytes = sum(f.stat().st_size for f in files)
    print("════════════════════════════════════════════════════════════")
    print("  W.E. C.A.P.E. — Verified Card Offload")
    print(f"  Source : {source}")
    print(f"  Camera : {args.camera}   Shoot: {args.shoot}")
    for i, d in enumerate(dests):
        print(f"  Dest {i+1} : {d}")
    print(f"  Files  : {len(files)}  ·  {human(total_bytes)}")
    print("════════════════════════════════════════════════════════════")

    if args.dry_run:
        for f in files:
            print(f"  would copy  {f.relative_to(root)}  ({human(f.stat().st_size)})")
        if want_manifest:
            preview = render_manifest(merge_manifest("", {**manifest_fields, "_camera": args.camera}))
            print(f"\n  would write {MANIFEST_NAME} to each shoot root:")
            for line in preview.splitlines():
                print(f"    {line}")
        print(f"\n(dry-run) {len(files)} file(s), {human(total_bytes)} -> {len(dests)} destination(s). Nothing written.")
        return 0

    manifest = {"tool": "offload_cards", "version": 1, "created": _now(),
                "source": str(source), "camera": args.camera, "shoot": args.shoot,
                "destinations": [str(d) for d in dests], "files": []}
    copied = skipped = mismatched = 0
    done_bytes = 0

    for f in files:
        rel = f.relative_to(root)
        size = f.stat().st_size
        src_hash = sha256(f)
        rec = {"relpath": str(rel), "size": size, "sha256": src_hash,
               "verified": [], "copied_at": _now()}
        file_ok = True
        states = []
        for d in dests:
            ok, dh, was_skipped = copy_verify(f, d / rel, src_hash)
            rec["verified"].append({"dest": str(d / rel), "ok": ok, "resumed": was_skipped})
            states.append("skip" if was_skipped else ("ok" if ok else "MISMATCH"))
            if not ok:
                file_ok = False
        manifest["files"].append(rec)
        done_bytes += size
        if not file_ok:
            mismatched += 1
            print(f"  ✗ MISMATCH  {rel}  — copy did NOT verify; do NOT trust this destination.")
        elif all(s == "skip" for s in states):
            skipped += 1
        else:
            copied += 1
        pct = 100 * done_bytes / total_bytes if total_bytes else 100
        print(f"  [{pct:5.1f}%] {rel}  ({human(size)})  [{' · '.join(states)}]")

    manifest["summary"] = {"files": len(files), "copied": copied, "resumed": skipped,
                           "mismatched": mismatched, "bytes": total_bytes}
    for d in dests:
        try:
            (d).mkdir(parents=True, exist_ok=True)
            (d / "_offload_manifest.json").write_text(json.dumps(manifest, indent=2))
        except OSError:
            pass

    print("────────────────────────────────────────────────────────────")
    print(f"  copied {copied} · resumed/verified {skipped} · MISMATCH {mismatched} · {human(total_bytes)}")
    print(f"  manifest: {dests[0] / '_offload_manifest.json'}")
    if mismatched:
        print(f"  ✗ {mismatched} file(s) FAILED verification — re-run to retry. DO NOT format the card.")
        return 1
    print("  ✓ every file verified in every destination.")
    if want_manifest:
        for shoot_root in dict.fromkeys(d.parent for d in dests):   # unique, order-preserving
            try:
                mp = write_shoot_manifest(shoot_root, args.camera, manifest_fields)
                print(f"  ✓ shoot manifest: {mp}"
                      + (f"  (trusted_clock: {args.trusted_clock})" if args.trusted_clock else ""))
            except OSError:
                print(f"  ⚠ could not write {MANIFEST_NAME} to {shoot_root}")
    print("  Safe to format the card now (your call — the tool never touches it).")
    print(f"  Next: python3 -m wecape --input \"{dests[0].parent}\" --output <OUTPUT> --proxy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
