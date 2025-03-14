# resources/group/types.py
from pydantic import BaseModel, UUID4


class GroupDict(BaseModel):
    """Represents a group."""

    id: int
    uuid: UUID4
