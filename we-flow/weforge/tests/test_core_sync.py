"""Tests for weforge.core.sync — SyncAdapter interface."""

import pytest
from weforge.core.sync import SyncAdapter, LocalOnlySyncAdapter


def test_sync_adapter_cannot_be_instantiated():
    with pytest.raises(TypeError):
        SyncAdapter()


def test_local_only_is_always_available():
    adapter = LocalOnlySyncAdapter()
    assert adapter.is_available() is True


def test_local_only_push_run_returns_true():
    adapter = LocalOnlySyncAdapter()
    assert adapter.push_run({"run_id": "test"}) is True


def test_local_only_push_registry_delta_returns_true():
    adapter = LocalOnlySyncAdapter()
    assert adapter.push_registry_delta({"delta": []}) is True


def test_local_only_pull_shared_library_returns_none():
    adapter = LocalOnlySyncAdapter()
    assert adapter.pull_shared_library("team-001") is None


def test_local_only_sync_status():
    adapter = LocalOnlySyncAdapter()
    status = adapter.get_sync_status()
    assert status["mode"] == "local"
    assert status["status"] == "active"
    assert status["last_sync"] is None


def test_local_only_makes_no_network_calls():
    """Verify LocalOnlySyncAdapter has no network imports."""
    import inspect
    import weforge.core.sync as sync_module
    source = inspect.getsource(sync_module)
    assert "import requests" not in source
    assert "import urllib" not in source
    assert "import http" not in source
