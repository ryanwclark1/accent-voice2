# Copyright 2025 Accent Communications

import pytest
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client.client import AuthClient


class TestAuthClient:
    """Test the AuthClient class."""

    def test_init(self):
        """Test client initialization."""
        client = AuthClient(
            host="test.example.com",
            port=443,
            version="0.1",
            username="test_user",
            password="test_password",
        )

        assert client.host == "test.example.com"
        assert client.port == 443
        assert client.version == "0.1"
        assert client.username == "test_user"
        assert client.password == "test_password"
        assert client.namespace == "accent_auth_client.commands"

    def test_sync_client_with_auth(self, auth_client, mock_httpx_client):
        """Test the sync_client property adds authentication."""
        # Get the client to trigger property
        client = auth_client.sync_client

        # Check that auth is set
        assert client.auth is not None
        assert isinstance(client.auth, httpx.BasicAuth)

    @pytest.mark.asyncio
    async def test_async_client_with_auth(self, auth_client, mock_httpx_async_client):
        """Test the async_client property adds authentication."""
        # Get the client to trigger property
        client = auth_client.async_client

        # Check that auth is set
        assert client.auth is not None
        assert isinstance(client.auth, httpx.BasicAuth)

    def test_session_deprecation_warning(self, auth_client):
        """Test that session() method logs a deprecation warning."""
        with patch("accent_auth_client.client.logger") as mock_logger:
            client = auth_client.session()

            # Check that warning was logged
            mock_logger.warning.assert_called_once_with(
                "Deprecated method 'session()' called. Use 'sync_client' instead"
            )

    def test_command_loading(self, auth_client):
        """Test that commands are loaded correctly."""
        # Check that commands are available
        assert hasattr(auth_client, "token")
        assert hasattr(auth_client, "users")
        assert hasattr(auth_client, "groups")
        assert hasattr(auth_client, "tenants")
        assert hasattr(auth_client, "policies")
        assert hasattr(auth_client, "sessions")
        assert hasattr(auth_client, "status")
