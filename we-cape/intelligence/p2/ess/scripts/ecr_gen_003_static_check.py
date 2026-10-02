#!/usr/bin/env python3
"""ecr_gen_003_static_check.py — non-executing validation of the ECR-GEN-003 changes.

Compares each B-3 producer as committed at the base commit with the working tree,
using `ast` only: no producer is imported or run. Checks, per file:

  S1  the new file parses;
  S2  every top-level statement of the base file that is NOT on that file's
      allow-list of modified statements is present, AST-identical, in the new file;
  S3  no numeric constant of the base file is lost or changed (multiset inclusion);
  S4  no string constant of the base file is lost, except the allow-listed
      machine paths, docstrings and (step0_offset) the segment-table literal;
  S5  no absolute filesystem path literal remains;
plus
  V1  produce_video_obs: the per-frame statements of observe_stream() equal the
      base observe() loop body, statement for statement, and the ffmpeg/ffprobe
      command literals are unchanged;
  O1  step0_offset: the segment table supplied by --segments, as recorded in the
      ECR-GEN-003 document, equals the base literal value for value.

USAGE  ecr_gen_003_static_check.py --base <commit> [--segments-json <file>]
Exit 0 = every check PASS.
"""
import argparse
import ast
import collections
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
REL = 'intelligence/p2/ess/scripts/'

# Top-level statements each file is AUTHORIZED to change (by function/class name, or
# by the source text the statement starts with). Everything else must be identical.
MODIFIED = {
    'produce_audio_rms.py': {'main'},
    'produce_video_obs.py': {'decode_frames', 'observe', 'main'},
    'fcpx_resolve.py': {'_emit', 'main', 'if __name__'},
    'derive_camera_runs.py': {'main'},
    'step0_offset.py': {'U=', 'cues=parse_srt(', 'rms=np.load(', 'tl=json.load(', 'segs=[',
                        'json.dump(res,'},
    'step0_anchors.py': {'U=', 'cues=parse(', 'tl=json.load(', 'json.dump(rows,'},
}
REMOVED_STRINGS_OK = re.compile(r'^(/mnt/|/home/claude/|inputs/lock_srt2\.srt$|audio_rms_0p25\.npy$)')


def git_show(base, rel):
    return subprocess.run(['git', 'show', '%s:./%s' % (base, rel)], cwd=REPO,
                          capture_output=True, check=True).stdout.decode('utf-8')


def label(node, src):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return node.name
    seg = ast.get_source_segment(src, node) or ''
    return seg.replace(' ', '')[:40]


def is_modified(node, src, allow):
    lab = label(node, src)
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return lab in allow
    seg = (ast.get_source_segment(src, node) or '')
    return any(seg.replace(' ', '').startswith(a.replace(' ', '')) for a in allow)


def docstring_node(tree):
    b = tree.body
    return b[0] if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], 'value', None), ast.Constant) \
        and isinstance(b[0].value.value, str) else None


def consts(tree, kind):
    doc = docstring_node(tree)
    docs = {id(doc.value)} if doc else set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(getattr(n.body[0], 'value', None), ast.Constant):
            docs.add(id(n.body[0].value))
    c = collections.Counter()
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and id(n) not in docs:
            v = n.value
            if kind == 'num' and isinstance(v, (int, float)) and not isinstance(v, bool):
                c[repr(v)] += 1
            if kind == 'str' and isinstance(v, str):
                c[v] += 1
    return c


