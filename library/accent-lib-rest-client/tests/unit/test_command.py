# Copyright 2025 Accent Communications

"""Unit tests for the HTTPCommand and RESTCommand classes."""

import time
from typing import Any, cast
from unittest.mock import Mock, PropertyMock

import httpx
import pytest
from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.command import HTTPCommand, RESTCommand
from accent_lib_rest_client.exceptions import (
    AccentAPIError,
    AuthenticationError,
    ResourceNotFoundError,
    ServerError,
)
from accent_lib_rest_client.models import CommandResponse, JSONResponse
from pytest_mock import MockerFixture


class TestHTTPCommand:
    """Test cases for the HTTPCommand class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Return a mock client."""
        mock = Mock(spec=BaseClient)
        mock.sync_client = Mock(spec=httpx.Client)
        mock.async_client = Mock(spec=httpx.AsyncClient)
        return mock

    @pytest.fixture
    def command(self, mock_client: Mock) -> HTTPCommand:
        """Return an HTTPCommand instance with a mock client."""
        return HTTPCommand(mock_client)

    def test_init(self, command: HTTPCommand, mock_client: Mock) -> None:
        """Test command initialization."""
        assert command._client is mock_client

    def test_sync_client(self, command: HTTPCommand, mock_client: Mock) -> None:
        """Test sync_client property."""
        assert command.sync_client is mock_client.sync_client

    def test_async_client(self, command: HTTPCommand, mock_client: Mock) -> None:
        """Test async_client property."""
        assert command.async_client is mock_client.async_client

    def test_session_deprecated(self, command: HTTPCommand, mock_client: Mock) -> None:
        """Test that session property returns sync_client."""
        assert command.session is mock_client.sync_client

    def test_raise_from_response_success(self) -> None:
        """Test raise_from_response with a successful response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 200

        # This should not raise
        HTTPCommand.raise_from_response(response)
        response.raise_for_status.assert_called_once()

    def test_raise_from_response_error_with_message(self) -> None:
        """Test raise_from_response with an error response containing a message."""
        response = Mock(spec=httpx.Response)
        response.status_code = 400
        response.json.return_value = {"message": "Custom error message"}
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad request", request=Mock(), response=response
        )

        with pytest.raises(httpx.HTTPStatusError) as excinfo:
            HTTPCommand.raise_from_response(response)

        # Check that the custom message was used
        assert "Custom error message" in str(excinfo.value)

    def test_raise_from_response_error_without_message(self) -> None:
        """Test raise_from_response with an error response without a message."""
        response = Mock(spec=httpx.Response)
        response.status_code = 400
        response.json.side_effect = ValueError("Invalid JSON")
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad request", request=Mock(), response=response
        )

        with pytest.raises(httpx.HTTPStatusError) as excinfo:
            HTTPCommand.raise_from_response(response)

        # Check that the exception was raised correctly
        assert "Bad request" in str(excinfo.value)

    def test_process_response_success(self, command: HTTPCommand) -> None:
        """Test process_response with a successful response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.content = b'{"key": "value"}'
        response.headers = {"Content-Type": "application/json"}

        start_time = time.time() - 0.5  # 500ms ago
        result = command.process_response(response, start_time)

        assert isinstance(result, CommandResponse)
        assert result.status_code == 200
        assert result.content == b'{"key": "value"}'
        assert result.headers == {"Content-Type": "application/json"}
        assert result.response_time is not None
        assert 0.4 < result.response_time < 0.6  # Approximately 500ms

    def test_process_response_error(
        self, command: HTTPCommand, mocker: MockerFixture
    ) -> None:
        """Test process_response with an error response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 404
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not found", request=Mock(), response=response
        )

        mock_handle_error = mocker.patch(
            "accent_lib_rest_client.command.handle_http_error"
        )

        with pytest.raises(Exception):
            command.process_response(response)

        mock_handle_error.assert_called_once()

    def test_process_json_response_success(self, command: HTTPCommand) -> None:
        """Test process_json_response with a successful response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.json.return_value = {"key": "value"}
        response.headers = {"Content-Type": "application/json"}

        result = command.process_json_response(response)

        assert isinstance(result, JSONResponse)
        assert result.status_code == 200
        assert result.data == {"key": "value"}
        assert result.headers == {"Content-Type": "application/json"}

    def test_process_json_response_error(
        self, command: HTTPCommand, mocker: MockerFixture
    ) -> None:
        """Test process_json_response with an error response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 500
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=Mock(), response=response
        )

        mock_handle_error = mocker.patch(
            "accent_lib_rest_client.command.handle_http_error"
        )

        with pytest.raises(Exception):
            command.process_json_response(response)

        mock_handle_error.assert_called_once()


class TestRESTCommand:
    """Test cases for the RESTCommand class."""

    # Implementation class, not a test class
    class TestRESTImpl(RESTCommand):
        """Concrete implementation of RESTCommand for testing."""

        resource = "test-resource"

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Return a mock client."""
        mock = Mock(spec=BaseClient)
        mock.url.return_value = "https://example.com/v1/test-resource"

        # Mock the config property
        config_mock = Mock()
        config_mock.timeout = 10.0
        type(mock).config = PropertyMock(return_value=config_mock)

        mock.sync_client = Mock(spec=httpx.Client)
        mock.async_client = Mock(spec=httpx.AsyncClient)
        return mock

    @pytest.fixture
    def rest_command(self, mock_client: Mock) -> TestRESTImpl:
        """Return a RESTCommand instance with a mock client."""
        return self.TestRESTImpl(mock_client)

    def test_init(
        self, rest_command: TestRESTImpl, mock_client: Mock
    ) -> None:
        """Test REST command initialization."""
        assert rest_command._client is mock_client
        assert rest_command.base_url == "https://example.com/v1/test-resource"
        assert rest_command.timeout == 10.0
        mock_client.url.assert_called_once_with("test-resource")

    def test_get_headers_default(self, rest_command: TestRESTImpl) -> None:
        """Test default headers."""
        headers = rest_command._get_headers()
        assert headers == {"Accept": "application/json"}

    def test_get_headers_with_tenant(
        self, rest_command: TestRESTImpl
    ) -> None:
        """Test headers with tenant UUID."""
        headers = rest_command._get_headers(tenant_uuid="test-tenant")
        assert headers == {
            "Accept": "application/json",
            "Accent-Tenant": "test-tenant",
        }

    def test_get_headers_ignores_other_kwargs(
        self, rest_command: TestRESTImpl
    ) -> None:
        """Test that other kwargs are ignored in headers."""
        headers = rest_command._get_headers(
            tenant_uuid="test-tenant",
            other_param="value",
            another_param=123,
        )
        assert headers == {
            "Accept": "application/json",
            "Accent-Tenant": "test-tenant",
        }
