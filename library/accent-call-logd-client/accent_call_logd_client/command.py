# Copyright 2025 Accent Communications

"""Command module for the accent-call-logd-client library."""

from __future__ import annotations

import logging

import httpx
from accent_lib_rest_client.command import HTTPCommand

from .exceptions import CallLogdError, CallLogdServiceUnavailable, InvalidCallLogdError

logger = logging.getLogger(__name__)


class CallLogdCommand(HTTPCommand):
    """Base command for Call Log daemon API requests."""

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Extract error information from a response and raise an appropriate exception.

        Args:
            response: The HTTP response

        Raises:
            CallLogdServiceUnavailable: If service is unavailable (503)
            CallLogdError: For other Call Log daemon API errors
            httpx.HTTPStatusError: For other HTTP errors

        """
        logger.debug("Processing response with status code: %s", response.status_code)

        if response.status_code == 503:
            logger.error("Call Log daemon service unavailable")
            raise CallLogdServiceUnavailable(response)

        try:
            logger.error("Call Log daemon error: %s", response.text)
            raise CallLogdError(response)
        except InvalidCallLogdError:
            logger.debug("Not a Call Log daemon error, delegating to base handler")
            HTTPCommand.raise_from_response(response)
