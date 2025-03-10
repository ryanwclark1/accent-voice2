# Copyright 2025 Accent Communications

"""Exception classes for the provisioning client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx

logger = logging.getLogger(__name__)


class ProvdError(Exception):
    """Base exception for provisioning errors.

    Attributes:
        message: Error message
        status_code: HTTP status code
        response: The HTTP response that caused the error

    """

    def __init__(
        self,
        message: str | Exception,
        *,
        response: httpx.Response | None = None,
        status_code: int | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message or original exception
            response: HTTP response that triggered the error
            status_code: HTTP status code

        """
        self.response = response
        self.status_code = status_code or getattr(response, "status_code", None)
        super().__init__(message)


class ProvdServiceUnavailable(ProvdError):
    """Exception raised when the provisioning service is unavailable."""

    def __init__(self, response: httpx.Response) -> None:
        """Initialize the exception.

        Args:
            response: HTTP response indicating service unavailability

        """
        super().__init__("Provisioning service unavailable", response=response)


class InvalidProvdError(ProvdError):
    """Exception raised for invalid provisioning operations."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message: Error message

        """
        super().__init__(message)
