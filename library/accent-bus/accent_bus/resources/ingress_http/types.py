# accent_bus/resources/ingress_http/types.py
# Copyright 2025 Accent Communications

"""Ingress HTTP types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class IngressHTTPDict(TypedDict, total=False):
    """Dictionary representing an HTTP ingress."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    uri: str
