# resources/ingress_http/types.py

from typing import TypedDict

from pydantic import UUID4


class IngressHTTPDict(TypedDict, total=False):
    """Represents an Ingress HTTP configuration (using TypedDict)."""

    uuid: UUID4
    tenant_uuid: UUID4
    uri: str
