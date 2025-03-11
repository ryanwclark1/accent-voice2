# Copyright 2025 Accent Communications
"""Status API for the Accent applicationd client.
"""

from __future__ import annotations

import logging
from typing import Any, Literal, TypeVar, overload

from accent_applicationd_client.api_client import ApiClient
from accent_applicationd_client.models.status import Status

T = TypeVar("T")
logger = logging.getLogger(__name__)


class StatusApi:
    """Status API.

    This API provides methods for checking service status.
    """

    def __init__(self, api_client: ApiClient | None = None) -> None:
        """Initialize the API.

        Args:
            api_client: API client instance

        """
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    @overload
    def status_status_get(
        self, *, async_req: Literal[False] = False, **kwargs: Any
    ) -> Status: ...

    @overload
    def status_status_get(self, *, async_req: Literal[True], **kwargs: Any) -> Any: ...

    def status_status_get(self, **kwargs: Any) -> Status | Any:
        """Get service status.

        Args:
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Status object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True

        if kwargs.get("async_req"):
            return self.status_status_get_with_http_info(**kwargs)
        (data) = self.status_status_get_with_http_info(**kwargs)
        return data

    async def status_status_get_async(self, **kwargs: Any) -> Status:
        """Get service status asynchronously.

        Args:
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Status object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True
        kwargs["async_req"] = True

        return await self.status_status_get_with_http_info_async(**kwargs)

    @overload
    def status_status_get_with_http_info(
        self, *, async_req: Literal[False] = False, **kwargs: Any
    ) -> tuple[Status, int, dict[str, str]]: ...

    @overload
    def status_status_get_with_http_info(
        self, *, async_req: Literal[True], **kwargs: Any
    ) -> Any: ...

    def status_status_get_with_http_info(
        self, **kwargs: Any
    ) -> tuple[Status, int, dict[str, str]] | Any:
        """Get service status with HTTP info.

        Args:
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Status object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Extract path parameters
        path_params = {}

        # Extract query parameters
        query_params = []

        # Extract header parameters
        header_params = {}

        # Set accept header
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "Status",
        }

        # Make the request
        return self.api_client.call_api(
            "/status",
            "GET",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs,
        )

    async def status_status_get_with_http_info_async(
        self, **kwargs: Any
    ) -> tuple[Status, int, dict[str, str]]:
        """Get service status with HTTP info asynchronously.

        Args:
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Status object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Extract path parameters
        path_params = {}

        # Extract query parameters
        query_params = []

        # Extract header parameters
        header_params = {}

        # Set accept header
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "Status",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/status",
            "GET",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs,
        )
