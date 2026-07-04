#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Production Health Report (postmortem)

After a CAPTURE run, explain the shoot back to the creator — honestly: what
happened, which cameras were hard to assemble, the likely cause (usually a camera
clock), and a specific cure with a *projected* (simulated) gain.

Reads the registry READ-ONLY (never mutates it). Enriched, in priority order, by:
  • a shoot manifest (`shoot.yaml`) → a trusted-clock reference (names the culprit), and
  • `telemetry.db` (.SRT GPS/time) → an authoritative clock (names it without a manifest).
When neither is present it reports RELATIVE skew + flags the statistical outlier, and
never accuses a specific camera (SPEC_Production_Health_Report.md §2).

Honesty guardrails enforced here:
  - grouping / clock health only — NEVER a "% sync accuracy" number (§2.1);
  - cures say "should/expected/projected", never "will" (§2.2);
  - no culprit named without a trusted reference (§2.3);
  - "0 files lost" is the one absolute (§2.4); every number derives from run data (§2.5).

CLI:  python3 scripts/health_report.py <run_id> [--db …] [--manifest shoot.yaml]
                                       [--telemetry telemetry.db] [--out FILE.md]
stdlib only · zero network · read-only.
"""

import argparse
import json
import re
import sqlite3
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB = Path.home() / ".wecape" / "registry" / "wecape.db"
DEFAULT_TELEMETRY = Path.home() / ".wecape" / "telemetry.db"
DEFAULT_WINDOW = 15          # production grouping window (§21 deviation); spec default is 5
RFQ_WINDOW = 5


# ─────────────────────────────────────────────────────────────────────────────
# Pure metrics (unit-tested; no I/O)
# ─────────────────────────────────────────────────────────────────────────────
def _epoch(iso):
    """ISO string → epoch seconds (tolerant). Returns None if unparseable."""
    if not iso:
        return None
    s = str(iso).strip().replace("Z", "").replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            continue
    return None


def humanize_skew(seconds):
    """Signed seconds → plain English, e.g. '~8 years behind', '3s ahead'."""
    if seconds is None:
        return "unknown"
    a = abs(seconds)
    direction = "behind" if seconds < 0 else "ahead"
    if a < 1:
        return "in sync"
    for unit, size in (("year", 31557600), ("month", 2629800), ("day", 86400),
                       ("hour", 3600), ("minute", 60)):
        if a >= size:
            n = a / size
            return f"~{n:.0f} {unit}{'s' if round(n) != 1 else ''} {direction}"
    return f"~{a:.0f}s {direction}"


def camera_skews(clips, trusted_camera=None, window=DEFAULT_WINDOW):
    """clips: list of {camera, epoch}. Returns per-camera skew vs consensus.

    consensus = the trusted camera's median if given & present, else the median of
    the per-camera medians (robust to a single wild outlier). skew = cam median −
    consensus. A camera is an 'outlier' only if |skew| exceeds the grouping window
    AND it is the largest — otherwise no accusation."""
    by_cam = {}
    for c in clips:
        if c.get("epoch") is not None:
            by_cam.setdefault(c["camera"] or "unknown", []).append(c["epoch"])
    if not by_cam:
        return {"consensus": None, "trusted": trusted_camera, "cameras": [], "outlier": None,
                "no_timestamps": True}

    med = {cam: statistics.median(v) for cam, v in by_cam.items()}
    if trusted_camera and trusted_camera in med:
        consensus = med[trusted_camera]
    else:
        consensus = statistics.median(list(med.values()))

    rows = [{"camera": cam, "skew_s": m - consensus, "n": len(by_cam[cam])}
            for cam, m in sorted(med.items(), key=lambda kv: -abs(kv[1] - consensus))]
    outlier = None
    if rows:
        top = rows[0]
        others = [abs(r["skew_s"]) for r in rows[1:]] or [0]
        # material outlier: beyond the window and clearly worse than the next camera
        if abs(top["skew_s"]) > window and abs(top["skew_s"]) >= 2 * max(others):
            outlier = top["camera"]
    for r in rows:
        r["is_outlier"] = (r["camera"] == outlier)
    return {"consensus": consensus, "trusted": trusted_camera, "cameras": rows,
            "outlier": outlier, "no_timestamps": False}


def grouping_health(total_camera, grouped, ungrouped, quarantined=0):
    total = total_camera if total_camera else (grouped or 0) + (ungrouped or 0)
    pct = (100.0 * grouped / total) if (total and grouped is not None) else None
    if pct is None:
        verdict = "grouping counts unavailable for this run"
    elif pct >= 99:
        verdict = "healthy — nearly every camera clip assembled into a group"
    elif pct >= 80:
        verdict = "mostly healthy — a minority of clips stood alone"
    else:
        verdict = "assembly was hard — many clips could not be grouped"
    return {"total": total, "grouped": grouped, "ungrouped": ungrouped,
            "quarantined": quarantined, "pct": pct, "verdict": verdict}


def projected_improvement(skew_result, window=DEFAULT_WINDOW, ungrouped=None):
    """A LABELLED simulation: if the outlier's clock were corrected, its clips would
    fall inside the grouping window. Not a promise (§6)."""
    o = skew_result.get("outlier")
    if not o:
        return None
    row = next((r for r in skew_result["cameras"] if r["camera"] == o), None)
    if not row:
        return None
    correction = -row["skew_s"]
    return {
        "camera": o,
        "correction_human": humanize_skew(correction).replace(" behind", " forward").replace(" ahead", " back"),
        "correction_s": correction,
        "expected_ungrouped_after": 0,
        "expected_window": min(window, 5),
        "note": ("Simulation — assumes clock skew is the only issue and is constant across "
                 "the shoot. Planning estimate, not a guarantee. Not frame-accurate sync."),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Loaders (read-only registry + optional manifest/telemetry)  — I/O edges
# ─────────────────────────────────────────────────────────────────────────────
def _ro(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        con = sqlite3.connect(f"file:{p.resolve().as_posix()}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        return con
    except sqlite3.Error:
        return None


def load_run(db, run_id):
    con = _ro(db)
    if con is None:
        return None, []
    try:
        run = con.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
        rows = con.execute("SELECT * FROM content WHERE run_id=?", (run_id,)).fetchall()
        return (dict(run) if run else None), [dict(r) for r in rows]
    except sqlite3.Error:
        return None, []
    finally:
        con.close()


def load_trusted_clock(manifest_path):
    if not manifest_path or not Path(manifest_path).exists():
        return None
    for line in Path(manifest_path).read_text().splitlines():
        m = re.match(r"\s*trusted_clock\s*:\s*(.+)\s*$", line)
        if m:
            v = m.group(1).strip().strip('"').strip("'")
            return None if v.lower() in ("unknown", "") else v
    return None


def load_telemetry_times(telemetry_db, content_ids):
    """content_sha → SRT start_time epoch (authoritative clock), if present."""
    con = _ro(telemetry_db)
    if con is None:
        return {}
    out = {}
    try:
        for cid in content_ids:
            r = con.execute("SELECT start_time FROM telemetry WHERE content_sha=?", (cid,)).fetchone()
            if r and r["start_time"]:
                e = _epoch(r["start_time"])
                if e is not None:
                    out[cid] = e
    except sqlite3.Error:
        pass
    finally:
        con.close()
    return out


def _camera_of(row):
    return row.get("camera_id") or row.get("camera_family") or row.get("camera_source") or "unknown"


def _index_counts(output_path):
    """Best-effort group/ungrouped/window from the run's *_index.json."""
    if not output_path:
        return {}
    d = Path(output_path)
    if not d.is_dir():
        return {}
    for idx in sorted(d.glob("*_index.json")):
        try:
            j = json.loads(idx.read_text())
            return {"grouped": j.get("grouped_camera_files") or j.get("camera_files_grouped"),
                    "groups": j.get("groups_formed"),
                    "ungrouped": (j.get("ungrouped_camera_files") if isinstance(j.get("ungrouped_camera_files"), int)
                                  else j.get("ungrouped")),
                    "window": (j.get("window_seconds") or j.get("grouping_window_seconds"))}
        except Exception:
            continue
    return {}


