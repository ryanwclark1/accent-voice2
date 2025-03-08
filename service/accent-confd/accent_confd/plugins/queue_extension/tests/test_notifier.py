# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.queue_extension.event import (
    QueueExtensionAssociatedEvent,
    QueueExtensionDissociatedEvent,
)
from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.queuefeatures import QueueFeatures as Queue

from ..notifier import QueueExtensionNotifier

SYSCONFD_HANDLERS = {'ipbx': ['dialplan reload']}


class TestQueueExtensionNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.sysconfd = Mock()
        self.extension = Mock(Extension, id=1)
        self.queue = Mock(Queue, id=2, tenant_uuid=uuid4())

        self.notifier = QueueExtensionNotifier(self.bus, self.sysconfd)

    def test_associate_then_bus_event(self):
        expected_event = QueueExtensionAssociatedEvent(
            self.queue.id, self.extension.id, self.queue.tenant_uuid
        )

        self.notifier.associated(self.queue, self.extension)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_associate_then_sysconfd_event(self):
        self.notifier.associated(self.queue, self.extension)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_dissociate_then_bus_event(self):
        expected_event = QueueExtensionDissociatedEvent(
            self.queue.id, self.extension.id, self.queue.tenant_uuid
        )

        self.notifier.dissociated(self.queue, self.extension)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_dissociate_then_sysconfd_event(self):
        self.notifier.dissociated(self.queue, self.extension)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
