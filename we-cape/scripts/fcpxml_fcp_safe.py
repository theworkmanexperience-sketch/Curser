#!/usr/bin/env python3
"""Strip non-FCP-importable assets (default: .insv) from a generated FCPXML.
Usage: python3 scripts/fcpxml_fcp_safe.py <file.fcpxml> [--exclude .insv .foo]
Writes <file>_FCP_SAFE.fcpxml. Companion to fcpxml_export.py; retires when
the exporter filters at generation (ENG-F-20260812B)."""
import sys, argparse, pathlib
import xml.etree.ElementTree as ET
ap = argparse.ArgumentParser()
ap.add_argument("fcpxml"); ap.add_argument("--exclude", nargs="*", default=[".insv", ".orf"])
args = ap.parse_args()
src = pathlib.Path(args.fcpxml)
dst = src.with_name(src.stem + "_FCP_SAFE.fcpxml")
ext = tuple(e.lower() for e in args.exclude)
tree = ET.parse(src); root = tree.getroot()
res = root.find("resources"); bad = set()
for a in list(res.findall("asset")):
    rep = a.find("media-rep")
    s = ((rep.get("src") if rep is not None else None) or a.get("src") or "").lower()
    if s.endswith(ext):
        bad.add(a.get("id")); res.remove(a)
def refs_bad(el):
    return el.get("ref") in bad or any(refs_bad(c) for c in el)
removed = 0
for parent in root.iter():
    for el in list(parent):
        if el.tag in ("asset-clip","mc-clip","clip","ref-clip") and refs_bad(el):
            parent.remove(el); removed += 1
tree.write(dst, encoding="UTF-8", xml_declaration=True)
print(f"assets removed: {len(bad)} | clips removed: {removed} | wrote: {dst}")
