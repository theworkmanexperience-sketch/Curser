#!/usr/bin/env python3
"""
B-5 mechanical re-derivation of the 08-22 segment set onto the 08-24 lineage. VERSION 2.

v2 CORRECTIONS (authorized by the Chairman 2026-09-30, after the R9 evidence check):
  C1 IDENTITY OVER SPINE GAPS. v1 gave pseudo-tiles only to overlay picture that was a
     DIRECT child of a spine gap. Picture carried by a secondary storyline (or
     positive-lane clip) ANCHORED TO A PRECEDING CLIP and running on over a gap was
     invisible to v1, so identical footage was booked REMOVED on one side and ADDED on
     the other (08-22 S14 body vs 08-24 "A2"). v2 collects overlay picture from EVERY
     depth-0 element and clips it to the union of spine-gap spans. Where the spine has
     a clip, the spine clip remains the identity, exactly as in v1.
  C2 CAPTION CHECK AT SNAPPED BOUNDARIES. v1 compared caption lag with picture lag at
     every boundary. At a SNAPPED boundary equal lags say nothing about position, so
     v1 could report CORROBORATED while the speech landed far from the boundary (S14
     end). v2 reports NOT_EVALUATED_AT_SNAPPED_BOUNDARY there, and still prints the
     caption lag and the 08-24 position the captions project for the ORIGINAL 08-22
     boundary, as information.
  C3 SUB-FRAME OVERLAP IN THE CHAIN. Overlay items routinely overlap by less than one
     frame at storyline joins (08-22: 0.027 s at 3325.125-3325.152). With v1's 1 ms
     tolerance the order-preserving chain treated such neighbours as conflicting and
     discarded one, which would book identical footage as removed + added. v2 admits
     overlaps shorter than one frame (1/24 s) between successive chained pieces; the
     union arithmetic already counts overlap once. Because such an overlap is one
     08-22 instant shown twice in 08-24 (the items are laid end to end there), the
     ledger carries it explicitly as overlap_absorbed_s = retained_0824 - retained_0822,
     and the identity is D22 - removed + added + overlap_absorbed = D24, exactly.
Everything else is v1, unchanged.

Authorized under EO-2026-09-29 D-2. MACHINE PROPOSAL ONLY: this script derives
where each 08-22 segment boundary falls on the ED-003 Picture Lock. It does not
ratify a segment set, does not touch EPR-001, and binds no beat to anything.

METHOD (declared in full so it can be repeated or refuted)
  1. Tile each timeline: the non-transition depth-0 children of the sequence
     spine. These tile [0, sequence duration] contiguously (proved for 08-24 by
     the ETC validation, 201/201; for 08-22 by the 08-22 ETC, 191/191).
  2. Media identity per tile:
       asset-clip -> ('A', asset uid)                        [strong]
       clip       -> ('C', clip name, uid of first nested media ref)  [compound]
       gap        -> no identity (keyless; never matched)
  3. Retained material = the intersection, per identity, of each 08-22 tile's
     local interval [start, start+dur) with each 08-24 tile's. Every retained
     piece carries a lag = t24 - t22. Unretained 08-22 time is REMOVED; 08-24
     time covered by no retained piece is ADDED.
  4. Boundary mapping. A segment START at t maps through the piece containing
     [t, t+e); an END through the piece containing (t-e, t]. Outcome classes:
       MAPPED            exactly one piece                  -> t + lag
       AMBIGUOUS         >1 piece (source reused)           -> STOP for that row
       SNAPPED           t lies in REMOVED material. Declared rule: a START
                         snaps forward to the first retained 08-22 time >= t;
                         an END snaps back to the last retained time <= t;
                         the snapped point is then MAPPED. The snap distance is
                         reported. Never silent.
  5. Caption corroboration (CF-001 stream vs the 08-22 SRT). The two SRTs are
     different transcriptions of the same speech, so cue-level matching is
     unreliable. Instead the 08-22 caption words within 20 s inside each
     boundary are aligned against the WHOLE CF-001 word stream; only runs of
     >= 3 identical consecutive words count. The median word lag is compared
     with the picture lag (agreement <= 1.0 s). A match whose word lags do not
     cluster (IQR > 2.0 s) is INCOHERENT - common phrases matched at scattered
     places - and is neither corroboration nor divergence. Thresholds are
     constants.

stdlib only · read-only on every input · deterministic output.
"""
import argparse, difflib, hashlib, json, re, sys
import xml.etree.ElementTree as ET
from fractions import Fraction

