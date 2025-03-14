# accent_bus/resources/line/event.py
# Copyright 2025 Accent Communications

"""Line events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import LineDict


class LineCreatedEvent(TenantEvent):
    """Event for when a line is created."""

    service = "confd"
    name = "line_created"
    routing_key_fmt = "config.line.created"

    def __init__(self, line: LineDict, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
          line: Line
          tenant_uuid: tenant UUID

        """
        super().__init__(line, tenant_uuid)


class LineDeletedEvent(TenantEvent):
    """Event for when a line is deleted."""

    service = "confd"
    name = "line_deleted"
    routing_key_fmt = "config.line.deleted"

    def __init__(self, line: LineDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            line (LineDict): The line details.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(line, tenant_uuid)


class LineEditedEvent(TenantEvent):
    """Event for when a line is edited."""

    service = "confd"
    name = "line_edited"
    routing_key_fmt = "config.line.edited"

    def __init__(self, line: LineDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           line: Line
           tenant_uuid: tenant UUID

        """
        super().__init__(line, tenant_uuid)


class LineStatusUpdatedEvent(TenantEvent):
    """Event for when a line status is updated."""

    service = "calld"
    name = "line_status_updated"
    routing_key_fmt = "lines.{id}.status.updated"

    def __init__(
        self,
        line_id: int,
        technology: str,
        endpoint_name: str,
        endpoint_registered: bool,
        endpoint_current_call_count: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           line_id: Line ID
           technology: Technology
           endpoint_name: Endpoint Name
           endpoint_registered: Endpoint Registration Status
           endpoint_current_call_count: Endpoint Current Call Count
           tenant_uuid: tenant UUID

        """
        content = {
            "id": line_id,
            "technology": technology,
            "name": endpoint_name,
            "registered": endpoint_registered,
            "current_call_count": endpoint_current_call_count,
        }
        super().__init__(content, tenant_uuid)
