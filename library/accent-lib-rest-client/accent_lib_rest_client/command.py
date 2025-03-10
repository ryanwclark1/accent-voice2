# Copyright 2025 Accent Communications

from __future__ import annotations

from abc import ABCMeta
from typing import Any, ClassVar

import httpx
from pydantic import BaseModel

from accent_lib_rest_client.client import BaseClient


class CommandResponse(BaseModel):
    """Standard response model for API command results.

    Attributes:
        content: Raw response content
        status_code: HTTP status code
        headers: Response headers

    """

    content: bytes | str
    status_code: int
    headers: dict[str, str]


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
                response.reason_phrase = response_json["message"]
        except (ValueError, KeyError, TypeError):
            pass

        response.raise_for_status()


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
