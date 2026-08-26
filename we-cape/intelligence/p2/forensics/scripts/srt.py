"""SRT parser + normalisation helpers. Custody: MACHINE.
Used by DAY2_PARENT_FORENSIC_AUDIT.md (2026-08-26)."""
import re
TS = re.compile(r'(\d+):(\d\d):(\d\d)[,.](\d\d\d)\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d\d\d)')
def secs(h,m,s,ms): return int(h)*3600+int(m)*60+int(s)+int(ms)/1000.0
def parse(path):
    raw = open(path, 'r', encoding='utf-8-sig', errors='replace').read()
    blocks = re.split(r'\r?\n\r?\n+', raw.strip())
    cues=[]
    for b in blocks:
        lines=[l for l in b.splitlines() if l.strip()!='']
        if not lines: continue
        ti=None
        for i,l in enumerate(lines):
            if TS.search(l): ti=i; break
        if ti is None: continue
        m=TS.search(lines[ti])
        cues.append({'i':len(cues)+1,'start':secs(*m.group(1,2,3,4)),
                     'end':secs(*m.group(5,6,7,8)),'text':' '.join(lines[ti+1:]).strip()})
    return cues
def tc(x):
    h=int(x//3600); m=int((x%3600)//60); s=x-h*3600-m*60
    return "%02d:%02d:%06.3f"%(h,m,s)
def norm(t):
    t=t.lower(); t=re.sub(r"[^a-z0-9' ]+",' ',t)
    return re.sub(r'\s+',' ',t).strip()
