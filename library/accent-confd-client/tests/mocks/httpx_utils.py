# Copyright 2025 Accent Communications

"""Utilities for mocking httpx requests."""

from collections.abc import Callable
from typing import Any, Dict, List, Optional, Union

import httpx
from pytest_httpx import HTTPXMock


def configure_mock_responses(httpx_mock: HTTPXMock, base_url: str) -> None:
    """Configure common mock responses.

    Args:
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    from tests.mocks.responses import (
        sample_call_logs_csv,
        sample_configuration,
        sample_devices,
        sample_error_response,
        sample_funckeys,
        sample_info,
        sample_users,
        sample_wizard,
    )

    # Mock successful responses
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/users",
        json={"items": sample_users, "total": len(sample_users)},
    )

    httpx_mock.add_response(
        method="GET", url=f"{base_url}/users/user1-uuid", json=sample_users[0]
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/devices",
        json={"items": sample_devices, "total": len(sample_devices)},
    )

    httpx_mock.add_response(
        method="GET", url=f"{base_url}/devices/dev1-id", json=sample_devices[0]
    )

    httpx_mock.add_response(
        method="GET", url=f"{base_url}/funckeys/templates/1", json=sample_funckeys
    )

    httpx_mock.add_response(method="GET", url=f"{base_url}/infos", json=sample_info)

    httpx_mock.add_response(
        method="GET", url=f"{base_url}/status", json={"status": "ok"}
    )

    httpx_mock.add_response(method="GET", url=f"{base_url}/wizard", json=sample_wizard)

    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/call_logs",
        text=sample_call_logs_csv,
        headers={"Content-Type": "text/csv"},
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/configuration/live_reload",
        json=sample_configuration["live_reload"],
    )

    # Mock error responses
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/error",
        status_code=500,
        json=sample_error_response,
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/users/nonexistent",
        status_code=404,
        json={"message": "Resource not found"},
    )


def add_create_response(
    httpx_mock: HTTPXMock, base_url: str, resource: str, data: dict[str, Any]
) -> None:
    """Add a mock response for resource creation.

    Args:
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests
        resource: Resource path
        data: Response data

    """
    httpx_mock.add_response(
        method="POST", url=f"{base_url}/{resource}", json=data, status_code=201
    )


def add_update_response(
    httpx_mock: HTTPXMock, base_url: str, resource: str, resource_id: str
) -> None:
    """Add a mock response for resource update.

    Args:
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests
        resource: Resource path
        resource_id: Resource ID

    """
    httpx_mock.add_response(
        method="PUT", url=f"{base_url}/{resource}/{resource_id}", status_code=204
    )


def add_delete_response(
    httpx_mock: HTTPXMock, base_url: str, resource: str, resource_id: str
) -> None:
    """Add a mock response for resource deletion.

    Args:
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests
        resource: Resource path
        resource_id: Resource ID

    """
    httpx_mock.add_response(
        method="DELETE", url=f"{base_url}/{resource}/{resource_id}", status_code=204
    )
