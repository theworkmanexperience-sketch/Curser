#!/usr/bin/env python3
"""
08-24 Decision C context ingestion. Authority: EO-2026-09-29 Addendum D (CHAIRMAN RULING - 08-24
OBSERVATION / INGESTION AUTHORITY, Decisions A and C, as corrected by CHAIRMAN CORRECTION -
DECISION C / 08-24 INGESTION, 2026-10-01, and by CHAIRMAN RULING - DECISION C FINAL SEMANTICS,
2026-10-02: git_commit = the 08-24 ingestion commit itself, closed by a two-commit procedure;
regen_run_id absent before generation; successor-manifest Music/ entry repaired to valid YAML).

Deterministic; every input hash-asserted; repository inputs read from git commit de0c902.
Does NOT run any B-3 observation producer: fcpx_resolve.py is not invoked - the resolver census is
the committed packet evidence (decision_packet_b5_b14/etc_validation_stdout.txt). No media is
decoded; build_context.py only hashes the sources. No proxy is created or designated.

Usage (from anywhere):
  build_ingest_0824.py [--out-root DIR] [--git-commit VALUE]
VALUE is AWAITING_INGESTION (default; the existing pre-ingestion representation, used for Commit A,
the ingestion commit) or the full 40-hex hash of Commit A (used for Commit B, provenance closure).
DIR defaults to the repository root (writes the proposed working-tree files); any other DIR
(scratch) receives the same relative layout, for the determinism check. Recorded paths are
repository-relative, so the bytes do not depend on DIR.

Writes, relative to DIR:
  intelligence/p2/ingest_0824/sources/AR2-0824_ETC.json                successor ETC (declared_lock)
  intelligence/p2/ingest_0824/sources/AR2-0824.timeline_census.json   committed resolver evidence
  intelligence/p2/ingest_0824/sources/AR2-0824.context.stub.json      declared context
  intelligence/p2/ess/context/AR2-0824.context.json                    measured context
  intelligence/p2/ingest_0824/superseded/INGESTION_MANIFEST_v0.1.0.yaml   incumbent, byte-identical
  intelligence/p2/ingest_0824/INGESTION_MANIFEST.yaml                  successor v0.2.0
"""
import argparse, hashlib, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
BASE = 'de0c902c681fcd42a5ea85712484994eb4b41844'
VOL = '/Volumes/WE_CAPE_OUTPUT/AlphaRoundUp_2026'
D = 'Alpha RoundUp Part 2 /ALPHA ROUNDUP DAY 2 ANALYSIS/Corrected Video Analysis Files/'
REL = {'fcpxml': D + 'Alpha RoudUp Part 2.fcpxmld/Info.fcpxml',
       'srt': D + 'Alpha RoudUp Part 2_SRT_English (United States).srt',
       'mp4': D + 'Alpha RoudUp Part 2.mov'}
LOCK = VOL + '/' + REL['fcpxml']
ESS, ING = 'intelligence/p2/ess/', 'intelligence/p2/ingest_0824/'
ETC_OLD = ESS + 'decision_packet_b5_b14/AR2-0824_ETC.json'
ETC_NEW = ING + 'sources/AR2-0824_ETC.json'
TL = ING + 'sources/AR2-0824.timeline_census.json'
STUB = ING + 'sources/AR2-0824.context.stub.json'
CTX = ESS + 'context/AR2-0824.context.json'
MAN = ING + 'INGESTION_MANIFEST.yaml'
MAN_SUP = ING + 'superseded/INGESTION_MANIFEST_v0.1.0.yaml'
VAL = ESS + 'decision_packet_b5_b14/etc_validation_stdout.txt'
H = {'fcpxml': 'd82c2c3ec0f788cf47262194d6fbb8aefcd5fc9b7eee899b04bd3487f02e3a80',
     'srt': 'd93d86a1b7cd99c9baad2ce8e625f486056a5cb8b6229918d04b3bdcb304ef82',
     'mp4': 'ff34278fe1f47f678b36066780c3498633d27761655001ea97163099da9bbffe',
     ETC_OLD: '8c76a8cf460a450ea0dcbcd7802cae7fb3245cb1c8b4576a3a9f55ab185b0aaa',
     CTX: 'b0f432613b5e159d97d9dd41e4255adb1d2d903ff7dedbbd134857fcd75dc048',
     MAN: 'a76ea18cb6a495e020b353f6b2d83d4ee5df738a4646908b34a3ec7cd612cf70',
     VAL: '2edf791613a154c3f2a06d1f45c1dd67e18eb850dd731d020929354d0e372b42',
     ESS + 'scripts/etc_extract.py': '69777762130dc8a794eb11749e176f93e8a7477ca85d98f1b780fc154291d651',
     ESS + 'scripts/build_context.py': '83e5a998eed2e1257b6f2f32772c9b26d994ced86cbdb022ed7f8f3d89af0912'}
