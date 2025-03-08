# Copyright 2023 Accent Communications

from accent_bus.resources.line_application.event import (
    LineApplicationAssociatedEvent,
    LineApplicationDissociatedEvent,
)

from accent_confd import bus, sysconfd
from accent_confd.plugins.application.schema import ApplicationSchema
from accent_confd.plugins.line.schema import LineSchema

LINE_FIELDS = [
    'id',
    'name',
    'endpoint_sip.uuid',
    'endpoint_sccp.id',
    'endpoint_custom.id',
]

APPLICATION_FIELDS = ['uuid']


class LineApplicationNotifier:
    REQUEST_HANDLERS = {'ipbx': ['module reload res_pjsip.so']}

    def __init__(self, bus, sysconfd):
        self._bus = bus
        self._sysconfd = sysconfd

    def associated(self, line, application):
        self._sysconfd.exec_request_handlers(self.REQUEST_HANDLERS)

        line_serialized = LineSchema(only=LINE_FIELDS).dump(line)
        application_serialized = ApplicationSchema(only=APPLICATION_FIELDS).dump(
            application
        )
        event = LineApplicationAssociatedEvent(
            line_serialized, application_serialized, line.tenant_uuid
        )
        self._bus.queue_event(event)

    def dissociated(self, line, application):
        self._sysconfd.exec_request_handlers(self.REQUEST_HANDLERS)

        line_serialized = LineSchema(only=LINE_FIELDS).dump(line)
        application_serialized = ApplicationSchema(only=APPLICATION_FIELDS).dump(
            application
        )
        event = LineApplicationDissociatedEvent(
            line_serialized, application_serialized, line.tenant_uuid
        )
        self._bus.queue_event(event)


def build_notifier():
    return LineApplicationNotifier(bus, sysconfd)
