# Copyright 2023 Accent Communications

from accent_bus.resources.incall_extension.event import (
    IncallExtensionAssociatedEvent,
    IncallExtensionDissociatedEvent,
)

from accent_confd import bus, sysconfd


class IncallExtensionNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['dialplan reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def associated(self, incall, extension):
        self.send_sysconfd_handlers()
        event = IncallExtensionAssociatedEvent(
            incall.id, extension.id, incall.tenant_uuid
        )
        self.bus.queue_event(event)

    def dissociated(self, incall, extension):
        self.send_sysconfd_handlers()
        event = IncallExtensionDissociatedEvent(
            incall.id, extension.id, incall.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return IncallExtensionNotifier(bus, sysconfd)
