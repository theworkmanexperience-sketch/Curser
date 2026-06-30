"""
Annotations layer — store CRUD (scripts/annotations.py) + dashboard read/render
(scripts/dashboard.py).

Annotations live in a SEPARATE annotations.db (not the deterministic registry),
written only by the CLI, read mode=ro by the dashboard. These tests pin: schema
idempotency, CRUD + soft-delete, tag/body normalization, scope validation, and
that the dashboard loads + renders notes (HTML-escaped) without touching wecape.db.
"""

import sqlite3
import sys
import tempfile
from pathlib import Path

# scripts/ is not a package — put it on the path so we can import the ops tools.
_REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import annotations as ann_mod          # scripts/annotations.py
import dashboard as dash               # scripts/dashboard.py


def _store(tmp):
    return ann_mod.AnnotationStore(Path(tmp) / "annotations.db")


# ── schema ────────────────────────────────────────────────────────────────
def test_init_is_idempotent():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.init_db()
        s.init_db()  # second call must not duplicate the version row or error
        c = sqlite3.connect(str(s.db_path))
        rows = list(c.execute("SELECT version FROM annotations_schema_version"))
        c.close()
        assert rows == [(1,)]


# ── create / read ───────────────────────────────────────────────────────────
def test_add_and_get_trims_body():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        aid = s.add("shoot", "WEF_R", "  90s cut.  ", label="O-SIX", author="T")
        got = s.get(aid)
        assert got["body"] == "90s cut."           # trimmed
        assert got["scope"] == "shoot"
        assert got["target_id"] == "WEF_R"
        assert got["target_label"] == "O-SIX"
        assert got["archived"] == 0


def test_scope_validation():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        for bad in ("run", "RUN", "", "movie"):
            try:
                s.add(bad, "T", "x")
                assert False, f"expected ValueError for scope={bad!r}"
            except ValueError:
                pass


def test_empty_body_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        for bad in ("", "   ", "\n\t"):
            try:
                s.add("clip", "sha", bad)
                assert False, "expected ValueError for empty body"
            except ValueError:
                pass


def test_tag_normalization_dedup_and_trim():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        aid = s.add("clip", "sha", "note", tags=" select , Select ,  hero ,select")
        assert s.get(aid)["tags"] == "select,hero"   # trimmed, case-insensitive dedup, order kept


# ── list / filter ─────────────────────────────────────────────────────────
def test_list_filters_by_scope_and_target():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.add("shoot", "R1", "a")
        s.add("clip", "C1", "b")
        s.add("clip", "C2", "c")
        assert len(s.list()) == 3
        assert len(s.list(scope="clip")) == 2
        assert len(s.list(scope="shoot")) == 1
        assert len(s.list(target_id="C1")) == 1


# ── update ──────────────────────────────────────────────────────────────────
def test_edit_changes_body_and_bumps_updated_at():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        aid = s.add("shoot", "R", "old")
        before = s.get(aid)
        assert s.edit(aid, body="new", tags="x,y") is True
        after = s.get(aid)
        assert after["body"] == "new"
        assert after["tags"] == "x,y"
        assert after["updated_at"] >= before["updated_at"]
        assert after["created_at"] == before["created_at"]   # created is stable


def test_edit_noop_returns_false():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        aid = s.add("shoot", "R", "x")
        assert s.edit(aid) is False   # nothing to change


# ── soft-delete / restore / hard-delete ─────────────────────────────────────
def test_archive_hides_then_restore_shows():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        aid = s.add("shoot", "R", "keep")
        assert s.archive(aid) is True
        assert s.list() == []                       # default excludes archived
        assert len(s.list(include_archived=True)) == 1
        assert s.archive(aid, archived=False) is True
        assert len(s.list()) == 1                    # restored


def test_hard_delete_is_permanent():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        aid = s.add("shoot", "R", "x")
        assert s.delete(aid) is True
        assert s.get(aid) is None
        assert s.list(include_archived=True) == []


# ── dashboard read + render (read-only, HTML-escaped) ───────────────────────
def test_dashboard_loads_index_and_renders():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.add("shoot", "WEF_R", "Ninety second cut.", label="O-SIX", tags="deliverable")
        s.add("clip", "sha_1", "Keeper take.", tags="select")
        idx = dash.load_annotations(s.db_path)
        assert idx["shoot"]["WEF_R"][0]["body"] == "Ninety second cut."
        assert idx["clip"]["sha_1"][0]["body"] == "Keeper take."
        assert len(idx["all"]) == 2

        section = dash.annotations_section(idx)
        assert "Ninety second cut." in section and "deliverable" in section
        card = dash.card_annotations_html(idx["shoot"]["WEF_R"])
        assert "Ninety second cut." in card and "📝" in card


def test_dashboard_load_excludes_archived():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.add("shoot", "R", "keep me")
        gone = s.add("shoot", "R", "archive me")
        s.archive(gone)
        idx = dash.load_annotations(s.db_path)
        bodies = [a["body"] for a in idx["all"]]
        assert "keep me" in bodies and "archive me" not in bodies


def test_dashboard_render_escapes_html():
    with tempfile.TemporaryDirectory() as tmp:
        s = _store(tmp)
        s.add("shoot", "R", "<script>alert(1)</script>")
        idx = dash.load_annotations(s.db_path)
        section = dash.annotations_section(idx)
        assert "<script>alert(1)</script>" not in section
        assert "&lt;script&gt;" in section


def test_dashboard_missing_db_is_empty():
    idx = dash.load_annotations(Path("/nonexistent/never/here.db"))
    assert idx == {"shoot": {}, "clip": {}, "all": []}


def test_dashboard_empty_state_message():
    empty = {"shoot": {}, "clip": {}, "all": []}
    assert "No annotations yet" in dash.annotations_section(empty)
