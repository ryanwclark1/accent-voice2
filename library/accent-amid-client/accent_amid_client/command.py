# Copyright 2025 Accent Communications

"""Base command classes for AMID API requests.

This module defines the base command class for all AMID API commands.
"""

from __future__ import annotations

import logging

import httpx
from accent_lib_rest_client.command import RESTCommand

from .exceptions import (
    AmidError,
    AmidProtocolError,
    AmidServiceUnavailable,
    InvalidAmidError,
)

logger = logging.getLogger(__name__)


class AmidCommand(RESTCommand):
    """Base class for AMID API commands.

    This class extends the RESTCommand with AMID-specific error handling.
    """

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Extract error information from a response and raise an exception.

        Args:
            response: The HTTP response

        Raises:
            AmidServiceUnavailable: If the response status code is 503
            AmidError: If the response contains a valid AMID error
            InvalidAmidError: If the response format is invalid

        """
        logger.debug(
            "Processing error response: %s %s",
            response.status_code,
            response.text[:200],
        )

        if response.status_code == 503:
            raise AmidServiceUnavailable(response)

        try:
            raise AmidError(response)
        except InvalidAmidError:
            # Fall back to base class error handling
            RESTCommand.raise_from_response(response)

    @staticmethod
    def raise_from_protocol(response: httpx.Response) -> None:
        """Extract protocol error information from a response and raise an exception.

        Args:
            response: The HTTP response

        Raises:
            AmidProtocolError: If the response contains a valid AMID protocol error
            InvalidAmidError: If the response format is invalid

        """
        logger.debug("Processing protocol error: %s", response.text[:200])

        try:
            raise AmidProtocolError(response)
        except InvalidAmidError:
            # Fall back to base class error handling
            RESTCommand.raise_from_response(response)
