# Copyright 2025 Accent Communications

"""Exceptions for Chat Daemon client."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)


class InvalidChatdError(Exception):
    """Raised when a response doesn't match the expected Chat Daemon format."""

    pass  # noqa: PIE790


class ChatdError(httpx.HTTPStatusError):
    """Base exception for Chat Daemon API errors."""

    def __init__(self, response: httpx.Response) -> None:
        """Initialize with error details from response.

        Args:
            response: The HTTP response

        Raises:
            InvalidChatdError: If the response doesn't match the expected format

        """
        try:
            body = response.json()
        except ValueError:
            raise InvalidChatdError

        self.status_code = response.status_code
        try:
            self.message = body["message"]
            self.error_id = body["error_id"]
            self.details = body["details"]
            self.timestamp = body["timestamp"]
            if resource := body.get("resource"):
                self.resource = resource
        except KeyError:
            raise InvalidChatdError

        exception_message = f"{self.message}: {self.details}"
        super().__init__(exception_message, request=response.request, response=response)


class ChatdServiceUnavailable(ChatdError):
    """Raised when the Chat Daemon service is unavailable."""

    pass  # noqa: PIE790
