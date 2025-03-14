# accent_bus/resources/directory/event.py
# Copyright 2025 Accent Communications

"""Directory events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class FavoriteAddedEvent(UserEvent):
    """Event for when a favorite is added to the directory."""

    service = "dird"
    name = "favorite_added"
    routing_key_fmt = "directory.{user_uuid}.favorite.created"

    def __init__(
        self,
        source_name: str,
        entry_id: str,
        accent_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            source_name (str): source name.
            entry_id (str): Entry ID.
            accent_uuid (UUIDStr): Accent UUID.
            tenant_uuid (UUIDStr): tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = {
            "accent_uuid": str(accent_uuid),
            "user_uuid": str(user_uuid),
            "source": source_name,
            "source_entry_id": entry_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class FavoriteDeletedEvent(UserEvent):
    """Event for when a favorite is deleted from the directory."""

    service = "dird"
    name = "favorite_deleted"
    routing_key_fmt = "directory.{user_uuid}.favorite.deleted"

    def __init__(
        self,
        source_name: str,
        entry_id: str,
        accent_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
          source_name: Source Name
          entry_id: Entry ID
          accent_uuid: Accent UUID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {
            "accent_uuid": str(accent_uuid),
            "user_uuid": str(user_uuid),
            "source": source_name,
            "source_entry_id": entry_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
