#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Camera Identity (footage-first)

The problem this solves: a SanDisk card's VOLUME LABEL is operator-set and lies.
On this kit the card named "DJIAction6" actually holds DJI Osmo Action 5 Pro
footage (verified 2026-07-04 from the on-camera serials). A novice — or our own
`detect` heuristic — that trusts the label writes the WRONG camera_id into the
deterministic registry, silently.

Design principle (agreed 2026-07-05): derive identity from the FOOTAGE whenever
possible, and only ask the human to CONFIRM what the system already knows — never
to SUPPLY what it can't reliably determine. Trust order:

    1. metadata serial/model  → registry match      (authoritative — "verified")
    2. filename family/brand  → the physical brand   (reliable — "file")
       · a brand that maps to exactly one known body identifies it outright;
       · an ambiguous brand (two DJI bodies) narrows it and defers to a confirm.
    3. volume label           → a WEAK HINT only     ("label" — never trusted alone)

If the weak label CONTRADICTS the footage (metadata/brand), that is a CONFLICT:
we stop and show both — never silently proceed. This is the "never trust a
*mis*-labeled card" extension of the existing "never offload an *un*-labeled card".

stdlib only · zero network · read-only. exiftool is optional and injectable
(so this is fully unit-testable and degrades gracefully when it's absent).
"""

import re
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CAMERAS_YAML = REPO / "cameras.yaml"

# Seeded from the on-camera Device/Camera Info screens (2026-07-04). This is the
# source of truth; cameras.yaml (if present) is merged over it by serial so the
# operator can add bodies without editing code. Serials here are the on-SCREEN
# serials; the EMBEDDED-in-file serial may differ — registry match is tolerant and
# also matches on device_name / model tokens (finalize once the exiftool probe runs).
# `model_code` is DJI's embedded per-file identifier (from the `model_name:AC0NN`
# token inside exiftool's Category tag) — the strongest DJI signal (no plain Serial
# tag is embedded). DJI's codes are OFFSET from the marketing name: AC003 = Action 4,
# AC004 = Action 5 Pro, AC006 = Action 6 (RESOLVED 2026-07-05 — AC004 confirmed as the
# 5 Pro by the camera self-reporting "OsmoAction5ProA715" + kit elimination). An
# unmapped code (e.g. AC003 = an Action 4 we don't own) safely falls through to
# "confirm which body", never a mislabel.
DEFAULT_REGISTRY = [
    {"label": "DJI Osmo Action 6", "short": "DJI ACTION 6", "brand": "DJI",
     "serial": "9KRXNC800BGX5N", "device_name": "OsmoAction6-84CB", "model_code": "AC006"},
    {"label": "DJI Osmo Action 5 Pro", "short": "DJI ACTION 5", "brand": "DJI",
     "serial": "82JXN4500BW1VE", "device_name": "OsmoAction5ProA715", "model_code": "AC004"},
    {"label": "Insta360 X5", "short": "Insta360 X5", "brand": "Insta360",
     "serial": "IAHEA2503SK8FE", "device_name": "Insta360 X5"},
]

# filename -> brand/family. Brand is ALWAYS reliable from a real card's files;
# the exact DJI body is NOT (both Action 5/6 write DJI_*), so "DJI" is a brand,
# not a body — it narrows, then we confirm.
_FAMILY = [
    (re.compile(r"^DJI_", re.I), "DJI"),
    (re.compile(r"^G[HXLP][0-9]{4,}", re.I), "GoPro"),
    (re.compile(r"^GOPR", re.I), "GoPro"),
    (re.compile(r"_00_\d+\.insv$", re.I), "Insta360 X5"),
    (re.compile(r"^(VID|PRO_VID|ISD)_", re.I), "Insta360 X5"),
    (re.compile(r"^LRV_", re.I), "Insta360 X5"),
    (re.compile(r"^IMG_\d+", re.I), "iPhone"),
    (re.compile(r"^MOV_\d+", re.I), "iPhone"),
    (re.compile(r"^P\d{7}", re.I), "OM System OM-1"),
    (re.compile(r"^P[A-C]\d{6}", re.I), "OM System OM-1"),
]

# exiftool tags that may carry a body serial or model, most-specific first.
_SERIAL_TAGS = ("Camera Serial No", "Serial Number", "SerialNumber",
                "Camera Serial Number", "Device Serial Number",
                "Internal Serial Number")
_MODEL_TAGS = ("Camera Model Name", "Model", "Device Name", "Camera Model")


# ─────────────────────────────────────────────────────────────────────────────
# Registry
# ─────────────────────────────────────────────────────────────────────────────
def load_registry(path=CAMERAS_YAML):
    """Seeded defaults, merged (by serial) with cameras.yaml if present. Uses PyYAML
    when available, else a tolerant stdlib parser for the simple list-of-maps shape."""
    reg = {r["serial"]: dict(r) for r in DEFAULT_REGISTRY}
    p = Path(path)
    if p.exists():
        for row in _parse_cameras_yaml(p.read_text()):
            ser = row.get("serial")
            if ser:
                reg[ser] = {**reg.get(ser, {}), **row}
    return list(reg.values())


def _parse_cameras_yaml(text):
    """Parse `cameras:` list-of-maps without a YAML dependency."""
    try:
        import yaml
        data = yaml.safe_load(text) or {}
        rows = data.get("cameras", []) if isinstance(data, dict) else []
        return [r for r in rows if isinstance(r, dict)]
    except Exception:
        pass
    rows, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"-\s+(\w+)\s*:\s*(.*)$", s)
        if m:                                   # new list item
            if cur:
                rows.append(cur)
            cur = {m.group(1): _clean(m.group(2))}
            continue
        m = re.match(r"(\w+)\s*:\s*(.*)$", s)
        if m and cur is not None:
            cur[m.group(1)] = _clean(m.group(2))
    if cur:
        rows.append(cur)
    return rows


def _clean(v):
    return v.strip().strip('"').strip("'")


# ─────────────────────────────────────────────────────────────────────────────
# Pure signal extractors
# ─────────────────────────────────────────────────────────────────────────────
def brand_from_files(sample_names):
    """The physical brand/family from filenames — reliable. Returns e.g. 'DJI'
    (ambiguous body), 'Insta360 X5', 'OM System OM-1', 'iPhone', 'GoPro', or None."""
    for n in sample_names or ():
        for rx, fam in _FAMILY:
            if rx.search(n):
                return fam
    return None


def label_hint_from_mount(mount_name, registry=None):
    """The WEAK hint from a volume/folder name. Returns a canonical label or None.
    Explicitly NOT authoritative — a card can be named anything."""
    name = (mount_name or "").lower()
    reg = registry or load_registry()
    # match on short code ('DJI ACTION 6') or label tokens present in the mount name
    cands = []
    for r in reg:
        for key in (r.get("short", ""), r.get("label", "")):
            if key and _norm(key) and _norm(key) in _norm(name):
                cands.append(r["label"])
    if cands:                                   # longest/most-specific match wins
        return sorted(set(cands), key=len)[-1]
    # bare body-number hint ("djiaction6" -> Action 6) as a last resort
    for r in reg:
        num = _model_num(r["label"])
        if num and r["brand"].lower() in name and num in re.sub(r"\D", "", name):
            return r["label"]
    return None


def serial_from_metadata(path, runner=None):
    """Best-effort {serial, model, make} from a media file via exiftool. Returns {}
    when exiftool is unavailable or nothing matches — callers must degrade gracefully.
    `runner(path)->text` is injectable for tests (no real exiftool needed)."""
    runner = runner or _exiftool_runner
    try:
        text = runner(path)
    except Exception:
        return {}
    if not text:
        return {}
    out = {}
    for tag in _SERIAL_TAGS:
        v = _grep_tag(text, tag)
        if v:
            out["serial"] = v
            break
    for tag in _MODEL_TAGS:
        v = _grep_tag(text, tag)
        if v:
            out["model"] = v
            break
    mk = _grep_tag(text, "Make")
    if mk:
        out["make"] = mk
    code = _dji_model_code(text)          # DJI's embedded model_name:AC0NN (strongest DJI signal)
    if code:
        out["model_code"] = code
    return out


def _dji_model_code(text):
    """Extract DJI's embedded model code, e.g. 'AC006', from the `model_name:AC0NN`
    token inside exiftool's Category tag. Returns None if absent."""
    m = re.search(r"model_name\s*:\s*(AC\d{3,})", text or "", re.I)
    return m.group(1).upper() if m else None


def _exiftool_runner(path):
    if not shutil.which("exiftool"):
        return ""
    r = subprocess.run(["exiftool", "-s", "-f", str(path)],
                       capture_output=True, text=True, timeout=30)
    return r.stdout or ""


def _grep_tag(text, tag):
    # exiftool -s prints "TagName    : value"; also tolerate "Tag Name : value"
    key = re.sub(r"\s+", "", tag).lower()
    for line in text.splitlines():
        m = re.match(r"\s*([A-Za-z0-9 ]+?)\s*:\s*(.+?)\s*$", line)
        if m and re.sub(r"\s+", "", m.group(1)).lower() == key:
            val = m.group(2).strip()
            if val and val != "-":
                return val
    return None


def registry_match(meta, registry=None):
    """Match a metadata dict {serial,model,make} to a registry entry. Exact serial
    first; else device_name/label token containment (probe-tolerant). Returns the
    entry or None."""
    reg = registry or load_registry()
    code = (meta or {}).get("model_code")          # DJI embedded code — strongest signal
    if code:
        for r in reg:
            if r.get("model_code") and r["model_code"].upper() == code.upper():
                return r
    ser = (meta or {}).get("serial")
    if ser:
        for r in reg:
            if r.get("serial") and _norm(r["serial"]) == _norm(ser):
                return r
    model = (meta or {}).get("model")
    if model:
        for r in reg:
            for key in (r.get("device_name", ""), r.get("label", ""), r.get("short", "")):
                if key and _norm(key) and (_norm(key) in _norm(model) or _norm(model) in _norm(key)):
                    return r
    return None


# ─────────────────────────────────────────────────────────────────────────────
# The decision
# ─────────────────────────────────────────────────────────────────────────────
def identify(mount_name="", sample_names=(), meta=None, registry=None):
    """Combine all signals into one identity decision. Returns a dict:
        label        canonical body label, or None if undetermined
        source       'metadata-serial' | 'filename-family' | 'volume-label' | None
        confidence   'verified' > 'file' > 'label' > 'none'
        conflict     True if the weak label CONTRADICTS the footage → STOP
        must_confirm True unless verified-and-consistent
        brand        physical brand from files (may be set even when body unknown)
        label_hint   what the volume name suggested (for the conflict message)
        detail       human sentence describing the basis
    """
    reg = registry or load_registry()
    brand = brand_from_files(sample_names)
    hint = label_hint_from_mount(mount_name, reg)
    matched = registry_match(meta, reg) if meta else None

    # 1) authoritative: metadata serial/model → registry
    if matched:
        conflict = bool(hint and not _labels_compatible(hint, matched["label"]))
        conflict = conflict or bool(brand and not _brand_compatible(brand, matched["brand"]))
        basis = matched.get("model_code") or matched.get("serial") or "metadata"
        return _mk(matched["label"], "metadata-serial", "verified",
                   conflict=conflict, must_confirm=conflict, brand=matched["brand"],
                   hint=hint, status=(STATUS_CONFLICT if conflict else STATUS_VERIFIED),
                   detail=(f"Identified from the footage metadata "
                           f"({basis}) as {matched['label']}."))

    # 2) reliable: filename brand
    if brand:
        bodies = [r for r in reg if _brand_compatible(brand, r["brand"])]
        one_body = _single_body_brand(brand, bodies)
        if one_body:                              # brand maps to exactly one known body
            conflict = bool(hint and not _labels_compatible(hint, one_body["label"]))
            return _mk(one_body["label"], "filename-family", "file",
                       conflict=conflict, must_confirm=conflict, brand=brand, hint=hint,
                       status=(STATUS_CONFLICT if conflict else STATUS_VERIFIED),
                       detail=(f"Identified from the file naming as {one_body['label']}."
                               + (f" (Card is named '{mount_name}', which disagrees — "
                                  "confirm before offloading.)" if conflict else "")))
        # ambiguous brand (e.g. two DJI bodies): narrowed, must confirm which.
        # The volume label is NOT trusted to break the tie (that's exactly the trap).
        options = [r["label"] for r in bodies] or None
        return _mk(None, "filename-family", "brand",
                   conflict=False, must_confirm=True, brand=brand, hint=hint, options=options,
                   status=STATUS_AMBIGUOUS,
                   detail=(f"Files are {brand}, but {brand} has multiple bodies in your kit "
                           f"({', '.join(options) if options else '—'}). "
                           "The card label can't be trusted to pick — please confirm which body."))

    # 3) weak: volume label only (never trusted silently)
    if hint:
        return _mk(hint, "volume-label", "label", conflict=False, must_confirm=True,
                   brand=None, hint=hint, status=STATUS_LABEL_ONLY,
                   detail=(f"Only the card name suggests {hint} — no footage signal to "
                           "confirm it. Card names are unreliable; please confirm the body."))

    # 4) nothing
    return _mk(None, None, "none", conflict=False, must_confirm=True, brand=None, hint=hint,
               status=STATUS_UNKNOWN,
               detail="Couldn't determine the camera from the card or its files — please choose.")


def confirm_prompt(idn):
    """A confirmation-style question the NOVICE can answer (confirm a fact, not guess).
    Never asks 'Action 5 or 6?' cold; states what we found and asks yes/no or a pick."""
    if idn["confidence"] == "verified" and not idn["conflict"]:
        return f"✓ {idn['label']} — verified from the footage. No action needed."
    if idn["conflict"]:
        return (f"⚠ CONFLICT: the card name suggests “{idn['label_hint']}”, but the footage says "
                f"“{idn['label']}”. Trust the footage. Offload as {idn['label']}? [Yes / No, choose]")
    if idn["label"]:
        return (f"This card looks like {idn['label']} — but only from its name, which can be wrong. "
                f"Is this your {idn['label']}? [Yes / No, choose]")
    if idn.get("options"):
        return ("Which camera recorded this card? "
                + " / ".join(idn["options"]) + " (the card name isn't reliable here).")
    return "Which camera recorded this card? Please choose from your cameras."


# ─────────────────────────────────────────────────────────────────────────────
# small helpers
# ─────────────────────────────────────────────────────────────────────────────
# Named identity outcomes (error taxonomy) — for UX wording, audit provenance, and
# debugging. Every identify() result carries exactly one.
STATUS_VERIFIED = "verified"        # body determined from the footage, consistent
STATUS_CONFLICT = "conflict"        # the volume label contradicts the footage
STATUS_AMBIGUOUS = "ambiguous"      # brand known, body not resolved — must pick
STATUS_LABEL_ONLY = "label_only"    # only the (weak) volume name suggested a body
STATUS_UNKNOWN = "unknown"          # no usable signal — must choose


def _mk(label, source, confidence, *, conflict, must_confirm, brand, hint,
        detail, options=None, status=STATUS_UNKNOWN):
    return {"label": label, "source": source, "confidence": confidence,
            "conflict": bool(conflict), "must_confirm": bool(must_confirm),
            "brand": brand, "label_hint": hint, "options": options,
            "detail": detail, "status": status}


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _model_num(label):
    m = re.search(r"\b(\d)\b", label or "")
    return m.group(1) if m else None


def brand_of_label(label):
    n = (label or "").lower()
    if "insta360" in n:
        return "Insta360"
    if "om system" in n or "olympus" in n:
        return "OM System OM-1"
    if "iphone" in n:
        return "iPhone"
    if "gopro" in n:
        return "GoPro"
    if "dji" in n or "osmo" in n:
        return "DJI"
    return None


def _brand_compatible(brand, other):
    """A filename brand vs a registry brand. 'Insta360 X5' family ~ 'Insta360' brand."""
    a, b = (brand or "").lower(), (other or "").lower()
    if a == b:
        return True
    return a.split()[0] == b.split()[0] if a and b else False


def _single_body_brand(brand, bodies):
    """If this brand corresponds to exactly one known body, return it (identifies the
    body outright). DJI has two bodies → None (ambiguous)."""
    b = (brand or "").lower()
    if b == "dji":
        return None                              # two Action bodies — ambiguous
    return bodies[0] if len(bodies) == 1 else None


def _labels_compatible(a, b):
    """Do two body labels refer to the same body? Brand must match; if both name a
    model number they must agree (this is what catches Action 6-label vs Action 5-footage)."""
    if _norm(a) == _norm(b):
        return True
    if brand_of_label(a) != brand_of_label(b):
        return False
    na, nb = _model_num(a), _model_num(b)
    if na and nb:
        return na == nb
    return True
