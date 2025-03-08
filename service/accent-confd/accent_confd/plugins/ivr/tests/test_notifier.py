# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from uuid import uuid4

from accent_bus.resources.ivr.event import (
    IVRCreatedEvent,
    IVRDeletedEvent,
    IVREditedEvent,
)
from accent_dao.alchemy.ivr import IVR

from ..notifier import IvrNotifier

SYSCONFD_HANDLERS = {'ipbx': ['dialplan reload']}


class TestIvrNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.sysconfd = Mock()
        self.ivr = Mock(IVR, id=2, tenant_uuid=uuid4())
        self.expected_headers = {'tenant_uuid': str(self.ivr.tenant_uuid)}

        self.notifier = IvrNotifier(self.bus, self.sysconfd)

    def test_when_ivr_created_then_event_sent_on_bus(self):
        expected_event = IVRCreatedEvent(self.ivr.id, self.ivr.tenant_uuid)

        self.notifier.created(self.ivr)

        self.bus.queue_event.assert_called_once_with(expected_event)
        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_when_ivr_edited_then_event_sent_on_bus(self):
        expected_event = IVREditedEvent(self.ivr.id, self.ivr.tenant_uuid)

        self.notifier.edited(self.ivr)

        self.bus.queue_event.assert_called_once_with(expected_event)
        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_when_ivr_deleted_then_event_sent_on_bus(self):
        expected_event = IVRDeletedEvent(self.ivr.id, self.ivr.tenant_uuid)

        self.notifier.deleted(self.ivr)

        self.bus.queue_event.assert_called_once_with(expected_event)
        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
