#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Local Read-Only Dashboard Generator (prototype)

Reads ~/.wecape/registry/wecape.db READ-ONLY and emits ONE self-contained HTML
file: zero CDN, zero network, no server. Open offline. A window, never a mutation
layer (DB opened mode=ro; never written).

Shows: per-shoot reference cards (Tier 1 registry + Tier 2 shoot-folder enrichment),
processing-time breakdown + normalized rate + idempotent-re-run flag, derivation
lineage, and processing-activity pie charts bucketed by processing date
(monthly / quarterly / semi-annual / annual) for shoots, files, proxies, footage.

Usage:  python3 scripts/dashboard.py [--db PATH] [--out PATH]   # stdlib only
"""

import argparse
import html
import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB = Path.home() / ".wecape" / "registry" / "wecape.db"
PALETTE = ['#4f8cff', '#3fb950', '#d29922', '#bc8cff', '#ff7b72', '#39c5cf',
           '#db61a2', '#e3b341', '#56d364', '#a371f7', '#f0883e', '#6e7681']


# ── read-only data access ───────────────────────────────────────────────────
def connect_ro(db_path):
    uri = f"file:{Path(db_path).resolve().as_posix()}?mode=ro"
    c = sqlite3.connect(uri, uri=True)
    c.row_factory = sqlite3.Row
    return c


def table_cols(conn, table):
    try:
        return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
    except sqlite3.Error:
        return set()


def schema_version(conn):
    try:
        return conn.execute("SELECT MAX(version) FROM schema_version").fetchone()[0] or 0
    except sqlite3.Error:
        return 0


def parse_stages(stage_results_json):
    """Return groups, variants, {stage:duration}, and the proxy counts dict."""
    groups = variants = None
    durations, proxy = {}, {}
    try:
        for s in json.loads(stage_results_json or "[]"):
            sid = s.get("stage_id")
            meta = s.get("metadata", {}) or {}
            d = s.get("duration_sec")
            if isinstance(d, (int, float)) and d > 0:
                durations[sid] = durations.get(sid, 0) + d
            if sid == "group" and "groups" in meta:
                groups = meta["groups"]
            if sid == "variants" and "variant_groups" in meta:
                variants = meta["variant_groups"]
            if sid == "proxy":
                proxy = {"transcoded": meta.get("transcoded"),
                         "skipped": meta.get("skipped"),
                         "failed": meta.get("failed")}
    except Exception:
        pass
    return groups, variants, durations, proxy


def enrich_from_folder(out_path, run_id, src_path):
    info = {"reachable": False, "source_mounted": bool(src_path and Path(src_path).exists())}
    try:
        if not out_path or not Path(out_path).is_dir():
            return info
        od = Path(out_path)
        info["reachable"] = True
        info["output_path"] = str(od)
        idx = od / f"{run_id}_index.json"
        if idx.exists():
            info["totals"] = json.loads(idx.read_text()).get("totals", {})
        members = []
        for m in sorted(od.glob("**/MULTICAM/*.json"))[:12]:
            try:
                g = json.loads(m.read_text())
                members.append({"id": g.get("group_id", m.stem),
                                "sources": sorted(set(g.get("camera_sources", []))),
                                "files": [Path(f.get("path", "")).name for f in g.get("files", [])][:12]})
            except Exception:
                pass
        info["groups"] = members
    except Exception:
        pass
    return info


def gather(conn):
    runs_cols = table_cols(conn, "runs")
    has_source_clip = "source_clip" in table_cols(conn, "content")
    content = [dict(r) for r in conn.execute("SELECT * FROM content")]
    runs = [dict(r) for r in conn.execute(
        "SELECT * FROM runs WHERE file_count > 0 ORDER BY timestamp DESC")]

    for r in runs:
        g, v, durs, proxy = parse_stages(r.get("stage_results"))
        r["_groups"], r["_variants"], r["_durs"], r["_proxy"] = g, v, durs, proxy
        try:
            r["_errors"] = len(json.loads(r.get("errors") or "[]"))
        except Exception:
            r["_errors"] = 0
        src = (r.get("source_path") or "").rstrip("/")
        rc = [c for c in content if src and (c.get("original_path") or "").startswith(src)]
        mix = {}
        for c in rc:
            fam = c.get("camera_family") or "(unclassified)"
            mix[fam] = mix.get(fam, 0) + 1
        r["_mix"] = dict(sorted(mix.items(), key=lambda x: -x[1]))
        r["_proxies"] = sum(1 for c in rc if c.get("proxy_path"))
        r["_bytes"] = sum((c.get("file_size_bytes") or 0) for c in rc)
        r["_selects"] = (sum(1 for c in rc if c.get("source_clip")) if has_source_clip else None)
        r["_t2"] = enrich_from_folder(r.get("output_path"), r.get("id"), src)

    by_cam = {}
    for c in content:
        fam = c.get("camera_family") or "(unclassified)"
        by_cam[fam] = by_cam.get(fam, 0) + 1

    lineage = None
    if has_source_clip:
        sel = [c for c in content if c.get("source_clip")]
        src_counts, pinned = {}, 0
        for c in sel:
            src_counts[c["source_clip"]] = src_counts.get(c["source_clip"], 0) + 1
            if c.get("source_clip_sha"):
                pinned += 1
        lineage = {"selects": len(sel), "sources": len(src_counts), "pinned": pinned,
                   "top": sorted(src_counts.items(), key=lambda x: -x[1])[:8]}

    return {"schema_version": schema_version(conn), "runs": runs,
            "content_total": len(content),
            "total_bytes": sum((c.get("file_size_bytes") or 0) for c in content),
            "proxied": sum(1 for c in content if c.get("proxy_path")),
            "by_cam": dict(sorted(by_cam.items(), key=lambda x: -x[1])),
            "lineage": lineage, "sample": content[:20]}


# ── formatting + charts (all inline; no external assets) ────────────────────
def esc(x):
    return html.escape(str(x if x is not None else ""))


def gb(n):
    return f"{(n or 0) / (1024**3):.1f} GB"


def svg_bars(pairs, width=520, bar_h=20, gap=7):
    if not pairs:
        return "<p class='muted'>No data.</p>"
    mx = max(v for _, v in pairs) or 1
    lw, vw, pad = 150, 56, 6
    pw = width - lw - vw
    h = len(pairs) * (bar_h + gap) + gap
    rows = []
    for i, (label, val) in enumerate(pairs):
        y = gap + i * (bar_h + gap)
        bw = max(2, int(pw * (val / mx)))
        rows.append(f"<text x='0' y='{y+bar_h*0.72:.0f}' class='lbl'>{esc(label)[:22]}</text>"
                    f"<rect x='{lw}' y='{y}' width='{bw}' height='{bar_h}' rx='3' class='bar'/>"
                    f"<text x='{lw+bw+pad}' y='{y+bar_h*0.72:.0f}' class='val'>{esc(val)}</text>")
    return f"<svg viewBox='0 0 {width} {h}' width='100%' height='{h}'>{''.join(rows)}</svg>"


def svg_pie(pairs, fmt=str, size=150):
    pairs = [(l, v) for l, v in pairs if v and v > 0]
    if not pairs:
        return "<p class='muted'>—</p>"
    total = sum(v for _, v in pairs) or 1
    cx = cy = size / 2
    r = size / 2 - 2
    a0 = -math.pi / 2
    paths, legend = [], []
    for i, (label, v) in enumerate(pairs):
        col = PALETTE[i % len(PALETTE)]
        frac = v / total
        if len(pairs) == 1:
            paths.append(f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{col}'/>")
        else:
            a1 = a0 + frac * 2 * math.pi
            x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
            x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
            large = 1 if frac > 0.5 else 0
            paths.append(f"<path d='M{cx:.1f},{cy:.1f} L{x0:.1f},{y0:.1f} "
                         f"A{r:.1f},{r:.1f} 0 {large} 1 {x1:.1f},{y1:.1f} Z' fill='{col}'/>")
            a0 = a1
        legend.append(f"<div class='leg'><span class='sw' style='background:{col}'></span>"
                      f"{esc(label)} · {esc(fmt(v))} ({round(100*frac)}%)</div>")
    return (f"<div class='pie'><svg viewBox='0 0 {size} {size}' width='{size}' height='{size}'>"
            f"{''.join(paths)}</svg><div class='legs'>{''.join(legend)}</div></div>")


def _ts_keys(ts):
    """(monthly, quarterly, semi, annual) keys from an ISO timestamp."""
    if not ts or len(ts) < 7:
        return ("unknown",) * 4
    y, m = ts[:4], int(ts[5:7])
    return (ts[:7], f"{y}-Q{(m-1)//3+1}", f"{y}-H{1 if m <= 6 else 2}", y)


def period_section(runs):
    groupings = ["Monthly", "Quarterly", "Semi-annual", "Annual"]
    blocks = []
    for gi, gname in enumerate(groupings):
        buckets = {}
        for r in runs:
            k = _ts_keys(r.get("timestamp") or "")[gi]
            b = buckets.setdefault(k, {"shoots": 0, "files": 0, "proxies": 0, "bytes": 0})
            b["shoots"] += 1
            b["files"] += r.get("file_count") or 0
            b["proxies"] += r.get("_proxies", 0)
            b["bytes"] += r.get("_bytes", 0)
        order = sorted(buckets)

        def pie(metric, fmt):
            return svg_pie([(k, buckets[k][metric]) for k in order], fmt=fmt)
        disp = "" if gi == 0 else "display:none"
        blocks.append(
            f"<div class='grp' id='grp{gi}' style='{disp}'><div class='pies'>"
            f"<div class='pieblock'><div class='pt'>Shoots</div>{pie('shoots', str)}</div>"
            f"<div class='pieblock'><div class='pt'>Files</div>{pie('files', str)}</div>"
            f"<div class='pieblock'><div class='pt'>Proxies</div>{pie('proxies', str)}</div>"
            f"<div class='pieblock'><div class='pt'>Footage</div>{pie('bytes', gb)}</div>"
            f"</div></div>")
    btns = ""
    for i, g in enumerate(groupings):
        on = " on" if i == 0 else ""
        btns += f"<button class='pbtn{on}' onclick='wcShow({i})'>{esc(g)}</button>"
    script = ("<script>function wcShow(i){var b=document.getElementsByClassName('pbtn');"
              "for(var j=0;j<4;j++){document.getElementById('grp'+j).style.display=(j==i?'':'none');"
              "b[j].className='pbtn'+(j==i?' on':'');}}</script>")
    return f"<div class='periodbtns'>{btns}</div>{''.join(blocks)}{script}"


def shoot_card(r):
    name = Path(r.get("output_path") or "").name or (r.get("id") or "")[:24]
    t2 = r["_t2"]
    if not t2["reachable"]:
        badge = "<span class='badge gray'>registry only · folder offline</span>"
    elif t2["source_mounted"]:
        badge = "<span class='badge good'>Ready to edit ✓ · originals mounted</span>"
    else:
        badge = "<span class='badge warn'>proxies editable ⚠ · originals' drive offline</span>"

    mix = " · ".join(f"{esc(k)} {v}" for k, v in r["_mix"].items()) or "—"
    g = r["_groups"] if r["_groups"] is not None else "—"
    v = r["_variants"] if r["_variants"] is not None else "—"
    sel = f" · {r['_selects']} selects" if r.get("_selects") else ""

    # Processing time: total, breakdown, normalized rate, re-run flag
    runtime = r.get("runtime_sec") or 0
    proxy = r.get("_proxy") or {}
    transcoded = proxy.get("transcoded")
    rerun = (transcoded == 0 and (proxy.get("skipped") or 0) > 0)
    prox_for_rate = transcoded if transcoded else r["_proxies"]
    gbv = (r["_bytes"] or 0) / (1024**3)
    rate_bits = []
    if runtime and prox_for_rate:
        rate_bits.append(f"{runtime/60/prox_for_rate:.2f} min/proxy")
    if runtime and gbv:
        rate_bits.append(f"{runtime/60/gbv:.2f} min/GB")
    durs = r.get("_durs") or {}
    breakdown = " · ".join(f"{esc(k)} {dv:.0f}s" for k, dv in
                           sorted(durs.items(), key=lambda x: -x[1])[:4]) if durs else ""
    rerun_html = " <span class='badge warn'>idempotent re-run · 0 transcoded</span>" if rerun else ""
    proc = (f"<div class='t2row'><b>Processing:</b> {runtime:.0f}s total"
            + (f" · {breakdown}" if breakdown else "")
            + (f" · {' · '.join(rate_bits)}" if rate_bits else "")
            + rerun_html + "</div>")

    t2_html = ""
    if t2["reachable"]:
        tot = t2.get("totals") or {}
        if tot:
            t2_html += ("<div class='t2row'><b>Classification:</b> "
                        f"camera {tot.get('camera_files','?')} · audio {tot.get('camera_audio_files','?')} · "
                        f"generic {tot.get('generic_files','?')} · reference {tot.get('reference_files','?')}</div>")
        for grp in t2.get("groups", []):
            t2_html += (f"<div class='t2row'><b>multicam {esc(grp['id'])[:16]}</b> "
                        f"({'+'.join(esc(s) for s in grp['sources'])}): "
                        f"{', '.join(esc(f) for f in grp['files'])}</div>")
        if t2.get("output_path"):
            t2_html += (f"<div class='t2row muted'>Output: <span class='mono'>{esc(t2['output_path'])}</span></div>")
    else:
        t2_html = ("<div class='t2row muted'>Shoot folder not reachable — mount its drive for "
                   "multicam membership, full classification, and the edit handoff.</div>")

    return f"""
    <div class="shoot">
      <div class="shoot-head"><span class="sname">{esc(name)}</span>{badge}</div>
      <div class="metrics"><b>{esc(r.get('file_count'))}</b> files <span class="good">· 0 lost</span> ·
        {esc(r['_proxies'])} proxies · {esc(g)} groups · {esc(v)} variants{esc(sel)} ·
        {esc(r['_errors'])} errors · {gb(r['_bytes'])}</div>
      <div class="metrics muted">cameras: {mix} · {esc((r.get('timestamp') or '')[:19])} UTC · profile {esc(r.get('profile_id') or '—')}</div>
      {proc}{t2_html}
    </div>"""


def render(d, db_path):
    cards = "".join(shoot_card(r) for r in d["runs"]) or "<p class='muted'>No shoots recorded.</p>"
    cam_bars = svg_bars(list(d["by_cam"].items()))
    periods = period_section(d["runs"])

    if d["lineage"] is None:
        lineage_html = ("<p class='muted'>Lineage available at schema v3+. Registry is v"
                        + esc(d["schema_version"]) + "; it auto-migrates on the next CAPTURE run.</p>")
    elif d["lineage"]["selects"] == 0:
        lineage_html = "<p class='muted'>No curated selects (<code>_sel&lt;NN&gt;</code>) recorded yet.</p>"
    else:
        L = d["lineage"]
        lineage_html = (f"<p><b>{L['selects']}</b> selects from <b>{L['sources']}</b> sources · "
                        f"{L['pinned']} SHA-pinned.</p>" + svg_bars([(k, v) for k, v in L["top"]]))

    sample = "".join(
        f"<tr><td class='mono'>{esc((c.get('id') or '')[:12])}…</td><td>{esc(c.get('filename'))}</td>"
        f"<td>{esc(c.get('camera_family') or '—')}</td><td>{esc(c.get('shoot_date') or '—')}</td>"
        f"<td>{'✓' if c.get('proxy_path') else ''}</td><td>{esc(c.get('source_clip') or '')}</td></tr>"
        for c in d["sample"]) or "<tr><td colspan='6' class='muted'>No content.</td></tr>"

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>W.E. C.A.P.E. — Production Dashboard</title>
<style>
 :root{{--bg:#0f1115;--card:#171a21;--ink:#e6e9ef;--muted:#8a93a3;--line:#262b35;--bar:#4f8cff;--good:#3fb950;--warn:#d29922}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
 .wrap{{max-width:1000px;margin:0 auto;padding:28px 20px 60px}}
 h1{{font-size:20px;margin:0 0 2px}} h2{{font-size:14px;margin:22px 0 12px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}}
 .sub{{color:var(--muted);margin:0 0 22px}}
 .cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}}
 .card .n{{font-size:26px;font-weight:600}} .card .k{{color:var(--muted);font-size:12px}}
 .shoot{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:12px}}
 .shoot-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}}
 .sname{{font-size:16px;font-weight:600}}
 .metrics{{font-size:13px;margin-bottom:4px}} .t2row{{font-size:12.5px;margin-top:6px;padding-left:10px;border-left:2px solid var(--line)}}
 .badge{{font-size:11px;border-radius:20px;padding:3px 9px;border:1px solid}}
 .badge.good{{background:#13351d;color:var(--good);border-color:#1e5130}} .badge.warn{{background:#33270a;color:var(--warn);border-color:#5a4410}}
 .badge.gray{{background:#1b1f27;color:var(--muted);border-color:var(--line)}}
 section{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:14px}}
 table{{width:100%;border-collapse:collapse}} th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);font-size:12.5px}}
 th{{color:var(--muted);font-weight:500}} .mono{{font-family:ui-monospace,Menlo,monospace;font-size:12px}} .muted{{color:var(--muted)}} .good{{color:var(--good)}}
 code{{background:#0b0d11;padding:1px 5px;border-radius:4px;font-size:12px}}
 text.lbl{{fill:var(--ink);font-size:12px}} text.val{{fill:var(--muted);font-size:12px}} rect.bar{{fill:var(--bar)}}
 .periodbtns{{margin-bottom:12px}} .pbtn{{background:#1b1f27;color:var(--muted);border:1px solid var(--line);border-radius:7px;padding:5px 12px;margin-right:6px;cursor:pointer;font-size:12.5px}}
 .pbtn.on{{background:var(--bar);color:#fff;border-color:var(--bar)}}
 .pies{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
 .pieblock{{background:#12151b;border:1px solid var(--line);border-radius:8px;padding:12px}}
 .pt{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:8px}}
 .pie{{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap}}
 .legs{{font-size:11.5px}} .leg{{margin:1px 0}} .sw{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px;vertical-align:middle}}
 .note{{border-left:3px solid var(--line);padding:6px 12px;color:var(--muted);margin-top:10px;font-size:12px}}
 footer{{color:var(--muted);font-size:12px;margin-top:26px;border-top:1px solid var(--line);padding-top:14px}}
</style></head><body><div class="wrap">
 <h1>W.E. C.A.P.E. — Production Dashboard</h1>
 <p class="sub">Local · read-only · {generated} · registry schema v{d['schema_version']} · <span class="mono">{esc(db_path)}</span></p>
 <div class="cards">
   <div class="card"><div class="n">{len(d['runs'])}</div><div class="k">Shoots</div></div>
   <div class="card"><div class="n">{d['content_total']}</div><div class="k">Files · 0 lost</div></div>
   <div class="card"><div class="n">{d['proxied']}</div><div class="k">Proxies</div></div>
   <div class="card"><div class="n">{gb(d['total_bytes'])}</div><div class="k">Footage</div></div>
 </div>

 <h2>Per-Shoot Reference</h2>
 {cards}

 <section><h2>Processing Activity · by period</h2>
   <p class="muted">Bucketed by processing date. Toggle granularity:</p>
   {periods}</section>

 <section><h2>Disposition · nothing dropped</h2>
   <p class="muted">Every ingested file preserved &amp; classified. By camera family:</p>{cam_bars}</section>

 <section><h2>Derivation Lineage</h2>{lineage_html}</section>

 <section><h2>Per-clip record (sample)</h2>
   <table><tr><th>SHA-256</th><th>Filename</th><th>Camera</th><th>Shoot date</th><th>Proxy</th><th>Source clip</th></tr>{sample}</table>
   <div class="note">Processing breakdown + rate + re-run flag populate for runs processed after stage-timing
     was added; older runs show total runtime only. Per-clip fallback/confidence &amp; conflict decisions
     live in <code>LOGS/*.json</code>; AI fields (quality/highlight/tags) are null in v1.</div></section>

 <footer>Opened the registry <code>mode=ro</code> · no network · no external assets. A window, not a mutation layer.</footer>
</div></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description="Generate a local read-only W.E. C.A.P.E. dashboard.")
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--out", type=Path, default=Path("wecape_dashboard.html"))
    args = ap.parse_args()
    if not args.db.exists():
        raise SystemExit(f"Registry not found: {args.db}")
    conn = connect_ro(args.db)
    try:
        data = gather(conn)
    finally:
        conn.close()
    args.out.write_text(render(data, args.db), encoding="utf-8")
    reachable = sum(1 for r in data["runs"] if r["_t2"]["reachable"])
    print(f"✓ Dashboard written: {args.out.resolve()}")
    print(f"  {len(data['runs'])} shoots ({reachable} folder-reachable) · "
          f"{data['content_total']} files · schema v{data['schema_version']}")
    print(f"  Open it: open \"{args.out.resolve()}\"")


if __name__ == "__main__":
    main()
