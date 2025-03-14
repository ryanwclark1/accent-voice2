# resources/endpoint_sip/types.py
from pydantic import UUID4, BaseModel


class EndpointSIPAuthSectionOptionsDict(BaseModel):
    """Represents authentication options for a SIP endpoint."""

    username: str


class EndpointSIPLineDict(BaseModel):
    """Represents a line associated with a SIP endpoint."""

    id: int


class EndpointSIPTrunkDict(BaseModel):
    """Represents a trunk associated with a SIP endpoint."""

    id: int


class EndpointSIPRegistrationSectionOptionsDict(BaseModel):
    """Represents registration options for a SIP endpoint."""

    client_uri: str


class EndpointSIPDict(BaseModel):
    """Represents a SIP endpoint."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    label: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict | None = None
    registration_section_options: EndpointSIPRegistrationSectionOptionsDict | None = (
        None  # Typo in original
    )
    trunk: EndpointSIPTrunkDict | None = None
    line: EndpointSIPLineDict | None = None
