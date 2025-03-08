# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.group_schedule.event import (
    GroupScheduleAssociatedEvent,
    GroupScheduleDissociatedEvent,
)

from ..notifier import GroupScheduleNotifier


class TestGroupScheduleNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.schedule = Mock(id=1)
        self.group = Mock(id=2, uuid=uuid4(), tenant_uuid=uuid4())

        self.notifier = GroupScheduleNotifier(self.bus)

    def test_associate_then_bus_event(self):
        expected_event = GroupScheduleAssociatedEvent(
            self.group.id,
            self.group.uuid,
            self.schedule.id,
            self.group.tenant_uuid,
        )

        self.notifier.associated(self.group, self.schedule)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_dissociate_then_bus_event(self):
        expected_event = GroupScheduleDissociatedEvent(
            self.group.id,
            self.group.uuid,
            self.schedule.id,
            self.group.tenant_uuid,
        )

        self.notifier.dissociated(self.group, self.schedule)

        self.bus.queue_event.assert_called_once_with(expected_event)
