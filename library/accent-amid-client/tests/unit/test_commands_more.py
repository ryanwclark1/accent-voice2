# tests/unit/test_commands_more.py
import pytest
from accent_amid_client.commands.status import StatusCommand
from accent_amid_client.models import JSON


def test_status_command_call_unit(mocker):
    """Unit test for StatusCommand.__call__ with mocked BaseClient methods."""
    mock_get_headers = mocker.patch(
        "accent_amid_client.command.AmidCommand._get_headers",
        return_value={"X-Test": "Value"},
    )
    mock_sync_get = mocker.patch(
        "httpx.Client.get",
        return_value=mocker.Mock(status_code=200, json=lambda: {"status": "OK"}),
    )

    client_mock = mocker.Mock()  # Mock the client
    client_mock.base_url = "http://example.com/api/amid/1.0/status"
    client_mock.sync_client = mocker.Mock()
    client_mock.sync_client.get = mock_sync_get
    command = StatusCommand(client_mock)
    result = command()

    mock_get_headers.assert_called_once()
    mock_sync_get.assert_called_once_with(
        "http://example.com/api/amid/1.0/status", headers={"X-Test": "Value"}
    )
    assert result == {"status": "OK"}


# Similar tests for async_call, and for other command classes.
