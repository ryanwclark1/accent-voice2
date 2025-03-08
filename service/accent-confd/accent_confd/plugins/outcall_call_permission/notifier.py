# Copyright 2023 Accent Communications

from accent_bus.resources.outcall_call_permission.event import (
    OutcallCallPermissionAssociatedEvent,
    OutcallCallPermissionDissociatedEvent,
)

from accent_confd import bus


class OutcallCallPermissionNotifier:
    def __init__(self, bus):
        self.bus = bus

    def associated(self, outcall, call_permission):
        event = OutcallCallPermissionAssociatedEvent(
            outcall.id, call_permission.id, outcall.tenant_uuid
        )
        self.bus.queue_event(event)

    def dissociated(self, outcall, call_permission):
        event = OutcallCallPermissionDissociatedEvent(
            outcall.id, call_permission.id, outcall.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return OutcallCallPermissionNotifier(bus)
