# Copyright 2025 Accent Communications

import pytest
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client import Client
from accent_auth_client.exceptions import (
    InvalidTokenException,
    MissingPermissionsTokenException,
)


@pytest.mark.integration
class TestAuthentication:
    """Integration tests for authentication flows."""

    @pytest.fixture
    def mock_responses(self):
        """Prepare mock responses for different endpoints."""
        token_response = MagicMock(spec=httpx.Response)
        token_response.status_code = 200
        token_response.json.return_value = {
            "data": {
                "token": "test-token-12345",
                "auth_id": "testuser",
                "accent_uuid": "00000000-0000-4000-a000-000000000001",
                "expires_at": "2025-12-31T23:59:59+00:00",
                "utc_expires_at": "2025-12-31T23:59:59+00:00",
                "issued_at": "2025-01-01T00:00:00+00:00",
                "utc_issued_at": "2025-01-01T00:00:00+00:00",
                "session_uuid": "00000000-0000-4000-a000-000000000005",
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

        valid_token_check = MagicMock(spec=httpx.Response)
        valid_token_check.status_code = 204

        invalid_token_check = MagicMock(spec=httpx.Response)
        invalid_token_check.status_code = 404

        return {
            "token": token_response,
            "valid_token": valid_token_check,
            "invalid_token": invalid_token_check,
        }

    def test_token_auth_flow(self, mock_responses):
        """Test complete token authentication flow."""
        # Set up mocks
        client = Client(host="test.example.com", port=443, version="0.1")

        # Override sync client for test
        client._sync_client = MagicMock(spec=httpx.Client)

        # Configure responses
        client._sync_client.post.return_value = mock_responses["token"]
        client._sync_client.head.return_value = mock_responses["valid_token"]

        # Step 1: Get a token
        token_data = client.token.new(username="testuser", password="password123")

        # Verify we got a token
        assert token_data["token"] == "test-token-12345"

        # Step 2: Set the token on the client
        client.set_token(token_data["token"])

        # Step 3: Verify the token is valid
        is_valid = client.token.check(token_data["token"])
        assert is_valid is True

        # Step 4: Check token scopes
        client._sync_client.post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "allowed": ["auth.users.read"],
                "denied": ["auth.users.create"],
            },
        )

        scopes_result = client.token.check_scopes(
            token_data["token"], ["auth.users.read", "auth.users.create"]
        )
        assert "allowed" in scopes_result
        assert "denied" in scopes_result
        assert "auth.users.read" in scopes_result["allowed"]

        # Step 5: Revoke the token
        client._sync_client.delete.return_value = MagicMock(status_code=204)
        client.token.revoke(token_data["token"])

        # Step 6: Verify token is now invalid
        client._sync_client.head.return_value = mock_responses["invalid_token"]
        with pytest.raises(InvalidTokenException):
            client.token.check(token_data["token"])

    @pytest.mark.asyncio
    async def test_async_token_auth_flow(self, mock_responses):
        """Test complete token authentication flow with async methods."""
        # Set up mocks
        client = Client(host="test.example.com", port=443, version="0.1")

        # Override async client for test
        client._async_client = MagicMock(spec=httpx.AsyncClient)

        # Configure responses
        async def mock_post(*args, **kwargs):
            return mock_responses["token"]

        async def mock_head(*args, **kwargs):
            return mock_responses["valid_token"]

        async def mock_delete(*args, **kwargs):
            response = MagicMock(spec=httpx.Response)
            response.status_code = 204
            return response

        client._async_client.post = mock_post
        client._async_client.head = mock_head
        client._async_client.delete = mock_delete

        # Step 1: Get a token asynchronously
        token_data = await client.token.new_async(
            username="testuser", password="password123"
        )

        # Verify we got a token
        assert token_data["token"] == "test-token-12345"

        # Step 2: Set the token on the client
        client.set_token(token_data["token"])

        # Step 3: Verify the token is valid asynchronously
        is_valid = await client.token.check_async(token_data["token"])
        assert is_valid is True

        # Step 4: Revoke the token asynchronously
        await client.token.revoke_async(token_data["token"])
