# Copyright 2025 Accent Communications

"""Unit tests for custom exceptions."""

import json
from unittest.mock import Mock

import httpx
import pytest
from accent_lib_rest_client.exceptions import (
    AccentAPIError,
    AuthenticationError,
    InvalidArgumentError,
    ResourceNotFoundError,
    ServerError,
    handle_http_error,
)

HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_FORBIDDEN = 403
HTTP_BAD_REQUEST = 400
HTTP_SERVER_ERROR = 500

class TestExceptions:
    """Test cases for custom exceptions."""

    def test_accent_api_error(self) -> None:
        """Test AccentAPIError initialization."""
        error = AccentAPIError("Test error", status_code=400)
        assert str(error) == "Test error"
        assert error.status_code == 400
        assert error.message == "Test error"

    def test_invalid_argument_error(self) -> None:
        """Test InvalidArgumentError initialization."""
        error = InvalidArgumentError("test_arg")
        assert str(error) == 'Invalid value for argument "test_arg"'
        assert error.argument_name == "test_arg"

    def test_authentication_error(self) -> None:
        """Test AuthenticationError initialization."""
        # Default message
        error = AuthenticationError()
        assert str(error) == "Authentication failed"
        assert error.status_code == 401

        # Custom message
        error = AuthenticationError("Invalid token")
        assert str(error) == "Invalid token"
        assert error.status_code == 401

    def test_resource_not_found_error(self) -> None:
        """Test ResourceNotFoundError initialization."""
        error = ResourceNotFoundError("user/123")
        assert str(error) == "Resource not found: user/123"
        assert error.status_code == 404
        assert error.resource == "user/123"

    def test_server_error(self) -> None:
        """Test ServerError initialization."""
        # Default message
        error = ServerError()
        assert str(error) == "Server error occurred"
        assert error.status_code == 500

        # Custom message
        error = ServerError("Database connection failed")
        assert str(error) == "Database connection failed"
        assert error.status_code == 500

    def test_handle_http_error_401(self) -> None:
        """Test handling of 401 HTTP errors."""
        response = Mock(spec=httpx.Response)
        response.status_code = 401
        response.json.return_value = {"message": "Authentication failed"}

        error = httpx.HTTPStatusError("HTTP Error", request=Mock(), response=response)

        with pytest.raises(AuthenticationError) as excinfo:
            handle_http_error(error)

        assert str(excinfo.value) == "Authentication failed"
        assert excinfo.value.status_code == 401

    def test_handle_http_error_404(self) -> None:
        """Test handling of 404 HTTP errors."""
        response = Mock(spec=httpx.Response)
        response.status_code = 404
        response.json.return_value = {"message": "Resource not found"}

        error = httpx.HTTPStatusError("HTTP Error", request=Mock(), response=response)

        with pytest.raises(ResourceNotFoundError) as excinfo:
            handle_http_error(error)

        # The ResourceNotFoundError format is "Resource not found: {message}"
        assert "Resource not found" in str(excinfo.value)

    def test_handle_http_error_500(self) -> None:
        """Test handling of 500 HTTP errors."""
        response = Mock(spec=httpx.Response)
        response.status_code = 500
        response.json.return_value = {"message": "Internal server error"}

        error = httpx.HTTPStatusError("HTTP Error", request=Mock(), response=response)

        with pytest.raises(ServerError) as excinfo:
            handle_http_error(error)

        assert str(excinfo.value) == "Internal server error"
        assert excinfo.value.status_code == 500

    def test_handle_http_error_other(self) -> None:
        """Test handling of other HTTP errors."""
        response = Mock(spec=httpx.Response)
        response.status_code = 403
        response.json.return_value = {"message": "Forbidden"}

        error = httpx.HTTPStatusError("HTTP Error", request=Mock(), response=response)

        with pytest.raises(AccentAPIError) as excinfo:
            handle_http_error(error)

        assert str(excinfo.value) == "Forbidden"
        assert excinfo.value.status_code == 403

    def test_handle_http_error_invalid_json(self) -> None:
        """Test handling of HTTP errors with invalid JSON response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 400
        response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        error = httpx.HTTPStatusError("Bad request", request=Mock(), response=response)

        with pytest.raises(AccentAPIError) as excinfo:
            handle_http_error(error)

        assert "Bad request" in str(excinfo.value)
        assert excinfo.value.status_code == 400
