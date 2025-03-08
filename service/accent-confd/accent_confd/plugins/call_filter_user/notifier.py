# Copyright 2023 Accent Communications

from accent_bus.resources.call_filter_user.event import (
    CallFilterRecipientUsersAssociatedEvent,
    CallFilterSurrogateUsersAssociatedEvent,
)

from accent_confd import bus


class CallFilterUserNotifier:
    def __init__(self, bus):
        self.bus = bus

    def recipient_users_associated(self, call_filter, users):
        user_uuids = [user.uuid for user in users]
        event = CallFilterRecipientUsersAssociatedEvent(
            call_filter.id, user_uuids, call_filter.tenant_uuid
        )
        self.bus.queue_event(event)

    def surrogate_users_associated(self, call_filter, users):
        user_uuids = [user.uuid for user in users]
        event = CallFilterSurrogateUsersAssociatedEvent(
            call_filter.id, user_uuids, call_filter.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return CallFilterUserNotifier(bus)
