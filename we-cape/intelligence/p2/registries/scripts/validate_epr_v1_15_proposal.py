#!/usr/bin/env python3
"""Validates EPR-001 v1.15.0-PROPOSED against ratified v1.14.0 (git 096d127). Read-only except one
deterministic rebuild and writing FIELD_DIFF_v1.14_to_v1.15.md. Exit 1 on any failure."""
import hashlib, os, re, subprocess, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
sys.path.insert(0, HERE); import build_epr_v1_15_proposal as B
out, fails = [], []
def check(n, ok, d=''):
    out.append(f'{"PASS" if ok else "FAIL"}  {n}' + (f'  -  {d}' if d else '')); ok or fails.append(n)
sha = lambda b: hashlib.sha256(b).hexdigest()
gb = lambda rel, c=B.BASE: subprocess.run(['git', 'show', f'{c}:./{rel}'], cwd=ROOT, capture_output=True, check=True).stdout

def diff(a, b, p=''):
    if isinstance(a, dict) and isinstance(b, dict):
        r = [('REMOVED', f'{p}.{k}') for k in a if k not in b]
        for k in a:
            if k in b: r += diff(a[k], b[k], f'{p}.{k}')
        return r + [('ADDED', f'{p}.{k}') for k in b if k not in a]
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        r = []
        for i, (x, y) in enumerate(zip(a, b)): r += diff(x, y, f'{p}[{i}]')
        return r
    return [] if a == b else [('CHANGED', p)]

def keys(o, acc):
    if isinstance(o, dict):
        for k, v in o.items(): acc.add(k); keys(v, acc)
    elif isinstance(o, list):
        for v in o: keys(v, acc)
    return acc

def pbc_blocks(text):
    s = text[text.index('path_b_consequences:\n'):]
    parts = re.split(r'(?=^  - id: PBC-\d)', s, flags=re.M)[1:]
    return {p.split('\n', 1)[0].split()[-1]: p for p in parts}

