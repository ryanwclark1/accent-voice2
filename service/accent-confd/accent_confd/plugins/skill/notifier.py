# Copyright 2023 Accent Communications

from accent_bus.resources.skill.event import (
    SkillCreatedEvent,
    SkillDeletedEvent,
    SkillEditedEvent,
)

from accent_confd import bus


class SkillNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, skill):
        event = SkillCreatedEvent(skill.id, skill.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, skill):
        event = SkillEditedEvent(skill.id, skill.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, skill):
        event = SkillDeletedEvent(skill.id, skill.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return SkillNotifier(bus)
