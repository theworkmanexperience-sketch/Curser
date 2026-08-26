import sys, hashlib, json
sys.path.insert(0,'/home/claude/work/scripts')
from srt import parse, tc, norm
U='/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK'
F={'PARENT':U+'/parent_audit/PARENT.srt','PART1':U+'/parent_audit/PART1.srt',
   'PART2':U+'/parent_audit/PART2.srt','PART3':U+'/parent_audit/PART3.srt',
   'LOCK':U+'/inputs/lock_srt2.srt','ANALYSIS_CUT':U+'/analysis_cut/srt_analysiscut.srt'}
out={}
for k,p in F.items():
    c=parse(p)
    h=hashlib.sha256(open(p,'rb').read()).hexdigest()
    dup=sum(1 for a,b in zip(c,c[1:]) if norm(a['text'])==norm(b['text']) and norm(a['text']))
    zero=sum(1 for x in c if x['end']<=x['start'])
    ov=sum(1 for a,b in zip(c,c[1:]) if b['start']<a['end']-1e-9)
    gaps=[(b['start']-a['end']) for a,b in zip(c,c[1:])]
    big=[(i+1,round(g,3),tc(c[i]['end']),tc(c[i+1]['start'])) for i,g in enumerate(gaps) if g>=10.0]
    words=sum(len(norm(x['text']).split()) for x in c)
    cov=sum(max(0.0,x['end']-x['start']) for x in c)
    out[k]={'sha256':h,'cues':len(c),'first_start':tc(c[0]['start']),'first_text':c[0]['text'][:80],
            'last_end':tc(c[-1]['end']),'last_text':c[-1]['text'][:80],
            'span_s':round(c[-1]['end']-c[0]['start'],3),'last_end_s':round(c[-1]['end'],3),
            'adjacent_identical_text_pairs':dup,'nonpositive_duration_cues':zero,'overlapping_pairs':ov,
            'gaps_ge_10s':len(big),'largest_gaps':sorted(big,key=lambda t:-t[1])[:8],
            'words':words,'captioned_time_s':round(cov,3)}
print(json.dumps(out,indent=1))
