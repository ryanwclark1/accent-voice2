# accent_bus/resources/endpoint_custom/types.py
# Copyright 2025 Accent Communications

"""Custom endpoint types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class EndpointCustomLineDict(TypedDict, total=False):
    """Dictionary representing a custom endpoint line."""

    id: int


class EndpointCustomTrunkDict(TypedDict, total=False):
    """Dictionary representing a custom endpoint trunk."""

    id: int


class EndpointCustomDict(TypedDict, total=False):
    """Dictionary representing a custom endpoint."""

    id: int
    tenant_uuid: UUIDStr
    interface: str
    trunk: EndpointCustomTrunkDict
    line: EndpointCustomLineDict
