# Copyright 2025 Accent Communications

import os
import pytest
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client import Client


@pytest.fixture
def mock_httpx_client():
    """Create a mock httpx client."""
    mock_client = MagicMock(spec=httpx.Client)
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_response.content = b'{"status": "ok"}'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    mock_client.put.return_value = mock_response
    mock_client.delete.return_value = mock_response
    mock_client.head.return_value = mock_response
    mock_client.patch.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_httpx_async_client():
    """Create a mock httpx async client."""
    mock_client = MagicMock(spec=httpx.AsyncClient)
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_response.content = b'{"status": "ok"}'
    mock_response.headers = {"Content-Type": "application/json"}

    async def mock_get(*args, **kwargs):
        return mock_response

    async def mock_post(*args, **kwargs):
        return mock_response

    async def mock_put(*args, **kwargs):
        return mock_response

    async def mock_delete(*args, **kwargs):
        return mock_response

    async def mock_head(*args, **kwargs):
        return mock_response

    async def mock_patch(*args, **kwargs):
        return mock_response

    mock_client.get = mock_get
    mock_client.post = mock_post
    mock_client.put = mock_put
    mock_client.delete = mock_delete
    mock_client.head = mock_head
    mock_client.patch = mock_patch

    return mock_client


@pytest.fixture
def auth_client(mock_httpx_client, mock_httpx_async_client):
    """Create a Client instance with mocked HTTP clients."""
    with patch("accent_auth_client.client.BaseClient._create_client") as mock_create:
        mock_create.return_value = mock_httpx_client
        client = Client(
            host="test.example.com",
            port=443,
            version="0.1",
            username="test_user",
            password="test_password",
        )
        # Override the clients with our mocks
        client._sync_client = mock_httpx_client
        client._async_client = mock_httpx_async_client
        return client


@pytest.fixture
def test_token():
    """Return a test token for authentication tests."""
    return "test-token-12345"


@pytest.fixture
def test_user_uuid():
    """Return a test user UUID."""
    return "00000000-0000-4000-a000-000000000001"


@pytest.fixture
def test_group_uuid():
    """Return a test group UUID."""
    return "00000000-0000-4000-a000-000000000002"


@pytest.fixture
def test_policy_uuid():
    """Return a test policy UUID."""
    return "00000000-0000-4000-a000-000000000003"


@pytest.fixture
def test_tenant_uuid():
    """Return a test tenant UUID."""
    return "00000000-0000-4000-a000-000000000004"


@pytest.fixture
def test_session_uuid():
    """Return a test session UUID."""
    return "00000000-0000-4000-a000-000000000005"


# Sample response data for different endpoints
@pytest.fixture
def user_data():
    """Return sample user data."""
    return {
        "uuid": "00000000-0000-4000-a000-000000000001",
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "emails": [
            {
                "uuid": "00000000-0000-4000-a000-000000000010",
                "address": "test@example.com",
                "confirmed": True,
                "main": True,
            }
        ],
        "enabled": True,
    }


@pytest.fixture
def token_data():
    """Return sample token data."""
    return {
        "data": {
            "token": "test-token-12345",
            "auth_id": "testuser",
            "accent_uuid": "00000000-0000-4000-a000-000000000001",
            "expires_at": "2025-12-31T23:59:59+00:00",
            "utc_expires_at": "2025-12-31T23:59:59+00:00",
            "issued_at": "2025-01-01T00:00:00+00:00",
            "utc_issued_at": "2025-01-01T00:00:00+00:00",
            "session_uuid": "00000000-0000-4000-a000-000000000005",
            "user_agent": "test-client",
            "remote_addr": "127.0.0.1",
            "acl": ["auth.users.read", "auth.tenants.read"],
            "metadata": {
                "uuid": "00000000-0000-4000-a000-000000000001",
                "tenant_uuid": "00000000-0000-4000-a000-000000000004",
                "auth_id": "testuser",
                "pbx_user_uuid": "00000000-0000-4000-a000-000000000001",
                "accent_uuid": "00000000-0000-4000-a000-000000000001",
            },
        }
    }
