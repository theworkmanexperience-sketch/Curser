import numpy as np
U='/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/parent_audit'
FS=100
X=np.load(U+'/env_parent.npy').astype(np.float64)
def tc(x):
    h=int(x//3600); m=int((x%3600)//60); s=x-h*3600-m*60
    return "%02d:%02d:%06.3f"%(h,m,s)
def r(a,b):
    a=a-a.mean(); b=b-b.mean()
    d=np.sqrt((a*a).sum()*(b*b).sum())
    return float((a*b).sum()/d) if d>0 else 0.0
def scan(P,lag,lo,hi,W=4.0,step=0.25,label=''):
    print("--- %s  boundary scan  lag=%.3f ---"%(label,lag))
    w=int(W*FS); rows=[]
    t=lo
    while t<hi:
        a=int(t*FS); p=P[a:a+w]
        if len(p)<w: break
        i0=a; i1=a+int(round(lag*FS))
        r0=r(p,X[i0:i0+w]) if i0+w<=len(X) else 0
        r1=r(p,X[i1:i1+w]) if i1>=0 and i1+w<=len(X) else 0
        rows.append((t,r0,r1)); t+=step
    prev=None
    for t,r0,r1 in rows:
        w_ = 'HEAD(lag0)' if r0>r1 else 'BODY(lag%d)'%int(lag)
        if w_!=prev:
            print("   switch at part %s   r_lag0=%.3f  r_body=%.3f   -> %s"%(tc(t),r0,r1,w_)); prev=w_
    return rows
for k,lag in [(2,1558.430),(3,3137.830)]:
    P=np.load(U+'/env_part%d.npy'%k).astype(np.float64)
    scan(P,lag,60.0,110.0,label='PART%d'%k)
# Part3 tail: where does body alignment end
P3=np.load(U+'/env_part3.npy').astype(np.float64)
print("--- PART3 tail: last valid body window ---")
w=int(4*FS)
t=1530.0
while t<1566.0:
    a=int(t*FS); i=a+int(round(3137.830*FS))
    if i+w<=len(X) and a+w<=len(P3):
        print("   part %s -> parent %s  r=%.3f"%(tc(t),tc(i/FS),r(P3[a:a+w],X[i:i+w])))
    else:
        print("   part %s -> parent index beyond PARENT END"%tc(t))
    t+=2.0
print("PARENT env length s:", len(X)/FS, " PART3 env length s:", len(P3)/FS)
