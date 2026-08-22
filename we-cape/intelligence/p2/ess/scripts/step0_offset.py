#!/usr/bin/env python3
"""Step 0 offset model, final.
Method A: SRT speech-mask x audio-envelope cross-correlation, with a
          circular-shift null distribution, edge rejection and sign gating.
Method B: SRT cue-start x picture-cut coincidence (SRT x FCPXML, no audio).
A segment is only assigned an offset if the peak beats its own null at p<0.05.
Otherwise it is INDETERMINATE with a categorized reason. Never inferred."""
import re, json, numpy as np
U="/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/"
H=0.25; RNG=np.random.default_rng(20260822)

def parse_srt(p):
    out=[]
    for b in re.split(r'\n\s*\n', open(p,encoding='utf-8-sig').read().strip()):
        L=[x for x in b.strip().split('\n') if x.strip()]
        if len(L)<2: continue
        m=re.match(r'(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)',L[1])
        if not m: continue
        g=[int(x) for x in m.groups()]
        out.append(dict(idx=int(L[0]),start=g[0]*3600+g[1]*60+g[2]+g[3]/1000,
                        end=g[4]*3600+g[5]*60+g[6]+g[7]/1000,text=' '.join(L[2:])))
    return out

cues=parse_srt(U+"inputs/lock_srt2.srt")
rms=np.load(U+"audio_rms_0p25.npy").astype(np.float64); N=len(rms)
mask=np.zeros(N)
for c in cues:
    mask[max(0,int(round(c['start']/H))):min(N,int(round(c['end']/H)))]=1.0
env=np.log10(rms+1e-6)

def z(x):
    x=np.asarray(x,float); s=x.std(); return (x-x.mean())/(s if s>1e-12 else 1.0)

def xcorr(e,m,maxlag_s):
    L=np.arange(-int(maxlag_s/H),int(maxlag_s/H)+1); e=z(e); m=z(m); out=[]
    for l in L:
        l=int(l)
        a,b=(e[l:],m[:len(e)-l]) if l>=0 else (e[:l],m[-l:])
        n=min(len(a),len(b))
        out.append(float(np.dot(a[:n],b[:n])/n) if n>50 else np.nan)
    return L*H, np.array(out)

def method_a(e,m,maxlag_s=12.0,ntrial=200):
    if len(e)<int(maxlag_s/H)*3: return dict(status="INDETERMINATE",
        reason="WINDOW_TOO_SHORT_FOR_LAG_SEARCH")
    lag,c=xcorr(e,m,maxlag_s); ok=~np.isnan(c)
    lag,c=lag[ok],c[ok]
    j=int(np.argmax(c)); peak=float(c[j]); best=float(lag[j])
    # null: circularly rotate the mask far beyond the search window
    nulls=[]
    lo=int(maxlag_s/H)*2
    for _ in range(ntrial):
        k=int(RNG.integers(lo,max(lo+1,len(m)-lo)))
        _,cn=xcorr(e,np.roll(m,k),maxlag_s)
        cn=cn[~np.isnan(cn)]
        if len(cn): nulls.append(float(np.nanmax(cn)))
    nulls=np.array(nulls); p=float((nulls>=peak).mean()) if len(nulls) else 1.0
    r=dict(best_lag_s=round(best,3),peak=round(peak,4),
           corr_at_zero=round(float(c[np.argmin(np.abs(lag))]),4),
           null_p=round(p,4),null_p95=round(float(np.percentile(nulls,95)),4) if len(nulls) else None)
    if peak<=0: r.update(status="INDETERMINATE",reason="NO_POSITIVE_CORRELATION_PEAK")
    elif abs(abs(best)-maxlag_s)<1e-6: r.update(status="INDETERMINATE",
            reason="ARGMAX_AT_SEARCH_WINDOW_EDGE(no interior peak)")
    elif p>=0.05: r.update(status="INDETERMINATE",
            reason=f"PEAK_NOT_SIGNIFICANT_VS_NULL(p={p:.3f})")
    elif abs(best)<=0.5: r.update(status="ALIGNED_ZERO_OFFSET")
    else: r.update(status="SHIFT_DETECTED")
    return r

res={'method':'A=envelope-xcorr w/ circular-shift null; B=cue-start vs picture-cut'}
res['inputs']=dict(n_cues=len(cues),srt_first_start=cues[0]['start'],
                   srt_last_end=cues[-1]['end'],env_seconds=round(N*H,3))
res['global_A']=method_a(env,mask,40.0,300)

