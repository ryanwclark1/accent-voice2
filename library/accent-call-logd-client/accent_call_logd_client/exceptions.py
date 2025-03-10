# Copyright 2025 Accent Communications

"""Exceptions for the accent-call-logd-client library."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)


class InvalidCallLogdError(Exception):
    """Raised when response doesn't match the expected Call Log daemon error format."""



class CallLogdError(httpx.HTTPStatusError):
    """Base exception for Call Log daemon API errors."""

    def __init__(self, response: httpx.Response) -> None:
        """Initialize from an HTTP response.

        Args:
            response: The HTTP response that triggered the error

        Raises:
            InvalidCallLogdError: If the response doesn't contain valid error data

        """
        try:
            body = response.json()
        except ValueError:
            logger.error("Invalid JSON in error response: %s", response.text)
            raise InvalidCallLogdError

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]
        except KeyError as e:
            logger.error("Missing required error field: %s", e)
            raise InvalidCallLogdError

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, request=response.request, response=response)


class CallLogdServiceUnavailable(CallLogdError):
    """Raised when the Call Log daemon service is unavailable."""

    pass  # noqa: PIE790

