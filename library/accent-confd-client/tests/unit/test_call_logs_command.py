# Copyright 2025 Accent Communications

"""Tests for the CallLogs command."""

import datetime
from typing import Any, Dict

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.responses import sample_call_logs_csv


def test_list_call_logs(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test listing call logs.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/call_logs",
        text=sample_call_logs_csv,
        headers={"Content-Type": "text/csv"},
    )

    # Call the API
    result = client.call_logs.list()

    # Verify the result
    assert isinstance(result, str)
    assert "Call ID,Caller,Called" in result
    assert "123,1001,1002" in result


@pytest.mark.asyncio
async def test_list_call_logs_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test listing call logs asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/call_logs",
        text=sample_call_logs_csv,
        headers={"Content-Type": "text/csv"},
    )

    # Call the API asynchronously
    result = await client.call_logs.list_async()

    # Verify the result
    assert isinstance(result, str)
    assert "Call ID,Caller,Called" in result
    assert "123,1001,1002" in result


def test_list_call_logs_with_dates(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str, mock_datetime: datetime
) -> None:
    """Test listing call logs with date filters.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests
        mock_datetime: Mock datetime

    """
    # Define date range
    start_date = mock_datetime
    end_date = mock_datetime.replace(day=31)

    # Format expected dates according to command's format
    expected_start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    expected_end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")

    # Configure mock response with date parameters
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/call_logs",
        text=sample_call_logs_csv,
        headers={"Content-Type": "text/csv"},
        match_query_params={
            "start_date": expected_start_date,
            "end_date": expected_end_date,
        },
    )

    # Call the API with date filters
    result = client.call_logs.list(start_date=start_date, end_date=end_date)

    # Verify the result
    assert isinstance(result, str)
    assert "Call ID,Caller,Called" in result


def test_list_call_logs_error(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test error handling for listing call logs.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock error response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/call_logs",
        status_code=500,
        json={"message": "Internal server error"},
    )

    # Call the API and expect an error
    with pytest.raises(httpx.HTTPStatusError):
        client.call_logs.list()


def test_build_params(client: ConfdClient, mock_datetime: datetime) -> None:
    """Test building parameters for call logs.

    Args:
        client: Client instance
        mock_datetime: Mock datetime

    """
    # Test with no parameters
    params = client.call_logs.build_params()
    assert params == {}

    # Test with start date only
    params = client.call_logs.build_params(start_date=mock_datetime)
    assert "start_date" in params
    assert params["start_date"] == mock_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    # Test with end date only
    params = client.call_logs.build_params(end_date=mock_datetime)
    assert "end_date" in params
    assert params["end_date"] == mock_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    # Test with both dates
    params = client.call_logs.build_params(
        start_date=mock_datetime, end_date=mock_datetime.replace(day=31)
    )
    assert "start_date" in params
    assert "end_date" in params
    assert params["start_date"] == mock_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    assert params["end_date"] == mock_datetime.replace(day=31).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
