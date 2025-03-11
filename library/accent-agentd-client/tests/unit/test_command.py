# tests/unit/test_command.py
import pytest
from unittest.mock import MagicMock
from accent_agentd_client.commands.agents import AgentsCommand
from accent_agentd_client.commands.status import StatusCommand

from accent_lib_rest_client.client import BaseClient


def test_agents_command_initialization(base_mock_client: BaseClient) -> None:
    """Tests the initialization of the AgentsCommand."""
    agents_command = AgentsCommand(base_mock_client)
    assert agents_command.resource == "agents"
    assert agents_command._req_factory._base_url == base_mock_client.url()


def test_status_command_initialization(base_mock_client: BaseClient) -> None:
    """Test initialization of StatusCommand."""
    status_command = StatusCommand(base_mock_client)
    assert status_command.resource == "status"
    assert status_command.base_url == f"{base_mock_client.url()}/status"

    # Test that headers are correctly set
    headers = status_command._get_headers()
    assert "Accept" in headers
    assert headers["Accept"] == "application/json"


def test_status_command_call(
    base_mock_client: BaseClient, mock_service_status: dict
) -> None:
    """Test __call__ method of StatusCommand."""
    status_command = StatusCommand(base_mock_client)
    base_mock_client.sync_client.get = MagicMock(
        return_value=MagicMock(status_code=200, json=lambda: mock_service_status)
    )  # Using lambda for json()

    status = status_command()
    assert status == mock_service_status
    base_mock_client.sync_client.get.assert_called_once_with(
        status_command.base_url, headers=status_command._get_headers()
    )


def test_status_command_call_failure(base_mock_client: BaseClient) -> None:
    """Test __call__ method of StatusCommand with a failure."""
    status_command = StatusCommand(base_mock_client)
    # Mock to simulate an error response
    base_mock_client.sync_client.get = MagicMock(
        return_value=MagicMock(status_code=404, json=lambda: {"error": "Not Found"})
    )

    with pytest.raises(Exception, match="Not Found"):
        status_command()
