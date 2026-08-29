#!/usr/bin/env python3
"""build_context.py — ECR-GEN-002 · B-4 / B-9

Turns a declared context stub into a MEASURED context.

Before this script, `AR2-<lineage>.context.json` was hand-written: its hashes,
byte counts, cue totals and ETC censuses were typed in, and nothing checked
them.  A typed number is indistinguishable from a measured one once it is in
the file, which is how the generator came to assert figures no computation had
ever produced.

This script computes every one of those values from the named source files and
from the resolver's own output, and REFUSES to emit a context whose declared
values disagree with the measured ones.  A disagreement is a STOP: the script
does not correct the declaration, because a declaration and a measurement
disagreeing is a governance condition, not a formatting error.

Everything it writes lands under two new blocks, so nothing existing changes
shape:

  source_manifest : per source - display_name, path, bytes, sha256
  measured        : ETC spine/connected/tag census, resolver census and
                    validation verdict, SRT cue count, expected out-of-range
                    count, derived lock timecodes

USAGE
  build_context.py --in <context.json> --out <enriched.json>
                   --sources <root> --timeline <timeline_resolved.json>
                   [--mp4 <path to designated proxy>]
                   [--etc <path to ETC>]   (default: sources/<source_files.etc>)

Exit codes
  0  enriched context written; every declared value agreed with measurement
  2  STOP - a declared value disagreed with measurement, or a source is missing
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter

SRT_TIME = re.compile(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->')


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def count_srt_cues(path):
    with open(path, 'rb') as fh:
        text = fh.read().decode('utf-8', 'replace')
    return len(SRT_TIME.findall(text))


def stop(msg):
    print('STOP: %s' % msg, file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--sources', required=True)
    ap.add_argument('--timeline', required=True)
    ap.add_argument('--mp4', default=None)
    ap.add_argument('--etc', default=None)
    a = ap.parse_args()

    ctx = json.load(open(a.inp))
    root = a.sources.rstrip('/') + '/'
    sf = ctx.get('source_files', {})
    declared_sha = ctx.get('sha', {})

    # ---- resolve each source to a real path -------------------------------
    paths = {}
    for key in ('fcpxml', 'srt', 'etc'):
        rel = sf.get(key)
        if key == 'etc' and a.etc:
            paths[key] = a.etc
        elif rel in (None, 'NOT_PRODUCED', 'NOT_DESIGNATED'):
            paths[key] = None
        else:
            paths[key] = root + rel
    paths['mp4'] = a.mp4 or (root + sf['mp4'] if sf.get('mp4') else None)

    display = {
        'fcpxml': os.path.basename(paths['fcpxml']) if paths['fcpxml'] else 'NOT_DESIGNATED',
        'srt': ctx.get('srt_display_name') or (os.path.basename(paths['srt'])
                                               if paths['srt'] else 'NOT_DESIGNATED'),
        'etc': os.path.basename(paths['etc']) if paths['etc'] else 'NOT_PRODUCED',
        'mp4': (ctx.get('proxy') or {}).get('name') or 'NOT_DESIGNATED',
    }

    manifest = {}
    for key in ('mp4', 'fcpxml', 'srt', 'etc'):
        p = paths[key]
        if not p:
            manifest[key] = dict(display_name=display[key], path=None,
                                 bytes=None, sha256=None, status='NOT_AVAILABLE')
            continue
        if not os.path.exists(p):
            stop('source %s declared at %s does not exist' % (key, p))
        measured = sha256_of(p)
        dec = declared_sha.get(key)
        if dec not in (None, 'NOT_DESIGNATED', 'NOT_PRODUCED') and dec != measured:
            stop('declared sha256 for %s (%s) does not equal the measured sha256 (%s) of %s'
                 % (key, dec, measured, p))
        manifest[key] = dict(display_name=display[key], path=p,
                             bytes=os.path.getsize(p), sha256=measured,
                             status='MEASURED')

    # ---- SRT cue census ----------------------------------------------------
    measured = {}
    if paths['srt']:
        cues = count_srt_cues(paths['srt'])
        dec = (ctx.get('srt') or {}).get('cues')
        if dec is not None and dec != cues:
            stop('declared srt.cues (%s) does not equal the measured cue count (%d)' % (dec, cues))
        measured['srt_cues'] = cues

    # ---- ETC census --------------------------------------------------------
    if paths['etc']:
        etc = json.load(open(paths['etc']))
        spine, conn = etc['spine'], etc.get('connected_elements', [])
        for name, got, dec in (('etc.spine', len(spine), (ctx.get('etc') or {}).get('spine')),
                               ('etc.connected', len(conn), (ctx.get('etc') or {}).get('connected'))):
            if dec is not None and dec != got:
                stop('declared %s (%s) does not equal the measured count (%d)' % (name, dec, got))
        measured['etc_spine_n'] = len(spine)
        measured['etc_connected_n'] = len(conn)
        measured['etc_connected_by_tag'] = dict(sorted(Counter(x['tag'] for x in conn).items()))
        measured['etc_spine_by_tag'] = dict(sorted(Counter(x['tag'] for x in spine).items()))
        measured['etc_connected_timeline_offset_all_null'] = all(
            x.get('timeline_offset_s') is None for x in conn)
        measured['etc_declared_source_sha256'] = etc.get('source_sha256')
        measured['etc_declared_sequence_duration_s'] = (etc.get('sequence') or {}).get('duration_s')
        measured['etc_declared_lock_tc'] = (etc.get('sequence') or {}).get('declared_lock')

    # ---- resolver census and verdict --------------------------------------
    tl = json.load(open(a.timeline))
    cen = tl.get('census')
    val = tl.get('validation', {})
    if cen is None:
        stop('%s carries no census block; it was produced by a pre-B-1 resolver. '
             'Re-run fcpx_resolve.py before building the context.' % a.timeline)
    measured['resolver'] = dict(
        total_elements=cen['total_resolved_elements'],
        depth0_all=cen['depth0_all'],
        depth0_transitions=cen['depth0_transitions'],
        spine_excl_transitions=cen['resolved_spine_n'],
        connected_lane_n=cen['connected_lane_n'],
        out_of_range_n=cen['out_of_range_n'],
        by_tag=cen['by_tag'],
        etc_validation=val.get('etc_validation'),
        spine_comparison=val.get('spine_comparison'),
        spine_offset_matches=val.get('spine_offset_matches'),
        tolerance_s=val.get('tolerance_s'),
        source_sha256_match=val.get('source_sha256_match'),
        sequence_duration_match=val.get('sequence_duration_match'),
        spine_end_s=val.get('spine_end_s'),
        spine_end_equals_lock=val.get('spine_end_equals_lock'))
    measured['expected_out_of_range_n'] = cen['out_of_range_n']

    # runtime agreement between the declared lock and the resolved spine end
    lock = ctx.get('runtime_s')
    end = val.get('spine_end_s')
    if lock is not None and end is not None and abs(float(lock) - float(end)) > 0.0005:
        stop('declared runtime_s (%s) does not equal the resolved spine end (%s)' % (lock, end))

    # ---- derived timecodes, computed once, never typed ---------------------
    fps = int(round(eval(str(ctx['frame_rate']))))          # e.g. "24/1" -> 24
    if lock is not None:
        h = int(lock // 3600); m = int((lock % 3600) // 60); s = int(lock % 60)
        frames = int(round((lock - int(lock)) * fps)) - 1
        measured['lock_tc_frames'] = '%02d:%02d:%02d:%02d' % (h, m, s, frames)
        measured['lock_tc_seconds'] = '%02d:%02d:%06.3f' % (h, m, lock % 60)
        measured['fps_int'] = fps

    ctx['source_manifest'] = manifest
    ctx['measured'] = measured
    ctx['context_provenance'] = dict(
        built_by='build_context.py',
        from_context=a.inp, sources_root=a.sources, timeline=a.timeline,
        note=('Every value under source_manifest and measured was computed from the named '
              'files by this run. Declared values that disagreed with measurement would have '
              'stopped this script rather than being overwritten.'))

    json.dump(ctx, open(a.out, 'w'), indent=1)
    print('wrote %s' % a.out)
    print('  sources measured : %s' % ', '.join(
        '%s=%s' % (k, v['status']) for k, v in manifest.items()))
    print('  etc              : spine=%s connected=%s titles=%s'
          % (measured.get('etc_spine_n'), measured.get('etc_connected_n'),
             (measured.get('etc_connected_by_tag') or {}).get('title')))
    print('  resolver         : total=%s depth0=%s spine=%s oor=%s verdict=%s %s'
          % (measured['resolver']['total_elements'], measured['resolver']['depth0_all'],
             measured['resolver']['spine_excl_transitions'],
             measured['resolver']['out_of_range_n'],
             measured['resolver']['etc_validation'],
             measured['resolver']['spine_comparison']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
