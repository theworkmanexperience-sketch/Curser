#!/usr/bin/env python3
"""
W.E. C.A.P.E. — Annotations store + CLI  (ops tooling, NOT the engine)

Human-authored notes on shoots (runs) and clips, kept in a SEPARATE SQLite file
(default ~/.wecape/annotations.db) so the deterministic production registry
(wecape.db) stays pure. "What the pipeline produced" (engine-owned, deterministic
— P1) is never mixed with "what the human noted" (freely mutable CRUD).

Design constraints (match the dashboard's locked ethos):
  • stdlib only · zero network · no server.
  • The dashboard opens THIS db mode=ro and renders it; ALL writes go through here.
  • Soft-delete (archive) by default — notes are never silently destroyed; --hard purges.

Targets:
  • scope 'shoot' -> target_id is a run_id   (the dashboard card key, runs.id)
  • scope 'clip'  -> target_id is a clip SHA (the per-clip table key, content.id)
Use `targets` to list valid run_ids / clip SHAs straight from the registry (read-only).

Examples:
  python3 scripts/annotations.py targets
  python3 scripts/annotations.py add --scope shoot --target WEF_20260630_125435_06980D \\
      --label "O-SIX Community Service" --body "Client wants a 90s cut." --tags deliverable,priority
  python3 scripts/annotations.py add --scope clip --target <sha256> --body "Best take." --tags select
  python3 scripts/annotations.py list
  python3 scripts/annotations.py edit a1b2c3d4 --body "Client wants 60s."
  python3 scripts/annotations.py rm a1b2c3d4          # archive (soft)
  python3 scripts/annotations.py rm a1b2c3d4 --hard   # purge
  python3 scripts/annotations.py restore a1b2c3d4
"""

