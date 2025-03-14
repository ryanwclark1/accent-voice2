# resources/chatd/events.py
from typing import ClassVar

from pydantic import UUID4
from resources.common.event import TenantEvent, UserEvent

from .types import MessageDict, RoomDict, UserPresenceDict


class ChatdEvent(TenantEvent):
    """Base class for chatd events."""

    service: ClassVar[str] = "chatd"
    content: dict


class PresenceUpdatedEvent(ChatdEvent):
    """Event for when a user's presence is updated."""

    name: ClassVar[str] = "chatd_presence_updated"
    routing_key_fmt: ClassVar[str] = "chatd.users.{uuid}.presences.updated"

    def __init__(self, user_presence_data: UserPresenceDict, **data):
        super().__init__(content=user_presence_data, **data)


class ChatdUserEvent(UserEvent):
    """Base class for chatd User events.
    """

    service: ClassVar[str] = "chatd"
    content: dict


class UserRoomCreatedEvent(ChatdUserEvent):
    """Event for when a user creates a chat room."""

    name: ClassVar[str] = "chatd_user_room_created"
    routing_key_fmt: ClassVar[str] = "chatd.users.{user_uuid}.rooms.created"

    def __init__(self, room_data: RoomDict, **data):
        super().__init__(content=room_data, **data)


class UserRoomMessageCreatedEvent(ChatdUserEvent):
    """Event for when a message is created in a user's chat room."""

    name: ClassVar[str] = "chatd_user_room_message_created"
    routing_key_fmt: ClassVar[str] = (
        "chatd.users.{user_uuid}.rooms.{room_uuid}.messages.created"
    )
    room_uuid: str

    def __init__(self, message_data: MessageDict, room_uuid: UUID4, **data):
        super().__init__(content=message_data, **data)
        if room_uuid is None:
            raise ValueError("room_uuid must have a value")
        self.room_uuid = str(room_uuid)
