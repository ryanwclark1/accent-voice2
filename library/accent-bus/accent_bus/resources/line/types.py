# resources/line/types.py
from typing import TypedDict

from pydantic import UUID4


class LineDict(TypedDict, total=False):
    """Represents a line."""

    id: int
    protocol: str
    name: str
    tenant_uuid: UUID4
