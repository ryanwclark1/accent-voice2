# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import ApplicationDict, LineDict


class LineApplicationAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_application_associated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.updated'

    def __init__(
        self,
        line: LineDict,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'application': application}
        super().__init__(content, tenant_uuid)


class LineApplicationDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_application_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.deleted'

    def __init__(
        self,
        line: LineDict,
        application: ApplicationDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'application': application}
        super().__init__(content, tenant_uuid)
