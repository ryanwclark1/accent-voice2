# resources/endpoint_custom/types.py
from typing import TypedDict

from pydantic import UUID4


class EndpointCustomLineDict(TypedDict, total=False):
    """Represents a custom endpoint line."""

    id: int


class EndpointCustomTrunkDict(TypedDict, total=False):
    """Represents a custom endpoint trunk."""

    id: int


class EndpointCustomDict(TypedDict, total=False):
    """Represents a custom endpoint."""

    id: int
    tenant_uuid: UUID4
    interface: str
    trunk: EndpointCustomTrunkDict
    line: EndpointCustomLineDict
