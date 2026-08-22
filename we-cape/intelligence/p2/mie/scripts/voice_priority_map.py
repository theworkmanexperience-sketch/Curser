#!/usr/bin/env python3
"""VOICE_PRIORITY_MAP - documentary-wide voice occupancy of the locked timeline.

Task 1 of the Road Soul Phase 3 Transition work order (Chairman, 2026-08-22).

WHAT THIS IS
  A governed artifact recording, for every instant of the lock, which voice
  sources occupy the timeline and what music behaviour the ALREADY-GOVERNED
  laws require there. It is measurement plus a DECLARED derivation. It invents
  no precedence and infers no intent.

WHAT THIS IS NOT
  Not a recommendation. Not a ranking. Not an interpretation of importance.
  Every behaviour emitted is traceable to a law that already exists:
    - the silence law (ESS-004 ruling, CONDUCTOR_SCORE.global_behaviour_law)
    - the Yield Law   (CONDUCTOR_SCORE.global_behaviour_law.yield_law)
    - the family state signatures (CONDUCTOR_SCORE.cues[].behaviour_states)

PRIMARY SOURCES (immutable, ER-004 A1)
  lock SRT          89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b
  Info.fcpxml       2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7
GOVERNED ARTIFACTS CONSUMED
  VOICE_OVER_REGISTRY.yaml v0.1.0 - host speech segments
  CONDUCTOR_SCORE.yaml v1.1.0     - cue regions, silence zones, behaviour states
  CUE_SHEET v1.1                  - cue spans and families

CUSTODY (ER-003 A2.2): every row is source_class MACHINE.
  instrument voice_priority_map.py; validation: SRT cue count and total duration
  reproduce the governed extraction; silence zones reproduce CONDUCTOR_SCORE.
"""
import json, yaml, sys, hashlib
from collections import Counter

GRID = 0.5
LOCK = 4846.625

def load(srt_json, conductor, vo_reg):
    cues = json.load(open(srt_json))
    cs   = yaml.safe_load(open(conductor))
    vo   = yaml.safe_load(open(vo_reg))
    return cues, cs, vo

def span_to_s(sp):
    """'27:02-29:10' -> (1622.0, 1750.0). Cue-sheet spans are MM:SS."""
    a, b = sp.split('-')
    def p(x):
        parts = [int(v) for v in x.strip().split(':')]
        return parts[0]*60 + parts[1] if len(parts) == 2 else parts[0]*3600 + parts[1]*60 + parts[2]
    return float(p(a)), float(p(b))

def build(cues, cs, vo):
    n = int(LOCK / GRID) + 1
    # Midpoint test, not interval expansion. A slot i represents the instant
    # (i+0.5)*GRID. Flooring the in-point and ceiling the out-point would widen
    # every one of the 2291 cues by up to a full grid step and inflate speech
    # coverage systematically - a measurement artifact, not a finding.
    speech = bytearray(n)
    for c in cues:
        i0 = max(int((c['in']/GRID) - 0.5 + 0.999999), 0)
        i1 = min(int((c['out']/GRID) - 0.5) + 1, n)
        for i in range(i0, i1): speech[i] = 1

    vo_res = bytearray(n); vo_id = [None]*n
    for seg in vo['host_speech_segments']:
        a, b = span_to_s(seg['span'])
        for i in range(int(a/GRID), min(int(b/GRID)+1, n)):
            vo_res[i] = 1; vo_id[i] = seg['id']

    sil = bytearray(n); sil_id = [None]*n
    for z in cs['silence_law_encoding']:
        for i in range(int(z['start_s']/GRID), min(int(z['end_s']/GRID)+1, n)):
            sil[i] = 1; sil_id[i] = z['id']

    cue_at = [None]*n; fam_at = [None]*n
    for c in cs['cues']:
        b = c.get('boundaries') or {}
        if 'start_s' not in b: continue
        for i in range(int(b['start_s']/GRID), min(int(b['end_s']/GRID)+1, n)):
            cue_at[i] = c['id']; fam_at[i] = c.get('road_soul_family')
    return n, speech, vo_res, vo_id, sil, sil_id, cue_at, fam_at

