# Copyright 2023 Accent Communications

from accent_bus.resources.user_external_app.event import (
    UserExternalAppCreatedEvent,
    UserExternalAppDeletedEvent,
    UserExternalAppEditedEvent,
)

from accent_confd import bus

from .schema import UserExternalAppSchema

ONLY_FIELDS = ['name']


class UserExternalAppNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, app, tenant_uuid):
        payload = UserExternalAppSchema(only=ONLY_FIELDS).dump(app)
        event = UserExternalAppCreatedEvent(payload, tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, app, tenant_uuid):
        payload = UserExternalAppSchema(only=ONLY_FIELDS).dump(app)
        event = UserExternalAppEditedEvent(payload, tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, app, tenant_uuid):
        payload = UserExternalAppSchema(only=ONLY_FIELDS).dump(app)
        event = UserExternalAppDeletedEvent(payload, tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return UserExternalAppNotifier(bus)
