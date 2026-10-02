#!/usr/bin/env python3
"""ecr_gen_004_static_check.py — non-executing check of the ECR-GEN-004 successor.

Compares derive_camera_runs_v2.py with its predecessor derive_camera_runs.py using `ast`
only (neither is imported or run) and passes only if:
  C1  every top-level statement other than the module docstring is AST-identical, except
      family();
  C2  family() differs from the predecessor in exactly one node: the fallback return
      constant 'COMPOUND' -> 'UNCERTAIN';
  C3  the successor contains no 'COMPOUND' string constant outside its docstring;
  C4  the predecessor file is byte-identical to its committed version (it is retained,
      unchanged, for the historical 08-22 outputs).
USAGE  ecr_gen_004_static_check.py [--base <commit>]   (default HEAD)
"""
import argparse
import ast
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
REL = 'intelligence/p2/ess/scripts/'


def body(tree):
    b = tree.body
    if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], 'value', None), ast.Constant):
        b = b[1:]
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='HEAD')
    a = ap.parse_args()
    old_src = open(os.path.join(HERE, 'derive_camera_runs.py'), encoding='utf-8').read()
    new_src = open(os.path.join(HERE, 'derive_camera_runs_v2.py'), encoding='utf-8').read()
    old, new = ast.parse(old_src), ast.parse(new_src)
    ob, nb = body(old), body(new)
    res = []
    same_len = len(ob) == len(nb)
    others = same_len and all(ast.dump(x) == ast.dump(y) for x, y in zip(ob, nb)
                              if not (isinstance(x, ast.FunctionDef) and x.name == 'family'))
    res.append(('C1 all other top-level statements identical', others))
    fo = [x for x in ob if isinstance(x, ast.FunctionDef) and x.name == 'family'][0]
    fn = [x for x in nb if isinstance(x, ast.FunctionDef) and x.name == 'family'][0]
    ro, rn = fo.body[-1], fn.body[-1]
    only_const = (len(fo.body) == len(fn.body)
                  and all(ast.dump(x) == ast.dump(y) for x, y in zip(fo.body[:-1], fn.body[:-1]))
                  and isinstance(ro, ast.Return) and isinstance(rn, ast.Return)
                  and getattr(ro.value, 'value', None) == 'COMPOUND'
                  and getattr(rn.value, 'value', None) == 'UNCERTAIN'
                  and ast.dump(fo.args) == ast.dump(fn.args))
    res.append(("C2 family(): only the fallback constant 'COMPOUND' -> 'UNCERTAIN'", only_const))
    consts = [n.value for n in ast.walk(ast.Module(body=nb, type_ignores=[]))
              if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    res.append(("C3 no 'COMPOUND' constant in successor code", not any('COMPOUND' in c for c in consts)))
    committed = subprocess.run(['git', 'show', '%s:./%s' % (a.base, REL + 'derive_camera_runs.py')],
                               cwd=REPO, capture_output=True, check=True).stdout
    res.append(('C4 predecessor unchanged vs %s' % a.base, committed == old_src.encode('utf-8')))
    for name, ok in res:
        print('%s  %s' % ('PASS' if ok else 'FAIL', name))
    print('successor sha256 %s' % hashlib.sha256(new_src.encode('utf-8')).hexdigest())
    print('%d/%d PASS' % (sum(ok for _, ok in res), len(res)))
    return 0 if all(ok for _, ok in res) else 1


if __name__ == '__main__':
    sys.exit(main())
