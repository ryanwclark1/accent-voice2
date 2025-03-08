# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_bus.resources.iax_callnumberlimits.event import IAXCallNumberLimitsEditedEvent
from accent_dao.alchemy.iaxcallnumberlimits import IAXCallNumberLimits

from ..notifier import IAXCallNumberLimitsNotifier

SYSCONFD_HANDLERS = {'ipbx': ['iax2 reload']}


class TestIAXCallNumberLimitsNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.iax_callnumberlimits = Mock(IAXCallNumberLimits)
        self.sysconfd = Mock()

        self.notifier = IAXCallNumberLimitsNotifier(self.bus, self.sysconfd)

    def test_when_iax_callnumberlimits_edited_then_event_sent_on_bus(self):
        expected_event = IAXCallNumberLimitsEditedEvent()

        self.notifier.edited(self.iax_callnumberlimits)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_iax_callnumberlimits_edited_then_iax_reloaded(self):
        self.notifier.edited(self.iax_callnumberlimits)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
