# accent_bus/resources/endpoint_iax/types.py
# Copyright 2025 Accent Communications

"""IAX endpoint types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class EndpointIAXTrunkDict(TypedDict, total=False):
    """Dictionary representing an IAX endpoint trunk."""

    id: int


class EndpointIAXDict(TypedDict, total=False):
    """Dictionary representing an IAX endpoint."""

    id: int
    tenant_uuid: UUIDStr
    trunk: EndpointIAXTrunkDict
