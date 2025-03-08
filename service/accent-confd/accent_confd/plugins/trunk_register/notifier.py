# Copyright 2023 Accent Communications

from accent_bus.resources.trunk_register.event import (
    TrunkRegisterIAXAssociatedEvent,
    TrunkRegisterIAXDissociatedEvent,
)

from accent_confd import bus


class TrunkRegisterIAXNotifier:
    def __init__(self, bus):
        self.bus = bus

    def associated(self, trunk, register):
        event = TrunkRegisterIAXAssociatedEvent(
            trunk.id, register.id, trunk.tenant_uuid
        )
        self.bus.queue_event(event)

    def dissociated(self, trunk, register):
        event = TrunkRegisterIAXDissociatedEvent(
            trunk.id, register.id, trunk.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier_iax():
    return TrunkRegisterIAXNotifier(bus)
