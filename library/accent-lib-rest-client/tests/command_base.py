from __future__ import annotations

import pytest

from accent_lib_rest_client import RESTCommand
from accent_lib_rest_client.exceptions import HTTPError


class CommandBase:
    """Base class for command testing."""
    Command: type[RESTCommand]  # This defines the type hint for Command class

    @pytest.fixture(autouse=True)
    def setup_command(self, mocker):
        """Set up command for testing."""
        if not hasattr(self, 'Command'):
            pytest.fail("Command class not defined")

        self.base_url = self.Command.resource
        self.client = mocker.Mock()
        self.client.timeout = mocker.sentinel.timeout
        self.client.tenant = mocker.Mock(return_value=None)
        self.client.url = mocker.Mock(return_value=self.base_url)
        self.session = self.client.session.return_value
        self.session.headers = {}
        self.command = self.Command(self.client)

    def raises_http_error(self, function, *args, **kwargs):
        """Check if function raises HTTPError."""
        with pytest.raises(HTTPError):
            function(*args, **kwargs)

    def new_response(self, mocker, status_code: int, json=None, body=None):
        """Create a new mock response."""
        response = mocker.Mock()
        response.status_code = status_code
        if status_code >= 300:
            response.raise_for_status.side_effect = HTTPError()
        if json is not None:
            response.json.return_value = json
        elif body is not None:
            response.text = body
            response.content = body
        else:
            response.json.side_effect = ValueError()
        return response

    def set_response(self, mocker, action: str, status_code: int, body=None):
        """Set the response for a given action."""
        mock_action = getattr(self.session, action)
        mock_action.return_value = self.new_response(mocker, status_code, json=body)
        return body

    def assert_request_sent(self, action: str, url: str, **kwargs):
        """Assert that a request was sent with the given parameters."""
        mock_action = getattr(self.session, action)
        mock_action.assert_called_once_with(url, **kwargs)


class RESTCommandBase(CommandBase):
    """Base class for REST command testing."""
    Command: type[RESTCommand]  # Reinforces the type hint for clarity

    scheme = 'http'
    host = 'accentvoice.io'
    port = 9486
    version = '1.0'

    @pytest.fixture(autouse=True)
    def setup_rest(self, setup_command):
        """Set up REST-specific attributes."""
        self.base_url = self.command.base_url
