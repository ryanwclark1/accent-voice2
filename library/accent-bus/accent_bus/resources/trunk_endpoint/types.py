# resources/trunk_endpoint/types.py
from typing import TypedDict

from pydantic import UUID4


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    """Represents authentication options for a SIP endpoint."""

    username: str


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    """Represents registration options for a SIP endpoint."""

    client_uri: str


class EndpointSIPDict(TypedDict, total=False):
    """Represents a SIP endpoint."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    registration_section_options: EndpointSIPRegistrationSectionOptionsDict


class EndpointIAXDict(TypedDict, total=False):
    """Represents an IAX endpoint."""

    id: int
    tenant_uuid: UUID4
    name: str


class EndpointCustomDict(TypedDict, total=False):
    """Represents a custom endpoint."""

    id: int
    tenant_uuid: UUID4
    interface: str


class TrunkDict(TypedDict, total=False):
    """Represents a trunk."""

    id: int
    tenant_uuid: UUID4
