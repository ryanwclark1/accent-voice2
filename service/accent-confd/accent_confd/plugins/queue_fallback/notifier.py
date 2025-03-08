# Copyright 2023 Accent Communications

from accent_bus.resources.queue.event import QueueFallbackEditedEvent

from accent_confd import bus


class QueueFallbackNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, queue):
        event = QueueFallbackEditedEvent(queue.id, queue.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return QueueFallbackNotifier(bus)
