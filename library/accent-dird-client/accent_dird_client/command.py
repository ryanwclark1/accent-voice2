# Copyright 2025 Accent Communications

"""Base command classes for directory service operations."""

import logging
from typing import TypeVar

import httpx
from accent_lib_rest_client.command import RESTCommand

from .exceptions import DirdError, DirdServiceUnavailable, InvalidDirdError

logger = logging.getLogger(__name__)
T = TypeVar("T")


class DirdCommand(RESTCommand):
    """Base command for directory service operations."""

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Raise appropriate exceptions based on response status.

        Args:
            response: The HTTP response

        Raises:
            DirdServiceUnavailable: If service is unavailable (503)
            DirdError: For other Dird-specific errors
            HTTPStatusError: For generic HTTP errors

        """
        if response.status_code == 503:
            raise DirdServiceUnavailable(response)

        try:
            raise DirdError(response)
        except InvalidDirdError:
            RESTCommand.raise_from_response(response)
