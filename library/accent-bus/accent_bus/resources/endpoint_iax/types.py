# resources/endpoint_iax/types.py
from typing import TypedDict

from pydantic import UUID4


class EndpointIAXTrunkDict(TypedDict, total=False):
    """Represents an IAX trunk."""

    id: int


class EndpointIAXDict(TypedDict, total=False):
    """Represents an IAX endpoint."""

    id: int
    tenant_uuid: UUID4
    trunk: EndpointIAXTrunkDict
