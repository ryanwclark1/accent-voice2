# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.group.event import GroupFallbackEditedEvent
from accent_dao.alchemy.groupfeatures import GroupFeatures as Group

from ..notifier import GroupFallbackNotifier


class TestGroupFallbackNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.group = Mock(Group, id=1, uuid=uuid4(), tenant_uuid=uuid4())

        self.notifier = GroupFallbackNotifier(self.bus)

    def test_edited_then_bus_event(self):
        expected_event = GroupFallbackEditedEvent(
            self.group.id, self.group.uuid, self.group.tenant_uuid
        )

        self.notifier.edited(self.group)

        self.bus.queue_event.assert_called_once_with(expected_event)
