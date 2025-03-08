# Copyright 2023 Accent Communications

from hamcrest import assert_that, has_entry

from accent_confd_client.tests import TestCommand

from ..configuration import ConfigurationCommand


class TestInfos(TestCommand):
    Command = ConfigurationCommand

    def test_get(self):
        self.set_response('get', 200, {'enabled': True})

        result = self.command.live_reload.get()

        self.session.get.assert_called_once_with('/configuration/live_reload')
        assert_that(result, has_entry('enabled', True))

    def test_calling_infos_with_no_method(self):
        self.set_response('put', 204)

        self.command.live_reload.update({'enabled': True})

        self.session.put.assert_called_once_with(
            '/configuration/live_reload', {'enabled': True}
        )
