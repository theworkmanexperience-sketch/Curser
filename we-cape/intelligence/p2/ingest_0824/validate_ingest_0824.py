#!/usr/bin/env python3
"""
Validator for the 08-24 Decision C context ingestion (build_ingest_0824.py; authority EO-2026-09-29
Addendum D). WRITE-FREE with respect to the repository: it reads the working tree and rebuilds the
proposed files into a caller-supplied scratch directory (--scratch) to prove byte-determinism.

Runs no B-3 producer and decodes no media: ffprobe reads container/stream headers of the designated
MOV only; hashes are computed by reading bytes.

Usage: validate_ingest_0824.py --scratch DIR [--git-commit VALUE]
VALUE = the git_commit the working tree must carry: AWAITING_INGESTION (Commit A state, default) or the
full hash of Commit A (Commit B state). The rebuild uses the same VALUE.
Exit 0 = every check PASS; 1 = any FAIL.
"""
import argparse, hashlib, json, os, subprocess, sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import build_ingest_0824 as B  # noqa: E402  (constants only; main() is not called)

SUC_SHA = '211b594c362689e0ecf081e7a6a0ff125f60a51bf4344f9e27b6eaf55c103dbf'
ADD_D = 'docs/rulings/EO-2026-09-29_ADDENDUM_D_0824_Observation_Ingestion_Authority.md'
PROPOSED = [B.ETC_NEW, B.TL, B.STUB, B.CTX, B.MAN_SUP, B.MAN]
ALLOWED_MODIFIED = {B.CTX, B.MAN}
ALLOWED_NEW = set(PROPOSED) - ALLOWED_MODIFIED | {ADD_D, B.ING + 'build_ingest_0824.py',
                                                  B.ING + 'validate_ingest_0824.py'}
PROTECTED = ['intelligence/p2/registries/TIMELINE_REGISTRY.yaml',
             'intelligence/p2/registries/EMOTIONAL_PROGRESSION_REGISTRY.yaml',
             B.ETC_OLD, B.VAL, B.ESS + 'scripts/etc_extract.py', B.ESS + 'scripts/build_context.py',
             B.ESS + 'scripts/gen_artifacts_v2.py', B.ESS + 'scripts/runtime_guards.py',
             B.ESS + 'scripts/fcpx_resolve.py', B.ESS + 'context/AR2-0822.context.json']
EXPECT_CHANGED = {'regen_run_id', 'sha', 'proxy', 'etc', 'source_files', 'display_names', 'regeneration_scope',
                  'declared_segment_overlaps', 'governed_narrative_boundaries', 'source_manifest', 'measured',
                  'context_provenance'}

results = []


def check(cid, cond, detail):
    results.append((cid, bool(cond), detail))


