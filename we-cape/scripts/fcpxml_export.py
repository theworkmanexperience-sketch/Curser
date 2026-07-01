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
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
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
        # SELECT * so a schema variant (a missing/renamed column) never makes this
        # silently return empty — downstream reads are all .get()-guarded.
        for r in conn.execute("SELECT * FROM content"):
            row = dict(r)
            if row.get("id"):
                idx[row["id"]] = row
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


def load_ungrouped(output_path, run_id):
    """Ungrouped camera files for this run, from <run_id>_index.json (authoritative
    per-run list — avoids cross-run registry ambiguity). Returns a list of paths."""
    base = Path(output_path)
    idx = base / f"{run_id}_index.json"
    if not idx.exists():
        hits = list(base.glob(f"**/{run_id}_index.json"))
        idx = hits[0] if hits else None
    if not idx or not idx.exists():
        return []
    try:
        data = json.loads(idx.read_text())
    except Exception:
        return []
    return [e.get("file") for e in data.get("ungrouped_camera_files", []) if e.get("file")]


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


# ── capture-time chronology (CAPTURE's corrected timestamps drive the order) ──
_NAME_DT = re.compile(r"(20\d{2})(\d{2})(\d{2})[_]?(\d{2})(\d{2})(\d{2})")


def _parse_name_dt(name):
    """DJI_20260314072347… / VID_20260314_120430… -> datetime (capture time in the filename)."""
    m = _NAME_DT.search(name or "")
    if not m:
        return None
    try:
        y, mo, d, h, mi, s = (int(x) for x in m.groups())
        return datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc)
    except Exception:
        return None


def _stamp(unix=None, iso=None, filename=None):
    """Best-available capture time -> (sort_key, display 'YYYY-MM-DD HH:MM:SS').
    Order of trust: unix epoch (group anchor) -> ISO (registry corrected_timestamp)
    -> filename-embedded time. Unknown -> ('9999', '') so it sorts last, unprefixed."""
    dt = None
    if unix:
        try:
            dt = datetime.fromtimestamp(float(unix), tz=timezone.utc)
        except Exception:
            dt = None
    if dt is None and iso:
        try:
            dt = datetime.fromisoformat(str(iso).replace("Z", "").split("+")[0].strip())
        except Exception:
            dt = None
    if dt is None:
        dt = _parse_name_dt(filename)
    if dt is None:
        return ("9999", "")
    s = dt.strftime("%Y-%m-%d %H:%M:%S")
    return (s, s)


def _pfx(display, base):
    return f"{display} · {base}" if display else base


