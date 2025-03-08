# Copyright 2023 Accent Communications

from accent_bus.resources.queue_schedule.event import (
    QueueScheduleAssociatedEvent,
    QueueScheduleDissociatedEvent,
)

from accent_confd import bus


class QueueScheduleNotifier:
    def __init__(self, bus):
        self.bus = bus

    def associated(self, queue, schedule):
        event = QueueScheduleAssociatedEvent(queue.id, schedule.id, queue.tenant_uuid)
        self.bus.queue_event(event)

    def dissociated(self, queue, schedule):
        event = QueueScheduleDissociatedEvent(queue.id, schedule.id, queue.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return QueueScheduleNotifier(bus)
