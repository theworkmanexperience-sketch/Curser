#!/usr/bin/env python3
"""
Ratification of EPR-001 v1.15.0 - "CHAIRMAN RATIFICATION - EPR-001 v1.15.0", 2026-10-01.
Follows the EPR-001 v1.14.0 ratification precedent (ratify_v1_14.py, commit 096d127): in-place
canonical promotion; the incumbent preserved byte-identical under registries/superseded/ with a
manifest entry; the ratified proposal file left byte-identical as review evidence; the proposal's
PROPOSED markers replaced by a registry_ratification record (prior record kept verbatim).

Inputs are read from git commit f8f74eb (the pushed proposal-custody state), each hash-asserted.
Usage: ratify_v1_15.py [--out-dir DIR]   (default: write in place; DIR = scratch, for the
determinism check, so committed evidence is never rewritten).
TIMELINE v1.1.0 is neither read for writing nor written.
"""
import argparse, hashlib, os, subprocess, sys

REG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
BASE = 'f8f74eb55041e24198844d51582f5f06c16dd027'
R = 'intelligence/p2/registries/'
P_EPR, C_EPR, MAN = 'EMOTIONAL_PROGRESSION_REGISTRY_v1.15.0-PROPOSED.yaml', 'EMOTIONAL_PROGRESSION_REGISTRY.yaml', 'superseded/SUPERSEDED_MANIFEST.yaml'
H = {P_EPR: 'f0650a04ebac81db993c105847aa6cf7bb137080a181d2d0d54fb6da2c260eb7',
     C_EPR: '4aeb1496bb836aab4fd9153cb750fd671b4f326871b7d4d98362054a566047b9',
     MAN: '2f4de09cc8ccada634599257e578c41fdaf6638cf4128ee18182a5d8e20852f3'}
SUP_NEW = 'superseded/EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0.yaml'
DATE = '2026-10-01'
BY = 'Executive Producer / Chairman'
AUTH = 'CHAIRMAN RATIFICATION - EPR-001 v1.15.0, 2026-10-01'
ADDC = 'docs/rulings/EO-2026-09-29_ADDENDUM_C_EPR07_Retirement_Rationale_Correction.md'
SCOPE = ['PBC-1 = RESOLVED_BY_RETIREMENT, resolved 2026-08-28;',
         'PBC-1 retains the caveat that the original support question was not substantively answered;',
         'PBC-1 cites the EPR-07 Retirement Rationale Correction / Addendum C;',
         'EPR-07 remains RETIRED;',
         "EPR-07's original historical text remains unchanged;",
         'the obsolete outside-runtime rationale is corrected by Addendum C rather than overwritten;',
         'PBC-2 = RESOLVED;',
         'PBC-3 remains unresolved, with no episode/segment assignment made;',
         'PBC-4 = RESOLVED;',
         'PBC-5 remains unchanged;',
         'all seven beat entries remain substantively identical to ratified v1.14.0;',
         'segment_authority, segment_authority_status, and the segment-authority note remain unchanged;',
         'the EPR segment_ref → timecode prohibition remains in force.']


def git_bytes(rel):
    return subprocess.run(['git', 'show', f'{BASE}:./{rel}'], cwd=ROOT, capture_output=True, check=True).stdout


def asserted(key, b):
    if hashlib.sha256(b).hexdigest() != H[key]:
        sys.exit(f'STOP FAILED_SOURCE_IDENTITY {key}')
    return b


