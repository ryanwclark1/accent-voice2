# resources/endpoint_sccp/types.py
from typing import TypedDict

from pydantic import UUID4


class EndpointSCCPLineDict(TypedDict, total=False):
    """Represents an SCCP line."""

    id: int


class EndpointSCCPDict(TypedDict, total=False):
    """Represents an SCCP endpoint."""

    id: int
    tenant_uuid: UUID4
    line: EndpointSCCPLineDict
