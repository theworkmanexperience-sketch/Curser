#!/usr/bin/env python3
"""FCPXML absolute-timeline resolver for WECAPE-AR2-SPRINT3A.
Resolves every story element to an absolute sequence-time in/out.
Validated against P2_LOCK_timing.json spine offsets (191 elements)."""
import xml.etree.ElementTree as ET
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
    # ---- validation vs ETC ----
    if etc_json in ('NONE','none',None):
        out['validation'] = dict(etc_validation='NOT_VALIDATED',
            reason='no Editorial Timing Contract supplied for this lineage',
            resolved_spine_n=len([x for x in rows if x['depth']==0]),
            sequence_duration_s=f2(seq_dur),
            spine_end_s=[x for x in rows if x['depth']==0][-1]['abs_out_s'])
        json.dump(out, open(outjson,'w'), indent=1)
        print(json.dumps(out['validation'], indent=1))
        import collections
        print('total resolved elements:', len(rows))
        print('by tag:', collections.Counter(x['tag'] for x in rows))
        return
    etc = json.load(open(etc_json))
    etc_spine = etc['spine']
    mine_spine = [x for x in rows if x['depth'] == 0]
    v = dict(etc_spine_n=len(etc_spine), resolved_spine_n=len(mine_spine))
    matches = 0; mism = []
    for a, b in zip(etc_spine, mine_spine):
        if abs(a['timeline_offset_s'] - b['abs_in_s']) < 0.0005 and \
           abs(a['duration_s'] - b['duration_s']) < 0.0005:
            matches += 1
        else:
            mism.append((a['name'][:40], a['timeline_offset_s'], b['abs_in_s'],
                         a['duration_s'], b['duration_s']))
    v['spine_offset_matches'] = matches
    v['spine_mismatches'] = mism[:10]
    last = mine_spine[-1]
    v['spine_end_s'] = last['abs_out_s']
    v['sequence_duration_s'] = f2(seq_dur)
    v['spine_end_equals_lock'] = abs(last['abs_out_s'] - float(seq_dur)) < 0.0005
    v['out_of_range'] = [x['path'] for x in rows
                         if x['abs_in_s'] < -0.001 or x['abs_out_s'] > float(seq_dur)+0.001][:20]
    v['n_out_of_range'] = len([x for x in rows
                         if x['abs_in_s'] < -0.001 or x['abs_out_s'] > float(seq_dur)+0.001])
    out['validation'] = v
    json.dump(out, open(outjson,'w'), indent=1)
    print(json.dumps(v, indent=1))
    import collections
    print('total resolved elements:', len(rows))
    print('by tag:', collections.Counter(x['tag'] for x in rows))
    print('by depth:', collections.Counter(x['depth'] for x in rows))

if __name__ == '__main__':
    main(*sys.argv[1:])
