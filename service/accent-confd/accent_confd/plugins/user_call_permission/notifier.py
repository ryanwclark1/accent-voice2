# Copyright 2023 Accent Communications

from accent_bus.resources.user_call_permission.event import (
    UserCallPermissionAssociatedEvent,
    UserCallPermissionDissociatedEvent,
)

from accent_confd import bus


class UserCallPermissionNotifier:
    def __init__(self, bus):
        self.bus = bus

    def associated(self, user, call_permission):
        event = UserCallPermissionAssociatedEvent(
            call_permission.id, user.tenant_uuid, user.uuid
        )
        self.bus.queue_event(event)

    def dissociated(self, user, call_permission):
        event = UserCallPermissionDissociatedEvent(
            call_permission.id, user.tenant_uuid, user.uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return UserCallPermissionNotifier(bus)
