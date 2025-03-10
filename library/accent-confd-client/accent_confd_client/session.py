# Copyright 2025 Accent Communications

"""Configuration Daemon session module."""

import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class ConfdSession:
    """Session for the Configuration Daemon API.

    This class wraps httpx clients to provide a consistent interface
    for making requests to the Accent Configuration Daemon API.
    """

    OK_STATUSES = (200, 201, 204)  # ok, created, no content

    READ_HEADERS = {"Accept": "application/json"}

    WRITE_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, client: httpx.Client, base_url: str) -> None:
        """Initialize the session.

        Args:
            client: Configured httpx client
            base_url: Base URL for the API

        """
        self.client = client
        self.base_url = base_url
        self.async_client: httpx.AsyncClient | None = None

    def check_response(self, response: httpx.Response, check: bool = True) -> None:
        """Check if a response indicates an error.

        Args:
            response: HTTP response to check
            check: Whether to actually perform the check

        Raises:
            httpx.HTTPStatusError: If the response indicates an error

        """
        if not check:
            return

        if response.status_code not in self.OK_STATUSES:
            try:
                messages = response.json()
            except ValueError:
                pass
            else:
                response.reason_phrase = ". ".join(messages)

            response.raise_for_status()

    def clean_url(self, part: str) -> str:
        """Create a clean URL by joining the base URL with a path part.

        Args:
            part: URL path part

        Returns:
            Complete URL

        """
        return f"{self.base_url.rstrip('/')}/{part.lstrip('/')}"

    def head(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a HEAD request.

        Args:
            url: URL path
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.READ_HEADERS)
        check_response = kwargs.pop("check_response", True)

        url = self.clean_url(url)
        response = self.client.head(url, **kwargs)

        self.check_response(response, check_response)
        return response

    async def head_async(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a HEAD request asynchronously.

        Args:
            url: URL path
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.READ_HEADERS)
        check_response = kwargs.pop("check_response", True)

        if self.async_client is None:
            # Create async client with same properties as sync client
            self.async_client = httpx.AsyncClient(
                verify=self.client.verify,
                headers=self.client.headers,
                timeout=self.client.timeout,
            )

        url = self.clean_url(url)
        response = await self.async_client.head(url, **kwargs)

        self.check_response(response, check_response)
        return response

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a GET request.

        Args:
            url: URL path
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.READ_HEADERS)
        check_response = kwargs.pop("check_response", True)

        url = self.clean_url(url)
        response = self.client.get(url, **kwargs)

        self.check_response(response, check_response)
        return response

    async def get_async(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a GET request asynchronously.

        Args:
            url: URL path
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.READ_HEADERS)
        check_response = kwargs.pop("check_response", True)

        if self.async_client is None:
            # Create async client with same properties as sync client
            self.async_client = httpx.AsyncClient(
                verify=self.client.verify,
                headers=self.client.headers,
                timeout=self.client.timeout,
            )

        url = self.clean_url(url)
        response = await self.async_client.get(url, **kwargs)

        self.check_response(response, check_response)
        return response

    def post(self, url: str, body: Any = None, **kwargs: Any) -> httpx.Response:
        """Send a POST request.

        Args:
            url: URL path
            body: Request body
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.WRITE_HEADERS)
        check_response = kwargs.pop("check_response", True)

        url = self.clean_url(url)
        encoded_body = self.encode_body(body, kwargs)
        response = self.client.post(url, content=encoded_body, **kwargs)

        self.check_response(response, check_response)
        return response

    async def post_async(
        self, url: str, body: Any = None, **kwargs: Any
    ) -> httpx.Response:
        """Send a POST request asynchronously.

        Args:
            url: URL path
            body: Request body
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.WRITE_HEADERS)
        check_response = kwargs.pop("check_response", True)

        if self.async_client is None:
            # Create async client with same properties as sync client
            self.async_client = httpx.AsyncClient(
                verify=self.client.verify,
                headers=self.client.headers,
                timeout=self.client.timeout,
            )

        url = self.clean_url(url)
        encoded_body = self.encode_body(body, kwargs)
        response = await self.async_client.post(url, content=encoded_body, **kwargs)

        self.check_response(response, check_response)
        return response

    def put(self, url: str, body: Any = None, **kwargs: Any) -> httpx.Response:
        """Send a PUT request.

        Args:
            url: URL path
            body: Request body
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.WRITE_HEADERS)
        check_response = kwargs.pop("check_response", True)

        url = self.clean_url(url)
        encoded_body = self.encode_body(body, kwargs)
        response = self.client.put(url, content=encoded_body, **kwargs)

        self.check_response(response, check_response)
        return response

    async def put_async(
        self, url: str, body: Any = None, **kwargs: Any
    ) -> httpx.Response:
        """Send a PUT request asynchronously.

        Args:
            url: URL path
            body: Request body
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.WRITE_HEADERS)
        check_response = kwargs.pop("check_response", True)

        if self.async_client is None:
            # Create async client with same properties as sync client
            self.async_client = httpx.AsyncClient(
                verify=self.client.verify,
                headers=self.client.headers,
                timeout=self.client.timeout,
            )

        url = self.clean_url(url)
        encoded_body = self.encode_body(body, kwargs)
        response = await self.async_client.put(url, content=encoded_body, **kwargs)

        self.check_response(response, check_response)
        return response

    def encode_body(self, body: Any, kwargs: dict[str, Any]) -> bytes | None:
        """Encode the request body.

        Args:
            body: Request body
            kwargs: Keyword arguments

        Returns:
            Encoded body or None

        """
        raw = kwargs.pop("raw", None)
        if raw:
            return raw
        if body is not None:
            return json.dumps(body).encode("utf-8")
        return None

    def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a DELETE request.

        Args:
            url: URL path
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.READ_HEADERS)
        check_response = kwargs.pop("check_response", True)

        url = self.clean_url(url)
        response = self.client.delete(url, **kwargs)

        self.check_response(response, check_response)
        return response

    async def delete_async(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a DELETE request asynchronously.

        Args:
            url: URL path
            **kwargs: Additional arguments passed to the request

        Returns:
            HTTP response

        """
        kwargs.setdefault("headers", self.READ_HEADERS)
        check_response = kwargs.pop("check_response", True)

        if self.async_client is None:
            # Create async client with same properties as sync client
            self.async_client = httpx.AsyncClient(
                verify=self.client.verify,
                headers=self.client.headers,
                timeout=self.client.timeout,
            )

        url = self.clean_url(url)
        response = await self.async_client.delete(url, **kwargs)

        self.check_response(response, check_response)
        return response
