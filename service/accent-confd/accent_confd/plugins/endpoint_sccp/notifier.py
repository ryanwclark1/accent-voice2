# Copyright 2023 Accent Communications

from accent_bus.resources.endpoint_sccp.event import (
    SCCPEndpointCreatedEvent,
    SCCPEndpointDeletedEvent,
    SCCPEndpointEditedEvent,
)

from accent_confd import bus, sysconfd

from .schema import SccpSchema

ENDPOINT_SCCP_FIELDS = [
    'id',
    'tenant_uuid',
    'line.id',
]


class SccpEndpointNotifier:
    def __init__(self, sysconfd, bus):
        self.sysconfd = sysconfd
        self.bus = bus

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['module reload chan_sccp.so', 'dialplan reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, sccp):
        sccp_serialized = SccpSchema(only=ENDPOINT_SCCP_FIELDS).dump(sccp)
        event = SCCPEndpointCreatedEvent(sccp_serialized, sccp.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, sccp):
        sccp_serialized = SccpSchema(only=ENDPOINT_SCCP_FIELDS).dump(sccp)
        self.send_sysconfd_handlers()
        event = SCCPEndpointEditedEvent(sccp_serialized, sccp.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, sccp):
        sccp_serialized = SccpSchema(only=ENDPOINT_SCCP_FIELDS).dump(sccp)
        self.send_sysconfd_handlers()
        event = SCCPEndpointDeletedEvent(sccp_serialized, sccp.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return SccpEndpointNotifier(sysconfd, bus)
