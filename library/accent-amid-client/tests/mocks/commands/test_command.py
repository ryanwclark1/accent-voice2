# tests/commands/tests/test_command.py

import pytest
import httpx
from accent_amid_client.commands.command import CommandCommand
from accent_amid_client.exceptions import AmidError


@pytest.fixture
def command_command(mock_client):
    return CommandCommand(mock_client)


def test_command(command_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/action/Command"
    httpx_mock.post(url, json={"command": "core show channels"}).mock(
        return_value=httpx.Response(200, json={"output": "Channels: 1 active"})
    )

    result = command_command("core show channels")
    assert result == {"output": "Channels: 1 active"}
    assert httpx_mock.get(url).called_once


def test_command_http_error(command_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/action/Command"
    httpx_mock.post(url, json={"command": "invalid command"}).mock(
        return_value=httpx.Response(500)
    )

    with pytest.raises(httpx.HTTPStatusError):  # Corrected exception type
        command_command("invalid command")
    assert httpx_mock.get(url).called_once
