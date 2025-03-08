# Copyright 2023 Accent Communications

from accent_bus.resources.switchboard.event import (
    SwitchboardCreatedEvent,
    SwitchboardDeletedEvent,
    SwitchboardEditedEvent,
)

from accent_confd import bus

from .schema import SwitchboardSchema


class SwitchboardNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, switchboard):
        payload = SwitchboardSchema().dump(switchboard)
        event = SwitchboardCreatedEvent(
            payload, switchboard.uuid, switchboard.tenant_uuid
        )
        self.bus.queue_event(event)

    def edited(self, switchboard):
        payload = SwitchboardSchema().dump(switchboard)
        event = SwitchboardEditedEvent(
            payload, switchboard.uuid, switchboard.tenant_uuid
        )
        self.bus.queue_event(event)

    def deleted(self, switchboard):
        payload = SwitchboardSchema().dump(switchboard)
        event = SwitchboardDeletedEvent(
            payload, switchboard.uuid, switchboard.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return SwitchboardNotifier(bus)
