"""
wecape.core.sync
=================
SyncAdapter — interface for all sync implementations.

The local engine ONLY calls methods on this interface.
Cloud implementation details are never visible to the pipeline.

v1: LocalOnlySyncAdapter (default, does nothing)
v2: LANSyncAdapter (team sync, no cloud)
v3: CloudSyncAdapter (optional, explicit user consent)

Privacy guarantee: the local engine is architecturally incapable
of making network calls. This is verifiable by code inspection.
"""

from abc import ABC, abstractmethod
from typing import Optional


class SyncAdapter(ABC):
    """Interface for all sync implementations."""

    @abstractmethod
    def is_available(self) -> bool:
        """Can this adapter currently sync?"""
        pass

    @abstractmethod
    def push_run(self, manifest: dict) -> bool:
        """Persist run data to sync target. Returns success."""
        pass

    @abstractmethod
    def push_registry_delta(self, delta: dict) -> bool:
        """Sync only changed registry records."""
        pass

    @abstractmethod
    def pull_shared_library(self, team_id: str) -> Optional[dict]:
        """Pull team-shared content library."""
        pass

    @abstractmethod
    def get_sync_status(self) -> dict:
        """Return current sync status for UI display."""
        pass


class LocalOnlySyncAdapter(SyncAdapter):
    """
    Default v1 implementation.
    All methods are safe no-ops.
    Zero network calls. Zero external dependencies.
    """

    def is_available(self) -> bool:
        return True

    def push_run(self, manifest: dict) -> bool:
        return True

    def push_registry_delta(self, delta: dict) -> bool:
        return True

    def pull_shared_library(self, team_id: str) -> Optional[dict]:
        return None

    def get_sync_status(self) -> dict:
        return {
            "mode": "local",
            "status": "active",
            "last_sync": None
        }
