# tests/commands/tests/test_config.py

import pytest
import httpx
from accent_amid_client.commands.config import ConfigCommand


@pytest.fixture
def config_command(mock_client):
    return ConfigCommand(mock_client)


def test_config_get(config_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/config"
    httpx_mock.get(url).mock(
        return_value=httpx.Response(200, json={"setting1": "value1"})
    )
    result = config_command()
    assert result == {"setting1": "value1"}
    assert httpx_mock.get(url).called_once


def test_config_patch(config_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/config"
    httpx_mock.patch(url).mock(
        return_value=httpx.Response(200, json={"setting1": "new_value"})
    )
    result = config_command.patch({"setting1": "new_value"})
    assert result == {"setting1": "new_value"}
    assert httpx_mock.patch(url).called_once


def test_config_get_http_error(config_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/config"
    httpx_mock.get(url).mock(return_value=httpx.Response(500))

    with pytest.raises(httpx.HTTPStatusError):
        config_command()
    assert httpx_mock.get(url).called_once


def test_config_patch_http_error(config_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/config"
    httpx_mock.patch(url).mock(return_value=httpx.Response(400))

    with pytest.raises(httpx.HTTPStatusError):
        config_command.patch({"setting1": "new_value"})
    assert httpx_mock.patch(url).called_once
