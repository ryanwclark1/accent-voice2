# resources/chatd/types.py

from pydantic import UUID4, BaseModel, Field


class LinePresenceDict(BaseModel):
    """Represents presence information for a line."""

    id: int
    state: str


class RoomUserDict(BaseModel):
    """Represents a user within a chat room."""

    uuid: UUID4
    tenant_uuid: UUID4
    accent_uuid: UUID4


class RoomDict(BaseModel):
    """Represents a chat room."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    users: list[RoomUserDict] = Field(default_factory=list)


class MessageDict(BaseModel):
    """Represents a chat message."""

    uuid: UUID4
    content: str
    alias: str
    user_uuid: UUID4
    tenant_uuid: UUID4
    accent_uuid: UUID4
    created_at: str
    room: RoomDict


class UserPresenceDict(BaseModel):
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
    lines: list[LinePresenceDict] = Field(default_factory=list)