E = Fraction(1, 1000)
FRAME = Fraction(1, 24)   # C3: chain tolerance for sub-frame overlap between successive pieces


def rt(v):
    if v is None:
        return None
    v = v.strip()[:-1] if v.strip().endswith('s') else v.strip()
    if '/' in v:
        n, d = v.split('/')
        return Fraction(int(n), int(d))
    return Fraction(v)


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def first_media_ref(node):
    for x in node.iter():
        if x is node:
            continue
        if x.get('ref'):
            return x.get('ref')
    return None


def tiles(path):
    root = ET.parse(path).getroot()
    uid = {a.get('id'): a.get('uid') for a in root.iter('asset')}
    seq = root.find('.//sequence')
    out, lanes, gaps, overlays = [], [], [], []
    for ch in seq.find('spine'):
        if ch.tag in ('transition',):
            continue
        if ch.tag not in ('asset-clip', 'clip', 'gap'):
            raise SystemExit(f'STOP: unexpected depth-0 tag {ch.tag}')
        off, dur = rt(ch.get('offset')), rt(ch.get('duration'))
        start = rt(ch.get('start')) or Fraction(0)
        if ch.tag == 'asset-clip':
            key = ('A', uid.get(ch.get('ref')))
        elif ch.tag == 'clip':
            key = ('C', ch.get('name'), uid.get(first_media_ref(ch)))
        else:
            key = None
        tm = ch.find('timeMap')
        tmsig = None if tm is None else ET.tostring(tm)
        out.append(dict(tag=ch.tag, name=ch.get('name') or '', key=key, t_in=off,
                        t_out=off + dur, src=start, tm=tmsig))
        if ch.tag == 'gap':
            gaps.append((off, off + dur))
        overlays.extend(overlay_items(ch, off, start, uid))
    # contiguity assertion
    for a, b in zip(out, out[1:]):
        if a['t_out'] != b['t_in']:
            raise SystemExit(f'STOP: tiles not contiguous at {float(a["t_out"])}')
    # C1: overlay picture from ANY depth-0 parent, clipped to spine-gap spans
    for el, t0, dur, src, tm in overlays:
        for g_in, g_out in gaps:
            lo, hi = max(t0, g_in), min(t0 + dur, g_out)
            if hi > lo:
                lanes.append(dict(tag='lane:' + el.tag, name=el.get('name') or '',
                                  key=media_key(el, uid), t_in=lo, t_out=hi,
                                  src=src + (lo - t0), tm=tm))
    return out, lanes, rt(seq.get('duration'))


def media_key(el, uid):
    if el.tag == 'asset-clip':
        return ('A', uid.get(el.get('ref')))
    return ('C', el.get('name'), uid.get(first_media_ref(el)))


def overlay_items(parent, p_in, p_start, uid):
    """C1: positive-lane asset-clips/clips and the items of positive-lane secondary
    storylines attached to a depth-0 element (gap, asset-clip or clip), with absolute
    start, duration, source start and retime signature. Not clipped here."""
    items = []
    for c in parent:
        lane = c.get('lane')
        if lane is None or int(lane) <= 0 or c.get('offset') is None:
            continue
        c_abs = p_in + (rt(c.get('offset')) - p_start)
        if c.tag in ('asset-clip', 'clip'):
            items.append((c, c_abs))
        elif c.tag == 'spine':
            for k in c:
                if k.tag in ('asset-clip', 'clip') and k.get('offset') is not None:
                    items.append((k, c_abs + rt(k.get('offset'))))
    out = []
    for el, t0 in items:
        tm = el.find('timeMap')
        out.append((el, t0, rt(el.get('duration')), rt(el.get('start')) or Fraction(0),
                    None if tm is None else ET.tostring(tm)))
    return out


