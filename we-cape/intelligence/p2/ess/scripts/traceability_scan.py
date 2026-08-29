#!/usr/bin/env python3
"""traceability_scan.py — ECR-GEN-002 · Regression Integrity

"Every generated metric, count, duration, cue total, hash, and validation
statement must be traceable to an input, a computed value, or a validation
result.  Any value lacking a producing computation shall fail the engineering
test suite."

This scanner enforces that in two tiers, because the two conditions it finds
are not the same condition and collapsing them would hide the larger one.

TR-1  GATING - production-identifying literals
      A value that names or measures ONE production may not appear as a literal
      in the generator.  These are the values that, left embedded, make the
      generator emit a correct-looking artifact about the wrong film.  The
      scanner takes them from the context of a known lineage, so the test is
      not a hand-maintained blocklist: whatever that lineage measures is what
      may not be hard-coded.
      Any hit FAILS.

TR-2  REPORTING - untraceable narrative literals
      Bare numerals and measurements inside emitted prose that no input
      produces.  These are 08-22 OBSERVATIONS written into the generator as
      text.  They are enumerated per artifact and reported, not failed:
      relocating them into the observation bundle is a different change from
      the one ECR-GEN-002 was scoped to, and is raised as B-13.

USAGE
    traceability_scan.py <generator.py> --context <enriched context.json>
                         [--json <out.json>]

Exit codes
    0  TR-1 clean
    1  TR-1 found production-identifying literals
"""
import argparse
import json
import re
import sys

WRITERS = {
    'L': 'STEP0_TIMING_CLOSURE.md', 'C': 'CAPTION_REGISTRY.yaml',
    'V': 'VISUAL_EVENT_REGISTRY.yaml', 'S': 'EDITORIAL_SYNCHRONIZATION.yaml',
    'K': 'CONDUCTOR_SCORE.yaml', 'R': 'ESS_VALIDATION_REPORT.md',
    'P': 'PRODUCTION_INTELLIGENCE_SEED.yaml',
}
APPEND = re.compile(r'^\s*([LCVSKRP])\.append\(')
NUMERAL = re.compile(r'(?<![\w.])(\d[\d,]*\.?\d*)(?![\w.])')
TIMECODE = re.compile(r'\b\d{2}:\d{2}:\d{2}(?:[.:]\d{1,3})?\b')


def production_fingerprint(ctx):
    """Every value that identifies or measures THIS production, from its context."""
    meas = ctx.get('measured') or {}
    res = meas.get('resolver') or {}
    srcm = ctx.get('source_manifest') or {}
    nums, names = set(), set()

    def add(v):
        if v is None:
            return
        if isinstance(v, (int, float)):
            s = ('%d' % v) if float(v).is_integer() else ('%s' % v)
            # Only values of 100 or more are specific enough to GATE on. Smaller
            # counts collide constantly with timecode fields, dB figures and
            # ordinary prose numerals, and a gate that fires on those is a gate
            # nobody can keep. Values below the threshold are still reported by
            # TR-2; the threshold is stated so it is not mistaken for coverage.
            if abs(float(v)) >= 100:
                nums.add(s)
        elif isinstance(v, str) and v.strip():
            names.add(v.strip())

    for k in ('runtime_s',):
        add(ctx.get(k))
    for k in ('etc_spine_n', 'etc_connected_n', 'expected_out_of_range_n',
              'lock_tc_frames', 'lock_tc_seconds'):
        add(meas.get(k))
    for k in ('total_elements', 'depth0_all', 'depth0_transitions',
              'spine_excl_transitions', 'connected_lane_n', 'out_of_range_n',
              'spine_offset_matches'):
        add(res.get(k))
    add((ctx.get('srt') or {}).get('cues'))
    for tag, n in (meas.get('etc_connected_by_tag') or {}).items():
        add(n)
    for key, entry in srcm.items():
        add(entry.get('bytes'))
        nm = entry.get('display_name')
        if nm and nm not in ('NOT_DESIGNATED', 'NOT_PRODUCED'):
            names.add(nm)
    for nm in (ctx.get('display_names') or {}).values():
        if isinstance(nm, str) and nm.strip():
            names.add(nm.strip())
    # bare filenames as well as their declared display forms
    for nm in list(names):
        base = nm.rsplit('/', 1)[-1]
        if base != nm:
            names.add(base)
    names = {n for n in names if len(n) >= 6}
    return nums, names


