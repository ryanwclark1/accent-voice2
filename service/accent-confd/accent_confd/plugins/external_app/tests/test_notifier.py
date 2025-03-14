# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.external_app.event import (
    ExternalAppCreatedEvent,
    ExternalAppDeletedEvent,
    ExternalAppEditedEvent,
)

from ..notifier import ExternalAppNotifier


class TestExternalAppNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.external_app = Mock(tenant_uuid=str(uuid4()))
        self.external_app.name = 'limitation of mock instantiation with name ...'
        self.app_serialized = {'name': self.external_app.name}

        self.notifier = ExternalAppNotifier(self.bus)

    def test_when_external_app_created_then_event_sent_on_bus(self):
        expected_event = ExternalAppCreatedEvent(
            self.app_serialized, self.external_app.tenant_uuid
        )

        self.notifier.created(self.external_app)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_external_app_edited_then_event_sent_on_bus(self):
        expected_event = ExternalAppEditedEvent(
            self.app_serialized, self.external_app.tenant_uuid
        )

        self.notifier.edited(self.external_app)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_external_app_deleted_then_event_sent_on_bus(self):
        expected_event = ExternalAppDeletedEvent(
            self.app_serialized, self.external_app.tenant_uuid
        )

        self.notifier.deleted(self.external_app)

        self.bus.queue_event.assert_called_once_with(expected_event)
