# resources/line_application/event.py
from typing import ClassVar

from resources.common.event import TenantEvent

from .types import ApplicationDict, LineDict


class LineApplicationEvent(TenantEvent):
    """Base class for Line Application events."""

    service: ClassVar[str] = "confd"
    content: dict


class LineApplicationAssociatedEvent(LineApplicationEvent):
    """Event for when an application is associated with a line."""

    name: ClassVar[str] = "line_application_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.applications.{application[uuid]}.updated"
    )

    def __init__(
        self,
        line: LineDict,
        application: ApplicationDict,
        **data,
    ):
        content = {"line": line, "application": application}
        super().__init__(content=content, **data)


class LineApplicationDissociatedEvent(LineApplicationEvent):
    """Event for when an application is dissociated from a line."""

    name: ClassVar[str] = "line_application_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.applications.{application[uuid]}.deleted"
    )

    def __init__(self, line: LineDict, application: ApplicationDict, **data):
        content = {"line": line, "application": application}
        super().__init__(content=content, **data)
