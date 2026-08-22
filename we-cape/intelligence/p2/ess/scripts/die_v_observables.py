#!/usr/bin/env python3
"""DIE-V observable segmentation: derive OBSERVED visual state runs from the
2 fps observable series. Pure measurement; no interpretation, no inference."""
import numpy as np, json
U="/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/"
a=np.load(U+"video_obs_2fps.npy"); FPS=2.0
R,G,B,L,S,D,LR,TOP,BOT=[a[:,i].astype(float) for i in range(9)]
t=np.arange(len(a))/FPS
def smooth(x,w):
    k=np.ones(w)/w
    return np.convolve(np.pad(x,(w//2,w//2),mode='edge'),k,mode='same')[w//2:w//2+len(x)]
Ls=smooth(L,21)          # ~10 s window
Ds=smooth(D,21)
warm=smooth((R+1)/(B+1),21)

# ---- illumination state: measured luma thresholds w/ hysteresis ----
NIGHT_IN, NIGHT_OUT = 70.0, 85.0     # measured from the bimodal luma histogram
state=[]; cur='DAY_OR_LIT_INTERIOR'
for v in Ls:
    if cur!='LOW_LIGHT_NIGHT' and v<NIGHT_IN: cur='LOW_LIGHT_NIGHT'
    elif cur=='LOW_LIGHT_NIGHT' and v>NIGHT_OUT: cur='DAY_OR_LIT_INTERIOR'
    state.append(cur)
# ---- motion class from smoothed inter-frame luma difference ----
q=np.percentile(Ds,[33,67])
def mcls(v): return 'MOTION_LOW' if v<q[0] else ('MOTION_MID' if v<q[1] else 'MOTION_HIGH')
motion=[mcls(v) for v in Ds]
# ---- shot-change density (cuts/min) from unsmoothed D ----
cut_thr=float(np.percentile(D,97))
cuts=(D>cut_thr)

def runs(labels,min_len_s=6.0):
    out=[];i=0
    while i<len(labels):
        j=i
        while j+1<len(labels) and labels[j+1]==labels[i]: j+=1
        if (j-i+1)/FPS>=min_len_s: out.append((i/FPS,(j+1)/FPS,labels[i]))
        elif out: out[-1]=(out[-1][0],(j+1)/FPS,out[-1][2])
        else: out.append((i/FPS,(j+1)/FPS,labels[i]))
        i=j+1
    # merge adjacent equal labels
    m=[]
    for s,e,l in out:
        if m and m[-1][2]==l: m[-1]=(m[-1][0],e,l)
        else: m.append((s,e,l))
    return m

ill=runs(state,20.0); mot=runs(motion,20.0)
def stats(s,e):
    i0,i1=int(s*FPS),max(int(e*FPS),int(s*FPS)+1)
    return dict(mean_luma=round(float(L[i0:i1].mean()),2),
                luma_sd=round(float(L[i0:i1].std()),2),
                mean_motion=round(float(D[i0:i1].mean()),2),
                warm_r_over_b=round(float(((R[i0:i1]+1)/(B[i0:i1]+1)).mean()),3),
                cuts_per_min=round(float(cuts[i0:i1].sum())/max(1e-9,(e-s))*60/1.0,2))
out=dict(grid_fps=FPS, n_samples=int(len(a)), duration_s=round(float(len(a)/FPS),3),
         thresholds=dict(night_in_luma=NIGHT_IN,night_out_luma=NIGHT_OUT,
                         motion_terciles=[round(float(q[0]),2),round(float(q[1]),2)],
                         cut_threshold_absdiff=round(cut_thr,2)),
         illumination_runs=[dict(start_s=round(s,1),end_s=round(e,1),state=l,**stats(s,e)) for s,e,l in ill],
         motion_runs=[dict(start_s=round(s,1),end_s=round(e,1),state=l,**stats(s,e)) for s,e,l in mot])
json.dump(out,open('/home/claude/work/out/die_v_observables.json','w'),indent=1)
print('illumination runs:',len(ill))
for s,e,l in ill: print(f'  {s:8.1f} -> {e:8.1f}  {l:22s} {stats(s,e)}')
print('motion runs:',len(mot))
for s,e,l in mot: print(f'  {s:8.1f} -> {e:8.1f}  {l}')
