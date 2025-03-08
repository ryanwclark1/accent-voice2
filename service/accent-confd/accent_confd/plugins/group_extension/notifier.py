# Copyright 2023 Accent Communications

from accent_bus.resources.group_extension.event import (
    GroupExtensionAssociatedEvent,
    GroupExtensionDissociatedEvent,
)

from accent_confd import bus, sysconfd


class GroupExtensionNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['dialplan reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def associated(self, group, extension):
        self.send_sysconfd_handlers()
        event = GroupExtensionAssociatedEvent(
            group.id, group.uuid, extension.id, group.tenant_uuid
        )
        self.bus.queue_event(event)

    def dissociated(self, group, extension):
        self.send_sysconfd_handlers()
        event = GroupExtensionDissociatedEvent(
            group.id, group.uuid, extension.id, group.tenant_uuid
        )
        self.bus.queue_event(event)


def build_notifier():
    return GroupExtensionNotifier(bus, sysconfd)
