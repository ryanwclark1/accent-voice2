# Copyright 2023 Accent Communications

from accent_bus.resources.ivr.event import (
    IVRCreatedEvent,
    IVRDeletedEvent,
    IVREditedEvent,
)

from accent_confd import bus, sysconfd


class IvrNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['dialplan reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, ivr):
        self.send_sysconfd_handlers()
        event = IVRCreatedEvent(ivr.id, ivr.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, ivr):
        self.send_sysconfd_handlers()
        event = IVREditedEvent(ivr.id, ivr.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, ivr):
        self.send_sysconfd_handlers()
        event = IVRDeletedEvent(ivr.id, ivr.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return IvrNotifier(bus, sysconfd)
