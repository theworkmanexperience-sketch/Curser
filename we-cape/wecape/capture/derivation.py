"""
wecape.capture.derivation
=========================
Derivation lineage — records that a curated *select* derives from a *source*
clip, WITHOUT the duplicate/redundancy semantics of variant detection (§8).

A select is named ``<source_stem><suffix>`` — e.g. ``VID_..._006_sel01.mp4``
derives from ``VID_..._006``. The suffix (default ``_sel<NN>``) lives OUTSIDE the
reserved variant patterns, so selects stay standalone, but their provenance is
captured in the registry (``content.source_clip`` / ``source_clip_sha``) for
querying and for W.E. ARCHIVE (J5).

This is additive metadata only — it never alters classification, grouping, or
variant detection, and is a safe no-op for files that don't match the pattern.
"""

import re
from pathlib import Path
from typing import Optional, Iterable, Tuple

DEFAULT_SELECT_PATTERN = r"_sel\d+"


class DerivationResolver:
    """Resolves a select filename to (source_stem, source_sha)."""

    def __init__(self, select_pattern: str = DEFAULT_SELECT_PATTERN, enabled: bool = True):
        self.enabled = bool(enabled)
        self._re = (
            re.compile(f"(?:{select_pattern})$", re.IGNORECASE)
            if (enabled and select_pattern) else None
        )
        self._stem_to_sha: dict = {}

    def index_sources(self, stem_sha_pairs: Iterable[Tuple[str, Optional[str]]]) -> None:
        """Register (stem, sha) for files in the run so a select can find its source hash."""
        for stem, sha in stem_sha_pairs:
            if stem and sha:
                self._stem_to_sha.setdefault(stem, sha)

    def source_stem(self, filename: str) -> Optional[str]:
        """Return the source stem if `filename` is a select, else None."""
        if not self._re:
            return None
        stem = Path(filename).stem
        m = self._re.search(stem)
        if not m or m.start() == 0:   # no match, or nothing precedes the suffix
            return None
        return stem[: m.start()]

    def resolve(self, filename: str) -> Tuple[Optional[str], Optional[str]]:
        """Return (source_clip_stem, source_clip_sha | None). (None, None) if not a select."""
        src = self.source_stem(filename)
        if src is None:
            return None, None
        return src, self._stem_to_sha.get(src)
