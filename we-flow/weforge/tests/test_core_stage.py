"""Tests for weforge.core.stage — PipelineStage interface."""

import pytest
from datetime import datetime
from weforge.core.stage import (
    PipelineStage, StageContext, StageResult, ValidationResult
)


class MockStage(PipelineStage):
    """Minimal concrete implementation for testing."""
    stage_id = "mock"
    stage_version = "1.0.0"
    stage_description = "Test stage"

    def validate_input(self, context):
        return ValidationResult(valid=True)

    def execute(self, context):
        return StageResult(
            stage_id=self.stage_id,
            stage_version=self.stage_version,
            success=True,
            files_processed=5,
        )

    def on_error(self, error, context):
        return {"message": str(error), "resolution": "check input"}


class MockRegistryWriter:
    def __init__(self):
        self.calls = []

    def write_stage_result(self, run_id, stage_id, result):
        self.calls.append((run_id, stage_id, result))


def make_context(registry_writer=None):
    return StageContext(
        run_id="run-test-001",
        source_path="/source",
        output_path="/output",
        profile={},
        registry_writer=registry_writer or MockRegistryWriter(),
        sync_adapter=None,
        timestamp=datetime.utcnow(),
    )


def test_stage_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        PipelineStage()


def test_mock_stage_validate_returns_valid():
    stage = MockStage()
    ctx = make_context()
    result = stage.validate_input(ctx)
    assert result.valid is True
    assert result.errors == []


def test_mock_stage_execute_returns_result():
    stage = MockStage()
    ctx = make_context()
    result = stage.execute(ctx)
    assert result.success is True
    assert result.files_processed == 5
    assert result.stage_id == "mock"


def test_write_registry_calls_writer():
    writer = MockRegistryWriter()
    stage = MockStage()
    ctx = make_context(registry_writer=writer)
    result = stage.execute(ctx)
    stage.write_registry(result, ctx)
    assert len(writer.calls) == 1
    assert writer.calls[0][0] == "run-test-001"
    assert writer.calls[0][1] == "mock"


def test_write_registry_no_error_when_writer_is_none():
    stage = MockStage()
    ctx = make_context(registry_writer=None)
    result = stage.execute(ctx)
    stage.write_registry(result, ctx)  # should not raise


def test_on_error_returns_dict():
    stage = MockStage()
    ctx = make_context()
    resolution = stage.on_error(ValueError("bad input"), ctx)
    assert isinstance(resolution, dict)
    assert "message" in resolution
    assert "resolution" in resolution


def test_stage_result_defaults():
    result = StageResult(
        stage_id="test",
        stage_version="1.0.0",
        success=True,
    )
    assert result.files_processed == 0
    assert result.files_skipped == 0
    assert result.files_failed == 0
    assert result.errors == []
    assert result.diagnostics == []
    assert result.metadata == {}
