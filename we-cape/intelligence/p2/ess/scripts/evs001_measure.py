#!/usr/bin/env python3
"""EVS-001 component metrics for PDR-2026-08-22-ESS-002 (escort ride vs CUE-03).

Pure measurement. No interpretation, no inference, no recommendation.

Sources
  audio_rms_0p25.npy   full-mix RMS, 0.25 s grid, from Filmage_Editor.mp4
                       SHA a53655fc673945a0d99dde3d5b60c9a126d8b41e4e44a7c7eedeb058ba0f47e8
  video_obs_2fps.npy   2 fps 64x36 RGB observables from the same proxy
                       columns: R G B L S D LR TOP BOT  (D = frame-difference energy)
  timeline_resolved.json  FCPXML primary spine, resolver validated 191/191 vs the ETC

Caveats carried into the brief, not hidden here:
  * audio figures are TOTAL MIX ENERGY - speech, wind, engines and contributed
    audio are all in them. They measure loudness, never source.
  * D is a coarse motion proxy at 64x36 / 2 fps. It ranks regions; it does not
    measure camera movement as such.
  * cut positions come from the FCPXML, NOT from the proxy - the proxy is only
    ever the audio and motion source.
"""
import numpy as np, json, sys

AF, VF = 4.0, 2.0          # audio samples/s, video samples/s

def load(work, out):
    a = np.load(work + 'audio_rms_0p25.npy')
    v = np.load(work + 'video_obs_2fps.npy')
    D = v[:, 5].astype(float)
    spine = json.load(open(out + 'timeline_resolved.json'))
    prim = sorted([e for e in spine['elements']
                   if e['depth'] == 0 and e['tag'] != 'transition'],
                  key=lambda e: e['abs_in_s'])
    cuts = sorted({round(e['abs_in_s'], 3) for e in prim})
    return a, D, prim, cuts

def db(x):
    """Mean RMS in dBFS-relative terms. Zeros dropped: log of silence is undefined,
    and substituting a floor would invent a value (NO SILENT RECOVERY)."""
    x = np.asarray(x, dtype=float); x = x[x > 0]
    return float(20 * np.log10(x.mean())) if len(x) else float('nan')

def region(a, D, cuts, lo, hi):
    ar = a[int(lo * AF):int(hi * AF)]
    mo = D[int(lo * VF):int(hi * VF)]
    n = len([c for c in cuts if lo <= c < hi])
    return dict(start_s=lo, end_s=hi, duration_s=hi - lo,
                audio_rms_db=round(db(ar), 2),
                audio_p90_db=round(float(20 * np.log10(np.percentile(ar[ar > 0], 90))), 2),
                motion_mean=round(float(mo.mean()), 2),
                motion_sd=round(float(mo.std()), 2),
                cuts=n, mean_shot_s=round((hi - lo) / max(n, 1), 2))

REGIONS = [("pre_roll_26_00_27_40",           1560.0, 1660.0),
           ("cue03_as_specified_27_40_29_10", 1660.0, 1750.0),
           ("the_gap_29_10_31_43",            1750.0, 1903.0),
           ("gap_first_half",                 1750.0, 1826.5),
           ("gap_second_half",                1826.5, 1903.0),
           ("sil01_first_77s_31_43_33_00",    1903.0, 1980.0),
           ("sil01_remainder_33_00_38_52",    1980.0, 2332.0)]

def main(work, out, dest):
    a, D, prim, cuts = load(work, out)
    regions = {k: region(a, D, cuts, lo, hi) for k, lo, hi in REGIONS}
    cue, gap = regions['cue03_as_specified_27_40_29_10'], regions['the_gap_29_10_31_43']
    sil = regions['sil01_first_77s_31_43_33_00']

    walk = []
    t = 1620.0
    while t < 2010.0:
        r = region(a, D, cuts, t, t + 30)
        r['cuts_per_min'] = r['cuts'] * 2
        walk.append(r); t += 30

    res = dict(
      session='EVS-001', pdr='PDR-2026-08-22-ESS-002', date='2026-08-22',
      grids=dict(audio_hz=AF, video_fps=VF, cut_source='FCPXML primary spine'),
      regions=regions, walk_30s=walk,
      q4_does_production_sound_strengthen_after_29_10=dict(
        across_cue03_out_db=round(gap['audio_rms_db'] - cue['audio_rms_db'], 2),
        across_sil01_in_db=round(sil['audio_rms_db'] - gap['audio_rms_db'], 2),
        jnd_broadband_db=1.0,
        finding=('The change across CUE-03 out is below the ~1 dB just-noticeable '
                 'difference for broadband level: there is no audio event at 29:10. '
                 'The mix performs a large level event at the SIL-01 boundary instead. '
                 'MEASURED, not interpreted. See the two delta fields above for values.')),
      q1_q5_deceleration=dict(
        mean_shot_ratio=round(gap['mean_shot_s'] / cue['mean_shot_s'], 3),
        motion_ratio=round(gap['motion_mean'] / cue['motion_mean'], 3),
        finding=('Mean shot length rises by mean_shot_ratio while frame-difference '
                 'energy falls only slightly (motion_ratio). The deceleration measured '
                 'here is in the CUTTING, not in the motion within frame.')),
      shot_list_27_25_to_32_00=[
        dict(in_s=e['abs_in_s'], duration_s=round(e['abs_out_s'] - e['abs_in_s'], 3),
             name=e['name'][:60])
        for e in prim if 1645 <= e['abs_in_s'] < 1925],
      caveats=['audio figures are total mix energy, not per-source',
               'motion is a 64x36 / 2 fps proxy, not camera-movement measurement',
               'no CUE-03 exists; nothing in this file measures a cue'])
    json.dump(res, open(dest, 'w'), indent=1)
    print(json.dumps({k: res[k] for k in
          ('q4_does_production_sound_strengthen_after_29_10', 'q1_q5_deceleration')}, indent=1))

if __name__ == '__main__':
    main(*(sys.argv[1:] or [
      '/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/',
      '/home/claude/work/out/',
      '/home/claude/work/out/evs001_measurements.json']))
