# resources/directory/event.py
from typing import ClassVar

from pydantic import UUID4

from accent_bus.resources.common.event import UserEvent


class DirectoryEvent(UserEvent):
    """Base class for Directory events."""

    service: ClassVar[str] = "dird"
    content: dict


class FavoriteAddedEvent(DirectoryEvent):
    """Event for when a favorite is added."""

    name: ClassVar[str] = "favorite_added"
    routing_key_fmt: ClassVar[str] = "directory.{user_uuid}.favorite.created"

    def __init__(self, source_name: str, entry_id: str, accent_uuid: UUID4, **data):
        content = {
            "accent_uuid": str(accent_uuid),
            "user_uuid": str(data["user_uuid"]),
            "source": source_name,
            "source_entry_id": entry_id,
        }
        super().__init__(content=content, **data)


class FavoriteDeletedEvent(DirectoryEvent):
    """Event for when a favorite is deleted."""

    name: ClassVar[str] = "favorite_deleted"
    routing_key_fmt: ClassVar[str] = "directory.{user_uuid}.favorite.deleted"

    def __init__(self, source_name: str, entry_id: str, accent_uuid: UUID4, **data):
        content = {
            "accent_uuid": str(accent_uuid),
            "user_uuid": str(data["user_uuid"]),
            "source": source_name,
            "source_entry_id": entry_id,
        }
        super().__init__(content=content, **data)
