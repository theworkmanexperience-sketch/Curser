"""
wecape.core.errors
==================
Shared error taxonomy for W.E. C.A.P.E. (Target structure: core/errors.py).

Kept dependency-free so every layer (capture, registry, sync, api) can import
it without creating cycles.
"""


class WeCapeError(Exception):
    """Base class for all W.E. C.A.P.E. errors."""


class ConfigError(WeCapeError):
    """Invalid or missing configuration."""


class StageValidationError(WeCapeError):
    """A stage's validate_input() rejected its inputs."""


class RegistryAuditError(WeCapeError):
    """
    An audit/registry write failed while strict audit mode was active.

    For a compliance-first product, a run that cannot record its audit trail
    must not be reported as a success. Set ``registry.strict: false`` in config
    to downgrade these to warnings and run without a guaranteed audit record.
    """
