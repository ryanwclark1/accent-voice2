# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch

from hamcrest import assert_that, calling, not_, raises

from accent_dird import plugin_manager


class TestPluginManagerServices(TestCase):
    def test_unload_services_calls_unload_on_services(self):
        plugin_manager.services_extension_manager = Mock()

        plugin_manager.unload_services()

        plugin_manager.services_extension_manager.map_method.assert_called_once_with('unload')

    def test_that_unload_services_does_nothing_when_load_services_has_not_been_run(
        self,
    ):
        with patch('accent_dird.plugin_manager.services_extension_manager', None):
            assert_that(calling(plugin_manager.unload_services), not_(raises(Exception)))