# ── build ────────────────────────────────────────────────────────────────────
def build_fcpxml(event_name, groups, media_index, probe=probe_media,
                 seq_fps=None, media_mode="both", ungrouped=None, timestamp_names=True):
    """Return (xml_str, stats). Pure-ish: `probe` is injectable for tests.

    `ungrouped` (optional) is a list of dicts {original, proxy, sha, camera,
    resolution, duration_sec} for single-camera clips that didn't form a group;
    they're emitted as ordinary <asset-clip>s in the Event so the whole shoot lands
    in FCP, not just the multicam moments.
    """
    stats = {"groups": 0, "angles": 0, "clips": 0, "assets": 0,
             "fallback": 0, "missing": 0, "ungrouped": 0}

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
        gts = g.get("timestamp_start")
        if not gts:
            _fts = [f.get("timestamp_unix") for f in g.get("files", []) if f.get("timestamp_unix")]
            gts = min(_fts) if _fts else None
        skey, sdisp = _stamp(unix=gts)
        mc_name = _pfx(sdisp, f"MC_{gid}") if timestamp_names else f"MC_{gid}"
        event_items.append(
            (skey, f'<mc-clip ref="{mid}" name="{_esc(mc_name)}" duration="{gdur}"/>'))

    # 4b) Ungrouped single-camera clips -> ordinary <asset-clip>s in the Event,
    #     so the whole shoot is available in FCP (not only the multicam moments).
    for u in (ungrouped or []):
        original = u.get("original")
        if not original:
            stats["missing"] += 1
            continue
        if original not in probe_cache:
            probe_cache[original] = probe(original)
        pr = probe_cache[original]
        if pr and pr["width"]:
            fmt = pr
        else:
            stats["fallback"] += 1
            w = h = 0
            res = u.get("resolution") or ""
            if "x" in res:
                try:
                    w, h = (int(v) for v in res.lower().split("x")[:2])
                except Exception:
                    w = h = 0
            fmt = {"width": w, "height": h, "fps_num": 0, "fps_den": 1,
                   "duration_s": float(u.get("duration_sec") or 0.0),
                   "has_video": True, "has_audio": True,
                   "audio_channels": 2, "audio_rate": 48000}
        c = {"sha": u.get("sha") or original, "camera": u.get("camera") or "Unknown",
             "original": original, "proxy": u.get("proxy"), "fmt": fmt}
        aid = asset_id(c)
        fid = format_id(fmt["width"], fmt["height"], fmt["fps_num"], fmt["fps_den"])
        dur, _ = _t(fmt["duration_s"], fmt["fps_num"] or seq_num, fmt["fps_den"] or seq_den)
        skey, sdisp = _stamp(iso=u.get("corrected_timestamp"), filename=Path(original).name)
        uname = _pfx(sdisp, Path(original).stem) if timestamp_names else Path(original).stem
        event_items.append(
            (skey, f'<asset-clip ref="{aid}" name="{_esc(uname)}" '
                   f'duration="{dur}" format="{fid}"/>'))
        stats["ungrouped"] += 1

    # 5) Assemble. Event items sorted CHRONOLOGICALLY by capture time (stable sort keeps
    #    same-timestamp items in insertion order). Resources: formats, assets, media.
    event_items.sort(key=lambda t: t[0])
    event_xml = [x for _, x in event_items]
    res = ([v[1] for v in formats.values()]
           + [v[1] for v in assets.values()]
           + media_xml)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n'
        f'<fcpxml version="{FCPXML_VERSION}">\n'
        "  <resources>\n    " + "\n    ".join(res) + "\n  </resources>\n"
        "  <library>\n"
        f'    <event name="{_esc(event_name)}">\n      ' + "\n      ".join(event_xml) +
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
    ap.add_argument("--groups-only", action="store_true",
                    help="export only the multicam groups (omit ungrouped single-camera clips)")
    ap.add_argument("--no-timestamp-prefix", action="store_true",
                    help="don't prefix clip names with the capture timestamp (order stays chronological)")
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

    ungrouped = []
    if not args.groups_only:
        by_path, by_name = {}, {}
        for row in media_index.values():
            if row.get("original_path"):
                by_path[row["original_path"]] = row
            if row.get("filename"):
                by_name.setdefault(row["filename"], row)
        for p in load_ungrouped(output_path, args.run):
            row = by_path.get(p) or by_name.get(Path(p).name) or {}
            ungrouped.append({"original": p, "proxy": row.get("proxy_path"),
                              "sha": row.get("id"), "camera": row.get("camera_family"),
                              "resolution": row.get("resolution"),
                              "duration_sec": row.get("duration_sec"),
                              "corrected_timestamp": row.get("corrected_timestamp")})

    xml, stats = build_fcpxml(event_name, groups, media_index, seq_fps=seq_fps,
                              media_mode=args.media, ungrouped=ungrouped,
                              timestamp_names=not args.no_timestamp_prefix)

    out = args.out or Path(f"{event_name}_multicam.fcpxml")
    Path(out).write_text(xml, encoding="utf-8")
    print(f"✓ FCPXML written: {Path(out).resolve()}")
    print(f"  {stats['groups']} multicam clip(s) · {stats['angles']} angle(s) · "
          f"{stats['clips']} clip placement(s) · {stats['assets']} asset(s)")
    if stats.get("ungrouped"):
        print(f"  + {stats['ungrouped']} ungrouped single-camera clip(s) in the Event")
    if stats["fallback"]:
        print(f"  ⚠ {stats['fallback']} clip(s) used registry metadata (ffprobe unavailable/offline) "
              f"— fps assumed; verify timing in FCP.")
    if stats["missing"]:
        print(f"  ⚠ {stats['missing']} file(s) had no resolvable path — skipped.")
    print(f"  Media: {args.media}. Import via FCP ▸ File ▸ Import ▸ XML, then 'Synchronize Clips' to lock audio.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
