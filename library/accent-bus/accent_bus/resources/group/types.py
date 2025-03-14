# resources/group/types.py

from pydantic import UUID4, BaseModel


class GroupDict(BaseModel):
    """Represents a group."""

    id: int
    uuid: UUID4
