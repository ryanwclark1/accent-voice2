# resources/endpoint_sip/types.py
from typing import TypedDict

from pydantic import UUID4


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    """Represents authentication options for a SIP endpoint."""

    username: str


class EndpointSIPLineDict(TypedDict, total=False):
    """Represents a line associated with a SIP endpoint."""

    id: int


class EndpointSIPTrunkDict(TypedDict, total=False):
    """Represents a trunk associated with a SIP endpoint."""

    id: int


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    """Represents registration options for a SIP endpoint."""

    client_uri: str


class EndpointSIPDict(TypedDict, total=False):
    """Represents a SIP endpoint."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    label: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    regsitration_section_options: (
        EndpointSIPRegistrationSectionOptionsDict  # Typo in original
    )
    trunk: EndpointSIPTrunkDict
    line: EndpointSIPLineDict
