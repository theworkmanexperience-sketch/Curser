"""
Tests for strict audit mode (CODEBASE_AUDIT_2026-06-23 finding #4).

A compliance-first product must not silently complete a run when its audit
record cannot be written. _audit_failure encodes that policy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from wecape.capture.pipeline import _audit_failure
from wecape.core.errors import RegistryAuditError


def test_strict_mode_raises_on_audit_failure():
    raised = False
    try:
        _audit_failure(strict=True, test_mode=False,
                       phase="write_run", exc=ValueError("db locked"))
    except RegistryAuditError as e:
        raised = True
        assert "strict audit mode" in str(e).lower()
    assert raised, "strict mode must abort the run on audit failure"


def test_non_strict_mode_does_not_raise():
    # Should return normally (warning only), not raise.
    _audit_failure(strict=False, test_mode=False,
                   phase="write_run", exc=ValueError("db locked"))


def test_test_mode_never_raises_even_when_strict():
    # Test mode intentionally skips the production registry; never abort on it.
    _audit_failure(strict=True, test_mode=True,
                   phase="registry-init", exc=ValueError("no db"))
