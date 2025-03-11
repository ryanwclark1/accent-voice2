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
from accent_applicationd_client.models.application import Application
from accent_applicationd_client.models.node import Node

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
        **kwargs: Any
    ) -> object: ...

    @overload
    def call_answer10_applications_application_uuid_calls_call_id_answer_put(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_answer10_applications_application_uuid_calls_call_id_answer_put(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
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
                application_uuid, call_id, **kwargs)
        (data) = self.call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
            application_uuid, call_id, **kwargs)
        return data

    async def call_answer10_applications_application_uuid_calls_call_id_answer_put_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> object:
        """Answer a call asynchronously.
        
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

        return await self.call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info_async(
            application_uuid, call_id, **kwargs)

    @overload
    def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]: ...

    @overload
    def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
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
            raise ApiValueError(
                "Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError(
                "Missing required parameter `call_id`")

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
        header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_uuid}/calls/{call_id}/answer", "PUT",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs
        )

    async def call_answer10_applications_application_uuid_calls_call_id_answer_put_with_http_info_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
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
            raise ApiValueError(
                "Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError(
                "Missing required parameter `call_id`")

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
        header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/1.0/applications/{application_uuid}/calls/{call_id}/answer", "PUT",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs
        )

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any
    ) -> object: ...

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_hangup10_applications_application_uuid_calls_call_id_delete(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
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
                application_uuid, call_id, **kwargs)
        (data) = self.call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
            application_uuid, call_id, **kwargs)
        return data

    async def call_hangup10_applications_application_uuid_calls_call_id_delete_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
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
            application_uuid, call_id, **kwargs)

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]: ...

    @overload
    def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
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
            raise ApiValueError(
                "Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError(
                "Missing required parameter `call_id`")

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
        header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_uuid}/calls/{call_id}", "DELETE",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs
        )

    async def call_hangup10_applications_application_uuid_calls_call_id_delete_with_http_info_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
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
            raise ApiValueError(
                "Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError(
                "Missing required parameter `call_id`")

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
        header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/1.0/applications/{application_uuid}/calls/{call_id}", "DELETE",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs
        )

    @overload
    def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any
    ) -> object: ...

    @overload
    def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> object | Any:
        """Start muting a call.
        
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
            return self.call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_with_http_info(
                application_uuid, call_id, **kwargs)
        (data) = self.call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_with_http_info(
            application_uuid, call_id, **kwargs)
        return data

    async def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> object:
        """Start muting a call asynchronously.
        
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

        return await self.call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_with_http_info_async(
            application_uuid, call_id, **kwargs)

    @overload
    def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]: ...

    @overload
    def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]] | Any:
        """Start muting a call with HTTP info.
        
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
            raise ApiValueError(
                "Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError(
                "Missing required parameter `call_id`")

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
        header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_uuid}/calls/{call_id}/mute/start", "POST",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs
        )

    async def call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post_with_http_info_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]:
        """Start muting a call with HTTP info asynchronously.
        
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
            raise ApiValueError(
                "Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError(
                "Missing required parameter `call_id`")

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
        header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/1.0/applications/{application_uuid}/calls/{call_id}/mute/start", "POST",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs
        )

    @overload
    def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any
    ) -> object: ...

    @overload
    def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> object | Any:
        """Stop muting a call.
        
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
            return self.call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_with_http_info(
                application_uuid, call_id, **kwargs)
        (data) = self.call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_with_http_info(
            application_uuid, call_id, **kwargs)
        return data

    async def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> object:
        """Stop muting a call asynchronously.
        
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

        return await self.call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_with_http_info_async(
            application_uuid, call_id, **kwargs)

    @overload
    def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[False] = False,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]: ...

    @overload
    def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        *,
        async_req: Literal[True],
        **kwargs: Any
    ) -> Any: ...

    def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_with_http_info(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]] | Any:
        """Stop muting a call with HTTP info.
        
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
            raise ApiValueError(
                "Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and call_id is None:
            raise ApiValueError(
                "Missing required parameter `call_id`")

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
        header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "object",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_uuid}/calls/{call_id}/mute/stop", "POST",
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs
        )

    async def call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post_with_http_info_async(
        self,
        application_uuid: str,
        call_id: str,
        **kwargs: Any
    ) -> tuple[object, int, dict[str, str]]:
        """Stop muting a call with HTTP info asynchronously.

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
            "/1.0/applications/{application_uuid}/calls/{call_id}/mute/stop",
            "POST",
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
    def create_node_with_calls10_applications_application_uuid_nodes_node_name_post(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        *,
        async_req: Literal[False] = False,
        **kwargs: Any,
    ) -> Node: ...

    @overload
    def create_node_with_calls10_applications_application_uuid_nodes_node_name_post(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        *,
        async_req: Literal[True],
        **kwargs: Any,
    ) -> Any: ...

    def create_node_with_calls10_applications_application_uuid_nodes_node_name_post(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        **kwargs: Any,
    ) -> Node | Any:
        """Create a node with calls.

        Args:
            application_uuid: Application UUID
            node_name: Node name
            request_body: List of call IDs
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Node object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True

        if kwargs.get("async_req"):
            return self.create_node_with_calls10_applications_application_uuid_nodes_node_name_post_with_http_info(
                application_uuid, node_name, request_body, **kwargs
            )
        (
            data
        ) = self.create_node_with_calls10_applications_application_uuid_nodes_node_name_post_with_http_info(
            application_uuid, node_name, request_body, **kwargs
        )
        return data

    async def create_node_with_calls10_applications_application_uuid_nodes_node_name_post_async(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        **kwargs: Any,
    ) -> Node:
        """Create a node with calls asynchronously.

        Args:
            application_uuid: Application UUID
            node_name: Node name
            request_body: List of call IDs
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Node object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True
        kwargs["async_req"] = True

        return await self.create_node_with_calls10_applications_application_uuid_nodes_node_name_post_with_http_info_async(
            application_uuid, node_name, request_body, **kwargs
        )

    @overload
    def create_node_with_calls10_applications_application_uuid_nodes_node_name_post_with_http_info(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        *,
        async_req: Literal[False] = False,
        **kwargs: Any,
    ) -> tuple[Node, int, dict[str, str]]: ...

    @overload
    def create_node_with_calls10_applications_application_uuid_nodes_node_name_post_with_http_info(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        *,
        async_req: Literal[True],
        **kwargs: Any,
    ) -> Any: ...

    def create_node_with_calls10_applications_application_uuid_nodes_node_name_post_with_http_info(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        **kwargs: Any,
    ) -> tuple[Node, int, dict[str, str]] | Any:
        """Create a node with calls with HTTP info.

        Args:
            application_uuid: Application UUID
            node_name: Node name
            request_body: List of call IDs
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Node object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_uuid is None:
            raise ApiValueError("Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and node_name is None:
            raise ApiValueError("Missing required parameter `node_name`")
        if self.api_client.client_side_validation and request_body is None:
            raise ApiValueError("Missing required parameter `request_body`")

        # Extract path parameters
        path_params = {
            "application_uuid": application_uuid,
            "node_name": node_name,
        }

        # Extract query parameters
        query_params = []

        # Extract header parameters
        header_params = {}

        # Set accept header
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Set content type
        header_params["Content-Type"] = self.api_client.select_header_content_type(
            ["application/json"]
        )

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "Node",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_uuid}/nodes/{node_name}",
            "POST",
            path_params,
            query_params,
            header_params,
            body=request_body,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs,
        )

    async def create_node_with_calls10_applications_application_uuid_nodes_node_name_post_with_http_info_async(
        self,
        application_uuid: str,
        node_name: str,
        request_body: list[str],
        **kwargs: Any,
    ) -> tuple[Node, int, dict[str, str]]:
        """Create a node with calls with HTTP info asynchronously.

        Args:
            application_uuid: Application UUID
            node_name: Node name
            request_body: List of call IDs
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Node object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_uuid is None:
            raise ApiValueError("Missing required parameter `application_uuid`")
        if self.api_client.client_side_validation and node_name is None:
            raise ApiValueError("Missing required parameter `node_name`")
        if self.api_client.client_side_validation and request_body is None:
            raise ApiValueError("Missing required parameter `request_body`")

        # Extract path parameters
        path_params = {
            "application_uuid": application_uuid,
            "node_name": node_name,
        }

        # Extract query parameters
        query_params = []

        # Extract header parameters
        header_params = {}

        # Set accept header
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Set content type
        header_params["Content-Type"] = self.api_client.select_header_content_type(
            ["application/json"]
        )

        # Authentication
        auth_settings = []

        # Map of response types
        response_types_map = {
            200: "Node",
            422: "HTTPValidationError",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/1.0/applications/{application_uuid}/nodes/{node_name}",
            "POST",
            path_params,
            query_params,
            header_params,
            body=request_body,
            post_params=[],
            files={},
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            **kwargs,
        )

    @overload
    def register_application10_applications_application_name_post(
        self, application_name: str, *, async_req: Literal[False] = False, **kwargs: Any
    ) -> Application: ...

    @overload
    def register_application10_applications_application_name_post(
        self, application_name: str, *, async_req: Literal[True], **kwargs: Any
    ) -> Any: ...

    def register_application10_applications_application_name_post(
        self, application_name: str, **kwargs: Any
    ) -> Application | Any:
        """Register an application.

        Args:
            application_name: Application name
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Application object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True

        if kwargs.get("async_req"):
            return self.register_application10_applications_application_name_post_with_http_info(
                application_name, **kwargs
            )
        (
            data
        ) = self.register_application10_applications_application_name_post_with_http_info(
            application_name, **kwargs
        )
        return data

    async def register_application10_applications_application_name_post_async(
        self, application_name: str, **kwargs: Any
    ) -> Application:
        """Register an application asynchronously.

        Args:
            application_name: Application name
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Application object

        Raises:
            ApiException: If the request fails

        """
        kwargs["_return_http_data_only"] = True
        kwargs["async_req"] = True

        return await self.register_application10_applications_application_name_post_with_http_info_async(
            application_name, **kwargs
        )

    @overload
    def register_application10_applications_application_name_post_with_http_info(
        self, application_name: str, *, async_req: Literal[False] = False, **kwargs: Any
    ) -> tuple[Application, int, dict[str, str]]: ...

    @overload
    def register_application10_applications_application_name_post_with_http_info(
        self, application_name: str, *, async_req: Literal[True], **kwargs: Any
    ) -> Any: ...

    def register_application10_applications_application_name_post_with_http_info(
        self, application_name: str, **kwargs: Any
    ) -> tuple[Application, int, dict[str, str]] | Any:
        """Register an application with HTTP info.

        Args:
            application_name: Application name
            async_req: Whether to execute the request asynchronously
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Application object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_name is None:
            raise ApiValueError("Missing required parameter `application_name`")

        # Extract path parameters
        path_params = {
            "application_name": application_name,
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
            200: "Application",
            422: "HTTPValidationError",
        }

        # Make the request
        return self.api_client.call_api(
            "/1.0/applications/{application_name}",
            "POST",
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

    async def register_application10_applications_application_name_post_with_http_info_async(
        self, application_name: str, **kwargs: Any
    ) -> tuple[Application, int, dict[str, str]]:
        """Register an application with HTTP info asynchronously.

        Args:
            application_name: Application name
            _return_http_data_only: Response data without head status code and headers
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _request_auth: Request authentication

        Returns:
            Application object with HTTP info

        Raises:
            ApiException: If the request fails

        """
        # Validate parameters
        if self.api_client.client_side_validation and application_name is None:
            raise ApiValueError("Missing required parameter `application_name`")

        # Extract path parameters
        path_params = {
            "application_name": application_name,
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
            200: "Application",
            422: "HTTPValidationError",
        }

        # Make the request
        return await self.api_client.call_api_async(
            "/1.0/applications/{application_name}",
            "POST",
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