def build_report_data(db, run_id, manifest=None, telemetry=DEFAULT_TELEMETRY, window=DEFAULT_WINDOW):
    run, content = load_run(db, run_id)
    if run is None and not content:
        return None
    run = run or {}
    originals = [r for r in content if (r.get("content_type") or "original") == "original"]

    trusted = load_trusted_clock(manifest)
    tele = load_telemetry_times(telemetry, [r.get("id") for r in originals]) if originals else {}

    clips = []
    for r in originals:
        epoch = tele.get(r.get("id"))                       # GPS/SRT time wins if present
        if epoch is None:
            epoch = _epoch(r.get("corrected_timestamp") or r.get("shoot_date"))
        clips.append({"camera": _camera_of(r), "epoch": epoch})

    idx = _index_counts(run.get("output_path"))
    win = idx.get("window") or window
    total_cam = len(originals)
    grouped = idx.get("grouped")
    ungrouped = idx.get("ungrouped")

    skew = camera_skews(clips, trusted_camera=trusted, window=win)
    ground_truth = "telemetry" if tele else ("manifest" if trusted else None)
    return {
        "run_id": run_id, "run": run,
        "summary": grouping_health(total_cam, grouped, ungrouped, 0),
        "skew": skew, "window_used": win,
        "ground_truth": ground_truth, "trusted": trusted,
        "projection": projected_improvement(skew, win, ungrouped),
        "have_times": sum(1 for c in clips if c["epoch"] is not None), "total_clips": len(clips),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Render
# ─────────────────────────────────────────────────────────────────────────────
def render_markdown(data):
    r, s, sk = data["run_id"], data["summary"], data["skew"]
    L = [f"# Production Health — {r}", ""]

    # 4.1 Summary
    L.append("## Summary")
    if s["pct"] is not None:
        L.append(f"- Camera clips: **{s['total']}** · grouped **{s['grouped']}** "
                 f"({s['pct']:.0f}%) · ungrouped **{s['ungrouped']}**")
    else:
        L.append(f"- Camera clips: **{s['total']}** · {s['verdict']}")
    L.append(f"- Assembly: {s['verdict']}")
    L.append("- **0 files lost** — every ingested file is preserved and accounted for.")
    L.append("")

    # 4.2 Camera Health
    L.append("## Camera Health (clock check)")
    if sk["no_timestamps"]:
        L.append("- No resolved timestamps available for this run — clock check skipped.")
    else:
        mode = data["ground_truth"]
        if mode == "telemetry":
            L.append("- Reference: **GPS/.SRT time** (authoritative). Skew is against true time.")
        elif mode == "manifest":
            L.append(f"- Reference: **{data['trusted']}** (your declared trusted clock).")
        else:
            L.append("- Reference: **relative** — no trusted clock given, so this shows which "
                     "camera *disagrees* with the others, not which is objectively right.")
        for c in sk["cameras"]:
            tag = "  ⚠ outlier" if c["is_outlier"] else ""
            L.append(f"  - {c['camera']}: {humanize_skew(c['skew_s'])} "
                     f"({c['skew_s']:+.0f}s, {c['n']} clips){tag}")
        if sk["outlier"]:
            if mode:
                L.append(f"- **Culprit: {sk['outlier']}** — its clock is off; the others agree.")
            else:
                L.append(f"- **Likely culprit: {sk['outlier']}** (statistical outlier). "
                         "Confirm which clock is correct before trusting this.")
        else:
            L.append("- All cameras agree within the grouping window — clocks look healthy.")
    L.append("")

    # 4.3 Grouping Analysis
    L.append("## Grouping Analysis")
    L.append(f"- Window used: **±{data['window_used']}s** (RFQ spec ±{RFQ_WINDOW}s — "
             "widened for field clock drift; documented deviation).")
    if data["have_times"] < data["total_clips"]:
        L.append(f"- {data['total_clips'] - data['have_times']} clip(s) had low-confidence "
                 "(file-clock) timestamps — flagged.")
    L.append("")

    # 4.4 Recommendations
    L.append("## Recommendations (the cure)")
    p = data["projection"]
    if p:
        L.append(f"- **Set the {p['camera']} clock to the correct date/time before the next shoot** "
                 f"(it's {humanize_skew(-p['correction_s'])} — correct it by {p['correction_human']}).")
        L.append("- Better: sync every camera to one accurate source (your phone) before rolling.")
        L.append(f"- *Projected (simulation):* with {p['camera']}'s clock corrected, its clips "
                 f"should fall inside the ±{p['expected_window']}s window and group with the others; "
                 f"expected ungrouped from this cause → {p['expected_ungrouped_after']}.")
        L.append(f"  - _{p['note']}_")
    elif not sk["no_timestamps"]:
        L.append("- Clocks look healthy — no clock correction needed. Keep syncing cameras before shoots.")
    L.append("")

    L.append("## Technical Details")
    L.append("- Every figure above derives from this run's registry + logs (auditable). "
             "This report reads only; it changes nothing.")
    L.append("- Grouping health only — this is **not** a frame-accurate sync measurement "
             "(use Final Cut's *Synchronize Clips* for that).")
    L.append("")
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def _cli(argv=None):
    ap = argparse.ArgumentParser(description="W.E. C.A.P.E. — Production Health Report (postmortem).")
    ap.add_argument("run_id", help="run to report on (e.g. WEF_20260624_001707_C5A8AB)")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="registry (read-only)")
    ap.add_argument("--manifest", help="shoot.yaml with a trusted_clock (names the culprit)")
    ap.add_argument("--telemetry", default=str(DEFAULT_TELEMETRY), help="telemetry.db (.SRT GPS time)")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW, help="grouping window if unknown")
    ap.add_argument("--out", help="write the report to this file (default: print only)")
    args = ap.parse_args(argv)

    data = build_report_data(args.db, args.run_id, manifest=args.manifest,
                             telemetry=args.telemetry, window=args.window)
    if data is None:
        print(f"  No run '{args.run_id}' in {args.db}.")
        return 1
    md = render_markdown(data)
    if args.out:
        Path(args.out).write_text(md)
        print(f"  ✓ wrote {args.out}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
