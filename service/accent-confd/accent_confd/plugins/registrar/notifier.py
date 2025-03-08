# Copyright 2023 Accent Communications

from accent_bus.resources.registrar.event import (
    RegistrarCreatedEvent,
    RegistrarDeletedEvent,
    RegistrarEditedEvent,
)

from .schema import RegistrarSchema


class RegistrarNotifier:
    schema = RegistrarSchema(exclude=['links'])

    def __init__(self, bus):
        self.bus = bus

    def created(self, registrar):
        payload = self.schema.dump(registrar)
        event = RegistrarCreatedEvent(payload)
        self.bus.queue_event(event)

    def edited(self, registrar):
        payload = self.schema.dump(registrar)
        event = RegistrarEditedEvent(payload)
        self.bus.queue_event(event)

    def deleted(self, registrar):
        payload = self.schema.dump(registrar)
        event = RegistrarDeletedEvent(payload)
        self.bus.queue_event(event)
