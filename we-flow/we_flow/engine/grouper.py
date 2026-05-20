"""
W.E. FLOW / W.E. FORGE — Multicam Grouping Engine
Section 7: Grouping Rules (LOCKED)

Rules:
  - ONLY camera files are eligible
  - Minimum 2 camera SOURCES required (not just 2 files)
  - Grouping window: ±5 seconds (configurable)
  - Conflict resolution: closest timestamp proximity, then alphabetical filename
  - NO duplicate group membership
  - All logic is deterministic

⚠️  UNSPOKEN FLAW: The RFQ uses "±5 seconds from what?" ambiguously.
    This implementation anchors on the EARLIEST file in a candidate group.
    All other files must be within ±5s of that anchor.
    An alternative (centroid-based) window would produce different results.
    This choice is logged per group for auditability.

⚠️  UNSPOKEN FLAW: "Minimum 2 camera SOURCES" is different from "minimum 2 camera FILES."
    If a DJI drone shoots 3 clips and an iPhone shoots 1, that's 2 sources — valid.
    If you have 3 DJI clips and nothing else, that's 1 source — INVALID GROUP.
    This implementation enforces the stricter (source-count) interpretation.
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from .classifier import ClassifiedFile


@dataclass
class MulticamGroup:
    """A validated multicam group (Section 7)."""
    group_id: str
    files: list[ClassifiedFile]
    anchor_timestamp: float        # Timestamp of earliest file in group
    camera_sources: list[str]      # Distinct camera sources present
    timestamp_deltas: dict[str, float]  # {filename: delta_from_anchor}
    conflict_resolved: bool = False
    conflict_note: Optional[str] = None

    @property
    def file_count(self) -> int:
        return len(self.files)

    @property
    def source_count(self) -> int:
        return len(set(self.camera_sources))


@dataclass
class GroupingResult:
    groups: list[MulticamGroup] = field(default_factory=list)
    ungrouped: list[ClassifiedFile] = field(default_factory=list)  # Camera files with no valid group
    ungrouped_reasons: dict[str, str] = field(default_factory=dict)  # filename → reason


class MulticamGrouper:
    """
    Deterministic multicam grouping engine.
    Implements Section 7 grouping rules with full conflict handling.
    """

    def __init__(self, config: dict):
        grouping_cfg = config.get('grouping', {})
        self.window_seconds: float = grouping_cfg.get('window_seconds', 5.0)
        self.min_cameras: int = grouping_cfg.get('min_cameras', 2)
        self.group_id_prefix: str = config.get('output', {}).get('group_id_prefix', 'MCG')

    def group(self, camera_files: list[ClassifiedFile]) -> GroupingResult:
        """
        Main grouping entry point.
        Operates on camera files only. All files must have timestamps set.

        Algorithm:
        1. Sort all camera files by timestamp (deterministic ordering)
        2. For each ungrouped file, find all files within ±window_seconds
        3. If candidate group has ≥2 distinct sources → form group
        4. Assign files to the group where they have the smallest timestamp delta
           (conflict resolution per Section 7)
        5. Files that cannot form a valid group → ungrouped
        """
        result = GroupingResult()

        if not camera_files:
            return result

        # Validate all files have timestamps
        timestamped = []
        for f in camera_files:
            if f.timestamp is None:
                result.ungrouped.append(f)
                result.ungrouped_reasons[f.path.name] = "No resolvable timestamp"
            else:
                timestamped.append(f)

        if not timestamped:
            return result

        # Sort deterministically: primary = timestamp, secondary = filename (tiebreaker)
        # ⚠️  This is the tiebreaker the RFQ doesn't define — alphabetical filename
        sorted_files = sorted(timestamped, key=lambda f: (f.timestamp, f.path.name))

        # Build candidate groups using a greedy sweep
        assigned: set[str] = set()  # Track assigned file paths to prevent duplicates

        for anchor in sorted_files:
            anchor_key = str(anchor.path)
            if anchor_key in assigned:
                continue

            # Find all files within ±window of this anchor
            candidates = [
                f for f in sorted_files
                if str(f.path) not in assigned
                and abs(f.timestamp - anchor.timestamp) <= self.window_seconds
            ]

            # Check if we have ≥ min distinct camera sources
            sources_in_candidates = list({f.camera_source for f in candidates})

            if len(sources_in_candidates) < self.min_cameras:
                # Not enough distinct sources — skip (will be revisited or end up ungrouped)
                continue

            # Resolve conflicts: if any file in candidates could belong to multiple
            # potential groups, assign to the group where its delta is smallest.
            # Since we process anchors in timestamp order, this is guaranteed by the sweep.
            conflict_resolved = False
            conflict_note = None

            # Conflict resolution: a file closer to a DIFFERENT future anchor of a
            # DIFFERENT camera source is deferred to that anchor's group.
            # This prevents false deferrals when the "future anchor" is in the same
            # candidate pool (same shoot, different file from a third camera).
            borderline = []
            for f in candidates:
                if f is anchor:
                    continue
                future_anchors = [
                    a for a in sorted_files
                    if str(a.path) not in assigned
                    and a is not anchor
                    and a not in candidates          # must be outside this group
                    and a.camera_source != anchor.camera_source
                    and abs(f.timestamp - a.timestamp) <= self.window_seconds
                    and a.timestamp > anchor.timestamp
                ]
                if future_anchors:
                    best_delta = abs(f.timestamp - anchor.timestamp)
                    future_best = min(abs(f.timestamp - a.timestamp) for a in future_anchors)
                    if future_best < best_delta:
                        borderline.append(str(f.path))
                        conflict_resolved = True
                        conflict_note = (
                            f"{f.path.name} closer to a later anchor "
                            f"(delta {future_best:.2f}s vs {best_delta:.2f}s) — deferred"
                        )

            # Remove borderline files from this group; anchor always stays
            final_candidates = [f for f in candidates if str(f.path) not in borderline]
            # Ensure anchor is always included
            if anchor not in final_candidates:
                final_candidates.insert(0, anchor)
            final_sources = list({f.camera_source for f in final_candidates})

            if len(final_sources) < self.min_cameras:
                # After conflict resolution, not enough sources remain
                continue

            # Form the group
            group_id = self._new_group_id(final_candidates, anchor.timestamp)
            deltas = {
                f.path.name: round(f.timestamp - anchor.timestamp, 3)
                for f in final_candidates
            }

            group = MulticamGroup(
                group_id=group_id,
                files=final_candidates,
                anchor_timestamp=anchor.timestamp,
                camera_sources=final_sources,
                timestamp_deltas=deltas,
                conflict_resolved=conflict_resolved,
                conflict_note=conflict_note,
            )
            result.groups.append(group)

            for f in final_candidates:
                assigned.add(str(f.path))

        # Any unassigned camera files → ungrouped
        for f in sorted_files:
            if str(f.path) not in assigned:
                result.ungrouped.append(f)
                result.ungrouped_reasons[f.path.name] = (
                    "No valid multicam group: insufficient distinct camera sources "
                    f"within ±{self.window_seconds}s window"
                )

        return result

    def _new_group_id(self, files: list, anchor_ts: float) -> str:
        """
        Deterministic group ID: SHA-256 of sorted filenames + anchor timestamp.
        Same input always produces the same group_id — required for §17 Test 6.
        """
        import hashlib
        key = f"{anchor_ts:.3f}:" + ":".join(sorted(f.path.name for f in files))
        digest = hashlib.sha256(key.encode()).hexdigest()[:8].upper()
        return f"{self.group_id_prefix}_{digest}"
