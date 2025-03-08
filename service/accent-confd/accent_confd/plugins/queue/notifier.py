# Copyright 2023 Accent Communications

from accent_bus.resources.queue.event import (
    QueueCreatedEvent,
    QueueDeletedEvent,
    QueueEditedEvent,
)

from accent_confd import bus, sysconfd


class QueueNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['module reload app_queue.so']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, queue):
        self.send_sysconfd_handlers()
        event = QueueCreatedEvent(queue.id, queue.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, queue):
        self.send_sysconfd_handlers()
        event = QueueEditedEvent(queue.id, queue.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, queue):
        self.send_sysconfd_handlers()
        event = QueueDeletedEvent(queue.id, queue.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return QueueNotifier(bus, sysconfd)
