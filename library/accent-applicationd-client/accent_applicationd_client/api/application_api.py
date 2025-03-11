# Copyright 2025 Accent Communications
"""Application API for the Accent applicationd client.
"""

from __future__ import annotations

import logging
from typing import Any, Literal, TypeVar, overload

from accent_applicationd_client.api_client import ApiClient
from accent_applicationd_client.exceptions import (
    ApiValueError,
)

T = TypeVar("T")
logger = logging.getLogger(__name__)


class ApplicationApi:
    """Application API.

    This API provides methods for interacting with applications.
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
    def call_answer10_applications_application_uuid_calls_call_id_answer_put(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any,
    ) -> object: ...

    @overload
    def call_answer10_applications_application_uuid_calls_call_id_answer_put(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any,
    ) -> Any: ...

    def call_answer10_applications_application_uuid_calls_call_id_answer_put(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> object | Any:
        """Answer a call.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True

        if kwargs.get("async_req"):
            return self.call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
                application_uuid, call_id, **kwargs
            )
        (
            data
        ) = self.call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
            application_uuid, call_id, **kwargs
        )
        return data

    async def call_answer10_applications_application_uuid_calls_call_id_answer_put_async(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> object:
        """Answer a call asynchronously.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True
        kwargs["async_req"] = True

        return await self.call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info_async(
            application_uuid, call_id, **kwargs
        )

    @overload
    def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any,
    ) -> tuple[object, int, dict[str, str]]: ...

    @overload
    def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any,
    ) -> Any: ...

    def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> tuple[object, int, dict[str, str]] | Any:
        """Answer a call with HTTP info.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_uuid is None:
            raise ApiValueError("Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError("Missing required parameter `call_id`")

        # Extract path parameters
        path_params = {
            "application_uuid": application_uuid,
            "call_id": call_id,
        }

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
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_uuid}/calls/{call_id}/answer",
            "PUT",
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

    async def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info_async(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]:
        """Answer a call with HTTP info asynchronously.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_uuid is None:
            raise ApiValueError("Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError("Missing required parameter `call_id`")

        # Extract path parameters
        path_params = {
            "application_uuid": application_uuid,
            "call_id": call_id,
        }

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
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/1.0/applications/{application_uuid}/calls/{call_id}/answer",
            "PUT",
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

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any,
    ) -> object: ...

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any,
    ) -> Any: ...

    def call_hangup10_applications_application_uuid_calls_call_id_delete(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> object | Any:
        """Hang up a call.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True

        if kwargs.get("async_req"):
            return self.call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
                application_uuid, call_id, **kwargs
            )
        (
            data
        ) = self.call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
            application_uuid, call_id, **kwargs
        )
        return data

    async def call_hangup10_applications_application_uuid_calls_call_id_delete_async(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> object:
        """Hang up a call asynchronously.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True
        kwargs["async_req"] = True

        return await self.call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info_async(
            application_uuid, call_id, **kwargs
        )

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any,
    ) -> tuple[object, int, dict[str, str]]: ...

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any,
    ) -> Any: ...

    def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> tuple[object, int, dict[str, str]] | Any:
        """Hang up a call with HTTP info.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_uuid is None:
            raise ApiValueError("Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError("Missing required parameter `call_id`")

        # Extract path parameters
        path_params = {
            "application_uuid": application_uuid,
            "call_id": call_id,
        }

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
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_uuid}/calls/{call_id}",
            "DELETE",
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

    async def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info_async(
        self, application_uuid: str, call_id: str, **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]:
        """Hang up a call with HTTP info asynchronously.

        Args:
            application_uuid: Application UUID
            call_id: Call ID
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            API response object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_uuid is None:
            raise ApiValueError("Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError("Missing required parameter `call_id`")

        # Extract path parameters
        path_params = {
            "application_uuid": application_uuid,
            "call_id": call_id,
        }

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
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/1.0/applications/{application_uuid}/calls/{call_id}",
            "DELETE",
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
