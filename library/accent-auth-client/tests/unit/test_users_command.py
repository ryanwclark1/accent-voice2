# Copyright 2025 Accent Communications

import pytest
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client.commands.users import UsersCommand


class TestUsersCommand:
    """Test the UsersCommand class."""

    def test_list(self, auth_client, mock_httpx_client):
        """Test listing users."""
        # Configure mock to return user list
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"uuid": "12345", "username": "user1"}],
            "total": 1,
        }
        mock_httpx_client.get.return_value = mock_response

        # Call the method
        result = auth_client.users.list(search="user")

        # Verify correct endpoint and parameters
        mock_httpx_client.get.assert_called_once()
        args, kwargs = mock_httpx_client.get.call_args
        assert args[0].endswith("/users")
        assert kwargs.get("params", {}).get("search") == "user"

        # Verify correct data is returned
        assert result == {"items": [{"uuid": "12345", "username": "user1"}], "total": 1}

    @pytest.mark.asyncio
    async def test_list_async(self, auth_client, mock_httpx_async_client):
        """Test listing users asynchronously."""
        # Configure mock to return user list
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"uuid": "12345", "username": "user1"}],
            "total": 1,
        }

        async def mock_get(*args, **kwargs):
            return mock_response

        mock_httpx_async_client.get = mock_get

        # Call the method
        result = await auth_client.users.list_async(search="user")

        # Verify correct data is returned
        assert result == {"items": [{"uuid": "12345", "username": "user1"}], "total": 1}

    def test_get(self, auth_client, mock_httpx_client, test_user_uuid, user_data):
        """Test getting a specific user."""
        # Configure mock to return user data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = user_data
        mock_httpx_client.get.return_value = mock_response

        # Call the method
        result = auth_client.users.get(test_user_uuid)

        # Verify correct endpoint
        mock_httpx_client.get.assert_called_once()
        args, kwargs = mock_httpx_client.get.call_args
        assert f"/users/{test_user_uuid}" in args[0]

        # Verify correct data is returned
        assert result == user_data

    def test_new(self, auth_client, mock_httpx_client, user_data):
        """Test creating a new user."""
        # Configure mock to return user data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = user_data
        mock_httpx_client.post.return_value = mock_response

        # Call the method
        result = auth_client.users.new(
            username="testuser",
            firstname="Test",
            lastname="User",
            email="test@example.com",
        )

        # Verify correct endpoint and data
        mock_httpx_client.post.assert_called_once()
        args, kwargs = mock_httpx_client.post.call_args
        assert args[0].endswith("/users")
        assert kwargs["json"]["username"] == "testuser"
        assert kwargs["json"]["firstname"] == "Test"
        assert kwargs["json"]["lastname"] == "User"
        assert kwargs["json"]["email"] == "test@example.com"

        # Verify correct data is returned
        assert result == user_data

    def test_update_emails(self, auth_client, mock_httpx_client, test_user_uuid):
        """Test updating user emails."""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emails": [{"address": "new@example.com", "confirmed": False, "main": True}]
        }
        mock_httpx_client.put.return_value = mock_response

        # Call the method
        emails = ["new@example.com"]
        result = auth_client.users.update_emails(test_user_uuid, emails)

        # Verify correct endpoint and data
        mock_httpx_client.put.assert_called_once()
        args, kwargs = mock_httpx_client.put.call_args
        assert f"/users/{test_user_uuid}/emails" in args[0]
        assert kwargs["json"]["emails"] == emails

        # Verify correct data is returned
        assert result == {
            "emails": [{"address": "new@example.com", "confirmed": False, "main": True}]
        }

    def test_delete(self, auth_client, mock_httpx_client, test_user_uuid):
        """Test deleting a user."""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_httpx_client.delete.return_value = mock_response

        # Call the method
        auth_client.users.delete(test_user_uuid)

        # Verify correct endpoint
        mock_httpx_client.delete.assert_called_once()
        args, kwargs = mock_httpx_client.delete.call_args
        assert f"/users/{test_user_uuid}" in args[0]