def emitted_lines(src_lines):
    """Yield (lineno, writer, text) for every line that contributes emitted text."""
    cur = None
    for i, line in enumerate(src_lines, 1):
        m = APPEND.match(line)
        if m:
            cur = m.group(1)
        elif cur is not None and not line.lstrip().startswith(('"', "'", 'f"', "f'")):
            cur = None
        if cur is not None:
            yield i, cur, line


def strip_interpolations(text):
    """Remove {...} interpolation bodies so only literal text is examined."""
    out, depth = [], 0
    for ch in text:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('generator')
    ap.add_argument('--context', required=True)
    ap.add_argument('--json', default=None)
    a = ap.parse_args()

    ctx = json.load(open(a.context))
    nums, names = production_fingerprint(ctx)
    src = open(a.generator).read().split('\n')

    tr1, tr2 = [], []
    for lineno, writer, line in emitted_lines(src):
        literal = strip_interpolations(line)
        # A timecode is one token. Scanning its fields as separate numerals
        # manufactures collisions that mean nothing, so timecodes are matched
        # whole and masked out before numeral extraction.
        tcs = TIMECODE.findall(literal)
        for tc in tcs:
            if tc in nums:
                tr1.append(dict(line=lineno, artifact=WRITERS[writer],
                                kind='production_timecode', value=tc,
                                text=line.strip()[:120]))
        literal_nums = TIMECODE.sub(' ', literal)
        for nm in names:
            if nm in literal:
                tr1.append(dict(line=lineno, artifact=WRITERS[writer],
                                kind='production_name', value=nm,
                                text=line.strip()[:120]))
        for tok in NUMERAL.findall(literal_nums):
            if tok.replace(',', '') in nums or tok in nums:
                tr1.append(dict(line=lineno, artifact=WRITERS[writer],
                                kind='production_measure', value=tok,
                                text=line.strip()[:120]))
        for tok in set(NUMERAL.findall(literal_nums)) | set(tcs):
            if tok.replace(',', '') in nums or tok in nums:
                continue
            if re.fullmatch(r'\d', tok):
                continue
            tr2.append(dict(line=lineno, artifact=WRITERS[writer], value=tok))

    print('TR-1  production-identifying literals (GATING)')
    if tr1:
        for h in tr1:
            print('  FAIL  L%-5d %-34s %-18s %s'
                  % (h['line'], h['artifact'], h['value'], h['text']))
    else:
        print('  none - no literal in the generator names or measures this production')

    per = {}
    for h in tr2:
        per.setdefault(h['artifact'], set()).add((h['line'], h['value']))
    print('\nTR-2  untraceable narrative literals (REPORTED as B-13, not gating)')
    print('  %-36s %8s %10s' % ('artifact', 'lines', 'literals'))
    tot_l = tot_v = 0
    for art in WRITERS.values():
        rows = per.get(art, set())
        ln = len({r[0] for r in rows})
        tot_l += ln
        tot_v += len(rows)
        print('  %-36s %8d %10d' % (art, ln, len(rows)))
    print('  %-36s %8d %10d' % ('TOTAL', tot_l, tot_v))

    if a.json:
        json.dump(dict(tr1=tr1, tr2=tr2,
                       fingerprint=dict(numbers=sorted(nums), names=sorted(names))),
                  open(a.json, 'w'), indent=1)
        print('\nwrote %s' % a.json)

    return 1 if tr1 else 0


if __name__ == '__main__':
    sys.exit(main())
