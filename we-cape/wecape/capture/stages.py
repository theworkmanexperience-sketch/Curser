"""
wecape.capture.stages
======================
PipelineStage-conforming adapters for the W.E. C.A.P.E. CAPTURE components.

These make the PipelineStage contract real: every capture step is exposed as an
instantiable PipelineStage with validate_input / execute / on_error and a
mandatory registry write (via the base class). They are the surface that becomes
the public extension API at J3 — and the identical shape the internal AI stages
(J1–J5) will implement.

Inter-stage data travels through StageContext.metadata under documented keys:

    source_files -> list[Path]            (ingest output;  ClassifyStage input)
    classified   -> list[ClassifiedFile]  (ClassifyStage output)
    groups       -> GroupingResult        (GroupStage output)
    variants     -> (groups, orphans)     (VariantStage output)
    sha_map      -> dict[Path, str]       (content hashes;  ProxyStage input)

Drive them with wecape.core.stage.run_stages(stages, context).

NOTE (honest boundary): the production Pipeline in pipeline.py still calls these
components directly today. These adapters + run_stages() are the seam the
pipeline migrates onto incrementally; doing so is tracked, not yet done. The
contract is real and tested now (tests/test_pipeline_stages.py); the internal
rewire is the next step. Until then, treat pipeline.py as the source of truth
for production behavior and these adapters as the canonical stage interface.
"""

from pathlib import Path

from ..core.stage import PipelineStage, StageResult, ValidationResult
from .classifier import FileClassifier
from .grouper import MulticamGrouper
from .variants import VariantDetector
from .proxy import ProxyGenerator


class ClassifyStage(PipelineStage):
    stage_id = "classify"
    stage_version = "1.0.0"
    stage_description = "Classify files: camera | camera_audio | generic | reference (§6)"

    def validate_input(self, context) -> ValidationResult:
        if not context.metadata.get("source_files"):
            return ValidationResult(False, ["ClassifyStage requires 'source_files' in context.metadata"])
        return ValidationResult(True)

    def execute(self, context) -> StageResult:
        files = list(context.metadata["source_files"])
        classified = FileClassifier(context.profile).classify_batch(files)
        context.metadata["classified"] = classified
        return StageResult(
            self.stage_id, self.stage_version, True,
            files_processed=len(classified),
            metadata={"camera": sum(1 for f in classified if f.is_camera)},
        )

    def on_error(self, error, context) -> dict:
        return {"stage": self.stage_id, "error": str(error),
                "resolution": "Verify source_files are readable media paths."}


class GroupStage(PipelineStage):
    stage_id = "group"
    stage_version = "1.0.0"
    stage_description = "Deterministic multicam grouping (§7)"

    def validate_input(self, context) -> ValidationResult:
        if context.metadata.get("classified") is None:
            return ValidationResult(False, ["GroupStage requires 'classified' (run ClassifyStage first)"])
        return ValidationResult(True)

    def execute(self, context) -> StageResult:
        classified = context.metadata["classified"]
        camera = [f for f in classified if f.is_camera]
        result = MulticamGrouper(context.profile).group(camera)
        context.metadata["groups"] = result
        return StageResult(
            self.stage_id, self.stage_version, True,
            files_processed=len(camera),
            metadata={"groups": len(result.groups), "ungrouped": len(result.ungrouped)},
        )

    def on_error(self, error, context) -> dict:
        return {"stage": self.stage_id, "error": str(error),
                "resolution": "Check grouping.window_seconds and that timestamps were extracted."}


class VariantStage(PipelineStage):
    stage_id = "variants"
    stage_version = "1.0.0"
    stage_description = "Parent-child variant detection, orphan -> standalone (§8)"

    def validate_input(self, context) -> ValidationResult:
        if context.metadata.get("classified") is None:
            return ValidationResult(False, ["VariantStage requires 'classified'"])
        return ValidationResult(True)

    def execute(self, context) -> StageResult:
        classified = context.metadata["classified"]
        groups, orphans = VariantDetector(context.profile).detect(classified)
        context.metadata["variants"] = (groups, orphans)
        return StageResult(
            self.stage_id, self.stage_version, True,
            files_processed=len(classified),
            metadata={"variant_groups": len(groups), "orphans": len(orphans)},
        )

    def on_error(self, error, context) -> dict:
        return {"stage": self.stage_id, "error": str(error),
                "resolution": "Review variant_detection patterns in config."}


class ProxyStage(PipelineStage):
    stage_id = "proxy"
    stage_version = "1.0.0"
    stage_description = "Proxy transcoding via ffmpeg (Stage 6)"

    def validate_input(self, context) -> ValidationResult:
        if context.metadata.get("classified") is None:
            return ValidationResult(False, ["ProxyStage requires 'classified'"])
        return ValidationResult(True)

    def execute(self, context) -> StageResult:
        classified = context.metadata["classified"]
        pg = ProxyGenerator(context.profile)
        if not pg.enabled:
            return StageResult(
                self.stage_id, self.stage_version, True,
                files_skipped=len(classified), metadata={"enabled": False},
            )
        out = Path(context.output_path)
        tmp = out / ".wecape_tmp"
        tmp.mkdir(parents=True, exist_ok=True)
        sha_map = context.metadata.get("sha_map", {})
        stats = pg.generate(classified, out, tmp, sha_map)
        return StageResult(
            self.stage_id, self.stage_version,
            success=stats.get("failed", 0) == 0,
            files_processed=stats.get("transcoded", 0),
            files_skipped=stats.get("skipped", 0),
            files_failed=stats.get("failed", 0),
            metadata={"eligible": stats.get("eligible", 0)},
        )

    def on_error(self, error, context) -> dict:
        return {"stage": self.stage_id, "error": str(error),
                "resolution": "Ensure ffmpeg/ffprobe are installed (see Measure 1)."}


class ArchiveStage(PipelineStage):
    stage_id = "archive"
    stage_version = "1.0.0"
    stage_description = "Stage 0.5 — archive & compression intelligence"

    def validate_input(self, context) -> ValidationResult:
        if context.metadata.get("source_files") is None:
            return ValidationResult(False, ["ArchiveStage requires 'source_files'"])
        return ValidationResult(True)

    def execute(self, context) -> StageResult:
        from ..archive.stage import ArchiveIntelligenceStage
        raw = list(context.metadata["source_files"])
        out = Path(context.output_path)
        engine = ArchiveIntelligenceStage(context.profile, out)
        files, result = engine.process(raw, context.run_id, out / "LOGS")
        # Extracted/normalized file set flows downstream.
        context.metadata["source_files"] = files
        return StageResult(
            self.stage_id, self.stage_version, True,
            files_processed=getattr(result, "files_scanned", len(raw)),
            metadata={"archives_detected": getattr(result, "archives_detected", 0)},
        )

    def on_error(self, error, context) -> dict:
        return {"stage": self.stage_id, "error": str(error),
                "resolution": "Inspect quarantine output and archive_engine config."}


# Built-in extension surface (J3): ordered, discoverable, swappable.
BUILTIN_STAGES = [ArchiveStage, ClassifyStage, GroupStage, VariantStage, ProxyStage]
STAGE_REGISTRY = {cls.stage_id: cls for cls in BUILTIN_STAGES}
