# accent_bus/resources/sysconfd/event.py
# Copyright 2025 Accent Communications

"""Sysconfd events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import ServiceEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class RequestHandlersProgressEvent(ServiceEvent):
    """Event for request handlers progress."""

    service = "sysconfd"
    name = "request_handlers_progress"
    routing_key_fmt = "sysconfd.request_handlers.{uuid}.{status}"

    def __init__(
        self,
        request_uuid: UUIDStr,
        request_context: dict | None,
        status: str,
    ) -> None:
        """Initialize the event.

        Args:
            request_uuid (UUIDStr): The request UUID.
            request_context (dict | None): The request context.
            status (str): The status of the request.

        """
        content = {
            "uuid": str(request_uuid),
            "status": status,
            "context": request_context,
        }
        super().__init__(content)


class AsteriskReloadProgressEvent(ServiceEvent):
    """Event for Asterisk reload progress."""

    service = "sysconfd"
    name = "asterisk_reload_progress"
    routing_key_fmt = "sysconfd.asterisk.reload.{uuid}.{status}"

    def __init__(
        self,
        uuid: UUIDStr,
        status: str,
        command: str,
        request_uuids: list[UUIDStr],
    ) -> None:
        """Initialize event.

        Args:
           uuid: UUID
           status: Status
           command: Command
           request_uuids: Request UUIDs

        """
        content = {
            "uuid": str(uuid),
            "status": status,
            "command": command,
            "request_uuids": request_uuids,
        }
        super().__init__(content)