def gap_lanes(gap, g_in, g_out, g_start, uid):   # v1 function, retained unused for reference
    """Picture carried ABOVE a spine gap: positive-lane asset-clips/clips, and the
    items of positive-lane secondary storylines. Each becomes a keyed pseudo-tile,
    clipped to the gap span. A gap has no media identity of its own; its lanes do."""
    items = []
    for c in gap:
        lane = c.get('lane')
        if lane is None or int(lane) <= 0 or c.get('offset') is None:
            continue
        c_abs = g_in + (rt(c.get('offset')) - g_start)
        if c.tag in ('asset-clip', 'clip'):
            items.append((c, c_abs))
        elif c.tag == 'spine':
            for k in c:
                if k.tag in ('asset-clip', 'clip') and k.get('offset') is not None:
                    items.append((k, c_abs + rt(k.get('offset'))))
    out = []
    for el, t0 in items:
        dur = rt(el.get('duration'))
        src = rt(el.get('start')) or Fraction(0)
        lo, hi = max(t0, g_in), min(t0 + dur, g_out)
        if hi <= lo:
            continue
        tm = el.find('timeMap')
        out.append(dict(tag='lane:' + el.tag, name=el.get('name') or '',
                        key=media_key(el, uid), t_in=lo, t_out=hi,
                        src=src + (lo - t0), tm=None if tm is None else ET.tostring(tm)))
    return out


def pieces(T22, T24):
    idx = {}
    for j, b in enumerate(T24):
        if b['key'] is not None:
            idx.setdefault(b['key'], []).append(j)
    ps = []
    for i, a in enumerate(T22):
        if a['key'] is None:
            continue
        for j in idx.get(a['key'], []):
            b = T24[j]
            lo = max(a['src'], b['src'])
            hi = min(a['src'] + a['t_out'] - a['t_in'], b['src'] + b['t_out'] - b['t_in'])
            if hi - lo <= 0:
                continue
            t22 = a['t_in'] + (lo - a['src'])
            t24 = b['t_in'] + (lo - b['src'])
            ps.append(dict(i22=i, i24=j, t22_in=t22, t22_out=t22 + (hi - lo),
                           t24_in=t24, lag=t24 - t22, len=hi - lo,
                           retime_differs=(a['tm'] != b['tm']), tag=a['tag'],
                           name=a['name']))
    ps.sort(key=lambda p: (p['t22_in'], p['t24_in']))
    return ps


def monotone_chain(allp):
    """Maximum-total-length chain of pieces strictly ordered in BOTH timelines.
    Source reuse produces cross-matches (the same media at two places); an
    order-preserving chain rejects them. Everything rejected is RETURNED and
    reported, so a genuine reorder would surface as excluded material rather
    than vanish. Ties broken by position, deterministically."""
    P = sorted(allp, key=lambda p: (p['t22_in'], p['t24_in'], p['len']))
    n = len(P)
    best = [p['len'] for p in P]
    prev = [-1] * n
    for j in range(n):
        for i in range(j):
            if (P[i]['t22_out'] <= P[j]['t22_in'] + FRAME and
                    P[i]['t24_in'] + P[i]['len'] <= P[j]['t24_in'] + FRAME and
                    P[j]['t22_in'] >= P[i]['t22_in'] + FRAME and
                    P[j]['t24_in'] >= P[i]['t24_in'] + FRAME and
                    best[i] + P[j]['len'] > best[j]):
                best[j] = best[i] + P[j]['len']
                prev[j] = i
    if not P:
        return [], []
    k = max(range(n), key=lambda x: (best[x], -x))
    chosen = set()
    while k != -1:
        chosen.add(k)
        k = prev[k]
    return [P[i] for i in sorted(chosen)], [P[i] for i in range(n) if i not in chosen]


def union_len(iv):
    iv = sorted(iv)
    tot, cur = Fraction(0), None
    for lo, hi in iv:
        if cur is None or lo > cur[1]:
            if cur:
                tot += cur[1] - cur[0]
            cur = [lo, hi]
        else:
            cur[1] = max(cur[1], hi)
    if cur:
        tot += cur[1] - cur[0]
    return tot


def containing(ps, t, side):
    if side == 'start':
        return [p for p in ps if p['t22_in'] <= t and t + E <= p['t22_out']]
    return [p for p in ps if p['t22_in'] <= t - E and t <= p['t22_out']]


