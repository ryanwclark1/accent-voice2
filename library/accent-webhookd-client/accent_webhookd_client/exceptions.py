# Copyright 2025 Accent Communications

"""Exception classes for the Webhookd client.

This module defines the custom exceptions used by the Webhookd client
for error handling and reporting.
"""

from __future__ import annotations

import logging

import httpx
from accent_lib_rest_client.exceptions import AccentAPIError

# Configure logging
logger = logging.getLogger(__name__)


class WebhookdError(AccentAPIError):
    """Base exception for Webhookd API errors.

    Attributes:
        status_code: HTTP status code
        message: Error message
        error_id: Error identifier
        details: Error details
        timestamp: Error timestamp

    """

    def __init__(self, response: httpx.Response) -> None:
        """Initialize from HTTP response.

        Args:
            response: The HTTP response containing error details

        Raises:
            InvalidWebhookdError: If the response doesn't contain valid error data

        """
        try:
            body = response.json()
        except ValueError:
            logger.error("Invalid JSON in error response")
            raise InvalidWebhookdError

        if not body:
            logger.error("Empty error response body")
            raise InvalidWebhookdError

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]
        except KeyError as e:
            logger.error("Missing required error field: %s", e)
            raise InvalidWebhookdError

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, status_code=self.status_code)


class WebhookdServiceUnavailable(WebhookdError):
    """Exception for service unavailable errors (503)."""

    pass  # noqa: PIE790


class InvalidWebhookdError(Exception):
    """Exception for invalid error responses from the Webhookd API."""

    pass  # noqa: PIE790