# ---------------- Method B : SRT cue starts vs picture cuts ----------------
tl=json.load(open('/home/claude/work/out/timeline_resolved.json'))
cuts=np.array(sorted({round(x['abs_in_s'],3) for x in tl['elements']
                      if x['depth']==0 and x['tag']!='transition'}))
starts=np.array([c['start'] for c in cues])
def coincidence(off,tol=0.5):
    s=starts+off
    idx=np.searchsorted(cuts,s)
    d=[]
    for si,i in zip(s,idx):
        cands=[cuts[k] for k in (i-1,i) if 0<=k<len(cuts)]
        d.append(min(abs(si-c) for c in cands) if cands else 9e9)
    d=np.array(d); return float((d<=tol).mean()), d
offs=np.arange(-10,10.001,0.125)
scores=[coincidence(o)[0] for o in offs]
scores=np.array(scores); jb=int(np.argmax(scores))
res['global_B']=dict(n_picture_cuts=len(cuts),n_cue_starts=len(starts),
    best_offset_s=round(float(offs[jb]),3), hit_rate_at_best=round(float(scores[jb]),4),
    hit_rate_at_zero=round(float(scores[np.argmin(np.abs(offs))]),4),
    baseline_median_hit_rate=round(float(np.median(scores)),4),
    curve_top5=[[round(float(offs[k]),3),round(float(scores[k]),4)]
                for k in np.argsort(scores)[::-1][:5]])

segs=[("S01","00:00","01:13","cold_open"),("S02","01:13","01:51","host_day_brief"),
      ("S03","01:51","27:02","interview_gauntlet_1"),("S04","27:02","27:23","ride_brief"),
      ("S05","27:40","29:10","escort_ride"),("S06","31:43","32:33","librarian_speech"),
      ("S07","32:45","33:50","council_profile"),("S08","33:51","35:56","town_proclamation"),
      ("S09","36:03","36:30","first_ride_moment"),("S10","36:59","38:52","state_proclamation"),
      ("S11","38:55","52:00","interview_gauntlet_2"),("S12","52:04","53:56","honors_and_silence"),
      ("S13","53:50","54:35","group_photo"),("S14","54:36","55:24","service_wrap_preview"),
      ("S15","56:10","58:43","riding_music_passage"),("S16","58:43","66:25","bike_night_arrivals"),
      ("S17","66:25","66:48","audience_cta"),("S18","69:25","79:40","bike_night_ambience"),
      ("S19","79:44","80:46","friday_wrap_part3_tease")]
def ms(x): m,s=x.split(':'); return int(m)*60+int(s)
per=[]
for sid,a,b,act in segs:
    s0,s1=ms(a),ms(b); i0,i1=int(s0/H),int(s1/H); dur=s1-s0
    cov=float(mask[i0:i1].mean()) if i1>i0 else 0.0
    row=dict(seg=sid,activity=act,span=f"{a}-{b}",start_s=s0,end_s=s1,dur_s=dur,
             srt_speech_coverage=round(cov,4),
             n_cues_in_span=int(sum(1 for c in cues if s0<=c['start']<s1)))
    if dur<60: row.update(status="INDETERMINATE",
        reason="SEGMENT_SHORTER_THAN_LAG_SEARCH_WINDOW(<60s)")
    elif cov<0.30: row.update(status="INDETERMINATE",
        reason="INSUFFICIENT_SRT_SPEECH_IN_SPAN(<30%) — non-speech segment by design")
    else: row.update(method_a(env[i0:i1],mask[i0:i1],12.0,150))
    per.append(row)
res['per_segment']=per
res['summary']=dict(
    aligned=sum(1 for r in per if r['status']=='ALIGNED_ZERO_OFFSET'),
    shifted=sum(1 for r in per if r['status']=='SHIFT_DETECTED'),
    indeterminate=sum(1 for r in per if r['status']=='INDETERMINATE'),
    aligned_seconds=sum(r['dur_s'] for r in per if r['status']=='ALIGNED_ZERO_OFFSET'),
    indeterminate_seconds=sum(r['dur_s'] for r in per if r['status']=='INDETERMINATE'))
json.dump(res,open('/home/claude/work/out/step0_offset.json','w'),indent=1)
print(json.dumps({k:v for k,v in res.items() if k!='per_segment'},indent=1))
print("--- per segment ---")
for r in per:
    print(f"{r['seg']:4s} {r['span']:14s} {r['dur_s']:5d}s cov={r['srt_speech_coverage']:.2f} "
          f"cues={r['n_cues_in_span']:4d} {r['status']:22s} "
          f"lag={r.get('best_lag_s','-')} p={r.get('null_p','-')} {r.get('reason','')}")
