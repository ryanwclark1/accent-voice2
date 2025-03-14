# resources/endpoint_iax/types.py
from pydantic import UUID4, BaseModel


class EndpointIAXTrunkDict(BaseModel):
    """Represents an IAX trunk."""

    id: int


class EndpointIAXDict(BaseModel):
    """Represents an IAX endpoint."""

    id: int
    tenant_uuid: UUID4
    trunk: EndpointIAXTrunkDict | None = None
