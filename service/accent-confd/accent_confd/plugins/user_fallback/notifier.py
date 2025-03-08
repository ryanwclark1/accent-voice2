# Copyright 2023 Accent Communications

from accent_bus.resources.user.event import UserFallbackEditedEvent

from accent_confd import bus


class UserFallbackNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, user):
        event = UserFallbackEditedEvent(user.id, user.tenant_uuid, user.uuid)
        self.bus.queue_event(event)


def build_notifier():
    return UserFallbackNotifier(bus)
