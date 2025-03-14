# resources/chatd/types.py
from typing import TypedDict

from pydantic import UUID4


class LinePresenceDict(TypedDict, total=False):
    """Represents presence information for a line."""

    id: int
    state: str


class MessageDict(TypedDict, total=False):
    """Represents a chat message."""

    uuid: UUID4
    content: str
    alias: str
    user_uuid: UUID4
    tenant_uuid: UUID4
    accent_uuid: UUID4
    created_at: str
    room: "RoomDict"  # Forward reference for circular dependency


class RoomUserDict(TypedDict, total=False):
    """Represents a user within a chat room."""

    uuid: UUID4
    tenant_uuid: UUID4
    accent_uuid: UUID4


class RoomDict(TypedDict, total=False):
    """Represents a chat room."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    users: list[RoomUserDict]


class UserPresenceDict(TypedDict, total=False):
    """Represents the presence status of a user."""

    uuid: UUID4
    tenant_uuid: UUID4
    state: str
    status: str
    last_activity: str
    line_state: str
    mobile: bool
    do_not_disturb: bool
    connected: bool
    lines: list[LinePresenceDict]
