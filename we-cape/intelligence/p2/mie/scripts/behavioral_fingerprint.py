#!/usr/bin/env python3
"""BEHAVIORAL_FINGERPRINT - measured behavioural transitions of the locked cut.

Executive Disposition, 2026-08-22, EMB-CUE-03 Continuation item 7:
  "Engineering is encouraged to preserve the measured behavioral transitions
   (e.g., the 34-second speech-free window) as behavioral fingerprints, NOT as
   arguments for boundary changes."

THIS FILE MAKES NO ARGUMENT. Every row is a measurement with a method. No row
recommends a boundary, ranks a cue, or expresses a preference (ER-001).
Significance is Executive (ER-003 Layer 3). Custody: MACHINE.

Why this exists: ER-003 - mechanics precede meaning. A fingerprint's value is
often unknown at ingestion. That uncertainty is not grounds for discarding it.
"""
import yaml, json, sys, statistics as st

G, LOCK = 0.5, 4846.625
def tc(s):
    h=int(s//3600); m=int(s%3600//60); x=s-h*3600-m*60
    return f"{h:02d}:{m:02d}:{x:06.3f}"
def ov(a0,a1,b0,b1): return max(0.0, min(a1,b1)-max(a0,b0))

def main(conductor, caption, vpm_path, tl_json, out_yaml):
    cs  = yaml.safe_load(open(conductor))
    cap = yaml.safe_load(open(caption))['captions']
    vpm = yaml.safe_load(open(vpm_path))
    els = json.load(open(tl_json))['elements']
    percue = {c['cue']: c for c in vpm['per_cue']}

    prim = sorted([e for e in els if e['depth']==0 and e['tag']!='transition'],
                  key=lambda e: e['abs_in_s'])
    cuts = sorted({round(e['abs_in_s'],3) for e in prim})
    trans = [e for e in els if e['tag']=='transition']
    maps  = [e for e in els if 'map' in (e['name'] or '').lower()]
    gfx   = [e for e in els if e['tag']=='video' and e['name'] and not e['name'].startswith('DJI_')]
    caps  = [(t['span']['start_s'], t['span']['end_s']) for t in cap]

    prints = []
    for c in cs['cues']:
        b = c.get('boundaries') or {}
        if 'start_s' not in b: continue
        a0, a1 = b['start_s'], b['end_s']; dur = a1-a0
        pc = percue.get(c['id'], {})

        inner = [x for x in cuts if a0 < x < a1]
        shots = [b_-a_ for a_,b_ in zip([a0]+inner, inner+[a1])]
        ntr = sum(1 for e in trans if ov(a0,a1,e['abs_in_s'],e['abs_out_s'])>0)
        trd = [e['duration_s'] for e in trans
               if ov(a0,a1,e['abs_in_s'],e['abs_out_s'])>0 and e['duration_s']]

        n = int(dur/G)+1; occ = bytearray(n)
        for x0,x1 in caps + [(e['abs_in_s'],e['abs_out_s']) for e in maps+gfx]:
            for i in range(max(0,int((x0-a0)/G)), min(n,int((x1-a0)/G)+1)): occ[i]=1
        orient_s = sum(occ)*G

        prints.append(dict(
            cue=c['id'], name=c.get('name'), family=c.get('road_soul_family'),
            span=dict(start_tc=b.get('start_tc'), end_tc=b.get('end_tc'), duration_s=round(dur,3)),
            cutting=dict(
                internal_cuts=len(inner),
                cuts_per_min=round(len(inner)/dur*60, 2),
                mean_shot_s=round(st.mean(shots), 3) if shots else None,
                median_shot_s=round(st.median(shots), 3) if shots else None,
                longest_shot_s=round(max(shots), 3) if shots else None,
                method="FCPXML primary spine, depth-0, transitions excluded"),
            transitions=dict(
                count=ntr,
                mean_duration_s=round(st.mean(trd), 3) if trd else None,
                method="FCPXML transition elements intersecting the span"),
            speech=dict(
                coverage=pc.get('speech_coverage'),
                free_total_s=pc.get('speech_free_s'),
                longest_free_window_s=pc.get('longest_speech_free_window_s'),
                free_windows_ge_8s=pc.get('speech_free_windows_ge_8s'),
                method="lock SRT 89d61f96..a1c6b, 2291 cues, midpoint occupancy on a 0.5 s grid"),
            voice_reservation=dict(
                vo_reserved_overlap_s=pc.get('vo_reserved_overlap_s'),
                method="VOICE_OVER_REGISTRY v0.1.0 host_speech_segments"),
            orientation_load=dict(
                orientation_bearing_s=round(orient_s, 2),
                fraction_of_span=round(min(orient_s/dur, 1.0), 4),
                titles=sum(1 for x0,x1 in caps if ov(a0,a1,x0,x1)>0),
                map_elements=sum(1 for e in maps if ov(a0,a1,e['abs_in_s'],e['abs_out_s'])>0),
                graphic_overlays=sum(1 for e in gfx if ov(a0,a1,e['abs_in_s'],e['abs_out_s'])>0),
                method=("union of CAPTION_REGISTRY title spans, map elements and non-camera video "
                        "overlays, at 0.5 s. Counts what is on screen; asserts nothing about why."),
                note="relevant to VPD-001 P9 scope; see the P9 block below. No conclusion drawn here."),
            behaviour_states=[s['state'] for s in c.get('behaviour_states',[])] or None))

    withorient = [p for p in prints if p['orientation_load']['orientation_bearing_s'] > 0]
    doc = dict(
        artifact_id="BEHAVIORAL_FINGERPRINT", version="1.0.0",
        status="FOR EXECUTIVE REVIEW",
        authorized_by="Executive Disposition, 2026-08-22, EMB-CUE-03 Continuation item 7",
        source_class="MACHINE",
        instrument=dict(name="behavioral_fingerprint.py", grid_s=G),
        purpose=("preserve measured behavioural transitions as FINGERPRINTS. Explicitly NOT "
                 "arguments for boundary changes, per the authorising disposition."),
        conformance=["ER-001 no ranking, no recommendation, no preference",
                     "ER-003 mechanics precede meaning; significance is Executive",
                     "ESS-002 retains ownership of the CUE-03 boundary; nothing here infers movement"],
        view=dict(source="CONDUCTOR_SCORE.yaml v1.1.0 + Info.fcpxml + lock SRT",
                  scope="all 15 governed cue and silence regions",
                  filter={"has_resolved_boundaries": True},
                  coverage=dict(displayed=len(prints), total=len(cs['cues']))),
        missing_data_policy="propagate_unknown",
        p9_scope_measurement=dict(
            question=("VPD-001 P9 - 'music should support orientation rather than lead the scene' - "
                      "was ruled on 2026-08-22 to apply to EVERY Road Soul cue including CUE-03. "
                      "This block measures where orientation elements actually occur. It poses the "
                      "scope question; it does not answer it."),
            cues_with_orientation_elements=len(withorient),
            cues_without=len(prints)-len(withorient),
            cues_without_list=[p['cue'] for p in prints
                               if p['orientation_load']['orientation_bearing_s'] == 0],
            motion_family_note=("the two MOTION cues differ completely on this axis: CUE-03 is "
                                "64.4% orientation-bearing, CUE-07 is 0.0%. Both carry LEAD."),
            unresolved=("LEAD is specified as 'music carries the span'. P9 says music should support "
                        "orientation rather than lead. Where orientation load is 0.0% - CUE-07, "
                        "CUE-09a, CUE-09b, CUE-02b, CUE-05 - it is unstated what P9 requires, and "
                        "unstated whether P9 modifies LEAD. P8 holds that the behaviour vocabulary "
                        "is unchanged 'unless and until formally revised', so no state is altered "
                        "here. AWAITING_EXECUTIVE_INPUT.")),
        fingerprints=prints)
    with open(out_yaml,'w') as f:
        f.write("# BEHAVIORAL_FINGERPRINT - measurements, not arguments. Every row carries its method.\n")
        yaml.safe_dump(doc, f, sort_keys=False, width=110, allow_unicode=True)
    print(f"fingerprints: {len(prints)}   orientation-bearing: {len(withorient)}/{len(prints)}")
    print(f"{'cue':9}{'cuts/min':>10}{'mean_shot':>11}{'speech%':>9}{'longest_free':>14}{'orient%':>9}")
    for p in prints:
        print(f"{p['cue']:9}{p['cutting']['cuts_per_min']:10.2f}"
              f"{(p['cutting']['mean_shot_s'] or 0):11.2f}"
              f"{100*(p['speech']['coverage'] or 0):9.1f}"
              f"{(p['speech']['longest_free_window_s'] or 0):14.1f}"
              f"{100*p['orientation_load']['fraction_of_span']:9.1f}")

if __name__ == '__main__':
    main(*(sys.argv[1:] or ['ess/CONDUCTOR_SCORE.yaml','ess/CAPTION_REGISTRY.yaml',
        'prod/VOICE_PRIORITY_MAP.yaml','out/timeline_resolved.json',
        'prod/BEHAVIORAL_FINGERPRINT.yaml']))
