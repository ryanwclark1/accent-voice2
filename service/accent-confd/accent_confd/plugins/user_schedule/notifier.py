# Copyright 2023 Accent Communications

from accent_bus.resources.user_schedule.event import (
    UserScheduleAssociatedEvent,
    UserScheduleDissociatedEvent,
)

from accent_confd import bus


class UserScheduleNotifier:
    def __init__(self, bus):
        self._bus = bus

    def associated(self, user, schedule):
        event = UserScheduleAssociatedEvent(schedule.id, user.tenant_uuid, user.uuid)
        self._bus.queue_event(event)

    def dissociated(self, user, schedule):
        event = UserScheduleDissociatedEvent(schedule.id, user.tenant_uuid, user.uuid)
        self._bus.queue_event(event)


def build_notifier():
    return UserScheduleNotifier(bus)
