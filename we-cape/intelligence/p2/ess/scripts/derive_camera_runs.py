#!/usr/bin/env python3
"""Derive camera_runs.json from a resolved timeline.

WHY THIS EXISTS. gen_artifacts.py consumed camera_runs.json, and NO SCRIPT IN THE
REPOSITORY PRODUCED IT. This module replaces that orphan input with a deterministic
derivation from the resolved FCPXML, so the pipeline has no unproduceable dependency.

Camera family is read from the FCPXML clip NAME - an editorial fact, not a visual
observation. Device family does NOT establish capture mode.

usage: derive_camera_runs.py <timeline_resolved.json> <out.json> [--families X5,DJI,OM1]
"""
import json, re, sys

NAME_RE = re.compile(r'^\s*\d+\s*[··]\s*[\d-]+\s+[\d:]+\s*[··]\s*([A-Za-z0-9]+)\s*[··]')

def family(name, known):
    m = NAME_RE.match(name or '')
    if m and m.group(1) in known:
        return m.group(1)
    return 'COMPOUND'

def derive(timeline_path, families):
    tl = json.load(open(timeline_path))
    known = set(families)
    runs = []
    for e in tl['elements']:
        if e.get('depth') != 0:            # primary spine only
            continue
        if e.get('tag') == 'transition':   # transitions are not camera runs
            continue
        runs.append(dict(camera=family(e.get('name'), known),
                         start_s=round(float(e['abs_in_s']), 3),
                         end_s=round(float(e['abs_out_s']), 3),
                         name=e.get('name'), tag=e.get('tag')))
    return runs

def main(timeline_path, out_path, fam='X5,DJI,OM1'):
    runs = derive(timeline_path, fam.split(','))
    json.dump(runs, open(out_path, 'w'), indent=1)
    tot = {}
    for r in runs:
        tot[r['camera']] = tot.get(r['camera'], 0.0) + r['end_s'] - r['start_s']
    print('camera runs:', len(runs))
    for k, v in sorted(tot.items(), key=lambda kv: -kv[1]):
        print(f'  {k:10s} {v:9.1f} s')
    return runs

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    f = [x.split('=',1)[1] for x in sys.argv[1:] if x.startswith('--families=')]
    main(*a, *(f or []))
