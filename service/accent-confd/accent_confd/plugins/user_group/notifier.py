# Copyright 2023 Accent Communications

from accent_bus.resources.user_group.event import UserGroupsAssociatedEvent

from accent_confd import bus, sysconfd


class UserGroupNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {
            'ipbx': [
                'module reload res_pjsip.so',
                'module reload app_queue.so',
                'module reload chan_sccp.so',
            ]
        }
        self.sysconfd.exec_request_handlers(handlers)

    def associated(self, user, groups):
        self.send_sysconfd_handlers()
        group_ids = [group.id for group in groups]
        event = UserGroupsAssociatedEvent(group_ids, user.tenant_uuid, user.uuid)
        self.bus.queue_event(event)


def build_notifier():
    return UserGroupNotifier(bus, sysconfd)