def func(tree, name):
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return n
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    ap.add_argument('--segments-json', default=None)
    a = ap.parse_args()
    results = []

    def rec(cid, ok, detail):
        results.append((cid, bool(ok), detail))

    for fn, allow in MODIFIED.items():
        old_src = git_show(a.base, REL + fn)
        new_src = open(os.path.join(HERE, fn), encoding='utf-8').read()
        old = ast.parse(old_src)
        try:
            new = ast.parse(new_src)
            rec('S1 ' + fn, True, 'parses')
        except SyntaxError as e:
            rec('S1 ' + fn, False, 'syntax error: %s' % e)
            continue
        new_dumps = [ast.dump(n) for n in new.body]
        missing, modified = [], []
        old_doc = docstring_node(old)
        for n in old.body:
            if n is old_doc or isinstance(n, (ast.Import, ast.ImportFrom)):
                continue
            if is_modified(n, old_src, allow):
                modified.append(label(n, old_src))
                continue
            if ast.dump(n) not in new_dumps:
                missing.append(label(n, old_src))
        rec('S2 ' + fn, not missing,
            'unmodified statements identical; authorized modifications: %s%s'
            % (sorted(modified), '' if not missing else '; CHANGED: %s' % missing))
        on, nn = consts(old, 'num'), consts(new, 'num')
        lost_n = {k: v for k, v in on.items() if nn[k] < v}
        added_n = sorted(k for k in nn if nn[k] > on[k])
        rec('S3 ' + fn, not lost_n, 'no numeric constant lost%s; added: %s'
            % ('' if not lost_n else ' - LOST %s' % lost_n, added_n))
        os_, ns_ = consts(old, 'str'), consts(new, 'str')
        lost_s = sorted(k for k, v in os_.items() if ns_[k] < v)
        seg_strings = set()
        if fn == 'step0_offset.py':
            for n in old.body:
                if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'segs':
                    seg_strings = {s for row in ast.literal_eval(n.value) for s in row}
        bad = [s for s in lost_s if not REMOVED_STRINGS_OK.match(s) and s not in seg_strings]
        rec('S4 ' + fn, not bad, 'string constants preserved except authorized removals %s%s'
            % ([s for s in lost_s if REMOVED_STRINGS_OK.match(s)],
               '' if not bad else '; UNAUTHORIZED LOSS: %s' % bad))
        abs_paths = [k for k in ns_ if re.match(r'^/(mnt|home|Users|Volumes|private|tmp)/', k)]
        rec('S5 ' + fn, not abs_paths, 'no absolute path literal' if not abs_paths else str(abs_paths))

        if fn == 'produce_video_obs.py':
            ob = func(old, 'observe')
            loop = [s for s in ob.body if isinstance(s, ast.For)][0]
            nb = func(new, 'observe_stream')
            nloop = [s for s in nb.body if isinstance(s, ast.For)][0]
            body_new = [ast.dump(s) for s in nloop.body]
            body_old = [ast.dump(s) for s in loop.body]
            k = body_new.index(body_old[0]) if body_old[0] in body_new else -1
            same = k >= 0 and body_new[k:k + len(body_old)] == body_old
            pre_old = [ast.dump(s) for s in ob.body if not isinstance(s, (ast.For, ast.Return))]
            a_b_ok = any(ast.dump(s) == d for s in nb.body for d in pre_old
                         if 'Name(id=\'a\'' in d)
            rec('V1 produce_video_obs.py per-frame body', same and a_b_ok,
                '%d per-frame statements identical to base observe(); band split a,b identical'
                % len(body_old))
            cmd_old = [ast.dump(n) for n in ast.walk(func(old, 'decode_frames')) if isinstance(n, ast.List)]
            cmd_new = [ast.dump(n) for n in ast.walk(func(new, 'stream_frames')) if isinstance(n, ast.List)]
            rec('V1 produce_video_obs.py ffmpeg command', cmd_old and cmd_old[0] in cmd_new,
                'ffmpeg decode command literal unchanged')
        if fn == 'fcpx_resolve.py':
            # R1 (Option (a), Chairman ruling): resolver stdout and output JSON unchanged. Stdout
            # is printed only by _emit() from out['validation'] and census, both built in main().
            # main() must equal the base once the one added sidecar-bookkeeping statement
            # (_PROV.update(...)) is removed; every print in _emit() must equal the base.
            def strip_prov(fnode):
                body = [s for s in fnode.body
                        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Call)
                                and ast.unparse(s.value.func) == '_PROV.update')] \
                    if hasattr(ast, 'unparse') else [s for s in fnode.body
                                                     if '_PROV' not in ast.dump(s)]
                return [ast.dump(s) for s in body]
            main_same = strip_prov(func(new, 'main')) == [ast.dump(s) for s in func(old, 'main').body]
            prints = lambda f: [ast.dump(n) for n in ast.walk(f) if isinstance(n, ast.Call)  # noqa: E731
                                and getattr(n.func, 'id', None) == 'print']
            emit_same = prints(func(new, '_emit')) == prints(func(old, '_emit'))
            no_key = 'etc_sha256' not in consts(new, 'str')
            sidecar_etc = "('etc', _PROV.get('etc'))" in new_src
            rec('R1 fcpx_resolve.py stdout/JSON unchanged', main_same and emit_same and no_key and sidecar_etc,
                'main() == base minus the sidecar-bookkeeping statement; _emit() prints == base; '
                'no etc_sha256 key; ETC hashed as a sidecar input')
        if fn == 'step0_offset.py' and a.segments_json:
            for n in old.body:
                if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'segs':
                    lit = [list(r) for r in ast.literal_eval(n.value)]
            rec('O1 step0_offset.py segment table', json.load(open(a.segments_json)) == lit,
                '%d rows; supplied table equals the base literal value for value' % len(lit))

    for cid, ok, d in results:
        print('%s  %-42s %s' % ('PASS' if ok else 'FAIL', cid, d))
    fails = [r for r in results if not r[1]]
    print('%d/%d PASS' % (len(results) - len(fails), len(results)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
