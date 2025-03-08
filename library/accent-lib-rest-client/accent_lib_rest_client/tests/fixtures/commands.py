from typing import Any

import httpx
import pytest

from accent_lib_rest_client import RESTCommand
from accent_lib_rest_client.exceptions import HTTPError


@pytest.fixture
def command_class() -> type[RESTCommand]:
    """Base command class fixture to be overridden."""
    class TestCommand(RESTCommand):
        resource = 'test'
    return TestCommand

@pytest.fixture
def base_url(command_class: type[RESTCommand]) -> str:
    """Get base URL for the command."""
    return command_class.resource

@pytest.fixture
def command_client(mocker, base_url: str):
    """Create a mock client for command testing."""
    client = mocker.Mock()
    client.timeout = mocker.sentinel.timeout
    client.tenant_uuid = None
    client.url = mocker.Mock(return_value=base_url)
    return client

@pytest.fixture
def command_session(mocker, command_client):
    """Create a mock session for command testing."""
    session = mocker.Mock(spec=httpx.Client)
    session.headers = {}
    command_client.session.return_value = session
    return session

@pytest.fixture
def command(command_class: type[RESTCommand], command_client) -> RESTCommand:
    """Create command instance for testing."""
    return command_class(command_client)

def create_response(mocker, status_code: int, json: Any = None, body: Any = None):
    """Create a mock response with the given parameters."""
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = status_code

    if status_code >= 300:
        response.raise_for_status.side_effect = HTTPError(response)

    if json is not None:
        response.json.return_value = json
    elif body is not None:
        response.text = body
        response.content = body
    else:
        response.json.side_effect = ValueError()

    return response