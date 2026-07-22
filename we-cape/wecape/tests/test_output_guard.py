"""Deliverable 2 — output-inside-input preflight guard."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import os
os.environ['WECAPE_TEST_MODE'] = '1'
from wecape.capture.pipeline import Pipeline


def _pipe(tmp_path):
    import yaml
    cfg = {"pipeline": {"run_id_prefix": "G", "file_operation": "copy",
                        "enable_duplicate_content_detection": False},
           "grouping": {"window_seconds": 5, "min_cameras": 2,
                        "camera_offsets": {}},
           "proxies": {"generate_proxies": False},
           "performance": {"max_workers": 1, "hash_chunk_size_mb": 1},
           "logging": {"log_level": "WARNING", "log_format": "json"},
           "output": {"date_format": "%Y-%m-%d", "group_id_prefix": "MCG"}}
    p = tmp_path / "cfg.yaml"
    p.write_text(yaml.dump(cfg))
    return Pipeline(p)


def test_output_inside_input_refused(tmp_path):
    src = tmp_path / "shoot"; (src / "clips").mkdir(parents=True)
    out = src / "CAPTURE"
    with pytest.raises(RuntimeError, match="REFUSED"):
        _pipe(tmp_path)._guard_output_geometry(src, out)


def test_output_equals_input_refused(tmp_path):
    src = tmp_path / "shoot"; src.mkdir()
    with pytest.raises(RuntimeError, match="REFUSED"):
        _pipe(tmp_path)._guard_output_geometry(src, src)


def test_sibling_output_allowed(tmp_path):
    src = tmp_path / "shoot/SOURCES"; src.mkdir(parents=True)
    out = tmp_path / "shoot/CAPTURE"
    _pipe(tmp_path)._guard_output_geometry(src, out)  # no raise


def test_input_inside_output_allowed(tmp_path):
    # writing beside/above input's parent is legitimate; only
    # output-inside-input recurses
    src = tmp_path / "big/shoot"; src.mkdir(parents=True)
    out = tmp_path / "big"
    _pipe(tmp_path)._guard_output_geometry(src, out)  # no raise
