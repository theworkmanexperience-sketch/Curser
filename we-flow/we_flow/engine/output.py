"""
W.E. FLOW / W.E. FORGE — Output Structure Builder
§10 Output Structure (LOCKED)

PROJECT/
  DATE/
    CAMERA/
      {source}/     ← per camera source
    CAMERA_AUDIO/   ← field recorders eligible for multicam association
    GENERIC/
    PROXIES/        ← Phase 1 only; created empty in Phase 0
    MULTICAM/
    OUTPUTS/
  REFERENCES/
  LOGS/

§11 Metadata schema (LOCKED):
  run_id, group_id, timestamp_start, timestamp_end,
  camera_sources, files, variants {parent, children}, classification

classification_note field added per §3.x edge case matrix.
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .classifier import ClassifiedFile
from .grouper import MulticamGroup, GroupingResult
from .variants import VariantGroup


class OutputBuilder:

    def __init__(self, config: dict, output_root: Path):
        self.config = config
        self.output_root = output_root
        self.file_op: str = config.get('pipeline', {}).get('file_operation', 'copy')
        self.date_fmt: str = config.get('output', {}).get('date_format', '%Y-%m-%d')
        self.generate_proxies: bool = config.get('proxies', {}).get('generate_proxies', False)

    def build(self, run_id: str, all_files: list[ClassifiedFile],
              grouping_result: GroupingResult,
              variant_groups: list[VariantGroup],
              standalone_files: list[ClassifiedFile]) -> dict:

        written: dict[str, list] = {
            'camera': [], 'camera_audio': [], 'generic': [],
            'reference': [], 'multicam': [],
        }

        for f in all_files:
            try:
                if f.classification == 'camera':
                    dest = self._camera_dest(f)
                    self._transfer(f.path, dest)
                    written['camera'].append(str(dest))
                elif f.classification == 'camera_audio':
                    dest = self._camera_audio_dest(f)
                    self._transfer(f.path, dest)
                    written['camera_audio'].append(str(dest))
                elif f.is_generic:
                    dest = self._generic_dest(f)
                    self._transfer(f.path, dest)
                    written['generic'].append(str(dest))
                elif f.is_reference:
                    dest = self._reference_dest(f)
                    self._transfer(f.path, dest)
                    written['reference'].append(str(dest))
            except Exception as e:
                pass  # Individual file errors don't halt pipeline (§13)

        # Multicam group metadata JSONs
        for group in grouping_result.groups:
            meta = self._group_meta(run_id, group)
            meta_path = self._multicam_meta_path(group)
            meta_path.parent.mkdir(parents=True, exist_ok=True)
            meta_path.write_text(json.dumps(meta, indent=2, default=str))
            written['multicam'].append(str(meta_path))

        # PROXIES/ — created empty per Phase 0 spec (§10.x LOCKED)
        # generate_proxies MUST be false in Phase 0
        if not self.generate_proxies:
            self._ensure_proxies_folders(all_files)

        # LOGS/ folder
        (self.output_root / 'LOGS').mkdir(parents=True, exist_ok=True)

        # Run index
        index = self._run_index(run_id, all_files, grouping_result, variant_groups)
        (self.output_root / f'{run_id}_index.json').write_text(
            json.dumps(index, indent=2, default=str)
        )

        return written

    # ------------------------------------------------------------------ #
    # Destination resolution                                               #
    # ------------------------------------------------------------------ #

    def _date_folder(self, f: ClassifiedFile) -> str:
        if f.timestamp:
            return datetime.fromtimestamp(f.timestamp, tz=timezone.utc).strftime(self.date_fmt)
        return 'UNDATED'

    def _camera_dest(self, f: ClassifiedFile) -> Path:
        d = self.output_root / self._date_folder(f) / 'CAMERA'
        if f.camera_source:
            d = d / f.camera_source
        d.mkdir(parents=True, exist_ok=True)
        return d / f.path.name          # deterministic: always source filename

    def _camera_audio_dest(self, f: ClassifiedFile) -> Path:
        d = self.output_root / self._date_folder(f) / 'CAMERA_AUDIO'
        d.mkdir(parents=True, exist_ok=True)
        return d / f.path.name

    def _generic_dest(self, f: ClassifiedFile) -> Path:
        d = self.output_root / self._date_folder(f) / 'GENERIC'
        d.mkdir(parents=True, exist_ok=True)
        return d / f.path.name

    def _reference_dest(self, f: ClassifiedFile) -> Path:
        d = self.output_root / 'REFERENCES'
        d.mkdir(parents=True, exist_ok=True)
        return d / f.path.name

    def _multicam_meta_path(self, group: MulticamGroup) -> Path:
        date = (datetime.fromtimestamp(group.anchor_timestamp, tz=timezone.utc)
                .strftime(self.date_fmt)) if group.files else 'UNDATED'
        return self.output_root / date / 'MULTICAM' / f'{group.group_id}.json'

    def _ensure_proxies_folders(self, all_files: list[ClassifiedFile]):
        """Create PROXIES/ folder structure (Phase 1 reserved, empty in Phase 0)."""
        dates = {self._date_folder(f) for f in all_files}
        for date in dates:
            (self.output_root / date / 'PROXIES').mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # §11 Metadata builders                                                #
    # ------------------------------------------------------------------ #

    def _group_meta(self, run_id: str, group: MulticamGroup) -> dict:
        files_data = []
        for f in group.files:
            files_data.append({
                'filename': f.path.name,
                'path': str(f.path),
                'camera_source': f.camera_source,
                'timestamp_unix': f.timestamp,
                'timestamp_delta_seconds': group.timestamp_deltas.get(f.path.name, 0),
                'timestamp_confidence': f.timestamp_confidence,
                'file_size_bytes': f.file_size,
                'file_hash_sha256': f.file_hash,
                'classification': f.classification,
                'classification_note': f.classification_note,
            })
        return {
            'run_id': run_id,
            'group_id': group.group_id,
            'timestamp_start': group.anchor_timestamp,
            'timestamp_end': max((f.timestamp or group.anchor_timestamp for f in group.files)),
            'camera_sources': list(set(group.camera_sources)),
            'files': files_data,
            'variants': {'parent': '', 'children': []},  # §11 locked schema
            'classification': 'camera',
            'conflict_resolved': group.conflict_resolved,
            'conflict_note': group.conflict_note,
        }

    def _run_index(self, run_id: str, all_files: list[ClassifiedFile],
                   grouping_result: GroupingResult,
                   variant_groups: list[VariantGroup]) -> dict:
        return {
            'run_id': run_id,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'totals': {
                'files_ingested': len(all_files),
                'camera_files': sum(1 for f in all_files if f.classification == 'camera'),
                'camera_audio_files': sum(1 for f in all_files if f.classification == 'camera_audio'),
                'generic_files': sum(1 for f in all_files if f.is_generic),
                'reference_files': sum(1 for f in all_files if f.is_reference),
                'multicam_groups': len(grouping_result.groups),
                'ungrouped_camera_files': len(grouping_result.ungrouped),
                'variant_groups': len(variant_groups),
            },
            'multicam_groups': [
                {'group_id': g.group_id, 'file_count': g.file_count,
                 'sources': list(set(g.camera_sources)), 'anchor_timestamp': g.anchor_timestamp}
                for g in grouping_result.groups
            ],
            'variants': [vg.to_metadata_dict() for vg in variant_groups],
            'ungrouped_camera_files': [
                {'file': str(f.path),
                 'reason': grouping_result.ungrouped_reasons.get(f.path.name, 'Unknown')}
                for f in grouping_result.ungrouped
            ],
        }

    # ------------------------------------------------------------------ #
    # File operations                                                      #
    # ------------------------------------------------------------------ #

    def _transfer(self, src: Path, dest: Path):
        if dest.exists():
            return  # Idempotent — skip existing outputs (§17 Test 6)
        if self.file_op == 'copy':
            shutil.copy2(src, dest)
        elif self.file_op == 'move':
            shutil.move(str(src), dest)
        elif self.file_op == 'symlink':
            dest.symlink_to(src.resolve())
        else:
            raise ValueError(f'Unknown file_operation: {self.file_op!r}')

    @staticmethod
    def _safe_dest(directory: Path, filename: str) -> Path:
        dest = directory / filename
        if not dest.exists():
            return dest
        stem, ext = Path(filename).stem, Path(filename).suffix
        counter = 1
        while dest.exists():
            dest = directory / f'{stem}_{counter}{ext}'
            counter += 1
        return dest
