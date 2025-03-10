# Copyright 2025 Accent Communications

"""Exceptions for the AMID client.

This module defines the custom exceptions raised by the AMID client.
"""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)


class InvalidAmidError(Exception):
    """Raised when a response doesn't match expected AMID format."""


class AmidError(httpx.HTTPStatusError):
    """Base exception for all AMID API errors.

    This exception is raised when the AMID API returns an error response.
    """

    def __init__(self, response: httpx.Response) -> None:
        """Initialize with details from the response.

        Args:
            response: The HTTP response containing error details

        Raises:
            InvalidAmidError: If the response doesn't match expected AMID format

        """
        try:
            body = response.json()
        except ValueError:
            logger.exception("Failed to parse error response as JSON")
            raise InvalidAmidError from None

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]
            if "resource" in body:
                self.resource = body["resource"]
        except KeyError as e:
            logger.exception("Missing required field in error response: %s", e)
            raise InvalidAmidError from None

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, request=response.request, response=response)


class AmidServiceUnavailable(AmidError):
    """Raised when the AMID service is unavailable (503 error)."""


class AmidProtocolError(AmidError):
    """Raised when the AMID protocol returns an error in the response body."""

    def __init__(self, response: httpx.Response) -> None:
        """Initialize with details from the response.

        Args:
            response: The HTTP response containing error details

        Raises:
            InvalidAmidError: If the response doesn't match expected AMID format

        """
        try:
            body = response.json()
        except ValueError:
            logger.exception("Failed to parse error response as JSON")
            raise InvalidAmidError from None

        try:
            for msg in body:
                if isinstance(msg, dict) and "Message" in msg:
                    self.message = msg["Message"]
                    break
            else:
                raise KeyError("No 'Message' found in response")
        except (TypeError, KeyError) as e:
            logger.exception("Invalid error response format: %s", e)
            raise InvalidAmidError from None

        # Note: This is a modified version of the parent class init
        # since we need a custom message format
        self.status_code = response.status_code
        exception_message = f"{self.message}"
        super(httpx.HTTPStatusError, self).__init__(
            exception_message, request=response.request, response=response
        )
