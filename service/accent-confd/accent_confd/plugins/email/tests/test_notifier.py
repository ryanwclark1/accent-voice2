# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_bus.resources.email.event import EmailConfigUpdatedEvent

from ..notifier import EmailConfigNotifier


class TestEmailConfigNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.sysconfd = Mock()

        self.notifier = EmailConfigNotifier(self.bus, self.sysconfd)

    def test_when_email_config_edited_then_event_sent_on_bus(self):
        expected_event = EmailConfigUpdatedEvent()

        self.notifier.edited()

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_when_email_config_edited_then_commonconf_regenerated(self):
        self.notifier.edited()
        self.sysconfd.commonconf_generate.assert_called_once_with()
        self.sysconfd.commonconf_apply.assert_called_once_with()
