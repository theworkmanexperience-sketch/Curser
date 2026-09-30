#!/usr/bin/env python3
"""F-5 / G-07: enumerate out-of-range anchored elements (08-24) and pair them with the
08-22 population. Read-only. Uses the committed resolver (fcpx_resolve.py, run with
NONE: no ETC, no generator) and the resolver's own out-of-range predicate:
    abs_in_s < -0.001  or  abs_out_s > sequence_duration + 0.001
Pairing key (mechanical): (tag, name, lane, round(duration_s, 3)). One-to-one, in order."""
import hashlib, json, subprocess, sys, tempfile, os, urllib.parse
import xml.etree.ElementTree as ET

F24, F22, OUT = sys.argv[1:4]
EXPECT = {F24: 'd82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80',
          F22: '2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7'}
HERE = os.path.dirname(os.path.abspath(__file__))
RESOLVER = os.path.join(HERE, '..', 'scripts', 'fcpx_resolve.py')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


for p, h in EXPECT.items():
    if sha(p) != h:
        sys.exit(f'STOP FAILED_SOURCE_IDENTITY {p}')


def oor(fcpxml):
    tmp = tempfile.mktemp(suffix='.json')
    subprocess.run([sys.executable, RESOLVER, fcpxml, 'NONE', tmp], check=True, capture_output=True)
    d = json.load(open(tmp)); os.unlink(tmp)
    D = d['sequence']['duration_s']
    root = ET.parse(fcpxml).getroot()
    src = {}
    for a in root.iter('asset'):
        mr = a.find('media-rep')
        src[a.get('id')] = urllib.parse.unquote(os.path.basename(mr.get('src'))) if mr is not None else a.get('name')
    rows, anchor = [], None
    for x in d['elements']:
        if x['depth'] == 0:
            anchor = x   # rows are emitted depth-first: the last depth-0 row is the ancestor
        if x['abs_in_s'] < -0.001 or x['abs_out_s'] > D + 0.001:
            rows.append(dict(id=x['path'], tag=x['tag'], lane=x['lane'], depth=x['depth'],
                             abs_in_s=x['abs_in_s'], abs_out_s=x['abs_out_s'], duration_s=x['duration_s'],
                             name=x['name'], parent=x['parent'],
                             anchor=dict(tag=anchor['tag'], name=anchor['name'],
                                         abs_in_s=anchor['abs_in_s'], abs_out_s=anchor['abs_out_s']), media=src.get(x['ref']) if x['ref'] else None,
                             side=('BEFORE_0' if x['abs_in_s'] < -0.001 else '') +
                                  ('+' if x['abs_in_s'] < -0.001 and x['abs_out_s'] > D + 0.001 else '') +
                                  ('AFTER_END' if x['abs_out_s'] > D + 0.001 else '')))
    return D, rows


D24, r24 = oor(F24)
D22, r22 = oor(F22)
key = lambda r: (r['tag'], r['name'], r['lane'], round(r['duration_s'], 3))
pool = list(r22)
for r in r24:
    m = next((q for q in pool if key(q) == key(r)), None)
    r['pair_0822'] = m['id'] if m else None
    if m:
        pool.remove(m)
json.dump(dict(fcpxml_0824=dict(path=F24, sha256=EXPECT[F24], duration_s=D24, n=len(r24)),
               fcpxml_0822=dict(path=F22, sha256=EXPECT[F22], duration_s=D22, n=len(r22)),
               rows_0824=r24, unpaired_0822=[q['id'] for q in pool]),
          open(OUT, 'w'), indent=1)
print(len(r24), len(r22), sum(1 for r in r24 if r['pair_0822']), [q['id'] for q in pool])
