# Copyright 2025 Accent Communications

"""Exception classes for the Calld API client.

This module defines custom exceptions for handling Calld API errors.
"""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)


class CalldError(httpx.HTTPStatusError):
    """Exception for Calld API errors.

    Attributes:
        status_code: HTTP status code
        message: Error message
        error_id: Error identifier
        details: Additional error details
        timestamp: When the error occurred

    """

    def __init__(self, response: httpx.Response) -> None:
        """Initialize the error from an HTTP response.

        Args:
            response: The HTTP response that triggered the error

        Raises:
            InvalidCalldError: If the response does not contain valid error data

        """
        try:
            body = response.json()
        except ValueError:
            raise InvalidCalldError

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]
        except KeyError:
            raise InvalidCalldError

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, request=response.request, response=response)


class InvalidCalldError(Exception):
    """Exception raised when a response cannot be parsed as a valid Calld error."""

