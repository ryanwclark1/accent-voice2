# resources/trunk/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class TrunkEvent(TenantEvent):
    """Base class for Trunk events."""

    service: ClassVar[str] = "confd"
    content: dict


class TrunkCreatedEvent(TrunkEvent):
    """Event for when a trunk is created."""

    name: ClassVar[str] = "trunk_created"
    routing_key_fmt: ClassVar[str] = "config.trunk.created"

    def __init__(self, trunk_id: int, **data):
        content = {"id": int(trunk_id)}
        super().__init__(content=content, **data)


class TrunkDeletedEvent(TrunkEvent):
    """Event for when a trunk is deleted."""

    name: ClassVar[str] = "trunk_deleted"
    routing_key_fmt: ClassVar[str] = "config.trunk.deleted"

    def __init__(self, trunk_id: int, **data):
        content = {"id": int(trunk_id)}
        super().__init__(content=content, **data)


class TrunkEditedEvent(TrunkEvent):
    """Event for when a trunk is edited."""

    name: ClassVar[str] = "trunk_edited"
    routing_key_fmt: ClassVar[str] = "config.trunk.edited"

    def __init__(self, trunk_id: int, **data):
        content = {"id": int(trunk_id)}
        super().__init__(content=content, **data)


class TrunkStatusUpdatedEvent(TrunkEvent):
    """Event for when a trunk status is updated."""

    service: ClassVar[str] = "calld"  # Different service
    name: ClassVar[str] = "trunk_status_updated"
    routing_key_fmt: ClassVar[str] = "trunks.{id}.status.updated"

    def __init__(
        self,
        trunk_id: int,
        technology: str,
        endpoint_name: str,
        endpoint_registered: bool,
        endpoint_current_call_count: int,
        **data,
    ):
        content = {
            "id": trunk_id,
            "technology": technology,
            "name": endpoint_name,
            "registered": endpoint_registered,
            "current_call_count": endpoint_current_call_count,
        }
        super().__init__(content=content, **data)
