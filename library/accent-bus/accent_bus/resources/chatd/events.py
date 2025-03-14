# accent_bus/resources/chatd/events.py
# Copyright 2025 Accent Communications

"""Chatd events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import TenantEvent, UserEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr

    from .types import MessageDict, RoomDict, UserPresenceDict


class PresenceUpdatedEvent(TenantEvent):
    """Event for when presence is updated."""

    service = "chatd"
    name = "chatd_presence_updated"
    routing_key_fmt = "chatd.users.{uuid}.presences.updated"

    def __init__(
        self,
        user_presence_data: UserPresenceDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           user_presence_data: User Presence data
           tenant_uuid: tenant UUID

        """
        super().__init__(user_presence_data, tenant_uuid)


class UserRoomCreatedEvent(UserEvent):
    """Event for when a user room is created."""

    service = "chatd"
    name = "chatd_user_room_created"
    routing_key_fmt = "chatd.users.{user_uuid}.rooms.created"

    def __init__(
        self,
        room_data: RoomDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           room_data: Room Data
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        super().__init__(room_data, tenant_uuid, user_uuid)


class UserRoomMessageCreatedEvent(UserEvent):
    """Event for when a user room message is created."""

    service = "chatd"
    name = "chatd_user_room_message_created"
    routing_key_fmt = "chatd.users.{user_uuid}.rooms.{room_uuid}.messages.created"

    def __init__(
        self,
        message_data: MessageDict,
        room_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          message_data: Message Data
          room_uuid: Room UUID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(message_data, tenant_uuid, user_uuid)
        if room_uuid is None:
            msg = "room_uuid must have a value"
            raise ValueError(msg)
        self.room_uuid = str(room_uuid)
