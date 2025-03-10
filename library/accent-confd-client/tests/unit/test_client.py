# Copyright 2025 Accent Communications

"""Tests for the Configuration Daemon client."""

import httpx
import pytest
from accent_confd_client.client import ConfdClient

from tests.mocks.httpx_utils import configure_mock_responses


def test_client_initialization() -> None:
    """Test client initialization."""
    # Test with default values
    client = ConfdClient("example.com")
    assert client.config.host == "example.com"
    assert client.config.port == 443
    assert client.config.prefix == "/api/confd"
    assert client.config.version == "1.1"

    # Test with custom values
    client = ConfdClient(
        host="custom.com",
        port=8443,
        prefix="/custom/api",
        version="2.0",
        token="test-token",
        tenant_uuid="test-tenant",
        https=False,
    )
    assert client.config.host == "custom.com"
    assert client.config.port == 8443
    assert client.config.prefix == "/custom/api"
    assert client.config.version == "2.0"
    assert client.config.token == "test-token"
    assert client.config.tenant_uuid == "test-tenant"
    assert client.config.https is False


def test_url_generation(client: ConfdClient) -> None:
    """Test URL generation.

    Args:
        client: Client instance

    """
    # Test base URL
    base_url = client.url()
    assert base_url == "https://example.com:443/api/confd/1.1"

    # Test URL with path
    resource_url = client.url("users")
    assert resource_url == "https://example.com:443/api/confd/1.1/users"

    # Test URL with path and ID
    resource_id_url = client.url("users", "123")
    assert resource_id_url == "https://example.com:443/api/confd/1.1/users/123"


def test_is_server_reachable(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test server reachability check.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses
    httpx_mock.add_response(method="HEAD", url=base_url, status_code=200)

    # Test reachability
    assert client.is_server_reachable() is True

    # Test unreachable server
    httpx_mock.reset()
    httpx_mock.add_exception(httpx.ConnectError("Connection refused"))

    assert client.is_server_reachable() is False


@pytest.mark.asyncio
async def test_is_server_reachable_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test server reachability check asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses
    httpx_mock.add_response(method="HEAD", url=base_url, status_code=200)

    # Test reachability asynchronously
    assert await client.is_server_reachable_async() is True

    # Test unreachable server
    httpx_mock.reset()
    httpx_mock.add_exception(httpx.ConnectError("Connection refused"))

    assert await client.is_server_reachable_async() is False


def test_session_compatibility(client: ConfdClient) -> None:
    """Test session compatibility method.

    Args:
        client: Client instance

    """
    # Test that the session method returns a session object
    session = client.session()
    assert session is not None

    # Ensure the same client is returned for multiple calls
    assert client.sync_client is client.session()


def test_command_loading(client: ConfdClient) -> None:
    """Test command loading.

    Args:
        client: Client instance

    """
    # Verify that essential commands are loaded
    assert hasattr(client, "users")
    assert hasattr(client, "devices")
    assert hasattr(client, "call_logs")
    assert hasattr(client, "funckeys")
    assert hasattr(client, "infos")
    assert hasattr(client, "wizard")
