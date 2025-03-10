# Copyright 2025 Accent Communications

"""Integration tests for CRUD operations."""

from typing import Any, Dict, List

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.httpx_utils import (
    add_create_response,
    add_delete_response,
    add_update_response,
    configure_mock_responses,
)
from tests.mocks.responses import sample_devices, sample_users


def test_users_crud_operations(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test CRUD operations on users.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses
    configure_mock_responses(httpx_mock, base_url)

    # Test list operation
    result_list = client.users.list()
    assert "items" in result_list
    assert len(result_list["items"]) == 2

    # Test get operation
    result_get = client.users.get("user1-uuid")
    assert result_get["uuid"] == "user1-uuid"
    assert result_get["firstname"] == "John"

    # Test create operation
    new_user = {"firstname": "Test", "lastname": "User", "username": "testuser"}

    created_user = new_user.copy()
    created_user["uuid"] = "test-uuid"

    add_create_response(httpx_mock, base_url, "users", created_user)

    result_create = client.users.create(new_user)
    assert result_create["uuid"] == "test-uuid"
    assert result_create["firstname"] == new_user["firstname"]

    # Test update operation
    updated_user = created_user.copy()
    updated_user["firstname"] = "Updated"

    add_update_response(httpx_mock, base_url, "users", "test-uuid")

    client.users.update(updated_user)

    # Test delete operation
    add_delete_response(httpx_mock, base_url, "users", "test-uuid")

    client.users.delete("test-uuid")


def test_devices_crud_operations(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test CRUD operations on devices.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses
    configure_mock_responses(httpx_mock, base_url)

    # Test list operation
    result_list = client.devices.list()
    assert "items" in result_list
    assert len(result_list["items"]) == 2

    # Test get operation
    result_get = client.devices.get("dev1-id")
    assert result_get["id"] == "dev1-id"
    assert result_get["mac"] == "00:11:22:33:44:55"

    # Test create operation
    new_device = {
        "mac": "CC:DD:EE:FF:00:11",
        "template_id": "template3",
        "vendor": "Acme",
        "model": "Phone X3",
    }

    created_device = new_device.copy()
    created_device["id"] = "dev3-id"

    add_create_response(httpx_mock, base_url, "devices", created_device)

    result_create = client.devices.create(new_device)
    assert result_create["id"] == "dev3-id"
    assert result_create["mac"] == new_device["mac"]

    # Test update operation
    updated_device = created_device.copy()
    updated_device["vendor"] = "Updated Vendor"

    add_update_response(httpx_mock, base_url, "devices", "dev3-id")

    client.devices.update(updated_device)

    # Test delete operation
    add_delete_response(httpx_mock, base_url, "devices", "dev3-id")

    client.devices.delete("dev3-id")


def test_error_handling(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test error handling in CRUD operations.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock error responses
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/users/nonexistent",
        status_code=404,
        json={"message": "Resource not found"},
    )

    httpx_mock.add_response(
        method="POST",
        url=f"{base_url}/users",
        status_code=400,
        json={"message": "Invalid data"},
    )

    httpx_mock.add_response(
        method="PUT",
        url=f"{base_url}/users/user1-uuid",
        status_code=400,
        json={"message": "Invalid data"},
    )

    httpx_mock.add_response(
        method="DELETE",
        url=f"{base_url}/users/user1-uuid",
        status_code=500,
        json={"message": "Internal server error"},
    )

    # Test get error
    with pytest.raises(httpx.HTTPStatusError) as excinfo:
        client.users.get("nonexistent")
    assert excinfo.value.response.status_code == 404

    # Test create error
    with pytest.raises(httpx.HTTPStatusError) as excinfo:
        client.users.create({"firstname": "Invalid"})
    assert excinfo.value.response.status_code == 400

    # Test update error
    with pytest.raises(httpx.HTTPStatusError) as excinfo:
        client.users.update({"uuid": "user1-uuid", "firstname": "Invalid"})
    assert excinfo.value.response.status_code == 400

    # Test delete error
    with pytest.raises(httpx.HTTPStatusError) as excinfo:
        client.users.delete("user1-uuid")
    assert excinfo.value.response.status_code == 500
