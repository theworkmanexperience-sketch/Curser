#!/usr/bin/env python3
"""Part-2 chrono-sets FCPXML generator (LOCKED 2026-08-13).
Doctrine: X5 curated = foundational spine, chronological; all cameras
interleaved by engine-true time; 20-min temporal SETs + scene keywords.
Reconciliation: prints per-camera counts + every skipped file w/ reason
(no-unexplained-deltas rule). Validated output: X5=40 DJI=31 OM1=9
TOTAL=80, 14 sets. Generalization -> engine scene/set stage (filed)."""
import pathlib, re, subprocess, urllib.parse, datetime as dt
JOB = pathlib.Path("/Volumes/WE_CAPE_OUTPUT/AlphaRoundUp_2026")
OUT = JOB / "XML" / "P2_CHRONO_SETS.fcpxml"
items, skipped = [], []
for f in sorted((JOB/"Curated_X5_JUN26").iterdir()):
    if f.name.startswith("._") or f.suffix.lower() not in (".mov", ".mp4"):
        if f.is_file() and not f.name.startswith("._"): skipped.append(("ext", f.name))
        continue
    m = re.match(r"VID_(\d{8})_(\d{6})_00_(\d+)", f.name)
    if not m:
        skipped.append(("name-pattern", f.name)); continue
    child = re.search(r"\((\d+)\)", f.name)
    t = dt.datetime.strptime(m.group(1)+m.group(2), "%Y%m%d%H%M%S") + dt.timedelta(seconds=int(child.group(1)) if child else 0)
    items.append((t, f, "X5"))
x5 = len(items)
for f in sorted((JOB/"STAGING_P2_JUN26").glob("DJI_*.MP4")):
    m = re.match(r"DJI_(\d{14})", f.name)
    if m: items.append((dt.datetime.strptime(m.group(1), "%Y%m%d%H%M%S"), f, "DJI"))
dji = len(items) - x5
for name in ["P6250003.MOV","P6250004.MOV","P6250005.MOV","P6250007.MOV","P6250014.MOV","P6250015.MOV","P6250016.MOV","P6260018.MOV","P6260017.JPG"]:
    f = JOB/"SOURCES/OM SYSTEM OM-1"/name
    if f.exists(): items.append((dt.datetime.fromtimestamp(f.stat().st_mtime), f, "OM1"))
    else: skipped.append(("missing", name))
om = len(items) - x5 - dji
items.sort(key=lambda x: x[0])
def dur(p):
    r = subprocess.run(["mdls","-raw","-name","kMDItemDurationSeconds",str(p)],capture_output=True,text=True).stdout.strip()
    try: return max(float(r), 1.0)
    except Exception: return 5.0
def scene(t):
    if t.day == 25 or (t.day == 26 and t.hour < 6): return "ARRIVAL_MEETNGREET"
    return "COMMUNITY_SERVICE" if t.hour < 15 else "BIKE_NIGHT"
assets, clips, setno, prev = [], [], 0, None
for i, (t, f, cam) in enumerate(items, 1):
    if prev is None or (t - prev).total_seconds() > 1200: setno += 1
    prev = t
    d = dur(f); rid = i + 1
    url = "file://" + urllib.parse.quote(str(f))
    nm = f"{i:03d} · {t:%m-%d %H:%M:%S} · {cam} · {f.name}"
    assets.append(f'<asset id="r{rid}" name="{nm}" start="0s" duration="{d}s" hasVideo="1"><media-rep kind="original-media" src="{url}"/></asset>')
    clips.append(f'<asset-clip ref="r{rid}" name="{nm}" duration="{d}s"><keyword start="0s" duration="{d}s" value="SET_{setno:02d}"/><keyword start="0s" duration="{d}s" value="{scene(t)}"/></asset-clip>')
OUT.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.10"><resources>' + "".join(assets) + '</resources><library><event name="P2_CHRONO_SETS">' + "".join(clips) + '</event></library></fcpxml>')
print(f"RECONCILIATION: X5={x5} DJI={dji} OM1={om} TOTAL={len(items)} · sets={setno}")
for why, name in skipped: print(f"  SKIPPED ({why}): {name}")
print(f"wrote {OUT}")
