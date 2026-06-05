"""
weforge.core.manifest
=====================
RunManifest — single source of truth for a completed pipeline run.

Three output formats, zero data duplication:
  to_json()   → Machine-readable. Registry, sync, API, developer tools.
  to_html()   → Human-readable. UI dashboard, audit report.
  to_fcpxml() → Final Cut Pro XML. v1: stub. Implemented at J4.
  to_drxml()  → DaVinci Resolve XML. v1: stub. Implemented at J4.

Design principle (P3 Auditability):
  Every pipeline run produces a complete manifest documenting every
  decision, every file processed, every error encountered, and every
  stage result. Manifests are permanent and append-only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

WEFORGE_VERSION = "1.0.0"


@dataclass
class ContentRecord:
    """Represents a single processed file in the manifest."""
    filename: str
    original_path: str
    content_id: str
    camera_family: Optional[str] = None
    camera_id: Optional[str] = None
    shoot_date: Optional[str] = None
    duration_sec: Optional[float] = None
    codec: Optional[str] = None
    resolution: Optional[str] = None
    file_size_bytes: Optional[int] = None
    scaffold_path: Optional[str] = None
    proxy_path: Optional[str] = None
    content_type: str = "original"
    metadata: dict = field(default_factory=dict)


@dataclass
class StageRecord:
    """Summary of a single stage's execution."""
    stage_id: str
    stage_version: str
    success: bool
    files_processed: int = 0
    files_skipped: int = 0
    files_failed: int = 0
    duration_sec: float = 0.0
    errors: list = field(default_factory=list)
    diagnostics: list = field(default_factory=list)


