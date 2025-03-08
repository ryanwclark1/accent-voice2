# Copyright 2023 Accent Communications

from accent_bus.resources.group.event import (
    GroupCreatedEvent,
    GroupDeletedEvent,
    GroupEditedEvent,
)

from accent_confd import bus, sysconfd

from .schema import GroupSchema

GROUP_FIELDS = ['id', 'uuid']


class GroupNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['module reload app_queue.so']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, group):
        self.send_sysconfd_handlers()
        group_payload = GroupSchema(only=GROUP_FIELDS).dump(group)
        event = GroupCreatedEvent(group_payload, group.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, group):
        self.send_sysconfd_handlers()
        group_payload = GroupSchema(only=GROUP_FIELDS).dump(group)
        event = GroupEditedEvent(group_payload, group.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, group):
        self.send_sysconfd_handlers()
        group_payload = GroupSchema(only=GROUP_FIELDS).dump(group)
        event = GroupDeletedEvent(group_payload, group.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return GroupNotifier(bus, sysconfd)
