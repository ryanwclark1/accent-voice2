# Copyright 2023 Accent Communications

from __future__ import annotations

from ..common.event import ServiceEvent
from ..common.types import UUIDStr


class RequestHandlersProgressEvent(ServiceEvent):
    service = 'sysconfd'
    name = 'request_handlers_progress'
    routing_key_fmt = 'sysconfd.request_handlers.{uuid}.{status}'

    def __init__(
        self,
        request_uuid: UUIDStr,
        request_context: dict | None,
        status: str,
    ):
        content = {
            'uuid': str(request_uuid),
            'status': status,
            'context': request_context,
        }
        super().__init__(content)


class AsteriskReloadProgressEvent(ServiceEvent):
    service = 'sysconfd'
    name = 'asterisk_reload_progress'
    routing_key_fmt = 'sysconfd.asterisk.reload.{uuid}.{status}'

    def __init__(
        self,
        uuid: UUIDStr,
        status: str,
        command: str,
        request_uuids: list[UUIDStr],
    ):
        content = {
            'uuid': str(uuid),
            'status': status,
            'command': command,
            'request_uuids': request_uuids,
        }
        super().__init__(content)
