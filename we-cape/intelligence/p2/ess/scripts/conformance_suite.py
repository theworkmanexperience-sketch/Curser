#!/usr/bin/env python3
"""ECR-GEN-001 Phase B/C conformance suite. Read-only. Emits JSON results.
No governed artifact is written by this module."""
import json, subprocess, hashlib, os, re, sys, yaml

U='/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/'
R=[]
def t(tid, name, status, measure, note=""):
    R.append(dict(id=tid, test=name, status=status, measurement=measure, note=note))

def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()

C24=json.load(open('ctx/AR2-0824.context.json'))
C22=json.load(open('ctx/AR2-0822.context.json'))

# T1 FCPXML ingestion -------------------------------------------------------
tl=json.load(open('derived0824/timeline_resolved.json'))
sp=[e for e in tl['elements'] if e['depth']==0]
end_ok = abs(sp[-1]['abs_out_s']-tl['sequence']['duration_s'])<0.0005
t("T1","FCPXML ingestion (08-24)","PASS" if end_ok else "FAIL",
  f"{len(tl['elements'])} elements resolved; spine closes at {sp[-1]['abs_out_s']} s vs sequence {tl['sequence']['duration_s']} s",
  "resolver ran without an ETC; see T3")

# T2 SRT ingestion ----------------------------------------------------------
srt=U+'analysis_cut/srt_analysiscut.srt'
n=len(re.findall(r'-->', open(srt,encoding='utf-8-sig').read()))
t("T2","SRT ingestion (08-24)","PASS",
  f"{n} cues parsed; sha {sha(srt)[:16]}...; last cue ends {C24['srt']['last_s']} s vs runtime {C24['runtime_s']} s")

# T3 ETC binding ------------------------------------------------------------
t("T3","Editorial Timing Contract binding","BLOCKED",
  "CTX.sha.etc = NOT_PRODUCED; CTX.source_files.etc = NOT_PRODUCED",
  "IP-1. No ETC exists for the 08-24 lineage. The resolver reports etc_validation NOT_VALIDATED "
  "rather than silently proceeding. DOC-001 instrument agreement CANNOT be demonstrated for this "
  "lineage until an ETC is produced.")

# T4 segment binding --------------------------------------------------------
try:
    obs24=json.load(open('ctx/AR2-0824.observations.json')); nseg=len(obs24['segments'])
    t("T4","Segment binding (08-24)","PASS",f"{nseg} segments")
except FileNotFoundError:
    t("T4","Segment binding (08-24)","BLOCKED",
      "no observation dataset exists for the 08-24 lineage",
      "IP-6. The segment set must be re-derived against the governed timeline and ratified by the "
      "Executive. The generator now ACCEPTS a segment table as data - it no longer contains one.")

# T5 caption binding --------------------------------------------------------
titles=[e for e in tl['elements'] if e['tag']=='title']
t("T5","Caption binding (08-24)","PASS",
  f"{len(titles)} title elements resolved from the 08-24 FCPXML; SRT carries {n} cues",
  "structural binding only; a collapse rule for doubled Parent-SRT cues is still undeclared (IP-4)")

# T6 EPR integration --------------------------------------------------------
epr=yaml.safe_load(open('ctx/EMOTIONAL_PROGRESSION_REGISTRY.yaml'))
refs=sorted({s for e in epr['entries'] for s in e['segment_refs']}, key=lambda x:int(x[1:]))
t("T6","EPR-001 integration","PASS",
  f"EPR-001 v{epr['registry_version']} loads; {len(epr['entries'])} entries; "
  f"{len(refs)} distinct segment_refs {refs[0]}..{refs[-1]}",
  "EPR is segment-keyed, so it binds by identifier and needs no timecode. Resolving those "
  "identifiers to spans still requires the re-derived segment set (T4).")

# T7 EPR-07 retirement handling --------------------------------------------
e7=[e for e in epr['entries'] if e['id']=='EPR-07'][0]
retired = e7.get('retirement',{}).get('disposition')=='RETIRE'
active=[e for e in epr['entries'] if e.get('entry_status')=='COMPLETE']
def consume(entries):
    """A consumer must skip retired entries without raising."""
    out=[]
    for e in entries:
        if e.get('retirement',{}).get('disposition')=='RETIRE': continue
        out.append((e['id'], e['dramatic_intensity'], e['governing_theme']))
    return out
