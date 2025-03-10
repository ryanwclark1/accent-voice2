# Copyright 2025 Accent Communications

"""Command implementations for the Calld API.

This module defines the base command class for Calld API operations.
"""

from __future__ import annotations

import logging

import httpx
from accent_lib_rest_client.command import RESTCommand

from .exceptions import CalldError, InvalidCalldError

logger = logging.getLogger(__name__)


class CalldCommand(RESTCommand):
    """Base command class for Calld API operations.

    This class handles common error processing for all Calld commands.
    """

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Extract error information from a response and raise a CalldError.

        Args:
            response: The HTTP response

        Raises:
            CalldError: If the response indicates a Calld error
            httpx.HTTPStatusError: If the response indicates another error type

        """
        try:
            raise CalldError(response)
        except InvalidCalldError:
            RESTCommand.raise_from_response(response)
