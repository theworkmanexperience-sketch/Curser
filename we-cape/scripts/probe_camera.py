#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Camera Probe (discovery / onboarding tool)

When the platform meets a camera it doesn't recognize, this turns the guesswork we
just lived through with DJI's AC-codes into one command. Point it at a file, a
folder, or a mounted card and it emits a **fingerprint** (structure, identity, time,
telemetry streams), a **coverage verdict** (does our identity already handle it, and
what's missing), and **paste-ready stubs** for the two extension points we already
have — `cameras.yaml` and `camera_folder_patterns`. So onboarding a new camera
becomes: run probe → read the gaps → paste the stub → add a test.

BOUNDARIES (deliberate):
  • NOT a telemetry decoder — it REPORTS that a djmd/gpmf/gps data stream exists and
    hands off to vendor tools; it does not parse IMU/GPS binary.
  • NOT a transcode tester — it reports codec/container as a proxy hint, nothing more.
  • NO engine coupling; read-only by DEFAULT. Writing cameras.yaml is opt-in (--add).
  • NO silent auto-registration — identity still defers unverified cameras to confirm.

Honest limits: exiftool/ffprobe read ~90% of consumer cameras; proprietary telemetry
needs vendor tools, and some cameras embed no useful identity — those land at
"brand only, confirm the model", never an invented name.

CLI:  python3 scripts/probe_camera.py <path> [--json] [--add] [--interactive]
stdlib only · zero network · read-only (except opt-in --add). exiftool + ffprobe are
optional and injectable (the tool degrades gracefully and says so when they're absent).
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import camera_identity as ci        # reuse the tolerant metadata reader + registry

MEDIA_EXTS = {"mp4", "mov", "m4v", "avi", "mxf", "mkv", "insv", "insp", "braw",
              "r3d", "dng", "cr3", "jpg", "jpeg", "heic", "png"}
SIDECAR_EXTS = {"srt", "lrv", "lrf", "thm", "gpx", "xml"}
SAMPLE_EXTS = MEDIA_EXTS | SIDECAR_EXTS
CARD_MARKERS = ("DCIM", "PRIVATE", "CLIPS", "XDROOT", "PANA", "MP_ROOT", "AVF_INFO")
# datetime tags, split by whether they're clock-independent (GPS) or the camera clock.
_DRIFT_FREE_TIME = ("GPSDateTime", "GPSDateStamp")
_CLOCK_TIME = ("DateTimeOriginal", "CreateDate", "MediaCreateDate", "TrackCreateDate",
               "CreationDate", "ModifyDate")
_TELEMETRY_HINTS = ("djmd", "gpmf", "gps", "meta", "tmcd", "text", "dvtm")


# ─────────────────────────────────────────────────────────────────────────────
# Runners (injectable; graceful when the tool is absent)
# ─────────────────────────────────────────────────────────────────────────────
def _exiftool(path):
    if not shutil.which("exiftool"):
        return ""
    try:
        return subprocess.run(["exiftool", "-s", "-G1", "-a", str(path)],
                              capture_output=True, text=True, timeout=30).stdout or ""
    except Exception:
        return ""


def _ffprobe(path):
    if not shutil.which("ffprobe"):
        return ""
    try:
        return subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "stream=index,codec_type,codec_name,width,height,avg_frame_rate:stream_tags=handler_name",
             "-of", "default=noprint_wrappers=1", str(path)],
            capture_output=True, text=True, timeout=30).stdout or ""
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# Pure signal extractors (unit-tested with injected text)
# ─────────────────────────────────────────────────────────────────────────────
def sample_files(path, n=8):
    """A file → [file]; a folder/card → the first n media files (sorted)."""
    p = Path(path)
    if p.is_file():
        return [p]
    if not p.is_dir():
        return []
    out = []
    for f in sorted(p.rglob("*")):
        if f.is_file() and f.suffix.lower().lstrip(".") in SAMPLE_EXTS \
                and not f.name.startswith("._") and f.name != ".DS_Store":
            out.append(f)
            if len(out) >= n:
                break
    return out


