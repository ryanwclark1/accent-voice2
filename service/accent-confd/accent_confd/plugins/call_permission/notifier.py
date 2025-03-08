# Copyright 2023 Accent Communications

from accent_bus.resources.call_permission.event import (
    CallPermissionCreatedEvent,
    CallPermissionDeletedEvent,
    CallPermissionEditedEvent,
)

from accent_confd import bus


class CallPermissionNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, call_permission):
        event = CallPermissionCreatedEvent(
            call_permission.id, call_permission.tenant_uuid
        )
        self.bus.queue_event(event)

    def edited(self, call_permission):
        event = CallPermissionEditedEvent(
            call_permission.id, call_permission.tenant_uuid
        )
        self.bus.queue_event(event)

    def deleted(self, call_permission):
        event = CallPermissionDeletedEvent(
            call_permission.id, call_permission.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return CallPermissionNotifier(bus)
