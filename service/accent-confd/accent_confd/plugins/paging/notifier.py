# Copyright 2023 Accent Communications

from accent_bus.resources.paging.event import (
    PagingCreatedEvent,
    PagingDeletedEvent,
    PagingEditedEvent,
)

from accent_confd import bus


class PagingNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, paging):
        event = PagingCreatedEvent(paging.id, paging.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, paging):
        event = PagingEditedEvent(paging.id, paging.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, paging):
        event = PagingDeletedEvent(paging.id, paging.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return PagingNotifier(bus)
