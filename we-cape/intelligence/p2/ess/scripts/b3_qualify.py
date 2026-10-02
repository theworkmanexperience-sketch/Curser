#!/usr/bin/env python3
"""b3_qualify.py — ECR-GEN-003 qualification harness for B-3 observation producers.

Runs ONE producer against ONE explicitly supplied fixture, two or more times, and
records mechanical evidence. It is evidence only:

  it DOES    assert every fixture input against its declared SHA-256 before running;
             run the producer as a subprocess (it never imports a producer);
             snapshot the declared watch roots and the work directory before and
             after every run, and report any write outside that run's output dir;
             require exactly the declared output files, and nothing else, in it;
             compare every output's bytes across runs (and, optionally, against
             expected SHA-256 values supplied in the fixture spec);
             record the producer SHA-256, input SHA-256, arguments, interpreter and
             external-tool identities, and a mechanical PASS / FAIL per check.
  it does NOT designate a producer, grant or activate any B-3 authority, interpret
             or adjudicate output, classify observation meaning, change thresholds,
             or touch any registry. A PASS is qualification evidence for the
             Chairman, nothing more.

No wall-clock value enters the report, and the report names files relative to the
work directory, so the same fixture on the same toolchain yields the same bytes.

USAGE
  b3_qualify.py --spec <fixture.json> --work <empty dir> --report <report.json>

FIXTURE SPEC (JSON)
  fixture_id          string
  producer            path to the producer script
  python              interpreter used to run the producer
  path                PATH given to the producer (selects ffmpeg/ffprobe); optional
  tools               external executables to identify on that PATH, e.g. ["ffmpeg"]
  inputs              {name: path}
  input_sha256        {name: sha256}          -- every input must be listed
  args                argument template; "{out}" = this run's output dir,
                      "{in:NAME}" = the input path called NAME
  declared_outputs    file names expected in the output dir, and only these
  expect_exit         expected exit status (default 0)
  expect_output_sha256  {output name: sha256}  -- optional oracle
  watch_roots         directories to snapshot for undeclared writes
  reruns              number of runs, >= 2 (default 2)

Exit codes: 0 = every check PASS, 1 = some check FAIL, 2 = spec or input STOP.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

REPORT_SCHEMA = 'b3-qualification/1'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()


def stop(msg):
    print('STOP: %s' % msg, file=sys.stderr)
    sys.exit(2)


def snapshot(root):
    """Metadata of every entry under root (lstat only; symlinks are not followed)."""
    snap = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in dirnames + sorted(filenames):
            p = os.path.join(dirpath, name)
            try:
                st = os.lstat(p)
            except OSError:
                continue
            snap[p] = (st.st_mode, st.st_size, st.st_mtime_ns, st.st_ino)
    return snap


def changed(before, after):
    out = []
    for p in sorted(set(before) | set(after)):
        if p not in before:
            out.append(('created', p))
        elif p not in after:
            out.append(('deleted', p))
        elif before[p] != after[p]:
            out.append(('modified', p))
    return out


def identify(python, path_env, tools):
    env = dict(os.environ, PATH=path_env) if path_env else dict(os.environ)
    py = subprocess.run([python, '-c', 'import os,platform,sys;print(platform.python_version());'
                         'print(sys.implementation.name);print(os.path.realpath(sys.executable))'],
                        capture_output=True, text=True, env=env)
    v, impl, real = (py.stdout.split('\n') + ['', '', ''])[:3]
    ident = dict(python=dict(version=v, implementation=impl, interpreter=real,
                             sha256=sha256(real) if real and os.path.exists(real) else None),
                 tools=[])
    for t in tools:
        w = subprocess.run(['/usr/bin/which', t], capture_output=True, text=True, env=env).stdout.strip()
        if not w:
            ident['tools'].append(dict(name=t, resolved=None))
            continue
        real_t = os.path.realpath(w)
        ver = subprocess.run([real_t, '-hide_banner', '-version'], capture_output=True, text=True)
        ident['tools'].append(dict(name=t, resolved=real_t, sha256=sha256(real_t),
                                   version=(ver.stdout.splitlines() or [None])[0]))
    return ident


def expand(template, out_dir, inputs):
    args = []
    for a in template:
        s = a.replace('{out}', out_dir)
        for name, p in inputs.items():
            s = s.replace('{in:%s}' % name, p)
        args.append(s)
    return args


def main():
    ap = argparse.ArgumentParser(description='B-3 producer qualification harness (evidence only).')
    ap.add_argument('--spec', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--report', required=True)
    a = ap.parse_args()

    spec = json.load(open(a.spec))
    for k in ('fixture_id', 'producer', 'python', 'inputs', 'input_sha256', 'args',
              'declared_outputs', 'watch_roots'):
        if k not in spec:
            stop('fixture spec is missing %r' % k)
    reruns = int(spec.get('reruns', 2))
    if reruns < 2:
        stop('reruns must be >= 2')
    work = os.path.abspath(a.work)
    if os.path.exists(work) and os.listdir(work):
        stop('work directory %s is not empty' % work)
    os.makedirs(work, exist_ok=True)
    report_path = os.path.abspath(a.report)
    if report_path.startswith(work + os.sep):
        stop('the report must be written outside the work directory')

    # ---- inputs: every one declared and hash-asserted before anything runs ----
    inputs = {k: os.path.abspath(v) for k, v in spec['inputs'].items()}
    in_rec = []
    for name in sorted(inputs):
        p = inputs[name]
        if name not in spec['input_sha256']:
            stop('input %r has no declared SHA-256' % name)
        if not os.path.isfile(p):
            stop('input %r does not exist: %s' % (name, p))
        got = sha256(p)
        if got != spec['input_sha256'][name]:
            stop('input %r SHA-256 %s != declared %s' % (name, got, spec['input_sha256'][name]))
        in_rec.append(dict(name=name, sha256=got, bytes=os.path.getsize(p)))

    producer = os.path.abspath(spec['producer'])
    roots = sorted({os.path.abspath(r) for r in spec['watch_roots']} | {work})
    env = dict(PATH=spec.get('path') or os.environ.get('PATH', ''), LANG='C', LC_ALL='C', TZ='UTC',
               PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', HOME=os.environ.get('HOME', ''))
    expect_exit = int(spec.get('expect_exit', 0))
    declared = sorted(spec['declared_outputs'])

    runs = []
    for k in range(1, reruns + 1):
        run_dir = os.path.join(work, 'run%d' % k)
        out_dir = os.path.join(run_dir, 'out')
        cwd = os.path.join(run_dir, 'cwd')
        os.makedirs(out_dir)
        os.makedirs(cwd)
        before = {r: snapshot(r) for r in roots}
        proc = subprocess.run([spec['python'], producer] + expand(spec['args'], out_dir, inputs),
                              cwd=cwd, env=env, capture_output=True)
        after = {r: snapshot(r) for r in roots}
        undeclared = []
        for r in roots:
            for kind, p in changed(before[r], after[r]):
                if p == out_dir or p.startswith(out_dir + os.sep):
                    continue
                undeclared.append(dict(change=kind, path=os.path.relpath(p, work)
                                       if p.startswith(work + os.sep) else p))
        present = sorted(os.listdir(out_dir))
        outputs = {n: dict(sha256=sha256(os.path.join(out_dir, n)),
                           bytes=os.path.getsize(os.path.join(out_dir, n)))
                   for n in present if os.path.isfile(os.path.join(out_dir, n))}
        norm = lambda b: b.replace(out_dir.encode(), b'{out}')   # noqa: E731
        runs.append(dict(run=k, exit=proc.returncode, outputs=outputs, files_present=present,
                         stdout_sha256=hashlib.sha256(norm(proc.stdout)).hexdigest(),
                         stderr_sha256=hashlib.sha256(norm(proc.stderr)).hexdigest(),
                         stderr_head=norm(proc.stderr).decode('utf-8', 'replace')[:400],
                         undeclared_writes=undeclared))

    first = runs[0]
    checks = dict(
        exit_as_expected=all(r['exit'] == expect_exit for r in runs),
        declared_outputs_exactly=all(r['files_present'] == declared for r in runs),
        no_undeclared_writes=all(not r['undeclared_writes'] for r in runs),
        outputs_byte_identical_across_runs=all(r['outputs'] == first['outputs'] for r in runs),
        stdout_identical_across_runs=all(r['stdout_sha256'] == first['stdout_sha256'] for r in runs),
    )
    oracle = spec.get('expect_output_sha256') or {}
    if oracle:
        checks['outputs_match_expected_sha256'] = all(
            r['outputs'].get(n, {}).get('sha256') == h for r in runs for n, h in oracle.items())

    report = dict(schema=REPORT_SCHEMA, fixture_id=spec['fixture_id'],
                  authority='NONE - qualification evidence only; designates nothing and '
                            'grants no B-3 authority',
                  producer=dict(path=spec['producer'], sha256=sha256(producer)),
                  args_template=spec['args'], inputs=in_rec, declared_outputs=declared,
                  expect_exit=expect_exit, expected_output_sha256=oracle,
                  environment=dict(PATH=env['PATH'], LANG='C', TZ='UTC', PYTHONHASHSEED='0',
                                   PYTHONDONTWRITEBYTECODE='1'),
                  toolchain=identify(spec['python'], spec.get('path'), spec.get('tools', [])),
                  watch_roots=[os.path.relpath(r, work) if r.startswith(work) else r for r in roots],
                  runs=runs, checks=checks,
                  verdict='PASS' if all(checks.values()) else 'FAIL')
    with open(report_path, 'w') as fh:
        fh.write(json.dumps(report, indent=1, sort_keys=True) + '\n')
    for name, ok in checks.items():
        print('%s  %s' % ('PASS' if ok else 'FAIL', name))
    print('verdict: %s  (evidence only; no authority granted)' % report['verdict'])
    return 0 if report['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
