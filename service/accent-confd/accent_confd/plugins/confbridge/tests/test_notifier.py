# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_bus.resources.confbridge.event import (
    ConfBridgeAccentDefaultBridgeEditedEvent,
    ConfBridgeAccentDefaultUserEditedEvent,
)

from ..notifier import ConfBridgeConfigurationNotifier

SYSCONFD_HANDLERS = {'ipbx': ['module reload app_confbridge.so']}


class TestConfBridgeConfigurationNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.confbridge = Mock()
        self.sysconfd = Mock()

        self.notifier = ConfBridgeConfigurationNotifier(self.bus, self.sysconfd)

    def test_when_confbridge_accent_default_bridge_edited_then_event_sent_on_bus(self):
        expected_event = ConfBridgeAccentDefaultBridgeEditedEvent()

        self.notifier.edited('accent_default_bridge', self.confbridge)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_confbridge_accent_default_bridge_edited_then_sip_reloaded(self):
        self.notifier.edited('accent_default_bridge', self.confbridge)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_when_confuser_accent_default_user_edited_then_event_sent_on_bus(self):
        expected_event = ConfBridgeAccentDefaultUserEditedEvent()

        self.notifier.edited('accent_default_user', self.confbridge)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_confuser_accent_default_user_edited_then_sip_reloaded(self):
        self.notifier.edited('accent_default_user', self.confbridge)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
