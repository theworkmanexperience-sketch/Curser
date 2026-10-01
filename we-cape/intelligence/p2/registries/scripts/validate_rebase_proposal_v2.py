#!/usr/bin/env python3
"""Validates the final (all-tier) rebase proposals. Read-only on every input. Exit 1 on any failure.
Writes FIELD_DIFF_v1.13_to_v1.14.md and prints the report (redirected to VALIDATION_v1.14.0-PROPOSED.txt)."""
import hashlib, json, os, subprocess, sys, tempfile
from fractions import Fraction
import yaml

HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
sys.path.insert(0, HERE); import build_rebase_proposal_v2 as B
EPR_NEW, TL_NEW = B.OUT_EPR, B.OUT_TL
out, fails = [], []
say = out.append
def check(n, ok, d=''):
    say(f'{"PASS" if ok else "FAIL"}  {n}' + (f'  -  {d}' if d else '')); ok or fails.append(n)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()

def diff(a, b, p=''):
    if isinstance(a, dict) and isinstance(b, dict):
        r = [('REMOVED', f'{p}.{k}', a[k], None) for k in a if k not in b]
        for k in a:
            if k in b: r += diff(a[k], b[k], f'{p}.{k}')
        return r + [('ADDED', f'{p}.{k}', None, b[k]) for k in b if k not in a]
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        r = []
        for i, (x, y) in enumerate(zip(a, b)): r += diff(x, y, f'{p}[{i}]')
        return r
    return [] if a == b else [('CHANGED', p, a, b)]

def secs(x):
    m, s = x.split(':'); return int(m) * 60 + Fraction(s)

