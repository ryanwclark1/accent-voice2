# Copyright 2023 Accent Communications

from accent_bus.resources.outcall.event import (
    OutcallCreatedEvent,
    OutcallDeletedEvent,
    OutcallEditedEvent,
)

from accent_confd import bus


class OutcallNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, outcall):
        event = OutcallCreatedEvent(outcall.id, outcall.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, outcall):
        event = OutcallEditedEvent(outcall.id, outcall.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, outcall):
        event = OutcallDeletedEvent(outcall.id, outcall.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return OutcallNotifier(bus)