def once(t, a, b):
    if t.count(a) != 1:
        sys.exit(f'STOP anchor x{t.count(a)}: {a[:80]!r}')
    return t.replace(a, b)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out-dir', default=REG); a = ap.parse_args()
    prop = asserted(P_EPR, git_bytes(R + P_EPR))
    if hashlib.sha256(open(os.path.join(REG, P_EPR), 'rb').read()).hexdigest() != H[P_EPR]:
        sys.exit('STOP: working-tree proposal differs from the ratified proposal bytes')
    inc = asserted(C_EPR, git_bytes(R + C_EPR))
    man = asserted(MAN, git_bytes(R + MAN)).decode()
    t = prop.decode()

    # 1 - PROPOSED banner off: the header returns to the v1.14.0 header exactly
    t = once(t, '# ============================================================================\n'
                '# STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION\n'
                '# EPR-001 v1.15.0-PROPOSED. v1.14.0 (EMOTIONAL_PROGRESSION_REGISTRY.yaml) is\n'
                '# unchanged and remains the RATIFIED registry until the Chairman rules.\n'
                '# ============================================================================\n', '')
    # 2 - version / proposal_status / the proposal's hold block (moved into the ratification record)
    i = t.index('registry_version: "1.15.0-PROPOSED"\n'); j = t.index('registry_ratification:\n', i)
    head = t[i:j]
    rt_lines = head.split('regeneration_trigger:\n', 1)[1]
    if 'proposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n' not in head:
        sys.exit('STOP: proposal_status not where expected')
    t = t[:i] + 'registry_version: "1.15.0"\n' + t[j:]
    # 3 - registry_ratification: v1.15.0 record; v1.14.0 record kept verbatim as prior
    k0 = t.index('registry_ratification:\n'); k1 = t.index('registry_version_note_1_15_0_PROPOSED: >-\n')
    prior = t[k0 + len('registry_ratification:\n'):k1]
    rec = ('registry_ratification:\n'
           '  status: RATIFIED\n'
           f"  ratified: '{DATE}'\n"
           f'  ratified_by: "{BY}"\n'
           f'  authority: "{AUTH}"\n'
           '  version: "1.15.0"\n'
           f'  ratified_artifact: {{file: "{P_EPR}", sha256: "{H[P_EPR]}", commit: "{BASE}"}}\n'
           '  ratified_change: >-\n'
           '    PROPOSED banner, proposal_status and version suffix removed; version note key de-suffixed;\n'
           '    the proposal\'s top-level regeneration_trigger (v1.15.0 HOLD) carried into this record; this\n'
           '    block updated (v1.14.0 record kept verbatim below). No entry, path_b_consequences record or\n'
           '    other field changed from the ratified proposal.\n'
           '  scope_verbatim:\n' + ''.join(f'    - "{x}"\n' for x in SCOPE) +
           '  regeneration_trigger:\n' + ''.join('  ' + l + '\n' for l in rt_lines.rstrip('\n').split('\n')) +
           f'  supersedes: {{version: "1.14.0", sha256: "{H[C_EPR]}", preserved_at: "intelligence/p2/registries/{SUP_NEW}", source_commit: "{BASE}"}}\n'
           '  prior_ratification_1_14_0:\n' + ''.join('  ' + l + '\n' for l in prior.rstrip('\n').split('\n')))
    t = t[:k0] + rec + t[k1:]
    t = once(t, 'registry_version_note_1_15_0_PROPOSED: >-\n  1.14.0 -> 1.15.0-PROPOSED, 2026-10-01.',
             'registry_version_note_1_15_0: >-\n  RATIFIED 2026-10-01 by the Chairman (proposal sha256 '
             f'{H[P_EPR][:16]}..., commit f8f74eb); proposal text follows unaltered. 1.14.0 -> 1.15.0-PROPOSED, 2026-10-01.')
    canon = t.encode()

    # 4 - manifest: one entry appended; existing entries and lines untouched
    entry = ('  - file: EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0.yaml\n'
             '    original_path: intelligence/p2/registries/EMOTIONAL_PROGRESSION_REGISTRY.yaml\n'
             '    version: "1.14.0"\n'
             f'    sha256: "{H[C_EPR]}"\n'
             f'    source_commit: "{BASE}"\n'
             '    ratified_at: "096d127"\n'
             '    status: SUPERSEDED\n'
             f'    superseded_by: {{version: "1.15.0", sha256: "{hashlib.sha256(canon).hexdigest()}", date: "{DATE}", authority: "{AUTH}"}}\n')
    man = once(man, '\nauthority: "', '\n' + entry + 'authority: "')

    out = a.out_dir
    os.makedirs(os.path.join(out, 'superseded'), exist_ok=True)
    open(os.path.join(out, SUP_NEW), 'wb').write(inc)
    open(os.path.join(out, C_EPR), 'wb').write(canon)
    open(os.path.join(out, MAN), 'w', encoding='utf-8').write(man)
    for f in (SUP_NEW, C_EPR, MAN):
        print(hashlib.sha256(open(os.path.join(out, f), 'rb').read()).hexdigest(), f)


if __name__ == '__main__':
    main()
