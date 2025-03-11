# tests/async/test_async_client.py
import pytest
from accent_agentd_client import Client
from accent_agentd_client.models import AgentStatus
from accent_agentd_client.error import AgentdClientError, NO_SUCH_AGENT
from httpx import Headers
import json
from unittest.mock import AsyncMock, MagicMock

pytestmark = pytest.mark.asyncio  # Mark all tests in this module as async


async def test_async_add_agent_to_queue(mock_client: Client, httpx_mock) -> None:
    """Tests adding an agent to a queue asynchronously."""
    await mock_client.agents.add_agent_to_queue_async(AGENT_ID, QUEUE_ID, TENANT_UUID)
    assert httpx_mock.get_request(url=f"/by-id/{AGENT_ID}/add") is not None


async def test_async_remove_agent_from_queue(mock_client: Client, httpx_mock) -> None:
    """Tests removing an agent from a queue asynchronously."""
    await mock_client.agents.remove_agent_from_queue_async(
        AGENT_ID, QUEUE_ID, TENANT_UUID
    )
    assert httpx_mock.get_request(url=f"/by-id/{AGENT_ID}/remove") is not None


async def test_async_login_agent(mock_client: Client, httpx_mock) -> None:
    """Tests logging in an agent asynchronously."""
    await mock_client.agents.login_agent_async(
        AGENT_ID, EXTENSION, CONTEXT, TENANT_UUID
    )
    assert httpx_mock.get_request(url=f"/by-id/{AGENT_ID}/login") is not None


async def test_async_login_agent_by_number(mock_client: Client, httpx_mock) -> None:
    """Tests logging in an agent by number asynchronously."""
    await mock_client.agents.login_agent_by_number_async(
        AGENT_NUMBER, EXTENSION, CONTEXT, TENANT_UUID
    )
    assert httpx_mock.get_request(url=f"/by-number/{AGENT_NUMBER}/login") is not None


async def test_async_logoff_agent(mock_client: Client, httpx_mock) -> None:
    """Tests logging off an agent asynchronously."""
    await mock_client.agents.logoff_agent_async(AGENT_ID, TENANT_UUID)
    assert httpx_mock.get_request(url=f"/by-id/{AGENT_ID}/logoff") is not None


async def test_async_logoff_agent_by_number(mock_client: Client, httpx_mock) -> None:
    """Tests logging off an agent by number asynchronously."""
    await mock_client.agents.logoff_agent_by_number_async(AGENT_NUMBER, TENANT_UUID)
    assert httpx_mock.get_request(url=f"/by-number/{AGENT_NUMBER}/logoff") is not None


async def test_async_pause_agent_by_number(mock_client: Client, httpx_mock) -> None:
    """Tests pausing an agent by number asynchronously."""
    await mock_client.agents.pause_agent_by_number_async(AGENT_NUMBER, TENANT_UUID)
    assert httpx_mock.get_request(url=f"/by-number/{AGENT_NUMBER}/pause") is not None


async def test_async_unpause_agent_by_number(mock_client: Client, httpx_mock) -> None:
    """Tests unpausing an agent by number asynchronously."""
    await mock_client.agents.unpause_agent_by_number_async(AGENT_NUMBER, TENANT_UUID)
    assert httpx_mock.get_request(url=f"/by-number/{AGENT_NUMBER}/unpause") is not None


async def test_async_logoff_all_agents(mock_client: Client, httpx_mock) -> None:
    """Tests logging off all agents asynchronously."""
    await mock_client.agents.logoff_all_agents_async(TENANT_UUID, recurse=True)
    assert httpx_mock.get_request(url=f"/logoff") is not None


async def test_async_relog_all_agents(mock_client: Client, httpx_mock) -> None:
    """Tests relogging all agents asynchronously."""
    await mock_client.agents.relog_all_agents_async(TENANT_UUID, recurse=False)
    assert httpx_mock.get_request(url=f"/relog") is not None


async def test_async_get_agent_status_success(
    mock_client: Client, httpx_mock, mock_agent_status_logged_in: dict
) -> None:
    """Tests getting an agent's status (logged in) asynchronously."""
    status = await mock_client.agents.get_agent_status_async(AGENT_ID, TENANT_UUID)
    assert status == AgentStatus.from_dict(mock_agent_status_logged_in)

    # More detailed assertions about the request
    request = httpx_mock.get_request(url=f"/by-id/{AGENT_ID}")
    assert request is not None
    assert request.headers["accent-tenant"] == TENANT_UUID  # Check header


async def test_async_get_agent_status_not_found(
    mock_client: Client, httpx_mock, mock_no_such_agent_error
) -> None:
    """Test async get agent status for an invalid agent."""
    with pytest.raises(AgentdClientError) as e:
        await mock_client.agents.get_agent_status_async("invalid_agent", TENANT_UUID)
    assert str(e.value) == NO_SUCH_AGENT