def main():
    old_b = gb(B.SRC); new_b = open(B.OUT, 'rb').read()
    check('V0 base v1.14.0 (git 096d127) hash', sha(old_b) == B.SRC_SHA)
    check('V0 working-tree canonical EPR v1.14.0 unmodified', sha(open(os.path.join(ROOT, B.SRC), 'rb').read()) == B.SRC_SHA)
    check('V0 canonical TIMELINE v1.1.0 unmodified', sha(open(os.path.join(REG, 'TIMELINE_REGISTRY.yaml'), 'rb').read()) == B.TL_SHA)
    old, new = yaml.safe_load(old_b), yaml.safe_load(new_b)
    check('V1 proposal parses', isinstance(new, dict))
    check('V1 registry_version 1.15.0-PROPOSED; proposal_status PROPOSED',
          new['registry_version'] == '1.15.0-PROPOSED' and new['proposal_status'] == 'PROPOSED — AWAITING CHAIRMAN RATIFICATION')

    d = diff(old, new)
    pbc_added = {('ADDED', f'.path_b_consequences[{i}].{k}') for i, ks in
                 ((0, ('status', 'resolved', 'resolution', 'resolved_by', 'note')), (1, ('status', 'resolved', 'resolution', 'resolved_by')),
                  (2, ('note',)), (3, ('status', 'resolved', 'resolution', 'resolved_by'))) for k in ks}
    allowed = pbc_added | {('CHANGED', '.registry_version'), ('ADDED', '.proposal_status'), ('ADDED', '.regeneration_trigger'),
                           ('ADDED', '.registry_version_note_1_15_0_PROPOSED')}
    check('V2 field diff == authorized set exactly', set(d) == allowed, f'{len(d)} changes')

    ob, nb = pbc_blocks(old_b.decode()), pbc_blocks(new_b.decode())
    for pid in ('PBC-1', 'PBC-2', 'PBC-3', 'PBC-4'):
        orig = ob[pid].rstrip('\n')
        check(f'V3 {pid} original lines byte-identical (preserved as prefix)', nb[pid].startswith(orig + '\n'))
    check('V3 PBC-5 block BYTE-identical', ob['PBC-5'] == nb['PBC-5'])
    for i in range(5):
        for k in ('condition', 'detail', 'disposition', 'owner'):
            check(f'V3 PBC-{i+1}.{k} unchanged', old['path_b_consequences'][i][k] == new['path_b_consequences'][i][k])

    pb = {p['id']: p for p in new['path_b_consequences']}
    check('V4 PBC-1 status RESOLVED_BY_RETIREMENT', pb['PBC-1'].get('status') == 'RESOLVED_BY_RETIREMENT')
    check('V4 PBC-2 status RESOLVED', pb['PBC-2'].get('status') == 'RESOLVED')
    check('V4 PBC-3 UNRESOLVED: no status added; disposition/owner unchanged',
          'status' not in pb['PBC-3'] and pb['PBC-3']['disposition'] == 'NOT_DERIVABLE_WITHOUT_REGENERATION')
    check('V4 PBC-3 note separates obsolete premise from current condition; no assignment',
          all(s in pb['PBC-3']['note'] for s in ('HISTORICAL PREMISE, NO LONGER TRUE', 'CURRENT CONDITION', 'remains UNRESOLVED',
                                                  'No assignment')))
    check('V4 PBC-4 status RESOLVED', pb['PBC-4'].get('status') == 'RESOLVED')
    check('V4 PBC-1 resolution carries the not-substantively-answered caveat', 'does NOT assert' in pb['PBC-1']['resolution'])
    check("V4 PBC-1 resolved date == governing ruling date (EPR-07 retirement.adjudicated)",
          pb['PBC-1']['resolved'] == [e for e in old['entries'] if e['id'] == 'EPR-07'][0]['retirement']['adjudicated'] == '2026-08-28')
    n1 = ' '.join(pb['PBC-1']['note'].split())
    check('V4 PBC-1 note: EPR-07 remains retired / rationale corrected / not reinstated / cites Addendum C + evidence',
          all(s in n1 for s in ('EPR-07 REMAINS RETIRED', 'CORRECTED by the G8-ratified re-derivation', 'does NOT reinstate EPR-07',
                                'EO-2026-09-29_ADDENDUM_C_EPR07_Retirement_Rationale_Correction.md', 'S19 row', '5bd4af48')))
    e7o = [e for e in old['entries'] if e['id'] == 'EPR-07'][0]; e7n = [e for e in new['entries'] if e['id'] == 'EPR-07'][0]
    check('V4 EPR-07 entry (incl. retirement, rationale_verbatim, segment_reference_status) unchanged',
          e7o == e7n and e7n['retirement']['disposition'] == 'RETIRE' and e7n['segment_reference_status'] == 'RESOLVED_BY_RETIREMENT')
    adc = os.path.join(ROOT, 'docs', 'rulings', 'EO-2026-09-29_ADDENDUM_C_EPR07_Retirement_Rationale_Correction.md')
    a = open(adc).read() if os.path.exists(adc) else ''
    check('V4 Addendum C exists and distinguishes operative disposition from historical rationale',
          all(s in a for s in ('OPERATIVE DISPOSITION: UNCHANGED', 'EPR-07 REMAINS RETIRED', 'HISTORICAL RATIONALE: SUPERSEDED AS TO FACT',
                               'does not itself rescind', '5bd4af486e9eb745660504b41290154fb5d8c0b511b6bc74cca5102dd4b0a28b')))

    vocab_keys = keys(old, set())
    added_keys = {p.rsplit('.', 1)[1] for o, p in d if o == 'ADDED' and p.startswith('.path_b_consequences')}
    rt_keys = set(new['regeneration_trigger'])
    check('V5 every added PBC field name already exists in v1.14.0', added_keys <= vocab_keys, str(sorted(added_keys)))
    check('V5 regeneration_trigger structure == v1.14.0 established structure',
          rt_keys == set(old['registry_ratification']['regeneration_trigger']), str(sorted(rt_keys)))
    tokens = set(re.findall(r'\b[A-Z][A-Z_]{3,}\b', old_b.decode()))
    used = {pb['PBC-1']['status'], pb['PBC-2']['status'], pb['PBC-4']['status'], new['regeneration_trigger']['disposition']}
    check('V5 every status/disposition token used already exists in v1.14.0', used <= tokens, str(sorted(used)))

    rt = new['regeneration_trigger']
    check('V6 v1.15.0 HOLD recorded (new, not inherited)', rt['disposition'] == 'HELD' and rt['increment'] == '1.14.0 -> 1.15.0'
          and 'PBC LIFECYCLE RECONCILIATION' in rt['authority'] and rt['executed'].startswith('NO'))
    check('V6 v1.14.0 ratification record (incl. its hold) unchanged', new['registry_ratification'] == old['registry_ratification'])

    check('V7 all seven beat entries deep-equal to v1.14.0', new['entries'] == old['entries'] and len(new['entries']) == 7)
    for k in ('segment_authority', 'segment_authority_status', 'segment_authority_note', 'intensity_scale', 'production_identity',
              'governing_invariants', 'prohibited_fields', 'field_definitions', 'undeclared_segments', 'precondition_contract'):
        check(f'V7 unchanged: {k}', new.get(k) == old.get(k))
    check('V7 safety rule still present', 'No consumer may resolve an EPR segment_ref to a timecode' in new['segment_authority_note'])

    added_text = ''.join(nb[p][len(ob[p].rstrip('\n')):] for p in ('PBC-1', 'PBC-2', 'PBC-3', 'PBC-4')) + \
        new['registry_version_note_1_15_0_PROPOSED'] + yaml.safe_dump(new['regeneration_trigger'])
    check('V8 no timecode-shaped text added', not re.search(r'\b\d{1,2}:\d{2}', added_text))

    tl = yaml.safe_load(open(os.path.join(REG, 'TIMELINE_REGISTRY.yaml')))
    refs = {r for e in new['entries'] for r in e['segment_refs']}
    check('V9 every segment_ref resolves in TIMELINE v1.1.0', refs <= {s['id'] for s in tl['segments']})

    lines = subprocess.run(['git', 'status', '--porcelain=v1', '--untracked-files=all', '--', '.'], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.splitlines()
    prefix = subprocess.run(['git', 'rev-parse', '--show-prefix'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    got = {(l[:2], l[3:].strip('"')[len(prefix):] if l[3:].strip('"').startswith(prefix) else l[3:].strip('"'))
           for l in lines}
    got = {g for g in got if not g[1].startswith('Claude outputs/')}
    r = 'intelligence/p2/registries/'
    exp = {('??', 'docs/rulings/EO-2026-09-29_ADDENDUM_C_EPR07_Retirement_Rationale_Correction.md')} | {('??', r + f) for f in ('EMOTIONAL_PROGRESSION_REGISTRY_v1.15.0-PROPOSED.yaml', 'scripts/build_epr_v1_15_proposal.py',
                                   'scripts/validate_epr_v1_15_proposal.py', 'FIELD_DIFF_v1.14_to_v1.15.md',
                                   'VALIDATION_v1.15.0-PROPOSED.txt')}
    check('V10 no change outside the authorized file set', got <= exp, str(sorted(got - exp)) if got - exp else f'{len(got)} new files')
    check('V10 no tracked file modified', not any(c[0] != '??' for c in got))

    h = sha(new_b)
    subprocess.run([sys.executable, os.path.join(HERE, 'build_epr_v1_15_proposal.py')], check=True, capture_output=True)
    check('V11 build deterministic (rebuild identical)', sha(open(B.OUT, 'rb').read()) == h)

    out.extend(['', f'EPR-001 v1.15.0-PROPOSED  sha256 {h}', f'RESULT: {"ALL PASS" if not fails else "FAIL: " + ", ".join(fails)}'])
    md = ['# FIELD DIFF — EPR-001 v1.14.0 → v1.15.0-PROPOSED (PBC lifecycle reconciliation)', '',
          f'**Status: PROPOSED — AWAITING CHAIRMAN RATIFICATION.** Base: ratified v1.14.0 `{B.SRC_SHA}` (commit 096d127). '
          f'Proposal: `{h}`. Generated by `scripts/validate_epr_v1_15_proposal.py` from parsed YAML.', '',
          f'## {len(d)} field changes (authorized set: exactly these)', '', '| op | field | new value |', '|---|---|---|']
    for o, p in sorted(d, key=lambda x: x[1]):
        node = new
        for part in re.findall(r'\.([A-Za-z0-9_]+)|\[(\d+)\]', p):
            node = node[part[0]] if part[0] else node[int(part[1])]
        v = ' '.join(str(node).split())
        md.append(f'| {o} | `{p}` | {v[:150] + ("…" if len(v) > 150 else "")} |')
    md += ['', 'Also added: a 5-line PROPOSED status banner (YAML comments).', '',
           '**Unchanged (verified):** every existing PBC line (condition, detail, disposition, owner; PBC-4 '
           'disposition_token_note) byte-identical; PBC-5 block byte-identical; all 7 entries; segment_authority, '
           'segment_authority_status, segment_authority_note (safety rule); intensity_scale; registry_ratification (v1.14.0 '
           'record and its hold); every other field.', '', '## Validation', '', '```'] + out + ['```', '']
    open(os.path.join(REG, 'FIELD_DIFF_v1.14_to_v1.15.md'), 'w').write('\n'.join(md))
    print('\n'.join(out)); sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
