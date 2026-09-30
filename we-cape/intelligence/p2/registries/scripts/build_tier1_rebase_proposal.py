#!/usr/bin/env python3
"""
Tier-1 mechanical rebase proposal, EO-2026-09-29 Addendum A (Tier 1) / Addendum B (G8).

EPR-001 v1.13.0 carries NO temporal values: beats bind to segment IDs only, and its
segment_authority_note forbids resolving a segment_ref to a timecode. Segment spans live
in TIMELINE_REGISTRY v1.0.0. Per the Chairman's answer on 2026-09-30 (the target question),
the rebase therefore lands in TWO proposed files:

  TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml
      Tier-1 spans (S01 S02 S04-S10 S17 S18) rebased to 08-24 seconds via the accepted
      mapping; Tier-2/3 spans (S03 S11 S12-S16) left in 08-22 seconds and annotated
      "pending row-level decisions"; S19 untouched.
  EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0-PROPOSED.yaml
      v1.13.0 plus a PROPOSED status header, a version string, and a changelog entry
      citing Addendum A Tier 1, the mapping hashes and the TIMELINE proposal.

TEXT-LEVEL edits only, each asserted to match exactly once, so every byte outside the
enumerated changes is carried over. Every input is hash-asserted before it is read.
Inputs are opened read-only; nothing is written next to them except the two proposals.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.dirname(HERE)
ESS = os.path.join(REG, '..', 'ess')

INPUTS = {
    'epr': (os.path.join(REG, 'EMOTIONAL_PROGRESSION_REGISTRY.yaml'),
            '1d54e674190eef8122f7ddd22af66ae07abcb13dead7f5077ed868c37dbe21a4'),
    'timeline': (os.path.join(REG, 'TIMELINE_REGISTRY.yaml'),
                 '34bd0f9ef7f1507cd8fa0f0745abadd675060b313d98d06ea2dd35c98bc8de76'),
    'rederivation': (os.path.join(ESS, 'decision_packet_b5_b14', 'rederivation.json'),
                     '5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117'),
    'disposition': (os.path.join(REG, '..', '..', '..', 'docs', 'rulings', 'AFFECTED_BEAT_DISPOSITION_SHEET.md'),
                    '5a1c7e767c1a39146b09b56953f30d36b48284f06f47bbd48d07e791ed8bd430'),
}
TIER1 = ['S01', 'S02', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S17', 'S18']
PENDING = ['S03', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16']
OUT_TL = os.path.join(REG, 'TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml')
OUT_EPR = os.path.join(REG, 'EMOTIONAL_PROGRESSION_REGISTRY_v1.14.0-PROPOSED.yaml')


def read_asserted(key):
    path, want = INPUTS[key]
    b = open(path, 'rb').read()
    got = hashlib.sha256(b).hexdigest()
    if got != want:
        sys.exit(f'STOP FAILED_SOURCE_IDENTITY {key}: expected {want}, measured {got}')
    return b.decode('utf-8')


def once(text, old, new):
    n = text.count(old)
    if n != 1:
        sys.exit(f'STOP: anchor matched {n} times, expected 1: {old[:80]!r}')
    return text.replace(old, new)


def mmss(t):
    """08-24 seconds -> the registry's MM:SS span form, milliseconds kept (never rounded
    to whole seconds, which would move a boundary)."""
    m, s = divmod(round(t * 1000), 60000)
    whole, ms = divmod(s, 1000)
    return f'{m:02d}:{whole:02d}' + (f'.{ms:03d}' if ms else '')


def main():
    epr = read_asserted('epr')
    tl = read_asserted('timeline')
    red = json.loads(read_asserted('rederivation'))
    read_asserted('disposition')      # scope source; asserted, not parsed

    seg = {r['segment']: r for r in red['segments']}
    for s in TIER1:
        r = seg[s]
        if r['start']['status'] != 'MAPPED' or r['end']['status'] != 'MAPPED':
            sys.exit(f'STOP: Tier-1 {s} boundary is not MAPPED - not a mechanical rebase')

    # ---------------- TIMELINE_REGISTRY v1.1.0-PROPOSED ----------------
    rows = {}
    for line in tl.splitlines(keepends=True):
        for s in TIER1 + PENDING:
            if line.startswith(f'  - {{id: {s}, span: '):
                rows[s] = line
    missing = [s for s in TIER1 + PENDING if s not in rows]
    if missing:
        sys.exit(f'STOP: segment rows not found {missing}')

    for s in TIER1:
        r = seg[s]
        old_span = rows[s].split('span: "', 1)[1].split('"', 1)[0]
        a, b = old_span.split('-')
        to_s = lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])
        if (to_s(a), to_s(b)) != (round(r['old_start']), round(r['old_end'])):
            sys.exit(f'STOP: {s} registry span {old_span} != packet 08-22 span '
                     f'{r["old_start"]}-{r["old_end"]}')
        new_span = f'{mmss(r["new_start"])}-{mmss(r["new_end"])}'
        new_row = rows[s].replace(f'span: "{old_span}"',
                                  f'span: "{new_span}", span_basis: "08-24 lock (rebased; was {old_span} in 08-22)"')
        tl = once(tl, rows[s], new_row)
    for s in PENDING:
        old_span = rows[s].split('span: "', 1)[1].split('"', 1)[0]
        tl = once(tl, rows[s], rows[s].replace(
            f'span: "{old_span}"',
            f'span: "{old_span}", span_basis: "08-22 assembly - pending row-level decisions"'))

    tl = once(tl, 'registry_version: 1.0.0\n', 'registry_version: 1.1.0-PROPOSED\n')
    tl = ('# ============================================================================\n'
          '# STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION\n'
          '# TIMELINE_REGISTRY v1.1.0-PROPOSED - Tier-1 mechanical rebase (EO-2026-09-29\n'
          '# Addendum A Tier 1). NOT the governed segment authority until ratified;\n'
          '# v1.0.0 (TIMELINE_REGISTRY.yaml) is unchanged and remains in force.\n'
          '# MIXED BASIS BY DESIGN: rows marked span_basis "08-24 lock" are rebased;\n'
          '# rows marked "08-22 assembly - pending row-level decisions" are NOT, and must\n'
          '# not be read against the 08-24 lock. S19 is untouched. sources / delta_note /\n'
          '# etc_anchors below still describe the 08-22 founding extraction.\n'
          '# ============================================================================\n'
          + tl)
    tl = tl.rstrip('\n') + '\n' + (
        'proposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n'
        'changelog:\n'
        '  - version: "1.0.0 -> 1.1.0-PROPOSED"\n'
        '    date: "2026-09-30"\n'
        '    authority: "EO-2026-09-29 Addendum A, TIER 1 - PRESERVE + REBASE; Addendum B G8 (structural)"\n'
        '    mapping: {artifact: "intelligence/p2/ess/decision_packet_b5_b14/rederivation.json",\n'
        '              sha256: "5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117",\n'
        '              lock_0824_sha256: "d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80",\n'
        '              lock_0822_sha256: "2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7"}\n'
        '    rebased: [S01, S02, S04, S05, S06, S07, S08, S09, S10, S17, S18]\n'
        '    pending_row_level_decisions: [S03, S11, S12, S13, S14, S15, S16]\n'
        '    untouched: [S19]\n'
        '    rule: "span = accepted mapping new_start-new_end, both boundaries MAPPED; ms precision kept"\n')

    # ---------------- EPR-001 v1.14.0-PROPOSED ----------------
    tl_sha = hashlib.sha256(tl.encode('utf-8')).hexdigest()
    epr = once(epr, 'registry_version: "1.13.0"\n',
               'registry_version: "1.14.0-PROPOSED"\n'
               'proposal_status: "PROPOSED — AWAITING CHAIRMAN RATIFICATION"\n')
    epr = once(epr, 'registry_version_note_1_13_0: >-\n',
               'registry_version_note_1_14_0_PROPOSED: >-\n'
               '  1.13.0 -> 1.14.0-PROPOSED, 2026-09-30. EO-2026-09-29 ADDENDUM A, TIER 1 - PRESERVE +\n'
               '  REBASE (S01, S02, S04-S10, S17, S18), under Addendum B G8 (structural ratification only).\n'
               '  NO BEAT, MEANING, governing_theme, dramatic_intensity, audience_state OR segment_refs\n'
               '  VALUE CHANGED. EPR-07 untouched. This registry carries no temporal values - beats bind to\n'
               '  segment IDs and segment_authority_note bars resolving a segment_ref to a timecode - so the\n'
               '  Tier-1 temporal rebase is carried by the segment authority proposal\n'
               '  TIMELINE_REGISTRY_v1.1.0-PROPOSED.yaml (sha256 ' + tl_sha + '),\n'
               '  per the Chairman answer of 2026-09-30. Mapping: decision_packet_b5_b14/rederivation.json\n'
               '  sha256 5d6994b3f36de5bc07d3987cdb3bd611f70493390a8f6a8ed50828a79d666117; 08-24 lock\n'
               '  d82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80. Tier-2 (S03, S11) and\n'
               '  Tier-3 (S12-S16) remain in 08-22 seconds, pending row-level decisions. segment_authority,\n'
               '  segment_authority_status and path_b_consequences are UNCHANGED: under the rebase S18\n'
               '  maps to 4007.875-4622.875 s, inside the 4689.5 s lock, which bears on PBC-2 - recorded\n'
               '  here, NOT applied; PBC-2 disposition stays the Chairman\'s.\n'
               'registry_version_note_1_13_0: >-\n')
    epr = ('# ============================================================================\n'
           '# STATUS: PROPOSED — AWAITING CHAIRMAN RATIFICATION\n'
           '# EPR-001 v1.14.0-PROPOSED. v1.13.0 (EMOTIONAL_PROGRESSION_REGISTRY.yaml) is\n'
           '# unchanged and remains the RATIFIED registry until the Chairman rules.\n'
           '# ============================================================================\n'
           + epr)

    open(OUT_TL, 'w', encoding='utf-8').write(tl)
    open(OUT_EPR, 'w', encoding='utf-8').write(epr)
    for p in (OUT_TL, OUT_EPR):
        print(hashlib.sha256(open(p, 'rb').read()).hexdigest(), os.path.basename(p))


if __name__ == '__main__':
    main()
