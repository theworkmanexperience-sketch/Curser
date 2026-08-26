import numpy as np
U='/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/parent_audit'
FS=100
X=np.load(U+'/env_parent.npy').astype(np.float64)
def tc(x):
    h=int(x//3600); m=int((x%3600)//60); s=x-h*3600-m*60
    return "%02d:%02d:%06.3f"%(h,m,s)
def r(a,b):
    a=a-a.mean(); b=b-b.mean(); d=np.sqrt((a*a).sum()*(b*b).sum())
    return float((a*b).sum()/d) if d>0 else 0.0
def fine(k,lag):
    P=np.load(U+'/env_part%d.npy'%k).astype(np.float64)
    w=int(1.0*FS); res=[]
    t=66.0
    while t<80.0:
        a=int(round(t*FS)); i1=a+int(round(lag*FS))
        r0=r(P[a:a+w],X[a:a+w]); r1=r(P[a:a+w],X[i1:i1+w])
        res.append((t,r0,r1)); t+=0.10
    last0=max((t for t,r0,r1 in res if r0>=0.90), default=None)
    first1=min((t for t,r0,r1 in res if r1>=0.90), default=None)
    print("PART%d  lag=%.3f   last window matching HEAD(lag0) at %s ; first window matching BODY at %s"%(k,lag,tc(last0) if last0 is not None else 'n/a', tc(first1) if first1 is not None else 'n/a'))
    for t,r0,r1 in res:
        if 68.0<=t<=76.5: print("    t=%7.2f  r_lag0=%+.3f  r_body=%+.3f"%(t,r0,r1))
    return last0,first1
b2=fine(2,1558.430)
print()
b3=fine(3,3137.830)
