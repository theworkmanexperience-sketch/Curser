#!/usr/bin/env python3
"""Independent semantic anchor test: ETC title text <-> lock-SRT cue text.
Measures delta(title_in - matched_cue_start) at points spread across the film.
A constant, small delta across the runtime == zero timebase offset."""
import re,json,numpy as np
U="/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/"
def parse(p):
    out=[]
    for b in re.split(r'\n\s*\n', open(p,encoding='utf-8-sig').read().strip()):
        L=[x for x in b.strip().split('\n') if x.strip()]
        if len(L)<2: continue
        m=re.match(r'(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)',L[1])
        if not m: continue
        g=[int(x) for x in m.groups()]
        out.append(dict(i=int(L[0]),s=g[0]*3600+g[1]*60+g[2]+g[3]/1000,
                        e=g[4]*3600+g[5]*60+g[6]+g[7]/1000,t=' '.join(L[2:])))
    return out
cues=parse(U+"inputs/lock_srt2.srt")
tl=json.load(open('/home/claude/work/out/timeline_resolved.json'))
titles=sorted([x for x in tl['elements'] if x['tag']=='title'],key=lambda y:y['abs_in_s'])
def norm(s): return re.sub(r'[^a-z ]',' ',s.lower()).split()
def score(a,b):
    A,B=set(norm(a)),set(norm(b))
    A={w for w in A if len(w)>2}; B={w for w in B if len(w)>2}
    return len(A&B)/max(1,len(A))
rows=[]
for t in titles:
    if not t['text'].strip(): continue
    win=[c for c in cues if abs(c['s']-t['abs_in_s'])<=25]
    best=None
    for c in win:
        sc=score(t['text'],c['t'])
        if sc>=0.6 and (best is None or sc>best[0]): best=(sc,c)
    if best:
        sc,c=best
        rows.append(dict(title_in=round(t['abs_in_s'],3),title=t['text'][:52],
                         cue=c['i'],cue_s=round(c['s'],3),cue_text=c['t'][:56],
                         delta_title_minus_cue=round(t['abs_in_s']-c['s'],3),match=round(sc,2)))
d=np.array([r['delta_title_minus_cue'] for r in rows]) if rows else np.array([])
print(f"anchors found: {len(rows)}")
for r in rows:
    print(f"  t={r['title_in']:9.3f}  d={r['delta_title_minus_cue']:+7.3f}  m={r['match']:.2f}  "
          f"{r['title']!r} <- cue#{r['cue']} {r['cue_text']!r}")
if len(d):
    print(f"\ndelta: n={len(d)} median={np.median(d):+.3f}s mean={d.mean():+.3f}s "
          f"sd={d.std():.3f}s min={d.min():+.3f} max={d.max():+.3f}")
    print(f"span of anchors: {min(r['title_in'] for r in rows):.1f}s .. {max(r['title_in'] for r in rows):.1f}s")
json.dump(rows,open('/home/claude/work/out/step0_anchors.json','w'),indent=1)
