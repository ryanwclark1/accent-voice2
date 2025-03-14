# resources/sysconfd/event.py
from typing import ClassVar

from pydantic import UUID4

from resources.common.event import ServiceEvent


class SysconfdEvent(ServiceEvent):
    """Base class for sysconfd events."""

    service: ClassVar[str] = "sysconfd"
    content: dict = {}


class RequestHandlersProgressEvent(SysconfdEvent):
    """Event for request handlers progress."""

    name: ClassVar[str] = "request_handlers_progress"
    routing_key_fmt: ClassVar[str] = "sysconfd.request_handlers.{uuid}.{status}"

    def __init__(
        self, request_uuid: UUID4, request_context: dict | None, status: str, **data
    ):
        content = {
            "uuid": str(request_uuid),
            "status": status,
            "context": request_context,
        }
        super().__init__(content=content, **data)


class AsteriskReloadProgressEvent(SysconfdEvent):
    """Event for Asterisk reload progress."""

    name: ClassVar[str] = "asterisk_reload_progress"
    routing_key_fmt: ClassVar[str] = "sysconfd.asterisk.reload.{uuid}.{status}"

    def __init__(
        self, uuid: UUID4, status: str, command: str, request_uuids: list[UUID4], **data
    ):
        content = {
            "uuid": str(uuid),
            "status": status,
            "command": command,
            "request_uuids": request_uuids,
        }
        super().__init__(content=content, **data)
