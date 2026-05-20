#!/usr/bin/env python3
"""
W.E. FLOW / W.E. FORGE — Acceptance Test Runner v4.1 ENHANCED
Runs all §17 tests without pytest. Self-contained.

Usage:
  python run_tests.py              # all tests
  python run_tests.py --suite 1    # Test 1 only (classification)
  python run_tests.py --suite 4    # Test 4 only (output structure)
  python run_tests.py --verbose    # show passing tests too

Exit codes:
  0  — all tests passed
  1  — one or more tests failed
"""

import sys
import argparse
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def _collect(module_path: str) -> list[tuple[str, callable]]:
    import importlib.util
    spec = importlib.util.spec_from_file_location("mod", module_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [
        (name, fn) for name, fn in vars(mod).items()
        if name.startswith("test_") and callable(fn)
    ]


SUITE_MAP = {
    "1":   ("§17 Test 1 — Classification",          "tests/test_classifier.py"),
    "2":   ("§17 Test 2 — Variant Detection",        "tests/test_variants.py"),
    "3":   ("§17 Test 3 — Multicam Grouping",        "tests/test_grouper.py"),
    "4,5": ("§17 Tests 4+5 — Output Structure + Logging", "tests/test_output.py"),
    "6":   ("§17 Test 6 + §3.x — Idempotency + Edge Cases", "tests/test_idempotency.py"),
    "5ts": ("§5 Timestamp Fallback Chain",           "tests/test_timestamp.py"),
}


def run_suite(label: str, module_path: str, verbose: bool) -> tuple[list, list]:
    base = Path(__file__).parent
    tests = _collect(str(base / module_path))
    passed, failed = [], []
    print(f"\n{label}")
    print("─" * len(label))
    for name, fn in tests:
        with tempfile.TemporaryDirectory() as td:
            try:
                fn(Path(td))
                passed.append(name)
                if verbose:
                    print(f"  ✓ {name}")
            except Exception as e:
                failed.append((name, str(e)))
                print(f"  ✗ {name}")
                print(f"      {e}")
    if not verbose:
        print(f"  {len(passed)}/{len(passed)+len(failed)} passed", end="")
        print("  ✓" if not failed else "")
    return passed, failed


def main():
    parser = argparse.ArgumentParser(description="W.E. FLOW Acceptance Runner")
    parser.add_argument("--suite", default="all",
                        help="Suite key: 1 2 3 4,5 6 5ts  (default: all)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print("=" * 60)
    print("  W.E. FLOW / W.E. FORGE — Acceptance Suite v4.1 ENHANCED")
    print("=" * 60)

    suites = SUITE_MAP.items() if args.suite == "all" else [
        (k, v) for k, v in SUITE_MAP.items() if k == args.suite
    ]

    all_passed, all_failed = [], []
    for key, (label, path) in suites:
        p, f = run_suite(label, path, args.verbose)
        all_passed.extend(p)
        all_failed.extend(f)

    total = len(all_passed) + len(all_failed)
    print(f"\n{'=' * 60}")
    print(f"TOTAL: {len(all_passed)}/{total} passed", end="")

    if all_failed:
        print(f"  —  {len(all_failed)} FAILED")
        print("\nFailed tests:")
        for name, err in all_failed:
            print(f"  ✗ {name}")
            print(f"      {err}")
        sys.exit(1)
    else:
        print("  — All acceptance tests passed ✓")
        print("\nDocument is contract-grade. Ready for vendor distribution.")
        sys.exit(0)


if __name__ == "__main__":
    main()
