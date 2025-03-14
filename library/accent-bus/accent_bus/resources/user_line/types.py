# resources/user_line/types.py
from pydantic import UUID4, BaseModel


class EndpointCustomDict(BaseModel):
    """Represents a custom endpoint."""

    id: int


class EndpointSCCPDict(BaseModel):
    """Represents an SCCP endpoint."""

    id: int


class EndpointSIPDict(BaseModel):
    """Represents a SIP endpoint."""

    uuid: UUID4


class LineDict(BaseModel):
    """Represents a line."""

    id: int
    name: str
    endpoint_sip: EndpointSIPDict | None = None
    endpoint_sccp: EndpointSCCPDict | None = None
    endpoint_custom: EndpointCustomDict | None = None
    # Removed tenant_uuid, as it is already in the base class


class UserDict(BaseModel):
    """Represents a user."""

    id: int
    uuid: UUID4
    tenant_uuid: UUID4  # Include tenant_uuid here
