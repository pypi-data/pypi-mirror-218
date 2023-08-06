from __future__ import annotations

from ._core import (
    Container,
    RegisteredService,
    Registry,
    ServiceNotFoundError,
    ServicePing,
)


__all__ = [
    "Registry",
    "RegisteredService",
    "ServiceNotFoundError",
    "ServicePing",
    "Container",
]

try:
    from . import flask  # noqa: F401
except ImportError:
    __all__.append("flask")
