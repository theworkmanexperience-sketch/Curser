"""
wecape.core.config
==================
Centralized configuration loading for W.E. C.A.P.E. (Target structure: core/config.py).

Single home for what was previously scattered across capture/main.py and the
pipeline: load the base YAML, merge a client profile, apply per-run CLI
overrides (proxy / engine / workers), and surface non-fatal validation warnings.

Dependency-light (yaml + core.errors) so any layer can import it; the profile
loader is imported lazily to avoid an import cycle with capture/.
"""

import copy
import tempfile
from pathlib import Path
from typing import Optional

import yaml

from .errors import ConfigError

VALID_ENGINES = ("stages", "legacy")


def load_base(config_path) -> dict:
    """Load and validate a base config YAML into a dict. Raises ConfigError."""
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ConfigError(
            f"Config root must be a mapping, got {type(data).__name__}: {path}"
        )
    return data


def apply_profile(config: dict, profile_name: str) -> dict:
    """Merge a client profile over the base config (profiles/{name}.yaml)."""
    from ..capture.profile import ProfileLoader  # lazy: avoids import cycle
    return ProfileLoader().load(profile_name, config)


def apply_overrides(
    config: dict,
    *,
    proxy: bool = False,
    engine: Optional[str] = None,
    workers: Optional[int] = None,
) -> dict:
    """Apply per-run CLI overrides. Returns a copy; never mutates the input."""
    config = copy.deepcopy(config)
    if proxy:
        config.setdefault("proxy_generation", {})["enabled"] = True
    if engine:
        config.setdefault("pipeline", {})["engine"] = engine
    if workers is not None:
        config.setdefault("performance", {})["max_workers"] = workers
    return config


def load_config(
    config_path,
    *,
    profile: Optional[str] = None,
    proxy: bool = False,
    engine: Optional[str] = None,
    workers: Optional[int] = None,
) -> dict:
    """Load base + optional profile + CLI overrides into one merged config dict."""
    config = load_base(config_path)
    if profile:
        config = apply_profile(config, profile)
    return apply_overrides(config, proxy=proxy, engine=engine, workers=workers)


def validate(config: dict) -> list:
    """Return a list of non-fatal, human-readable warnings about the config."""
    warnings = []
    engine = config.get("pipeline", {}).get("engine", "stages")
    if engine not in VALID_ENGINES:
        warnings.append(
            f"pipeline.engine '{engine}' unknown (expected {'|'.join(VALID_ENGINES)})"
        )
    workers = config.get("performance", {}).get("max_workers", 8)
    if not isinstance(workers, int) or workers < 1:
        warnings.append(
            f"performance.max_workers should be a positive int, got {workers!r}"
        )
    return warnings


def write_temp(config: dict) -> Path:
    """Serialize a merged config to a temp YAML file (Pipeline takes a path)."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, prefix="wecape_config_"
    )
    yaml.dump(config, tmp)
    tmp.close()
    return Path(tmp.name)
