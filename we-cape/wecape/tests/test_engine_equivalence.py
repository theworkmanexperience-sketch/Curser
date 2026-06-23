"""
Regression guard for the run_stages() rewire (Rewire Plan).

The 'stages' engine (run() routed through core.stage.run_stages) must produce
the same result as the 'legacy' engine (direct stage-method calls). This locks
in behavioral equivalence so future stage changes can't silently diverge the
two paths.

Full end-to-end equivalence (incl. proxies + audit streams) is also validated
out-of-suite against synthetic 1080p footage; this in-suite test keeps it fast
(proxy disabled, no ffmpeg dependency).
"""

import os
import sys
import json
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("WECAPE_TEST_MODE", "1")
os.environ.setdefault("WECAPE_NONINTERACTIVE", "1")

from wecape.capture.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent.parent.parent
BASE_CFG = yaml.safe_load((ROOT / "wecape/config.yaml").read_text())


def _cfg(engine, tmp_path):
    c = json.loads(json.dumps(BASE_CFG))
    c.setdefault("pipeline", {})["engine"] = engine
    c["pipeline"]["file_operation"] = "symlink"
    c.setdefault("proxy_generation", {})["enabled"] = False
    p = tmp_path / f"cfg_{engine}.yaml"
    p.write_text(yaml.dump(c))
    return p


def _norm_tree(out, run_id):
    return sorted(
        str(p.relative_to(out)).replace(run_id, "RUNID")
        for p in out.rglob("*") if p.is_file()
    )


def _run(engine, tmp_path, src):
    out = tmp_path / f"out_{engine}"
    pipe = Pipeline(config_path=_cfg(engine, tmp_path))
    run_id = pipe.run_id
    summary = pipe.run(input_path=src, output_path=out)
    metrics = {k: summary.get(k) for k in
               ("files_ingested", "multicam_groups_formed",
                "variants_detected", "errors")}
    return metrics, _norm_tree(out, run_id)


def test_legacy_and_stages_engines_are_equivalent(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    for name in ["GX010001.MP4", "GX010002.MP4", "notes.txt"]:
        (src / name).write_bytes(b"\x00" * 32)

    m_legacy, tree_legacy = _run("legacy", tmp_path, src)
    m_stages, tree_stages = _run("stages", tmp_path, src)

    assert m_legacy == m_stages, f"metrics diverged: {m_legacy} vs {m_stages}"
    assert tree_legacy == tree_stages, (
        f"output tree diverged: {set(tree_legacy) ^ set(tree_stages)}"
    )
