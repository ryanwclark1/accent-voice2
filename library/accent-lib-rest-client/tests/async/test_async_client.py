# Copyright 2025 Accent Communications

"""Async tests for accent-lib-rest-client."""

import asyncio
from typing import Any, AsyncGenerator, Dict

import httpx
import pytest
import pytest_asyncio
from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.command import RESTCommand
from accent_lib_rest_client.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ServerError,
    handle_http_error,
)


# We're extending the RESTCommand class for testing, not creating a test class
class AsyncTestCommandImpl(RESTCommand):
    """Test command implementation with async methods."""

    resource = "test"

    async def get_data(self) -> Dict[str, Any]:
        """Get test data asynchronously."""
        response = await self.async_client.get(f"{self.base_url}/data")
        response.raise_for_status()
        return response.json()

    async def create_item(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item asynchronously."""
        response = await self.async_client.post(f"{self.base_url}/create", json=data)
        response.raise_for_status()
        return response.json()


# We're extending the BaseClient class for testing, not creating a test class
class AsyncTestClientImpl(BaseClient):
    """Test client implementation for async tests."""

    namespace = "async_test_client.commands"
    test: AsyncTestCommandImpl


@pytest_asyncio.fixture
async def async_client(mock_server) -> AsyncGenerator[AsyncTestClientImpl, None]:
    """Create an AsyncTestClient connected to the mock server."""
    client = AsyncTestClientImpl(
        host="127.0.0.1",
        port=8000,
        version="v1",
        https=False,
    )
    # Manually add the command since we're not using stevedore
    client.test = AsyncTestCommandImpl(client)

    yield client

    # Close the client after the test
    await client._close_async_client()


class TestAsyncClient:
    """Async tests for the client."""

    @pytest.mark.asyncio
    async def test_async_client_creation(self) -> None:
        """Test async client creation."""
        # Use AsyncTestClientImpl instead of BaseClient to avoid namespace issues
        client = AsyncTestClientImpl(host="example.com")
        async_client = client.async_client

        assert isinstance(async_client, httpx.AsyncClient)
        assert async_client.headers["Connection"] == "close"

        # Clean up
        await client._close_async_client()

    @pytest.mark.asyncio
    async def test_is_server_reachable_async(
        self, async_client: AsyncTestClientImpl
    ) -> None:
        """Test async server reachability check."""
        assert await async_client.is_server_reachable_async() is True

        # Test with an unreachable server
        unreachable_client = AsyncTestClientImpl(
            host="invalid-host",
            port=9999,
            https=False,
        )
        assert await unreachable_client.is_server_reachable_async() is False

    @pytest.mark.asyncio
    async def test_get_data_async(self, async_client: AsyncTestClientImpl) -> None:
        """Test getting data asynchronously."""
        result = await async_client.test.get_data()

        assert result["status"] == "success"
        assert "data" in result
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_create_item_async(self, async_client: AsyncTestClientImpl) -> None:
        """Test creating an item asynchronously."""
        test_data = {"name": "Async Test", "value": 100}
        result = await async_client.test.create_item(test_data)

        assert result["status"] == "created"
        assert result["id"] == "new-item"
        assert result["data"] == test_data
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_error_handling_async(
        self, async_client: AsyncTestClientImpl
    ) -> None:
        """Test async error handling."""
        # Import inside the test to avoid circular imports
        import httpx

        # 404 Not Found
        with pytest.raises(ResourceNotFoundError):
            try:
                response = await async_client.async_client.get(
                    "http://127.0.0.1:8000/v1/not-found"
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                handle_http_error(e)

        # 500 Server Error
        with pytest.raises(ServerError):
            try:
                response = await async_client.async_client.get(
                    "http://127.0.0.1:8000/v1/error"
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                handle_http_error(e)

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, async_client: AsyncTestClientImpl) -> None:
        """Test running multiple async requests concurrently."""
        # Create tasks for multiple concurrent requests
        tasks = []

        # Add data fetching tasks
        tasks.append(async_client.test.get_data())
        tasks.append(async_client.test.get_data())

        # Add item creation tasks
        for i in range(5):
            tasks.append(
                async_client.test.create_item({"name": "Concurrent Test", "value": i})
            )

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Verify each result
        for i, result in enumerate(results):
            if i < 2:  # First two are get_data calls
                assert result["status"] == "success"
                assert "data" in result
            else:  # The rest are create_item calls
                assert result["status"] == "created"
                assert result["id"] == "new-item"
                assert result["data"]["name"] == "Concurrent Test"
