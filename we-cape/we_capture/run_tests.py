#!/usr/bin/env python3
"""DEPRECATED — use repo-root run_tests.py (python run_tests.py)."""
import runpy, sys
from pathlib import Path
sys.argv[0]=str(Path(__file__).resolve().parent.parent/"run_tests.py")
runpy.run_path(sys.argv[0], run_name="__main__")