def main():
    for k, (p, h) in B.INPUTS.items():
        check(f'V0 input hash {k}', sha(p) == h, sha(p)[:16])
    if fails: print('\n'.join(out)); sys.exit(1)
    for k in ('epr', 'timeline'):
        p, h = B.INPUTS[k]
        hb = hashlib.sha256(subprocess.run(['git', 'show', f'HEAD:./{os.path.relpath(p, ROOT)}'], cwd=ROOT,
                            capture_output=True, check=True).stdout).hexdigest()
        check(f'V2 ratified original byte-identical: {os.path.basename(p)}', sha(p) == h == hb)
    D = {}
    for n, p in (('eo', B.INPUTS['epr'][0]), ('en', EPR_NEW), ('to', B.INPUTS['timeline'][0]), ('tn', TL_NEW)):
        try:
            D[n] = yaml.safe_load(open(p, encoding='utf-8')); check(f'V1 parses {os.path.basename(p)}', isinstance(D[n], dict))
        except yaml.YAMLError as e:
            check(f'V1 parses {os.path.basename(p)}', False, str(e)[:100])
    if fails: print('\n'.join(out)); sys.exit(1)
    v2 = json.load(open(B.INPUTS['v2'][0])); seg = {r['segment']: r for r in v2['segments']}

    de = diff(D['eo'], D['en'])
    check('V3 EPR field diff == allowed set exactly', {(o, p) for o, p, _, _ in de} ==
          {('CHANGED', '.registry_version'), ('ADDED', '.proposal_status'), ('ADDED', '.registry_version_note_1_14_0_PROPOSED')},
          ', '.join(sorted(p for _, p, _, _ in de)))
    check('V3 EPR version 1.14.0-PROPOSED', D['en']['registry_version'] == '1.14.0-PROPOSED')
    check('V5 EPR entries deep-equal (all 7, incl. EPR-07)', D['eo']['entries'] == D['en']['entries'])
    for k in ('segment_authority', 'segment_authority_status', 'segment_authority_note', 'path_b_consequences',
              'registry_ratification', 'undeclared_segments', 'intensity_scale', 'governing_invariants'):
        check(f'V5 untouched: {k}', D['eo'].get(k) == D['en'].get(k))
    pbc2 = lambda d: [x for x in d['path_b_consequences'] if x['id'] == 'PBC-2'][0]
    check('V5 PBC-2 record identical', pbc2(D['eo']) == pbc2(D['en']), pbc2(D['en'])['disposition'])
    note = D['en']['registry_version_note_1_14_0_PROPOSED']
    for t, lab in ((sha(TL_NEW), 'TIMELINE proposal hash'), (B.V2, 'v2 hash'), ('R9 A2 MOOT', 'R9'),
                   ('B-14', 'B-14'), ('REVISE-BOUNDARY', 'R6'), ('38971/12', 'S14 exact end')):
        check(f'V7 EPR changelog cites {lab}', t in note)

    io = {s['id']: i for i, s in enumerate(D['to']['segments'])}; inn = {s['id']: i for i, s in enumerate(D['tn']['segments'])}
    check('V9 R9: segment set unchanged (S01..S19, no A2 row, no new segment)',
          [s['id'] for s in D['tn']['segments']] == [s['id'] for s in D['to']['segments']] == [f'S{i:02d}' for i in range(1, 20)])
    dt = diff(D['to'], D['tn'])
    allowed = {('CHANGED', '.registry_version'), ('ADDED', '.proposal_status'), ('ADDED', '.changelog')}
    for s in [f'S{i:02d}' for i in range(1, 19)]:
        allowed.add(('ADDED', f'.segments[{inn[s]}].span_basis'))
        if D['to']['segments'][io[s]]['span'] != D['tn']['segments'][inn[s]]['span']:
            allowed.add(('CHANGED', f'.segments[{inn[s]}].span'))
    allowed.add(('CHANGED', f'.segments[{inn["S16"]}].interview_count'))   # Chairman S16 ruling 2026-10-01
    allowed.add(('CHANGED', f'.segments[{inn["S16"]}].participants[0]'))   # Chairman S16 participants ruling 2026-10-01
    got = {(o, p) for o, p, _, _ in dt}
    check('V4 TIMELINE field diff ⊆ {version, status, changelog, span, span_basis on S01-S18}', got <= allowed and
          all(not p.startswith(f'.segments[{inn["S19"]}]') for _, p in got), f'{len(dt)} changes')
    allowed.add(('CHANGED', f'.segments[{inn["S16"]}].interview_count'))   # Chairman S16 ruling 2026-10-01
    check('V4b S16 interview_count 8 -> 7 (Chairman ruling)',
          D['to']['segments'][io['S16']]['interview_count'] == 8 and D['tn']['segments'][inn['S16']]['interview_count'] == 7)
    check('V4b S16 participants [R68-R75] -> [R68-R74] (Chairman ruling)',
          D['to']['segments'][io['S16']]['participants'] == ['R68-R75'] and D['tn']['segments'][inn['S16']]['participants'] == ['R68-R74'])
    check('V4b changelog records the S16 participants ruling', D['tn']['changelog'][0].get('s16_participants', {}).get('to') == '[R68-R74]')
    check('V4b changelog records the S16 ruling', D['tn']['changelog'][0].get('s16_interview_count', {}).get('to') == 7)
    for s in D['tn']['segments']:
        o = D['to']['segments'][io[s['id']]]
        skip = ('span', 'span_basis') + (('interview_count', 'participants') if s['id'] == 'S16' else ())
        check(f'V4 {s["id"]} non-span fields identical' + (' (except ruled interview_count, participants)' if s['id'] == 'S16' else ''),
              {k: v for k, v in o.items() if k not in skip} == {k: v for k, v in s.items() if k not in skip})

    tier1 = subprocess.run(['git', 'show', f'{B.TIER1_PROPOSAL_COMMIT}:./intelligence/p2/registries/TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml'],
                           cwd=ROOT, capture_output=True, check=True).stdout.decode()
    t1 = {l[9:12]: l for l in tier1.splitlines() if l.startswith('  - {id: S')}
    nw = {l[9:12]: l for l in open(TL_NEW, encoding='utf-8').read().splitlines() if l.startswith('  - {id: S')}
    for s in B.TIER1:
        check(f'V6 Tier-1 {s} row byte-identical to {B.TIER1_PROPOSAL_COMMIT}', t1[s] == nw[s])
    for s in list(B.RULING) + B.TIER1:
        a, b = D['tn']['segments'][inn[s]]['span'].split('-')
        ok = abs(secs(a) - Fraction(str(seg[s]['new_start']))) < Fraction(1, 2000) and abs(secs(b) - Fraction(str(seg[s]['new_end']))) < Fraction(1, 2000)
        check(f'V6 {s} span == v2 mapping {seg[s]["new_start"]}-{seg[s]["new_end"]}', ok, D['tn']['segments'][inn[s]]['span'])
    a, b = D['tn']['segments'][inn['S14']]['span'].split('-')
    check('V8 S14 start = v2-mapped 3205.701625 (ms repr, not frame-aligned)', secs(a) == Fraction('3205.702') and
          abs(secs(a) - B.S14_START_EXACT) <= Fraction(1, 2000), a)
    check('V8 S14 end = R6 38971/12 (ms repr 3247.583)', secs(b) == Fraction('3247.583') and
          abs(secs(b) - B.S14_END_EXACT) <= Fraction(1, 2000), b)
    check('V8 S14 span_basis carries exact rational, frame 77942, 00:54:07:14',
          all(x in D['tn']['segments'][inn['S14']]['span_basis'] for x in ('38971/12', '77942', '00:54:07:14', '3205.701625')))
    check('V8 S14 end is NOT the superseded mapped 3246.432', secs(b) != Fraction('3246.432'))
    check('V6 S19 row entirely unchanged', D['to']['segments'][io['S19']] == D['tn']['segments'][inn['S19']])
    sp = [(secs(x['span'].split('-')[0]), secs(x['span'].split('-')[1])) for x in D['tn']['segments'][:18]]
    check('V6 S01-S18 spans ordered, positive, non-overlapping, within 4689.5s',
          all(a < b for a, b in sp) and all(sp[i][1] <= sp[i + 1][0] for i in range(17)) and sp[-1][1] <= Fraction('4689.5'))
    check('V10 both outputs PROPOSED', D['en']['proposal_status'] == D['tn']['proposal_status'] == 'PROPOSED — AWAITING CHAIRMAN RATIFICATION')
    h1 = (sha(EPR_NEW), sha(TL_NEW))
    subprocess.run([sys.executable, os.path.join(HERE, 'build_rebase_proposal_v2.py')], check=True, capture_output=True)
    check('V11 build deterministic (rebuild identical)', (sha(EPR_NEW), sha(TL_NEW)) == h1)

    say(''); say(f'EPR-001 v1.14.0-PROPOSED  sha256 {sha(EPR_NEW)}'); say(f'TIMELINE v1.1.0-PROPOSED  sha256 {sha(TL_NEW)}')
    say(f'RESULT: {"ALL PASS" if not fails else "FAIL: " + ", ".join(fails)}')

    md = ['# FIELD DIFF — EPR-001 v1.13.0 → v1.14.0-PROPOSED · TIMELINE v1.0.0 → v1.1.0-PROPOSED (final rebase)', '',
          '**Status: PROPOSED — AWAITING CHAIRMAN RATIFICATION.** Generated by `scripts/validate_rebase_proposal_v2.py` '
          'from parsed YAML (field level). Supersedes the Tier-1-only diff of `c5a72dc`.', '',
          '| artifact | sha256 |', '|---|---|',
          f'| EPR-001 v1.13.0 (RATIFIED, unchanged) | `{B.INPUTS["epr"][1]}` |', f'| **EPR-001 v1.14.0-PROPOSED** | `{sha(EPR_NEW)}` |',
          f'| TIMELINE v1.0.0 (in force, unchanged) | `{B.INPUTS["timeline"][1]}` |', f'| **TIMELINE v1.1.0-PROPOSED** | `{sha(TL_NEW)}` |',
          f'| mapping: v2 `rederivation_v2.json` (G8-ratified) | `{B.V2}` |',
          f'| final disposition sheet (R1-R9 closed) | `{B.INPUTS["sheet"][1]}` |', '',
          f'## EPR-001 — {len(de)} field changes (allowed set: exactly these 3)', '', '| op | field | v1.13.0 | proposed |', '|---|---|---|---|']
    for o, p, a, b in de:
        md.append(f'| {o} | `{p}` | {"—" if a is None else f"`{a}`"} | ' + (f'`{b}`' if o == 'CHANGED' else (str(b)[:120] + '…')) + ' |')
    md += ['', 'Unchanged and verified deep-equal: all 7 `entries`, segment_authority, segment_authority_status, '
           'segment_authority_note, path_b_consequences (PBC-2 included), registry_ratification, undeclared_segments, '
           'intensity_scale, governing_invariants. A 5-line STATUS banner comment was also added.', '',
           f'## TIMELINE — {len(dt)} field changes', '', '| seg | basis | v1.0.0 (08-22) | v1.1.0-PROPOSED (08-24) |', '|---|---|---|---|']
    for s in D['tn']['segments']:
        o = D['to']['segments'][io[s['id']]]
        basis = ('Tier 1 (unchanged vs c5a72dc)' if s['id'] in B.TIER1 else 'R6 REVISE-BOUNDARY' if s['id'] == 'S14'
                 else f'{B.RULING[s["id"]][0]} {B.RULING[s["id"]][1]}' if s['id'] in B.RULING else 'untouched (EPR-07 RETIRED)')
        md.append(f'| {s["id"]} | {basis} | `{o["span"]}` | `{s["span"]}` |')
    md += ['', 'Plus: `registry_version` 1.0.0 → 1.1.0-PROPOSED, `proposal_status`, `changelog`, and `span_basis` on S01–S18. '
           'Every non-span field of every row is identical to v1.0.0, except S16 interview_count 8 → 7 and participants [R68-R75] → [R68-R74] (Chairman S16 rulings, 2026-10-01).', '', '## Validation', '', '```'] + out + ['```', '']
    open(os.path.join(REG, 'FIELD_DIFF_v1.13_to_v1.14.md'), 'w').write('\n'.join(md))
    print('\n'.join(out)); sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
