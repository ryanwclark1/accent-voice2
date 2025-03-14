# accent_bus/resources/line_application/event.py
# Copyright 2025 Accent Communications

"""Line application events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import ApplicationDict, LineDict


class LineApplicationAssociatedEvent(TenantEvent):
    """Event for when a line application is associated."""

    service = "confd"
    name = "line_application_associated"
    routing_key_fmt = "config.lines.{line[id]}.applications.{application[uuid]}.updated"

    def __init__(
        self,
        line: LineDict,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            line (LineDict): line details.
            application (ApplicationDict): application details.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {"line": line, "application": application}
        super().__init__(content, tenant_uuid)


class LineApplicationDissociatedEvent(TenantEvent):
    """Event for when a line application is dissociated."""

    service = "confd"
    name = "line_application_dissociated"
    routing_key_fmt = "config.lines.{line[id]}.applications.{application[uuid]}.deleted"

    def __init__(
        self,
        line: LineDict,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
           line: Line
           application: Application
           tenant_uuid: tenant UUID

        """
        content = {"line": line, "application": application}
        super().__init__(content, tenant_uuid)