DECLARED_LOCK = '01:18:09:11'
MUSIC_OLD = ('  - {asset: "Final Data Source Files/Music/", note: >-\n'
             '      a directory named Music inside the governed source folder. Contents NOT inspected. Bears on\n'
             '      the copyright-exposure question that CUSTODY_ALERT_001 section 6 declined to answer without\n'
             '      a validated instrument.}\n')
MUSIC_NEW = ('  - asset: "Final Data Source Files/Music/"\n'
             '    note: >-\n'
             '      a directory named Music inside the governed source folder. Contents NOT inspected. Bears on\n'
             '      the copyright-exposure question that CUSTODY_ALERT_001 section 6 declined to answer without\n'
             '      a validated instrument.\n')
RULING = 'EO-2026-09-29 Addendum D (CHAIRMAN RULING - 08-24 OBSERVATION / INGESTION AUTHORITY, as corrected 2026-10-01)'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def git_bytes(rel):
    b = subprocess.run(['git', 'show', f'{BASE}:./{rel}'], cwd=ROOT, capture_output=True, check=True).stdout
    if hashlib.sha256(b).hexdigest() != H[rel]:
        sys.exit(f'STOP FAILED_SOURCE_IDENTITY {rel}')
    return b


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out-root', default=ROOT)
    ap.add_argument('--git-commit', default='AWAITING_INGESTION'); a = ap.parse_args()
    out = os.path.abspath(a.out_root)
    gc = a.git_commit
    if gc != 'AWAITING_INGESTION' and not (len(gc) == 40 and all(ch in '0123456789abcdef' for ch in gc)):
        sys.exit('STOP: --git-commit must be AWAITING_INGESTION or a full 40-hex commit hash')
    for k in (ESS + 'scripts/etc_extract.py', ESS + 'scripts/build_context.py'):
        git_bytes(k)
        if sha(os.path.join(ROOT, k)) != H[k]:
            sys.exit(f'STOP: working-tree {k} differs from {BASE[:7]}')
    if sha(LOCK) != H['fcpxml']:
        sys.exit('STOP FAILED_SOURCE_IDENTITY ED-003 lock')
    old_ctx, old_man, vs, old_etc = git_bytes(CTX), git_bytes(MAN), git_bytes(VAL), git_bytes(ETC_OLD)
    for d in ('sources', 'superseded'):
        os.makedirs(os.path.join(out, ING, d), exist_ok=True)
    os.makedirs(os.path.join(out, ESS, 'context'), exist_ok=True)

    # 1 - successor ETC by the established producer; same source string; declared_lock only
    subprocess.run([sys.executable, os.path.join(ROOT, ESS, 'scripts/etc_extract.py'), LOCK,
                    os.path.join(out, ETC_NEW), '--source', LOCK, '--declared-lock', DECLARED_LOCK,
                    '--expect-sha256', H['fcpxml']], check=True, capture_output=True)
    inc = json.loads(old_etc); suc = json.load(open(os.path.join(out, ETC_NEW)))
    if dict(inc, sequence=dict(inc['sequence'], declared_lock=DECLARED_LOCK)) != suc:
        sys.exit('STOP: successor ETC differs from the incumbent beyond declared_lock')
    etc_sha = sha(os.path.join(out, ETC_NEW))

    # 2 - resolver census from COMMITTED evidence (fcpx_resolve.py NOT run)
    t = vs.decode()
    val, _ = json.JSONDecoder().raw_decode(t[t.index('{'):])
    cen = json.loads(t[t.index('census:') + len('census:'):].strip().splitlines()[0])
    with open(os.path.join(out, TL), 'w') as f:
        json.dump({'validation': val, 'census': cen, 'provenance': {
            'source': VAL, 'source_sha256': H[VAL], 'source_commit': BASE,
            'note': ('fcpx_resolve.py output as committed with the B-5 decision packet, validating the '
                     'incumbent ETC ' + H[ETC_OLD][:16] + '... whose spine and connected_elements are '
                     'identical to the successor ETC. The resolver was NOT re-run (B-3 producer authority '
                     'not effective; Chairman correction, resume step 4).')}}, f, indent=1)

    # 3 - declared context stub: incumbent context + Chairman-approved values only
    c = json.loads(old_ctx)
    c['git_commit'] = gc            # Addendum D section 4.1: the 08-24 ingestion commit (Commit A)
    del c['regen_run_id']           # Addendum D section 4.2: absent until a regeneration run is assigned
    c['sha'].update(mp4=H['mp4'], etc=etc_sha)
    c['proxy'] = {'name': 'Alpha RoudUp Part 2.mov', 'video_duration_s': 4689.5, 'container_duration_s': 4689.5,
                  'resolution': '3840x2160', 'fps': 24}
    c['etc'] = {'spine': 201, 'connected': 459}
    c['source_files'] = {'fcpxml': REL['fcpxml'], 'srt': REL['srt'], 'etc': ETC_NEW, 'mp4': REL['mp4']}
    c['display_names'] = {'mp4': 'Alpha RoudUp Part 2.mov', 'fcpxml': 'Info.fcpxml',
                          'fcpxml_header': 'Alpha RoudUp Part 2.fcpxmld/Info.fcpxml', 'srt': 'CF-001 caption stream',
                          'srt_manifest': 'Alpha RoudUp Part 2_SRT_English (United States).srt',
                          'etc': 'AR2-0824_ETC.json'}
    c['regeneration_scope'] = {'mode': 'CANONICAL_EDITORIAL_TIMELINE', 'authority': RULING + ', correction item 2'}
    c['declared_segment_overlaps'] = []
    c['governed_narrative_boundaries'] = []
    with open(os.path.join(out, STUB), 'w') as f:
        json.dump(c, f, indent=1)

    # 4 - measured context via the established instrument; relative args -> path-independent bytes
    r = subprocess.run([sys.executable, os.path.join(ROOT, ESS, 'scripts/build_context.py'), '--in', STUB,
                        '--out', CTX, '--sources', VOL, '--timeline', TL, '--etc', ETC_NEW],
                       cwd=out, capture_output=True, text=True)
    if r.returncode:
        sys.exit('STOP build_context: ' + r.stderr)

    # 5 - manifest supersession: incumbent byte-identical under superseded/; successor v0.2.0
    open(os.path.join(out, MAN_SUP), 'wb').write(old_man)
    m = old_man.decode()

    def once(x, y):
        nonlocal m
        if m.count(x) != 1:
            sys.exit(f'STOP manifest anchor x{m.count(x)}: {x[:60]!r}')
        m = m.replace(x, y)
    once(MUSIC_OLD, MUSIC_NEW)       # Addendum D section 4.3: successor only; v0.1.0 keeps its defect
    once('# STATE: PREPARED_NOT_EXECUTED\n#\n',
         '# STATE: PREPARED_NOT_EXECUTED\n#\n'
         '# v0.2.0 (2026-10-01): records the Decision C CONTEXT INGESTION only - the designated sources\n'
         '# hashed and pinned into intelligence/p2/ess/context/AR2-0824.context.json (designated_sources\n'
         '# below). Registry population, parsing and regeneration have NOT been performed. Every 0.1.0\n'
         '# entry below is carried unedited as historical record (CF-001 section 2.4, ED-003); v0.1.0 is\n'
         '# preserved byte-identical at ingest_0824/superseded/INGESTION_MANIFEST_v0.1.0.yaml.\n#\n')
    once('manifest_version: 0.1.0\n', 'manifest_version: 0.2.0\n'
         f'supersedes: {{version: "0.1.0", sha256: "{H[MAN]}", preserved_at: "{MAN_SUP}", source_commit: "{BASE}"}}\n')
    ctx_sha = sha(os.path.join(out, CTX))
    vol = 'WE_CAPE_OUTPUT/AlphaRoundUp_2026'
    block = (
        '\n# ---------------------------------------------------------------------------\n'
        f'# DESIGNATED 08-24 SOURCES - Decision C context ingestion ({RULING})\n'
        '# Status token MEASURED is build_context.py source_manifest\'s own token. The assembly_assets\n'
        '# entries above are retained as historical record and are not the governed sources.\n'
        '# ---------------------------------------------------------------------------\n'
        'designated_sources:\n'
        f'  - {{role: fcpxml, authority: "ED-003", path: "{REL["fcpxml"]}", volume: "{vol}", sha256: {H["fcpxml"]}, ingestion_status: MEASURED}}\n'
        f'  - {{role: srt, authority: "CF-001", path: "{REL["srt"]}", volume: "{vol}", sha256: {H["srt"]}, ingestion_status: MEASURED}}\n'
        f'  - {{role: mp4, authority: "Addendum D, Decision A (observed directly; no proxy)", path: "{REL["mp4"]}", volume: "{vol}", sha256: {H["mp4"]}, ingestion_status: MEASURED}}\n'
        f'  - {{role: etc, authority: "Addendum D, Decision C as corrected (successor ETC, declared_lock {DECLARED_LOCK})", path: "{ETC_NEW}", sha256: {etc_sha}, supersedes: {{sha256: {H[ETC_OLD]}, preserved_at: "{ETC_OLD}"}}, ingestion_status: MEASURED}}\n'
        + ('# git_commit = the 08-24 ingestion commit (Addendum D section 4.1). AWAITING_INGESTION here means\n'
           '# Commit A (ingestion custody); the provenance-closure commit (Commit B) that follows Commit A\n'
           '# writes Commit A\'s full hash. basis_commit = the repository state the ingestion was built from.\n')
        + f'  - {{role: context, authority: "Addendum D, Decision C", path: "{CTX}", sha256: {ctx_sha}, built_by: build_context.py, git_commit: "{gc}", basis_commit: "{BASE}"}}\n')
    once('\n# ---------------------------------------------------------------------------\n# PUBLIC DISTRIBUTION ASSETS',
         block + '\n# ---------------------------------------------------------------------------\n# PUBLIC DISTRIBUTION ASSETS')
    with open(os.path.join(out, MAN), 'w') as f:
        f.write(m)
    for p in (ETC_NEW, TL, STUB, CTX, MAN_SUP, MAN):
        print(sha(os.path.join(out, p)), p)


if __name__ == '__main__':
    main()
