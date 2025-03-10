# Copyright 2025 Accent Communications

"""Unit tests for the BaseClient class."""

import os
from unittest.mock import patch

import httpx
import pytest
from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.exceptions import InvalidArgumentError
from pytest_mock import MockerFixture


# Test client implementation for unit testing
class TestClientImpl(BaseClient):
    """Test client implementation to avoid namespace issues."""

    namespace = "test_client_namespace"


class TestBaseClient:
    """Test cases for the BaseClient class."""

    def test_init_requires_host(self) -> None:
        """Test that initialization requires a host."""
        with pytest.raises(InvalidArgumentError):
            TestClientImpl(host="")

    def test_init_sets_config(self) -> None:
        """Test that initialization sets the config properly."""
        client = TestClientImpl(
            host="example.com",
            port=8080,
            version="v1",
            token="abc123",
            tenant_uuid="tenant1",
            https=True,
            timeout=5.0,
        )

        assert client.config.host == "example.com"
        assert client.config.port == 8080
        assert client.config.version == "v1"
        assert client.config.token == "abc123"
        assert client.config.tenant_uuid == "tenant1"
        assert client.config.https is True
        assert client.config.timeout == 5.0

    def test_build_prefix(self) -> None:
        """Test prefix building logic."""
        client = TestClientImpl(host="example.com")

        assert client._build_prefix(None) == ""
        assert client._build_prefix("") == ""
        assert client._build_prefix("api") == "/api"
        assert client._build_prefix("/api") == "/api"

    def test_url_building(self) -> None:
        """Test URL building with various parameters."""
        # Basic URL
        client = TestClientImpl(host="example.com")
        assert client.url() == "https://example.com"

        # With port
        client = TestClientImpl(host="example.com", port=8080)
        assert client.url() == "https://example.com:8080"

        # With version
        client = TestClientImpl(host="example.com", version="v1")
        assert client.url() == "https://example.com/v1"

        # With prefix
        client = TestClientImpl(host="example.com", prefix="api")
        assert client.url() == "https://example.com/api"

        # With HTTP instead of HTTPS
        client = TestClientImpl(host="example.com", https=False)
        assert client.url() == "http://example.com"

        # With all options and fragments
        client = TestClientImpl(
            host="example.com",
            port=8080,
            version="v1",
            prefix="api",
            https=True,
        )
        assert client.url() == "https://example.com:8080/api/v1"
        assert client.url("resource") == "https://example.com:8080/api/v1/resource"
        assert (
            client.url("resource", "item")
            == "https://example.com:8080/api/v1/resource/item"
        )

    def test_sync_client_creation(self) -> None:
        """Test synchronous client creation."""
        client = TestClientImpl(
            host="example.com",
            token="abc123",
            tenant_uuid="tenant1",
            user_agent="test-agent",
        )

        sync_client = client.sync_client
        assert isinstance(sync_client, httpx.Client)
        assert sync_client.headers["X-Auth-Token"] == "abc123"
        assert sync_client.headers["Accent-Tenant"] == "tenant1"
        assert sync_client.headers["User-agent"] == "test-agent"
        assert sync_client.headers["Connection"] == "close"

    def test_session_deprecated(self, mocker: MockerFixture) -> None:
        """Test that session() method is deprecated but works."""
        mock_logger = mocker.patch("accent_lib_rest_client.client.logger")

        client = TestClientImpl(host="example.com")
        session = client.session()

        assert isinstance(session, httpx.Client)
        mock_logger.warning.assert_called_once()

    def test_set_token(self) -> None:
        """Test setting a token after initialization."""
        client = TestClientImpl(host="example.com")

        # Initially no token
        assert client.config.token is None

        # Set a token
        client.set_token("new-token")
        assert client.config.token == "new-token"

        # Check that the client gets recreated with the new token
        assert client._sync_client is None  # Should be reset
        sync_client = client.sync_client
        assert sync_client.headers["X-Auth-Token"] == "new-token"

    def test_set_tenant_deprecated(self, mocker: MockerFixture) -> None:
        """Test that set_tenant() method is deprecated but works."""
        mock_logger = mocker.patch("accent_lib_rest_client.client.logger")

        client = TestClientImpl(host="example.com")
        client.set_tenant("new-tenant")

        assert client.config.tenant_uuid == "new-tenant"
        mock_logger.warning.assert_called_once()

    def test_tenant_deprecated(self, mocker: MockerFixture) -> None:
        """Test that tenant() method is deprecated but works."""
        mock_logger = mocker.patch("accent_lib_rest_client.client.logger")

        client = TestClientImpl(host="example.com", tenant_uuid="test-tenant")
        tenant = client.tenant()

        assert tenant == "test-tenant"
        mock_logger.warning.assert_called_once()

    def test_is_server_reachable(self) -> None:
        """Test checking if server is reachable."""
        # Create client and set up mock responses directly
        client = TestClientImpl(host="example.com")

        # Test successful response
        with patch.object(client, "sync_client") as mock_client:
            mock_client.head.return_value = httpx.Response(200)
            assert client.is_server_reachable() is True

        # Test HTTP error (server is still reachable)
        with patch.object(client, "sync_client") as mock_client:
            mock_client.head.side_effect = httpx.HTTPStatusError(
                "HTTP Error",
                request=httpx.Request("HEAD", "https://example.com"),
                response=httpx.Response(500),
            )
            assert client.is_server_reachable() is True

        # Test connection error (server is not reachable)
        with patch.object(client, "sync_client") as mock_client:
            mock_client.head.side_effect = httpx.ConnectError("Failed to connect")
            assert client.is_server_reachable() is False

    @pytest.mark.asyncio
    async def test_is_server_reachable_async(self) -> None:
        """Test checking if server is reachable asynchronously."""
        # Create client and set up mock responses directly
        client = TestClientImpl(host="example.com")

        # Test successful response
        with patch.object(client, "async_client") as mock_client:
            mock_client.head.return_value = httpx.Response(200)
            assert await client.is_server_reachable_async() is True

        # Test HTTP error (server is still reachable)
        with patch.object(client, "async_client") as mock_client:
            mock_client.head.side_effect = httpx.HTTPStatusError(
                "HTTP Error",
                request=httpx.Request("HEAD", "https://example.com"),
                response=httpx.Response(500),
            )
            assert await client.is_server_reachable_async() is True

        # Test connection error (server is not reachable)
        with patch.object(client, "async_client") as mock_client:
            mock_client.head.side_effect = httpx.ConnectError("Failed to connect")
            assert await client.is_server_reachable_async() is False

    def test_user_agent_from_argv(self) -> None:
        """Test that user_agent defaults to the program name."""
        with patch.object(os, "path") as mock_path:
            mock_path.basename.return_value = "test-program"

            client = TestClientImpl(host="example.com")
            assert client.config.user_agent == "test-program"
