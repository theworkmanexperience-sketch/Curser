"""
Tests for the PipelineStage seam (CODEBASE_AUDIT_2026-06-23 finding #1).

Proves the contract is real: the built-in capture stages actually implement
PipelineStage (instantiable -> no missing abstract methods), the run_stages
driver validates/executes/persists/halts correctly, and registry writes are
mandatory per stage.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.core.stage import StageContext, PipelineStage, run_stages
from wecape.core.sync import LocalOnlySyncAdapter
from wecape.capture.stages import (
    STAGE_REGISTRY, ClassifyStage, GroupStage,
)


class FakeWriter:
    """Captures write_stage_result calls to prove the mandatory registry write."""
    def __init__(self):
        self.calls = []

    def write_stage_result(self, run_id, stage_id, result):
        self.calls.append((run_id, stage_id, result))


def _ctx(tmp_path, source_files, writer):
    return StageContext(
        run_id="RUN1",
        source_path=str(tmp_path),
        output_path=str(tmp_path / "out"),
        profile={},
        registry_writer=writer,
        sync_adapter=LocalOnlySyncAdapter(),
        timestamp=datetime.utcnow(),
        metadata={"source_files": list(source_files)},
    )


def test_all_builtin_stages_actually_implement_the_contract(tmp_path):
    for stage_id, cls in STAGE_REGISTRY.items():
        assert issubclass(cls, PipelineStage)
        instance = cls()  # raises TypeError if any abstract method is missing
        assert instance.stage_id == stage_id
        assert instance.stage_version


def test_classify_then_group_chain_runs_and_writes_registry(tmp_path):
    files = []
    for name in ["GX010001.MP4", "GX010002.MP4", "notes.txt"]:
        p = tmp_path / name
        p.write_bytes(b"\x00" * 16)
        files.append(p)

    writer = FakeWriter()
    ctx = _ctx(tmp_path, files, writer)
    results = run_stages([ClassifyStage(), GroupStage()], ctx)

    assert len(results) == 2
    assert all(r.success for r in results), [r.errors for r in results]
    assert results[0].files_processed == 3          # all files classified
    assert "classified" in ctx.metadata
    assert "groups" in ctx.metadata
    # Mandatory registry write fired once per stage, in order.
    assert [c[1] for c in writer.calls] == ["classify", "group"]


def test_validation_failure_halts_chain(tmp_path):
    writer = FakeWriter()
    ctx = _ctx(tmp_path, [], writer)
    ctx.metadata.pop("classified", None)
    # GroupStage first, with no 'classified' -> must fail and stop the chain.
    results = run_stages([GroupStage(), ClassifyStage()], ctx)
    assert len(results) == 1
    assert results[0].success is False
    assert results[0].errors


def test_on_error_returns_resolution_dict():
    guidance = ClassifyStage().on_error(ValueError("boom"), None)
    assert isinstance(guidance, dict)
    assert "resolution" in guidance
