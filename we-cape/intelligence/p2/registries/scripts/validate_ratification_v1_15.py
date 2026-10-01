#!/usr/bin/env python3
"""Post-ratification validation for EPR-001 v1.15.0. WRITE-FREE: reads the working tree and git; its
determinism check rebuilds into a temporary directory. It never rewrites any committed artifact.
Prints the report (redirected by the operator). Exit 1 on any failure."""
import hashlib, os, re, subprocess, sys, tempfile
import yaml

HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
sys.path.insert(0, HERE); import ratify_v1_15 as R
out, fails = [], []
def check(n, ok, d=''):
    out.append(f'{"PASS" if ok else "FAIL"}  {n}' + (f'  -  {d}' if d else '')); ok or fails.append(n)
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, 'rb').read()
gb = lambda rel: subprocess.run(['git', 'show', f'{R.BASE}:./{rel}'], cwd=ROOT, capture_output=True, check=True).stdout

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

def pbc_text(t):
    return t[t.index('path_b_consequences:\n'):]

def main():
    W = lambda f: os.path.join(REG, f)
    prop_b, canon_b, inc_b = rb(W(R.P_EPR)), rb(W(R.C_EPR)), gb(R.R + R.C_EPR)
    check('V0 proposal bytes == ratified proposal (f0650a04) == committed', sha(prop_b) == R.H[R.P_EPR] and prop_b == gb(R.R + R.P_EPR))
    check('V0 incumbent at f8f74eb is EPR v1.14.0 (4aeb1496)', sha(inc_b) == R.H[R.C_EPR])
    sup = rb(W(R.SUP_NEW))
    check('V1 preserved v1.14.0 byte-identical to incumbent', sup == inc_b and sha(sup) == R.H[R.C_EPR], sha(sup)[:16])
    for f, h in (('superseded/TIMELINE_REGISTRY_v1.0.0.yaml', '34bd0f9ef7f1507cd8fa0f0745abadd675060b313d98d06ea2dd35c98bc8de76'),
                 ('superseded/EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml', '1d54e674190eef8122f7ddd22af66ae07abcb13dead7f5077ed868c37dbe21a4')):
        check(f'V1 earlier preserved copy unchanged: {f}', sha(rb(W(f))) == h)
    mo, mn = yaml.safe_load(gb(R.R + R.MAN)), yaml.safe_load(rb(W(R.MAN)))
    check('V1 manifest: existing entries and authority unchanged', mn['entries'][:len(mo['entries'])] == mo['entries']
          and mn['authority'] == mo['authority'] and mn['manifest_id'] == mo['manifest_id'])
    e = mn['entries'][-1]
    check('V1 manifest: one new v1.14.0 entry, hashes linked', len(mn['entries']) == len(mo['entries']) + 1
          and e['sha256'] == R.H[R.C_EPR] and e['superseded_by']['sha256'] == sha(canon_b) and e['superseded_by']['version'] == '1.15.0')
    check('V1 manifest text: append-only', rb(W(R.MAN)).decode().startswith(gb(R.R + R.MAN).decode().split('\nauthority: "')[0]))

    P, C, I = yaml.safe_load(prop_b), yaml.safe_load(canon_b), yaml.safe_load(inc_b)
    check('V2 canonical parses; version 1.15.0', isinstance(C, dict) and C['registry_version'] == '1.15.0')
    d = set(diff(P, C)); top = {p for o, p in d if not p.startswith('.registry_ratification')}
    check('V2 canonical vs ratified proposal: only ratification-procedure fields',
          top == {'.proposal_status', '.regeneration_trigger', '.registry_version', '.registry_version_note_1_15_0_PROPOSED',
                  '.registry_version_note_1_15_0'}, str(sorted(top)))
    check('V2 header identical to v1.14.0 header', canon_b.decode().split('registry_id:')[0] == inc_b.decode().split('registry_id:')[0])
    check('V2 no PROPOSED marker left', 'PROPOSED — AWAITING' not in canon_b.decode() and 'proposal_status' not in C)
    rr = C['registry_ratification']
    check('V3 ratification: RATIFIED 2026-10-01, version 1.15.0', rr['status'] == 'RATIFIED' and rr['ratified'] == '2026-10-01' and rr['version'] == '1.15.0')
    check('V3 linkage: proposal hash -> ratification -> canonical', rr['ratified_artifact']['sha256'] == R.H[R.P_EPR]
          and rr['ratified_artifact']['commit'] == R.BASE and e['superseded_by']['sha256'] == sha(canon_b))
    check('V3 supersedes v1.14.0 (4aeb1496) preserved path', rr['supersedes']['sha256'] == R.H[R.C_EPR]
          and rr['supersedes']['preserved_at'].endswith(R.SUP_NEW))
    check('V3 prior v1.14.0 ratification record preserved verbatim', rr['prior_ratification_1_14_0'] == I['registry_ratification'])
    check('V3 no unauthorized governing_provenance key (Chairman strike ruling)', 'governing_provenance' not in rr
          and 'governing_provenance' not in C and 'governing_provenance' not in canon_b.decode())
    check('V3 Addendum C cited via the approved PBC-1 note', 'EO-2026-09-29_ADDENDUM_C_EPR07_Retirement_Rationale_Correction.md'
          in ' '.join({x['id']: x for x in C['path_b_consequences']}['PBC-1']['note'].split()))
    check('V3 ratification record keys == authorized set', set(rr) == {'status', 'ratified', 'ratified_by', 'authority', 'version',
          'ratified_artifact', 'ratified_change', 'scope_verbatim', 'regeneration_trigger', 'supersedes', 'prior_ratification_1_14_0'},
          str(sorted(rr)))
    check('V3 scope_verbatim == Chairman scope (13 items)', rr['scope_verbatim'] == R.SCOPE)
    h = rr['regeneration_trigger']
    check('V4 v1.15.0 HOLD carried: content == proposal hold block', h == P['regeneration_trigger'])
    check('V4 hold is the v1.15.0 ruling (not the inherited v1.14.0 hold)', h['disposition'] == 'HELD' and h['increment'] == '1.14.0 -> 1.15.0'
          and 'PBC LIFECYCLE RECONCILIATION' in h['authority'] and h != I['registry_ratification']['regeneration_trigger'])
    check('V4 not executed', h['executed'].startswith('NO'))

    check('V5 path_b_consequences deep-equal to proposal', C['path_b_consequences'] == P['path_b_consequences'])
    check('V5 path_b_consequences TEXT byte-identical to proposal', pbc_text(canon_b.decode()) == pbc_text(prop_b.decode()))
    pb = {x['id']: x for x in C['path_b_consequences']}
    check('V5 PBC-1 RESOLVED_BY_RETIREMENT 2026-08-28, caveat + Addendum C', pb['PBC-1']['status'] == 'RESOLVED_BY_RETIREMENT'
          and pb['PBC-1']['resolved'] == '2026-08-28' and 'does NOT assert' in pb['PBC-1']['resolution'] and 'ADDENDUM_C' in pb['PBC-1']['note'])
    check('V5 PBC-2 RESOLVED; PBC-4 RESOLVED', pb['PBC-2']['status'] == 'RESOLVED' and pb['PBC-4']['status'] == 'RESOLVED')
    check('V5 PBC-3 unresolved: no status, no assignment', 'status' not in pb['PBC-3'] and pb['PBC-3']['disposition'] == 'NOT_DERIVABLE_WITHOUT_REGENERATION'
          and 'remains UNRESOLVED' in pb['PBC-3']['note'])
    check('V5 PBC-5 unchanged from v1.14.0', pb['PBC-5'] == {x['id']: x for x in I['path_b_consequences']}['PBC-5'])
    check('V6 entries deep-equal to v1.14.0 and proposal', C['entries'] == I['entries'] == P['entries'])
    e7 = {x['id']: x for x in C['entries']}['EPR-07']
    check('V6 EPR-07 RETIRED, original text unchanged', e7['retirement']['disposition'] == 'RETIRE' and e7 == {x['id']: x for x in I['entries']}['EPR-07'])
    for k in ('segment_authority', 'segment_authority_status', 'segment_authority_note', 'intensity_scale', 'production_identity',
              'governing_invariants', 'prohibited_fields', 'field_definitions', 'undeclared_segments', 'precondition_contract'):
        check(f'V6 unchanged from v1.14.0: {k}', C.get(k) == I.get(k))
    check('V6 safety rule in force', 'No consumer may resolve an EPR segment_ref to a timecode' in C['segment_authority_note'])
    added = canon_b.decode()[canon_b.decode().index('registry_ratification:\n'):canon_b.decode().index('  prior_ratification_1_14_0:')]
    check('V7 no timecode-shaped text in the new ratification record', not re.search(r'\b\d{1,2}:\d{2}', added))
    check('V8 Addendum C unchanged', sha(rb(os.path.join(ROOT, R.ADDC))) == 'e81156fe1cce000725caf53a7f8822c41388f64ecb170d2d26ede2a43fdeabbc')
    check('V8 TIMELINE v1.1.0 unchanged', sha(rb(W('TIMELINE_REGISTRY.yaml'))) == '510697b9bbd1ed01c6c61ab6c6063dd511cfc71abad0ad11629fbeb807db0da3')
    tl = yaml.safe_load(rb(W('TIMELINE_REGISTRY.yaml')))
    check('V8 every segment_ref resolves in TIMELINE v1.1.0', {r for x in C['entries'] for r in x['segment_refs']} <= {s['id'] for s in tl['segments']})
    for f, hh in (('FIELD_DIFF_v1.14_to_v1.15.md', '10f410b5c3814b82f8b1fd8be358fe91a25deef59ed5f90025837c12361cb692'),
                  ('VALIDATION_v1.15.0-PROPOSED.txt', '7c80b8795356d87b9913b13556554e364820bf48ff19855e0d4cf9f0b52a0fce')):
        check(f'V8 proposal evidence unchanged: {f}', sha(rb(W(f))) == hh)

    prefix = subprocess.run(['git', 'rev-parse', '--show-prefix'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    lines = subprocess.run(['git', 'status', '--porcelain=v1', '--untracked-files=all', '--', '.'], cwd=ROOT, capture_output=True,
                           text=True, check=True).stdout.splitlines()
    got = set()
    for l in lines:
        p = l[3:].strip('"'); p = p[len(prefix):] if p.startswith(prefix) else p
        if not p.startswith('Claude outputs/'): got.add((l[:2], p))
    exp = {(' M', R.R + R.C_EPR), (' M', R.R + R.MAN), ('??', R.R + R.SUP_NEW), ('??', R.R + 'scripts/ratify_v1_15.py'),
           ('??', R.R + 'scripts/validate_ratification_v1_15.py'), ('??', R.R + 'VALIDATION_RATIFICATION_v1.15.0.txt')}
    check('V9 no change outside the authorized ratification set', got <= exp, str(sorted(got - exp)) if got - exp else f'{len(got)} changes')

    with tempfile.TemporaryDirectory() as td:
        subprocess.run([sys.executable, os.path.join(HERE, 'ratify_v1_15.py'), '--out-dir', td], check=True, capture_output=True)
        same = all(rb(os.path.join(td, f)) == rb(W(f)) for f in (R.C_EPR, R.MAN, R.SUP_NEW))
    check('V10 ratification deterministic (scratch rebuild byte-identical; nothing rewritten)', same)
    out.extend(['', f'EPR-001 v1.15.0 canonical  sha256 {sha(canon_b)}', f'RESULT: {"ALL PASS" if not fails else "FAIL: " + ", ".join(fails)}'])
    print('\n'.join(out)); sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
