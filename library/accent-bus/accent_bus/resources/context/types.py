# resources/context/types.py
from typing import TypedDict

from pydantic import UUID4


class ContextDict(TypedDict, total=False):
    """Represents context data."""

    id: int
    name: str
    type: str
    tenant_uuid: UUID4
