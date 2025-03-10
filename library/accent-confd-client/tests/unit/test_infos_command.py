# Copyright 2025 Accent Communications

"""Tests for the Infos command."""

from typing import Any, Dict

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.responses import sample_info


def test_get_infos(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test getting system information.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/infos", json=sample_info)

    # Call the API
    result = client.infos.get()

    # Verify the result
    assert result["api_version"] == "1.1"
    assert result["accent_version"] == "5.0.0"
    assert result["accent_codename"] == "Mercury"
    assert result["accent_status"] == "production"


@pytest.mark.asyncio
async def test_get_infos_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test getting system information asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/infos", json=sample_info)

    # Call the API asynchronously
    result = await client.infos.get_async()

    # Verify the result
    assert result["api_version"] == "1.1"
    assert result["accent_version"] == "5.0.0"
    assert result["accent_codename"] == "Mercury"
    assert result["accent_status"] == "production"


def test_call_method(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test calling the infos command as a function.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/infos", json=sample_info)

    # Call the API as a function
    result = client.infos()

    # Verify the result
    assert result["api_version"] == "1.1"
    assert result["accent_version"] == "5.0.0"


@pytest.mark.asyncio
async def test_call_method_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test calling the infos command as a function asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/infos", json=sample_info)

    # Call the API as a function asynchronously
    result = await client.infos.__call_async__()

    # Verify the result
    assert result["api_version"] == "1.1"
    assert result["accent_version"] == "5.0.0"


def test_get_infos_error(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test error handling when getting system information.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock error response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/infos",
        status_code=500,
        json={"message": "Internal server error"},
    )

    # Call the API and expect an error
    with pytest.raises(httpx.HTTPStatusError):
        client.infos.get()
