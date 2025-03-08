# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.call_permission.event import (
    CallPermissionCreatedEvent,
    CallPermissionDeletedEvent,
    CallPermissionEditedEvent,
)
from accent_dao.alchemy.rightcall import RightCall as CallPermission

from ..notifier import CallPermissionNotifier


class TestCallPermissionNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.call_permission = Mock(CallPermission, id=1234, tenant_uuid=str(uuid4()))
        self.expected_headers = {'tenant_uuid': self.call_permission.tenant_uuid}

        self.notifier = CallPermissionNotifier(self.bus)

    def test_when_call_permission_created_then_event_sent_on_bus(self):
        expected_event = CallPermissionCreatedEvent(
            self.call_permission.id, self.call_permission.tenant_uuid
        )

        self.notifier.created(self.call_permission)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_call_permission_edited_then_event_sent_on_bus(self):
        expected_event = CallPermissionEditedEvent(
            self.call_permission.id, self.call_permission.tenant_uuid
        )

        self.notifier.edited(self.call_permission)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_call_permission_deleted_then_event_sent_on_bus(self):
        expected_event = CallPermissionDeletedEvent(
            self.call_permission.id, self.call_permission.tenant_uuid
        )

        self.notifier.deleted(self.call_permission)

        self.bus.queue_event.assert_called_once_with(expected_event)
