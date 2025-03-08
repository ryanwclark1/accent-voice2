# Copyright 2023 Accent Communications

from accent_bus.resources.incall_schedule.event import (
    IncallScheduleAssociatedEvent,
    IncallScheduleDissociatedEvent,
)

from accent_confd import bus


class IncallScheduleNotifier:
    def __init__(self, bus):
        self._bus = bus

    def associated(self, incall, schedule):
        event = IncallScheduleAssociatedEvent(
            incall.id, schedule.id, incall.tenant_uuid
        )
        self._bus.queue_event(event)

    def dissociated(self, incall, schedule):
        event = IncallScheduleDissociatedEvent(
            incall.id, schedule.id, incall.tenant_uuid
        )
        self._bus.queue_event(event)


def build_notifier():
    return IncallScheduleNotifier(bus)
