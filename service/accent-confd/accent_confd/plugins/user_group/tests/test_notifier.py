# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.user_group.event import UserGroupsAssociatedEvent
from accent_dao.alchemy.groupfeatures import GroupFeatures as Group
from accent_dao.alchemy.userfeatures import UserFeatures as User

from ..notifier import UserGroupNotifier

SYSCONFD_HANDLERS = {
    'ipbx': [
        'module reload res_pjsip.so',
        'module reload app_queue.so',
        'module reload chan_sccp.so',
    ]
}


class TestUserGroupNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.sysconfd = Mock()
        self.group1 = Mock(Group, id=1)
        self.group2 = Mock(Group, id=2)
        self.user = Mock(User, uuid='abcd-1234', tenant_uuid=str(uuid4()))

        self.notifier = UserGroupNotifier(self.bus, self.sysconfd)

    def test_associate_then_bus_event(self):
        expected_event = UserGroupsAssociatedEvent(
            [self.group1.id, self.group2.id], self.user.tenant_uuid, self.user.uuid
        )

        self.notifier.associated(self.user, [self.group1, self.group2])

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_associate_then_sysconfd_event(self):
        self.notifier.associated(self.user, [self.group1, self.group2])

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
