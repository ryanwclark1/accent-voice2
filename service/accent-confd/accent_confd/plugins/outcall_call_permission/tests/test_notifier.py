# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.outcall_call_permission.event import (
    OutcallCallPermissionAssociatedEvent,
    OutcallCallPermissionDissociatedEvent,
)
from accent_dao.alchemy.outcall import Outcall
from accent_dao.alchemy.rightcall import RightCall as CallPermission

from ..notifier import OutcallCallPermissionNotifier


class TestOutcallCallPermissionNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.call_permission = Mock(CallPermission, id=4)
        self.outcall = Mock(Outcall, id=5, tenant_uuid=uuid4())

        self.notifier = OutcallCallPermissionNotifier(self.bus)

    def test_when_call_permission_associate_to_outcall_then_event_sent_on_bus(self):
        expected_event = OutcallCallPermissionAssociatedEvent(
            self.outcall.id, self.call_permission.id, self.outcall.tenant_uuid
        )

        self.notifier.associated(self.outcall, self.call_permission)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_call_permission_dissociate_to_outcall_then_event_sent_on_bus(self):
        expected_event = OutcallCallPermissionDissociatedEvent(
            self.outcall.id, self.call_permission.id, self.outcall.tenant_uuid
        )

        self.notifier.dissociated(self.outcall, self.call_permission)

        self.bus.queue_event.assert_called_once_with(expected_event)
