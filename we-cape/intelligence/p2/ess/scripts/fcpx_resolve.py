#!/usr/bin/env python3
"""FCPXML absolute-timeline resolver for WECAPE-AR2-SPRINT3A.
Resolves every story element to an absolute sequence-time in/out.
Validates against an Editorial Timing Contract when one is supplied:
source identity, sequence duration, strict spine cardinality, then
element-wise offset and duration agreement at TOL seconds.
Any failed gate is a STOP with a recorded stop_reason and exit 2."""
import xml.etree.ElementTree as ET
import collections
from fractions import Fraction
import json, sys, hashlib

STORY = {'asset-clip','clip','title','video','audio','gap','spine','ref-clip',
         'mc-clip','sync-clip','audition','transition','caption'}
CONTAINER = STORY  # any story element may contain anchored children

def rt(s):
    if s is None: return None
    s = s.strip()
    if s.endswith('s'): s = s[:-1]
    if s == '': return Fraction(0)
    if '/' in s:
        n,d = s.split('/'); return Fraction(int(n), int(d))
    return Fraction(s) if '.' not in s else Fraction(s)

def f2(x):
    return None if x is None else round(float(x), 6)

# ECR-GEN-002 / B-1: the single comparison tolerance for ETC binding, in seconds.
# Stated once so no caller and no report can assert a different one.
TOL = 0.0005

def _emit(out, outjson, census):
    """Write the resolve output and print the validation block and census.
    Called on every exit path so a STOP is as fully recorded as a pass."""
    json.dump(out, open(outjson, "w"), indent=1)
    print(json.dumps(out["validation"], indent=1))
    print("census:", json.dumps(census))

class Resolver:
    def __init__(self):
        self.rows = []

    def walk(self, node, node_abs, node_local, depth, parent_desc, path):
        """node_abs: absolute seq time where node's local time == node_local."""
        for ch in node:
            if ch.tag not in STORY:
                continue
            off = rt(ch.get('offset')) if ch.get('offset') is not None else None
            if off is None:
                # pass-through container (e.g. top-level <spine> with no offset)
                if ch.tag == 'spine':
                    self.walk(ch, node_abs, node_local, depth, parent_desc, path)
                continue
            ch_abs = node_abs + (off - node_local)
            dur = rt(ch.get('duration')) if ch.get('duration') is not None else Fraction(0)
            start = rt(ch.get('start')) if ch.get('start') is not None else Fraction(0)
            lane = ch.get('lane')
            name = ch.get('name') or ''
            if ch.tag == 'title':
                # Each <text> element is one on-screen text block; its
                # <text-style> children are styling runs of the SAME string
                # and must be concatenated, not separated.
                blocks = []
                for t in ch.findall('text'):
                    s = ''.join(t.itertext())
                    if s.strip():
                        blocks.append(' '.join(s.split()))
                text = ' / '.join(blocks)
            else:
                text = ''
            self.rows.append(dict(
                tag=ch.tag, name=name, text=text, lane=lane, depth=depth,
                parent=parent_desc, path=path + '/' + ch.tag + f'[{len(self.rows)}]',
                abs_in_s=f2(ch_abs), abs_out_s=f2(ch_abs + dur),
                duration_s=f2(dur), offset_raw=ch.get('offset'),
                start_raw=ch.get('start'), source_start_s=f2(start),
                ref=ch.get('ref')))
            # children of ch are expressed in ch's local timebase, which begins at ch.start
            # For a secondary-storyline <spine>, children offsets are in the PARENT timebase
            if ch.tag == 'spine':
                # Anchored (secondary-storyline) spine: children offsets are
                # expressed in the storyline's own timebase, which begins at 0.
                self.walk(ch, ch_abs, Fraction(0), depth+1, name or 'SPINE-2',
                          path + '/spine')
            else:
                self.walk(ch, ch_abs, start, depth+1, name or ch.tag, path + '/' + ch.tag)

