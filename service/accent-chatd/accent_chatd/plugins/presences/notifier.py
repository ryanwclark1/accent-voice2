# Copyright 2023 Accent Communications

from accent_bus.resources.chatd.events import PresenceUpdatedEvent

from .schemas import UserPresenceSchema


class PresenceNotifier:
    def __init__(self, bus):
        self._bus = bus

    def updated(self, user):
        payload = UserPresenceSchema().dump(user)
        event = PresenceUpdatedEvent(payload, user.tenant_uuid)
        self._bus.publish(event)
