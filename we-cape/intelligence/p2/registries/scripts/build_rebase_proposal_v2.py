#!/usr/bin/env python3
"""
Final rebase proposal - all tiers - from the Chairman's completed dispositions (R1-R9) and the
G8-ratified v2 mapping. Supersedes the Tier-1-only build (build_tier1_rebase_proposal.py, c5a72dc),
which is retained unchanged.

  TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml
      Tier 1 rows (S01 S02 S04-S10 S17 S18): byte-identical to the c5a72dc proposal rows
          (their v2-mapped values equal their v1-mapped values).
      S03 S11 S12 S13 S15 S16: v2-mapped spans; span_basis cites v2 + the final ruling.
      S14: start v2-mapped (3205.701625 s exact -> 3205.702 in ms representation), end the
          Chairman-confirmed picture end 38971/12 s (-> 3247.583); exact rational, frame 77942
          and 00:54:07:14 kept in span_basis and changelog.
      S19 untouched. R9 MOOT: no segment row is created.
  EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0-PROPOSED.yaml
      v1.13.0 + PROPOSED header + version + one changelog entry. No beat value changes.
      PBC-2, segment_authority, segment_authority_status untouched.

REPRESENTATION RULE (Chairman, 2026-10-01): millisecond spans. Representation only; nothing is
snapped, frame-aligned or editorially altered. Text-level edits, each asserted to match exactly once.
"""
import hashlib, json, os, subprocess, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(REG, '..', '..', '..'))
INPUTS = {
    'epr': (os.path.join(REG, 'EMOTIONAL_PROGRESSION_REGISTRY.yaml'),
            '1d54e674190eef8122f7ddd22af66ae07abcb13dead7f5077ed868c37dbe21a4'),
    'timeline': (os.path.join(REG, 'TIMELINE_REGISTRY.yaml'),
                 '34bd0f9ef7f1507cd8fa0f0745abadd675060b313d98d06ea2dd35c98bc8de76'),
    'v2': (os.path.join(REG, '..', 'ess', 'decision_packet_b5_b14', 'v2', 'rederivation_v2.json'),
           '5bd4af486e9eb745660504b41290154fb5d8c0b511b6bc74cca5102dd4b0a28b'),
    'sheet': (os.path.join(ROOT, 'docs', 'rulings', 'AFFECTED_BEAT_DISPOSITION_SHEET.md'),
              '53f7f39940c134f6aed119db82f139266e86b9a2d5b6e65d210dd5623a576e42'),
}
TIER1_PROPOSAL_COMMIT = 'c5a72dc'
TIER1 = ['S01', 'S02', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S17', 'S18']
S14_START_EXACT = Fraction(25645613, 8000)        # 3205.701625 s, v2-mapped (not frame-aligned)
S14_END_EXACT = Fraction(38971, 12)               # 3247.583333.. s, frame 77942, 00:54:07:14
RULING = {  # segment -> (row, decision, commit)
    'S03': ('R1', 'PRESERVE', '2b3416f'), 'S11': ('R2', 'PRESERVE', 'e563b17'),
    'S12': ('R3', 'PRESERVE', '2b45e11'), 'S13': ('R5', 'PRESERVE', '36623ee'),
    'S15': ('R7', 'PRESERVE', '3176446'), 'S16': ('R8', 'PRESERVE', '1a80d2a'),
}
EXTRA = {'S12': '; end = R4-ratified EPR-05->06 transition 3193.167 (a857377)',
         'S13': '; start = R4-ratified EPR-05->06 transition 3193.167 (a857377)'}
OUT_TL = os.path.join(REG, 'TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml')
OUT_EPR = os.path.join(REG, 'EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0-PROPOSED.yaml')
V2 = INPUTS['v2'][1]


def read(key):
    p, want = INPUTS[key]; b = open(p, 'rb').read(); got = hashlib.sha256(b).hexdigest()
    if got != want:
        sys.exit(f'STOP FAILED_SOURCE_IDENTITY {key}: expected {want}, measured {got}')
    return b.decode('utf-8')


def once(text, old, new):
    n = text.count(old)
    if n != 1:
        sys.exit(f'STOP: anchor matched {n} times: {old[:80]!r}')
    return text.replace(old, new)


def mmss(t):
    """seconds -> registry MM:SS[.mmm]; millisecond representation, half-up on the exact value."""
    ms = int((Fraction(t) * 1000 + Fraction(1, 2)) // 1)
    m, rem = divmod(ms, 60000); s, f = divmod(rem, 1000)
    return f'{m:02d}:{s:02d}' + (f'.{f:03d}' if f else '')


def main():
    epr, tl, red, sheet = read('epr'), read('timeline'), json.loads(read('v2')), read('sheet')
    if sheet.count('CHAIRMAN DECISION: ____') != 0:
        sys.exit('STOP: disposition sheet still has open cells')
    for must in ('CHAIRMAN DECISION: MOOT', 'CHAIRMAN RE-RULING (corrected evidence basis): REVISE-BOUNDARY',
                 '38971/12 s'):
        if must not in sheet:
            sys.exit(f'STOP: expected ruling text not found in sheet: {must}')
    tier1 = subprocess.run(['git', 'show', f'{TIER1_PROPOSAL_COMMIT}:./intelligence/p2/registries/'
                            'TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml'], cwd=ROOT, capture_output=True,
                           check=True).stdout.decode()
    seg = {r['segment']: r for r in red['segments']}

    rows = {}
    for line in tl.splitlines(keepends=True):
        if line.startswith('  - {id: S'):
            rows[line[9:12]] = line
    t1rows = {l[9:12]: l for l in tier1.splitlines(keepends=True) if l.startswith('  - {id: S')}

    for s in TIER1:                                   # byte-identical to the c5a72dc rows
        r = seg[s]
        if mmss(Fraction(str(r['new_start']))) not in t1rows[s] or mmss(Fraction(str(r['new_end']))) not in t1rows[s]:
            sys.exit(f'STOP: Tier-1 {s} v2 value differs from the c5a72dc proposal')
        tl = once(tl, rows[s], t1rows[s])

    for s, (row, dec, commit) in RULING.items():
        r = seg[s]; old = rows[s].split('span: "', 1)[1].split('"', 1)[0]
        new = f'{mmss(Fraction(str(r["new_start"])))}-{mmss(Fraction(str(r["new_end"])))}'
        basis = (f'08-24 lock (v2 mapping {V2[:8]}, G8-ratified; {row} {dec} {commit}{EXTRA.get(s, "")}; '
                 f'was {old} in 08-22)')
        tl = once(tl, rows[s], rows[s].replace(f'span: "{old}"', f'span: "{new}", span_basis: "{basis}"'))

    # Chairman S16 interview-count ruling (2026-10-01): 8 -> 7, conforming to the finalized R8
    # measured evidence (one closing interview removed). ONLY this field; participants unchanged.
    s16 = [l for l in tl.splitlines(keepends=True) if l.startswith('  - {id: S16,')][0]
    # Chairman S16 participants ruling (2026-10-01): [R68-R75] -> [R68-R74]; R75 is the removed
    # interviewee (RIDER_REGISTRY anchor #2192 lies in the removed interval). ONLY this field.
    tl = once(tl, s16, once(once(s16, 'interview_count: 8,', 'interview_count: 7,'),
                            'participants: [R68-R75]', 'participants: [R68-R74]'))

    old = rows['S14'].split('span: "', 1)[1].split('"', 1)[0]
    new = f'{mmss(S14_START_EXACT)}-{mmss(S14_END_EXACT)}'
    basis = (f'08-24 lock (R6 REVISE-BOUNDARY 2f814a1; start v2-mapped {V2[:8]} = 3205.701625s exact; '
             f'end = Chairman-confirmed picture end 38971/12s = 3247.583333s = frame 77942 '
             f'(last included 77941) = 00:54:07:14; R9 MOOT ee515d1, no residual A2; was {old} in 08-22)')
    tl = once(tl, rows['S14'], rows['S14'].replace(f'span: "{old}"', f'span: "{new}", span_basis: "{basis}"'))

    tl = once(tl, 'registry_version: 1.0.0\n', 'registry_version: 1.1.0-PROPOSED\n')
    tl = ('# ============================================================================\n'
          '# STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION\n'
          '# TIMELINE_REGISTRY v1.1.0-PROPOSED - complete 08-24 rebase from the Chairman\'s final\n'
          '# B-5 dispositions (R1-R9) and the G8-ratified v2 mapping. NOT the governed segment\n'
          '# authority until ratified; v1.0.0 (TIMELINE_REGISTRY.yaml) is unchanged and in force.\n'
          '# S01-S18 are in 08-24 seconds (millisecond representation); S19 (EPR-07 RETIRED) is\n'
          '# untouched and remains in 08-22 seconds. sources / delta_note / etc_anchors below still\n'
          '# describe the 08-22 founding extraction.\n'
          '# ============================================================================\n' + tl)
    tl = tl.rstrip('\n') + '\n' + (
        'proposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n'
        'changelog:\n'
        '  - version: "1.0.0 -> 1.1.0-PROPOSED"\n'
        '    date: "2026-10-01"\n'
        '    authority: "EO-2026-09-29 Addendum A (Tiers 1-3) and Addendum B G8; Chairman dispositions R1-R9"\n'
        f'    mapping: {{artifact: "intelligence/p2/ess/decision_packet_b5_b14/v2/rederivation_v2.json",\n'
        f'              sha256: "{V2}", g8: "ratified 1f806de",\n'
        '              historical_v1: "5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117",\n'
        '              lock_0824_sha256: "d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80",\n'
        '              lock_0822_sha256: "2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7"}\n'
        '    rulings: {R1: "S03 PRESERVE 2b3416f", R2: "S11 PRESERVE e563b17", R3: "S12 PRESERVE 2b45e11",\n'
        '              R4: "EPR-05->06 edge 3193.167 PRESERVE a857377", R5: "S13 PRESERVE 36623ee",\n'
        '              R6: "S14 REVISE-BOUNDARY 2f814a1 (original PRESERVE cb548f4 retained as history)",\n'
        '              R7: "S15 PRESERVE 3176446", R8: "S16 PRESERVE 1a80d2a", R9: "A2 MOOT ee515d1",\n'
        '              B-14: "CLOSED-MOOT (Addendum A)"}\n'
        '    tier1_unchanged: [S01, S02, S04, S05, S06, S07, S08, S09, S10, S17, S18]\n'
        '    rebased_on_ruling: [S03, S11, S12, S13, S14, S15, S16]\n'
        '    untouched: [S19]\n'
        '    s14_end_exact: {seconds: "38971/12", decimal: "3247.583333...", frame: 77942,\n'
        '                    last_included_frame: 77941, timecode_24ndf: "00:54:07:14"}\n'
        '    s14_start_exact: {seconds: "25645613/8000", decimal: "3205.701625", frame_aligned: false}\n'
        '    representation: "millisecond spans (half-up on exact values); representation only - no snapping"\n'
        '    r9: "MOOT - no segment created, no beat membership assigned"\n'
        '    s16_interview_count: {from: 8, to: 7, authority: "Chairman S16 interview-count ruling 2026-10-01",\n'
        '                          basis: "finalized R8 measured evidence - closing interview removed (1a80d2a)",\n'
        '                          scope: "interview_count only"}\n'
        '    s16_participants: {from: "[R68-R75]", to: "[R68-R74]", authority: "Chairman S16 participants ruling 2026-10-01",\n'
        '                       basis: "R75 = removed interviewee: RIDER_REGISTRY v1.0.0 (c389a5af) anchor GT-2 #2192 lies in removed interval 3947.208-3984.792 (v2); R68-R74 anchors corroborated in lock native captions at -119.5s",\n'
        '                       scope: "participants only"}\n')

    tl_sha = hashlib.sha256(tl.encode()).hexdigest()
    epr = once(epr, 'registry_version: "1.13.0"\n',
               'registry_version: "1.14.0-PROPOSED"\n'
               'proposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n')
    epr = once(epr, 'registry_version_note_1_13_0: >-\n',
               'registry_version_note_1_14_0_PROPOSED: >-\n'
               '  1.13.0 -> 1.14.0-PROPOSED, 2026-10-01. Completed B-5 rebase under EO-2026-09-29 ADDENDUM A\n'
               '  (Tiers 1-3) and ADDENDUM B G8. NO BEAT, MEANING, governing_theme, dramatic_intensity,\n'
               '  audience_state OR segment_refs VALUE CHANGED; EPR-07 untouched. Chairman dispositions:\n'
               '  R1 S03 PRESERVE (2b3416f); R2 S11 PRESERVE (e563b17); R3 S12 PRESERVE (2b45e11); R4 EPR-05->06\n'
               '  transition at 3193.167s PRESERVE (a857377); R5 S13 PRESERVE (36623ee); R6 S14 REVISE-BOUNDARY\n'
               '  (2f814a1; end 38971/12s - frame and timecode provenance in the TIMELINE proposal changelog;\n'
               '  original PRESERVE cb548f4 retained as history); R7 S15 PRESERVE (3176446); R8 S16 PRESERVE\n'
               '  (1a80d2a); R9 A2 MOOT (ee515d1); B-14\n'
               '  CLOSED-MOOT (Addendum A). This registry carries no temporal values, so the rebase is carried\n'
               '  by the segment authority proposal TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml (sha256\n'
               f'  {tl_sha}). Mapping: G8-ratified v2\n'
               f'  rederivation_v2.json {V2}\n'
               '  (historical v1 5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117). 08-24 lock\n'
               '  d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80. segment_authority,\n'
               '  segment_authority_status and path_b_consequences (PBC-2 included) are UNCHANGED; under the\n'
               '  rebase S18 lies at 4007.875-4622.875s, inside the 4689.5s lock - recorded, NOT applied.\n'
               'registry_version_note_1_13_0: >-\n')
    epr = ('# ============================================================================\n'
           '# STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION\n'
           '# EPR-001 v1.14.0-PROPOSED. v1.13.0 (EMOTIONAL_PROGRESSION_REGISTRY.yaml) is\n'
           '# unchanged and remains the RATIFIED registry until the Chairman rules.\n'
           '# ============================================================================\n' + epr)
    open(OUT_TL, 'w', encoding='utf-8').write(tl); open(OUT_EPR, 'w', encoding='utf-8').write(epr)
    for p in (OUT_TL, OUT_EPR):
        print(hashlib.sha256(open(p, 'rb').read()).hexdigest(), os.path.basename(p))


if __name__ == '__main__':
    main()
