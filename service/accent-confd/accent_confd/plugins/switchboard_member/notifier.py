# Copyright 2023 Accent Communications

from accent_bus.resources.switchboard.event import SwitchboardMemberUserAssociatedEvent

from accent_confd import bus


class SwitchboardMemberUserNotifier:
    def __init__(self, bus):
        self.bus = bus

    def members_associated(self, switchboard, users):
        user_uuids = [user.uuid for user in users]
        event = SwitchboardMemberUserAssociatedEvent(
            switchboard.uuid, switchboard.tenant_uuid, user_uuids
        )
        self.bus.queue_event(event)


def build_notifier():
    return SwitchboardMemberUserNotifier(bus)
