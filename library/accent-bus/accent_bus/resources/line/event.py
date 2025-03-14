# resources/line/event.py
from typing import ClassVar

from resources.common.event import TenantEvent

from .types import LineDict


class LineEvent(TenantEvent):
    """Base class for Line events."""

    service: ClassVar[str] = "confd"
    content: dict


class LineCreatedEvent(LineEvent):
    """Event for when a line is created."""

    name: ClassVar[str] = "line_created"
    routing_key_fmt: ClassVar[str] = "config.line.created"

    def __init__(self, line: LineDict, **data):
        super().__init__(content=line, **data)


class LineDeletedEvent(LineEvent):
    """Event for when a line is deleted."""

    name: ClassVar[str] = "line_deleted"
    routing_key_fmt: ClassVar[str] = "config.line.deleted"

    def __init__(self, line: LineDict, **data):
        super().__init__(content=line, **data)


class LineEditedEvent(LineEvent):
    """Event for when a line is edited."""

    name: ClassVar[str] = "line_edited"
    routing_key_fmt: ClassVar[str] = "config.line.edited"

    def __init__(self, line: LineDict, **data):
        super().__init__(content=line, **data)


class LineStatusUpdatedEvent(LineEvent):
    """Event for when a line status is updated."""

    service: ClassVar[str] = "calld"  # Different service
    name: ClassVar[str] = "line_status_updated"
    routing_key_fmt: ClassVar[str] = "lines.{id}.status.updated"

    def __init__(
        self,
        line_id: int,
        technology: str,
        endpoint_name: str,
        endpoint_registered: bool,
        endpoint_current_call_count: int,
        **data,
    ):
        content = {
            "id": line_id,
            "technology": technology,
            "name": endpoint_name,
            "registered": endpoint_registered,
            "current_call_count": endpoint_current_call_count,
        }
        super().__init__(content=content, **data)
