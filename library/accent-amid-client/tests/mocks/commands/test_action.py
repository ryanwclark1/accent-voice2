# tests/commands/tests/test_action.py

import pytest
import httpx
from accent_amid_client.commands.action import ActionCommand
from accent_amid_client.models import AmidActionResult
from accent_amid_client.exceptions import AmidProtocolError


@pytest.fixture
def action_command(mock_client):
    return ActionCommand(mock_client)


def test_action_no_params(action_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/action/QueueSummary"
    httpx_mock.post(url).mock(
        return_value=httpx.Response(
            200, json=[{"Response": "Success", "Queue": "support", "Members": 1}]
        )
    )

    result = action_command("QueueSummary")

    assert len(result) == 1
    assert isinstance(result[0], AmidActionResult)
    assert result[0].response == "Success"
    assert result[0].data == {"Queue": "support", "Members": 1}
    assert httpx_mock.get(url).called_once


def test_action_with_params(action_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/action/DBGet"
    httpx_mock.post(url, json={"Family": "testfamily", "Key": "testkey"}).mock(
        return_value=httpx.Response(
            200, json=[{"Response": "Success", "Value": "testvalue"}]
        )
    )

    result = action_command("DBGet", {"Family": "testfamily", "Key": "testkey"})

    assert len(result) == 1
    assert isinstance(result[0], AmidActionResult)
    assert result[0].response == "Success"
    assert result[0].data == {"Value": "testvalue"}
    assert httpx_mock.get(url).called_once


def test_action_protocol_error(action_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/action/ErrorAction"
    httpx_mock.post(url).mock(
        return_value=httpx.Response(
            200, json=[{"Response": "Error", "Message": "Action failed"}]
        )
    )

    with pytest.raises(AmidProtocolError) as excinfo:
        action_command("ErrorAction")
    assert "Action failed" in str(excinfo.value)
    assert httpx_mock.get(url).called_once


def test_action_http_error(action_command, mock_server, httpx_mock):
    url = f"{mock_server}/api/amid/1.0/action/HttpErrorAction"
    httpx_mock.post(url).mock(return_value=httpx.Response(500))
    with pytest.raises(httpx.HTTPStatusError):
        action_command("HttpErrorAction")
    assert httpx_mock.get(url).called_once
