#!/usr/bin/env python3
"""MUSIC_OVERLAY_TIMELINE - every governed music region of the lock, in order,
with the transition at each boundary.

Task 2 of the Road Soul Phase 3 Transition work order (Chairman, 2026-08-22).

Measurement and declared derivation only. No ranking, no recommendation, no
artistic preference (ER-001). Every behaviour cited to an existing law (ER-003).
Custody: MACHINE (ER-003 A2.2).
"""
import yaml, json, sys

LOCK = 4846.625
def tc(s):
    h=int(s//3600); m=int(s%3600//60); x=s-h*3600-m*60
    return f"{h:02d}:{m:02d}:{x:06.3f}"

def main(conductor, vpm_path, out_yaml):
    cs  = yaml.safe_load(open(conductor))
    vpm = yaml.safe_load(open(vpm_path))
    percue = {c['cue']: c for c in vpm['per_cue']}

    regions = []
    for c in cs['cues']:
        b = c.get('boundaries') or {}
        if 'start_s' not in b: continue
        pc = percue.get(c['id'], {})
        is_sil = c.get('road_soul_family') in (None, 'NONE') and c['id'].startswith('SIL')
        regions.append(dict(
            id=c['id'], name=c.get('name'),
            region_class='MANDATORY_SILENCE' if is_sil else 'CUE',
            family=c.get('road_soul_family'),
            energy_target=c.get('energy_target'),
            reason_for_existing=c.get('reason_for_existing'),
            start_s=b['start_s'], end_s=b['end_s'], duration_s=round(b['end_s']-b['start_s'],3),
            start_tc=b.get('start_tc'), end_tc=b.get('end_tc'),
            behaviour_states=[s['state'] for s in c.get('behaviour_states',[])] or None,
            voice_condition=dict(
                speech_coverage=pc.get('speech_coverage'),
                speech_free_s=pc.get('speech_free_s'),
                longest_speech_free_window_s=pc.get('longest_speech_free_window_s'),
                vo_reserved_overlap_s=pc.get('vo_reserved_overlap_s'))))
    # conducted silences that are not cue entries (R46 carve-out)
    have = {r['id'] for r in regions}
    for z in cs['silence_law_encoding']:
        if z['id'] in have: continue
        regions.append(dict(id=z['id'], name=z.get('name'),
            region_class='FULL_OUT_WITHIN_CUE' if z.get('mode')=='FULL_OUT_WITHIN_CUE' else 'MANDATORY_SILENCE',
            family=None, energy_target=None, reason_for_existing=z.get('note'),
            start_s=z['start_s'], end_s=z['end_s'], duration_s=round(z['end_s']-z['start_s'],3),
            start_tc=z.get('start_tc'), end_tc=z.get('end_tc'),
            behaviour_states=z.get('states'), parent_cue=z.get('parent_cue'),
            voice_condition=None))
    regions.sort(key=lambda r: r['start_s'])

    # uncovered gaps between top-level regions
    top = [r for r in regions if r['region_class'] != 'FULL_OUT_WITHIN_CUE']
    gaps = []; prev = 0.0
    for r in top:
        if r['start_s'] - prev > 0.001:
            gaps.append(dict(id=f"GAP-{len(gaps)+1:02d}", region_class='UNCOVERED',
                start_s=round(prev,3), end_s=round(r['start_s'],3),
                start_tc=tc(prev), end_tc=tc(r['start_s']),
                duration_s=round(r['start_s']-prev,3),
                note="no governed cue region; no music behaviour is specified here"))
        prev = max(prev, r['end_s'])
    if LOCK - prev > 0.001:
        gaps.append(dict(id=f"GAP-{len(gaps)+1:02d}", region_class='UNCOVERED',
            start_s=round(prev,3), end_s=LOCK, start_tc=tc(prev), end_tc=tc(LOCK),
            duration_s=round(LOCK-prev,3),
            note="no governed cue region; no music behaviour is specified here"))

    # transitions between consecutive top-level regions
    seq = sorted(top + gaps, key=lambda r: r['start_s'])
    trans = []
    for a, b in zip(seq, seq[1:]):
        ac, bc = a['region_class'], b['region_class']
        if ac == 'CUE' and bc == 'MANDATORY_SILENCE':
            kind, law = 'HANDOFF_TO_SILENCE', "silence law: APPROACH reduces to floor before the boundary; nothing may tail across"
        elif ac == 'MANDATORY_SILENCE' and bc == 'CUE':
            kind, law = 'RETURN_FROM_SILENCE', "silence law: RETURN begins only after the last word of the zone"
        elif ac == 'CUE' and bc == 'CUE':
            kind, law = 'CUE_TO_CUE', "family signature: HANDOFF"
        elif bc == 'UNCOVERED' or ac == 'UNCOVERED':
            kind, law = 'TO_OR_FROM_UNCOVERED', "no governed behaviour: the boundary is unspecified"
        else:
            kind, law = 'OTHER', "not covered by an existing rule"
        trans.append(dict(at_s=round(b['start_s'],3), at_tc=tc(b['start_s']),
            from_region=a['id'], to_region=b['id'], transition=kind, governing_law=law,
            contiguous=abs(b['start_s']-a['end_s']) < 0.001,
            gap_s=round(b['start_s']-a['end_s'],3)))

    covered = sum(r['duration_s'] for r in top)
    doc = dict(
        artifact_id="MUSIC_OVERLAY_TIMELINE", version="1.0.0",
        status="FOR EXECUTIVE REVIEW",
        work_order="Road Soul Phase 3 Transition, task 2 (Chairman, 2026-08-22)",
        source_class="MACHINE",
        instrument=dict(name="music_overlay_timeline.py"),
        governed_artifacts_consumed=["CONDUCTOR_SCORE.yaml v1.1.0",
                                     "VOICE_PRIORITY_MAP.yaml v1.0.0", "CUE_SHEET v1.1"],
        conformance=["ER-001 no ranking, no recommendation, no preference",
                     "ER-003 mechanics precede meaning; significance is Executive",
                     "ER-003 A2.1 this is a DERIVED VIEW and declares its scope and coverage"],
        view=dict(source="CONDUCTOR_SCORE.yaml v1.1.0",
                  scope="all governed music regions and their boundary transitions",
                  filter={"region_class": ["CUE", "MANDATORY_SILENCE", "FULL_OUT_WITHIN_CUE", "UNCOVERED"]},
                  coverage=dict(displayed=len(seq), total=len(seq),
                                covered_s=round(covered,3), lock_s=LOCK,
                                uncovered_s=round(sum(g['duration_s'] for g in gaps),3))),
        missing_data_policy="propagate_unknown",
        counts_note="counts by region class; no aggregate score",
        counts=dict(cue_regions=sum(1 for r in top if r['region_class']=='CUE'),
                    mandatory_silence=sum(1 for r in top if r['region_class']=='MANDATORY_SILENCE'),
                    full_out_within_cue=sum(1 for r in regions if r['region_class']=='FULL_OUT_WITHIN_CUE'),
                    uncovered=len(gaps), transitions=len(trans)),
        regions=[r for r in regions],
        uncovered_regions=gaps,
        transitions=trans)
    with open(out_yaml,'w') as f:
        f.write("# MUSIC_OVERLAY_TIMELINE - derived view. Scope, filter and coverage declared per ER-003 A2.1.\n")
        yaml.safe_dump(doc, f, sort_keys=False, width=110, allow_unicode=True)
    print(f"regions {len(regions)}  uncovered {len(gaps)}  transitions {len(trans)}")
    print(f"covered {covered:.1f}s of {LOCK}  uncovered {sum(g['duration_s'] for g in gaps):.1f}s")
    for t in trans: print(f"  {t['at_tc']}  {t['from_region']:>9} -> {t['to_region']:<9} {t['transition']:22} gap={t['gap_s']:+.3f}")

if __name__ == '__main__':
    main(*(sys.argv[1:] or ['ess/CONDUCTOR_SCORE.yaml','prod/VOICE_PRIORITY_MAP.yaml',
                            'prod/MUSIC_OVERLAY_TIMELINE.yaml']))
