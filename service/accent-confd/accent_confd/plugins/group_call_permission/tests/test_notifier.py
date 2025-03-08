# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.group_call_permission.event import (
    GroupCallPermissionAssociatedEvent,
    GroupCallPermissionDissociatedEvent,
)
from accent_dao.alchemy.groupfeatures import GroupFeatures as Group
from accent_dao.alchemy.rightcall import RightCall as CallPermission

from ..notifier import GroupCallPermissionNotifier


class TestGroupCallPermissionNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.call_permission = Mock(CallPermission, id=4)
        self.group = Mock(Group, id=5, uuid=uuid4(), tenant_uuid=uuid4())
        self.expected_headers = {'tenant_uuid': str(self.group.tenant_uuid)}

        self.notifier = GroupCallPermissionNotifier(self.bus)

    def test_when_call_permission_associate_to_group_then_event_sent_on_bus(self):
        expected_event = GroupCallPermissionAssociatedEvent(
            self.group.id,
            self.group.uuid,
            self.call_permission.id,
            self.group.tenant_uuid,
        )

        self.notifier.associated(self.group, self.call_permission)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_call_permission_dissociate_to_group_then_event_sent_on_bus(self):
        expected_event = GroupCallPermissionDissociatedEvent(
            self.group.id,
            self.group.uuid,
            self.call_permission.id,
            self.group.tenant_uuid,
        )

        self.notifier.dissociated(self.group, self.call_permission)

        self.bus.queue_event.assert_called_once_with(expected_event)
