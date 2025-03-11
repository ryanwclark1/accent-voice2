# Copyright 2025 Accent Communications

"""Command base classes for Chat Daemon API."""

from __future__ import annotations

import logging
from typing import ClassVar

import httpx
from accent_lib_rest_client.command import RESTCommand as BaseRESTCommand

from .exceptions import ChatdError, ChatdServiceUnavailable, InvalidChatdError

logger = logging.getLogger(__name__)


class ChatdCommand(BaseRESTCommand):
    """Base command class for Chat Daemon API requests.

    Extends the REST command with Chat Daemon-specific error handling.
    """

    _headers: ClassVar[dict[str, str]] = {"Accept": "application/json"}

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Extract error information from a response and raise an appropriate exception.

        Args:
            response: The HTTP response

        Raises:
            ChatdServiceUnavailable: If the service is unavailable
            ChatdError: For other Chat Daemon-specific errors
            httpx.HTTPStatusError: For standard HTTP errors

        """
        if response.status_code == 503:
            raise ChatdServiceUnavailable(response)

        try:
            raise ChatdError(response)
        except InvalidChatdError:
            BaseRESTCommand.raise_from_response(response)