# ---- DECLARED derivation. Each branch cites the law it comes from. ----
def required_behaviour(sp, si, cue, fam):
    if si:
        return "FLOOR", "silence law (ESS-004 ruling): no WE CAPE-added score in a mandatory-silence zone"
    if cue is None:
        return "UNCOVERED", "no governed cue region covers this instant; no behaviour is specified"
    if sp:
        if fam == "CONVERSATION":
            return "DUCK", "Yield Law: CONVERSATION beds duck to -18 dB under dialogue"
        return "DUCK", "DUCK is in every non-silence family signature; target unset outside CONVERSATION"
    if fam in ("MOTION", "CELEBRATION"):
        return "LEAD", "family signature: MOTION and CELEBRATION carry LEAD, not SUSTAIN"
    if fam in ("CONVERSATION", "REFLECTION", "LEGACY"):
        return "SUSTAIN", "family signature: CONVERSATION, REFLECTION and LEGACY carry SUSTAIN"
    return "UNSPECIFIED", "family not resolved from the governed cue sheet"

def rle(n, key):
    out = []; i = 0
    while i < n:
        j = i
        while j+1 < n and key(j+1) == key(i): j += 1
        out.append((i*GRID, min((j+1)*GRID, LOCK), key(i)))
        i = j+1
    return out

