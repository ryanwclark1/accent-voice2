# Copyright 2025 Accent Communications

"""Data models for Chat Daemon API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from datetime import datetime


class Room(BaseModel):
    """Model representing a chat room.

    Attributes:
        uuid: Unique identifier for the room
        name: Name of the room
        description: Optional description
        created_at: When the room was created
        members: List of user UUIDs who are members
        owner_uuid: UUID of the room owner
        is_private: Whether the room is private

    """

    uuid: str
    name: str
    description: str | None = None
    created_at: datetime
    members: list[str] = Field(default_factory=list)
    owner_uuid: str
    is_private: bool = False


class Message(BaseModel):
    """Model representing a chat message.

    Attributes:
        uuid: Unique identifier for the message
        room_uuid: UUID of the room containing the message
        user_uuid: UUID of the user who sent the message
        content: Message content
        created_at: When the message was sent
        updated_at: When the message was last updated
        attachments: Optional list of attachment metadata

    """

    uuid: str
    room_uuid: str
    user_uuid: str
    content: str
    created_at: datetime
    updated_at: datetime | None = None
    attachments: list[dict[str, Any]] = Field(default_factory=list)


class UserPresence(BaseModel):
    """Model representing a user's presence status.

    Attributes:
        user_uuid: UUID of the user
        status: Current presence status
        status_message: Optional custom status message
        last_active: When the user was last active

    """

    user_uuid: str
    status: Literal["online", "away", "busy", "offline"] = "offline"
    status_message: str | None = None
    last_active: datetime | None = None


class ChatdConfig(BaseModel):
    """Model representing Chat Daemon configuration.

    Attributes:
        max_rooms_per_user: Maximum rooms a user can create
        max_message_length: Maximum length of a message
        file_attachment_limit: Maximum file size for attachments in bytes
        allowed_attachment_types: List of allowed MIME types for attachments

    """

    max_rooms_per_user: int = 100
    max_message_length: int = 5000
    file_attachment_limit: int = 10485760  # 10MB
    allowed_attachment_types: list[str] = Field(default_factory=list)
