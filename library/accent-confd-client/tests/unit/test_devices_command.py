# Copyright 2025 Accent Communications

"""Tests for the Devices command."""

from typing import Any, Dict

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.responses import create_paginated_response, sample_devices


def test_list_devices(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test listing devices.
    
    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/devices",
        json=create_paginated_response(sample_devices)
    )

    # Call the API
    result = client.devices.list()

    # Verify the result
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["id"] == "dev1-id"
    assert result["items"][1]["id"] == "dev2-id"


@pytest.mark.asyncio
async def test_list_devices_async(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test listing devices asynchronously.
    
    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/devices",
        json=create_paginated_response(sample_devices)
    )

    # Call the API asynchronously
    result = await client.devices.list_async()

    # Verify the result
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["id"] == "dev1-id"
    assert result["items"][1]["id"] == "dev2-id"


def test_get_device(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test getting a device by ID.
    
    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/devices/dev1-id",
        json=sample_devices[0]
    )

    # Call the API
    result = client.devices.get("dev1-id")

    # Verify the result
    assert result["id"] == "dev1-id"
    assert result["mac"] == "00:11:22:33:44:55"
    assert result["vendor"] == "Acme"


def test_create_device(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test creating a device.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define device data
    new_device = {
        "mac": "CC:DD:EE:FF:00:11",
        "template_id": "template3",
        "vendor": "Acme",
        "model": "Phone X3"
    }

    # Configure mock response
    created_device = new_device.copy()
    created_device["id"] = "dev3-id"

    httpx_mock.add_response(
        method="POST",
        url=f"{base_url}/devices",
        json=created_device,
        status_code=201
    )

    # Call the API
    result = client.devices.create(new_device)

    # Verify the result
    assert result["id"] == "dev3-id"
    assert result["mac"] == new_device["mac"]
    assert result["vendor"] == new_device["vendor"]

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert request.json() == new_device


def test_update_device(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test updating a device.
    
    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define update data
    update_data = sample_devices[0].copy()
    update_data["vendor"] = "Updated Vendor"

    # Configure mock response
    httpx_mock.add_response(
        method="PUT",
        url=f"{base_url}/devices/dev1-id",
        status_code=204
    )

    # Call the API
    client.devices.update(update_data)

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "PUT"
    assert request.url == f"{base_url}/devices/dev1-id"

    # Check that links are stripped from the request
    request_json = request.json()
    assert "links" not in request_json
    assert request_json["vendor"] == "Updated Vendor"


def test_delete_device(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test deleting a device.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="DELETE",
        url=f"{base_url}/devices/dev1-id",
        status_code=204
    )

    # Call the API
    client.devices.delete("dev1-id")

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "DELETE"
    assert request.url == f"{base_url}/devices/dev1-id"


def test_autoprov_device(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test auto-provisioning a device.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/devices/dev1-id/autoprov",
        status_code=204
    )

    # Call the API
    client.devices.autoprov("dev1-id")

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert request.url == f"{base_url}/devices/dev1-id/autoprov"


@pytest.mark.asyncio
async def test_autoprov_device_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test auto-provisioning a device asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET", url=f"{base_url}/devices/dev1-id/autoprov", status_code=204
    )

    # Call the API asynchronously
    await client.devices.autoprov_async("dev1-id")

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert request.url == f"{base_url}/devices/dev1-id/autoprov"


def test_synchronize_device(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test synchronizing a device.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET", url=f"{base_url}/devices/dev1-id/synchronize", status_code=204
    )

    # Call the API
    client.devices.synchronize("dev1-id")

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert request.url == f"{base_url}/devices/dev1-id/synchronize"


@pytest.mark.asyncio
async def test_synchronize_device_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test synchronizing a device asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET", url=f"{base_url}/devices/dev1-id/synchronize", status_code=204
    )

    # Call the API asynchronously
    await client.devices.synchronize_async("dev1-id")

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert request.url == f"{base_url}/devices/dev1-id/synchronize"


def test_device_relation(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test device relations.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response for listing lines
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/devices/dev1-id/lines",
        json={"items": [{"id": "line1"}, {"id": "line2"}], "total": 2},
    )

    # Test getting device relation
    device_relation = client.devices.relations("dev1-id")
    assert device_relation is not None

    # Test listing lines
    lines = device_relation.list_lines()
    assert "items" in lines
    assert len(lines["items"]) == 2

    # Configure mock responses for line operations
    httpx_mock.add_response(
        method="PUT", url=f"{base_url}/lines/line3/devices/dev1-id", status_code=204
    )

    httpx_mock.add_response(
        method="DELETE", url=f"{base_url}/lines/line3/devices/dev1-id", status_code=204
    )

    # Test adding a line
    device_relation.add_line("line3")
    request = httpx_mock.get_request(0)
    assert request.method == "PUT"
    assert request.url == f"{base_url}/lines/line3/devices/dev1-id"

    # Test removing a line
    device_relation.remove_line("line3")
    request = httpx_mock.get_request(1)
    assert request.method == "DELETE"
    assert request.url == f"{base_url}/lines/line3/devices/dev1-id"
