#!/usr/bin/env python3
"""Validation of the v2 re-derivation against v1. Read-only. Exit 1 on any failure."""
import hashlib, json, os, subprocess, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(H)
V1 = ('rederivation.json', '5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117')
fails = []
def check(n, ok, d=''):
    print(f'{"PASS" if ok else "FAIL"}  {n}' + (f'  -  {d}' if d else '')); ok or fails.append(n)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
v1p, v2p = os.path.join(P, V1[0]), os.path.join(H, 'rederivation_v2.json')
check('V1 artifact unmodified (== G8 ratified hash)', sha(v1p) == V1[1], sha(v1p)[:16])
a, b = json.load(open(v1p)), json.load(open(v2p))
check('inputs identical to v1 (same 4 media hashes)', {k: v['sha256'] for k, v in a['inputs'].items()} ==
      {k: v['sha256'] for k, v in b['inputs'].items()})
check('v2 identity closes exactly', b['ledger']['closes'] is True, b['ledger']['identity_check'])
r = json.load(open(os.path.join(H, 'reconciliation.json')))
check('v2 per-segment residuals: no unexplained deltas', r['unexplained_segment_deltas'] == [])
check('v2 categorized reconciliation closes (rounding bound)', r['closes'] is True, f"tol {r['closes_tolerance_s']}")
sa = {x['segment']: x for x in a['segments']}; sb = {x['segment']: x for x in b['segments']}
changed = sorted(s for s in sa if any(sa[s][k] != sb[s][k] for k in ('new_start', 'new_end'))
                 or sa[s]['start']['status'] != sb[s]['start']['status'] or sa[s]['end']['status'] != sb[s]['end']['status'])
check('BOUNDED DIFF: only S14 boundaries change', changed == ['S14'], str(changed))
for s in ('S03', 'S11', 'S12', 'S13', 'S15', 'S16'):   # decided rows R1-R5, R7, R8 (R4 = S12 end / S13 start)
    check(f'decided row segment {s} boundaries identical', (sa[s]['new_start'], sa[s]['new_end']) == (sb[s]['new_start'], sb[s]['new_end']),
          f"{sb[s]['new_start']}-{sb[s]['new_end']}")
check('R4 edge 3193.167 unchanged (S12 end == S13 start)', sb['S12']['new_end'] == sb['S13']['new_start'] == 3193.167)
t1 = ['S01', 'S02', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S17', 'S18']
check('Tier-1 (TIMELINE proposal c5a72dc inputs) identical', all((sa[s]['new_start'], sa[s]['new_end']) == (sb[s]['new_start'], sb[s]['new_end']) for s in t1))
check('S14 v2 = 3205.702 -> 3246.432, both MAPPED', (sb['S14']['new_start'], sb['S14']['new_end'], sb['S14']['start']['status'], sb['S14']['end']['status'])
      == (3205.702, 3246.432, 'MAPPED', 'MAPPED'))
a2 = [x for x in b['added'] if x['t24_in'] < 3247.583 and x['t24_out'] > 3212.743]
check('A2 residue = boundary slivers only (< 0.1 s each)', all(x['dur'] < 0.1 for x in a2), str([(x['t24_in'], x['dur']) for x in a2]))
check('excluded cross-match set identical to v1', {(p['t22_in'], p['t24_in']) for p in a['excluded_pieces']} ==
      {(p['t22_in'], p['t24_in']) for p in b['excluded_pieces']})
with tempfile.TemporaryDirectory() as d:
    subprocess.run([os.path.join(P, 'run_v2.sh'), d], check=True, capture_output=True)
    check('v2 deterministic (fresh re-run byte-identical)', all(sha(os.path.join(d, f)) == sha(os.path.join(H, f))
          for f in ('rederivation_v2.json', 'reconciliation.json', 'mapping_table.csv', 'mapping_table.md')))
with tempfile.TemporaryDirectory() as d:
    subprocess.run([os.path.join(P, 'run.sh'), d], check=True, capture_output=True)
    check('v1 still reproduces byte-for-byte', sha(os.path.join(d, 'rederivation.json')) == V1[1])
print(f'\nv1 {V1[1]}\nv2 {sha(v2p)}\nRESULT: {"ALL PASS" if not fails else "FAIL: " + ", ".join(fails)}')
sys.exit(1 if fails else 0)
