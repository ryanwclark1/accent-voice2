# Copyright 2025 Accent Communications

"""Exception classes for the Setupd client."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)


class InvalidSetupdError(Exception):
    """Raised when a response cannot be parsed as a valid Setupd error."""

    pass  # noqa: PIE790


class SetupdError(httpx.HTTPStatusError):
    """Base exception for Setupd API errors."""

    def __init__(self, response: httpx.Response) -> None:
        """Initialize the exception from an HTTP response.

        Args:
            response: The HTTP response

        Raises:
            InvalidSetupdError: If the response is not a valid Setupd error

        """
        try:
            body = response.json()
        except ValueError:
            logger.error("Invalid JSON in error response")
            raise InvalidSetupdError

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]
        except KeyError as e:
            logger.error("Missing required error field: %s", e)
            raise InvalidSetupdError

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, request=response.request, response=response)


class SetupdServiceUnavailable(SetupdError):
    """Raised when the Setupd service is unavailable."""

    pass  # noqa: PIE790


class SetupdSetupError(SetupdError):
    """Raised when a setup operation fails."""

    pass  # noqa: PIE790
