#!/usr/bin/env python3
"""Derive camera_runs.json from a resolved timeline.

ECR-GEN-004 SEMANTIC SUCCESSOR of derive_camera_runs.py (Chairman ruling, Decision B / G5):
an element whose camera family cannot be assigned under the clip-name convention below -
an unrecognized family, a name outside the convention, contributed or non-camera media, or a
gap - is UNCERTAIN; no family is inferred. The predecessor's fallback label COMPOUND is not an
authorized camera-family value; it survives only in historical 08-22 outputs, which the
predecessor (retained unchanged) still reproduces. Nothing else differs from the predecessor.

WHY THIS EXISTS. gen_artifacts.py consumed camera_runs.json, and NO SCRIPT IN THE
REPOSITORY PRODUCED IT. This module replaces that orphan input with a deterministic
derivation from the resolved FCPXML, so the pipeline has no unproduceable dependency.

Camera family is read from the FCPXML clip NAME - an editorial fact, not a visual
observation. Device family does NOT establish capture mode.

usage: derive_camera_runs_v2.py <timeline_resolved.json> <out.json> [--families X5,DJI,OM1]

ECR-GEN-003: a deterministic provenance sidecar `<out.json>.provenance.json` (script
SHA-256, input SHA-256, the families argument, interpreter identity; no wall-clock
value) is written beside the output. The clip-name pattern, camera-family rule,
defaults and the UNCERTAIN fallback are as stated above.
"""
import json, re, sys
import hashlib, os, platform

NAME_RE = re.compile(r'^\s*\d+\s*[··]\s*[\d-]+\s+[\d:]+\s*[··]\s*([A-Za-z0-9]+)\s*[··]')

def family(name, known):
    m = NAME_RE.match(name or '')
    if m and m.group(1) in known:
        return m.group(1)
    return 'UNCERTAIN'

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

def _sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def write_provenance(out_path, timeline_path, fam):
    rec = dict(schema='b3-provenance/1',
               producer=os.path.basename(__file__), producer_sha256=_sha256(__file__),
               arguments=dict(families=fam),
               inputs=[dict(role='timeline', path=timeline_path, sha256=_sha256(timeline_path),
                            bytes=os.path.getsize(timeline_path))],
               outputs=[dict(path=os.path.basename(out_path), sha256=_sha256(out_path),
                             bytes=os.path.getsize(out_path))],
               toolchain=dict(python=platform.python_version(),
                              implementation=sys.implementation.name,
                              interpreter=os.path.realpath(sys.executable),
                              machine=platform.machine()))
    with open(out_path + '.provenance.json', 'w') as fh:
        fh.write(json.dumps(rec, indent=1, sort_keys=True) + '\n')

def main(timeline_path, out_path, fam='X5,DJI,OM1'):
    runs = derive(timeline_path, fam.split(','))
    with open(out_path, 'w') as fh:
        json.dump(runs, fh, indent=1)
    write_provenance(out_path, timeline_path, fam)
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
