#!/usr/bin/env python3
"""Independent semantic anchor test: ETC title text <-> lock-SRT cue text.
Measures delta(title_in - matched_cue_start) at points spread across the film.
A constant, small delta across the runtime == zero timebase offset.

usage: step0_anchors.py --srt <lock.srt> --timeline <timeline_resolved.json>
                        --out <step0_anchors.json>

ECR-GEN-003 (path parameterization only; matching rule and statistics unchanged):
inputs and output are explicit arguments, replacing the machine-specific Sprint 3A
paths. A deterministic provenance sidecar `<out>.provenance.json` is written."""
import re,json,numpy as np
import argparse,hashlib,os,platform,sys
_AP=argparse.ArgumentParser(description='Step 0 semantic anchors: ETC title text vs lock-SRT cue text.')
_AP.add_argument('--srt',required=True)
_AP.add_argument('--timeline',required=True)
_AP.add_argument('--out',required=True)
A=_AP.parse_args()
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
cues=parse(A.srt)
tl=json.load(open(A.timeline))
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
with open(A.out,'w') as _fh: json.dump(rows,_fh,indent=1)

def _sha256(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
with open(A.out+'.provenance.json','w') as _fh:
    _fh.write(json.dumps(dict(schema='b3-provenance/1',
        producer=os.path.basename(__file__),producer_sha256=_sha256(__file__),
        arguments=dict(),
        inputs=[dict(role=r,path=p,sha256=_sha256(p),bytes=os.path.getsize(p)) for r,p in
                (('srt',A.srt),('timeline',A.timeline))],
        outputs=[dict(path=os.path.basename(A.out),sha256=_sha256(A.out),bytes=os.path.getsize(A.out))],
        toolchain=dict(python=platform.python_version(),implementation=sys.implementation.name,
                       interpreter=os.path.realpath(sys.executable),machine=platform.machine(),
                       numpy=dict(version=np.__version__))),
        indent=1,sort_keys=True)+'\n')
