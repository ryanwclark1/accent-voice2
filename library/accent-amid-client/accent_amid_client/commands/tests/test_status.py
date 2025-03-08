# Copyright 2023 Accent Communications

from hamcrest import assert_that, equal_to
from accent_lib_rest_client.tests.command import RESTCommandTestCase

from ..status import StatusCommand


class TestStatus(RESTCommandTestCase):
    Command = StatusCommand

    def test_status(self):
        json_response = {'return': 'value'}
        self.session.get.return_value = self.new_response(200, json=json_response)

        result = self.command()

        self.session.get.assert_called_once_with(
            f'{self.base_url}', headers={'Accept': 'application/json'}
        )
        assert_that(result, equal_to(json_response))
