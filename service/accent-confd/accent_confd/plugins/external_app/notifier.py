# Copyright 2023 Accent Communications

from accent_bus.resources.external_app.event import (
    ExternalAppCreatedEvent,
    ExternalAppDeletedEvent,
    ExternalAppEditedEvent,
)

from accent_confd import bus

from .schema import ExternalAppSchema

ONLY_FIELDS = ['name']


class ExternalAppNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, app):
        app_serialized = ExternalAppSchema(only=ONLY_FIELDS).dump(app)
        event = ExternalAppCreatedEvent(app_serialized, app.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, app):
        app_serialized = ExternalAppSchema(only=ONLY_FIELDS).dump(app)
        event = ExternalAppEditedEvent(app_serialized, app.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, app):
        app_serialized = ExternalAppSchema(only=ONLY_FIELDS).dump(app)
        event = ExternalAppDeletedEvent(app_serialized, app.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return ExternalAppNotifier(bus)