def structure_signals(paths, root=None):
    names = [p.name for p in paths]
    exts = sorted({p.suffix.lower().lstrip(".") for p in paths if p.suffix})
    markers = []
    if root and Path(root).is_dir():
        try:
            dirs = {e.name.upper() for e in Path(root).iterdir() if e.is_dir()}
            markers = sorted(dirs & {m.upper() for m in CARD_MARKERS})
        except OSError:
            pass
    sidecars = sorted({p.suffix.lower().lstrip(".") for p in paths
                       if p.suffix.lower().lstrip(".") in ("srt", "lrv", "lrf", "thm", "xml", "gpx")})
    return {"extensions": exts, "card_markers": markers, "filename_examples": names[:5],
            "filename_regex": _regex_from_names(names), "sidecars": sidecars}


def _regex_from_names(names):
    """Suggest a FAMILY_PATTERN regex from a filename: prefix kept, digit runs → \\d+."""
    if not names:
        return None
    stem = Path(names[0]).stem
    esc = re.escape(stem)
    esc = re.sub(r"\d+", lambda m: r"\d+", esc)      # collapse digit runs (fn repl = literal)
    return "^" + esc


def time_signals(exif_text):
    tags, drift, clock = {}, [], []
    for tag in _DRIFT_FREE_TIME + _CLOCK_TIME:
        v = _grep(exif_text, tag)
        if v:
            tags[tag] = v
            (drift if tag in _DRIFT_FREE_TIME else clock).append(tag)
    return {"tags": tags, "drift_free": drift, "camera_clock": clock}


