# resources/endpoint_sccp/types.py

from pydantic import UUID4, BaseModel


class EndpointSCCPLineDict(BaseModel):
    """Represents an SCCP line."""

    id: int


class EndpointSCCPDict(BaseModel):
    """Represents an SCCP endpoint."""

    id: int
    tenant_uuid: UUID4
    line: EndpointSCCPLineDict | None = None
