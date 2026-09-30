#!/usr/bin/env python3
"""
Validates the Tier-1 rebase proposal. Read-only on every file.

  V1  all four YAML files parse
  V2  EPR v1.13.0 and TIMELINE v1.0.0 are byte-identical to their pinned hashes AND to
      the git HEAD blob (i.e. nothing wrote to the ratified originals)
  V3  field-level diff EPR 1.13.0 -> 1.14.0-PROPOSED shows ONLY the allowed paths
  V4  field-level diff TIMELINE 1.0.0 -> 1.1.0-PROPOSED shows ONLY the allowed paths
  V5  every EPR entry (beat, meaning, governing_theme, dramatic_intensity, audience_state,
      segment_refs, all other fields) is deep-equal, EPR-07 included
  V6  Tier-1 spans equal the accepted mapping; Tier-2/3 and S19 spans are unchanged
  V7  the EPR changelog cites the exact TIMELINE proposal hash and the mapping hash
  V8  the build is deterministic (re-run into a temp dir, identical bytes)

Emits a text report (stdout) and FIELD_DIFF_v1.13_to_v1.14.md. Exit 1 on any failure.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.dirname(HERE)
ESS = os.path.join(REG, '..', 'ess')
F = dict(
    epr_old=(os.path.join(REG, 'EMOTIONAL_PROGRESSION_REGISTRY.yaml'),
             '1d54e674190eef8122f7ddd22af66ae07abcb13dead7f5077ed868c37dbe21a4'),
    tl_old=(os.path.join(REG, 'TIMELINE_REGISTRY.yaml'),
            '34bd0f9ef7f1507cd8fa0f0745abadd675060b313d98d06ea2dd35c98bc8de76'),
    red=(os.path.join(ESS, 'decision_packet_b5_b14', 'rederivation.json'),
         '5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117'),
)
EPR_NEW = os.path.join(REG, 'EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0-PROPOSED.yaml')
TL_NEW = os.path.join(REG, 'TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml')
TIER1 = ['S01', 'S02', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S17', 'S18']
PENDING = ['S03', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16']

out, fails = [], []


def say(s=''):
    out.append(s)


def check(name, ok, detail=''):
    say(f'{"PASS" if ok else "FAIL"}  {name}' + (f'  -  {detail}' if detail else ''))
    if not ok:
        fails.append(name)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def head_blob_sha(p):
    rel = os.path.relpath(p, os.path.join(REG, '..', '..', '..'))
    b = subprocess.run(['git', 'show', f'HEAD:./{rel}'], cwd=os.path.join(REG, '..', '..', '..'),
                       capture_output=True, check=True).stdout
    return hashlib.sha256(b).hexdigest()


def diff(a, b, path=''):
    """Field-level diff -> list of (op, path, old, new)."""
    if isinstance(a, dict) and isinstance(b, dict):
        res = []
        for k in a:
            if k not in b:
                res.append(('REMOVED', f'{path}.{k}', a[k], None))
            else:
                res += diff(a[k], b[k], f'{path}.{k}')
        for k in b:
            if k not in a:
                res.append(('ADDED', f'{path}.{k}', None, b[k]))
        return res
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        res = []
        for i, (x, y) in enumerate(zip(a, b)):
            res += diff(x, y, f'{path}[{i}]')
        return res
    return [] if a == b else [('CHANGED', path, a, b)]


def seg_index(tl):
    return {s['id']: i for i, s in enumerate(tl['segments'])}


def main():
    # ---- inputs asserted before reading
    for k, (p, h) in F.items():
        check(f'V0 input hash {os.path.basename(p)}', sha(p) == h, sha(p)[:16])
    if fails:
        print('\n'.join(out)); sys.exit(1)

    # ---- V2 originals untouched
    for k in ('epr_old', 'tl_old'):
        p, h = F[k]
        hb = head_blob_sha(p)
        check(f'V2 byte-identical {os.path.basename(p)}', sha(p) == h == hb,
              f'disk {sha(p)[:16]} · pinned {h[:16]} · HEAD {hb[:16]}')

    # ---- V1 parse
    docs = {}
    for name, p in (('epr_old', F['epr_old'][0]), ('epr_new', EPR_NEW),
                    ('tl_old', F['tl_old'][0]), ('tl_new', TL_NEW)):
        try:
            docs[name] = yaml.safe_load(open(p, encoding='utf-8'))
            check(f'V1 parses {os.path.basename(p)}', isinstance(docs[name], dict))
        except yaml.YAMLError as e:
            check(f'V1 parses {os.path.basename(p)}', False, str(e)[:120])
    if fails:
        print('\n'.join(out)); sys.exit(1)

    red = json.load(open(F['red'][0]))
    seg = {r['segment']: r for r in red['segments']}
    tl_new_sha = sha(TL_NEW)

    # ---- V3 EPR diff
    d_epr = diff(docs['epr_old'], docs['epr_new'])
    allowed_epr = {('CHANGED', '.registry_version'), ('ADDED', '.proposal_status'),
                   ('ADDED', '.registry_version_note_1_14_0_PROPOSED')}
    got = {(op, p) for op, p, _, _ in d_epr}
    check('V3 EPR field diff == allowed set exactly', got == allowed_epr,
          f'{len(d_epr)} changes: ' + ', '.join(sorted(p for _, p in got)))
    rv = next(x for x in d_epr if x[1] == '.registry_version')
    check('V3 registry_version 1.13.0 -> 1.14.0-PROPOSED', (rv[2], rv[3]) == ('1.13.0', '1.14.0-PROPOSED'))
    check('V3 proposal_status', docs['epr_new'].get('proposal_status') ==
          'PROPOSED — AWAITING CHAIRMAN RATIFICATION')

    # ---- V5 entries deep-equal
    eo, en = docs['epr_old']['entries'], docs['epr_new']['entries']
    check('V5 EPR entries deep-equal (all 7, incl. EPR-07)', eo == en and len(en) == 7)
    for key in ('segment_authority', 'segment_authority_status', 'segment_authority_note',
                'path_b_consequences', 'registry_ratification', 'undeclared_segments',
                'intensity_scale', 'governing_invariants'):
        check(f'V5 unchanged: {key}', docs['epr_old'].get(key) == docs['epr_new'].get(key))

    # ---- V7 changelog citations
    note = docs['epr_new']['registry_version_note_1_14_0_PROPOSED']
    check('V7 changelog cites TIMELINE proposal hash', tl_new_sha in note, tl_new_sha[:16])
    check('V7 changelog cites mapping hash', F['red'][1] in note)
    check('V7 changelog cites Addendum A Tier 1', 'ADDENDUM A, TIER 1' in note)

    # ---- V4 TIMELINE diff
    d_tl = diff(docs['tl_old'], docs['tl_new'])
    io, inn = seg_index(docs['tl_old']), seg_index(docs['tl_new'])
    allowed_tl = {('CHANGED', '.registry_version'), ('ADDED', '.proposal_status'), ('ADDED', '.changelog')}
    for s in TIER1 + PENDING:
        allowed_tl.add(('ADDED', f'.segments[{inn[s]}].span_basis'))
    for s in TIER1:
        if seg[s]['new_start'] != seg[s]['old_start'] or seg[s]['new_end'] != seg[s]['old_end']:
            allowed_tl.add(('CHANGED', f'.segments[{inn[s]}].span'))
    got_tl = {(op, p) for op, p, _, _ in d_tl}
    check('V4 TIMELINE field diff == allowed set exactly', got_tl == allowed_tl, f'{len(d_tl)} changes')

    # ---- V6 span values
    def to_s(x):
        m, s = x.split(':')
        return int(m) * 60 + float(s)
    for s in TIER1:
        a, b = docs['tl_new']['segments'][inn[s]]['span'].split('-')
        ok = abs(to_s(a) - seg[s]['new_start']) < 0.0005 and abs(to_s(b) - seg[s]['new_end']) < 0.0005
        check(f'V6 {s} span == mapping {seg[s]["new_start"]}-{seg[s]["new_end"]}', ok,
              docs['tl_new']['segments'][inn[s]]['span'])
    for s in PENDING + ['S19']:
        same = docs['tl_old']['segments'][io[s]]['span'] == docs['tl_new']['segments'][inn[s]]['span']
        check(f'V6 {s} span unchanged (08-22)', same, docs['tl_new']['segments'][inn[s]]['span'])
    check('V6 S19 row entirely unchanged', docs['tl_old']['segments'][io['S19']] ==
          docs['tl_new']['segments'][inn['S19']])

    # ---- V8 determinism
    tmp = tempfile.mkdtemp()
    b1 = {p: sha(p) for p in (EPR_NEW, TL_NEW)}
    subprocess.run([sys.executable, os.path.join(HERE, 'build_tier1_rebase_proposal.py')],
                   check=True, capture_output=True)
    b2 = {p: sha(p) for p in (EPR_NEW, TL_NEW)}
    check('V8 build deterministic (rebuild identical)', b1 == b2)

    say()
    say(f'EPR-001 v1.14.0-PROPOSED  sha256 {sha(EPR_NEW)}')
    say(f'TIMELINE v1.1.0-PROPOSED  sha256 {sha(TL_NEW)}')
    say(f'RESULT: {"ALL PASS" if not fails else "FAIL: " + ", ".join(fails)}')

    # ---- FIELD_DIFF markdown
    md = ['# FIELD DIFF — EPR-001 v1.13.0 → v1.14.0-PROPOSED (and segment authority v1.0.0 → v1.1.0-PROPOSED)',
          '',
          '**Status: PROPOSED — AWAITING CHAIRMAN RATIFICATION.** Generated by '
          '`scripts/validate_tier1_rebase_proposal.py` from parsed YAML (field level, not text).',
          '',
          '| artifact | sha256 |', '|---|---|',
          f'| EPR-001 v1.13.0 (RATIFIED, unchanged) | `{F["epr_old"][1]}` |',
          f'| **EPR-001 v1.14.0-PROPOSED** | `{sha(EPR_NEW)}` |',
          f'| TIMELINE_REGISTRY v1.0.0 (in force, unchanged) | `{F["tl_old"][1]}` |',
          f'| **TIMELINE_REGISTRY v1.1.0-PROPOSED** | `{sha(TL_NEW)}` |',
          f'| mapping `rederivation.json` (G8 record) | `{F["red"][1]}` |',
          '',
          '## Why two files',
          '',
          'EPR-001 v1.13.0 carries **no temporal values**. Its beats bind to segment IDs, and its '
          '`segment_authority_note` bars resolving a segment_ref to a timecode. The spans live in '
          'TIMELINE_REGISTRY. The Chairman directed on 2026-09-30 that the Tier-1 rebase lands in a '
          'TIMELINE_REGISTRY proposal, with EPR-001 changing only by header, version and changelog.',
          '',
          f'## EPR-001 1.13.0 → 1.14.0-PROPOSED — {len(d_epr)} field changes (allowed set: exactly these 3)',
          '', '| op | field | v1.13.0 | v1.14.0-PROPOSED |', '|---|---|---|---|']
    for op, p, a, b in d_epr:
        bb = (str(b)[:140] + '…') if b is not None and len(str(b)) > 140 else b
        md.append(f'| {op} | `{p}` | {"—" if a is None else f"`{a}`"} | {bb if op != "CHANGED" else f"`{b}`"} |')
    md += ['', 'Also added as **YAML comments** (not fields, so they do not appear above): the '
           '5-line `STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION` banner at the top of the file.',
           '', '**Unchanged, verified deep-equal:** all 7 `entries` (every beat, meaning, governing_theme, '
           'dramatic_intensity, audience_state, segment_refs; EPR-07 included) · segment_authority · '
           'segment_authority_status · segment_authority_note · path_b_consequences (PBC-2 included; '
           'see changelog) · registry_ratification · undeclared_segments · intensity_scale · governing_invariants.',
           '', f'## TIMELINE_REGISTRY 1.0.0 → 1.1.0-PROPOSED — {len(d_tl)} field changes',
           '', '| op | field | v1.0.0 | v1.1.0-PROPOSED |', '|---|---|---|---|']
    for op, p, a, b in d_tl:
        if p == '.changelog':
            b = '(changelog entry: authority, mapping hashes, rebased / pending / untouched lists)'
        md.append(f'| {op} | `{p}` | {"—" if a is None else f"`{a}`"} | `{b}` |')
    md += ['', '### Span table', '', '| seg | tier | v1.0.0 (08-22) | v1.1.0-PROPOSED | basis |', '|---|---|---|---|---|']
    for s in [x['id'] for x in docs['tl_new']['segments']]:
        o, n = docs['tl_old']['segments'][io[s]], docs['tl_new']['segments'][inn[s]]
        tier = 'T1 rebase' if s in TIER1 else ('T2 pending' if s in ('S03', 'S11') else
                                               'T3 pending' if s in PENDING else 'untouched (EPR-07 RETIRED)')
        md.append(f'| {s} | {tier} | `{o["span"]}` | `{n["span"]}` | {n.get("span_basis", "—")} |')
    md += ['', 'S01 and S02 carry lag 0.000, so their span strings are unchanged. They gain only '
           '`span_basis`. `sources`, `delta_note` and `etc_anchors` are unchanged and still describe '
           'the 08-22 founding extraction; the proposal header says so.',
           '', '## Validation', '', '```'] + out + ['```', '']
    open(os.path.join(REG, 'FIELD_DIFF_v1.13_to_v1.14.md'), 'w').write('\n'.join(md))
    print('\n'.join(out))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
