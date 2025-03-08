# Copyright 2023 Accent Communications

from accent_bus.resources.call_filter.event import (
    CallFilterCreatedEvent,
    CallFilterDeletedEvent,
    CallFilterEditedEvent,
)

from accent_confd import bus


class CallFilterNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, call_filter):
        event = CallFilterCreatedEvent(call_filter.id, call_filter.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, call_filter):
        event = CallFilterEditedEvent(call_filter.id, call_filter.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, call_filter):
        event = CallFilterDeletedEvent(call_filter.id, call_filter.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return CallFilterNotifier(bus)
