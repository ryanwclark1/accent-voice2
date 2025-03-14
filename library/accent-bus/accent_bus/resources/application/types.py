# resources/application/types.py
from typing import Dict, TypedDict

from pydantic import UUID4


class ApplicationDict(TypedDict, total=False):
    """Represents the structure of an Application dictionary."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    destination: str | None
    destination_options: dict[str, str]