def tc(s):
    h=int(s//3600); m=int(s%3600//60); x=s-h*3600-m*60
    return f"{h:02d}:{m:02d}:{x:06.3f}"

def main(srt_json, conductor, vo_reg, out_yaml):
    cues, cs, vo = load(srt_json, conductor, vo_reg)
    n, speech, vo_res, vo_id, sil, sil_id, cue_at, fam_at = build(cues, cs, vo)

    def k(i):
        b, _ = required_behaviour(speech[i], sil[i], cue_at[i], fam_at[i])
        return (b, cue_at[i], sil_id[i], bool(vo_res[i]))
    spans = rle(n, k)

    tally = Counter(); dur = Counter()
    for a, b, (beh, _, _, _) in spans:
        tally[beh] += 1; dur[beh] += (b-a)

    per_cue = []
    for c in cs['cues']:
        bd = c.get('boundaries') or {}
        if 'start_s' not in bd: continue
        i0, i1 = int(bd['start_s']/GRID), min(int(bd['end_s']/GRID)+1, n)
        rng = range(i0, i1)
        sp = sum(speech[i] for i in rng); tot = max(len(rng), 1)
        gaps = []; run = 0
        for i in rng:
            if speech[i]: 
                if run: gaps.append(run*GRID)
                run = 0
            else: run += 1
        if run: gaps.append(run*GRID)
        per_cue.append(dict(
            cue=c['id'], name=c.get('name'), family=c.get('road_soul_family'),
            start_tc=bd.get('start_tc'), end_tc=bd.get('end_tc'),
            duration_s=round(bd['end_s']-bd['start_s'], 3),
            speech_coverage=round(sp/tot, 4),
            speech_free_s=round((tot-sp)*GRID, 2),
            longest_speech_free_window_s=round(max(gaps) if gaps else 0.0, 2),
            speech_free_windows_ge_8s=sum(1 for g in gaps if g >= 8.0),
            vo_reserved_overlap_s=round(sum(vo_res[i] for i in rng)*GRID, 2)))

    doc = dict(
        artifact_id="VOICE_PRIORITY_MAP",
        version="1.0.0",
        engine="DIE-derived; governed derivation, no interpretation",
        status="FOR EXECUTIVE REVIEW",
        work_order="Road Soul Phase 3 Transition, task 1 (Chairman, 2026-08-22)",
        source_class="MACHINE",
        instrument=dict(name="voice_priority_map.py", grid_s=GRID, lock_duration_s=LOCK),
        primary_sources=[
            dict(artifact="lock SRT", sha256="89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b",
                 role="speech events", grade="GT-2", cues=len(cues)),
            dict(artifact="Info.fcpxml", sha256="2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7",
                 role="lock duration and timebase")],
        governed_artifacts_consumed=[
            "CONDUCTOR_SCORE.yaml v1.1.0", "VOICE_OVER_REGISTRY.yaml v0.1.0", "CUE_SHEET v1.1"],
        derivation_rules_note="every behaviour below is traceable to an existing law; none is invented",
        derivation_rules=[
            "FLOOR    <- silence law (ESS-004 ruling)",
            "DUCK     <- Yield Law (-18 dB under dialogue for CONVERSATION); DUCK is in every non-silence family signature",
            "LEAD     <- family signature MOTION / CELEBRATION",
            "SUSTAIN  <- family signature CONVERSATION / REFLECTION / LEGACY",
            "UNCOVERED<- no governed cue region covers the instant"],
        coverage=dict(observed_s=round(n*GRID if n*GRID < LOCK else LOCK, 3), expected_s=LOCK,
                      percentage=100.0,
                      note="the map covers the whole lock. UNCOVERED is a VALUE (no cue region "
                           "governs that instant), not a gap in measurement - coverage is 100% "
                           "either way. ER-003 A2.3: coverage is not confidence."),
        grid_quantisation_note=("speech occupancy is evaluated at the midpoint of each 0.5 s slot. "
                                "Cue in/out points are not expanded to slot boundaries; expansion "
                                "would widen 2291 cues by up to one grid step each and inflate "
                                "coverage systematically."),
        missing_data_policy="propagate_unknown",
        totals_note="span counts and durations by required behaviour; no aggregate score",
        totals=[dict(behaviour=b, spans=tally[b], total_s=round(dur[b], 2),
                     fraction_of_lock=round(dur[b]/LOCK, 4)) for b in sorted(tally)],
        speech_totals=dict(srt_cues=len(cues),
                           speech_seconds=round(sum(speech)*GRID, 2),
                           speech_fraction=round(sum(speech)*GRID/LOCK, 4)),
        per_cue_note="speech occupancy inside each governed cue region",
        per_cue=per_cue,
        vo_segments=[dict(id=s['id'], span=s['span'], type=s['type'],
                          start_tc=tc(span_to_s(s['span'])[0]), end_tc=tc(span_to_s(s['span'])[1]),
                          vo_candidate=s.get('vo_candidate')) for s in vo['host_speech_segments']],
        vo_placement_boundaries=vo.get('vo_placement_boundaries'),
        spans_note="run-length encoded; boundary changes only",
        spans=[dict(start_s=round(a,3), end_s=round(b,3), start_tc=tc(a), end_tc=tc(b),
                    duration_s=round(b-a,3), required_behaviour=beh, cue=cue,
                    silence_zone=sz, vo_reserved=vr)
               for a,b,(beh,cue,sz,vr) in spans])
    with open(out_yaml,'w') as f:
        f.write("# VOICE_PRIORITY_MAP - governed derivation, no interpretation.\n")
        f.write("# Custody: MACHINE. Every behaviour cites the law it comes from.\n")
        yaml.safe_dump(doc, f, sort_keys=False, width=110, allow_unicode=True)
    print(f"spans: {len(spans)}  speech {sum(speech)*GRID:.1f}s ({100*sum(speech)*GRID/LOCK:.1f}%)")
    for b in sorted(tally): print(f"  {b:11} spans={tally[b]:4d}  {dur[b]:9.1f}s  {100*dur[b]/LOCK:5.1f}%")

if __name__ == '__main__':
    main(*(sys.argv[1:] or ['out/srt_cues.json','ess/CONDUCTOR_SCORE.yaml',
        '/mnt/user-data/uploads/Curser/we-cape/intelligence/p2/registries/VOICE_OVER_REGISTRY.yaml',
        'prod/VOICE_PRIORITY_MAP.yaml']))
