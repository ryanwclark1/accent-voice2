# resources/line_endpoint/types.py

from typing import TypedDict

from pydantic import UUID4


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    """Represents authentication options for a SIP endpoint."""

    username: str


class LineEndpointSIPDict(TypedDict, total=False):
    """Represents a SIP endpoint for a line."""

    uuid: UUID4
    tenant_uuid: UUID4
    label: str
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict


class LineEndpointSCCPDict(TypedDict, total=False):
    """Represents an SCCP endpoint for a line."""

    id: int
    tenant_uuid: UUID4


class LineEndpointCustomDict(TypedDict, total=False):
    """Represents a custom endpoint for a line."""

    id: int
    tenant_uuid: UUID4
    interface: str


class LineDict(TypedDict, total=False):
    """Represents line information."""

    id: int
    tenant_uuid: UUID4
    name: str
