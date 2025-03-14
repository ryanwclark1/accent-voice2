# resources/group_extension/event.py
from typing import ClassVar

from pydantic import UUID4
from resources.common.event import TenantEvent


class GroupExtensionEvent(TenantEvent):
    """Base class for Group Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class GroupExtensionAssociatedEvent(GroupExtensionEvent):
    """Event for when an extension is associated with a group."""

    name: ClassVar[str] = "group_extension_associated"
    routing_key_fmt: ClassVar[str] = "config.groups.extensions.updated"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        extension_id: int,
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)


class GroupExtensionDissociatedEvent(GroupExtensionEvent):
    """Event for when an extension is dissociated from a group."""

    name: ClassVar[str] = "group_extension_dissociated"
    routing_key_fmt: ClassVar[str] = "config.groups.extensions.deleted"

    def __init__(
        self,
        group_id: int,
        group_uuid: UUID4,
        extension_id: int,
        **data,
    ):
        content = {
            "group_id": group_id,
            "group_uuid": str(group_uuid),
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)
