# tests/commands/tests/test_status.py

import pytest
import httpx
from accent_amid_client.commands.status import StatusCommand
from accent_amid_client.exceptions import AmidError


@pytest.fixture
def status_command(mock_client):
    return StatusCommand(mock_client)


def test_status(status_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/status"
    httpx_mock.get(url).mock(return_value=httpx.Response(200, json={"status": "OK"}))

    result = status_command()
    assert result == {"status": "OK"}
    assert httpx_mock.get(url).called_once


def test_status_http_error(status_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/status"
    httpx_mock.get(url).mock(return_value=httpx.Response(503))

    with pytest.raises(httpx.HTTPStatusError):  # Corrected exception type
        status_command()
    assert httpx_mock.get(url).called_once