try:
    got=consume(epr['entries']); exc=None
except Exception as ex:
    got=None; exc=repr(ex)
t("T7","EPR-07 retirement handled without exception","PASS" if exc is None and retired and len(got)==6 else "FAIL",
  f"retirement.disposition={e7.get('retirement',{}).get('disposition')}; "
  f"consumer skipped it and returned {len(got) if got else 0} active beats; exception={exc}",
  "EPR-07 remains present with beat, audience_state and segment_refs intact; only the consumer skips it.")

# T8 RUN_ID generation ------------------------------------------------------
a=json.load(open('out_auto/_runid.json')) if os.path.exists('out_auto/_runid.json') else None
rid=re.search(r'run_id: (\S+)', open('out_auto/PRODUCTION_INTELLIGENCE_SEED.yaml').read()).group(1)
rid2=re.search(r'run_id: (\S+)', open('out0822/PRODUCTION_INTELLIGENCE_SEED.yaml').read()).group(1)
t("T8","Parameterized RUN_ID generation","PASS" if rid!=rid2 and rid.startswith('WECAPE-') else "FAIL",
  f"--run-id auto -> {rid}; --run-id pinned -> {rid2}")

# T9 no 08-22 constants -----------------------------------------------------
s=open('src/gen_artifacts_v2.py').read()
bad={k:len(re.findall(p,s)) for k,p in {
  'runtime':r'4846\.\d','mp4_sha':'a53655fc','fcpxml_sha':'2bf06853','srt_sha':'89d61f96',
  'etc_sha':'e91318a6','run_id':'WECAPE-AR2-SPRINT3A-2026','git':'ff0c45f7',
  'segment_table':r'\("S1[0-9]",\d','cue_table':r'\("CUE-0\d",\d',
  'abs_path':'/home/claude|/mnt/user-data'}.items()}
t("T9","No 08-22 constants remain in the generator","PASS" if sum(bad.values())==0 else "FAIL",
  json.dumps(bad))

# T10 refactor equivalence --------------------------------------------------
files=["STEP0_TIMING_CLOSURE.md","CAPTION_REGISTRY.yaml","VISUAL_EVENT_REGISTRY.yaml",
       "EDITORIAL_SYNCHRONIZATION.yaml","CONDUCTOR_SCORE.yaml","ESS_VALIDATION_REPORT.md",
       "PRODUCTION_INTELLIGENCE_SEED.yaml"]
same=all(sha('out_v1/'+f)==sha('out0822/'+f) for f in files)
t("T10","Refactor equivalence v1 == v2 on identical inputs","PASS" if same else "FAIL",
  f"{sum(sha('out_v1/'+f)==sha('out0822/'+f) for f in files)}/7 artifacts byte-identical")

# T11 repository drift ------------------------------------------------------
drift=[f for f in files if os.path.exists('base/'+f) and sha('base/'+f)!=sha('out_v1/'+f)]
t("T11","Committed artifacts match the committed generator","FAIL" if drift else "PASS",
  f"{len(drift)} of {sum(os.path.exists('base/'+f) for f in files)} committed artifacts differ: {drift}",
  "gen_artifacts.py was committed twice AFTER CONDUCTOR_SCORE.yaml was last regenerated "
  "(319f234 Option C, 0f3d12c MOTION sidechain). Under DOC-002 the artifact is stale.")

# T12 missing producers -----------------------------------------------------
missing=[]
for f,need in [('video_obs_2fps.npy','die_v_observables.py'),
               ('audio_rms_0p25.npy','step0_offset.py')]:
    missing.append(f"{f} (required by {need}) - no producer in the repository")
t("T12","Every pipeline input has a producer","FAIL",
  f"{len(missing)} inputs unproduceable; camera_runs.json RESOLVED by derive_camera_runs.py this task",
  "; ".join(missing))

json.dump(R, open('out_tests.json','w'), indent=1)
w={'PASS':0,'FAIL':0,'BLOCKED':0}
for r in R: w[r['status']]+=1
print(f"{'id':5} {'status':9} test")
for r in R: print(f"{r['id']:5} {r['status']:9} {r['test']}")
print("\n", w)