@dataclass
class RunManifest:
    """
    Complete record of a W.E. FORGE pipeline run.
    Built at run completion. Written to registry and disk.
    """
    run_id: str
    source_path: str
    output_path: str
    profile_id: Optional[str]
    started_at: str
    completed_at: str
    runtime_sec: float
    we_forge_version: str = WEFORGE_VERSION

    # Content
    content: list[ContentRecord] = field(default_factory=list)
    stage_records: list[StageRecord] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    diagnostics: list[dict] = field(default_factory=list)

    # Intelligence results — populated at respective junctures
    quality_summary: Optional[dict] = None    # J2
    alignment_summary: Optional[dict] = None  # J3
    highlight_summary: Optional[dict] = None  # J4

    # ------------------------------------------------------------------ #
    # Computed properties                                                  #
    # ------------------------------------------------------------------ #

    @property
    def total_files(self) -> int:
        return len(self.content)

    @property
    def proxied_files(self) -> int:
        return sum(1 for c in self.content if c.proxy_path)

    @property
    def total_duration_sec(self) -> float:
        return sum(c.duration_sec or 0.0 for c in self.content)

    @property
    def camera_families(self) -> list[str]:
        return sorted(set(
            c.camera_family for c in self.content if c.camera_family
        ))

    @property
    def shoot_dates(self) -> list[str]:
        return sorted(set(
            c.shoot_date for c in self.content if c.shoot_date
        ))

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    # ------------------------------------------------------------------ #
    # Output formats                                                       #
    # ------------------------------------------------------------------ #

    def to_json(self) -> dict:
        """
        Machine-readable. Used by registry, sync, and API.
        This is the canonical representation of the run.
        """
        return {
            "schema_version": "1.0",
            "platform": "W.E. FORGE",
            "weforge_version": self.we_forge_version,
            "run": {
                "id": self.run_id,
                "profile_id": self.profile_id,
                "source_path": self.source_path,
                "output_path": self.output_path,
                "started_at": self.started_at,
                "completed_at": self.completed_at,
                "runtime_sec": round(self.runtime_sec, 2),
            },
            "statistics": {
                "total_files": self.total_files,
                "proxied_files": self.proxied_files,
                "total_duration_sec": round(self.total_duration_sec, 2),
                "camera_families": self.camera_families,
                "shoot_dates": self.shoot_dates,
                "error_count": self.error_count,
            },
            "stages": [
                {
                    "stage_id": s.stage_id,
                    "stage_version": s.stage_version,
                    "success": s.success,
                    "files_processed": s.files_processed,
                    "files_skipped": s.files_skipped,
                    "files_failed": s.files_failed,
                    "duration_sec": round(s.duration_sec, 2),
                    "errors": s.errors,
                    "diagnostics": s.diagnostics,
                }
                for s in self.stage_records
            ],
            "content": [
                {
                    "id": c.content_id,
                    "filename": c.filename,
                    "original_path": c.original_path,
                    "scaffold_path": c.scaffold_path,
                    "proxy_path": c.proxy_path,
                    "camera_family": c.camera_family,
                    "camera_id": c.camera_id,
                    "shoot_date": c.shoot_date,
                    "duration_sec": c.duration_sec,
                    "codec": c.codec,
                    "resolution": c.resolution,
                    "file_size_bytes": c.file_size_bytes,
                    "content_type": c.content_type,
                }
                for c in self.content
            ],
            "errors": self.errors,
            "diagnostics": self.diagnostics,
            "intelligence": {
                "quality": self.quality_summary,
                "alignment": self.alignment_summary,
                "highlights": self.highlight_summary,
            },
        }

    def to_json_str(self, indent: int = 2) -> str:
        """JSON string representation."""
        return json.dumps(self.to_json(), indent=indent, default=str)

    def to_html(self) -> str:
        """
        Human-readable audit report.
        Rendered in the UI dashboard and written as a .html file.
        """
        status_color = "#2d6a4f" if not self.has_errors else "#c1121f"
        status_label = "COMPLETED" if not self.has_errors else f"COMPLETED WITH {self.error_count} ERROR(S)"

        hours = int(self.runtime_sec // 3600)
        minutes = int((self.runtime_sec % 3600) // 60)
        seconds = int(self.runtime_sec % 60)
        runtime_str = f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"

        stage_rows = "".join(
            f"""
            <tr>
                <td>{s.stage_id}</td>
                <td style="color:{'#2d6a4f' if s.success else '#c1121f'}">
                    {'✓' if s.success else '✗'}
                </td>
                <td>{s.files_processed}</td>
                <td>{s.files_skipped}</td>
                <td>{s.files_failed}</td>
                <td>{round(s.duration_sec, 1)}s</td>
            </tr>"""
            for s in self.stage_records
        )

        error_section = ""
        if self.errors:
            error_rows = "".join(
                f"<li><code>{json.dumps(e, default=str)}</code></li>"
                for e in self.errors
            )
            error_section = f"<h2>Errors</h2><ul>{error_rows}</ul>"

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>W.E. FORGE — Run Report {self.run_id}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         max-width: 900px; margin: 40px auto; padding: 0 20px; color: #1a1a2e; }}
  h1 {{ font-size: 1.4rem; margin-bottom: 4px; }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px;
            color: white; background: {status_color}; font-size: 0.85rem; }}
  .meta {{ color: #666; font-size: 0.9rem; margin: 12px 0 24px; }}
  .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 24px 0; }}
  .stat {{ background: #f8f9fa; border-radius: 8px; padding: 16px; text-align: center; }}
  .stat-value {{ font-size: 2rem; font-weight: 700; color: #1a1a2e; }}
  .stat-label {{ font-size: 0.75rem; color: #666; text-transform: uppercase; }}
  table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
  th {{ background: #1a1a2e; color: white; padding: 8px 12px; text-align: left;
        font-size: 0.8rem; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #eee; font-size: 0.85rem; }}
  h2 {{ font-size: 1.1rem; margin: 32px 0 8px; border-bottom: 2px solid #eee; padding-bottom: 6px; }}
  code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.8rem; }}
  .footer {{ color: #aaa; font-size: 0.75rem; margin-top: 48px; text-align: center; }}
</style>
</head>
<body>
<h1>W.E. FORGE — Run Report</h1>
<span class="badge">{status_label}</span>
<div class="meta">
  Run ID: <code>{self.run_id}</code> &nbsp;|&nbsp;
  Profile: <code>{self.profile_id or 'default'}</code> &nbsp;|&nbsp;
  Runtime: {runtime_str} &nbsp;|&nbsp;
  {self.completed_at[:19].replace('T', ' ')} UTC
</div>

<div class="stats">
  <div class="stat">
    <div class="stat-value">{self.total_files}</div>
    <div class="stat-label">Files Processed</div>
  </div>
  <div class="stat">
    <div class="stat-value">{self.proxied_files}</div>
    <div class="stat-label">Proxies Generated</div>
  </div>
  <div class="stat">
    <div class="stat-value">{len(self.camera_families)}</div>
    <div class="stat-label">Camera Families</div>
  </div>
  <div class="stat">
    <div class="stat-value">{self.error_count}</div>
    <div class="stat-label">Errors</div>
  </div>
</div>

<h2>Source</h2>
<p><code>{self.source_path}</code> → <code>{self.output_path}</code></p>
<p>Cameras: {', '.join(self.camera_families) or 'unknown'} &nbsp;|&nbsp;
   Shoot dates: {', '.join(self.shoot_dates) or 'unknown'}</p>

<h2>Pipeline Stages</h2>
<table>
  <thead>
    <tr><th>Stage</th><th>Status</th><th>Processed</th>
        <th>Skipped</th><th>Failed</th><th>Duration</th></tr>
  </thead>
  <tbody>{stage_rows}</tbody>
</table>

{error_section}

<div class="footer">
  Generated by W.E. FORGE {self.we_forge_version} &nbsp;|&nbsp;
  W.E. FLOW — The Production Intelligence Platform
</div>
</body>
</html>"""

    def to_fcpxml(self) -> str:
        """
        Final Cut Pro XML.
        v1: Stub — interface exists, implementation at J4.
        J4: Imports scaffold as organized event with proxy references.
        """
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE fcpxml>\n'
            f'<!-- W.E. FORGE {self.we_forge_version} | Run: {self.run_id} -->\n'
            '<!-- FCPXML output: implemented at J4 (Editorial Intelligence) -->\n'
            '<fcpxml version="1.11">\n'
            '  <resources/>\n'
            '  <library/>\n'
            '</fcpxml>'
        )

    def to_drxml(self) -> str:
        """
        DaVinci Resolve XML.
        v1: Stub — interface exists, implementation at J4.
        """
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<!-- W.E. FORGE {self.we_forge_version} | Run: {self.run_id} -->\n'
            '<!-- DaVinci Resolve XML: implemented at J4 (Editorial Intelligence) -->\n'
            '<xmeml version="5">\n'
            '  <sequence/>\n'
            '</xmeml>'
        )

    # ------------------------------------------------------------------ #
    # Factory                                                              #
    # ------------------------------------------------------------------ #

    @classmethod
    def create(
        cls,
        run_id: str,
        source_path: str,
        output_path: str,
        started_at: datetime,
        profile_id: Optional[str] = None,
    ) -> "RunManifest":
        """Create a new manifest at run start."""
        now = datetime.now(timezone.utc)
        return cls(
            run_id=run_id,
            source_path=source_path,
            output_path=output_path,
            profile_id=profile_id,
            started_at=started_at.isoformat(),
            completed_at=now.isoformat(),
            runtime_sec=(now - started_at).total_seconds(),
        )
