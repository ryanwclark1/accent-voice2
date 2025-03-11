# Copyright 2025 Accent Communications

"""Exceptions for the Accent Deployd client.

This module defines the exceptions specific to the Deployd client,
including error handling for API responses.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class DeploydError(httpx.HTTPStatusError):
    """Exception raised for Deployd API errors.

    Attributes:
        status_code: HTTP status code
        message: Error message
        error_id: Error identifier
        details: Additional error details
        timestamp: When the error occurred
        resource: Optional affected resource

    """

    def __init__(self, response: httpx.Response) -> None:
        """Initialize the exception from an HTTP response.

        Args:
            response: The HTTP response

        Raises:
            InvalidDeploydError: If the response is not a valid Deployd error

        """
        try:
            body: dict[str, Any] = response.json()
        except ValueError:
            raise InvalidDeploydError

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]
            self.resource = body.get("resource")
        except KeyError:
            raise InvalidDeploydError

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, request=response.request, response=response)

        logger.error(
            "Deployd error: %s (ID: %s, Status: %s)",
            self.message,
            self.error_id,
            self.status_code,
        )


class DeploydServiceUnavailable(DeploydError):
    """Exception raised when the Deployd service is unavailable."""

    def __init__(self, response: httpx.Response) -> None:
        """Initialize the service unavailable exception.

        Args:
            response: The HTTP response

        """
        super().__init__(response)
        logger.warning("Deployd service unavailable")


class InvalidDeploydError(Exception):
    """Exception raised when a response cannot be parsed as a Deployd error."""

    def __init__(self) -> None:
        """Initialize the invalid error exception."""
        super().__init__("Response does not contain valid Deployd error information")
        logger.warning("Received invalid Deployd error format")
