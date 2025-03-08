# Copyright 2023 Accent Communications

from accent_bus.resources.ingress_http.event import (
    IngressHTTPCreatedEvent,
    IngressHTTPDeletedEvent,
    IngressHTTPEditedEvent,
)

from accent_confd import bus

from .schema import IngressHTTPSchema


class IngressHTTPNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, ingress_http):
        serialized = IngressHTTPSchema().dump(ingress_http)
        event = IngressHTTPCreatedEvent(serialized, ingress_http.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, ingress_http):
        serialized = IngressHTTPSchema().dump(ingress_http)
        event = IngressHTTPEditedEvent(serialized, ingress_http.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, ingress_http):
        serialized = IngressHTTPSchema().dump(ingress_http)
        event = IngressHTTPDeletedEvent(serialized, ingress_http.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return IngressHTTPNotifier(bus)
