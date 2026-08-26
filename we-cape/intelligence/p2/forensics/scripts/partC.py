import sys, json, difflib
sys.path.insert(0,'/home/claude/work/scripts')
from srt import parse, tc, norm
U='/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK'
def stream(path, dedupe_adjacent=True):
    cues=parse(path); words=[]; prev=None
    for c in cues:
        n=norm(c['text'])
        if not n: continue
        if dedupe_adjacent and n==prev: continue
        prev=n
        toks=n.split(); d=(c['end']-c['start'])/max(1,len(toks))
        for j,t in enumerate(toks):
            words.append((t, c['start']+j*d, c['i']))
    return cues, words
res={}
P_cues,P=stream(U+'/parent_audit/PARENT.srt')
L_cues,L=stream(U+'/inputs/lock_srt2.srt')
A_cues,A=stream(U+'/analysis_cut/srt_analysiscut.srt')
print("stream sizes parent=%d lock=%d analysis=%d"%(len(P),len(L),len(A)))
PT=[w[0] for w in P]
for name in ['PART1','PART2','PART3']:
    c,S=stream(U+'/parent_audit/%s.srt'%name)
    ST=[w[0] for w in S]
    sm=difflib.SequenceMatcher(None, ST, PT, autojunk=False)
    blocks=[b for b in sm.get_matching_blocks() if b.size>=6]
    tot=sum(b.size for b in blocks)
    segs=[]
    for b in blocks:
        segs.append({'part_start':round(S[b.a][1],3),'part_end':round(S[b.a+b.size-1][1],3),
                     'parent_start':round(P[b.b][1],3),'parent_end':round(P[b.b+b.size-1][1],3),
                     'n':b.size,'offset':round(P[b.b][1]-S[b.a][1],3),
                     'txt':' '.join(ST[b.a:b.a+min(b.size,8)])})
    res[name]={'part_words':len(ST),'matched_words_ge6':tot,
               'blocks':len(blocks),'segs':segs}
    print("\n=== %s : %d words, %d matched in %d blocks(>=6) ==="%(name,len(ST),tot,len(blocks)))
    for s in segs[:60]:
        print("  part %s-%s -> parent %s-%s  n=%-4d off=%+9.3f  %s"%(tc(s['part_start']),tc(s['part_end']),tc(s['parent_start']),tc(s['parent_end']),s['n'],s['offset'],s['txt'][:60]))
    if len(segs)>60: print("  ... %d more blocks"%(len(segs)-60))
json.dump(res, open('/home/claude/work/prod/partC_blocks.json','w'), indent=1)
