"""Tests for wecape.core.config — the centralized config layer (Target structure)."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.core.config import (
    load_base, load_config, apply_overrides, validate, write_temp,
)
from wecape.core.errors import ConfigError


def _write(tmp_path, text):
    p = tmp_path / "c.yaml"
    p.write_text(text)
    return p


def test_load_base_valid(tmp_path):
    p = _write(tmp_path, "pipeline:\n  engine: stages\nperformance:\n  max_workers: 4\n")
    cfg = load_base(p)
    assert cfg["pipeline"]["engine"] == "stages"


def test_load_base_missing_raises(tmp_path):
    try:
        load_base(tmp_path / "nope.yaml")
        assert False, "should raise ConfigError"
    except ConfigError:
        pass


def test_load_base_bad_yaml_raises(tmp_path):
    p = _write(tmp_path, "pipeline: [unclosed\n")
    try:
        load_base(p)
        assert False, "should raise ConfigError"
    except ConfigError:
        pass


def test_load_base_non_mapping_raises(tmp_path):
    p = _write(tmp_path, "- just\n- a\n- list\n")
    try:
        load_base(p)
        assert False, "should raise ConfigError"
    except ConfigError:
        pass


def test_apply_overrides_sets_values_without_mutating_input():
    base = {"pipeline": {"engine": "stages"}}
    out = apply_overrides(base, proxy=True, engine="legacy", workers=8)
    assert out["proxy_generation"]["enabled"] is True
    assert out["pipeline"]["engine"] == "legacy"
    assert out["performance"]["max_workers"] == 8
    # original untouched
    assert "proxy_generation" not in base
    assert base["pipeline"]["engine"] == "stages"


def test_load_config_applies_overrides(tmp_path):
    p = _write(tmp_path, "pipeline:\n  engine: stages\n")
    cfg = load_config(p, proxy=True, engine="legacy")
    assert cfg["pipeline"]["engine"] == "legacy"
    assert cfg["proxy_generation"]["enabled"] is True


def test_validate_flags_bad_engine():
    warns = validate({"pipeline": {"engine": "bogus"}})
    assert any("engine" in w for w in warns)


def test_validate_clean_config_has_no_warnings():
    assert validate({"pipeline": {"engine": "stages"},
                     "performance": {"max_workers": 4}}) == []


def test_write_temp_roundtrips(tmp_path):
    p = write_temp({"pipeline": {"engine": "stages"}})
    assert p.exists()
    assert yaml.safe_load(p.read_text())["pipeline"]["engine"] == "stages"
