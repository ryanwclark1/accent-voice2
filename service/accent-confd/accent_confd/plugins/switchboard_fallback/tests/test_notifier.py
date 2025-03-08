# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.switchboard.event import SwitchboardFallbackEditedEvent
from accent_dao.alchemy.switchboard import Switchboard

from ..notifier import SwitchboardFallbackNotifier
from ..schema import SwitchboardFallbackSchema


class TestSwitchboardFallbackNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.switchboard = Mock(Switchboard, uuid=1, tenant_uuid=uuid4())

        self.notifier = SwitchboardFallbackNotifier(self.bus)

    def test_edited_then_bus_event(self):
        event_body = SwitchboardFallbackSchema().dump(self.switchboard)
        expected_event = SwitchboardFallbackEditedEvent(
            event_body, self.switchboard.uuid, self.switchboard.tenant_uuid
        )

        self.notifier.edited(self.switchboard)

        self.bus.queue_event.assert_called_once_with(expected_event)
