"""
W.E. C.A.P.E. CAPTURE / W.E. C.A.P.E. — Variant Detection Engine
§8 Variant Rules (LOCKED) + §9 Parent File Selection

Orphan variant rule (§3.x Edge Case Matrix, Option B — LOCKED):
  Variant pattern detected, no matching base file →
  Reclassify as standalone. Do NOT populate variants object.
  Log: classification_note = "variant_pattern_no_base_found"

Parent selection (§9):
  largest_file | lowest_index | earliest_timestamp
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .classifier import ClassifiedFile


@dataclass
class VariantGroup:
    parent: ClassifiedFile
    children: list[ClassifiedFile] = field(default_factory=list)
    parent_selection_method: str = ''

    @property
    def all_files(self) -> list[ClassifiedFile]:
        return [self.parent] + self.children

    def to_metadata_dict(self) -> dict:
        return {
            "parent": str(self.parent.path),
            "children": [str(c.path) for c in self.children],
            "parent_selection_method": self.parent_selection_method,
        }


class VariantDetector:

    def __init__(self, config: dict):
        v = config.get('variant_detection', {})
        self.parent_selection: str = v.get('parent_selection', 'largest_file')
        self._indexed_re = re.compile(
            v.get('indexed_pattern', r'[\(\[](\d+)[\)\]]'), re.IGNORECASE
        )
        self._suffix_patterns = [
            re.compile(p, re.IGNORECASE) for p in v.get('suffix_patterns', ['_v\\d+', '_edit', '_final'])
        ]
        self._duplicate_keywords = [kw.lower() for kw in v.get('duplicate_keywords', ['copy', 'final', 'backup'])]

    def detect(self, files: list[ClassifiedFile]) -> tuple[list[VariantGroup], list[ClassifiedFile]]:
        if not files:
            return [], []

        base_stems = {f.path: self._base_stem(f.path.stem) for f in files}

        # Group by (base_stem, extension, parent_directory)
        buckets: dict[tuple, list[ClassifiedFile]] = {}
        for f in files:
            key = (base_stems[f.path], f.path.suffix.lower(), f.path.parent)
            buckets.setdefault(key, []).append(f)

        variant_groups: list[VariantGroup] = []
        standalone: list[ClassifiedFile] = []

        for key, group in buckets.items():
            if len(group) == 1:
                file = group[0]
                # Orphan variant check: single file that looks like a variant but has no siblings
                if self._looks_like_variant(file.path.stem):
                    # §3.x Option B: reclassify as standalone, log note
                    file.classification_note = 'variant_pattern_no_base_found'
                standalone.append(file)
                continue

            parent = self._select_parent(group)
            children = [f for f in group if f.path != parent.path]
            variant_groups.append(VariantGroup(
                parent=parent, children=children,
                parent_selection_method=self.parent_selection,
            ))

        return variant_groups, standalone

    def _looks_like_variant(self, stem: str) -> bool:
        if self._indexed_re.search(stem):
            return True
        for p in self._suffix_patterns:
            if p.search(stem):
                return True
        stem_lower = stem.lower()
        return any(kw in stem_lower for kw in self._duplicate_keywords)

    def _base_stem(self, stem: str) -> str:
        result = self._indexed_re.sub('', stem).strip()
        for pattern in self._suffix_patterns:
            result = pattern.sub('', result).strip()
        for kw in self._duplicate_keywords:
            result = re.sub(
                r'[\s_\-]?' + re.escape(kw) + r'[\s_\-\d]*$', '',
                result, flags=re.IGNORECASE,
            ).strip()
        result = result.rstrip(' _-').strip()
        return result.lower() if result else stem.lower()

    def _select_parent(self, files: list[ClassifiedFile]) -> ClassifiedFile:
        if self.parent_selection == 'largest_file':
            return max(files, key=lambda f: (f.file_size, f.path.name))
        elif self.parent_selection == 'lowest_index':
            return min(files, key=lambda f: (self._extract_index(f.path.stem), f.path.name))
        elif self.parent_selection == 'earliest_timestamp':
            timestamped = [f for f in files if f.timestamp is not None]
            if timestamped:
                return min(timestamped, key=lambda f: (f.timestamp, f.path.name))
            return min(files, key=lambda f: f.path.name)
        return max(files, key=lambda f: (f.file_size, f.path.name))

    def _extract_index(self, stem: str) -> int:
        m = self._indexed_re.search(stem)
        if m:
            return int(m.group(1))
        for p in self._suffix_patterns:
            m = p.search(stem)
            if m:
                nums = re.findall(r'\d+', m.group(0))
                if nums:
                    return int(nums[0])
        return 0
