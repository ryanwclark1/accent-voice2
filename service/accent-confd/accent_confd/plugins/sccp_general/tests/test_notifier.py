# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_bus.resources.sccp_general.event import SCCPGeneralEditedEvent
from accent_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings

from ..notifier import SCCPGeneralNotifier

SYSCONFD_HANDLERS = {'ipbx': ['module reload chan_sccp.so']}


class TestSCCPGeneralNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.sccp_general = Mock(SCCPGeneralSettings)
        self.sysconfd = Mock()

        self.notifier = SCCPGeneralNotifier(self.bus, self.sysconfd)

    def test_when_sccp_general_edited_then_event_sent_on_bus(self):
        expected_event = SCCPGeneralEditedEvent()

        self.notifier.edited(self.sccp_general)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_sccp_general_edited_then_sccp_reloaded(self):
        self.notifier.edited(self.sccp_general)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
