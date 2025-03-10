# Copyright 2025 Accent Communications

"""Integration tests for asynchronous operations."""

import asyncio
from typing import Any, Dict, List

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.httpx_utils import configure_mock_responses


@pytest.mark.asyncio
async def test_multiple_concurrent_requests(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test making multiple concurrent requests.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses
    configure_mock_responses(httpx_mock, base_url)

    # Make multiple concurrent requests
    tasks = [
        client.users.list_async(),
        client.devices.list_async(),
        client.infos.get_async(),
        client.wizard.get_async(),
    ]

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Verify the results
    assert len(results) == 4

    # Check users
    assert "items" in results[0]
    assert len(results[0]["items"]) == 2

    # Check devices
    assert "items" in results[1]
    assert len(results[1]["items"]) == 2

    # Check info
    assert "api_version" in results[2]

    # Check wizard
    assert "configured" in results[3]


@pytest.mark.asyncio
async def test_error_handling_in_concurrent_requests(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test error handling in concurrent requests.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses - one successful, one error
    httpx_mock.add_response(
        method="GET", url=f"{base_url}/users", json={"items": [], "total": 0}
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/error",
        status_code=500,
        json={"message": "Internal server error"},
    )

    # Create tasks
    successful_task = client.users.list_async()
    error_task = client.async_client.get(f"{base_url}/error")

    # Run the successful task
    result = await successful_task
    assert "items" in result

    # Run the error task and expect an exception
    with pytest.raises(httpx.HTTPStatusError):
        response = await error_task
        response.raise_for_status()


@pytest.mark.asyncio
async def test_crud_operations_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test CRUD operations asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses for create
    new_user = {"firstname": "Test", "lastname": "User", "username": "testuser"}

    created_user = new_user.copy()
    created_user["uuid"] = "test-uuid"

    httpx_mock.add_response(
        method="POST", url=f"{base_url}/users", json=created_user, status_code=201
    )

    # Configure mock responses for get
    httpx_mock.add_response(
        method="GET", url=f"{base_url}/users/test-uuid", json=created_user
    )

    # Configure mock responses for update
    httpx_mock.add_response(
        method="PUT", url=f"{base_url}/users/test-uuid", status_code=204
    )

    # Configure mock responses for delete
    httpx_mock.add_response(
        method="DELETE", url=f"{base_url}/users/test-uuid", status_code=204
    )

    # Test create operation
    result_create = await client.users.create_async(new_user)
    assert result_create["uuid"] == "test-uuid"
    assert result_create["firstname"] == new_user["firstname"]

    # Test get operation
    result_get = await client.users.get_async("test-uuid")
    assert result_get["uuid"] == "test-uuid"
    assert result_get["firstname"] == new_user["firstname"]

    # Test update operation
    updated_user = created_user.copy()
    updated_user["firstname"] = "Updated"
    await client.users.update_async(updated_user)

    # Test delete operation
    await client.users.delete_async("test-uuid")
