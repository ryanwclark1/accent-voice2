# accent_bus/resources/line_extension/event.py
# Copyright 2025 Accent Communications

"""Line extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class LineExtensionAssociatedEvent(TenantEvent):
    """Event for when a line extension is associated."""

    service = "confd"
    name = "line_extension_associated"
    routing_key_fmt = "config.line_extension_associated.updated"

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           line_id: Line ID
           extension_id: Extension ID
           tenant_uuid: tenant UUID

        """
        content = {"line_id": line_id, "extension_id": extension_id}
        super().__init__(content, tenant_uuid)


class LineExtensionDissociatedEvent(TenantEvent):
    """Event for when a line extension is dissociated."""

    service = "confd"
    name = "line_extension_dissociated"
    routing_key_fmt = "config.line_extension_associated.deleted"

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            line_id (int): line ID.
            extension_id (int): extension ID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"line_id": line_id, "extension_id": extension_id}
        super().__init__(content, tenant_uuid)
