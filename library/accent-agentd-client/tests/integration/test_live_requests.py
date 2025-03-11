# tests/integration/test_live_requests.py
import pytest
from accent_agentd_client import Client
from accent_agentd_client.models import AgentStatus
from accent_agentd_client.error import (
    AgentdClientError,
    UNAUTHORIZED,
    CONTEXT_DIFFERENT_TENANT,
)  # Import errors
from .conftest import (
    MOCK_SERVER_HOST,
    MOCK_SERVER_PORT,
    AGENT_ID,
    AGENT_NUMBER,
    EXTENSION,
    CONTEXT,
    LINE_ID,
    QUEUE_ID,
    TENANT_UUID,
    INVALID_TENANT_UUID,
)


def test_add_agent_to_queue_live(mock_client: Client, mock_server) -> None:
    """Tests adding an agent to a queue against the mock server."""
    mock_client.agents.add_agent_to_queue(AGENT_ID, QUEUE_ID, TENANT_UUID)


def test_remove_agent_from_queue_live(mock_client: Client, mock_server) -> None:
    """Tests removing an agent from a queue against the mock server."""
    mock_client.agents.remove_agent_from_queue(AGENT_ID, QUEUE_ID, TENANT_UUID)


def test_login_agent_live(mock_client: Client, mock_server) -> None:
    """Tests logging in an agent against the mock server."""
    mock_client.agents.login_agent(AGENT_ID, EXTENSION, CONTEXT, TENANT_UUID)


def test_login_agent_by_number_live(mock_client: Client, mock_server) -> None:
    """Tests logging in an agent by number against the mock server."""
    mock_client.agents.login_agent_by_number(
        AGENT_NUMBER, EXTENSION, CONTEXT, TENANT_UUID
    )


def test_logoff_agent_live(mock_client: Client, mock_server) -> None:
    """Tests logging off an agent against the mock server."""
    mock_client.agents.logoff_agent(AGENT_ID, TENANT_UUID)


def test_logoff_agent_by_number_live(mock_client: Client, mock_server) -> None:
    """Tests logging off an agent by number against the mock server."""
    mock_client.agents.logoff_agent_by_number(AGENT_NUMBER, TENANT_UUID)


def test_pause_agent_by_number_live(mock_client: Client, mock_server) -> None:
    """Tests pausing an agent by number"""
    mock_client.agents.pause_agent_by_number(AGENT_NUMBER, tenant_uuid=TENANT_UUID)


def test_unpause_agent_by_number_live(mock_client: Client, mock_server) -> None:
    """Test unpausing an agent by number."""
    mock_client.agents.unpause_agent_by_number(AGENT_NUMBER, tenant_uuid=TENANT_UUID)


def test_logoff_all_agents_live(mock_client: Client, mock_server) -> None:
    """Tests logging off all agents against the mock server."""
    mock_client.agents.logoff_all_agents(TENANT_UUID, recurse=True)


def test_relog_all_agents_live(mock_client: Client, mock_server) -> None:
    """Tests relogging all agents against the mock server."""
    mock_client.agents.relog_all_agents(TENANT_UUID, recurse=False)


def test_get_agent_status_live_content(mock_client: Client, mock_server) -> None:
    """Tests getting agent status and verifies the response content."""
    status = mock_client.agents.get_agent_status(AGENT_ID, TENANT_UUID)
    assert isinstance(status, AgentStatus)
    assert status.id == AGENT_ID
    assert status.number == AGENT_NUMBER
    assert status.logged is True  # Check specific fields
    # ... add more assertions based on your expected data ...


def test_get_agent_statuses_live_empty(mock_client: Client, mock_server) -> None:
    """Test case when no agents exist.  Requires server modification"""
    # This test will initially fail and that is expected.
    statuses = mock_client.agents.get_agent_statuses(
        TENANT_UUID, recurse=False
    )  # No tenant
    assert statuses == []


def test_authentication_failure_no_token(mock_client: Client, mock_server) -> None:
    """Tests authentication failure (no token)."""
    # Create a client *without* a token
    no_token_client = Client(host=MOCK_SERVER_HOST, port=MOCK_SERVER_PORT, token=None)
    with pytest.raises(AgentdClientError) as excinfo:
        no_token_client.agents.get_agent_status(
            AGENT_ID, TENANT_UUID
        )  # Any authenticated endpoint
    assert str(excinfo.value) == UNAUTHORIZED


def test_authentication_failure_invalid_token(mock_client: Client, mock_server) -> None:
    """Test authentication failure (invalid token)"""
    invalid_token_client = Client(
        host=MOCK_SERVER_HOST, port=MOCK_SERVER_PORT, token="wrong-token"
    )
    with pytest.raises(AgentdClientError) as excinfo:
        invalid_token_client.agents.get_agent_status(AGENT_ID, TENANT_UUID)
    assert str(excinfo.value) == UNAUTHORIZED


def test_tenant_isolation_failure(mock_client: Client, mock_server) -> None:
    """Test tenant isolation failure."""
    with pytest.raises(AgentdClientError) as excinfo:
        mock_client.agents.get_agent_status(AGENT_ID, tenant_uuid=INVALID_TENANT_UUID)
    assert str(excinfo.value) == CONTEXT_DIFFERENT_TENANT


def test_get_agent_status_by_number_live(mock_client: Client, mock_server) -> None:
    """Tests getting an agent's status by number against the mock server."""
    status = mock_client.agents.get_agent_status_by_number(AGENT_NUMBER, TENANT_UUID)
    assert isinstance(status, AgentStatus)
    assert status.number == AGENT_NUMBER


def test_get_agent_statuses_live(mock_client: Client, mock_server) -> None:
    """Tests getting all agent statuses against the mock server."""
    statuses = mock_client.agents.get_agent_statuses(TENANT_UUID, recurse=True)
    assert isinstance(statuses, list)
    assert all(isinstance(s, AgentStatus) for s in statuses)


def test_login_user_agent_live(mock_client: Client, mock_server) -> None:
    """Test login a user agent live."""
    mock_client.agents.login_user_agent(LINE_ID, tenant_uuid=TENANT_UUID)


def test_logoff_user_agent_live(mock_client: Client, mock_server) -> None:
    """Test logoff a user agent live."""
    mock_client.agents.logoff_user_agent(tenant_uuid=TENANT_UUID)


def test_pause_user_agent_live(mock_client: Client, mock_server) -> None:
    """Test pause user agent live."""
    mock_client.agents.pause_user_agent(tenant_uuid=TENANT_UUID)


def test_unpause_user_agent_live(mock_client: Client, mock_server) -> None:
    """Test unpause user agent live."""
    mock_client.agents.unpause_user_agent(tenant_uuid=TENANT_UUID)


def test_get_user_agent_status_live(mock_client: Client, mock_server) -> None:
    """Test get user agent status live."""
    status = mock_client.agents.get_user_agent_status(tenant_uuid=TENANT_UUID)
    assert isinstance(status, AgentStatus)


def test_status_command_live(mock_client: Client, mock_server) -> None:
    """Test service status command live."""
    status = mock_client.status()
    assert isinstance(status, dict)
    assert "status" in status
    assert "version" in status


@pytest.mark.asyncio
async def test_status_command_async_live(mock_client: Client, mock_server) -> None:
    """Test async version of service status command live."""
    status = await mock_client.status.__call_async__()
    assert isinstance(status, dict)
    assert "status" in status
    assert "version" in status
