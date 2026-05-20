#!/usr/bin/env python3
"""
W.E. FLOW / W.E. FORGE — CLI Entry Point v4.1 ENHANCED

Usage:
  python main.py --input /path/to/media --output /path/to/project
  python main.py --input /path/to/media --output /path/to/project --config custom.yaml
  python main.py --input /path/to/media --output /path/to/project --workers 16
"""

import sys
import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog='we_flow',
        description='W.E. FLOW / W.E. FORGE — Deterministic Media Ingestion Engine v4.1',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default single-folder ingest (§3 primary mode)
  python main.py --input /Volumes/CARD/DCIM --output ~/Projects/Shoot_2024

  # Custom config (override grouping window, camera offsets, workers)
  python main.py --input ./raw --output ./project --config ./custom.yaml

  # High-core machine (Studio tier requires ≥8 workers)
  python main.py --input ./raw --output ./project --workers 16
        """
    )
    p.add_argument('--input', '-i', type=Path, required=True,
                   help='Input path: single mixed folder (default mode, §4).')
    p.add_argument('--output', '-o', type=Path, required=True,
                   help='Output root. Created if absent.')
    p.add_argument('--config', '-c', type=Path,
                   default=Path(__file__).parent / 'config.yaml',
                   help='Config file path (default: config.yaml in project root).')
    p.add_argument('--workers', '-w', type=int, default=None,
                   help='Override max_workers from config (§6.x: ≥8 for Studio tier).')
    return p.parse_args()


def main():
    args = parse_args()

    if not args.input.exists():
        print(f'[ERROR] Input path does not exist: {args.input}')
        sys.exit(1)
    if not args.config.exists():
        print(f'[ERROR] Config file not found: {args.config}')
        sys.exit(1)

    from engine.pipeline import Pipeline

    print('=' * 60)
    print('  W.E. FLOW / W.E. FORGE  |  v4.1 ENHANCED')
    print('  Deterministic Media Ingestion Engine')
    print('=' * 60)

    pipeline = Pipeline(config_path=args.config)

    # CLI --workers overrides config value
    if args.workers is not None:
        pipeline.max_workers = args.workers
        print(f'  Workers: {args.workers} (CLI override)')

    summary = pipeline.run(input_path=args.input, output_path=args.output)

    # Exit non-zero if there were non-recoverable errors
    fatal = [e for e in summary.get('pipeline_errors', []) if e.startswith('FATAL')]
    sys.exit(1 if fatal else 0)


if __name__ == '__main__':
    main()
