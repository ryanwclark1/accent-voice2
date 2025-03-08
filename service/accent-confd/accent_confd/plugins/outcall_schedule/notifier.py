# Copyright 2023 Accent Communications

from accent_bus.resources.outcall_schedule.event import (
    OutcallScheduleAssociatedEvent,
    OutcallScheduleDissociatedEvent,
)

from accent_confd import bus


class OutcallScheduleNotifier:
    def __init__(self, bus):
        self._bus = bus

    def associated(self, outcall, schedule):
        event = OutcallScheduleAssociatedEvent(
            outcall.id, schedule.id, outcall.tenant_uuid
        )
        self._bus.queue_event(event)

    def dissociated(self, outcall, schedule):
        event = OutcallScheduleDissociatedEvent(
            outcall.id, schedule.id, outcall.tenant_uuid
        )
        self._bus.queue_event(event)


def build_notifier():
    return OutcallScheduleNotifier(bus)
