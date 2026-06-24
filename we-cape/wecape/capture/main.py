#!/usr/bin/env python3
"""
W.E. C.A.P.E. CAPTURE — Canonical CLI Entry Point

Run as:
  python -m wecape --input /path/to/media --output /path/to/project
  python -m wecape --input ./raw --output ./project --profile ryderz
  python -m wecape --input ./raw --output ./project --workers 16

(The legacy `python we_capture/main.py` shim still works but is deprecated.)
"""

import sys
import argparse
from pathlib import Path

# Canonical config lives at the package root: wecape/config.yaml
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / 'config.yaml'


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog='wecape',
        description='W.E. C.A.P.E. CAPTURE — Deterministic Media Ingestion Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default single-folder ingest (§3 primary mode)
  python -m wecape --input /Volumes/CARD/DCIM --output ~/Projects/Shoot_2024

  # Client profile (overrides grouping window, camera offsets, workers)
  python -m wecape --input ./raw --output ./project --profile ryderz

  # High-core machine (Studio tier requires >=8 workers)
  python -m wecape --input ./raw --output ./project --workers 16
        """
    )
    p.add_argument('--profile', default=None,
                   help='Client profile name (e.g. --profile ryderz)')
    p.add_argument('--list-profiles', action='store_true',
                   help='List all available profiles and exit')
    p.add_argument('--input', '-i', type=Path, required=False,
                   help='Input path: single mixed folder (default mode, §4).')
    p.add_argument('--output', '-o', type=Path, required=False,
                   help='Output root. Created if absent.')
    p.add_argument('--proxy', action='store_true', default=False,
                   help='Enable proxy generation for this run (overrides profile setting)')
    p.add_argument('--config', '-c', type=Path, default=DEFAULT_CONFIG,
                   help='Config file path (default: wecape/config.yaml).')
    p.add_argument('--workers', '-w', type=int, default=None,
                   help='Override max_workers from config (§6.x: >=8 for Studio tier).')
    p.add_argument('--engine', choices=['stages', 'legacy'], default=None,
                   help='Orchestration engine: stages (default) routes through '
                        'run_stages(); legacy is the pre-rewire rollback path.')
    return p.parse_args()


def main():
    args = parse_args()

    # --list-profiles doesn't need --input or --output
    if getattr(args, 'list_profiles', False):
        from wecape.capture.profile import ProfileLoader
        profiles = ProfileLoader().list_profiles()
        if not profiles:
            print("No profiles found in wecape/profiles/ or ~/.wecape/profiles/")
        else:
            print(f"\n{'Name':<20} {'Client':<25} Description")
            print("-" * 70)
            for prof in profiles:
                print(f"{prof['name']:<20} {prof['client']:<25} {prof['description'][:25]}")
            print()
        raise SystemExit(0)

    if args.input is None or not args.input.exists():
        print('[ERROR] Input path is required and must exist')
        sys.exit(1)
    if not args.config.exists():
        print(f'[ERROR] Config file not found: {args.config}')
        sys.exit(1)
    if not args.output:
        print('[ERROR] --output is required')
        sys.exit(1)

    from wecape.capture.pipeline import Pipeline

    print('=' * 60)
    print('  W.E. C.A.P.E. CAPTURE  |  Deterministic Media Ingestion Engine')
    print('=' * 60)

    # Build the full run config — base + optional profile + CLI overrides —
    # centralized in wecape.core.config.
    from wecape.core.config import load_config, validate, write_temp
    try:
        config = load_config(
            args.config,
            profile=args.profile,
            proxy=getattr(args, 'proxy', False),
            engine=getattr(args, 'engine', None),
            workers=args.workers,
        )
    except Exception as e:
        print(f'[ERROR] {e}')
        sys.exit(1)

    if args.profile:
        meta = config.get('_active_profile', {})
        print(f"  [PROFILE] {args.profile}"
              + (f" — {meta['client']}" if meta.get('client') else ""))
    if getattr(args, 'proxy', False):
        print('  [PROXY] proxy generation enabled via --proxy flag')
    if args.workers is not None:
        print(f'  [WORKERS] {args.workers} (CLI override)')
    if getattr(args, 'engine', None):
        print(f'  [ENGINE] {args.engine}')
    for w in validate(config):
        print(f'  [config] ⚠ {w}')

    pipeline = Pipeline(config_path=write_temp(config))

    summary = pipeline.run(input_path=args.input, output_path=args.output)

    fatal = [e for e in summary.get('pipeline_errors', []) if e.startswith('FATAL')]
    sys.exit(1 if fatal else 0)


if __name__ == '__main__':
    main()
