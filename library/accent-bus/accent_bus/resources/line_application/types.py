# resources/line_application/types.py

from pydantic import UUID4, BaseModel


class ApplicationDict(BaseModel):
    """Represents an application (for association with a line)."""

    uuid: UUID4


class LineEndpointSIPDict(BaseModel):
    """Represents a SIP endpoint associated with a line."""

    uuid: UUID4


class LineEndpointSCCPDict(BaseModel):
    """Represents an SCCP endpoint associated with a line."""

    id: int


class LineEndpointCustomDict(BaseModel):
    """Represents a custom endpoint associated with a line."""

    id: int


class LineDict(BaseModel):
    """Represents a line with associated endpoint information."""

    id: int
    name: str
    endpoint_sip: LineEndpointSIPDict | None = None
    endpoint_sccp: LineEndpointSCCPDict | None = None
    endpoint_custom: LineEndpointCustomDict | None = None
    tenant_uuid: UUID4 | None = None
