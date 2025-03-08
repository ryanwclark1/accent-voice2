# Copyright 2023 Accent Communications

from accent_bus.resources.user_agent.event import (
    UserAgentAssociatedEvent,
    UserAgentDissociatedEvent,
)

from accent_confd import bus


class UserAgentNotifier:
    def __init__(self, bus):
        self.bus = bus

    def associated(self, user, agent):
        event = UserAgentAssociatedEvent(agent.id, user.tenant_uuid, user.uuid)
        self.bus.queue_event(event)

    def dissociated(self, user, agent):
        event = UserAgentDissociatedEvent(agent.id, user.tenant_uuid, user.uuid)
        self.bus.queue_event(event)


def build_notifier():
    return UserAgentNotifier(bus)