def stream_signals(ffprobe_text):
    """Parse ffprobe blocks → codec/res/fps + any data/telemetry streams flagged."""
    blocks, cur = [], {}
    for line in (ffprobe_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("index=") and cur:
            blocks.append(cur); cur = {}
        if "=" in line:
            k, v = line.split("=", 1)
            cur[k.strip()] = v.strip()
    if cur:
        blocks.append(cur)
    video = next((b for b in blocks if b.get("codec_type") == "video"), {})
    data = [b for b in blocks if b.get("codec_type") == "data"]
    telem = []
    for b in blocks:
        blob = " ".join(str(x).lower() for x in b.values())
        for h in _TELEMETRY_HINTS:
            if h in blob and b.get("codec_type") in ("data", "subtitle"):
                telem.append({"codec": b.get("codec_name"), "handler": b.get("tag:handler_name") or b.get("handler_name"), "hint": h})
                break
    res = (f"{video.get('width')}x{video.get('height')}"
           if video.get("width") else None)
    return {"video_codec": video.get("codec_name"), "resolution": res,
            "fps": _fps(video.get("avg_frame_rate")), "data_streams": len(data),
            "telemetry": telem, "stream_count": len(blocks)}


def _fps(rate):
    if not rate or "/" not in rate:
        return rate
    a, b = rate.split("/")
    try:
        return round(int(a) / int(b), 2) if int(b) else None
    except ValueError:
        return rate


def _grep(text, tag):
    key = re.sub(r"\s+", "", tag).lower()
    for line in (text or "").splitlines():
        m = re.match(r"\s*(?:\[[^\]]*\]\s*)?([A-Za-z0-9 ]+?)\s*:\s*(.+?)\s*$", line)
        if m and re.sub(r"\s+", "", m.group(1)).lower() == key:
            val = m.group(2).strip()
            if val and val != "-":
                return val
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Coverage verdict + label suggestion
# ─────────────────────────────────────────────────────────────────────────────
def suggest_label(identity, brand, registry):
    """Smarter naming: canonical when known; brand+code when both present; and a clear
    'Unknown <Brand> - TODO confirm model' when only the brand is known (never a guess)."""
    matched = ci.registry_match(identity, registry) if identity else None
    if matched:
        return matched["label"], True                     # canonical, already known
    code = (identity or {}).get("model_code")
    model = (identity or {}).get("model")
    if brand and code:
        return f"{brand} {code} - TODO confirm model", False
    if brand and model:
        return f"{brand} {model} - TODO confirm model", False
    if brand:
        return f"Unknown {brand} - TODO confirm model", False
    return "Unknown camera - TODO confirm make/model", False


def coverage(identity, brand, filename_regex, registry, patterns):
    idn = ci.identify("", [], meta=identity or None, registry=registry)
    in_registry = ci.registry_match(identity, registry) is not None if identity else False
    gaps = []
    if not in_registry:
        gaps.append("serial/model_code not in cameras.yaml — add it (stub below)")
    if brand and not identity:
        gaps.append(f"identity is brand-only ({brand}); exact body unresolved — confirm the model")
    if not brand and not identity:
        gaps.append("no brand from filenames — add a camera_folder_patterns entry (line below)")
    return {"identify_status": idn["status"], "identify_label": idn["label"],
            "in_registry": in_registry, "brand": brand, "gaps": gaps}


# ─────────────────────────────────────────────────────────────────────────────
# Fingerprint
# ─────────────────────────────────────────────────────────────────────────────
def build_fingerprint(path, exif_runner=None, ffprobe_runner=None, registry=None, patterns=None):
    exif_runner = exif_runner or _exiftool
    ffprobe_runner = ffprobe_runner or _ffprobe
    registry = registry if registry is not None else ci.load_registry()
    files = sample_files(path)
    root = path if Path(path).is_dir() else str(Path(path).parent)
    struct = structure_signals(files, root)
    exif_text = exif_runner(files[0]) if files else ""
    ff_text = ffprobe_runner(files[0]) if files else ""
    identity = ci.serial_from_metadata(files[0], runner=lambda p: exif_text) if files else {}
    # brand from filenames (reliable) — else fall back to the exif Make tag (helps
    # a genuinely unknown camera that our filename patterns don't yet cover).
    brand = ci.brand_from_files([f.name for f in files]) or identity.get("make")
    times = time_signals(exif_text)
    streams = stream_signals(ff_text)
    label, known = suggest_label(identity, brand, registry)
    cov = coverage(identity, brand, struct["filename_regex"], registry, patterns)
    return {
        "path": str(path), "sampled": [f.name for f in files],
        "tools": {"exiftool": bool(shutil.which("exiftool")), "ffprobe": bool(shutil.which("ffprobe"))},
        "structure": struct, "identity": identity, "brand": brand,
        "time": times, "streams": streams, "coverage": cov,
        "suggested_label": label, "already_known": known,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Renders + stubs
# ─────────────────────────────────────────────────────────────────────────────
def cameras_yaml_stub(fp):
    idn = fp["identity"]
    lines = ["  - label: " + fp["suggested_label"],
             "    brand: " + (fp["brand"] or "TODO"),
             "    short: TODO"]
    if idn.get("serial"):
        lines.append("    serial: " + idn["serial"])
    if idn.get("model_code"):
        lines.append("    model_code: " + idn["model_code"])
    if idn.get("model"):
        lines.append("    device_name: " + idn["model"])
    return "\n".join(lines)


def family_pattern_line(fp):
    rx = fp["structure"]["filename_regex"]
    body = fp["suggested_label"]
    return f'(re.compile(r"{rx}", re.I), "{body}"),' if rx else None


def _next_step(fp):
    cov = fp["coverage"]
    if fp["already_known"] and cov["identify_status"] == "verified":
        return f"✓ Already recognized as {cov['identify_label']} — no action needed."
    if fp["identity"].get("serial") or fp["identity"].get("model_code"):
        return "Add this camera to cameras.yaml (paste the stub below, or re-run with --add)."
    if fp["brand"]:
        return ("Add a camera_folder_patterns line (below) for the filename, and a cameras.yaml "
                "stub — the exact model needs confirming.")
    return "Unrecognized — inspect the tags below; this camera may need vendor tools to decode."


def render_report(fp):
    L = [f"# Camera Probe — {fp['path']}", ""]
    L.append(f"➤ Recommended next step: {_next_step(fp)}")     # UX: action first
    L.append("")
    if not fp["tools"]["exiftool"]:
        L.append("⚠ exiftool not found — identity/time signals are limited. `brew install exiftool`.")
    if not fp["tools"]["ffprobe"]:
        L.append("⚠ ffprobe not found — stream/telemetry detection skipped. (ships with ffmpeg)")
    L.append(f"Sampled: {', '.join(fp['sampled']) or '(none)'}")
    s = fp["structure"]
    L.append("")
    L.append("## Structure")
    L.append(f"- Extensions: {', '.join(s['extensions']) or '—'}")
    L.append(f"- Card markers: {', '.join(s['card_markers']) or '—'}")
    L.append(f"- Sidecars: {', '.join(s['sidecars']) or '—'}")
    L.append(f"- Filename pattern: `{s['filename_regex'] or '—'}`")
    L.append("")
    L.append("## Identity")
    idn = fp["identity"]
    L.append(f"- Brand (from files): {fp['brand'] or '—'}")
    L.append(f"- Serial: {idn.get('serial','—')} · Model: {idn.get('model','—')} · "
             f"Code: {idn.get('model_code','—')}")
    L.append(f"- Suggested label: **{fp['suggested_label']}**")
    L.append("")
    L.append("## Time")
    t = fp["time"]
    L.append(f"- Drift-free (GPS): {', '.join(t['drift_free']) or '— none (relies on camera clock)'}")
    L.append(f"- Camera-clock: {', '.join(t['camera_clock']) or '—'}")
    L.append("")
    L.append("## Streams")
    st = fp["streams"]
    L.append(f"- Video: {st.get('video_codec','—')} {st.get('resolution','') or ''} "
             f"{('@'+str(st['fps'])+'fps') if st.get('fps') else ''}".rstrip())
    if st.get("telemetry"):
        hints = ", ".join(f"{x['hint']}({x.get('codec')})" for x in st["telemetry"])
        L.append(f"- **Telemetry stream(s) present: {hints}** — decode with vendor tools "
                 "(Telemetry Extractor / Gyroflow); this tool only flags presence.")
    else:
        L.append(f"- Data streams: {st.get('data_streams', 0)} (no telemetry hints matched)")
    L.append("")
    L.append("## Coverage")
    cov = fp["coverage"]
    L.append(f"- identify() → status **{cov['identify_status']}**"
             + (f", label {cov['identify_label']}" if cov['identify_label'] else ""))
    L.append(f"- In cameras.yaml: {'yes' if cov['in_registry'] else 'no'}")
    for g in cov["gaps"]:
        L.append(f"  - gap: {g}")
    if not fp["already_known"]:
        L.append("")
        L.append("## Paste-ready — cameras.yaml")
        L.append("```yaml")
        L.append(cameras_yaml_stub(fp))
        L.append("```")
        fpl = family_pattern_line(fp)
        if fpl:
            L.append("## Paste-ready — new_shoot FAMILY_PATTERNS / config camera_folder_patterns")
            L.append("```python")
            L.append(fpl)
            L.append("```")
    return "\n".join(L)


def add_to_cameras_yaml(fp, path=None):
    """Opt-in: append the stub to cameras.yaml (never automatic). Returns the path or
    None if the camera is already known (nothing to add)."""
    if fp["already_known"]:
        return None
    target = Path(path or ci.CAMERAS_YAML)
    stub = cameras_yaml_stub(fp)
    text = target.read_text() if target.exists() else "cameras:\n"
    if not text.rstrip().endswith(("cameras:",)) and "cameras:" not in text:
        text = "cameras:\n" + text
    target.write_text(text.rstrip() + "\n\n" + stub + "\n")
    return target


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def _cli(argv=None):
    ap = argparse.ArgumentParser(description="W.E. C.A.P.E. — probe an unknown camera's metadata.")
    ap.add_argument("path", help="a media file, a folder, or a mounted card")
    ap.add_argument("--json", action="store_true", help="emit the fingerprint as JSON")
    ap.add_argument("--add", action="store_true", help="append the cameras.yaml stub (opt-in write)")
    ap.add_argument("--interactive", action="store_true",
                    help="prompt to confirm/name the body before writing")
    args = ap.parse_args(argv)

    if not Path(args.path).exists():
        print(f"  path not found: {args.path}")
        return 1
    fp = build_fingerprint(args.path)
    if args.json:
        print(json.dumps(fp, indent=2))
    else:
        print(render_report(fp))
    if args.add:
        if args.interactive and not fp["already_known"]:
            ans = input(f"\nAdd '{fp['suggested_label']}' to cameras.yaml? [y/N] ").strip().lower()
            if ans != "y":
                print("  not added.")
                return 0
        p = add_to_cameras_yaml(fp)
        print(f"\n  ✓ appended stub to {p}" if p else "\n  (already known — nothing to add)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
