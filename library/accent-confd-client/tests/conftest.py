# Copyright 2025 Accent Communications

"""Test fixtures for the Configuration Daemon client tests."""

import json
from datetime import datetime
from typing import Any, Dict

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock


@pytest.fixture
def client() -> ConfdClient:
    """Create a client instance for testing.

    Returns:
        Client instance

    """
    return ConfdClient("example.com", port=443, prefix="/api/confd", version="1.1")


@pytest.fixture
def base_url() -> str:
    """Get the base URL for API requests.

    Returns:
        Base URL

    """
    return "https://example.com:443/api/confd/1.1"


@pytest.fixture
def sample_items() -> dict[str, Any]:
    """Get sample items for testing.

    Returns:
        Sample items

    """
    return {
        "items": [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}],
        "total": 2,
    }


@pytest.fixture
def mock_datetime() -> datetime:
    """Get a mock datetime for testing.

    Returns:
        Mock datetime

    """
    return datetime(2025, 1, 1, 12, 0, 0)
