# Copyright 2025 Accent Communications

"""Integration tests for accent-lib-rest-client with a mock server."""

import httpx
import pytest
from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.command import RESTCommand
from accent_lib_rest_client.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ServerError,
    handle_http_error,
)


# Implementation class, not a test class
class TestCommandImpl(RESTCommand):
    """Test command implementation for integration tests."""

    resource = "test"

    def get_data(self) -> dict:
        """Get test data."""
        response = self.sync_client.get(f"{self.base_url}/data")
        response.raise_for_status()
        return response.json()

    async def get_data_async(self) -> dict:
        """Get test data asynchronously."""
        response = await self.async_client.get(f"{self.base_url}/data")
        response.raise_for_status()
        return response.json()

    def create_item(self, data: dict) -> dict:
        """Create a new item."""
        response = self.sync_client.post(f"{self.base_url}/create", json=data)
        response.raise_for_status()
        return response.json()

    async def create_item_async(self, data: dict) -> dict:
        """Create a new item asynchronously."""
        response = await self.async_client.post(f"{self.base_url}/create", json=data)
        response.raise_for_status()
        return response.json()


# Implementation class, not a test class
class TestClientImpl(BaseClient):
    """Test client implementation for integration tests."""

    namespace = "test_client.commands"
    test: TestCommandImpl  # This would be populated by stevedore in real usage


class TestLiveRequests:
    """Integration tests with a mock server."""

    @pytest.fixture
    def client(self, mock_server) -> TestClientImpl:
        """Create a TestClient connected to the mock server."""
        client = TestClientImpl(
            host="127.0.0.1",
            port=8000,
            version="v1",
            https=False,
        )
        # Manually add the command since we're not using stevedore
        client.test = TestCommandImpl(client)
        return client

    def test_get_data(self, client: TestClientImpl) -> None:
        """Test getting data from the server."""
        result = client.test.get_data()
        assert result["status"] == "success"
        assert "data" in result
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_get_data_async(self, client: TestClientImpl) -> None:
        """Test getting data from the server asynchronously."""
        result = await client.test.get_data_async()
        assert result["status"] == "success"
        assert "data" in result
        assert "timestamp" in result

    def test_create_item(self, client: TestClientImpl) -> None:
        """Test creating an item on the server."""
        test_data = {"name": "Test Item", "value": 42}
        result = client.test.create_item(test_data)

        assert result["status"] == "created"
        assert result["id"] == "new-item"
        assert result["data"] == test_data
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_create_item_async(self, client: TestClientImpl) -> None:
        """Test creating an item on the server asynchronously."""
        test_data = {"name": "Test Item", "value": 42}
        result = await client.test.create_item_async(test_data)

        assert result["status"] == "created"
        assert result["id"] == "new-item"
        assert result["data"] == test_data
        assert "timestamp" in result

    def test_error_handling(self, client: TestClientImpl) -> None:
        """Test error handling with different status codes."""
        # 404 Not Found
        with pytest.raises(ResourceNotFoundError):
            try:
                response = client.sync_client.get("http://127.0.0.1:8000/v1/not-found")
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                handle_http_error(e)

        # 500 Server Error
        with pytest.raises(ServerError):
            try:
                response = client.sync_client.get("http://127.0.0.1:8000/v1/error")
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                handle_http_error(e)

    def test_url_building(self, client: TestClientImpl) -> None:
        """Test URL building with the client."""
        assert client.url() == "http://127.0.0.1:8000/v1"
        assert client.url("test") == "http://127.0.0.1:8000/v1/test"
        assert client.url("test", "data") == "http://127.0.0.1:8000/v1/test/data"

    def test_server_reachable(self, client: TestClientImpl) -> None:
        """Test server reachability check."""
        assert client.is_server_reachable() is True

        # Test with an unreachable server
        unreachable_client = TestClientImpl(
            host="invalid-host",
            port=9999,
            https=False,
        )
        assert unreachable_client.is_server_reachable() is False
