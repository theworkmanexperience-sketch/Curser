#!/usr/bin/env python3
"""
DEPRECATED entry point.

The canonical CLI is now `python -m wecape` (source: wecape/capture/main.py),
with config at wecape/config.yaml and profiles at wecape/profiles/.

This shim remains only so existing `python we_capture/main.py ...` invocations
keep working. It will be removed in a future release.
"""

import sys
from pathlib import Path

# Put the repo root on the path so `import wecape` resolves when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wecape.capture.main import main

if __name__ == '__main__':
    print("[deprecated] we_capture/main.py — use:  python -m wecape", file=sys.stderr)
    main()
