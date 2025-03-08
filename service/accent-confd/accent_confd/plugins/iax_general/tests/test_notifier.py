# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_bus.resources.iax_general.event import IAXGeneralEditedEvent
from accent_dao.alchemy.staticiax import StaticIAX

from ..notifier import IAXGeneralNotifier

SYSCONFD_HANDLERS = {'ipbx': ['iax2 reload']}


class TestIAXGeneralNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.iax_general = Mock(StaticIAX)
        self.sysconfd = Mock()

        self.notifier = IAXGeneralNotifier(self.bus, self.sysconfd)

    def test_when_iax_general_edited_then_event_sent_on_bus(self):
        expected_event = IAXGeneralEditedEvent()

        self.notifier.edited(self.iax_general)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_iax_general_edited_then_iax_reloaded(self):
        self.notifier.edited(self.iax_general)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
