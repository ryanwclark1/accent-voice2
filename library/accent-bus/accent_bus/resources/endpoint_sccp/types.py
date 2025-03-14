# accent_bus/resources/endpoint_sccp/types.py
# Copyright 2025 Accent Communications

"""SCCP endpoint types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class EndpointSCCPLineDict(TypedDict, total=False):
    """Dictionary representing an SCCP endpoint line."""

    id: int


class EndpointSCCPDict(TypedDict, total=False):
    """Dictionary representing an SCCP endpoint."""

    id: int
    tenant_uuid: UUIDStr
    line: EndpointSCCPLineDict
