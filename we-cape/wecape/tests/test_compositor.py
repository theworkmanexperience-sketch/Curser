"""
Deliverable 2 regression suite — the 5 ratified safeguard cases.
Release gate: ALL must pass before commit (Board contract, July 2026).

  1. Happy path: verified header composites; compliance record complete
  2. Tampered header (content changed) -> HeaderIntegrityError, no output
  3. Missing header -> HeaderIntegrityError (never substitute)
  4. Wrong-dimension asset w/ correct-name -> refused (no scaling)
  5. Unregistered brand -> UnregisteredBrandError (stop, don't improvise)
"""

import shutil
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from wecape.progressions.compositor import (
    compose, HeaderIntegrityError, UnregisteredBrandError, _sha256)

REPO = Path(__file__).resolve().parents[2]
REAL_HEADER = REPO / "brand_assets/TWE_PROGRESSIONS_MASTER_HEADER_OFFICIAL_v3.0.png"


def _mk_env(tmp_path, header_bytes=None, sha_override=None,
            width=1983, height=793):
    """Isolated repo-root with its own brand_assets + profile."""
    root = tmp_path / "root"
    (root / "brand_assets").mkdir(parents=True)
    (root / "brand_profiles").mkdir()
    hdr = root / "brand_assets/HEADER.png"
    if header_bytes is None:
        shutil.copy2(REAL_HEADER, hdr)
    else:
        hdr.write_bytes(header_bytes)
    profile = {
        "brand_id": "testbrand",
        "display_name": "Test",
        "locked_header": {
            "filename": "brand_assets/HEADER.png",
            "sha256": sha_override or _sha256(hdr),
            "width": width, "height": height,
            "placement": "top_center"},
        "canvas": {"width": 2048, "height": 2560, "background": "#0E0E0E"},
    }
    (root / "brand_profiles/testbrand.yaml").write_text(yaml.dump(profile))
    return root


def test_1_happy_path_composites_and_records(tmp_path):
    root = _mk_env(tmp_path)
    out = tmp_path / "out/collage.png"
    rec = compose("testbrand", out, repo_root=root,
                  profiles_dir=root / "brand_profiles")
    assert out.exists()
    assert rec["header_verified"] is True
    assert rec["placement"] == "top_center"
    assert rec["output_sha256"] == _sha256(out)


def test_2_tampered_header_refused_no_output(tmp_path):
    root = _mk_env(tmp_path)
    hdr = root / "brand_assets/HEADER.png"
    hdr.write_bytes(hdr.read_bytes() + b"\x00TAMPER")  # content changed
    out = tmp_path / "out/collage.png"
    with pytest.raises(HeaderIntegrityError, match="MISMATCH"):
        compose("testbrand", out, repo_root=root,
                profiles_dir=root / "brand_profiles")
    assert not out.exists()  # fail closed — nothing written


def test_3_missing_header_refused_never_substituted(tmp_path):
    root = _mk_env(tmp_path)
    (root / "brand_assets/HEADER.png").unlink()
    out = tmp_path / "out/collage.png"
    with pytest.raises(HeaderIntegrityError, match="MISSING"):
        compose("testbrand", out, repo_root=root,
                profiles_dir=root / "brand_profiles")
    assert not out.exists()


def test_4_wrong_dimensions_refused_no_scaling(tmp_path):
    from PIL import Image
    root = _mk_env(tmp_path)
    hdr = root / "brand_assets/HEADER.png"
    Image.new("RGB", (991, 396), "#FF0000").save(hdr)  # half-size imposter
    # Re-record its sha so ONLY the dimension gate is under test
    prof_p = root / "brand_profiles/testbrand.yaml"
    prof = yaml.safe_load(prof_p.read_text())
    prof["locked_header"]["sha256"] = _sha256(hdr)
    prof_p.write_text(yaml.dump(prof))
    with pytest.raises(HeaderIntegrityError, match="dimensions"):
        compose("testbrand", tmp_path / "out/c.png", repo_root=root,
                profiles_dir=root / "brand_profiles")


def test_5_unregistered_brand_stops(tmp_path):
    root = _mk_env(tmp_path)
    with pytest.raises(UnregisteredBrandError, match="not registered"):
        compose("ghostbrand", tmp_path / "out/c.png", repo_root=root,
                profiles_dir=root / "brand_profiles")
