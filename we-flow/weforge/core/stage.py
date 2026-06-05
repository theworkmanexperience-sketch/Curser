"""
weforge.core.stage
==================
PipelineStage — the abstract interface every W.E. FORGE stage implements.

This is the internal seam that becomes the public extension API at J3.
Third-party plugins and internal AI stages implement identical interfaces.

Rules (enforced by convention, tested by CI):
  - Stages NEVER import from other stages
  - Stages write to registry via context.registry_writer ONLY
  - Stages NEVER make network calls
  - Stages must be idempotent
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class StageContext:
    """Passed between stages. Immutable per run."""
    run_id: str
    source_path: str
    output_path: str
    profile: dict
    registry_writer: object   # injected — never imported directly
    sync_adapter: object      # injected — LocalOnly by default
    timestamp: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class ValidationResult:
    valid: bool
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


@dataclass
class StageResult:
    """Returned by every stage execute() call."""
    stage_id: str
    stage_version: str
    success: bool
    files_processed: int = 0
    files_skipped: int = 0
    files_failed: int = 0
    duration_sec: float = 0.0
    errors: list = field(default_factory=list)
    diagnostics: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class PipelineStage(ABC):
    """
    Base interface for every W.E. FORGE pipeline stage.

    This interface is the internal seam that becomes the public
    extension API at J3. Third-party plugins and internal AI stages
    implement identical interfaces.
    """

    stage_id: str = ""
    stage_version: str = "0.0.0"
    stage_description: str = ""

    @abstractmethod
    def validate_input(self, context: StageContext) -> ValidationResult:
        """
        Pre-flight check. Called before execute().
        Must not modify any files or state.
        """
        pass

    @abstractmethod
    def execute(self, context: StageContext) -> StageResult:
        """
        Core processing logic.
        Must write results to registry before returning.
        Must be idempotent — safe to re-run on same input.
        """
        pass

    @abstractmethod
    def on_error(self, error: Exception, context: StageContext) -> dict:
        """
        Error handler. Returns user-facing resolution guidance.
        Must never raise — always returns a resolution dict.
        """
        pass

    def write_registry(self, result: StageResult, context: StageContext) -> None:
        """
        Persist stage results to local registry.
        Not overrideable — registry writes are mandatory.
        """
        if hasattr(context, 'registry_writer') and context.registry_writer:
            context.registry_writer.write_stage_result(
                run_id=context.run_id,
                stage_id=self.stage_id,
                result=result
            )
