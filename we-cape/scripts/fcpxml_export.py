#!/usr/bin/env python3
"""
W.E. C.A.P.E. — FCPXML Export Bridge  (ops tooling, NOT the engine)

Turns a CAPTURE run's multicam GROUPS into a Final Cut Pro **multicam clip** per
group: each camera (DJI Osmo Action 5/6, Insta360 X5, …) becomes an angle, and
each clip is placed on its angle by the corrected-timestamp delta CAPTURE already
computed. One Event per shoot, one <mc-clip> per group.

Honest scope (say it out loud): v1 aligns angles by TIMESTAMP (±seconds, drift-
corrected from filenames), NOT by audio waveform. So FCP receives the right
cameras grouped together and roughly aligned — then you run FCP's "Synchronize
Clips" (or future J3) to lock audio to the frame. CAPTURE decides *what belongs
together*; FCP/J3 does the *frame-accurate* part.

Media (default --media both): each asset gets an <media-rep kind="original-media">
AND a <media-rep kind="proxy-media"> (the CAPTURE proxy), so FCP's Proxy/Optimized
toggle works — edit offline on proxies, conform to originals when the 10TB mounts.
Proxy paths are joined by SHA-256 (content.id) and survive across runs via the
registry's field-preserving upsert, so a no-proxy re-CAPTURE still links proxies.

Read-only on the registry. stdlib + ffprobe. Zero network.

Usage:
  python3 scripts/fcpxml_export.py --run WEF_20260630_125435_06980D
  python3 scripts/fcpxml_export.py --run <id> --media proxies --out ~/Desktop/shoot.fcpxml
  python3 scripts/fcpxml_export.py --run <id> --fps 30000/1001        # force sequence timebase
Then: import the .fcpxml into Final Cut Pro (File ▸ Import ▸ XML).
"""

import argparse
import json
import sqlite3
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

FCPXML_VERSION = "1.9"
DEFAULT_DB = Path.home() / ".wecape" / "registry" / "wecape.db"
DEFAULT_FPS = (30, 1)   # used only if nothing can be probed and no --fps given


# ── registry (read-only) ─────────────────────────────────────────────────────
def connect_ro(db_path):
    uri = f"file:{Path(db_path).resolve().as_posix()}?mode=ro"
    c = sqlite3.connect(uri, uri=True)
    c.row_factory = sqlite3.Row
    return c


def find_run(conn, run_id):
    r = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
    return dict(r) if r else None


def load_media_index(conn):
    """SHA-256 (content.id) -> media row. Spans ALL runs so proxies linked in a
    prior run are found for a no-proxy re-CAPTURE (P5 field-preserving upsert)."""
    idx = {}
    try:
        for r in conn.execute(
            "SELECT id, original_path, proxy_path, resolution, duration_sec, "
            "filename, codec FROM content"
        ):
            idx[r["id"]] = dict(r)
    except sqlite3.Error:
        pass
    return idx


# ── groups from the shoot's output folder ────────────────────────────────────
def load_groups(output_path):
    base = Path(output_path)
    groups = []
    if not base.is_dir():
        return groups
    for mj in sorted(base.glob("**/MULTICAM/*.json")):
        try:
            groups.append(json.loads(mj.read_text()))
        except Exception:
            pass
    return groups


