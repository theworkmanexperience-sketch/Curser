"""
W.E. PROGRESSIONS — Deterministic Header Compositor (Deliverable 2).

Behavioral contract (Board-ratified, contract locked July 2026):
  1. Verify the official header asset against the recorded SHA-256.
  2. Proceed ONLY on an exact hash match.
  3. Abort immediately on any mismatch (HeaderIntegrityError).
  4. NEVER substitute, regenerate, or repair the asset.
Also enforced: recorded dimensions (no scaling — the header composites
at native size or not at all) and registered-brand-only operation.
Deterministic: same profile + same inputs -> byte-stable placement.
"""

import hashlib
from pathlib import Path
from typing import Optional

import yaml
from PIL import Image


class CompositorError(RuntimeError):
    """Base class — all failures are refusals, never repairs."""


class UnregisteredBrandError(CompositorError):
    pass


class HeaderIntegrityError(CompositorError):
    pass


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_profile(brand_id: str, profiles_dir: Path) -> dict:
    p = profiles_dir / f"{brand_id}.yaml"
    if not p.exists():
        raise UnregisteredBrandError(
            f"brand '{brand_id}' is not registered — no profile at {p}. "
            "STOP: register the brand and its verified header first; "
            "the compositor never proceeds on an unregistered brand.")
    return yaml.safe_load(p.read_text())


def verify_header(profile: dict, repo_root: Path) -> Path:
    """Contract rules 1-4 + dimension lock. Returns verified path."""
    lh = profile["locked_header"]
    path = repo_root / lh["filename"]
    if not path.exists():
        raise HeaderIntegrityError(
            f"official header MISSING at {path}. STOP: never substitute — "
            "restore the verified asset.")
    actual = _sha256(path)
    if actual != lh["sha256"]:
        raise HeaderIntegrityError(
            "header SHA-256 MISMATCH — asset is not the official header.\n"
            f"  recorded: {lh['sha256']}\n  actual:   {actual}\n"
            "STOP: never substitute, regenerate, or repair.")
    with Image.open(path) as im:
        if (im.width, im.height) != (lh["width"], lh["height"]):
            raise HeaderIntegrityError(
                f"header dimensions {im.width}x{im.height} != recorded "
                f"{lh['width']}x{lh['height']} — refuse (no scaling).")
    return path


def compose(brand_id: str, output_path: Path,
            repo_root: Optional[Path] = None,
            profiles_dir: Optional[Path] = None) -> dict:
    """Compose the verified header onto the brand canvas (top-center,
    native size). Returns a compliance record for the job manifest."""
    root = repo_root or Path(__file__).resolve().parents[2]
    profiles = profiles_dir or (root / "brand_profiles")
    profile = load_profile(brand_id, profiles)
    header_path = verify_header(profile, root)

    cv = profile["canvas"]
    canvas = Image.new("RGB", (cv["width"], cv["height"]), cv["background"])
    with Image.open(header_path) as header:
        x = (cv["width"] - header.width) // 2   # top_center, deterministic
        canvas.paste(header, (x, 0))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG")

    return {
        "header_verified": True,
        "header_sha256": profile["locked_header"]["sha256"],
        "brand_id": brand_id,
        "placement": "top_center",
        "output": str(output_path),
        "output_sha256": _sha256(output_path),
    }
