#!/usr/bin/env python3
"""Gate ledger enumerator — answers 'Is anything closed?' for the whole repository.

Conforms to WET-SPEC-GATE-001 v1.0. Discovery is by the `gate_class: EXECUTION_GATE`
marker, never by filename: filenames drift, markers do not.

Exit codes (so this can be a CI check, not a habit):
  0  every gate OPEN and none stale
  1  one or more gates CLOSED
  2  one or more gates STALE or NON-CONFORMING (reported even if all are OPEN)

Usage: python3 scripts/gate_status.py [root] [--json]
"""
import sys, os, json, datetime, re

try:
    import yaml
except ImportError:
    sys.stderr.write("gate_status: PyYAML required (pip install pyyaml)\n")
    sys.exit(2)

MARKER = re.compile(r'^gate_class:\s*EXECUTION_GATE\s*$', re.M)
REQUIRED = ["gate_class", "gate_kind", "gate_id", "schema_version", "scope", "subject",
            "state", "authorized", "unblock_condition", "blocking_items", "authority",
            "issued", "review_by", "status_history", "composition", "on_open"]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", "_to_delete"}


def discover(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith((".yaml", ".yml")):
                continue
            p = os.path.join(dirpath, fn)
            try:
                head = open(p, encoding="utf-8", errors="replace").read(8192)
            except OSError:
                continue
            if MARKER.search(head):
                found.append(p)
    return sorted(found)


def assess(path, today):
    row = {"path": path, "findings": []}
    try:
        d = yaml.safe_load(open(path, encoding="utf-8"))
    except Exception as e:
        row.update(gate_id=os.path.basename(path), state="UNREADABLE", authorized=False,
                   conforming=False)
        row["findings"].append(f"unparseable: {type(e).__name__}")
        return row

    missing = [k for k in REQUIRED if k not in d]
    row["gate_id"] = d.get("gate_id", os.path.basename(path))
    row["kind"] = d.get("gate_kind", "?")
    row["scope"] = d.get("scope", "?")
    row["subject"] = d.get("subject", "")
    row["state"] = d.get("state", "?")
    row["conforming"] = not missing
    # A non-conforming gate fails shut (standard section 3).
    row["authorized"] = bool(d.get("authorized")) and not missing
    if missing:
        row["findings"].append("NON-CONFORMING, missing: " + ", ".join(missing))

    items = d.get("blocking_items") or []
    open_items = [i for i in items if str(i.get("status", "")).upper() == "OPEN"]
    row["blocking_total"] = len(items)
    row["blocking_open"] = len(open_items)

    rb = d.get("review_by")
    if rb:
        try:
            if datetime.date.fromisoformat(str(rb)) < today:
                row["findings"].append(f"STALE: review_by {rb} has passed")
        except ValueError:
            row["findings"].append(f"review_by not an ISO date: {rb!r}")

    if row["state"] == "CLOSED" and items and not open_items:
        row["findings"].append(
            "STALE: every blocking item is resolved but state is still CLOSED")
    if row["state"] == "OPEN" and open_items:
        row["findings"].append(
            f"INCONSISTENT: state OPEN with {len(open_items)} blocking item(s) still OPEN")
    return row


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = args[0] if args else "."
    as_json = "--json" in sys.argv
    today = datetime.date.today()

    rows = [assess(p, today) for p in discover(root)]
    closed = [r for r in rows if not r["authorized"]]
    flagged = [r for r in rows if r["findings"]]

    if as_json:
        print(json.dumps({"gate_count": len(rows), "all_open": not closed,
                          "closed": len(closed), "flagged": len(flagged),
                          "gates": rows}, indent=1))
    else:
        print(f"Gate ledger — {len(rows)} gate(s) discovered under {os.path.abspath(root)}")
        print()
        for r in rows:
            mark = "OPEN  " if r["authorized"] else "CLOSED"
            print(f"  [{mark}] {r['gate_id']}  ({r['kind']}/{r['scope']})")
            print(f"           {r['subject']}")
            if r.get("blocking_total"):
                print(f"           blocking: {r['blocking_open']} open of {r['blocking_total']}")
            for f in r["findings"]:
                print(f"           ! {f}")
            print(f"           {r['path']}")
            print()
        print("IS GATE OPEN? " + ("YES — all gates open." if not closed
                                  else f"NO — {len(closed)} of {len(rows)} closed."))
        if len(rows) > 8:
            print(f"NOTE: {len(rows)} gates in the ledger. Gate proliferation is a governance risk "
                  f"(WET-SPEC-GATE-001 section 7) — prefer scoping up over declaring more.")

    if flagged and not closed:
        return 2
    return 1 if closed else 0


if __name__ == "__main__":
    sys.exit(main())