def map_boundary(ps, t, side):
    hit = containing(ps, t, side)
    snapped_from = None
    if not hit:
        if side == 'start':
            cands = sorted(p['t22_in'] for p in ps if p['t22_in'] >= t)
            if not cands:
                return dict(status='UNMAPPABLE', t=None)
            snapped_from, t = t, cands[0]
        else:
            cands = sorted((p['t22_out'] for p in ps if p['t22_out'] <= t), reverse=True)
            if not cands:
                return dict(status='UNMAPPABLE', t=None)
            snapped_from, t = t, cands[0]
        hit = containing(ps, t, side)
    lags = sorted({p['lag'] for p in hit})
    if len(lags) != 1:
        return dict(status='AMBIGUOUS', t=None,
                    candidates=[float(t + l) for l in lags])
    p = hit[0]
    return dict(status='SNAPPED' if snapped_from is not None else 'MAPPED',
                t=t + lags[0], lag=lags[0],
                snap_s=None if snapped_from is None else float(t - snapped_from),
                via=f"{p['tag']} '{p['name'][:60]}'",
                retime_differs=p['retime_differs'])


# ---------------- captions ----------------
TS = re.compile(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)')


def srt(path):
    txt = open(path, encoding='utf-8-sig').read()
    cues = []
    for block in re.split(r'\n\s*\n', txt.strip()):
        lines = block.strip().splitlines()
        for k, ln in enumerate(lines):
            m = TS.search(ln)
            if m:
                g = list(map(int, m.groups()))
                a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                cues.append(dict(a=a, b=b, text=' '.join(lines[k + 1:])))
                break
    return cues


def norm(s):
    s = re.sub(r'<[^>]+>', ' ', s)          # CF-001 cues carry <font> markup
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', s.lower()).split())


CAP_WINDOW_S = 20.0    # caption words taken from this much of the segment, at the boundary
CAP_MIN_BLOCK = 3      # only runs of >= 3 consecutive identical words count as a match
CAP_MIN_WORDS = 6      # fewer matched words than this = insufficient caption evidence
CAP_AGREE_S = 1.0      # caption lag agrees with picture lag within this (transcripts re-time)
CAP_COHERENT_IQR_S = 2.0  # matched-word lags must cluster this tightly to count as ONE alignment


def words(cues):
    """Word stream with a per-word time, linearly interpolated inside its cue."""
    out = []
    for c in cues:
        w = norm(c['text']).split()
        for k, x in enumerate(w):
            out.append((x, c['a'] + (c['b'] - c['a']) * (k + 0.5) / len(w)))
    return out


