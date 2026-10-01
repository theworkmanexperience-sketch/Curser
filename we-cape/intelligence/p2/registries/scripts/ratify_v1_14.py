#!/usr/bin/env python3
"""
Ratification of TIMELINE v1.1.0 and EPR-001 v1.14.0 - Chairman authorization 2026-10-01
("CHAIRMAN AUTHORIZATION - RATIFICATION WORKING-TREE EXECUTION", following "CHAIRMAN GOVERNANCE
RULING - PRE-RATIFICATION").

Procedure: in-place canonical promotion (EPR-001 v1.13.0 precedent, c7b5d3a) PLUS byte-identical
preserved copies of the superseded incumbents under registries/superseded/ (Chairman ruling 3).

Every input is read from git commit c9fa343 (the pushed, reviewed state) or from the two ratified
proposal files, each hash-asserted, so this script is idempotent and re-running it reproduces the
same bytes. Text-level edits, each asserted to match exactly once. PBC-2 is carried byte-identically.
The two -PROPOSED files are read, never written.
"""
import hashlib, os, subprocess, sys

REG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
BASE = 'c9fa34327de289905bc9cbfb2f1001a58a28c94f'
DATE = '2026-10-01'
BY = 'Executive Producer / Chairman'
AUTH = ('CHAIRMAN GOVERNANCE RULING - PRE-RATIFICATION and CHAIRMAN AUTHORIZATION - RATIFICATION '
        'WORKING-TREE EXECUTION, 2026-10-01')
P_TL, P_EPR = 'TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml', 'EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0-PROPOSED.yaml'
C_TL, C_EPR = 'TIMELINE_REGISTRY.yaml', 'EMOTIONAL_PROGRESSION_REGISTRY.yaml'
PDR = os.path.join('docs', 'pdr', 'PDR-2026-08-22-ESS-001_S16_Label_vs_Observed_Illumination.md')
H = {P_TL: 'd89ca46159e6850cfbc842e75c623de041c43e3455583dc99e3610192c9496cd',
     P_EPR: '3a04b5e60d8c133d5533cdfc47d12b722d9d454f1dd2d370b08f1ec7d558d2ac',
     C_TL: '34bd0f9ef7f1507cd8fa0f0745abadd675060b313d98d06ea2dd35c98bc8de76',
     C_EPR: '1d54e674190eef8122f7ddd22af66ae07abcb13dead7f5077ed868c37dbe21a4',
     PDR: 'f4453f06727d8fa1d37dd2bce731f347663835eca9721775e17b0951979d36c6'}
SUP = os.path.join(REG, 'superseded')
SCOPE = ['Accept the regenerated v2-mapped spans and finalized Chairman rulings R1-R9.',
         'Accept the finalized S14 R6 replacement endpoint.',
         'Accept S16 interview_count: 7.',
         'Accept S16 participants: [R68-R74].',
         'Accept R9 as MOOT, with no A2 segment and no beat membership created.']
NOT_ADJ = ['PBC-2 (byte-identical)',
           'historical/extraction references to R75 or R68-R75 outside the proposal set',
           'PDR-2026-08-22-ESS-001 (open; notice only)']


def git_bytes(rel):
    return subprocess.run(['git', 'show', f'{BASE}:./{rel}'], cwd=ROOT, capture_output=True, check=True).stdout


def asserted(key, b):
    got = hashlib.sha256(b).hexdigest()
    if got != H[key]:
        sys.exit(f'STOP FAILED_SOURCE_IDENTITY {key}: expected {H[key]}, measured {got}')
    return b


def once(t, a, b):
    if t.count(a) != 1:
        sys.exit(f'STOP anchor x{t.count(a)}: {a[:80]!r}')
    return t.replace(a, b)


def yl(items, ind):
    return ''.join(f'{ind}- "{x}"\n' for x in items)


