# Copyright 2023 Accent Communications

from accent_bus.resources.skill_rule.event import (
    SkillRuleCreatedEvent,
    SkillRuleDeletedEvent,
    SkillRuleEditedEvent,
)

from accent_confd import bus, sysconfd


class SkillRuleNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['module reload app_queue.so']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, skill_rule):
        self.send_sysconfd_handlers()
        event = SkillRuleCreatedEvent(skill_rule.id, skill_rule.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, skill_rule):
        self.send_sysconfd_handlers()
        event = SkillRuleEditedEvent(skill_rule.id, skill_rule.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, skill_rule):
        self.send_sysconfd_handlers()
        event = SkillRuleDeletedEvent(skill_rule.id, skill_rule.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return SkillRuleNotifier(bus, sysconfd)
