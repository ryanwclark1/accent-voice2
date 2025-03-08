# Copyright 2023 Accent Communications

from accent_bus.resources.switchboard.event import SwitchboardFallbackEditedEvent

from accent_confd import bus

from .schema import SwitchboardFallbackSchema


class SwitchboardFallbackNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, switchboard):
        payload = SwitchboardFallbackSchema().dump(switchboard)
        event = SwitchboardFallbackEditedEvent(
            payload, switchboard.uuid, switchboard.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return SwitchboardFallbackNotifier(bus)