import argparse
import json
import sqlite3
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB = Path.home() / ".wecape" / "annotations.db"
DEFAULT_REGISTRY = Path.home() / ".wecape" / "registry" / "wecape.db"
SCHEMA_VERSION = 1
VALID_SCOPES = ("shoot", "clip")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS annotations (
    id           TEXT PRIMARY KEY,
    scope        TEXT NOT NULL,            -- 'shoot' (run_id) | 'clip' (content SHA)
    target_id    TEXT NOT NULL,
    target_label TEXT,                     -- folder name / filename for display
    body         TEXT NOT NULL,
    tags         TEXT,                     -- normalized comma-separated
    author       TEXT,
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL,
    archived     INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_ann_target ON annotations(scope, target_id, archived);
CREATE TABLE IF NOT EXISTS annotations_schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL,
    description TEXT
);
"""


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_id():
    return uuid.uuid4().hex[:8]


def _norm_tags(tags):
    """Accept a list or a comma string -> normalized comma string (trim, dedup, keep order)."""
    if not tags:
        return None
    parts = tags.split(",") if isinstance(tags, str) else [str(t) for t in tags]
    seen, out = set(), []
    for raw in parts:
        t = raw.strip()
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return ",".join(out) or None


class AnnotationStore:
    """CRUD over annotations.db. Each call opens/commits/closes its own connection."""

    def __init__(self, db_path=DEFAULT_DB):
        self.db_path = Path(db_path)

    @contextmanager
    def _conn(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        c = sqlite3.connect(str(self.db_path))
        c.row_factory = sqlite3.Row
        try:
            yield c
            c.commit()
        finally:
            c.close()

    def init_db(self):
        """Create schema if absent. Idempotent — safe to call before every op."""
        with self._conn() as c:
            c.executescript(SCHEMA_SQL)
            cur = c.execute("SELECT MAX(version) FROM annotations_schema_version").fetchone()[0]
            if not cur:
                c.execute(
                    "INSERT INTO annotations_schema_version(version, applied_at, description) "
                    "VALUES (?,?,?)",
                    (SCHEMA_VERSION, _now(), "initial annotations schema"),
                )
        return self

    def add(self, scope, target_id, body, label=None, tags=None, author=None):
        if scope not in VALID_SCOPES:
            raise ValueError(f"scope must be one of {VALID_SCOPES}, got {scope!r}")
        if not target_id:
            raise ValueError("target_id is required")
        if not (body and body.strip()):
            raise ValueError("body must be non-empty")
        self.init_db()
        aid, now = _short_id(), _now()
        with self._conn() as c:
            c.execute(
                "INSERT INTO annotations "
                "(id,scope,target_id,target_label,body,tags,author,created_at,updated_at,archived) "
                "VALUES (?,?,?,?,?,?,?,?,?,0)",
                (aid, scope, target_id, label, body.strip(), _norm_tags(tags), author, now, now),
            )
        return aid

    def get(self, aid):
        self.init_db()
        with self._conn() as c:
            r = c.execute("SELECT * FROM annotations WHERE id=?", (aid,)).fetchone()
            return dict(r) if r else None

    def list(self, scope=None, target_id=None, include_archived=False):
        self.init_db()
        q, p = ["SELECT * FROM annotations WHERE 1=1"], []
        if not include_archived:
            q.append("AND archived=0")
        if scope:
            q.append("AND scope=?"); p.append(scope)
        if target_id:
            q.append("AND target_id=?"); p.append(target_id)
        q.append("ORDER BY created_at DESC")
        with self._conn() as c:
            return [dict(r) for r in c.execute(" ".join(q), p)]

    def edit(self, aid, body=None, label=None, tags=None, author=None):
        self.init_db()
        sets, p = [], []
        if body is not None:
            if not body.strip():
                raise ValueError("body must be non-empty")
            sets.append("body=?"); p.append(body.strip())
        if label is not None:
            sets.append("target_label=?"); p.append(label)
        if tags is not None:
            sets.append("tags=?"); p.append(_norm_tags(tags))
        if author is not None:
            sets.append("author=?"); p.append(author)
        if not sets:
            return False
        sets.append("updated_at=?"); p.append(_now())
        p.append(aid)
        with self._conn() as c:
            return c.execute(f"UPDATE annotations SET {','.join(sets)} WHERE id=?", p).rowcount > 0

    def archive(self, aid, archived=True):
        """Soft-delete (default) or restore."""
        self.init_db()
        with self._conn() as c:
            return c.execute(
                "UPDATE annotations SET archived=?, updated_at=? WHERE id=?",
                (1 if archived else 0, _now(), aid),
            ).rowcount > 0

    def delete(self, aid):
        """Hard delete — irreversible."""
        self.init_db()
        with self._conn() as c:
            return c.execute("DELETE FROM annotations WHERE id=?", (aid,)).rowcount > 0


# ── registry read-only helper: discover valid targets ───────────────────────
def registry_targets(registry_path=DEFAULT_REGISTRY, clip_limit=0):
    """Read the registry mode=ro and list valid shoot (run) + clip targets."""
    rp = Path(registry_path)
    if not rp.exists():
        return {"runs": [], "clips": [], "error": f"registry not found: {rp}"}
    uri = f"file:{rp.resolve().as_posix()}?mode=ro"
    c = sqlite3.connect(uri, uri=True)
    c.row_factory = sqlite3.Row
    try:
        runs = [
            {"run_id": r["id"],
             "shoot": Path(r["output_path"] or "").name or r["id"],
             "files": r["file_count"], "timestamp": r["timestamp"]}
            for r in c.execute(
                "SELECT id,output_path,file_count,timestamp FROM runs "
                "WHERE file_count>0 ORDER BY timestamp DESC")
        ]
        clips = []
        if clip_limit:
            clips = [
                {"clip_id": r["id"], "filename": r["filename"], "camera": r["camera_family"]}
                for r in c.execute(
                    "SELECT id,filename,camera_family FROM content ORDER BY filename LIMIT ?",
                    (clip_limit,))
            ]
        return {"runs": runs, "clips": clips, "error": None}
    except sqlite3.Error as e:
        return {"runs": [], "clips": [], "error": str(e)}
    finally:
        c.close()


# ── CLI ──────────────────────────────────────────────────────────────────────
def _fmt(a):
    tags = f"  [{a['tags']}]" if a.get("tags") else ""
    who = f"  ({a['author']})" if a.get("author") else ""
    arch = "  ARCHIVED" if a.get("archived") else ""
    label = a.get("target_label") or a.get("target_id")
    return (f"{a['id']}  {a['scope']:<5}  {label}\n"
            f"    {a['body']}{tags}{who}\n"
            f"    updated {a.get('updated_at', '')[:19]}{arch}")


def main(argv=None):
    # Shared flags attached to every subcommand, so `--db`/`--json` work AFTER
    # the verb (git-style) — e.g. `annotations.py list --json`, `get <id> --json`.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", type=Path, default=DEFAULT_DB,
                        help=f"annotations db (default {DEFAULT_DB})")
    common.add_argument("--json", action="store_true", help="machine-readable output")

    ap = argparse.ArgumentParser(
        description="W.E. C.A.P.E. annotations — notes on shoots/clips in a separate annotations.db.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("add", parents=[common], help="create a note")
    sp.add_argument("--scope", required=True, choices=VALID_SCOPES)
    sp.add_argument("--target", required=True, help="run_id (shoot) or clip SHA (clip)")
    sp.add_argument("--body", required=True)
    sp.add_argument("--label", help="display label (shoot/file name)")
    sp.add_argument("--tags", help="comma-separated")
    sp.add_argument("--author")

    sp = sub.add_parser("list", parents=[common], help="list notes")
    sp.add_argument("--scope", choices=VALID_SCOPES)
    sp.add_argument("--target")
    sp.add_argument("--all", action="store_true", help="include archived")

    sp = sub.add_parser("get", parents=[common], help="show one note"); sp.add_argument("id")

    sp = sub.add_parser("edit", parents=[common], help="change a note")
    sp.add_argument("id")
    sp.add_argument("--body"); sp.add_argument("--label"); sp.add_argument("--tags"); sp.add_argument("--author")

    sp = sub.add_parser("rm", parents=[common], help="archive (soft) or purge a note")
    sp.add_argument("id"); sp.add_argument("--hard", action="store_true", help="purge instead of archive")

    sp = sub.add_parser("restore", parents=[common], help="un-archive a note"); sp.add_argument("id")

    sp = sub.add_parser("targets", parents=[common], help="list valid targets from the registry (read-only)")
    sp.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    sp.add_argument("--clips", type=int, default=0, help="also list up to N clip SHAs")

    sub.add_parser("init", parents=[common], help="create the annotations db (no-op if it exists)")

    args = ap.parse_args(argv)
    store = AnnotationStore(args.db)

    if args.cmd == "targets":
        t = registry_targets(args.registry, clip_limit=args.clips)
        if args.json:
            print(json.dumps(t, indent=2)); return 0
        if t["error"]:
            print(f"[!] {t['error']}", file=sys.stderr); return 1
        print(f"Shoots (scope 'shoot' · --target <run_id>) — {len(t['runs'])}:")
        for r in t["runs"]:
            print(f"  {r['run_id']}  {r['files']:>4} files  {r['timestamp'][:19]}  {r['shoot']}")
        if args.clips:
            print(f"\nClips (scope 'clip' · --target <SHA>) — first {len(t['clips'])}:")
            for c in t["clips"]:
                print(f"  {c['clip_id'][:16]}…  {c['camera'] or '—':<20}  {c['filename']}")
        return 0

    if args.cmd == "init":
        store.init_db()
        print(f"✓ annotations db ready: {store.db_path}"); return 0

    if args.cmd == "add":
        aid = store.add(args.scope, args.target, args.body,
                        label=args.label, tags=args.tags, author=args.author)
        print(json.dumps({"id": aid}) if args.json else f"✓ added {aid}"); return 0

    if args.cmd == "list":
        rows = store.list(scope=args.scope, target_id=args.target, include_archived=args.all)
        if args.json:
            print(json.dumps(rows, indent=2)); return 0
        if not rows:
            print("(no annotations)"); return 0
        for a in rows:
            print(_fmt(a)); print()
        return 0

    if args.cmd == "get":
        a = store.get(args.id)
        if not a:
            print("(not found)", file=sys.stderr); return 1
        print(json.dumps(a, indent=2) if args.json else _fmt(a)); return 0

    if args.cmd == "edit":
        ok = store.edit(args.id, body=args.body, label=args.label, tags=args.tags, author=args.author)
        print(("✓ updated " if ok else "(no change / not found) ") + args.id); return 0 if ok else 1

    if args.cmd == "rm":
        ok = store.delete(args.id) if args.hard else store.archive(args.id, True)
        verb = "purged" if args.hard else "archived"
        print((f"✓ {verb} " if ok else "(not found) ") + args.id); return 0 if ok else 1

    if args.cmd == "restore":
        ok = store.archive(args.id, False)
        print(("✓ restored " if ok else "(not found) ") + args.id); return 0 if ok else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
