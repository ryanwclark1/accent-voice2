# Copyright 2023 Accent Communications

from accent_bus.resources.call_filter.event import CallFilterFallbackEditedEvent

from accent_confd import bus


class CallFilterFallbackNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, call_filter):
        event = CallFilterFallbackEditedEvent(call_filter.id, call_filter.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return CallFilterFallbackNotifier(bus)
