# resources/endpoint_custom/types.py
from pydantic import UUID4, BaseModel


class EndpointCustomLineDict(BaseModel):
    """Represents a custom endpoint line."""

    id: int


class EndpointCustomTrunkDict(BaseModel):
    """Represents a custom endpoint trunk."""

    id: int


class EndpointCustomDict(BaseModel):
    """Represents a custom endpoint."""

    id: int
    tenant_uuid: UUID4
    interface: str
    trunk: EndpointCustomTrunkDict | None = None
    line: EndpointCustomLineDict | None = None
