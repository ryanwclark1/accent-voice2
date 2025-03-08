# Copyright 2023 Accent Communications

from accent_bus.resources.paging_user.event import (
    PagingCallerUsersAssociatedEvent,
    PagingMemberUsersAssociatedEvent,
)

from accent_confd import bus


class PagingUserNotifier:
    def __init__(self, bus):
        self.bus = bus

    def callers_associated(self, paging, users):
        user_uuids = [user.uuid for user in users]
        event = PagingCallerUsersAssociatedEvent(
            paging.id, user_uuids, paging.tenant_uuid
        )
        self.bus.queue_event(event)

    def members_associated(self, paging, users):
        user_uuids = [user.uuid for user in users]
        event = PagingMemberUsersAssociatedEvent(
            paging.id, user_uuids, paging.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return PagingUserNotifier(bus)
