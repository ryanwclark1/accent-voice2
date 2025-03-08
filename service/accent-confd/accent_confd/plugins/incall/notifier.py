# Copyright 2023 Accent Communications

from accent_bus.resources.incall.event import (
    IncallCreatedEvent,
    IncallDeletedEvent,
    IncallEditedEvent,
)

from accent_confd import bus


class IncallNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, incall):
        event = IncallCreatedEvent(incall.id, incall.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, incall):
        event = IncallEditedEvent(incall.id, incall.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, incall):
        event = IncallDeletedEvent(incall.id, incall.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return IncallNotifier(bus)
