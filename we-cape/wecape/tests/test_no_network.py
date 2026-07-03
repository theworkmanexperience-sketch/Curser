"""
P2 INVARIANT — the local engine makes NO network calls.

A static guard: no network-capable module may be imported anywhere under wecape/
(the engine), excluding tests/. This turns the "zero network" claim (P2, and the
SECURITY_RISK_ANALYSIS Q3 control) from an assertion into an enforced invariant —
the suite fails the moment someone adds `import requests`, `urllib`, `socket`, etc.

Scope: the ENGINE only. Ops tooling in scripts/ (e.g. the rclone backup) is
deliberately out of scope — P2 is specifically about the local processing engine.

When the OPTIONAL J3 CloudSyncAdapter is built, add its file (e.g. 'sync/cloud.py')
to NETWORK_ALLOWED below — an explicit, code-reviewed, visible exemption. The
engine default stays deny.
"""

import ast
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent          # wecape/

# Top-level module names that imply a network capability.
FORBIDDEN = {
    "socket", "socketserver", "ssl", "urllib", "http", "ftplib", "smtplib",
    "poplib", "imaplib", "nntplib", "telnetlib", "xmlrpc", "webbrowser",
    "requests", "aiohttp", "httpx", "urllib3", "websocket", "websockets",
    "paramiko", "boto3", "botocore", "grpc", "pycurl", "google", "azure",
    "requests_oauthlib", "httplib2",
}

# Explicit, visible allowlist (engine-relative POSIX paths). Empty by design today.
# Future J3 cloud adapter would be added here with a code review, e.g. "sync/cloud.py".
NETWORK_ALLOWED = set()


def _engine_files():
    for p in ENGINE.rglob("*.py"):
        rel = p.relative_to(ENGINE).as_posix()
        if rel.startswith("tests/") or rel in NETWORK_ALLOWED:
            continue
        yield p, rel


def _imported_roots(tree):
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                roots.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:            # absolute imports only
                roots.add(node.module.split(".")[0])
    return roots


def test_engine_has_no_network_imports():
    offenders = []
    for p, rel in _engine_files():
        try:
            tree = ast.parse(p.read_text())
        except (SyntaxError, UnicodeDecodeError):
            continue
        bad = _imported_roots(tree) & FORBIDDEN
        if bad:
            offenders.append(f"{rel}: {sorted(bad)}")
    assert not offenders, (
        "P2 VIOLATION — network-capable import(s) found in the local engine:\n  "
        + "\n  ".join(offenders)
        + "\n(If this is the intentional J3 cloud adapter, add the file to NETWORK_ALLOWED.)"
    )


def test_guard_actually_detects_a_violation():
    """The guard must catch a planted import — proves it isn't vacuously passing."""
    tree = ast.parse("import os\nimport requests\nfrom urllib.request import urlopen\n")
    assert _imported_roots(tree) & FORBIDDEN == {"requests", "urllib"}
