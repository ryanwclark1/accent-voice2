# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
import time
from abc import ABCMeta
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar

# Direct imports needed for runtime
import httpx

# Imports only for type checking
if TYPE_CHECKING:
    from accent_lib_rest_client.client import BaseClient
    from accent_lib_rest_client.models import CommandResponse as CommandResponseType
    from accent_lib_rest_client.models import JSONResponse as JSONResponseType

from accent_lib_rest_client.exceptions import handle_http_error
from accent_lib_rest_client.models import CommandResponse, JSONResponse

logger = logging.getLogger(__name__)
T = TypeVar("T")


class HTTPCommand:
    """Base class for HTTP commands.

    This provides basic HTTP functionality common to all commands.
    """

    def __init__(self, client: BaseClient) -> None:
        """Initialize the command with a client.

        Args:
            client: The API client to use for requests

        """
        self._client = client

    @property
    def sync_client(self) -> httpx.Client:
        """Get the synchronous HTTP client.

        Returns:
            Configured httpx.Client instance

        """
        return self._client.sync_client

    @property
    def async_client(self) -> httpx.AsyncClient:
        """Get the asynchronous HTTP client.

        Returns:
            Configured httpx.AsyncClient instance

        """
        return self._client.async_client

    # For backwards compatibility
    @property
    def session(self) -> httpx.Client:
        """Get the synchronous HTTP client (compatibility method).

        Returns:
            Configured httpx.Client instance

        """
        return self._client.sync_client

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Extract error information from a response and raise an exception.

        Args:
            response: The HTTP response

        Raises:
            httpx.HTTPStatusError: If the response indicates an error

        """
        try:
            response_json = response.json()
            if isinstance(response_json, dict) and "message" in response_json:
                # Note: Can't modify reason_phrase directly as it's read-only
                # We'll raise the exception with the custom message later
                custom_message = response_json["message"]
                # This might still raise an exception, which we allow to propagate
                response.raise_for_status()
                # If we get here, create a custom exception with our message
                raise httpx.HTTPStatusError(
                    custom_message,
                    request=response.request,
                    response=response,
                )
        except (ValueError, KeyError, TypeError):
            pass

        response.raise_for_status()

    def process_response(
        self, response: httpx.Response, start_time: float | None = None
    ) -> CommandResponseType:
        """Process an HTTP response into a standard CommandResponse.

        Args:
            response: The HTTP response
            start_time: Optional start time for calculating response time

        Returns:
            Standardized response object

        Raises:
            AccentAPIError: If the response indicates an error

        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            handle_http_error(e)

        response_time = None
        if start_time:
            response_time = time.time() - start_time

        return CommandResponse(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers.items()),
            response_time=response_time,
        )

    def process_json_response(
        self, response: httpx.Response, start_time: float | None = None
    ) -> JSONResponseType:
        """Process an HTTP response into a JSON response object.

        Args:
            response: The HTTP response
            start_time: Optional start time for calculating response time

        Returns:
            JSON response object

        Raises:
            AccentAPIError: If the response indicates an error
            ValueError: If the response is not valid JSON

        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            handle_http_error(e)

        response_time = None
        if start_time:
            response_time = time.time() - start_time

        return JSONResponse(
            data=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers.items()),
            response_time=response_time,
        )


class RESTCommand(HTTPCommand):
    """Base class for REST API commands.

    This extends HTTPCommand with REST-specific functionality.
    """

    __metaclass__ = ABCMeta

    resource: ClassVar[str]
    _headers: ClassVar[dict[str, str]] = {"Accept": "application/json"}

    def __init__(self, client: BaseClient) -> None:
        """Initialize the REST command.

        Args:
            client: The API client to use for requests

        """
        super().__init__(client)
        self.base_url = self._client.url(self.resource)
        self.timeout = self._client.config.timeout

    # The ANN401 warning for Any in **kwargs is unavoidable here
    # because we need to support arbitrary keyword arguments
    def _get_headers(self, **kwargs: Any) -> dict[str, str]:
        """Get headers for the request, including custom tenant if specified.

        Args:
            **kwargs: Additional parameters, can include tenant_uuid

        Returns:
            Headers dictionary

        """
        headers = dict(self._headers)
        # The client will use client.tenant_uuid by default
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        if tenant_uuid:
            headers["Accent-Tenant"] = str(tenant_uuid)
        return headers
