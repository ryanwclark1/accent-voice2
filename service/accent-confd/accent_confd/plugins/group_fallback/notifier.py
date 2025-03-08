# Copyright 2023 Accent Communications

from accent_bus.resources.group.event import GroupFallbackEditedEvent

from accent_confd import bus


class GroupFallbackNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, group):
        event = GroupFallbackEditedEvent(group.id, group.uuid, group.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return GroupFallbackNotifier(bus)
