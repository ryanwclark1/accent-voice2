# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch
from unittest.mock import sentinel as s

from accent_bus.resources.plugins.events import (
    PluginInstallProgressEvent,
    PluginUninstallProgressEvent,
)

from accent_plugind.bus import Publisher


@patch.object(Publisher, 'publish')
class TestPublisher(TestCase):
    def setUp(self):
        self.publisher = Publisher()

    def test_that_install_publishes_the_right_event(self, publish):
        ctx = Mock(uuid=s.uuid)

        self.publisher.install(ctx, s.status)

        expected_event = PluginInstallProgressEvent(s.uuid, s.status)

        publish.assert_called_once_with(expected_event)

    def test_that_install_error_publish_an_error(self, publish):
        ctx = Mock(uuid=s.uuid)

        self.publisher.install_error(ctx, s.error_id, s.message, None)

        errors = {
            'error_id': s.error_id,
            'message': s.message,
            'resource': 'plugins',
            'details': {},
        }
        expected_event = PluginInstallProgressEvent(s.uuid, 'error', errors=errors)

        publish.assert_called_once_with(expected_event)

    def test_that_uninstall_publishes_the_right_event(self, publish):
        ctx = Mock(uuid=s.uuid)

        self.publisher.uninstall(ctx, s.status)

        expected_event = PluginUninstallProgressEvent(s.uuid, s.status)

        publish.assert_called_once_with(expected_event)

    def test_that_uninstall_error_publish_an_error(self, publish):
        ctx = Mock(uuid=s.uuid)

        self.publisher.uninstall_error(ctx, s.error_id, s.message, None)

        errors = {
            'error_id': s.error_id,
            'message': s.message,
            'resource': 'plugins',
            'details': {},
        }
        expected_event = PluginUninstallProgressEvent(s.uuid, 'error', errors=errors)

        publish.assert_called_once_with(expected_event)
