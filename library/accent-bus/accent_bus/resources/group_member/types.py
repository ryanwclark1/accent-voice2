# resources/group_member/types.py

from pydantic import BaseModel


class GroupExtensionDict(BaseModel):
    """Represents a group extension."""

    exten: str
    context: str
