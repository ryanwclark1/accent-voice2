# Copyright 2025 Accent Communications

"""Base command module for Webhookd API interactions.

This module defines the base command class for Webhookd API operations,
including error handling and response processing.
"""

from __future__ import annotations

import logging
from typing import Any, TypeVar

import httpx
from accent_lib_rest_client.command import RESTCommand

from accent_webhookd_client.exceptions import (
    InvalidWebhookdError,
    WebhookdError,
    WebhookdServiceUnavailable,
)

# Configure logging
logger = logging.getLogger(__name__)

T = TypeVar("T")


class WebhookdCommand(RESTCommand):
    """Base command for Webhookd API operations.

    This command extends the RESTCommand with specialized error handling
    for Webhookd API responses.
    """

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Raise appropriate exceptions based on the HTTP response.

        Args:
            response: The HTTP response to process

        Raises:
            WebhookdServiceUnavailable: If the service is unavailable (503)
            WebhookdError: For other Webhookd-specific errors
            httpx.HTTPStatusError: For general HTTP errors

        """
        if response.status_code == 503:
            raise WebhookdServiceUnavailable(response)

        try:
            raise WebhookdError(response)
        except InvalidWebhookdError:
            # Fall back to standard error handling
            RESTCommand.raise_from_response(response)

    async def _async_request(
        self, method: str, url: str, **kwargs: Any
    ) -> httpx.Response:
        """Make an asynchronous HTTP request with retry logic.

        Args:
            method: HTTP method (get, post, etc.)
            url: Target URL
            **kwargs: Additional arguments for the request

        Returns:
            HTTP response

        Raises:
            WebhookdError: If the request fails

        """
        headers = kwargs.pop("headers", self._get_headers())
        max_retries = self._client.config.max_retries

        for attempt in range(max_retries):
            try:
                request_method = getattr(self.async_client, method.lower())
                response = await request_method(url, headers=headers, **kwargs)
                return response
            except httpx.RequestError as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        "Request failed (attempt %d/%d): %s",
                        attempt + 1,
                        max_retries,
                        str(e),
                    )
                    import asyncio

                    await asyncio.sleep(self._client.config.retry_delay)
                    continue
                logger.error(
                    "Request failed after %d attempts: %s", max_retries, str(e)
                )
                raise

    def _sync_request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Make a synchronous HTTP request with retry logic.

        Args:
            method: HTTP method (get, post, etc.)
            url: Target URL
            **kwargs: Additional arguments for the request

        Returns:
            HTTP response

        Raises:
            WebhookdError: If the request fails

        """
        headers = kwargs.pop("headers", self._get_headers())
        max_retries = self._client.config.max_retries

        for attempt in range(max_retries):
            try:
                request_method = getattr(self.sync_client, method.lower())
                response = request_method(url, headers=headers, **kwargs)
                return response
            except httpx.RequestError as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        "Request failed (attempt %d/%d): %s",
                        attempt + 1,
                        max_retries,
                        str(e),
                    )
                    import time

                    time.sleep(self._client.config.retry_delay)
                    continue
                logger.error(
                    "Request failed after %d attempts: %s", max_retries, str(e)
                )
                raise
