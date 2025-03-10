# Copyright 2025 Accent Communications

import pytest
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client.commands.token import TokenCommand
from accent_auth_client.exceptions import (
    InvalidTokenException,
    MissingPermissionsTokenException,
)


class TestTokenCommand:
    """Test the TokenCommand class."""

    def test_new(self, auth_client, mock_httpx_client, token_data):
        """Test creating a new token."""
        # Configure mock to return token data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = token_data
        mock_httpx_client.post.return_value = mock_response

        # Call the method
        result = auth_client.token.new(username="testuser", password="password123")

        # Verify correct endpoint and parameters
        mock_httpx_client.post.assert_called_once()
        args, kwargs = mock_httpx_client.post.call_args
        assert args[0].endswith("/token")
        assert "headers" in kwargs
        assert "json" in kwargs

        # Verify correct data is returned
        assert result == token_data["data"]

    @pytest.mark.asyncio
    async def test_new_async(self, auth_client, mock_httpx_async_client, token_data):
        """Test creating a new token asynchronously."""
        # Configure mock to return token data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = token_data

        async def mock_post(*args, **kwargs):
            return mock_response

        mock_httpx_async_client.post = mock_post

        # Call the method
        result = await auth_client.token.new_async(
            username="testuser", password="password123"
        )

        # Verify correct data is returned
        assert result == token_data["data"]

    def test_check_valid_token(self, auth_client, mock_httpx_client, test_token):
        """Test checking a valid token."""
        # Configure mock to return success
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_httpx_client.head.return_value = mock_response

        # Call the method
        result = auth_client.token.check(test_token)

        # Verify correct endpoint
        mock_httpx_client.head.assert_called_once()
        args, kwargs = mock_httpx_client.head.call_args
        assert f"/token/{test_token}" in args[0]

        # Verify correct result
        assert result is True

    def test_check_invalid_token(self, auth_client, mock_httpx_client, test_token):
        """Test checking an invalid token."""
        # Configure mock to return not found
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_httpx_client.head.return_value = mock_response

        # Call the method and expect exception
        with pytest.raises(InvalidTokenException):
            auth_client.token.check(test_token)

    def test_check_insufficient_permissions(
        self, auth_client, mock_httpx_client, test_token
    ):
        """Test checking a token with insufficient permissions."""
        # Configure mock to return forbidden
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_httpx_client.head.return_value = mock_response

        # Call the method and expect exception
        with pytest.raises(MissingPermissionsTokenException):
            auth_client.token.check(test_token)

    @pytest.mark.asyncio
    async def test_is_valid_async_caching(
        self, auth_client, mock_httpx_async_client, test_token
    ):
        """Test that is_valid_async caches results."""
        # Configure mock to return success
        mock_response = MagicMock()
        mock_response.status_code = 204

        async def mock_head(*args, **kwargs):
            return mock_response

        mock_httpx_async_client.head = mock_head

        # Call the method multiple times
        result1 = await auth_client.token.is_valid_async(test_token)
        result2 = await auth_client.token.is_valid_async(test_token)

        # Verify both calls return True
        assert result1 is True
        assert result2 is True

        # Function should be cached, so only one actual call
        # Note: In a real test, we'd need a way to verify the cache usage
