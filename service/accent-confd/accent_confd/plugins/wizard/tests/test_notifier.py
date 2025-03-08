# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_bus.resources.wizard.event import WizardCreatedEvent

from ..notifier import WizardNotifier


class TestWizardNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()

        self.notifier = WizardNotifier(self.bus)

    def test_when_wizard_created_then_event_sent_on_bus(self):
        expected_event = WizardCreatedEvent()

        self.notifier.created()

        self.bus.queue_event.assert_called_once_with(expected_event)
