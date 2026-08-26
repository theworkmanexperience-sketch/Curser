import numpy as np, json, sys
from numpy.fft import rfft, irfft
U='/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/parent_audit'
FS=100.0
X=np.load(U+'/env_parent.npy').astype(np.float64)
def tc(x):
    h=int(x//3600); m=int((x%3600)//60); s=x-h*3600-m*60
    return "%02d:%02d:%06.3f"%(h,m,s)
N=len(X)
cs=np.concatenate(([0.0],np.cumsum(X))); cs2=np.concatenate(([0.0],np.cumsum(X*X)))
n2=1
while n2 < N+8192: n2*=2
FX=rfft(X, n2)
def best_lag(p):
    L=len(p); pm=p-p.mean(); ps=np.sqrt((pm*pm).sum())
    if ps==0: return None
    FP=rfft(pm[::-1], n2)
    corr=irfft(FX*FP, n2)[L-1:L-1+(N-L+1)]
    s=cs[L:]-cs[:-L+0][:N-L+1] if False else (cs[L:N+1]-cs[0:N-L+1])
    s2=cs2[L:N+1]-cs2[0:N-L+1]
    var=s2-s*s/L; var[var<1e-9]=1e-9
    sc=corr/(np.sqrt(var)*ps)
    i=int(np.argmax(sc))
    return i, float(sc[i])
out={}
for k in [1,2,3]:
    P=np.load(U+'/env_part%d.npy'%k).astype(np.float64)
    W=int(30*FS); STEP=int(30*FS)
    rows=[]
    for a in range(0,len(P)-W,STEP):
        r=best_lag(P[a:a+W])
        if r is None: continue
        i,sc=r
        rows.append({'part_t':a/FS,'parent_t':i/FS,'lag':(i-a)/FS,'r':round(sc,4)})
    out['PART%d'%k]=rows
    good=[x for x in rows if x['r']>=0.5]
    lags=np.array([x['lag'] for x in good]) if good else np.array([])
    print("=== PART%d : %d windows, %d with r>=0.5 ==="%(k,len(rows),len(good)))
    if len(lags):
        print("   lag median %.3f  min %.3f  max %.3f  stdev %.3f"%(np.median(lags),lags.min(),lags.max(),lags.std()))
    for x in rows:
        flag='' if x['r']>=0.5 else '   <-- LOW'
        print("   part %s -> parent %s  lag %+9.3f  r=%.3f%s"%(tc(x['part_t']),tc(x['parent_t']),x['lag'],x['r'],flag))
json.dump(out, open('/home/claude/work/prod/partE_lags.json','w'), indent=1)
