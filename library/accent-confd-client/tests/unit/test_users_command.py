# Copyright 2025 Accent Communications

"""Tests for the Users command."""

from typing import Any, Dict, List

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.responses import create_paginated_response, sample_users


def test_list_users(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test listing users.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/users",
        json=create_paginated_response(sample_users),
    )

    # Call the API
    result = client.users.list()

    # Verify the result
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["uuid"] == "user1-uuid"
    assert result["items"][1]["uuid"] == "user2-uuid"


@pytest.mark.asyncio
async def test_list_users_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test listing users asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/users",
        json=create_paginated_response(sample_users),
    )

    # Call the API asynchronously
    result = await client.users.list_async()

    # Verify the result
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["uuid"] == "user1-uuid"
    assert result["items"][1]["uuid"] == "user2-uuid"


def test_get_user(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test getting a user by ID.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET", url=f"{base_url}/users/user1-uuid", json=sample_users[0]
    )

    # Call the API
    result = client.users.get("user1-uuid")

    # Verify the result
    assert result["uuid"] == "user1-uuid"
    assert result["firstname"] == "John"
    assert result["lastname"] == "Doe"
    assert result["username"] == "johndoe"
    assert result["enabled"] is True


def test_create_user(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test creating a user.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define user data
    new_user = {
        "firstname": "Alice",
        "lastname": "Johnson",
        "username": "alicejohnson",
        "enabled": True,
    }

    # Configure mock response
    created_user = new_user.copy()
    created_user["uuid"] = "user3-uuid"

    httpx_mock.add_response(
        method="POST", url=f"{base_url}/users", json=created_user, status_code=201
    )

    # Call the API
    result = client.users.create(new_user)

    # Verify the result
    assert result["uuid"] == "user3-uuid"
    assert result["firstname"] == new_user["firstname"]
    assert result["lastname"] == new_user["lastname"]
    assert result["username"] == new_user["username"]
    assert result["enabled"] is True

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert request.json() == new_user


def test_update_user(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test updating a user.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define update data
    update_data = sample_users[0].copy()
    update_data["firstname"] = "Updated John"

    # Configure mock response
    httpx_mock.add_response(
        method="PUT", url=f"{base_url}/users/user1-uuid", status_code=204
    )

    # Call the API
    client.users.update(update_data)

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "PUT"
    assert request.url == f"{base_url}/users/user1-uuid"

    # Check that links are stripped from the request
    request_json = request.json()
    assert "links" not in request_json
    assert request_json["firstname"] == "Updated John"


def test_delete_user(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test deleting a user.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="DELETE", url=f"{base_url}/users/user1-uuid", status_code=204
    )

    # Call the API
    client.users.delete("user1-uuid")

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "DELETE"
    assert request.url == f"{base_url}/users/user1-uuid"


def test_import_csv(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test importing users from CSV.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define CSV data
    csv_data = b"firstname,lastname,username\nJohn,Doe,johndoe\nJane,Smith,janesmith"

    # Configure mock response
    import_result = {
        "created": ["user1-uuid", "user2-uuid"],
        "updated": [],
        "errors": [],
    }

    httpx_mock.add_response(
        method="POST",
        url=f"{base_url}/users/import",
        json=import_result,
        status_code=200,
    )

    # Call the API
    result = client.users.import_csv(csv_data)

    # Verify the result
    assert "created" in result
    assert len(result["created"]) == 2
    assert result["created"][0] == "user1-uuid"
    assert result["created"][1] == "user2-uuid"

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert request.url == f"{base_url}/users/import"
    assert request.content == csv_data
    assert request.headers["Content-Type"] == "text/csv; charset=utf-8"


@pytest.mark.asyncio
async def test_import_csv_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test importing users from CSV asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define CSV data
    csv_data = b"firstname,lastname,username\nJohn,Doe,johndoe\nJane,Smith,janesmith"

    # Configure mock response
    import_result = {
        "created": ["user1-uuid", "user2-uuid"],
        "updated": [],
        "errors": [],
    }

    httpx_mock.add_response(
        method="POST",
        url=f"{base_url}/users/import",
        json=import_result,
        status_code=200,
    )

    # Call the API asynchronously
    result = await client.users.import_csv_async(csv_data)

    # Verify the result
    assert "created" in result
    assert len(result["created"]) == 2
    assert result["created"][0] == "user1-uuid"
    assert result["created"][1] == "user2-uuid"


def test_export_csv(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test exporting users to CSV.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define CSV data
    csv_data = b"firstname,lastname,username\nJohn,Doe,johndoe\nJane,Smith,janesmith"

    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/users/export",
        content=csv_data,
        headers={"Content-Type": "text/csv; charset=utf-8"},
    )

    # Call the API
    result = client.users.export_csv()

    # Verify the result
    assert result == csv_data

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert request.url == f"{base_url}/users/export"
    assert request.headers["Accept"] == "text/csv; charset=utf-8"


def test_exist(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test checking if a user exists.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses
    httpx_mock.add_response(
        method="HEAD", url=f"{base_url}/users/user1-uuid", status_code=200
    )

    httpx_mock.add_response(
        method="HEAD", url=f"{base_url}/users/nonexistent", status_code=404
    )

    # Test existing user
    assert client.users.exist("user1-uuid") is True

    # Test non-existent user
    assert client.users.exist("nonexistent") is False
