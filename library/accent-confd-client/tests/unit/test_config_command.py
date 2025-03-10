# Copyright 2025 Accent Communications

"""Tests for the Configuration command."""

from typing import Any, Dict

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.responses import sample_configuration


def test_get_live_reload(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test getting live reload configuration.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/configuration/live_reload",
        json=sample_configuration["live_reload"],
    )

    # Call the API
    result = client.configuration.live_reload.get()

    # Verify the result
    assert isinstance(result, dict)
    assert result["enabled"] is True
    assert result["interval"] == 60


@pytest.mark.asyncio
async def test_get_live_reload_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test getting live reload configuration asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/configuration/live_reload",
        json=sample_configuration["live_reload"],
    )

    # Call the API asynchronously
    result = await client.configuration.live_reload.get_async()

    # Verify the result
    assert isinstance(result, dict)
    assert result["enabled"] is True
    assert result["interval"] == 60


def test_update_live_reload(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test updating live reload configuration.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define update data
    update_data = {"enabled": False, "interval": 120}

    # Configure mock response
    httpx_mock.add_response(
        method="PUT", url=f"{base_url}/configuration/live_reload", status_code=204
    )

    # Call the API
    client.configuration.live_reload.update(update_data)

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "PUT"
    assert request.url == f"{base_url}/configuration/live_reload"
    assert request.json() == update_data


@pytest.mark.asyncio
async def test_update_live_reload_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test updating live reload configuration asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define update data
    update_data = {"enabled": False, "interval": 120}

    # Configure mock response
    httpx_mock.add_response(
        method="PUT", url=f"{base_url}/configuration/live_reload", status_code=204
    )

    # Call the API asynchronously
    await client.configuration.live_reload.update_async(update_data)

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "PUT"
    assert request.url == f"{base_url}/configuration/live_reload"
    assert request.json() == update_data


def test_get_live_reload_error(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test error handling for getting live reload configuration.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock error response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/configuration/live_reload",
        status_code=500,
        json={"message": "Internal server error"},
    )

    # Call the API and expect an error
    with pytest.raises(httpx.HTTPStatusError):
        client.configuration.live_reload.get()
