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
CONF={1:(0.0,0.000,0.0,1648.082721),2:(75.2,1558.430,0.0,1668.911020),3:(75.6,3137.830,0.0,1566.882540)}
print("Internal continuity test: 10 s windows every 10 s across each Part BODY at the fixed body lag")
for k,(bstart,lag,_,plen) in CONF.items():
    P=np.load(U+'/env_part%d.npy'%k).astype(np.float64)
    w=int(10*FS); low=[]; n=0
    t=bstart
    while t+10.0<=plen:
        a=int(round(t*FS)); i=a+int(round(lag*FS))
        if i+w>len(X):
            low.append((t,None)); t+=10.0; continue
        rr=r(P[a:a+w],X[i:i+w]); n+=1
        if rr<0.70: low.append((t,rr))
        t+=10.0
    print("  PART%d  body lag %+.3f s : %d windows tested, %d below r=0.70"%(k,lag,n,len([x for x in low if x[1] is not None])))
    for t,rr in low:
        if rr is None: print("      part %s  -> BEYOND PARENT END"%tc(t))
        else: print("      part %s -> parent %s  r=%.3f"%(tc(t),tc(t+lag),rr))
