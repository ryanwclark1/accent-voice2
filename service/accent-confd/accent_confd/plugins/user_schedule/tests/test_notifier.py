# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.user_schedule.event import (
    UserScheduleAssociatedEvent,
    UserScheduleDissociatedEvent,
)

from ..notifier import UserScheduleNotifier

TENANT_UUID = str(uuid4())


class TestUserScheduleNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.schedule = Mock(id=1)
        self.user = Mock(id=2, tenant_uuid=TENANT_UUID)

        self.notifier = UserScheduleNotifier(self.bus)

    def test_associate_then_bus_event(self):
        expected_event = UserScheduleAssociatedEvent(
            self.schedule.id, self.user.tenant_uuid, self.user.uuid
        )

        self.notifier.associated(self.user, self.schedule)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_dissociate_then_bus_event(self):
        expected_event = UserScheduleDissociatedEvent(
            self.schedule.id, self.user.tenant_uuid, self.user.uuid
        )

        self.notifier.dissociated(self.user, self.schedule)

        self.bus.queue_event.assert_called_once_with(expected_event)
