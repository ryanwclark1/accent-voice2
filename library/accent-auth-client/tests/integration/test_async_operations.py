# Copyright 2025 Accent Communications

import pytest
import asyncio
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client import Client


@pytest.mark.integration
class TestAsyncOperations:
    """Test async operation capabilities."""

    @pytest.fixture
    def async_client(self):
        """Create a client instance for async tests."""
        client = Client(host="test.example.com", port=443, version="0.1")

        # Override async client for test
        client._async_client = MagicMock(spec=httpx.AsyncClient)

        # Set up basic responses
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}

        async def mock_get(*args, **kwargs):
            return mock_response

        async def mock_post(*args, **kwargs):
            return mock_response

        async def mock_put(*args, **kwargs):
            return mock_response

        async def mock_delete(*args, **kwargs):
            response = MagicMock(spec=httpx.Response)
            response.status_code = 204
            return response

        client._async_client.get = mock_get
        client._async_client.post = mock_post
        client._async_client.put = mock_put
        client._async_client.delete = mock_delete

        return client

    @pytest.mark.asyncio
    async def test_parallel_operations(self, async_client):
        """Test executing multiple async operations in parallel."""
        # Configure responses for different endpoints
        user_data = {
            "uuid": "00000000-0000-4000-a000-000000000001",
            "username": "testuser",
        }

        group_data = {
            "uuid": "00000000-0000-4000-a000-000000000002",
            "name": "testgroup",
        }

        policy_data = {
            "uuid": "00000000-0000-4000-a000-000000000003",
            "name": "testpolicy",
        }

        # Override the mocked methods to return different data based on URL
        async def custom_get(*args, **kwargs):
            url = args[0]
            response = MagicMock(spec=httpx.Response)
            response.status_code = 200

            if "/users/" in url:
                response.json.return_value = user_data
            elif "/groups/" in url:
                response.json.return_value = group_data
            elif "/policies/" in url:
                response.json.return_value = policy_data
            else:
                response.json.return_value = {"status": "ok"}

            return response

        async_client._async_client.get = custom_get

        # Run multiple operations in parallel
        results = await asyncio.gather(
            async_client.users.get_async("00000000-0000-4000-a000-000000000001"),
            async_client.groups.get_async("00000000-0000-4000-a000-000000000002"),
            async_client.policies.get_async("00000000-0000-4000-a000-000000000003"),
        )

        # Verify results
        assert results[0] == user_data
        assert results[1] == group_data
        assert results[2] == policy_data

    @pytest.mark.asyncio
    async def test_error_handling_in_parallel(self, async_client):
        """Test error handling when executing parallel operations."""

        # Configure responses to include errors
        async def custom_get(*args, **kwargs):
            url = args[0]
            response = MagicMock(spec=httpx.Response)

            if "/users/" in url:
                response.status_code = 200
                response.json.return_value = {
                    "uuid": "00000000-0000-4000-a000-000000000001"
                }
            elif "/groups/" in url:
                response.status_code = 404
                response.json.return_value = {"message": "Group not found"}
                response.raise_for_status.side_effect = httpx.HTTPStatusError(
                    "Group not found", request=MagicMock(), response=response
                )
            else:
                response.status_code = 200
                response.json.return_value = {"status": "ok"}

            return response

        async_client._async_client.get = custom_get

        # Run operations with error handling
        user_data = None
        group_error = None

        try:
            user_data = await async_client.users.get_async(
                "00000000-0000-4000-a000-000000000001"
            )
        except Exception as e:
            pass

        try:
            await async_client.groups.get_async("00000000-0000-4000-a000-000000000002")
        except Exception as e:
            group_error = e

        # Verify results
        assert user_data is not None
        assert user_data["uuid"] == "00000000-0000-4000-a000-000000000001"
        assert group_error is not None