def main(fcpxml, etc_json, outjson):
    # etc_json may be the literal string NONE: the resolver then runs without
    # ETC validation and reports etc_validation: NOT_VALIDATED (DOC-001).
    tree = ET.parse(fcpxml); root = tree.getroot()
    seq = root.find('.//sequence')
    seq_dur = rt(seq.get('duration')); tc0 = rt(seq.get('tcStart') or '0s')
    fmt = root.find(".//format[@id='%s']" % seq.get('format'))
    fd = rt(fmt.get('frameDuration')); fps = 1/fd
    r = Resolver()
    top = seq.find('spine')
    r.walk(top, Fraction(0), tc0, 0, 'SPINE', '/sequence/spine')
    rows = r.rows
    out = dict(sequence=dict(duration_s=f2(seq_dur), fps=float(fps),
                             frame_duration_s=f2(fd), tcStart=str(tc0),
                             format=fmt.get('name'), width=fmt.get('width'),
                             height=fmt.get('height')),
               elements=rows)
    # ---- validation vs ETC  (B-1 remediation, ECR-GEN-002) ----
    # The Editorial Timing Contract's spine census EXCLUDES transitions; the
    # resolver's depth-0 set includes them.  Pairing the two positionally is a
    # category error and was the defect reported as B-1.  The comparison set is
    # therefore the non-transition depth-0 elements, and cardinality is asserted
    # BEFORE any pairing is attempted: an unequal census is a STOP, never a
    # silently truncated comparison.
    d0 = [x for x in rows if x['depth'] == 0]
    mine_spine = [x for x in d0 if x['tag'] != 'transition']
    census = dict(total_resolved_elements=len(rows),
                  depth0_all=len(d0),
                  depth0_transitions=len(d0) - len(mine_spine),
                  resolved_spine_n=len(mine_spine),
                  connected_lane_n=len([x for x in rows
                                        if x.get('lane') not in (None, '')]),
                  by_tag=dict(sorted(collections.Counter(
                      x['tag'] for x in rows).items())),
                  by_depth=dict(sorted(collections.Counter(
                      x['depth'] for x in rows).items())),
                  out_of_range_n=len([x for x in rows
                                      if x['abs_in_s'] < -0.001
                                      or x['abs_out_s'] > float(seq_dur) + 0.001]))
    out['census'] = census
    last = mine_spine[-1]
    oor = [x['path'] for x in rows
           if x['abs_in_s'] < -0.001 or x['abs_out_s'] > float(seq_dur) + 0.001]

    if etc_json in ('NONE', 'none', None):
        out['validation'] = dict(
            etc_validation='NOT_VALIDATED',
            reason='no Editorial Timing Contract supplied for this lineage',
            tolerance_s=TOL,
            resolved_spine_n=len(mine_spine),
            sequence_duration_s=f2(seq_dur),
            spine_end_s=last['abs_out_s'],
            spine_end_equals_lock=abs(last['abs_out_s'] - float(seq_dur)) < TOL,
            n_out_of_range=len(oor),
            out_of_range_status=('NONE' if not oor
                                 else 'PRESENT_REQUIRES_DECLARED_DISPOSITION'),
            out_of_range=oor[:20])
        _emit(out, outjson, census)
        return out

    etc = json.load(open(etc_json))
    v = dict(etc_validation='PENDING',
             etc_file=etc_json,
             tolerance_s=TOL,
             etc_spine_n=len(etc['spine']),
             etc_connected_n=len(etc.get('connected_elements', [])),
             resolved_spine_n=len(mine_spine),
             depth0_including_transitions=len(d0))

    # gate 1 - the contract must name the FCPXML this run actually parsed.
    computed = hashlib.sha256(open(fcpxml, 'rb').read()).hexdigest()
    v['fcpxml_sha256_computed'] = computed
    v['fcpxml_sha256_declared_by_etc'] = etc.get('source_sha256')
    v['source_sha256_match'] = (computed == etc.get('source_sha256'))
    if not v['source_sha256_match']:
        v['etc_validation'] = 'FAILED_SOURCE_IDENTITY'
        v['stop_reason'] = ('ETC source_sha256 does not equal the SHA-256 of the '
                            'FCPXML parsed by this run; the contract describes a '
                            'different export.')
        out['validation'] = v; _emit(out, outjson, census); sys.exit(2)

    # gate 2 - the contract's declared sequence duration must agree.
    etc_dur = (etc.get('sequence') or {}).get('duration_s')
    v['etc_sequence_duration_s'] = etc_dur
    v['sequence_duration_s'] = f2(seq_dur)
    v['sequence_duration_match'] = (etc_dur is not None and
                                    abs(float(etc_dur) - float(seq_dur)) < TOL)
    if not v['sequence_duration_match']:
        v['etc_validation'] = 'FAILED_SEQUENCE_DURATION'
        v['stop_reason'] = ('ETC sequence.duration_s does not equal the resolved '
                            'sequence duration.')
        out['validation'] = v; _emit(out, outjson, census); sys.exit(2)

    # gate 3 - STRICT CARDINALITY.  No pairing unless the censuses are equal,
    # which makes zip()-style truncation structurally impossible.
    if len(etc['spine']) != len(mine_spine):
        v['etc_validation'] = 'FAILED_CARDINALITY'
        v['stop_reason'] = ('ETC spine census (%d) does not equal the resolved '
                            'non-transition depth-0 census (%d). No element-wise '
                            'comparison was attempted.'
                            % (len(etc['spine']), len(mine_spine)))
        out['validation'] = v; _emit(out, outjson, census); sys.exit(2)

    # gate 4 - element-wise comparison across the whole census.
    n = len(mine_spine); matches = 0; mism = []
    for i in range(n):
        a = etc['spine'][i]; b = mine_spine[i]
        if a.get('timeline_offset_s') is None or a.get('duration_s') is None:
            mism.append(dict(index=i, name=str(a.get('name'))[:60],
                             condition='NULL_FIELD_IN_ETC'))
            continue
        do = abs(float(a['timeline_offset_s']) - float(b['abs_in_s']))
        dd = abs(float(a['duration_s']) - float(b['duration_s']))
        if do < TOL and dd < TOL:
            matches += 1
        else:
            mism.append(dict(index=i, name=str(a.get('name'))[:60],
                             etc_offset_s=a['timeline_offset_s'],
                             resolved_offset_s=b['abs_in_s'],
                             etc_duration_s=a['duration_s'],
                             resolved_duration_s=b['duration_s'],
                             d_offset_s=round(do, 6), d_duration_s=round(dd, 6)))
    v['spine_offset_matches'] = matches
    v['spine_comparison'] = '%d / %d' % (matches, n)
    v['spine_mismatches'] = mism[:10]
    v['spine_end_s'] = last['abs_out_s']
    v['spine_end_equals_lock'] = abs(last['abs_out_s'] - float(seq_dur)) < TOL
    # Out-of-range elements are anchored children whose resolved out-time
    # exceeds the sequence duration.  They are an FCPXML nesting observable,
    # NOT an ETC binding failure - the 08-22 fixture carries 18 of them and
    # binds 191/191.  They are reported here and escalated: the generator's
    # runtime guard asserts this count against a DECLARED expectation in the
    # context, so the condition is dispositioned rather than absorbed.
    v['out_of_range'] = oor[:20]
    v['n_out_of_range'] = len(oor)
    v['out_of_range_status'] = ('NONE' if not oor
                                else 'PRESENT_REQUIRES_DECLARED_DISPOSITION')

    if matches != n:
        v['etc_validation'] = 'FAILED_COMPARISON'
        v['stop_reason'] = ('%d of %d spine elements agree within %.4f s.'
                            % (matches, n, TOL))
        out['validation'] = v; _emit(out, outjson, census); sys.exit(2)

    if not v['spine_end_equals_lock']:
        v['etc_validation'] = 'FAILED_TIMELINE_CLOSURE'
        v['stop_reason'] = ('resolved spine end %s does not equal sequence '
                            'duration %s within %.4f s.'
                            % (v['spine_end_s'], v['sequence_duration_s'], TOL))
        out['validation'] = v; _emit(out, outjson, census); sys.exit(2)

    v['etc_validation'] = 'VALIDATED'
    out['validation'] = v
    _emit(out, outjson, census)
    return out

if __name__ == '__main__':
    main(*sys.argv[1:])
