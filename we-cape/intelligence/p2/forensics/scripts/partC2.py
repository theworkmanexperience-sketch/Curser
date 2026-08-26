import sys, json, difflib, statistics as st
sys.path.insert(0,'/home/claude/work/scripts')
from srt import parse, tc, norm
U='/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK'
def stream(path):
    cues=parse(path); words=[]; prev=None
    for c in cues:
        n=norm(c['text'])
        if not n: continue
        if n==prev: continue
        prev=n
        toks=n.split(); d=(c['end']-c['start'])/max(1,len(toks))
        for j,t in enumerate(toks): words.append((t, c['start']+j*d, c['start'], c['i']))
    return cues, words
P_cues,P=stream(U+'/parent_audit/PARENT.srt')
PT=[w[0] for w in P]
summary={}
for name in ['PART1','PART2','PART3']:
    c,S=stream(U+'/parent_audit/%s.srt'%name); ST=[w[0] for w in S]
    sm=difflib.SequenceMatcher(None, ST, PT, autojunk=False)
    bl=[b for b in sm.get_matching_blocks() if b.size>=6]
    offs=[P[b.b][2]-S[b.a][2] for b in bl]
    f,l=bl[0],bl[-1]
    # parent words covered by matched blocks
    covered=set()
    for b in bl:
        for k in range(b.b,b.b+b.size): covered.add(k)
    # part cue indices matched
    pc=set()
    for b in bl:
        for k in range(b.a,b.a+b.size): pc.add(S[k][3])
    summary[name]={
     'part_cues':len(c),'part_words':len(ST),
     'matched_words':sum(b.size for b in bl),'blocks':len(bl),
     'part_cues_with_match':len(pc),
     'part_span':[tc(c[0]['start']),tc(c[-1]['end'])],
     'first_match':{'part':tc(S[f.a][2]),'parent':tc(P[f.b][2]),'n':f.size,'txt':' '.join(ST[f.a:f.a+10])},
     'last_match':{'part':tc(S[l.a][2]),'parent':tc(P[l.b][2]),'n':l.size,'txt':' '.join(ST[l.a:l.a+10])},
     'offset_median':round(st.median(offs),3),'offset_min':round(min(offs),3),'offset_max':round(max(offs),3),
     'offset_stdev':round(st.pstdev(offs),3),
     'parent_region':[tc(min(P[b.b][2] for b in bl)), tc(max(P[b.b+b.size-1][2] for b in bl))],
     'parent_words_covered':len(covered),
    }
print(json.dumps(summary,indent=1))
print("\nparent stream words:",len(PT))
# where does each part's parent region sit
