# Copyright 2025 Accent Communications

"""Base command classes for the Accent Deployd client.

This module provides the base command classes that implement the common
functionality for interacting with the Deployd API.
"""

from __future__ import annotations

import logging
from typing import Any, TypeVar, cast

import httpx
from accent_lib_rest_client.command import RESTCommand

from .exceptions import DeploydError, DeploydServiceUnavailable, InvalidDeploydError

logger = logging.getLogger(__name__)
T = TypeVar("T")


class DeploydCommand(RESTCommand):
    """Base command class for Deployd API operations.

    This class extends the REST command functionality with Deployd-specific
    error handling and response processing.
    """

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Extract error information from a response and raise an exception.

        Args:
            response: The HTTP response

        Raises:
            DeploydServiceUnavailable: If the service is unavailable
            DeploydError: If the response indicates an error
            httpx.HTTPStatusError: If the response indicates an unknown error

        """
        if response.status_code == 503:
            raise DeploydServiceUnavailable(response)

        try:
            raise DeploydError(response)
        except InvalidDeploydError:
            RESTCommand.raise_from_response(response)

    async def _process_get_request(
        self, url: str, headers: dict[str, str], params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Process a GET request and return the JSON response.

        Args:
            url: Request URL
            headers: Request headers
            params: Optional query parameters

        Returns:
            JSON response data

        Raises:
            DeploydError: If the response indicates an error

        """
        logger.debug("GET request to %s with params %s", url, params)

        response = await self.async_client.get(url, headers=headers, params=params)

        if response.status_code != 200:
            self.raise_from_response(response)

        return cast(dict[str, Any], response.json())

    async def _process_post_request(
        self, url: str, data: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        """Process a POST request and return the JSON response.

        Args:
            url: Request URL
            data: Request payload
            headers: Request headers

        Returns:
            JSON response data

        Raises:
            DeploydError: If the response indicates an error

        """
        logger.debug("POST request to %s", url)

        response = await self.async_client.post(url, json=data, headers=headers)

        if response.status_code != 201:
            self.raise_from_response(response)

        return cast(dict[str, Any], response.json())

    async def _process_put_request(
        self, url: str, data: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        """Process a PUT request and return the JSON response.

        Args:
            url: Request URL
            data: Request payload
            headers: Request headers

        Returns:
            JSON response data

        Raises:
            DeploydError: If the response indicates an error

        """
        logger.debug("PUT request to %s", url)

        response = await self.async_client.put(url, json=data, headers=headers)

        if response.status_code != 200:
            self.raise_from_response(response)

        return cast(dict[str, Any], response.json())

    async def _process_delete_request(self, url: str, headers: dict[str, str]) -> None:
        """Process a DELETE request.

        Args:
            url: Request URL
            headers: Request headers

        Raises:
            DeploydError: If the response indicates an error

        """
        logger.debug("DELETE request to %s", url)

        response = await self.async_client.delete(url, headers=headers)

        if response.status_code != 204:
            self.raise_from_response(response)
