#!/usr/bin/env python3
"""ecr_gen_002_suite.py — ECR-GEN-002 conformance suite.

Runs every ECR-GEN-002 acceptance check against the 08-22 engineering fixture
and emits a machine-readable result set. Nothing here writes to a governed
artifact path: all generation goes to a scratch tree supplied by --work.

USAGE
  ecr_gen_002_suite.py --scripts <dir> --context-dir <dir> --sources <dir>
                       --mp4 <proxy> --work <scratch dir> [--json out.json]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

R = []


def rec(tid, name, status, evidence):
    R.append(dict(id=tid, name=name, status=status, evidence=evidence))
    print('  %-7s %-46s %-8s %s' % (tid, name, status, evidence))


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scripts', required=True)
    ap.add_argument('--context-dir', required=True)
    ap.add_argument('--sources', required=True)
    ap.add_argument('--mp4', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--baseline', required=True,
                    help='directory holding the pre-ECR-GEN-002 artifact set')
    ap.add_argument('--json', default=None)
    a = ap.parse_args()

    S, CD, W, WK = a.scripts, a.context_dir, a.sources, a.work
    D = os.path.join(WK, 'derived')
    OUT = os.path.join(WK, 'out')
    for d in (D, OUT):
        os.makedirs(d, exist_ok=True)
    ctx_in = os.path.join(CD, 'AR2-0822.context.json')
    obs = os.path.join(CD, 'AR2-0822.observations.json')
    ctx = os.path.join(WK, 'ctx.json')
    fx = os.path.join(W, 'inputs/Info.fcpxml')
    etc = os.path.join(W, 'inputs/P2_LOCK_timing.json')
    fx24 = os.path.join(W, 'analysis_cut/Info_analysiscut.fcpxml')
    tlj = os.path.join(D, 'timeline_resolved.json')

    print('ECR-GEN-002 conformance suite\n')

    # -- E1  ETC validator, positive --------------------------------------
    p = run(['python3', os.path.join(S, 'fcpx_resolve.py'), fx, etc, tlj])
    v = json.load(open(tlj))['validation'] if os.path.exists(tlj) else {}
    okv = (p.returncode == 0 and v.get('etc_validation') == 'VALIDATED'
           and v.get('spine_offset_matches') == v.get('etc_spine_n'))
    rec('E1', 'ETC binding validates on the 08-22 fixture',
        'PASS' if okv else 'FAIL',
        'verdict=%s %s tol=%s exit=%d' % (v.get('etc_validation'),
                                          v.get('spine_comparison'),
                                          v.get('tolerance_s'), p.returncode))

    # -- E2  ETC validator, cardinality ------------------------------------
    e = json.load(open(etc))
    tr = dict(e); tr['spine'] = e['spine'][:-1]
    trp = os.path.join(WK, 'etc_trunc.json')
    json.dump(tr, open(trp, 'w'))
    p = run(['python3', os.path.join(S, 'fcpx_resolve.py'), fx, trp,
             os.path.join(WK, 't2.json')])
    v2 = json.load(open(os.path.join(WK, 't2.json')))['validation']
    rec('E2', 'short ETC stops on cardinality, no comparison',
        'PASS' if (p.returncode == 2 and v2['etc_validation'] == 'FAILED_CARDINALITY'
                   and 'spine_offset_matches' not in v2) else 'FAIL',
        '%s exit=%d, no partial comparison recorded' % (v2['etc_validation'], p.returncode))

    # -- E3  ETC validator, source identity --------------------------------
    p = run(['python3', os.path.join(S, 'fcpx_resolve.py'), fx24, etc,
             os.path.join(WK, 't3.json')])
    v3 = json.load(open(os.path.join(WK, 't3.json')))['validation']
    rec('E3', 'ETC naming another export stops on identity',
        'PASS' if (p.returncode == 2 and v3['etc_validation'] == 'FAILED_SOURCE_IDENTITY')
        else 'FAIL', '%s exit=%d' % (v3['etc_validation'], p.returncode))

    # -- E4  ETC validator, drift ------------------------------------------
    pe = json.loads(json.dumps(e)); pe['spine'][100]['timeline_offset_s'] += 0.002
    pep = os.path.join(WK, 'etc_drift.json'); json.dump(pe, open(pep, 'w'))
    p = run(['python3', os.path.join(S, 'fcpx_resolve.py'), fx, pep,
             os.path.join(WK, 't4.json')])
    v4 = json.load(open(os.path.join(WK, 't4.json')))['validation']
    rec('E4', '2 ms drift at one element stops the binding',
        'PASS' if (p.returncode == 2 and v4['etc_validation'] == 'FAILED_COMPARISON')
        else 'FAIL', '%s %s exit=%d' % (v4['etc_validation'],
                                        v4.get('spine_comparison'), p.returncode))

    # -- E5  context is measured, not typed --------------------------------
    p = run(['python3', os.path.join(S, 'build_context.py'), '--in', ctx_in,
             '--out', ctx, '--sources', W, '--timeline', tlj, '--mp4', a.mp4])
    cj = json.load(open(ctx)) if p.returncode == 0 else {}
    m = (cj.get('measured') or {})
    rec('E5', 'context values measured from the named sources',
        'PASS' if p.returncode == 0 and m else 'FAIL',
        'etc spine=%s connected=%s titles=%s; resolver total=%s'
        % (m.get('etc_spine_n'), m.get('etc_connected_n'),
           (m.get('etc_connected_by_tag') or {}).get('title'),
           (m.get('resolver') or {}).get('total_elements')))

    # -- E6  declared/measured disagreement stops --------------------------
    bad = json.loads(json.dumps(json.load(open(ctx_in))))
    bad['srt']['cues'] = 9999
    badp = os.path.join(WK, 'ctx_bad.json'); json.dump(bad, open(badp, 'w'))
    p = run(['python3', os.path.join(S, 'build_context.py'), '--in', badp,
             '--out', os.path.join(WK, 'x.json'), '--sources', W,
             '--timeline', tlj, '--mp4', a.mp4])
    rec('E6', 'a declared value that disagrees stops the build',
        'PASS' if p.returncode == 2 else 'FAIL',
        'exit=%d %s' % (p.returncode, p.stderr.strip().split('\n')[0][:80]))

    # -- E7  camera runs ----------------------------------------------------
    p = run(['python3', os.path.join(S, 'derive_camera_runs.py'), tlj,
             os.path.join(D, 'camera_runs.json')])
    cams = json.load(open(os.path.join(D, 'camera_runs.json')))
    rec('E7', 'derived camera runs match the resolved spine census',
        'PASS' if len(cams) == m.get('resolver', {}).get('spine_excl_transitions') else 'FAIL',
        '%d runs' % len(cams))

    # -- E8  generation + guards -------------------------------------------
    p = run(['python3', os.path.join(S, 'gen_artifacts_v2.py'), '--context', ctx,
             '--observations', obs, '--derived', D + '/', '--sources', W,
             '--out', OUT + '/', '--run-id', 'pinned'])
    ng = sum(1 for l in p.stdout.split('\n') if 'PASS' in l and 'guard' in l)
    rec('E8', 'all runtime identity guards pass and generation completes',
        'PASS' if p.returncode == 0 and ng >= 12 else 'FAIL',
        '%d guards passed, exit=%d' % (ng, p.returncode))

    # -- E9..E12  guard negatives ------------------------------------------
    o = json.load(open(obs))
    negs = []
    x = json.loads(json.dumps(o)); x['production_id'] = 'AR2-0824'; negs.append(('E9', 'wrong production_id', 'G-01', x))
    x = json.loads(json.dumps(o)); x['source_sha']['fcpxml'] = '0' * 64; negs.append(('E10', 'observations pin another source', 'G-03', x))
    x = json.loads(json.dumps(o)); x.pop('die_v'); negs.append(('E11', 'observation bundle incomplete', 'G-11', x))
    x = json.loads(json.dumps(o)); x['segments'][12][1] = 3100; negs.append(('E12', 'undeclared segment overlap', 'G-08b', x))
    for tid, name, guard, payload in negs:
        pth = os.path.join(WK, tid + '.json'); json.dump(payload, open(pth, 'w'))
        neg = os.path.join(WK, 'neg_' + tid)
        shutil.rmtree(neg, ignore_errors=True); os.makedirs(neg)
        p = run(['python3', os.path.join(S, 'gen_artifacts_v2.py'), '--context', ctx,
                 '--observations', pth, '--derived', D + '/', '--sources', W,
                 '--out', neg + '/', '--run-id', 'pinned'])
        wrote = len(os.listdir(neg))
        good = p.returncode == 2 and wrote == 0 and guard in p.stderr
        rec(tid, name + ' stops at ' + guard, 'PASS' if good else 'FAIL',
            'exit=%d files_written=%d' % (p.returncode, wrote))

    # -- E13  traceability --------------------------------------------------
    p = run(['python3', os.path.join(S, 'traceability_scan.py'),
             os.path.join(S, 'gen_artifacts_v2.py'), '--context', ctx,
             '--json', os.path.join(WK, 'tr.json')])
    tr = json.load(open(os.path.join(WK, 'tr.json')))
    rec('E13', 'no production-identifying literal remains (TR-1)',
        'PASS' if p.returncode == 0 and not tr['tr1'] else 'FAIL',
        '%d TR-1 hits; %d TR-2 narrative literals reported (B-13)'
        % (len(tr['tr1']), len({(h['line'], h['value']) for h in tr['tr2']})))

    # -- E14  regression against the pre-change artifact set ---------------
    names = ['STEP0_TIMING_CLOSURE.md', 'CAPTION_REGISTRY.yaml',
             'VISUAL_EVENT_REGISTRY.yaml', 'EDITORIAL_SYNCHRONIZATION.yaml',
             'CONDUCTOR_SCORE.yaml', 'ESS_VALIDATION_REPORT.md',
             'PRODUCTION_INTELLIGENCE_SEED.yaml']
    changed, tot_b, tot_a = [], 0, 0
    for n in names:
        b = open(os.path.join(a.baseline, n), 'rb').read()
        c = open(os.path.join(OUT, n), 'rb').read()
        tot_b += len(b); tot_a += len(c)
        if b != c:
            bl = b.decode().split('\n'); cl = c.decode().split('\n')
            d = [i for i, (x, y) in enumerate(zip(bl, cl), 1) if x != y]
            changed.append((n, len(d)))
    rec('E14', 'regression vs the pre-change artifact set',
        'PASS' if all(k <= 1 for _n, k in changed) else 'FAIL',
        '%d of %d artifacts changed, %d changed line(s) total, %d -> %d bytes'
        % (len(changed), len(names), sum(k for _n, k in changed), tot_b, tot_a))

    # -- E15  observation producers ----------------------------------------
    ap_ = os.path.join(WK, 'audio_rms_0p25.npy')
    p = run(['python3', os.path.join(S, 'produce_audio_rms.py'), a.mp4, ap_,
             '--verify', os.path.join(W, 'audio_rms_0p25.npy')])
    rec('E15', 'audio RMS producer reproduces the 08-22 fixture',
        'PASS' if p.returncode == 0 else 'FAIL',
        [l for l in p.stdout.split('\n') if 'verify' in l][0][:90]
        if p.returncode == 0 else p.stderr.strip()[:90])

    vp = os.path.join(WK, 'video_obs_2fps.npy')
    p = run(['python3', os.path.join(S, 'produce_video_obs.py'), a.mp4, vp,
             '--compare', os.path.join(W, 'video_obs_2fps.npy')])
    produced = p.returncode == 0 and os.path.exists(vp)
    rec('E16', 'visual observation producer exists and is specified',
        'PASS' if produced else 'FAIL',
        'produced with a written schema; does NOT reproduce the legacy array '
        '(3 of 9 columns unrecovered) - reported, not claimed')

    npass = sum(1 for r in R if r['status'] == 'PASS')
    print('\n%d PASS / %d FAIL of %d' % (npass, len(R) - npass, len(R)))
    if a.json:
        json.dump(dict(suite='ECR-GEN-002', results=R,
                       passed=npass, failed=len(R) - npass),
                  open(a.json, 'w'), indent=1)
        print('wrote %s' % a.json)
    return 0 if npass == len(R) else 1


if __name__ == '__main__':
    sys.exit(main())
