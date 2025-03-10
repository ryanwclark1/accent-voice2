# Copyright 2025 Accent Communications

"""Tests for the Wizard command."""

from typing import Any, Dict

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.responses import sample_wizard


def test_get_wizard(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test getting wizard configuration.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/wizard", json=sample_wizard)

    # Call the API
    result = client.wizard.get()

    # Verify the result
    assert result["configured"] is True
    assert "steps" in result
    assert result["steps"]["welcome"] is True
    assert result["steps"]["license"] is True
    assert result["steps"]["language"] is True
    assert result["steps"]["context"] is True
    assert result["steps"]["admin"] is True
    assert result["steps"]["entities"] is True


@pytest.mark.asyncio
async def test_get_wizard_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test getting wizard configuration asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/wizard", json=sample_wizard)

    # Call the API asynchronously
    result = await client.wizard.get_async()

    # Verify the result
    assert result["configured"] is True
    assert "steps" in result
    assert result["steps"]["welcome"] is True


def test_create_wizard(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test creating wizard configuration.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define wizard data
    wizard_data = {
        "admin_password": "secure-password",
        "language": "en_US",
        "timezone": "America/New_York",
        "context_internal": "default",
        "context_outcall": "outcall",
        "entity_name": "example",
    }

    # Configure mock response
    create_result = {
        "configured": True,
        "steps": {
            "welcome": True,
            "license": True,
            "language": True,
            "context": True,
            "admin": True,
            "entities": True,
        },
    }

    httpx_mock.add_response(
        method="POST", url=f"{base_url}/wizard", json=create_result, status_code=201
    )

    # Call the API
    result = client.wizard.create(wizard_data)

    # Verify the result
    assert result["configured"] is True
    assert "steps" in result
    assert result["steps"]["welcome"] is True

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert request.url == f"{base_url}/wizard"
    assert request.json() == wizard_data


@pytest.mark.asyncio
async def test_create_wizard_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test creating wizard configuration asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define wizard data
    wizard_data = {
        "admin_password": "secure-password",
        "language": "en_US",
        "timezone": "America/New_York",
        "context_internal": "default",
        "context_outcall": "outcall",
        "entity_name": "example",
    }

    # Configure mock response
    create_result = {
        "configured": True,
        "steps": {
            "welcome": True,
            "license": True,
            "language": True,
            "context": True,
            "admin": True,
            "entities": True,
        },
    }

    httpx_mock.add_response(
        method="POST", url=f"{base_url}/wizard", json=create_result, status_code=201
    )

    # Call the API asynchronously
    result = await client.wizard.create_async(wizard_data)

    # Verify the result
    assert result["configured"] is True
    assert "steps" in result
    assert result["steps"]["welcome"] is True

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert request.url == f"{base_url}/wizard"
    assert request.json() == wizard_data


def test_discover(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test discovering wizard configuration.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    discover_result = {
        "timezone": {
            "value": "America/New_York",
            "options": ["America/New_York", "Europe/Paris", "Asia/Tokyo"],
        },
        "language": {"value": "en_US", "options": ["en_US", "fr_FR", "es_ES"]},
        "domain": "example.com",
    }

    httpx_mock.add_response(
        method="GET", url=f"{base_url}/wizard/discover", json=discover_result
    )

    # Call the API
    result = client.wizard.discover()

    # Verify the result
    assert "timezone" in result
    assert "language" in result
    assert "domain" in result
    assert result["timezone"]["value"] == "America/New_York"
    assert result["language"]["value"] == "en_US"
    assert result["domain"] == "example.com"


@pytest.mark.asyncio
async def test_discover_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test discovering wizard configuration asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    discover_result = {
        "timezone": {
            "value": "America/New_York",
            "options": ["America/New_York", "Europe/Paris", "Asia/Tokyo"],
        },
        "language": {"value": "en_US", "options": ["en_US", "fr_FR", "es_ES"]},
        "domain": "example.com",
    }

    httpx_mock.add_response(
        method="GET", url=f"{base_url}/wizard/discover", json=discover_result
    )

    # Call the API asynchronously
    result = await client.wizard.discover_async()

    # Verify the result
    assert "timezone" in result
    assert "language" in result
    assert "domain" in result
    assert result["timezone"]["value"] == "America/New_York"
    assert result["language"]["value"] == "en_US"
    assert result["domain"] == "example.com"


def test_call_method(client: ConfdClient, httpx_mock: HTTPXMock, base_url: str) -> None:
    """Test calling the wizard command as a function.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/wizard", json=sample_wizard)

    # Call the API as a function
    result = client.wizard()

    # Verify the result
    assert result["configured"] is True
    assert "steps" in result
    assert result["steps"]["welcome"] is True


@pytest.mark.asyncio
async def test_call_method_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test calling the wizard command as a function asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(method="GET", url=f"{base_url}/wizard", json=sample_wizard)

    # Call the API as a function asynchronously
    result = await client.wizard.__call_async__()

    # Verify the result
    assert result["configured"] is True
    assert "steps" in result
    assert result["steps"]["welcome"] is True
