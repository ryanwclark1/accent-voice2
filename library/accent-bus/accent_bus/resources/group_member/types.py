# resources/group_member/types.py
from typing import TypedDict


class GroupExtensionDict(TypedDict, total=False):
    """Represents a group extension."""

    exten: str
    context: str
