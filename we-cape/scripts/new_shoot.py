#!/usr/bin/env python3
"""
W.E. C.A.P.E. — New Shoot core  (headless, testable orchestration spine)

Chains the pieces you already have — verified card offload -> CAPTURE -> FCPXML
export -> Final Cut Pro — behind ONE guided flow, and captures the shoot
manifest (name / date / location / trusted-clock) as a sidecar that later feeds
export keywords and the Production Health report.

DESIGN — deliberately thin:
  • Every step is a plain function, independently callable and unit-testable
    with NO GUI and NO network. The heavy lifting stays in the tools this calls
    (offload_cards.py, `python -m wecape`, fcpxml_export.py) — this module only
    sequences them, checks free space up front, keeps an audit trail, and stays
    idempotent on re-run (offload resumes by hash; CAPTURE skips by SHA).
  • A graphical skin (PyWebView) can sit on top later without touching a line of
    logic here. The CLI below is the v1 front end.
  • Card->camera mapping is a best-effort GUESS the human confirms — this module
    never silently mis-labels a card.

stdlib only · zero network · read-only on camera cards.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Reuse the verified-copy helpers rather than reimplement them.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import camera_identity as ci                      # footage-first identity (optional)
except Exception:                                    # pragma: no cover - import guard
    ci = None
try:
    from offload_cards import is_cruft, human, KNOWN_CAMERAS
    from offload_cards import main as offload_main
except Exception:                                    # pragma: no cover - import guard
    KNOWN_CAMERAS = ("DJI ACTION 5", "DJI ACTION 6", "Insta360 X5")
    offload_main = None

    def human(n):
        n = float(n or 0)
        for u in ("B", "KB", "MB", "GB", "TB"):
            if n < 1024 or u == "TB":
                return f"{n:.1f} {u}"
            n /= 1024

    def is_cruft(p):
        return p.name.startswith("._") or p.name == ".DS_Store"

REPO = Path(__file__).resolve().parent.parent
RUN_ID_RE = re.compile(r"WEF_\d{8}_\d{6}_[0-9A-Fa-f]{6}")

# Per-camera folder-name -> physical body. Mirrors config.yaml
# classification.camera_folder_patterns; augmented from config when PyYAML is present.
DEFAULT_CAMERA_PATTERNS = [
    ("DJI ACTION 6", "DJI Osmo Action 6"),
    ("DJI ACTION 5", "DJI Osmo Action 5"),
    ("Insta360 X5", "Insta360 X5"),
    ("iPhone", "iPhone"),
    ("OM SYSTEM", "OM System OM-1"),
]

# Filename -> camera family, for guessing when the card/volume name is generic.
FAMILY_PATTERNS = [
    (re.compile(r"^DJI_", re.I), "DJI"),
    (re.compile(r"^G[HXLP][0-9]{4,}", re.I), "GoPro"),
    (re.compile(r"^GOPR", re.I), "GoPro"),
    (re.compile(r"_00_\d+\.insv$", re.I), "Insta360 X5"),
    (re.compile(r"^(VID|PRO_VID|ISD)_", re.I), "Insta360 X5"),
    (re.compile(r"^IMG_\d+", re.I), "iPhone"),
    (re.compile(r"^MOV_\d+", re.I), "iPhone"),
    # OM System / Olympus DCF: P<month><day><seq> (month 1-9, then A/B/C for Oct-Dec)
    (re.compile(r"^P\d{7}", re.I), "OM System OM-1"),
    (re.compile(r"^P[A-C]\d{6}", re.I), "OM System OM-1"),
]

MEDIA_EXTS = {
    "mp4", "mov", "m4v", "avi", "mxf", "mkv", "insv", "insp", "braw",
    "lrv", "thm", "srt", "wav", "jpg", "jpeg", "heic", "png", "dng", "cr3",
}
VIDEO_EXTS = {"mp4", "mov", "m4v", "avi", "mxf", "mkv", "insv", "braw"}
# Root-level folders that mark an actual camera card. A general hard drive full of
# loose videos has NONE of these at its root — which is how we avoid mis-detecting
# an archive/backup drive (e.g. a 1 TB FreeAgent) as a "card".
CARD_MARKERS = ("DCIM", "PRIVATE", "CLIPS", "XDROOT", "PANA", "MP_ROOT", "AVF_INFO")
# Volumes we never treat as camera cards.
SYSTEM_VOLUMES = {"Macintosh HD", "Macintosh HD - Data", "com.apple.TimeMachine.localsnapshots"}


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─────────────────────────────────────────────────────────────────────────────
# Pure helpers (unit-tested; no I/O side effects beyond reading the given path)
# ─────────────────────────────────────────────────────────────────────────────
def load_camera_patterns(config_path=None):
    """(folder-substring, camera-model) pairs. Defaults, augmented from config.yaml if PyYAML present."""
    pairs = list(DEFAULT_CAMERA_PATTERNS)
    cfg = Path(config_path) if config_path else (REPO / "wecape" / "config.yaml")
    try:
        import yaml  # optional; scripts stay runnable without it
        data = yaml.safe_load(cfg.read_text())
        for row in (data.get("classification", {}) or {}).get("camera_folder_patterns", []) or []:
            pat, model = row.get("pattern"), row.get("camera_model")
            if pat and model and (pat, model) not in pairs:
                pairs.append((pat, model))
    except Exception:
        pass
    # longest pattern first so "DJI ACTION 6" wins over a hypothetical "DJI".
    return sorted(pairs, key=lambda p: -len(p[0]))


def guess_camera(mount_name, sample_names=(), patterns=None):
    """Best-effort (label, confidence). confidence in {'high','medium','low'}.
    high  = the card/volume name matches a per-body folder pattern.
    medium= filenames match a known camera family.
    low   = nothing matched — the human must choose."""
    patterns = patterns or load_camera_patterns()
    name = (mount_name or "").lower()
    for sub, model in patterns:
        if sub.lower() in name:
            return model, "high"
    for n in sample_names:
        for rx, fam in FAMILY_PATTERNS:
            if rx.search(n):
                return fam, "medium"
    return None, "low"


def scan_media(path, exts=None):
    """Return (files, total_bytes, video_count) for everything offload would copy."""
    root = Path(path)
    files, total, vids = [], 0, 0
    if not root.exists():
        return files, 0, 0
    it = [root] if root.is_file() else sorted(root.rglob("*"))
    for p in it:
        try:
            if not p.is_file() or is_cruft(p):
                continue
            ext = p.suffix.lower().lstrip(".")
            if exts and ext not in exts:
                continue
            sz = p.stat().st_size
        except OSError:
            continue
        files.append(p)
        total += sz
        if ext in VIDEO_EXTS:
            vids += 1
    return files, total, vids


def is_camera_card(path, patterns=None):
    """True only if the mount has a recognizable card STRUCTURE at its root — a
    DCIM/PRIVATE/CLIPS/… folder, or a top-level folder matching a known camera
    pattern (e.g. 'DJI ACTION 6', 'Insta360 X5').

    Deliberately does NOT treat 'has some video files' as a card: a general archive
    or backup drive scatters videos in arbitrary folders and would be a false
    positive (the FreeAgent-GoFlex case). A real card always has the structure."""
    root = Path(path)
    if not root.is_dir():
        return False
    try:
        dirs = {e.name for e in root.iterdir() if e.is_dir()}
    except OSError:
        return False
    upper = {d.upper() for d in dirs}
    if upper & {m.upper() for m in CARD_MARKERS}:
        return True
    # a hand-organized per-camera folder at the root also counts
    subs = [p.lower() for p, _ in (patterns or load_camera_patterns())]
    return any(sub in d.lower() for d in dirs for sub in subs)


# A removable camera card tops out around 1-2 TB; anything larger is a fixed/archive
# drive (10TB, WE_CAPE_OUTPUT, …) that we must NOT walk during detection — doing so
# would grind through millions of files. Overridable via detect_cards(max_card_bytes=).
MAX_CARD_BYTES = int(2.5 * 1024 ** 4)          # ~2.5 TB


def _volume_capacity(mount):
    try:
        return shutil.disk_usage(str(mount)).total
    except OSError:
        return None


# new-scheme confidence -> old badge vocabulary (GUI/HTML understands high/medium/low).
# The INVERSION lives here: a volume-name-only match ('label') is now 'low' — the
# operator must confirm — because the card's name is the least trustworthy signal.
_CONF_BADGE = {"verified": "high", "file": "high", "brand": "medium",
               "label": "low", "none": "low"}


def _card_metadata(mount, files):
    """Best-effort {serial,model} from the mount's first video (footage-first identity).
    Read-only, graceful: returns {} if camera_identity/exiftool unavailable."""
    if ci is None:
        return {}
    vid = next((f for f in files if f.suffix.lower().lstrip(".") in VIDEO_EXTS), None)
    return ci.serial_from_metadata(vid) if vid else {}


def detect_cards(volumes="/Volumes", patterns=None, max_card_bytes=None,
                 capacity_fn=None, metadata_fn=None):
    """Scan mounts and return candidate cards, each with a footage-first identity.

    Identity comes from the FOOTAGE (metadata serial > filename brand) and treats the
    volume label as a weak hint only; if the label CONTRADICTS the footage the card is
    flagged `conflict` (the caller must stop and confirm — never silently offload a
    mis-labeled card). `metadata_fn(mount, files)->meta` and `capacity_fn` are injectable
    for tests. Oversized volumes (>~2.5 TB) are skipped WITHOUT being walked."""
    patterns = patterns or load_camera_patterns()
    max_card_bytes = MAX_CARD_BYTES if max_card_bytes is None else max_card_bytes
    capacity_fn = capacity_fn or _volume_capacity
    metadata_fn = metadata_fn or _card_metadata
    registry = ci.load_registry() if ci is not None else None
    vroot = Path(volumes)
    out = []
    if not vroot.is_dir():
        return out
    for mount in sorted(vroot.iterdir()):
        try:
            if mount.name in SYSTEM_VOLUMES or not mount.is_dir():
                continue
            cap = capacity_fn(mount)                       # cheap — before any file walk
            if cap is not None and cap > max_card_bytes:
                continue                                   # fixed/archive drive, not a card
            if not is_camera_card(mount, patterns):        # require a real card structure
                continue
        except OSError:
            continue
        files, total, vids = scan_media(mount, MEDIA_EXTS)
        sample = [f.name for f in files[:40]]
        card = {"mount": str(mount), "file_count": len(files),
                "video_count": vids, "bytes": total}
        if ci is not None:
            try:
                meta = metadata_fn(mount, files)
            except Exception:
                meta = {}
            idn = ci.identify(mount.name, sample, meta=meta, registry=registry)
            # `camera` = a preselection for the dropdown: the resolved body, else the
            # known brand (so 'DJI' still shows), else nothing.
            camera = idn["label"] or idn["brand"]
            conf = "low" if idn["conflict"] else _CONF_BADGE.get(idn["confidence"], "low")
            card.update({"camera": camera, "camera_derived": camera, "confidence": conf,
                         "conflict": idn["conflict"], "must_confirm": idn["must_confirm"],
                         "identity_source": idn["source"], "identity_status": idn["status"],
                         "detail": idn["detail"], "options": idn["options"],
                         "prompt": ci.confirm_prompt(idn)})
        else:                                              # legacy fallback (no ci module)
            label, conf = guess_camera(mount.name, sample, patterns)
            card.update({"camera": label, "confidence": conf, "conflict": False,
                         "must_confirm": conf != "high"})
        out.append(card)
    return out


def identity_provenance(c):
    """How a card's camera_id was derived — persisted to the manifest + audit (P3).
    If the human's final camera differs from the footage-derived one, it's flagged an
    override so an audit can see the human overrode the footage (progressive
    disclosure: the system defers to the human, but records that it did)."""
    derived = c.get("camera_derived")               # footage-derived label, if detect set one
    src = c.get("identity_source") or "user"
    status = c.get("identity_status") or "user_specified"
    if derived and c.get("camera") and c["camera"] != derived:
        src, status = "user-override", "overridden"
    return {"label": c.get("camera"), "source": c.get("mount"),
            "identified_by": src, "identity_status": status}


def free_bytes(path):
    try:
        return shutil.disk_usage(str(path)).free
    except OSError:
        return None


def preflight_space(needed_bytes, dests, headroom=1.10):
    """Per-destination free-space check BEFORE any copy starts. headroom = safety margin."""
    need = int(needed_bytes * headroom)
    rows = []
    for d in dests:
        free = free_bytes(Path(d).parent if not Path(d).exists() else d)
        ok = free is None or free >= need   # unknown free (unmounted) -> flagged elsewhere
        rows.append({"dest": str(d), "free": free, "needed": need,
                     "ok": bool(ok), "known": free is not None})
    return {"needed_raw": int(needed_bytes), "needed": need,
            "ok": all(r["ok"] for r in rows), "dests": rows}


# ─────────────────────────────────────────────────────────────────────────────
# Shoot manifest sidecar (shoot.yaml) — minimal, stdlib-only, human-readable
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class ShootManifest:
    name: str
    date: str = ""
    location: str = ""
    trusted_clock: str = "unknown"       # which camera's clock to trust for time, or 'unknown'
    cameras: list = field(default_factory=list)   # [{'label':.., 'source':..}]
    notes: str = ""
    created: str = field(default_factory=_now)

    def to_yaml(self):
        def sc(v):
            s = "" if v is None else str(v)
            if s == "":
                return '""'
            return json.dumps(s) if (s.strip() != s or any(c in s for c in ":#")) else s
        lines = ["# W.E. C.A.P.E. — shoot manifest (feeds export keywords + Production Health)",
                 f"name: {sc(self.name)}",
                 f"date: {sc(self.date)}",
                 f"location: {sc(self.location)}",
                 f"trusted_clock: {sc(self.trusted_clock)}",
                 f"notes: {sc(self.notes)}",
                 f"created: {sc(self.created)}",
                 "cameras:"]
        if self.cameras:
            for c in self.cameras:
                lines.append(f"  - label: {sc(c.get('label',''))}")
                lines.append(f"    source: {sc(c.get('source',''))}")
                if c.get("identified_by"):          # P3: how this camera_id was derived
                    lines.append(f"    identified_by: {sc(c.get('identified_by'))}")
                if c.get("identity_status"):
                    lines.append(f"    identity_status: {sc(c.get('identity_status'))}")
        else:
            lines.append("  []")
        return "\n".join(lines) + "\n"

    def write(self, out_dir):
        p = Path(out_dir) / "shoot.yaml"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_yaml())
        return p


def read_manifest(path):
    """Parse the simple subset of YAML that write() emits (no PyYAML dependency)."""
    text = Path(path).read_text()
    out = {"cameras": []}
    cur = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - label:"):
            cur = {"label": _unq(raw.split(":", 1)[1].strip()), "source": ""}
            out["cameras"].append(cur)
        elif raw.startswith("    ") and ":" in raw and cur is not None:
            k, v = raw.strip().split(":", 1)          # source / identified_by / identity_status / future
            cur[k.strip()] = _unq(v.strip())
        elif raw.startswith("cameras:"):
            continue
        elif ":" in raw and not raw.startswith(" "):
            k, v = raw.split(":", 1)
            out[k.strip()] = _unq(v.strip())
    return out


def _unq(s):
    if len(s) >= 2 and s[0] == s[-1] == '"':
        try:
            return json.loads(s)
        except Exception:
            return s[1:-1]
    return s


# ─────────────────────────────────────────────────────────────────────────────
# D1 (SECURITY_RISK_ANALYSIS) — paths readable LOCALLY, hashed on anything shared
# ─────────────────────────────────────────────────────────────────────────────
# Full paths stay in shoot.yaml / the session log for local troubleshooting, but
# any copy that leaves the machine (offsite backup, a shared manifest) has its
# path-like fields hashed with the SAME scheme the engine's audit uses
# (wecape/capture/audit.py: 'sha256:' + sha256(str(path))). Names / date /
# location stay readable because they're useful and low-risk.
SHARE_NOTE = "Paths hashed for privacy; full paths available locally."
_PATH_KEYS = {"source", "mount", "path", "paths", "original_path", "out",
              "dest", "dest2", "output", "scaffold_path", "proxy_path"}


def _path_hash(value):
    return "sha256:" + hashlib.sha256(str(value).encode()).hexdigest()


def redact_paths(obj):
    """Recursively replace path-like string fields with their hash. Names are kept."""
    if isinstance(obj, dict):
        return {k: (_path_hash(v) if (k in _PATH_KEYS and isinstance(v, str) and v)
                    else redact_paths(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_paths(x) for x in obj]
    return obj


def redact_for_sharing(out_dir):
    """Write path-hashed *.shared.* copies of a shoot's manifest + session log,
    for offsite backup or sharing. Leaves the local full-path originals untouched."""
    out_dir = Path(out_dir)
    written = []
    man = out_dir / "shoot.yaml"
    if man.exists():
        d = read_manifest(man)
        for c in d.get("cameras", []):
            if c.get("source"):
                c["source"] = _path_hash(c["source"])       # mount/path -> hash
        note = (d.get("notes", "") + (" | " if d.get("notes") else "") + SHARE_NOTE).strip()
        sm = ShootManifest(name=d.get("name", ""), date=d.get("date", ""),
                           location=d.get("location", ""),
                           trusted_clock=d.get("trusted_clock", "unknown"),
                           cameras=d.get("cameras", []), notes=note,
                           created=d.get("created", _now()))
        p = out_dir / "shoot.shared.yaml"
        p.write_text(sm.to_yaml())
        written.append(p)
    log = out_dir / "_new_shoot_session.jsonl"
    if log.exists():
        out_lines = [json.dumps({"_note": SHARE_NOTE})]
        for raw in log.read_text().splitlines():
            if not raw.strip():
                continue
            try:
                out_lines.append(json.dumps(redact_paths(json.loads(raw))))
            except Exception:
                continue
        p = out_dir / "_new_shoot_session.shared.jsonl"
        p.write_text("\n".join(out_lines) + "\n")
        written.append(p)
    return written


# ─────────────────────────────────────────────────────────────────────────────
# Audit trail (P3) — one JSONL line per step, travels with the shoot output
# ─────────────────────────────────────────────────────────────────────────────
def audit(out_dir, action, **fields):
    try:
        p = Path(out_dir)
        p.mkdir(parents=True, exist_ok=True)
        rec = {"ts": _now(), "action": action, **fields}
        with open(p / "_new_shoot_session.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Plan (dry-run preview: what WILL happen, before committing)
# ─────────────────────────────────────────────────────────────────────────────
def build_plan(manifest, cards, dest, output, dest2=None, proxy=True, stills=None):
    steps = [f"Write shoot manifest -> {Path(output) / 'shoot.yaml'}"]
    for c in cards:
        d2 = f"  +  {dest2}/{manifest.name}/{c['camera']}" if dest2 else ""
        steps.append(f"Offload (verified) {c['mount']}  ->  {dest}/{manifest.name}/{c['camera']}{d2}")
    steps.append(f"CAPTURE  {dest}/{manifest.name}  ->  {output}" + ("  (+proxies)" if proxy else ""))
    steps.append(f"Export FCPXML for the new run -> {output}" + (f"  (+stills {stills})" if stills else ""))
    steps.append("Open Final Cut Pro on the import sheet + the Next-Steps guide")
    return steps


# ─────────────────────────────────────────────────────────────────────────────
# Impure edges — real tool invocations (guarded; injectable for tests)
# ─────────────────────────────────────────────────────────────────────────────
def run_offload(source, camera, shoot, dest, dest2=None, dry_run=False):
    if offload_main is None:
        raise RuntimeError("offload_cards not importable")
    argv = ["--source", str(source), "--camera", camera, "--shoot", shoot, "--dest", str(dest)]
    if dest2:
        argv += ["--dest2", str(dest2)]
    if dry_run:
        argv += ["--dry-run"]
    return offload_main(argv)          # 0 = all verified, 1 = a mismatch


def run_capture(source, output, extra=None, python="python3"):
    """Run CAPTURE; return the new run_id (parsed from stdout, else newest in registry)."""
    env = dict(os.environ, WECAPE_NONINTERACTIVE="1")
    cmd = [python, "-m", "wecape", "--input", str(source), "--output", str(output)] + list(extra or [])
    proc = subprocess.run(cmd, cwd=str(REPO), env=env, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        raise RuntimeError(f"CAPTURE failed (exit {proc.returncode})")
    ids = RUN_ID_RE.findall(proc.stdout)
    return ids[-1] if ids else None


def run_export(run_id, out, db, stills=None, python="python3"):
    cmd = [python, str(REPO / "scripts" / "fcpxml_export.py"),
           "--run", run_id, "--db", str(db), "--out", str(out)]
    for s in (stills or []):
        cmd += ["--stills", str(s)]
    return subprocess.run(cmd).returncode


def open_file(path):
    if shutil.which("open"):
        subprocess.run(["open", str(path)])
        return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator — sequences the steps; `runners` lets tests inject fakes
# ─────────────────────────────────────────────────────────────────────────────
def run_new_shoot(manifest, cards, dest, output, dest2=None, stills=None,
                  proxy=True, dry_run=False, db=None, runners=None, progress=None):
    """Execute the full flow. Returns a result dict. Idempotent: offload resumes by
    hash, CAPTURE skips by SHA — re-running a finished shoot is safe and fast.

    `progress(stage, detail)` is an OPTIONAL callback fired at each step (for a GUI
    or live log); omit it and the core runs exactly as before, fully headless."""
    r = runners or {}
    _offload = r.get("offload", run_offload)
    _capture = r.get("capture", run_capture)
    _export = r.get("export", run_export)
    _open = r.get("open", open_file)
    db = db or (Path.home() / ".wecape" / "registry" / "wecape.db")
    output = Path(output)
    result = {"manifest": None, "offloaded": [], "run_id": None, "exported": False, "opened": False,
              "dry_run": dry_run, "errors": []}

    def _emit(stage, **detail):
        if progress:
            try:
                progress(stage, detail)
            except Exception:
                pass

    # 1) manifest sidecar — record HOW each camera_id was derived (P3 provenance).
    manifest.cameras = manifest.cameras or [identity_provenance(c) for c in cards]
    mpath = manifest.write(output)
    result["manifest"] = str(mpath)
    audit(output, "manifest", path=str(mpath), name=manifest.name, dry_run=dry_run)
    _emit("manifest", path=str(mpath), name=manifest.name)

    # 2) pre-flight space (needed across all cards) — abort before touching anything
    total = sum(int(c.get("bytes", 0)) for c in cards)
    dests = [dest] + ([dest2] if dest2 else [])
    pf = preflight_space(total, dests)
    audit(output, "preflight", **pf)
    _emit("preflight", ok=pf["ok"], needed=pf["needed"])
    if not pf["ok"] and not dry_run:
        result["errors"].append("insufficient free space — see preflight")
        _emit("done", ok=False, errors=result["errors"])
        return result

    # 3) verified offload, per card
    for c in cards:
        if not c.get("camera"):
            result["errors"].append(f"card {c['mount']} has no camera label — skipped")
            audit(output, "offload_skip", mount=c["mount"], reason="no camera label")
            _emit("offload_skip", mount=c["mount"])
            continue
        _emit("offload_start", mount=c["mount"], camera=c["camera"])
        rc = _offload(c["mount"], c["camera"], manifest.name, dest, dest2, dry_run)
        prov = identity_provenance(c)                # how this camera_id was derived (P3)
        audit(output, "offload", mount=c["mount"], camera=c["camera"], rc=rc, dry_run=dry_run,
              identified_by=prov["identified_by"], identity_status=prov["identity_status"],
              conflict=bool(c.get("conflict")))
        _emit("offload", mount=c["mount"], camera=c["camera"], ok=(rc == 0))
        if rc != 0:
            result["errors"].append(f"offload verification FAILED for {c['mount']} — card not safe to format")
            _emit("done", ok=False, errors=result["errors"])
            return result
        result["offloaded"].append(c["mount"])

    if dry_run:
        audit(output, "dry_run_complete")
        _emit("done", ok=True, dry_run=True)
        return result

    # 4) CAPTURE the offloaded shoot folder
    src = Path(dest) / manifest.name
    extra = ["--proxy"] if proxy else []
    _emit("capture_start", source=str(src))
    run_id = _capture(src, output, extra)
    result["run_id"] = run_id
    audit(output, "capture", source=str(src), run_id=run_id)
    _emit("capture", run_id=run_id)
    if not run_id:
        result["errors"].append("CAPTURE produced no run_id — export skipped")
        _emit("done", ok=False, errors=result["errors"])
        return result

    # 5) export FCPXML
    out_xml = output / f"{output.name}_multicam.fcpxml"
    _emit("export_start", out=str(out_xml))
    rc = _export(run_id, out_xml, db, stills)
    result["exported"] = (rc == 0)
    audit(output, "export", out=str(out_xml), rc=rc)
    _emit("export", ok=result["exported"])
    if rc != 0:
        result["errors"].append("FCPXML export failed")
        _emit("done", ok=False, errors=result["errors"])
        return result

    # 6) hand off to FCP + open the Next-Steps guide
    result["opened"] = _open(out_xml)
    guide = REPO / "scripts" / "next_steps_fcp.html"
    if guide.exists():
        _open(guide)
    audit(output, "handoff", opened=result["opened"])
    _emit("done", ok=True, run_id=run_id, opened=result["opened"], errors=result["errors"])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# CLI front end (v1). Subcommands: detect · plan · run · wizard
# ─────────────────────────────────────────────────────────────────────────────
def _print_cards(cards):
    if not cards:
        print("  No camera cards detected under the volumes path.")
        return
    print(f"\n  Detected {len(cards)} card(s):\n")
    for i, c in enumerate(cards, 1):
        cam = c["camera"] or "??? (choose a camera)"
        flag = {"high": "✓", "medium": "~", "low": "?"}.get(c["confidence"], "?")
        print(f"   {i:>2}. [{flag}] {cam:<20} {c['video_count']:>4} video · "
              f"{human(c['bytes']):>9}   {c['mount']}")
    print("\n   ✓ name-matched · ~ guessed from filenames · ? unknown (you choose)")


def _cli(argv=None):
    ap = argparse.ArgumentParser(description="W.E. C.A.P.E. — New Shoot (offload -> CAPTURE -> FCPXML -> FCP).")
    sub = ap.add_subparsers(dest="cmd")

    ap.add_argument("--volumes", default="/Volumes", help="where to look for cards (default /Volumes)")
    ap.add_argument("--max-card-tb", type=float, default=None,
                    help="skip volumes larger than this many TB when detecting (default ~2.5)")

    sub.add_parser("detect", help="list detected camera cards + guessed cameras")

    rp = sub.add_parser("redact", help="write path-hashed *.shared.* copies of a shoot's "
                                       "manifest + session log (for offsite/sharing)")
    rp.add_argument("--output", required=True, help="the shoot's output folder")

    for name in ("plan", "run"):
        p = sub.add_parser(name, help="preview (plan) or execute (run) a new shoot")
        p.add_argument("--name", required=True, help="shoot name (top folder)")
        p.add_argument("--date", default="", help="shoot date YYYY-MM-DD")
        p.add_argument("--location", default="", help="location")
        p.add_argument("--trusted-clock", default="unknown", help="camera whose clock is correct, or 'unknown'")
        p.add_argument("--dest", required=True, help="primary offload destination root")
        p.add_argument("--dest2", help="optional second destination (true two-copy safety)")
        p.add_argument("--output", required=True, help="CAPTURE output folder")
        p.add_argument("--stills", action="append", help="stills folder for the export (repeatable)")
        p.add_argument("--card", action="append", default=[],
                       help="MOUNT=CAMERA override, e.g. '/Volumes/CARD=Insta360 X5' (repeatable)")
        p.add_argument("--no-proxy", action="store_true", help="skip proxy transcode in CAPTURE")

    args = ap.parse_args(argv)
    mcb = int(args.max_card_tb * 1024 ** 4) if args.max_card_tb else None
    if args.cmd == "detect" or args.cmd is None:
        _print_cards(detect_cards(args.volumes, max_card_bytes=mcb))
        return 0

    if args.cmd == "redact":
        w = redact_for_sharing(args.output)
        if not w:
            print("  Nothing to redact (no shoot.yaml / session log in that folder).")
            return 1
        for p in w:
            print(f"  ✓ wrote path-hashed copy: {p}")
        print(f"  ({SHARE_NOTE})")
        return 0

    cards = detect_cards(args.volumes, max_card_bytes=mcb)
    overrides = dict(x.split("=", 1) for x in args.card if "=" in x)
    for c in cards:                                  # apply --card overrides
        if c["mount"] in overrides:
            c["camera"], c["confidence"] = overrides[c["mount"]], "high"
    manifest = ShootManifest(name=args.name, date=args.date, location=args.location,
                             trusted_clock=args.trusted_clock)

    if args.cmd == "plan":
        print("\n  PLAN (nothing will be written):\n")
        for i, s in enumerate(build_plan(manifest, cards, args.dest, args.output,
                                          args.dest2, not args.no_proxy, args.stills), 1):
            print(f"   {i}. {s}")
        unknown = [c["mount"] for c in cards if not c["camera"]]
        if unknown:
            print(f"\n  ⚠ {len(unknown)} card(s) have no camera label — pass --card MOUNT=CAMERA:")
            for m in unknown:
                print(f"      --card '{m}=DJI ACTION 6'")
        print()
        return 0

    res = run_new_shoot(manifest, cards, args.dest, args.output, dest2=args.dest2,
                        stills=args.stills, proxy=not args.no_proxy)
    print("\n  " + ("✓ done" if not res["errors"] else "✗ stopped"))
    for k in ("manifest", "run_id", "exported", "opened"):
        print(f"    {k}: {res[k]}")
    for e in res["errors"]:
        print(f"    ⚠ {e}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(_cli())
