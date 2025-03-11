# Copyright 2025 Accent Communications

"""Base command implementation for Setupd client."""

from __future__ import annotations

import logging

import httpx
from accent_lib_rest_client.command import RESTCommand

from .exceptions import (
    InvalidSetupdError,
    SetupdError,
    SetupdServiceUnavailable,
    SetupdSetupError,
)

logger = logging.getLogger(__name__)


class SetupdCommand(RESTCommand):
    """Base command for Setupd API operations."""

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Extract error information from a response and raise an appropriate exception.

        Args:
            response: The HTTP response

        Raises:
            SetupdServiceUnavailable: If the service is unavailable
            SetupdSetupError: If a setup error occurred
            SetupdError: For other Setupd-specific errors
            httpx.HTTPStatusError: For general HTTP errors

        """
        if response.status_code == 503:
            raise SetupdServiceUnavailable(response)

        if response.status_code == 500:
            try:
                raise SetupdSetupError(response)
            except InvalidSetupdError:
                pass

        try:
            raise SetupdError(response)
        except InvalidSetupdError:
            RESTCommand.raise_from_response(response)