def corroborate(w22, w24, t, side, picture_lag, _cache={}):
    """Independent check of a picture-derived boundary against the captions.
    08-22 caption words inside the segment within CAP_WINDOW_S of the boundary are
    aligned against the WHOLE CF-001 word stream (not a window around the picture
    prediction), so the caption lag is not conditioned on the lag it checks."""
    lo, hi = (t, t + CAP_WINDOW_S) if side == 'start' else (t - CAP_WINDOW_S, t)
    q = [(x, tt) for x, tt in w22 if lo <= tt < hi]
    if len(q) < CAP_MIN_WORDS:
        return dict(status='INSUFFICIENT_08-22_CAPTION_WORDS', words_in_window=len(q))
    key = id(w24)
    if key not in _cache:
        _cache[key] = [x for x, _ in w24]
    b = _cache[key]
    sm = difflib.SequenceMatcher(None, [x for x, _ in q], b, autojunk=False)
    lags = []
    for blk in sm.get_matching_blocks():
        if blk.size >= CAP_MIN_BLOCK:
            for k in range(blk.size):
                lags.append(w24[blk.b + k][1] - q[blk.a + k][1])
    if len(lags) < CAP_MIN_WORDS:
        return dict(status='INSUFFICIENT_CAPTION_MATCH', words_in_window=len(q),
                    words_matched=len(lags))
    lags.sort()
    med = lags[len(lags) // 2]
    spread = lags[(3 * len(lags)) // 4] - lags[len(lags) // 4]
    agree = picture_lag is not None and abs(med - picture_lag) <= CAP_AGREE_S
    status = ('INCOHERENT_CAPTION_MATCH' if spread > CAP_COHERENT_IQR_S
              else 'CORROBORATED' if agree else 'DIVERGENT')
    return dict(status=status,
                words_in_window=len(q), words_matched=len(lags),
                caption_lag_median=round(med, 3), caption_lag_iqr=round(spread, 3),
                picture_minus_caption_s=None if picture_lag is None else round(picture_lag - med, 3))


def cap_v2(res, m, t22):
    """C2: at a SNAPPED boundary the lag comparison is not evidence of position."""
    if m.get('status') != 'SNAPPED':
        return res
    out = dict(res, status='NOT_EVALUATED_AT_SNAPPED_BOUNDARY', v1_status=res['status'])
    if res.get('caption_lag_median') is not None and res.get('caption_lag_iqr', 99) <= CAP_COHERENT_IQR_S:
        out['caption_projected_08_24_s'] = round(t22 + res['caption_lag_median'], 3)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fcpxml-0822', required=True)
    ap.add_argument('--fcpxml-0824', required=True)
    ap.add_argument('--srt-0822', required=True)
    ap.add_argument('--srt-0824', required=True)
    ap.add_argument('--observations-0822', required=True)
    ap.add_argument('--expect', nargs=4, metavar=('F22', 'F24', 'S22', 'S24'), required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    ins = [a.fcpxml_0822, a.fcpxml_0824, a.srt_0822, a.srt_0824]
    got = [sha256(p) for p in ins]
    for p, g, e in zip(ins, got, a.expect):
        if g != e:
            sys.exit(f'STOP FAILED_SOURCE_IDENTITY {p}\n expected {e}\n measured {g}')

    T22, L22, D22 = tiles(a.fcpxml_0822)
    T24, L24, D24 = tiles(a.fcpxml_0824)
    allp = pieces(T22 + L22, T24 + L24)
    ps, excluded = monotone_chain(allp)

    # ---- whole-timeline delta ledger ----
    ret22 = union_len([(p['t22_in'], p['t22_out']) for p in ps])
    ret24 = union_len([(p['t24_in'], p['t24_in'] + p['len']) for p in ps])
    multi = sum(p['len'] for p in ps) - ret22   # 0 by construction of the chain
    removed = D22 - ret22
    added = D24 - ret24
    gaps22 = sum(t['t_out'] - t['t_in'] for t in T22 if t['key'] is None)
    gaps24 = sum(t['t_out'] - t['t_in'] for t in T24 if t['key'] is None)

    # lag blocks: consecutive retained pieces with equal lag
    blocks = []
    for p in ps:
        if blocks and blocks[-1]['lag'] == p['lag'] and abs(blocks[-1]['t22_out'] - p['t22_in']) <= E:
            blocks[-1]['t22_out'] = max(blocks[-1]['t22_out'], p['t22_out'])
            blocks[-1]['n'] += 1
        else:
            blocks.append(dict(t22_in=p['t22_in'], t22_out=p['t22_out'], lag=p['lag'], n=1))

    # removed / added intervals
    def complement(iv, D):
        iv = sorted(iv); out = []; cur = Fraction(0)
        for lo, hi in iv:
            if lo > cur:
                out.append((cur, lo))
            cur = max(cur, hi)
        if cur < D:
            out.append((cur, D))
        return out
    TL22, TL24 = T22 + L22, T24 + L24
    rem_iv = complement([(p['t22_in'], p['t22_out']) for p in ps], D22)
    add_iv = complement([(p['t24_in'], p['t24_in'] + p['len']) for p in ps], D24)

    def label(T, lo, hi):
        names = []
        for t in T:
            if t['t_in'] < hi and t['t_out'] > lo:
                names.append(f"{t['tag']}:{t['name'][:48]}" if t['key'] else 'gap')
        return names

    # ---- segments ----
    obs = json.load(open(a.observations_0822))
    c22, c24 = srt(a.srt_0822), srt(a.srt_0824)
    w22, w24 = words(c22), words(c24)
    rows = []
    for seg in obs['segments']:
        sid, s, e, name = seg[0], Fraction(seg[1]), Fraction(seg[2]), seg[3]
        ms, me = map_boundary(ps, s, 'start'), map_boundary(ps, e, 'end')
        # retained / removed content inside the segment
        inside = [(max(p['t22_in'], s), min(p['t22_out'], e)) for p in ps
                  if p['t22_in'] < e and p['t22_out'] > s]
        kept = union_len(inside)
        seg_lags = sorted({float(p['lag']) for p in ps if p['t22_in'] < e and p['t22_out'] > s})
        row = dict(segment=sid, label=name, old_start=float(s), old_end=float(e),
                   old_dur=float(e - s),
                   start=dict(ms, t=None if ms['t'] is None else round(float(ms['t']), 3),
                              lag=None if ms.get('lag') is None else round(float(ms['lag']), 3)),
                   end=dict(me, t=None if me['t'] is None else round(float(me['t']), 3),
                            lag=None if me.get('lag') is None else round(float(me['lag']), 3)),
                   retained_in_segment_s=round(float(kept), 3),
                   removed_in_segment_s=round(float((e - s) - kept), 3),
                   lags_inside_segment=[round(x, 3) for x in seg_lags],
                   caption_start=cap_v2(corroborate(w22, w24, float(s), 'start',
                                             None if ms.get('lag') is None else float(ms['lag'])), ms, float(s)),
                   caption_end=cap_v2(corroborate(w22, w24, float(e), 'end',
                                           None if me.get('lag') is None else float(me['lag'])), me, float(e)))
        if ms['t'] is not None and me['t'] is not None:
            row['new_start'] = round(float(ms['t']), 3)
            row['new_end'] = round(float(me['t']), 3)
            row['new_dur'] = round(float(me['t'] - ms['t']), 3)
            row['d_start'] = round(float(ms['t'] - s), 3)
            row['d_end'] = round(float(me['t'] - e), 3)
            row['d_dur'] = round(float((me['t'] - ms['t']) - (e - s)), 3)
        rows.append(row)

    out = dict(
        instrument='rederive_segments_v2.py', authority='EO-2026-09-29 D-2 (machine proposal only)',
        inputs=dict(zip(['fcpxml_0822', 'fcpxml_0824', 'srt_0822', 'srt_0824'],
                        [dict(path=p, sha256=g) for p, g in zip(ins, got)])),
        observations_0822=dict(path=a.observations_0822, sha256=sha256(a.observations_0822)),
        timelines=dict(d22=float(D22), d24=float(D24), delta=float(D24 - D22),
                       tiles22=len(T22), tiles24=len(T24), lane_tiles22=len(L22), lane_tiles24=len(L24),
                       caption_cues_0822=len(c22), caption_cues_0824=len(c24)),
        ledger=dict(retained_0822_s=round(float(ret22), 3), retained_0824_s=round(float(ret24), 3),
                    removed_s=round(float(removed), 3), added_s=round(float(added), 3),
                    reused_0822_time_s=round(float(multi), 3),
                    gaps_0822_s=round(float(gaps22), 3), gaps_0824_s=round(float(gaps24), 3),
                    overlap_absorbed_s=round(float(ret24 - ret22), 3),
                    identity_check=f'{float(D22)} - {float(removed):.3f} + {float(added):.3f} '
                                   f'+ {float(ret24 - ret22):.3f} = {float(D22 - removed + added + (ret24 - ret22)):.3f} vs {float(D24)}',
                    closes=(D22 - removed + added + (ret24 - ret22) == D24),
                    retime_differs_pieces=sum(1 for p in ps if p['retime_differs']),
                    pieces_total=len(allp), pieces_chained=len(ps),
                    pieces_excluded=len(excluded),
                    excluded_len_s=round(float(sum(p['len'] for p in excluded)), 3)),
        excluded_pieces=[dict(t22_in=round(float(p['t22_in']), 3), t24_in=round(float(p['t24_in']), 3),
                              len=round(float(p['len']), 3), lag=round(float(p['lag']), 3),
                              via=f"{p['tag']} '{p['name'][:48]}'") for p in excluded],
        lag_blocks=[dict(t22_in=round(float(b['t22_in']), 3), t22_out=round(float(b['t22_out']), 3),
                         lag=round(float(b['lag']), 3), pieces=b['n']) for b in blocks],
        removed=[dict(t22_in=round(float(lo), 3), t22_out=round(float(hi), 3),
                      dur=round(float(hi - lo), 3), elements=label(TL22, lo, hi)) for lo, hi in rem_iv],
        added=[dict(t24_in=round(float(lo), 3), t24_out=round(float(hi), 3),
                    dur=round(float(hi - lo), 3), elements=label(TL24, lo, hi)) for lo, hi in add_iv],
        segments=rows)
    with open(a.out, 'w') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out['timelines']), json.dumps(out['ledger'], indent=1), sep='\n')


if __name__ == '__main__':
    main()
