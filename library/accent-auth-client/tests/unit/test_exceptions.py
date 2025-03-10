# Copyright 2025 Accent Communications

import pytest
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client.exceptions import (
    InvalidTokenException,
    MissingPermissionsTokenException,
)
from accent_lib_rest_client.exceptions import (
    AccentAPIError,
    AuthenticationError,
    InvalidArgumentError,
    ResourceNotFoundError,
    ServerError,
    handle_http_error,
)


class TestExceptions:
    """Test exception handling."""

    def test_invalid_token_exception(self):
        """Test InvalidTokenException."""
        exception = InvalidTokenException()
        assert str(exception) == "Invalid or missing token"

        exception = InvalidTokenException("Custom message")
        assert str(exception) == "Custom message"

    def test_missing_permissions_exception(self):
        """Test MissingPermissionsTokenException."""
        exception = MissingPermissionsTokenException()
        assert str(exception) == "Token lacks required permissions"

        exception = MissingPermissionsTokenException("Custom message")
        assert str(exception) == "Custom message"

    def test_handle_http_error_authentication(self):
        """Test handling of 401 authentication errors."""
        # Create mock response with 401 status
        response = MagicMock()
        response.status_code = 401
        response.json.return_value = {"message": "Authentication failed"}

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Authentication failed", request=MagicMock(), response=response
        )

        # Test exception handling
        with pytest.raises(AuthenticationError) as exc_info:
            handle_http_error(error)

        assert exc_info.value.status_code == 401
        assert str(exc_info.value) == "Authentication failed"

    def test_handle_http_error_not_found(self):
        """Test handling of 404 not found errors."""
        # Create mock response with 404 status
        response = MagicMock()
        response.status_code = 404
        response.json.return_value = {"message": "Resource not found"}

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Resource not found", request=MagicMock(), response=response
        )

        # Test exception handling
        with pytest.raises(ResourceNotFoundError) as exc_info:
            handle_http_error(error)

        assert exc_info.value.status_code == 404
        assert "Resource not found" in str(exc_info.value)

    def test_handle_http_error_server_error(self):
        """Test handling of 500 server errors."""
        # Create mock response with 500 status
        response = MagicMock()
        response.status_code = 500
        response.json.return_value = {"message": "Internal server error"}

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Internal server error", request=MagicMock(), response=response
        )

        # Test exception handling
        with pytest.raises(ServerError) as exc_info:
            handle_http_error(error)

        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value)

    def test_handle_http_error_json_decode_error(self):
        """Test handling of errors with invalid JSON responses."""
        # Create mock response with error status
        response = MagicMock()
        response.status_code = 400
        response.json.side_effect = ValueError("Invalid JSON")

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Bad request", request=MagicMock(), response=response
        )

        # Test exception handling
        with pytest.raises(AccentAPIError) as exc_info:
            handle_http_error(error)

        assert exc_info.value.status_code == 400
        assert "Bad request" in str(exc_info.value)
