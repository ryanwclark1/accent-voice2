# Copyright 2023 Accent Communications

from accent_bus.resources.queue_extension.event import (
    QueueExtensionAssociatedEvent,
    QueueExtensionDissociatedEvent,
)

from accent_confd import bus, sysconfd


class QueueExtensionNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['dialplan reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def associated(self, queue, extension):
        self.send_sysconfd_handlers()
        event = QueueExtensionAssociatedEvent(queue.id, extension.id, queue.tenant_uuid)
        self.bus.queue_event(event)

    def dissociated(self, queue, extension):
        self.send_sysconfd_handlers()
        event = QueueExtensionDissociatedEvent(
            queue.id, extension.id, queue.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return QueueExtensionNotifier(bus, sysconfd)
