# Copyright 2025 Accent Communications

"""Exception classes for the Directory Service API."""

import logging

import httpx

logger = logging.getLogger(__name__)


class InvalidDirdError(Exception):
    """Raised when a response doesn't match expected format."""

    pass  # noqa: PIE790


class DirdError(httpx.HTTPStatusError):
    """Base exception for all directory service errors."""

    def __init__(self, response: httpx.Response) -> None:
        """Initialize from an HTTP response.

        Args:
            response: The HTTP response

        Raises:
            InvalidDirdError: If response is not in expected format

        """
        try:
            body = response.json()
        except ValueError:
            raise InvalidDirdError

        if not body:
            raise InvalidDirdError

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]

        except KeyError:
            raise InvalidDirdError

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, request=response.request, response=response)


class DirdServiceUnavailable(DirdError):
    """Raised when the directory service is unavailable."""

    pass  # noqa: PIE790
