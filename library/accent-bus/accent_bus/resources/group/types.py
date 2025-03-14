# resources/group/types.py
from typing import TypedDict

from pydantic import UUID4


class GroupDict(TypedDict, total=False):
    """Represents a group."""

    id: int
    uuid: UUID4
