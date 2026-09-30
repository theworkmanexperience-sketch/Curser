#!/usr/bin/env python3
"""Turns rederivation.json into the packet's mapping table and 157.125 s
reconciliation. Pure arithmetic over the machine product; no new measurement.
Emits mapping_table.csv, mapping_table.md, reconciliation.json.

CATEGORY RULES (mechanical, declared):
  MICRO_RETRIM        removed/added interval shorter than 0.2 s (< 5 frames)
  GAP_REPOSITIONED    a keyless removed gap and a keyless added gap of equal
                      duration where added.t24_in == removed.t22_in + the lag of
                      the retained block immediately before it (net 0)
  REMOVED_MATERIAL    any other 08-22 interval with no 08-24 counterpart
  ADDED_MATERIAL      any other 08-24 interval with no 08-22 counterpart
Every interval is then located: inside a segment (by 08-22 span for removed,
by re-derived 08-24 span for added) or INTER_SEGMENT."""
import csv, json, sys

d = json.load(open(sys.argv[1]))
out = sys.argv[2]
EPS = 0.0015


def tc(t):
    fr = round(t * 24)
    return f"{fr // 86400:02d}:{fr // 1440 % 60:02d}:{fr // 24 % 60:02d}:{fr % 24:02d}"


def blk_lag_before(t22):
    prev = [b for b in d['lag_blocks'] if b['t22_out'] <= t22 + EPS]
    return prev[-1]['lag'] if prev else 0.0


def seg_at(lo, hi, which):
    hits = []
    for r in d['segments']:
        a, b = (r['old_start'], r['old_end']) if which == 'old' else (r.get('new_start'), r.get('new_end'))
        if a is None:
            continue
        ov = min(hi, b) - max(lo, a)
        if ov > EPS:
            hits.append((r['segment'], round(ov, 3)))
    return hits


rem, add = [dict(x) for x in d['removed']], [dict(x) for x in d['added']]
for x in rem:
    x['category'] = 'MICRO_RETRIM' if x['dur'] < 0.2 else 'REMOVED_MATERIAL'
for x in add:
    x['category'] = 'MICRO_RETRIM' if x['dur'] < 0.2 else 'ADDED_MATERIAL'
for x in rem:
    if x['category'] == 'REMOVED_MATERIAL' and x['elements'] == ['gap']:
        exp = round(x['t22_in'] + blk_lag_before(x['t22_in']), 3)
        for y in add:
            if (y['category'] == 'ADDED_MATERIAL' and y['elements'] == ['gap']
                    and abs(y['dur'] - x['dur']) <= EPS and abs(y['t24_in'] - exp) <= EPS):
                x['category'] = y['category'] = 'GAP_REPOSITIONED'
                x['pair'] = y['t24_in']; y['pair'] = x['t22_in']
for x in rem:
    x['segments'] = seg_at(x['t22_in'], x['t22_out'], 'old')
for x in add:
    x['segments'] = seg_at(x['t24_in'], x['t24_out'], 'new')

# ---- per-segment decomposition: d_dur must equal added-in-new-span - removed-in-old-span
rows, unexplained = [], []
for r in d['segments']:
    rin = sum(ov for x in rem for s, ov in x['segments'] if s == r['segment'])
    ain = sum(ov for x in add for s, ov in x['segments'] if s == r['segment'])
    resid = round(r['d_dur'] - (ain - rin), 3)
    if abs(resid) > 0.002:
        unexplained.append((r['segment'], resid))
    cs, ce = r['caption_start'], r['caption_end']
    rows.append(dict(
        segment=r['segment'], label=r['label'], in_EO_scope=r['segment'] != 'S19',
        old_start=r['old_start'], old_end=r['old_end'], old_dur=r['old_dur'],
        old_start_tc=tc(r['old_start']), old_end_tc=tc(r['old_end']),
        new_start=r['new_start'], new_end=r['new_end'], new_dur=r['new_dur'],
        new_start_tc=tc(r['new_start']), new_end_tc=tc(r['new_end']),
        d_start=r['d_start'], d_end=r['d_end'], d_dur=r['d_dur'],
        start_status=r['start']['status'], start_snap_s=r['start'].get('snap_s'),
        end_status=r['end']['status'], end_snap_s=r['end'].get('snap_s'),
        removed_in_segment=round(rin, 3), added_in_segment=round(ain, 3), residual=resid,
        caption_start=cs['status'], caption_start_lag=cs.get('caption_lag_median'),
        caption_end=ce['status'], caption_end_lag=ce.get('caption_lag_median')))

tot = lambda L, c=None: round(sum(x['dur'] for x in L if c is None or x['category'] == c), 3)
recon = dict(
    lock_0822_s=d['timelines']['d22'], lock_0824_s=d['timelines']['d24'],
    delta_s=round(d['timelines']['d24'] - d['timelines']['d22'], 3),
    removed_total_s=tot(rem), added_total_s=tot(add),
    by_category=dict(
        removed=dict(MICRO_RETRIM=tot(rem, 'MICRO_RETRIM'), GAP_REPOSITIONED=tot(rem, 'GAP_REPOSITIONED'),
                     REMOVED_MATERIAL=tot(rem, 'REMOVED_MATERIAL')),
        added=dict(MICRO_RETRIM=tot(add, 'MICRO_RETRIM'), GAP_REPOSITIONED=tot(add, 'GAP_REPOSITIONED'),
                   ADDED_MATERIAL=tot(add, 'ADDED_MATERIAL'))),
    closes=abs(d['timelines']['d22'] - tot(rem) + tot(add) - d['timelines']['d24']) <= 0.002,
    removed=rem, added=add, unexplained_segment_deltas=unexplained)
json.dump(recon, open(f'{out}/reconciliation.json', 'w'), indent=1)

with open(f'{out}/mapping_table.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

md = ['| Seg | label | 08-22 in → out (s) | 08-24 in → out (s) | Δin | Δout | Δdur | boundary status | removed in seg | added in seg | residual | captions (start / end) |',
      '|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---|']
for r in rows:
    st = r['start_status'] + (f" (snap +{r['start_snap_s']:.3f})" if r['start_snap_s'] else '')
    en = r['end_status'] + (f" (snap {r['end_snap_s']:.3f})" if r['end_snap_s'] else '')
    md.append(f"| {r['segment']}{'' if r['in_EO_scope'] else ' †'} | {r['label']} | {r['old_start']:.3f} → {r['old_end']:.3f} "
              f"| {r['new_start']:.3f} → {r['new_end']:.3f} | {r['d_start']:+.3f} | {r['d_end']:+.3f} | {r['d_dur']:+.3f} "
              f"| {st} / {en} | {r['removed_in_segment']:.3f} | {r['added_in_segment']:.3f} | {r['residual']:.3f} "
              f"| {r['caption_start']} / {r['caption_end']} |")
open(f'{out}/mapping_table.md', 'w').write('\n'.join(md) + '\n')
print(json.dumps({k: recon[k] for k in ('delta_s', 'removed_total_s', 'added_total_s', 'by_category', 'closes', 'unexplained_segment_deltas')}, indent=1))
