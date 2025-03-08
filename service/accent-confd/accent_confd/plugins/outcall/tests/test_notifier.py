# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.outcall.event import (
    OutcallCreatedEvent,
    OutcallDeletedEvent,
    OutcallEditedEvent,
)
from accent_dao.alchemy.outcall import Outcall

from ..notifier import OutcallNotifier


class TestOutcallNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.outcall = Mock(Outcall, id=1234, tenant_uuid=uuid4())

        self.notifier = OutcallNotifier(self.bus)

    def test_when_outcall_created_then_event_sent_on_bus(self):
        expected_event = OutcallCreatedEvent(self.outcall.id, self.outcall.tenant_uuid)

        self.notifier.created(self.outcall)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_outcall_edited_then_event_sent_on_bus(self):
        expected_event = OutcallEditedEvent(self.outcall.id, self.outcall.tenant_uuid)

        self.notifier.edited(self.outcall)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_outcall_deleted_then_event_sent_on_bus(self):
        expected_event = OutcallDeletedEvent(self.outcall.id, self.outcall.tenant_uuid)

        self.notifier.deleted(self.outcall)

        self.bus.queue_event.assert_called_once_with(expected_event)
