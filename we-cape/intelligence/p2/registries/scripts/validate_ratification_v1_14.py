#!/usr/bin/env python3
"""Post-ratification validation for TIMELINE v1.1.0 / EPR-001 v1.14.0. Read-only except for one
idempotence re-run of ratify_v1_14.py (which must reproduce identical bytes). Exit 1 on any failure."""
import hashlib, os, re, subprocess, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
sys.path.insert(0, HERE); import ratify_v1_14 as R
out, fails = [], []
def check(n, ok, d=''):
    out.append(f'{"PASS" if ok else "FAIL"}  {n}' + (f'  -  {d}' if d else '')); ok or fails.append(n)
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, 'rb').read()
gb = lambda rel: subprocess.run(['git', 'show', f'{R.BASE}:./{rel}'], cwd=ROOT, capture_output=True, check=True).stdout
RREL = lambda f: os.path.join('intelligence', 'p2', 'registries', f)

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

def block(text, start, end):
    i = text.index(start); return text[i:text.index(end, i)]

def main():
    P = {k: rb(os.path.join(REG, k)) for k in (R.P_TL, R.P_EPR, R.C_TL, R.C_EPR)}
    check('R1 ratified proposal TIMELINE bytes unchanged', sha(P[R.P_TL]) == R.H[R.P_TL])
    check('R1 ratified proposal EPR bytes unchanged', sha(P[R.P_EPR]) == R.H[R.P_EPR])
    check('R1 proposals == committed c9fa343 bytes', P[R.P_TL] == gb(RREL(R.P_TL)) and P[R.P_EPR] == gb(RREL(R.P_EPR)))
    s_tl, s_epr = rb(os.path.join(R.SUP, 'TIMELINE_REGISTRY_v1.0.0.yaml')), rb(os.path.join(R.SUP, 'EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml'))
    check('R2 superseded TIMELINE v1.0.0 copy byte-identical to incumbent', s_tl == gb(RREL(R.C_TL)) and sha(s_tl) == R.H[R.C_TL], sha(s_tl)[:16])
    check('R2 superseded EPR v1.13.0 copy byte-identical to incumbent', s_epr == gb(RREL(R.C_EPR)) and sha(s_epr) == R.H[R.C_EPR], sha(s_epr)[:16])
    man = yaml.safe_load(open(os.path.join(R.SUP, 'SUPERSEDED_MANIFEST.yaml')))
    ok = {e['file']: e for e in man['entries']}
    check('R2 manifest hashes/provenance', ok['TIMELINE_REGISTRY_v1.0.0.yaml']['sha256'] == R.H[R.C_TL]
          and ok['EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml']['sha256'] == R.H[R.C_EPR]
          and ok['TIMELINE_REGISTRY_v1.0.0.yaml']['superseded_by']['sha256'] == sha(P[R.C_TL])
          and ok['EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml']['superseded_by']['sha256'] == sha(P[R.C_EPR]))

    pt, ct = yaml.safe_load(P[R.P_TL]), yaml.safe_load(P[R.C_TL])
    pe, ce = yaml.safe_load(P[R.P_EPR]), yaml.safe_load(P[R.C_EPR])
    old_e = yaml.safe_load(gb(RREL(R.C_EPR)))
    check('R3 canonical files parse', all(isinstance(x, dict) for x in (ct, ce)))
    dt = set(diff(pt, ct))
    check('R4 TIMELINE canonical vs ratified proposal: only ratification fields',
          dt == {('REMOVED', '.proposal_status'), ('CHANGED', '.registry_version'), ('ADDED', '.registry_ratification')}, str(sorted(dt)))
    check('R4 TIMELINE segments + changelog identical to ratified proposal', ct['segments'] == pt['segments'] and ct['changelog'] == pt['changelog'])
    check('R4 TIMELINE version 1.1.0, RATIFIED', ct['registry_version'] == '1.1.0' and ct['registry_ratification']['status'] == 'RATIFIED')
    de = {p for o, p in diff(pe, ce)}
    allowed_top = {'.proposal_status', '.registry_version', '.registry_version_note_1_14_0_PROPOSED', '.registry_version_note_1_14_0',
                   '.segment_authority', '.segment_authority_status', '.segment_authority_note'}
    check('R5 EPR canonical vs ratified proposal: only authorized fields',
          all(p in allowed_top or p.startswith('.registry_ratification') for p in de), str(sorted(de)))
    check('R5 EPR entries deep-equal (proposal and v1.13.0)', ce['entries'] == pe['entries'] == old_e['entries'])
    check('R5 EPR path_b_consequences deep-equal', ce['path_b_consequences'] == old_e['path_b_consequences'])
    pb = lambda t: block(t, '  - id: PBC-2\n', '  - id: PBC-3\n')
    check('R5 PBC-2 BYTE-identical to v1.13.0', pb(P[R.C_EPR].decode()) == pb(gb(RREL(R.C_EPR)).decode()))
    for k in ('production_identity', 'governing_invariants', 'intensity_scale', 'undeclared_segments', 'prohibited_fields', 'field_definitions'):
        check(f'R5 EPR untouched: {k}', ce.get(k) == old_e.get(k))
    check('R5 EPR header identical to v1.13.0 header',
          P[R.C_EPR].decode().split('registry_id:')[0] == gb(RREL(R.C_EPR)).decode().split('registry_id:')[0])
    check('R5 prior v1.13.0 ratification preserved verbatim', ce['registry_ratification']['prior_ratification_1_13_0'] == old_e['registry_ratification'])
    check('R6 segment_authority = "TIMELINE_REGISTRY v1.1.0 (S01-S19)"', ce['segment_authority'] == 'TIMELINE_REGISTRY v1.1.0 (S01-S19)')
    check('R6 segment_authority_status = RATIFIED', ce['segment_authority_status'] == 'RATIFIED')
    n = ce['segment_authority_note']
    check('R6 note: no longer states re-derivation pending', 'PENDING' not in n and 'suspended' not in n)
    check('R6 SAFETY RULE retained', 'No consumer may resolve an EPR segment_ref to a timecode until the Chairman rules otherwise' in n)
    check('R6 note: no timecode-shaped strings (EPR prohibited field)', not re.search(r'\b\d{2}:\d{2}(:\d{2})?', n))
    rt = ce['registry_ratification']['regeneration_trigger']
    check('R7 regeneration trigger HELD, not executed', rt['disposition'] == 'HELD' and rt['executed'].startswith('NO')
          and rt['increment'] == '1.13.0 -> 1.14.0')
    check('R8 segment IDs S01..S19 in canonical TIMELINE (EPR refs resolve)', [s['id'] for s in ct['segments']] == [f'S{i:02d}' for i in range(1, 20)])

    pdr_old, pdr_new = gb(R.PDR).decode(), rb(os.path.join(ROOT, R.PDR)).decode()
    check('R9 PDR notice additive only (issued text preserved as prefix)', pdr_new.startswith(pdr_old.rstrip('\n')) and len(pdr_new) > len(pdr_old))
    check('R9 PDR remains OPEN (status line unchanged)', 'Status: **OPEN — AWAITING EXECUTIVE DISPOSITION**' in pdr_new
          and '> _To be recorded by the Executive Producer._' in pdr_new)
    # R9 (corrected): judge the notice on its issued text with blockquote markers, Markdown emphasis
    # and line wrapping normalised away, bullet by bullet - independent of where lines wrap.
    notice = pdr_new[len(pdr_old.rstrip('\n')):]
    bullets = [' '.join(re.sub(r'[*`]', '', b.replace('\n>', ' ')).split())
               for b in re.split(r'\n> - ', notice)[1:]]
    has = lambda *ts: any(all(t in b for t in ts) for b in bullets)
    check('R9 PDR notice states: v1.1.0 is not reserved by this PDR', has('v1.1.0 is not reserved by this PDR'))
    check('R9 PDR notice states: ratification of TIMELINE v1.1.0 does not resolve this PDR',
          has('TIMELINE_REGISTRY v1.1.0 has been ratified', 'That ratification does not resolve this PDR'))
    check('R9 PDR notice states: Option B transition is v1.1.0 to v1.2.0', has('If Option B is later selected', 'v1.1.0 to v1.2.0'))
    check('R9 PDR notice states: evidence and decision remain open', has("This PDR's substantive evidence and decision remain open"))

    # R10 (corrected): paths relative to the we-cape root (the git toplevel is its parent), every
    # untracked file listed individually; only the pre-existing 'Claude outputs/' directories ignored.
    prefix = subprocess.run(['git', 'rev-parse', '--show-prefix'], cwd=ROOT, capture_output=True, text=True,
                            check=True).stdout.strip()
    lines = subprocess.run(['git', 'status', '--porcelain=v1', '--untracked-files=all', '--', '.'], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.splitlines()
    got = set()
    for l in lines:
        code, path = l[:2], l[3:].strip('"')
        path = path[len(prefix):] if path.startswith(prefix) else path
        if path.startswith('Claude outputs/'):
            continue
        got.add((code, path))
    reg = 'intelligence/p2/registries/'
    exp = {(' M', 'docs/pdr/PDR-2026-08-22-ESS-001_S16_Label_vs_Observed_Illumination.md'),
           (' M', reg + 'EMOTIONAL_PROGRESSION_REGISTRY.yaml'), (' M', reg + 'TIMELINE_REGISTRY.yaml'),
           ('??', reg + 'scripts/ratify_v1_14.py'), ('??', reg + 'scripts/validate_ratification_v1_14.py'),
           ('??', reg + 'superseded/TIMELINE_REGISTRY_v1.0.0.yaml'),
           ('??', reg + 'superseded/EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml'),
           ('??', reg + 'superseded/SUPERSEDED_MANIFEST.yaml'),
           ('??', reg + 'VALIDATION_RATIFICATION_v1.14.0.txt')}
    check('R10 no change outside the authorized file set (we-cape-relative)', got <= exp,
          'unauthorized: ' + str(sorted(got - exp)) if got - exp else f'{len(got)} changes, all authorized')
    check('R10 every authorized ratification change present', got >= exp - {('??', reg + 'VALIDATION_RATIFICATION_v1.14.0.txt')},
          str(sorted(exp - got)))

    before = [sha(rb(os.path.join(REG, f))) for f in (R.C_TL, R.C_EPR)] + [sha(rb(os.path.join(R.SUP, 'SUPERSEDED_MANIFEST.yaml'))), sha(rb(os.path.join(ROOT, R.PDR)))]
    subprocess.run([sys.executable, os.path.join(HERE, 'ratify_v1_14.py')], check=True, capture_output=True)
    after = [sha(rb(os.path.join(REG, f))) for f in (R.C_TL, R.C_EPR)] + [sha(rb(os.path.join(R.SUP, 'SUPERSEDED_MANIFEST.yaml'))), sha(rb(os.path.join(ROOT, R.PDR)))]
    check('R11 ratification deterministic / idempotent (re-run identical)', before == after)

    out.append(''); out.extend([f'TIMELINE v1.1.0  {before[0]}', f'EPR-001 v1.14.0  {before[1]}'])
    out.append(f'RESULT: {"ALL PASS" if not fails else "FAIL: " + ", ".join(fails)}')
    print('\n'.join(out)); sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
