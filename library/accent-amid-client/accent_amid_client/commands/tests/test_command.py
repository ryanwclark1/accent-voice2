# Copyright 2023 Accent Communications

from hamcrest import assert_that, equal_to
from accent_lib_rest_client.tests.command import RESTCommandTestCase

from ..command import CommandCommand


class TestCommand(RESTCommandTestCase):
    Command = CommandCommand

    def test_command(self):
        asterisk_command = 'core show channels'
        self.session.post.return_value = self.new_response(
            200, json={'return': 'value'}
        )

        result = self.command(asterisk_command)

        self.session.post.assert_called_once_with(
            f'{self.base_url}/Command',
            json={'command': asterisk_command},
        )
        assert_that(result, equal_to({'return': 'value'}))
