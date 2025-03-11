# Copyright 2025 Accent Communications
"""Exceptions for the Accent applicationd client.
"""

from __future__ import annotations

import logging
from typing import ClassVar

import httpx

logger = logging.getLogger(__name__)


class OpenApiException(Exception):
    """Base exception class for all OpenAPI exceptions."""


class ApiTypeError(OpenApiException, TypeError):
    """Type error in API usage."""

    def __init__(
        self,
        msg: str,
        path_to_item: list[str | int] | None = None,
        valid_classes: tuple[type, ...] | None = None,
        key_type: bool | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            msg: Exception message
            path_to_item: Path to the item causing the error
            valid_classes: Valid classes that the item should be
            key_type: Whether the item is a key in a mapping

        """
        self.path_to_item = path_to_item
        self.valid_classes = valid_classes
        self.key_type = key_type
        full_msg = msg
        if path_to_item:
            full_msg = f"{msg} at {render_path(path_to_item)}"
        super().__init__(full_msg)


class ApiValueError(OpenApiException, ValueError):
    """Value error in API usage."""

    def __init__(self, msg: str, path_to_item: list[str | int] | None = None) -> None:
        """Initialize the exception.

        Args:
            msg: Exception message
            path_to_item: Path to the item causing the error

        """
        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = f"{msg} at {render_path(path_to_item)}"
        super().__init__(full_msg)


class ApiAttributeError(OpenApiException, AttributeError):
    """Attribute error in API usage."""

    def __init__(self, msg: str, path_to_item: list[str | int] | None = None) -> None:
        """Initialize the exception.

        Args:
            msg: Exception message
            path_to_item: Path to the item causing the error

        """
        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = f"{msg} at {render_path(path_to_item)}"
        super().__init__(full_msg)


class ApiKeyError(OpenApiException, KeyError):
    """Key error in API usage."""

    def __init__(self, msg: str, path_to_item: list[str | int] | None = None) -> None:
        """Initialize the exception.

        Args:
            msg: Exception message
            path_to_item: Path to the item causing the error

        """
        self.path_to_item = path_to_item
        full_msg = msg
        if path_to_item:
            full_msg = f"{msg} at {render_path(path_to_item)}"
        super().__init__(full_msg)


class ApiException(OpenApiException):
    """Generic API exception."""

    def __init__(
        self,
        status: int | None = None,
        reason: str | None = None,
        http_resp: httpx.Response | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            status: HTTP status code
            reason: Reason phrase
            http_resp: HTTP response object

        """
        if http_resp:
            self.status = http_resp.status_code
            self.reason = http_resp.reason_phrase
            self.body = http_resp.content
            self.headers = http_resp.headers
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            Formatted error message

        """
        error_message = f"({self.status})\nReason: {self.reason}\n"

        if self.headers:
            error_message += f"HTTP response headers: {dict(self.headers)}\n"

        if self.body:
            error_message += f"HTTP response body: {self.body}\n"

        return error_message


class NotFoundException(ApiException):
    """Resource not found exception."""

    STATUS_CODE: ClassVar[int] = 404


class UnauthorizedException(ApiException):
    """Unauthorized exception."""

    STATUS_CODE: ClassVar[int] = 401


class ForbiddenException(ApiException):
    """Forbidden exception."""

    STATUS_CODE: ClassVar[int] = 403


class ServiceException(ApiException):
    """Service error exception."""

    STATUS_CODE: ClassVar[int] = 500


def render_path(path_to_item: list[str | int]) -> str:
    """Format a path for error messages.

    Args:
        path_to_item: Path to the item

    Returns:
        Formatted path string

    """
    result = ""
    for pth in path_to_item:
        if isinstance(pth, int):
            result += f"[{pth}]"
        else:
            result += f"['{pth}']"
    return result


def handle_http_error(error: httpx.HTTPStatusError) -> None:
    """Handle HTTP errors by raising appropriate exceptions.

    Args:
        error: HTTP status error

    Raises:
        UnauthorizedException: For 401 errors
        ForbiddenException: For 403 errors
        NotFoundException: For 404 errors
        ServiceException: For 5xx errors
        ApiException: For other errors

    """
    status_code = error.response.status_code
    reason = error.response.reason_phrase

    logger.error("HTTP error: %s - %s", status_code, reason)

    if status_code == UnauthorizedException.STATUS_CODE:
        raise UnauthorizedException(http_resp=error.response)
    if status_code == ForbiddenException.STATUS_CODE:
        raise ForbiddenException(http_resp=error.response)
    if status_code == NotFoundException.STATUS_CODE:
        raise NotFoundException(http_resp=error.response)
    if 500 <= status_code < 600:
        raise ServiceException(http_resp=error.response)
    raise ApiException(http_resp=error.response)