def main():
    rel = lambda f: os.path.join('intelligence', 'p2', 'registries', f)
    tl = asserted(P_TL, open(os.path.join(REG, P_TL), 'rb').read()).decode()
    epr = asserted(P_EPR, open(os.path.join(REG, P_EPR), 'rb').read()).decode()
    old_tl = asserted(C_TL, git_bytes(rel(C_TL)))
    old_epr = asserted(C_EPR, git_bytes(rel(C_EPR)))
    pdr = asserted(PDR, git_bytes(PDR)).decode()

    # ---------- preserved superseded copies (byte-identical) ----------
    os.makedirs(SUP, exist_ok=True)
    open(os.path.join(SUP, 'TIMELINE_REGISTRY_v1.0.0.yaml'), 'wb').write(old_tl)
    open(os.path.join(SUP, 'EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml'), 'wb').write(old_epr)

    # ---------- TIMELINE v1.1.0 ----------
    cut = tl.index('registry_id: TIMELINE_REGISTRY\n')
    tl = ('# ============================================================================\n'
          '# TIMELINE_REGISTRY v1.1.0 - RATIFIED by the Chairman 2026-10-01 (registry_ratification below).\n'
          '# Segment authority for EPR-001 v1.14.0. Complete 08-24 rebase from the Chairman\'s final B-5\n'
          '# dispositions (R1-R9) and the G8-ratified v2 mapping. S01-S18 in 08-24 seconds (millisecond\n'
          '# representation); S19 (EPR-07 RETIRED) untouched, in 08-22 seconds. sources / delta_note /\n'
          '# etc_anchors still describe the 08-22 founding extraction. Superseded v1.0.0 preserved\n'
          '# byte-identical at superseded/TIMELINE_REGISTRY_v1.0.0.yaml.\n'
          '# ============================================================================\n' + tl[cut:])
    tl = once(tl, 'registry_version: 1.1.0-PROPOSED\n', 'registry_version: 1.1.0\n')
    tl = once(tl, 'proposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n',
              'registry_ratification:\n'
              '  status: RATIFIED\n'
              f"  ratified: '{DATE}'\n"
              f'  ratified_by: "{BY}"\n'
              f'  authority: "{AUTH}"\n'
              '  version: "1.1.0"\n'
              f'  ratified_artifact: {{file: "{P_TL}", sha256: "{H[P_TL]}", commit: "{BASE}"}}\n'
              '  ratified_change: "PROPOSED banner, proposal_status and version suffix removed; this block added. No segment, span, row or changelog value changed."\n'
              '  scope_verbatim:\n' + yl(SCOPE, '    ') +
              '  not_adjudicated:\n' + yl(NOT_ADJ, '    ') +
              '  segment_authority_for: "EPR-001 v1.14.0 (segment_authority_status: RATIFIED)"\n'
              f'  supersedes: {{version: "1.0.0", sha256: "{H[C_TL]}", preserved_at: "intelligence/p2/registries/superseded/TIMELINE_REGISTRY_v1.0.0.yaml", source_commit: "{BASE}"}}\n'
              '  version_number_note: >-\n'
              '    PDR-2026-08-22-ESS-001 (OPEN) does not reserve v1.1.0. Ratifying this rebase as v1.1.0 is\n'
              '    permitted (Chairman ruling 4). If that PDR later selects its relabel Option B, the minor\n'
              '    transition is from the then-current v1.1.0 to v1.2.0. The PDR is not resolved here.\n')

    # ---------- EPR-001 v1.14.0 ----------
    banner = ('# ============================================================================\n'
              '# STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION\n'
              '# EPR-001 v1.14.0-PROPOSED. v1.13.0 (EMOTIONAL_PROGRESSION_REGISTRY.yaml) is\n'
              '# unchanged and remains the RATIFIED registry until the Chairman rules.\n'
              '# ============================================================================\n')
    epr = once(epr, banner, '')
    epr = once(epr, 'registry_version: "1.14.0-PROPOSED"\nproposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n',
               'registry_version: "1.14.0"\n')
    i = epr.index("registry_ratification:\n  status: RATIFIED\n  ratified: '2026-08-28'\n")
    j = epr.index('registry_version_note_1_14_0_PROPOSED: >-\n')
    prior = epr[i + len('registry_ratification:\n'):j]
    epr = epr[:i] + (
        'registry_ratification:\n'
        '  status: RATIFIED\n'
        f"  ratified: '{DATE}'\n"
        f'  ratified_by: "{BY}"\n'
        f'  authority: "{AUTH}"\n'
        '  version: "1.14.0"\n'
        f'  ratified_artifact: {{file: "{P_EPR}", sha256: "{H[P_EPR]}", commit: "{BASE}"}}\n'
        '  ratified_change: >-\n'
        '    PROPOSED banner, proposal_status and version suffix removed; version note key de-suffixed;\n'
        '    this block updated (v1.13.0 record kept verbatim below); segment_authority,\n'
        '    segment_authority_status and segment_authority_note set by Chairman ruling 1. No entry,\n'
        '    no path_b_consequences record (PBC-2 byte-identical) and no other field changed.\n'
        '  scope_verbatim:\n' + yl(SCOPE, '    ') +
        '  not_adjudicated:\n' + yl(NOT_ADJ, '    ') +
        '  regeneration_trigger:\n'
        '    rule: "ratification order section 4.5 - a registry_version increment is the regeneration trigger"\n'
        '    increment: "1.13.0 -> 1.14.0"\n'
        '    disposition: HELD\n'
        f'    authority: "Chairman, CHAIRMAN GOVERNANCE RULING - PRE-RATIFICATION, {DATE}"\n'
        '    reason_verbatim: "this ratification is itself the completion of the authorized rebase/regeneration cycle, and immediately firing another regeneration solely because the ratified version increments would create a recursive second cycle without new source evidence."\n'
        '    executed: "NO - no regeneration was run"\n'
        f'  supersedes: {{version: "1.13.0", sha256: "{H[C_EPR]}", preserved_at: "intelligence/p2/registries/superseded/EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml", source_commit: "{BASE}"}}\n'
        '  prior_ratification_1_13_0:\n' +
        ''.join('  ' + l + '\n' for l in prior.rstrip('\n').split('\n'))) + epr[j:]
    epr = once(epr, 'registry_version_note_1_14_0_PROPOSED: >-\n  1.13.0 -> 1.14.0-PROPOSED, 2026-10-01.',
               'registry_version_note_1_14_0: >-\n  RATIFIED 2026-10-01 by the Chairman (proposal sha256 '
               f'{H[P_EPR][:16]}..., commit c9fa343); proposal text follows unaltered. '
               '1.13.0 -> 1.14.0-PROPOSED, 2026-10-01.')
    epr = once(epr, 'segment_authority: "TIMELINE_REGISTRY v1.0.0 (S01-S19)"\n'
                    'segment_authority_status: SUPERSEDED_PENDING_REDERIVATION\n',
               'segment_authority: "TIMELINE_REGISTRY v1.1.0 (S01-S19)"\n'
               'segment_authority_status: RATIFIED\n')
    k0 = epr.index('segment_authority_note: >-\n'); k1 = epr.index('missing_data_policy:', k0)
    epr = epr[:k0] + (
        'segment_authority_note: >-\n'
        '  TIMELINE_REGISTRY v1.1.0, ratified by the Chairman 2026-10-01, is the segment authority. Its\n'
        '  S01-S18 spans are positions in the governed 08-24 production, re-derived mechanically from the\n'
        '  ED-003 picture lock under EO-2026-09-29 (D-2, Addenda A and B) through the G8-ratified v2\n'
        "  mapping and the Chairman's dispositions R1-R9; S19 is unchanged. Its segment IDENTIFIERS\n"
        '  (S01-S19) remain the keys this registry is written against and are unchanged.\n'
        '  TIMELINE_REGISTRY v1.0.0, pinned to the 08-22 assembly, is SUPERSEDED and preserved\n'
        '  byte-identical at intelligence/p2/registries/superseded/TIMELINE_REGISTRY_v1.0.0.yaml.\n'
        '  No consumer may resolve an EPR segment_ref to a timecode until the Chairman rules otherwise;\n'
        '  this ratification establishes the governing segment authority and does not authorize\n'
        '  EPR-to-timecode resolution.\n') + epr[k1:]

    # ---------- manifest ----------
    tl_b, epr_b = tl.encode(), epr.encode()
    man = ('# Preserved superseded canonical registries. Byte-identical copies; NEVER edit these files.\n'
           f'# Chairman ruling 3 (CHAIRMAN GOVERNANCE RULING - PRE-RATIFICATION, {DATE}).\n'
           'manifest_id: REGISTRY_SUPERSEDED_MANIFEST\n'
           'entries:\n'
           '  - file: TIMELINE_REGISTRY_v1.0.0.yaml\n'
           '    original_path: intelligence/p2/registries/TIMELINE_REGISTRY.yaml\n'
           '    version: "1.0.0"\n'
           f'    sha256: "{H[C_TL]}"\n'
           f'    source_commit: "{BASE}"\n'
           '    introduced_at: "67fcd91"\n'
           '    status: SUPERSEDED\n'
           f'    superseded_by: {{version: "1.1.0", sha256: "{hashlib.sha256(tl_b).hexdigest()}", date: "{DATE}"}}\n'
           '  - file: EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml\n'
           '    original_path: intelligence/p2/registries/EMOTIONAL_PROGRESSION_REGISTRY.yaml\n'
           '    version: "1.13.0"\n'
           f'    sha256: "{H[C_EPR]}"\n'
           f'    source_commit: "{BASE}"\n'
           '    ratified_at: "c7b5d3a"\n'
           '    status: SUPERSEDED\n'
           f'    superseded_by: {{version: "1.14.0", sha256: "{hashlib.sha256(epr_b).hexdigest()}", date: "{DATE}"}}\n'
           f'authority: "{AUTH}"\n')

    # ---------- PDR notice (additive; issued text preserved) ----------
    pdr = pdr.rstrip('\n') + '\n' + (
        '\n---\n\n'
        '> **NOTICE (2026-10-01, Chairman ruling 4; issued text above preserved unaltered; this PDR is NOT resolved).**\n'
        '> - **v1.1.0 is not reserved by this PDR.** Option B\'s "TIMELINE_REGISTRY 1.0.0 → 1.1.0" describes the\n'
        '>   minor bump a relabel would require, counted from the version then in force.\n'
        '> - **TIMELINE_REGISTRY v1.1.0 has been ratified (2026-10-01) as the B-5 08-24 rebase.** That ratification\n'
        '>   does not resolve this PDR; `activity: bike_night_arrivals` is unchanged.\n'
        '> - **If Option B is later selected,** the applicable minor-version transition is from the then-current\n'
        '>   **v1.1.0 to v1.2.0**.\n'
        '> - **This PDR\'s substantive evidence and decision remain open.** (Its spans and measurements were taken on\n'
        '>   the 08-22 assembly; under the 08-24 rebase S16 is a different span - recorded as fact, not as disposition.)\n')

    open(os.path.join(REG, C_TL), 'wb').write(tl_b)
    open(os.path.join(REG, C_EPR), 'wb').write(epr_b)
    open(os.path.join(SUP, 'SUPERSEDED_MANIFEST.yaml'), 'w', encoding='utf-8').write(man)
    open(os.path.join(ROOT, PDR), 'w', encoding='utf-8').write(pdr)
    for p in (os.path.join(REG, C_TL), os.path.join(REG, C_EPR), os.path.join(SUP, 'TIMELINE_REGISTRY_v1.0.0.yaml'),
              os.path.join(SUP, 'EMOTIONAL_PROGRESSION_REGISTRY_v1.13.0.yaml'), os.path.join(SUP, 'SUPERSEDED_MANIFEST.yaml'),
              os.path.join(ROOT, PDR)):
        print(hashlib.sha256(open(p, 'rb').read()).hexdigest(), os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
