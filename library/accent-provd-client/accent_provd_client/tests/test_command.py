# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch

from hamcrest import assert_that, calling, raises
from requests.exceptions import HTTPError

from ..command import ProvdCommand
from ..exceptions import ProvdError, ProvdServiceUnavailable


class TestProvdCommand(TestCase):
    @patch('accent_provd_client.command.RESTCommand.raise_from_response')
    def test_raise_from_response_no_error(self, parent_raise):
        response = Mock()
        ProvdCommand.raise_from_response(response)

        parent_raise.assert_called_once_with(response)

    def test_raise_from_response_503(self):
        response = Mock(status_code=503)

        assert_that(
            calling(ProvdCommand.raise_from_response).with_args(response),
            raises(ProvdServiceUnavailable),
        )

    def test_raise_from_response_default_error(self):
        response = Mock()
        response.raise_for_status.side_effect = HTTPError('Error')

        assert_that(
            calling(ProvdCommand.raise_from_response).with_args(response),
            raises(ProvdError),
        )
        response.raise_for_status.assert_called_once()