async def test_async_get_agent_statuses_empty(
    mock_client: Client, httpx_mock, mock_agent_statuses_empty: list
) -> None:
    """Tests getting all agent statuses when there are no agents."""
    statuses = (
        await mock_client.agents.get_agent_statuses_async()
    )  # No tenant, no recurse
    assert statuses == []  # Expect an empty list

    request = httpx_mock.get_request(url=f"/")  # No params
    assert request is not None
    assert "accent-tenant" not in request.headers  # No tenant


async def test_async_add_agent_to_queue_with_headers(
    mock_client: Client, httpx_mock
) -> None:
    """Test async add agent to queue with header verification"""
    await mock_client.agents.add_agent_to_queue_async(AGENT_ID, QUEUE_ID, TENANT_UUID)
    request = httpx_mock.get_request(url=f"/by-id/{AGENT_ID}/add")
    assert request is not None
    assert request.headers["accent-tenant"] == TENANT_UUID
    assert request.headers["content-type"] == "application/json"
    req_body = json.loads(request.content)
    assert req_body["queue_id"] == QUEUE_ID


async def test_async_get_agent_status_by_number(
    mock_client: Client, httpx_mock, mock_agent_status_logged_in: dict
) -> None:
    """Tests getting an agent's status by number asynchronously."""
    status = await mock_client.agents.get_agent_status_by_number_async(
        AGENT_NUMBER, TENANT_UUID
    )
    assert status == AgentStatus.from_dict(mock_agent_status_logged_in)
    assert httpx_mock.get_request(url=f"/by-number/{AGENT_NUMBER}") is not None


async def test_async_get_agent_statuses(
    mock_client: Client, httpx_mock, mock_agent_statuses_multiple: list
) -> None:
    """Tests getting all agent statuses asynchronously."""
    statuses = await mock_client.agents.get_agent_statuses_async(
        TENANT_UUID, recurse=True
    )
    assert statuses == [AgentStatus.from_dict(s) for s in mock_agent_statuses_multiple]
    assert httpx_mock.get_request(url=f"/") is not None  # Corrected URL


async def test_async_login_user_agent(mock_client: Client, httpx_mock) -> None:
    """Test async login user agent."""
    await mock_client.agents.login_user_agent_async(LINE_ID, tenant_uuid=TENANT_UUID)
    assert httpx_mock.get_request(url=f"/users/me/agents/login") is not None


async def test_async_logoff_user_agent(mock_client: Client, httpx_mock) -> None:
    """Test async logoff user agent"""
    await mock_client.agents.logoff_user_agent_async(tenant_uuid=TENANT_UUID)
    assert httpx_mock.get_request(url=f"/users/me/agents/logoff") is not None


async def test_async_pause_user_agent(mock_client: Client, httpx_mock) -> None:
    """Test async pause user agent"""
    await mock_client.agents.pause_user_agent_async(tenant_uuid=TENANT_UUID)
    assert httpx_mock.get_request(url=f"/users/me/agents/pause") is not None


async def test_async_unpause_user_agent(mock_client: Client, httpx_mock) -> None:
    """Test async unpause user agent."""
    await mock_client.agents.unpause_user_agent_async(tenant_uuid=TENANT_UUID)
    assert httpx_mock.get_request(url=f"/users/me/agents/unpause") is not None


async def test_async_get_user_agent_status(
    mock_client: Client, httpx_mock, mock_agent_status_logged_in: dict
) -> None:
    """Test async get user agent status"""
    status = await mock_client.agents.get_user_agent_status_async(
        tenant_uuid=TENANT_UUID
    )
    assert status == AgentStatus.from_dict(mock_agent_status_logged_in)
    assert httpx_mock.get_request(url=f"/users/me/agents") is not None


async def test_async_status_command_call(
    mock_client: Client, mock_service_status: dict
) -> None:
    """Test __call_async__ method of StatusCommand."""
    from accent_agentd_client.commands.status import StatusCommand

    status_command = StatusCommand(mock_client)
    mock_client.async_client.get = AsyncMock(
        return_value=MagicMock(status_code=200, json=lambda: mock_service_status)
    )  # Using lambda for json()

    status = await status_command.__call_async__()
    assert status == mock_service_status
    mock_client.async_client.get.assert_awaited_once_with(
        status_command.base_url, headers=status_command._get_headers()
    )


async def test_async_status_command_call_failure(mock_client: Client) -> None:
    """Test async call of status command with failure."""
    from accent_agentd_client.commands.status import StatusCommand

    status_command = StatusCommand(mock_client)
    mock_client.async_client.get = AsyncMock(
        return_value=MagicMock(status_code=404, json=lambda: {"error": "Not Found"})
    )
    with pytest.raises(AgentdClientError, match="Not Found"):
        await status_command.__call_async__()
