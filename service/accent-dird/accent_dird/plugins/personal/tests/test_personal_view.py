# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock

from hamcrest import assert_that, equal_to

from ..http import PersonalAll, PersonalImport, PersonalOne
from ..plugin import PersonalViewPlugin


class TestPersonalView(TestCase):
    def setUp(self):
        self.plugin = PersonalViewPlugin()
        self.api = Mock()

    def test_that_load_with_no_personal_service_does_not_add_routes(self):
        self.plugin.load({'config': {}, 'http_namespace': Mock(), 'api': self.api, 'services': {}})

        assert_that(self.api.add_resource.call_count, equal_to(0))

    def test_that_load_adds_the_routes(self):
        args = {
            'config': {'displays': {}, 'profile_to_display': {}},
            'http_namespace': Mock(),
            'api': self.api,
            'services': {'personal': Mock()},
        }

        self.plugin.load(args)

        self.api.add_resource.assert_any_call(PersonalAll, PersonalViewPlugin.personal_all_url)
        self.api.add_resource.assert_any_call(PersonalOne, PersonalViewPlugin.personal_one_url)
        self.api.add_resource.assert_any_call(PersonalImport, PersonalViewPlugin.personal_import_url)