def P(rel):
    return os.path.join(ROOT, rel)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def git(*a):
    return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, check=True).stdout


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--scratch', required=True)
    ap.add_argument('--git-commit', default='AWAITING_INGESTION'); a = ap.parse_args()
    gc = a.git_commit
    head = git('rev-parse', 'HEAD').decode().strip()
    anc = subprocess.run(['git', 'merge-base', '--is-ancestor', B.BASE, 'HEAD'], cwd=ROOT).returncode == 0
    check('V00', anc, f'basis {B.BASE[:7]} is an ancestor of HEAD {head[:7]}')

    # -- ETC: incumbent preserved, successor = incumbent + declared_lock only ----------------
    check('V01', sha(P(B.ETC_OLD)) == B.H[B.ETC_OLD], 'incumbent ETC 8c76a8cf... unchanged in place')
    check('V02', sha(P(B.ETC_NEW)) == SUC_SHA, f'successor ETC sha256 = {SUC_SHA}')
    old = git('show', f'{B.BASE}:./{B.ETC_OLD}').decode().split('\n'); new = open(P(B.ETC_NEW)).read().split('\n')
    diff = [(i + 1, x, y) for i, (x, y) in enumerate(zip(old, new)) if x != y]
    check('V03', len(old) == len(new) and diff == [(7, '  "declared_lock": null', '  "declared_lock": "01:18:09:11"')],
          f'ETC byte diff: exactly line 7 declared_lock null -> "01:18:09:11" ({len(diff)} line(s) differ)')
    oj, nj = json.loads('\n'.join(old)), json.load(open(P(B.ETC_NEW)))
    check('V04', oj['spine'] == nj['spine'] and oj['connected_elements'] == nj['connected_elements']
          and nj['source'] == B.LOCK and nj['source_sha256'] == B.H['fcpxml'],
          'spine, connected_elements identical; source = ED-003 lock path; source_sha256 = d82c2c3e')

    # -- context ----------------------------------------------------------------------------
    c = json.load(open(P(B.CTX))); oc = json.loads(git('show', f'{B.BASE}:./{B.CTX}'))
    changed = {k for k in set(c) | set(oc) if c.get(k) != oc.get(k)}
    check('V05', changed == EXPECT_CHANGED | ({'git_commit'} if gc != 'AWAITING_INGESTION' else set()), f'changed context keys = {sorted(changed)}')
    sm = c['source_manifest']
    want = {'mp4': B.H['mp4'], 'fcpxml': B.H['fcpxml'], 'srt': B.H['srt'], 'etc': SUC_SHA}
    check('V06', all(sm[k]['status'] == 'MEASURED' and sm[k]['sha256'] == v == c['sha'][k] for k, v in want.items()),
          'sha.{mp4,fcpxml,srt,etc} declared == measured == authorized; all MEASURED')
    check('V07', sm['mp4']['bytes'] == 29321383259 and sm['fcpxml']['bytes'] == 7264164
          and sm['srt']['bytes'] == 184470 and sm['etc']['bytes'] == os.path.getsize(P(B.ETC_NEW)),
          f"bytes mp4 {sm['mp4']['bytes']} fcpxml {sm['fcpxml']['bytes']} srt {sm['srt']['bytes']} etc {sm['etc']['bytes']}")
    check('V08', sm['mp4']['path'] == B.VOL + '/' + B.REL['mp4'] and sm['fcpxml']['path'] == B.LOCK
          and sm['srt']['path'] == B.VOL + '/' + B.REL['srt'] and sm['etc']['path'] == B.ETC_NEW,
          'source paths = Decision A MOV, ED-003 FCPXML, CF-001 SRT, successor ETC')
    for k in ('mp4', 'fcpxml', 'srt'):
        check('V09.' + k, sha(B.VOL + '/' + B.REL[k]) == B.H[k], f'{k} re-hashed from the volume = {B.H[k][:16]}...')
    m = c['measured']
    check('V10', m['etc_spine_n'] == c['etc']['spine'] == 201 and m['etc_connected_n'] == c['etc']['connected'] == 459,
          f"ETC spine {m['etc_spine_n']} / connected {m['etc_connected_n']}")
    check('V11', m['srt_cues'] == c['srt']['cues'] == 2034, f"SRT cues {m['srt_cues']}")
    check('V12', m['lock_tc_frames'] == '01:18:09:11' == m['etc_declared_lock_tc'],
          f"lock_tc_frames {m['lock_tc_frames']} == successor ETC declared_lock {m['etc_declared_lock_tc']}")
    check('V13', m['lock_tc_seconds'] == '01:18:09.500' and c['runtime_s'] == 4689.5
          and m['etc_declared_sequence_duration_s'] == 4689.5 and m['resolver']['spine_end_s'] == 4689.5,
          'lock time 01:18:09.500 = runtime 4689.5 = ETC duration = resolver spine end')
    check('V14', m['expected_out_of_range_n'] == 23 == m['resolver']['out_of_range_n'], 'expected out-of-range 23')
    check('V15', m['resolver']['etc_validation'] == 'VALIDATED' and m['resolver']['spine_comparison'] == '201 / 201'
          and m['etc_declared_source_sha256'] == B.H['fcpxml'], 'committed resolver evidence VALIDATED 201/201')
    tl = json.load(open(P(B.TL)))
    check('V16', tl['provenance']['source_sha256'] == sha(P(B.VAL)) == B.H[B.VAL],
          'resolver census traced to committed etc_validation_stdout.txt 2edf7916...')
    check('V17', c['regeneration_scope']['mode'] == 'CANONICAL_EDITORIAL_TIMELINE',
          'regeneration_scope.mode = CANONICAL_EDITORIAL_TIMELINE (G-12 mode check satisfied)')
    blob = json.dumps(c)
    check('V18', c['declared_segment_overlaps'] == [] and c['governed_narrative_boundaries'] == []
          and 'GNB-001' not in blob and 'TRANSITIONAL_OVERLAP' not in blob,
          'no S12/S13 overlap carried: declared_segment_overlaps [] and governed_narrative_boundaries []')
    check('V19', 'regen_run_id' not in c and c['run_id'] == 'auto' and c['git_commit'] == gc,
          f'regen_run_id absent (generator falls back to its own RUN_ID); run_id auto; git_commit = {gc}')
    if gc != 'AWAITING_INGESTION':
        a_ctx = json.loads(git('show', f'{gc}:./{B.CTX}'))
        a_parent = git('rev-parse', f'{gc}^').decode().strip()
        check('V19b', a_parent == B.BASE and a_ctx['git_commit'] == 'AWAITING_INGESTION' and 'regen_run_id' not in a_ctx
              and {k: v for k, v in a_ctx.items() if k != 'git_commit'} == {k: v for k, v in c.items() if k != 'git_commit'}
              and subprocess.run(['git', 'merge-base', '--is-ancestor', gc, 'HEAD'], cwd=ROOT).returncode == 0,
              f'git_commit {gc[:12]} = Commit A: child of {B.BASE[:7]}, ancestor of HEAD, carries the ingestion '
              'context (AWAITING_INGESTION); context differs from it only in git_commit')
    pv = c['proxy']
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                    'format=duration:stream=codec_type,codec_name,profile,width,height,r_frame_rate,duration,sample_rate,channels',
                                    '-of', 'json', B.VOL + '/' + B.REL['mp4']], capture_output=True, check=True).stdout)
    v = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]; au = [s for s in pr['streams'] if s['codec_type'] == 'audio'][0]
    check('V20', (v['codec_name'], v['profile'], v['width'], v['height'], v['r_frame_rate']) == ('h264', 'High', 3840, 2160, '24/1')
          and (au['codec_name'], au['sample_rate'], au['channels']) == ('aac', '48000', 2)
          and float(v['duration']) == pv['video_duration_s'] == 4689.5 and float(pr['format']['duration']) == pv['container_duration_s']
          and pv['resolution'] == '%dx%d' % (v['width'], v['height']) and pv['fps'] == 24,
          f"ffprobe: h264 High {v['width']}x{v['height']} {v['r_frame_rate']}, aac {au['sample_rate']} {au['channels']}ch, "
          f"video {v['duration']} s, container {pr['format']['duration']} s")

    # -- manifest supersession --------------------------------------------------------------
    om = git('show', f'{B.BASE}:./{B.MAN}')
    check('V21', open(P(B.MAN_SUP), 'rb').read() == om and sha(P(B.MAN_SUP)) == B.H[B.MAN],
          'v0.1.0 preserved byte-identical under superseded/ (a76ea18c...)')
    # v0.1.0 (87ef710) is not parseable YAML (block scalar inside a flow mapping, observed_unclassified
    # 'Music/' entry) - a pre-existing defect carried unedited, so the check is textual: the successor
    # minus its three insertions must equal v0.1.0 byte-for-byte, and each insertion must parse alone.
    nm = open(P(B.MAN)).read(); ot = om.decode()
    i0 = nm.index('# v0.2.0 (2026-10-01)'); i1 = nm.index('manifest_id: INGEST-0824')
    hdr = nm[i0:nm.index('# Prepared 2026-08-28', i0)]
    s0 = nm.index('supersedes: {'); s1 = nm.index('\n', s0) + 1
    d0 = nm.index('\n# ---------------------------------------------------------------------------\n# DESIGNATED')
    d1 = nm.index('\n# ---------------------------------------------------------------------------\n# PUBLIC DISTRIBUTION')
    rebuilt = ((nm[:s0] + nm[s1:d0] + nm[d1:]).replace(hdr, '', 1).replace('manifest_version: 0.2.0', 'manifest_version: 0.1.0', 1)
               .replace(B.MUSIC_NEW, B.MUSIC_OLD, 1))
    check('V22', rebuilt == ot and i0 < i1 and nm.count('manifest_version: 0.2.0') == 1 and B.MUSIC_NEW in nm
          and B.MUSIC_OLD not in nm,
          'successor = v0.1.0 + header note + version 0.2.0 + supersedes + designated_sources + Music/ repair (all else byte-identical)')
    try:
        y = yaml.safe_load(nm); parsed = True
    except yaml.YAMLError:
        y = yaml.safe_load(nm[s0:s1] + nm[d0:d1]); parsed = False
    check('V22b', parsed, 'successor v0.2.0 parses as YAML (whole document)')
    yo = yaml.safe_load(ot.replace(B.MUSIC_OLD, B.MUSIC_NEW, 1))  # v0.1.0 read with only the repair applied
    music = [e for e in (y.get('observed_unclassified') or []) if e.get('asset') == 'Final Data Source Files/Music/']
    check('V22c', parsed and {k: v for k, v in y.items() if k not in ('manifest_version', 'supersedes', 'designated_sources')}
          == {k: v for k, v in yo.items() if k != 'manifest_version'} and y['manifest_version'] == '0.2.0'
          and music == [{'asset': 'Final Data Source Files/Music/', 'note': (
              'a directory named Music inside the governed source folder. Contents NOT inspected. Bears on the '
              'copyright-exposure question that CUSTODY_ALERT_001 section 6 declined to answer without a validated '
              'instrument.')}],
          'semantic content = v0.1.0 + version/supersedes/designated_sources only; Music/ note value exact')
    check('V22d', [(r['id'], r['status']) for r in y['ingestion_preconditions']] == [
        ('IP-1', 'NOT_PRODUCED'), ('IP-2', 'NOT_VALIDATED'), ('IP-3', 'NOT_DESIGNATED'), ('IP-4', 'NOT_DECLARED'),
        ('IP-5', 'IN_PROGRESS'), ('IP-6', 'NOT_DERIVED'), ('IP-7', 'NOT_DERIVABLE_WITHOUT_IP-1'), ('IP-8', 'NOT_PERFORMED')],
          'IP-1..IP-8 statuses unchanged from v0.1.0')
    check('V22e', y['supersedes']['sha256'] == B.H[B.MAN] and y['supersedes']['preserved_at'] == B.MAN_SUP,
          'supersedes record -> v0.1.0 a76ea18c... at superseded/')
    ds = {d['role']: d for d in y['designated_sources']}
    check('V23', ds['fcpxml']['sha256'] == B.H['fcpxml'] and ds['srt']['sha256'] == B.H['srt'] and ds['mp4']['sha256'] == B.H['mp4']
          and ds['etc']['sha256'] == SUC_SHA and ds['etc']['supersedes']['sha256'] == B.H[B.ETC_OLD]
          and ds['context']['sha256'] == sha(P(B.CTX)) and str(ds['context']['git_commit']) == gc
          and ds['context']['basis_commit'] == B.BASE,
          'designated_sources hashes == measured files (context sha bound)')
    check('V24', 'state: PREPARED_NOT_EXECUTED\n' in nm and '  regeneration_performed: false\n' in nm
          and '  gen_artifacts_py: LOCKED\n' in nm,
          'manifest state/execution_state unchanged; regeneration_performed false')

    # -- ruling record ----------------------------------------------------------------------
    ad = open(P(ADD_D)).read()
    check('V25', all(s in ad for s in ('DECISION A — B-7 OBSERVATION SOURCE: APPROVED',
                                       'DECISION C — 08-24 INGESTION AND PINNING: APPROVED',
                                       'declared_lock: 01:18:09:11', 'step0_offset.py',
                                       'regeneration_scope.mode: CANONICAL_EDITORIAL_TIMELINE',
                                       'CHAIRMAN RULING — DECISION C FINAL SEMANTICS', '2. regen_run_id — OPTION (b)')),
          'Addendum D carries Decisions A-D, correction items 1-4 and final-semantics sections 1-5 verbatim')

    # -- scope: protected files untouched; only authorized paths changed -------------------
    check('V26', all(sha(P(f)) == hashlib.sha256(git('show', f'{B.BASE}:./{f}')).hexdigest() for f in PROTECTED),
          'TIMELINE v1.1.0, EPR-001 v1.15.0, incumbent ETC, resolver evidence, generator/guards/producers, 08-22 context unchanged')
    top = git('rev-parse', '--show-toplevel').decode().strip()
    st = [l.split('\t') for l in git('diff', '--name-status', B.BASE, '--', '.').decode().split('\n') if l]
    mod = {os.path.relpath(os.path.join(top, x[1]), ROOT) for x in st if x[0] == 'M'}
    added = {os.path.relpath(os.path.join(top, x[1]), ROOT) for x in st if x[0] == 'A'}
    other = [x for x in st if x[0] not in ('M', 'A')]
    unt = {x for x in git('ls-files', '--others', '--exclude-standard', '--', 'intelligence', 'docs').decode().split('\n') if x}
    mod_all = mod | added | unt
    check('V27', mod == ALLOWED_MODIFIED and (added | unt) == ALLOWED_NEW and not other,
          f'vs {B.BASE[:7]}: modified {sorted(mod)}; new {sorted(added | unt)}')
    check('V28', not any(x.endswith('observations.json') or x.lower().endswith(('.mov', '.mp4', '.m4v')) for x in mod_all)
          and not os.path.exists(P(B.ESS + 'context/AR2-0824.observations.json')),
          'no AR2-0824.observations.json, no media/proxy file created')

    # -- determinism -------------------------------------------------------------------------
    for run in ('d1', 'd2'):
        o = os.path.join(a.scratch, run)
        subprocess.run([sys.executable, os.path.join(HERE, 'build_ingest_0824.py'), '--out-root', o, '--git-commit', gc],
                       check=True, capture_output=True)
        check('V29.' + run, all(open(os.path.join(o, f), 'rb').read() == open(P(f), 'rb').read() for f in PROPOSED),
              f'scratch rebuild {run} byte-identical to the working tree (6 files)')

    fails = [r for r in results if not r[1]]
    for cid, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'} {cid:7} {d}")
    print(f'{len(results) - len(fails)}/{len(results)} PASS')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
