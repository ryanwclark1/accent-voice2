# Copyright 2025 Accent Communications

from __future__ import annotations

import json

import httpx
import structlog

logger = structlog.get_logger(__name__)


class AccentAPIError(Exception):
    """Base exception for all API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: Optional HTTP status code

        """
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class InvalidArgumentError(Exception):
    """Raised when an invalid argument is provided to the client."""

    def __init__(self, argument_name: str) -> None:
        """Initialize the exception.

        Args:
            argument_name: Name of the invalid argument

        """
        super().__init__(f'Invalid value for argument "{argument_name}"')
        self.argument_name = argument_name


class AuthenticationError(AccentAPIError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        """Initialize the exception.

        Args:
            message: Error message

        """
        super().__init__(message, status_code=401)


class ResourceNotFoundError(AccentAPIError):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str) -> None:
        """Initialize the exception.

        Args:
            resource: The requested resource name

        """
        super().__init__(f"Resource not found: {resource}", status_code=404)
        self.resource = resource


class ServerError(AccentAPIError):
    """Raised when the server encounters an error."""

    def __init__(self, message: str = "Server error occurred") -> None:
        """Initialize the exception.

        Args:
            message: Error message

        """
        super().__init__(message, status_code=500)


def handle_http_error(error: httpx.HTTPStatusError) -> None:
    """Handle HTTP errors by raising appropriate exceptions.

    Args:
        error: The HTTP error

    Raises:
        AuthenticationError: For 401 errors
        ResourceNotFoundError: For 404 errors
        ServerError: For 5xx errors
        AccentAPIError: For other errors

    """
    response = error.response
    status_code = response.status_code

    try:
        error_data = response.json()
        message = error_data.get("message", str(error))
    except (json.JSONDecodeError, ValueError):
        message = str(error)

    logger.error("http_error", status_code=status_code, message=message)

    if status_code == 401:
        raise AuthenticationError(message)
    if status_code == 404:
        raise ResourceNotFoundError(message)
    if 500 <= status_code < 600:
        raise ServerError(message)
    raise AccentAPIError(message, status_code=status_code)