# ── ffprobe (with graceful fallback to registry metadata) ────────────────────
def probe_media(path):
    """Return {width,height,fps_num,fps_den,duration_s,has_video,has_audio,
    audio_channels,audio_rate} or None if ffprobe is unavailable / file offline."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_streams", "-show_format", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode != 0:
            return None
        data = json.loads(out.stdout)
    except Exception:
        return None
    info = {"width": 0, "height": 0, "fps_num": 0, "fps_den": 1, "duration_s": 0.0,
            "has_video": False, "has_audio": False, "audio_channels": 0, "audio_rate": 0}
    for s in data.get("streams", []):
        if s.get("codec_type") == "video" and not info["has_video"]:
            info["has_video"] = True
            info["width"] = int(s.get("width") or 0)
            info["height"] = int(s.get("height") or 0)
            rate = s.get("r_frame_rate") or s.get("avg_frame_rate") or "0/1"
            try:
                n, d = rate.split("/")
                info["fps_num"], info["fps_den"] = int(n), int(d or 1)
            except Exception:
                pass
        elif s.get("codec_type") == "audio" and not info["has_audio"]:
            info["has_audio"] = True
            info["audio_channels"] = int(s.get("channels") or 0)
            try:
                info["audio_rate"] = int(s.get("sample_rate") or 0)
            except Exception:
                pass
    try:
        info["duration_s"] = float(data.get("format", {}).get("duration") or 0.0)
    except Exception:
        pass
    if not info["fps_num"] or not info["fps_den"]:
        info["fps_num"], info["fps_den"] = 0, 1   # signal: unknown fps
    return info


# ── time helpers (frame-conformed rational time, FCPXML "N/Ds") ──────────────
def _t(secs, fps_num, fps_den):
    """Seconds -> (timestring, frames) conformed to the given fps."""
    frames = int(round(secs * fps_num / fps_den)) if fps_num else 0
    fr = Fraction(frames * fps_den, fps_num) if fps_num else Fraction(0)
    s = f"{fr.numerator}/{fr.denominator}s" if fr.denominator != 1 else f"{fr.numerator}s"
    return s, frames


def _framedur(fps_num, fps_den):
    fr = Fraction(fps_den, fps_num)
    return f"{fr.numerator}/{fr.denominator}s" if fr.denominator != 1 else f"{fr.numerator}s"


def _esc(x):
    return (str(x).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _uri(path):
    p = Path(path)
    try:
        return p.as_uri()                      # absolute -> file:///... (encodes spaces)
    except ValueError:
        return "file://" + _esc(str(p))         # relative fallback (shouldn't happen)


# ── build ────────────────────────────────────────────────────────────────────
def build_fcpxml(event_name, groups, media_index, probe=probe_media,
                 seq_fps=None, media_mode="both"):
    """Return (xml_str, stats). Pure-ish: `probe` is injectable for tests."""
    stats = {"groups": 0, "angles": 0, "clips": 0, "assets": 0, "fallback": 0, "missing": 0}

    # 1) Resolve every clip across all groups.
    clips = []          # {group_id, sha, camera, delta, original, proxy, fmt}
    probe_cache = {}
    for g in groups:
        gid = g.get("group_id") or "group"
        for f in g.get("files", []):
            sha = f.get("file_hash_sha256") or ""
            original = f.get("path") or (media_index.get(sha, {}).get("original_path"))
            if not original:
                stats["missing"] += 1
                continue
            row = media_index.get(sha, {})
            proxy = row.get("proxy_path")
            # format: probe original (cache), else registry resolution + assumed fps
            if original not in probe_cache:
                probe_cache[original] = probe(original)
            pr = probe_cache[original]
            if pr and pr["width"]:
                fmt = pr
            else:
                stats["fallback"] += 1
                w = h = 0
                res = (row.get("resolution") or "")
                if "x" in res:
                    try:
                        w, h = (int(v) for v in res.lower().split("x")[:2])
                    except Exception:
                        w = h = 0
                fmt = {"width": w, "height": h, "fps_num": 0, "fps_den": 1,
                       "duration_s": float(row.get("duration_sec") or 0.0),
                       "has_video": True, "has_audio": True,
                       "audio_channels": 2, "audio_rate": 48000}
            clips.append({"group_id": gid, "sha": sha or original,
                          "camera": f.get("camera_source") or "Unknown",
                          "delta": float(f.get("timestamp_delta_seconds") or 0.0),
                          "original": original, "proxy": proxy, "fmt": fmt})

    # 2) Sequence timebase: explicit --fps, else the most common probed fps, else default.
    if seq_fps:
        seq_num, seq_den = seq_fps
    else:
        counts = {}
        for c in clips:
            fn, fd = c["fmt"]["fps_num"], c["fmt"]["fps_den"]
            if fn:
                counts[(fn, fd)] = counts.get((fn, fd), 0) + 1
        seq_num, seq_den = (max(counts, key=counts.get) if counts else DEFAULT_FPS)

    # 3) Allocate resource ids; dedupe formats and assets.
    rid = [0]
    def _rid():
        rid[0] += 1
        return f"r{rid[0]}"

    formats = {}        # (w,h,num,den) -> id
    def format_id(w, h, num, den):
        num = num or seq_num
        den = den or seq_den
        key = (w, h, num, den)
        if key not in formats:
            fid = _rid()
            formats[key] = (fid,
                f'<format id="{fid}" name="FFVideoFormat{w}x{h}p{round((num/den) if den else 0)}" '
                f'frameDuration="{_framedur(num, den)}" width="{w or 1920}" height="{h or 1080}" '
                f'colorSpace="1-1-1 (Rec. 709)"/>')
        return formats[key][0]

    assets = {}         # sha -> (id, xml)
    def asset_id(c):
        sha = c["sha"]
        if sha in assets:
            return assets[sha][0]
        fm = c["fmt"]
        fid = format_id(fm["width"], fm["height"], fm["fps_num"], fm["fps_den"])
        dur, _ = _t(fm["duration_s"], fm["fps_num"] or seq_num, fm["fps_den"] or seq_den)
        aid = _rid()
        name = Path(c["original"]).stem
        audio = ""
        if fm.get("has_audio"):
            audio = (f' audioSources="1" audioChannels="{fm.get("audio_channels") or 2}"'
                     f' audioRate="{fm.get("audio_rate") or 48000}"')
        reps = []
        if media_mode in ("both", "originals"):
            reps.append(f'<media-rep kind="original-media" src="{_esc(_uri(c["original"]))}"/>')
        if media_mode in ("both", "proxies") and c.get("proxy"):
            reps.append(f'<media-rep kind="proxy-media" src="{_esc(_uri(c["proxy"]))}"/>')
        if not reps:    # proxies-only but no proxy on file -> fall back to original
            reps.append(f'<media-rep kind="original-media" src="{_esc(_uri(c["original"]))}"/>')
        xml = (f'<asset id="{aid}" name="{_esc(name)}" start="0s" duration="{dur}" '
               f'hasVideo="1" videoSources="1" hasAudio="{1 if fm.get("has_audio") else 0}"'
               f'{audio} format="{fid}">' + "".join(reps) + "</asset>")
        assets[sha] = (aid, xml)
        stats["assets"] += 1
        return aid

    # 4) Build one <media><multicam> per group + the <mc-clip> that references it.
    media_xml, event_items = [], []
    for g in groups:
        gid = g.get("group_id") or "group"
        gclips = [c for c in clips if c["group_id"] == gid]
        if not gclips:
            continue
        stats["groups"] += 1
        base_delta = min(c["delta"] for c in gclips)     # normalize earliest -> 0
        by_cam = {}
        for c in gclips:
            by_cam.setdefault(c["camera"], []).append(c)

        angles, group_end_s = [], 0.0
        ai = 0
        for cam, cs in by_cam.items():
            ai += 1
            stats["angles"] += 1
            angle_clips = []
            for c in sorted(cs, key=lambda x: x["delta"]):
                stats["clips"] += 1
                aid = asset_id(c)
                off_s = c["delta"] - base_delta
                off, _ = _t(off_s, seq_num, seq_den)
                dur_s = c["fmt"]["duration_s"] or 0.0
                dur, _ = _t(dur_s, seq_num, seq_den)
                group_end_s = max(group_end_s, off_s + dur_s)
                angle_clips.append(
                    f'<asset-clip ref="{aid}" offset="{off}" name="{_esc(Path(c["original"]).stem)}" '
                    f'duration="{dur}" format="{format_id(c["fmt"]["width"], c["fmt"]["height"], c["fmt"]["fps_num"], c["fmt"]["fps_den"])}"/>')
            angles.append(f'<mc-angle name="{_esc(cam)}" angleID="A{ai}">' + "".join(angle_clips) + "</mc-angle>")

        mid = _rid()
        seq_fmt = format_id(gclips[0]["fmt"]["width"], gclips[0]["fmt"]["height"], seq_num, seq_den)
        gdur, _ = _t(group_end_s, seq_num, seq_den)
        media_xml.append(
            f'<media id="{mid}" name="MC_{_esc(gid)}">'
            f'<multicam format="{seq_fmt}" tcStart="0s" tcFormat="NDF">' + "".join(angles) +
            "</multicam></media>")
        # NOTE: the FCPXML DTD does NOT allow 'format'/'tcFormat' on <mc-clip>
        # (FCP rejects them — DTD validation error). The format/timecode live on
        # the referenced <multicam>; mc-clip derives from it.
        event_items.append(
            f'<mc-clip ref="{mid}" name="MC_{_esc(gid)}" duration="{gdur}"/>')

    # 5) Assemble. Formats first, then assets, then media (FCPXML resource order).
    res = ([v[1] for v in formats.values()]
           + [v[1] for v in assets.values()]
           + media_xml)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n'
        f'<fcpxml version="{FCPXML_VERSION}">\n'
        "  <resources>\n    " + "\n    ".join(res) + "\n  </resources>\n"
        "  <library>\n"
        f'    <event name="{_esc(event_name)}">\n      ' + "\n      ".join(event_items) +
        "\n    </event>\n  </library>\n</fcpxml>\n")
    return xml, stats


# ── CLI ──────────────────────────────────────────────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(description="Export a CAPTURE run's multicam groups to FCPXML.")
    ap.add_argument("--run", required=True, help="run_id to export (see the dashboard / registry)")
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--out", type=Path, help="output .fcpxml (default: <shoot>_multicam.fcpxml)")
    ap.add_argument("--media", choices=["both", "proxies", "originals"], default="both")
    ap.add_argument("--fps", help="force sequence timebase, e.g. 30000/1001 or 30")
    ap.add_argument("--event", help="override the Event name (default: shoot folder name)")
    args = ap.parse_args(argv)

    if not args.db.exists():
        raise SystemExit(f"Registry not found: {args.db}")
    conn = connect_ro(args.db)
    try:
        run = find_run(conn, args.run)
        if not run:
            raise SystemExit(f"Run not found in registry: {args.run}")
        output_path = run.get("output_path") or ""
        groups = load_groups(output_path)
        if not groups:
            raise SystemExit(
                f"No MULTICAM/*.json under {output_path!r}. Is the shoot's output drive mounted, "
                "and did this run form groups?")
        media_index = load_media_index(conn)
    finally:
        conn.close()

    seq_fps = None
    if args.fps:
        n, _, d = args.fps.partition("/")
        seq_fps = (int(n), int(d or 1))

    event_name = args.event or (Path(output_path).name or args.run)
    xml, stats = build_fcpxml(event_name, groups, media_index,
                              seq_fps=seq_fps, media_mode=args.media)

    out = args.out or Path(f"{event_name}_multicam.fcpxml")
    Path(out).write_text(xml, encoding="utf-8")
    print(f"✓ FCPXML written: {Path(out).resolve()}")
    print(f"  {stats['groups']} multicam clip(s) · {stats['angles']} angle(s) · "
          f"{stats['clips']} clip placement(s) · {stats['assets']} asset(s)")
    if stats["fallback"]:
        print(f"  ⚠ {stats['fallback']} clip(s) used registry metadata (ffprobe unavailable/offline) "
              f"— fps assumed; verify timing in FCP.")
    if stats["missing"]:
        print(f"  ⚠ {stats['missing']} file(s) had no resolvable path — skipped.")
    print(f"  Media: {args.media}. Import via FCP ▸ File ▸ Import ▸ XML, then 'Synchronize Clips' to lock audio.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
