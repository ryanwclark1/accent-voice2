# Copyright 2023 Accent Communications

from accent_bus.resources.schedule.event import (
    ScheduleCreatedEvent,
    ScheduleDeletedEvent,
    ScheduleEditedEvent,
)

from accent_confd import bus


class ScheduleNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, schedule):
        event = ScheduleCreatedEvent(schedule.id, schedule.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, schedule):
        event = ScheduleEditedEvent(schedule.id, schedule.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, schedule):
        event = ScheduleDeletedEvent(schedule.id, schedule.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return ScheduleNotifier(bus)
