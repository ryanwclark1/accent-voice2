# Copyright 2025 Accent Communications
"""API client for the Accent applicationd client.
"""

from __future__ import annotations

import asyncio
import json
import logging
import mimetypes
import os
from datetime import date, datetime
from typing import Any, TypeVar

import httpx

from accent_applicationd_client.configuration import Configuration
from accent_applicationd_client.exceptions import (
    ApiException,
    ApiValueError,
    handle_http_error,
)

T = TypeVar("T")
logger = logging.getLogger(__name__)

class ApiClient:
    """Generic API client for OpenAPI client library builds.

    This client handles client-server communication and is invariant
    across implementations.

    Attributes:
        configuration: Client configuration
        default_headers: Default headers for requests
        user_agent: User agent for requests
        cookie: Cookie for requests
        client_side_validation: Whether to validate parameters client-side

    """

    # Types that don't require special handling when serializing
    PRIMITIVE_TYPES = (float, bool, bytes, str, int)

    # Mapping of Python types to the types used in the API
    NATIVE_TYPES_MAPPING = {
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "date": date,
        "datetime": datetime,
        "object": object,
    }

    def __init__(
        self,
        configuration: Configuration | None = None,
        header_name: str | None = None,
        header_value: str | None = None,
        cookie: str | None = None,
    ) -> None:
        """Initialize API client.

        Args:
            configuration: Client configuration
            header_name: Header name to add to all requests
            header_value: Header value to add to all requests
            cookie: Cookie to add to all requests

        """
        if configuration is None:
            configuration = Configuration.get_default_copy()
        self.configuration = configuration

        # Default attributes
        self.default_headers: dict[str, str] = {}
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie

        # Default User-Agent
        self.user_agent = "OpenAPI-Generator/2.0.0/python"
        self.client_side_validation = configuration.client_side_validation

        # HTTP Clients
        self._sync_client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    def __enter__(self) -> ApiClient:
        """Enter the context manager.

        Returns:
            The client instance

        """
        return self

    def __exit__(self, exc_type: type[Exception] | None, exc_val: Exception | None, exc_tb: Any) -> None:
        """Exit the context manager, closing resources.

        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised

        """
        self.close()

    def close(self) -> None:
        """Close the client, releasing resources."""
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None

        if self._async_client:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self._close_async_client())
                else:
                    loop.run_until_complete(self._close_async_client())
            except RuntimeError:
                # No event loop or event loop is closed
                pass

    async def _close_async_client(self) -> None:
        """Close the async client safely."""
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

    @property
    def sync_client(self) -> httpx.Client:
        """Get the synchronous HTTP client.

        Returns:
            httpx.Client: Configured HTTP client

        """
        if self._sync_client is None:
            # Configure transport options
            limits = httpx.Limits(
                max_connections=self.configuration.connection_pool_maxsize
            )

            # Configure timeout
            timeout = httpx.Timeout(self.configuration.settings.timeout)

            # Configure client
            self._sync_client = httpx.Client(
                limits=limits,
                timeout=timeout,
                verify=self.configuration.verify_ssl,
                cert=self._get_cert_config(),
                proxies=self.configuration.proxy,
                trust_env=True,
            )

        return self._sync_client

    @property
    def async_client(self) -> httpx.AsyncClient:
        """Get the asynchronous HTTP client.

        Returns:
            httpx.AsyncClient: Configured async HTTP client

        """
        if self._async_client is None:
            # Configure transport options
            limits = httpx.Limits(
                max_connections=self.configuration.connection_pool_maxsize
            )

            # Configure timeout
            timeout = httpx.Timeout(self.configuration.settings.timeout)

            # Configure client
            self._async_client = httpx.AsyncClient(
                limits=limits,
                timeout=timeout,
                verify=self.configuration.verify_ssl,
                cert=self._get_cert_config(),
                proxies=self.configuration.proxy,
                trust_env=True,
            )

        return self._async_client

    def _get_cert_config(self) -> tuple[str, str] | str | None:
        """Get certificate configuration.

        Returns:
            Certificate configuration tuple or string

        """
        if self.configuration.cert_file and self.configuration.key_file:
            return (self.configuration.cert_file, self.configuration.key_file)
        if self.configuration.cert_file:
            return self.configuration.cert_file
        return None

    @property
    def user_agent(self) -> str:
        """Get the User-Agent header.

        Returns:
            User-Agent header value

        """
        return self.default_headers.get("User-Agent", "")

    @user_agent.setter
    def user_agent(self, value: str) -> None:
        """Set the User-Agent header.

        Args:
            value: User-Agent header value

        """
        self.default_headers["User-Agent"] = value

    def set_default_header(self, header_name: str, header_value: str) -> None:
        """Set a default header.

        Args:
            header_name: Header name
            header_value: Header value

        """
        self.default_headers[header_name] = header_value

    def sanitize_for_serialization(self, obj: Any) -> Any:
        """Build a JSON serializable object.

        Args:
            obj: The object to serialize

        Returns:
            JSON serializable version of the object

        """
        if obj is None:
            return None
        if isinstance(obj, self.PRIMITIVE_TYPES):
            return obj
        if isinstance(obj, list):
            return [self.sanitize_for_serialization(sub_obj) for sub_obj in obj]
        if isinstance(obj, tuple):
            return tuple(self.sanitize_for_serialization(sub_obj) for sub_obj in obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        if isinstance(obj, dict):
            obj_dict = obj
        # Convert model obj to dict using attribute map
        # to convert attribute names to JSON keys
        elif hasattr(obj, "attribute_map") and hasattr(obj, "openapi_types"):
            obj_dict = {
                obj.attribute_map[attr]: getattr(obj, attr)
                for attr, _ in obj.openapi_types.items()
                if getattr(obj, attr) is not None
            }
        elif hasattr(obj, "model_dump"):
            # If it's a Pydantic model, use model_dump
            return obj.model_dump(mode="json", exclude_none=True)
        else:
            obj_dict = obj.__dict__

        return {key: self.sanitize_for_serialization(val) for key, val in obj_dict.items()}

    def deserialize(self, response: httpx.Response, response_type: str | type[T] | None) -> Any:
        """Deserialize a response into an object.

        Args:
            response: HTTP response
            response_type: The class to deserialize into

        Returns:
            Deserialized object

        """
        # Handle file downloading
        if response_type == "file":
            return self.__deserialize_file(response)

        try:
            data = response.json()
        except ValueError:
            data = response.text

        return self.__deserialize(data, response_type)

    def __deserialize(self, data: Any, klass: str | type[T] | None) -> Any:
        """Deserialize data into an object of the specified class.

        Args:
            data: The data to deserialize
            klass: The class to deserialize into

        Returns:
            Deserialized object

        """
        if data is None:
            return None

        if isinstance(klass, str):
            if klass.startswith("list["):
                sub_kls = klass[5:-1]
                return [self.__deserialize(sub_data, sub_kls) for sub_data in data]

            if klass.startswith("dict("):
                sub_kls = klass[5:-1].split(", ")[1]
                return {k: self.__deserialize(v, sub_kls) for k, v in data.items()}

            # convert str to class
            if klass in self.NATIVE_TYPES_MAPPING:
                klass = self.NATIVE_TYPES_MAPPING[klass]
            else:
                # Import the class from the models package
                import importlib
                module = importlib.import_module("accent_applicationd_client.models")
                klass = getattr(module, klass)

        if klass in self.PRIMITIVE_TYPES:
            return self.__deserialize_primitive(data, klass)
        if klass == object:
            return self.__deserialize_object(data)
        if klass == date:
            return self.__deserialize_date(data)
        if klass == datetime:
            return self.__deserialize_datetime(data)
        return self.__deserialize_model(data, klass)

    def __deserialize_file(self, response: httpx.Response) -> str:
        """Deserialize response body to a file.

        Args:
            response: HTTP response

        Returns:
            Path to the saved file

        """
        import tempfile

        fd, path = tempfile.mkstemp(dir=self.configuration.temp_folder_path)
        os.close(fd)
        os.remove(path)

        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            import re
            filename_match = re.search(r'filename=[\'"]?([^\'"\s]+)[\'"]?',
                                      content_disposition)
            if filename_match:
                filename = filename_match.group(1)
                path = os.path.join(os.path.dirname(path), filename)

        with open(path, "wb") as f:
            f.write(response.content)

        return path

    def __deserialize_primitive(self, data: Any, klass: type) -> Any:
        """Deserialize a primitive type.

        Args:
            data: The data to deserialize
            klass: The class to deserialize into

        Returns:
            Deserialized primitive

        """
        try:
            return klass(data)
        except UnicodeEncodeError:
            return str(data)
        except TypeError:
            return data

    def __deserialize_object(self, value: Any) -> Any:
        """Return the object itself.

        Args:
            value: The object

        Returns:
            The object itself

        """
        return value

    def __deserialize_date(self, string: str) -> date | str:
        """Deserialize string to date.

        Args:
            string: String to deserialize

        Returns:
            Date object or string if parsing fails

        Raises:
            ApiException: If date parsing fails

        """
        try:
            from dateutil.parser import parse
            return parse(string).date()
        except ImportError:
            return string
        except ValueError as e:
            raise ApiException(
                status=0,
                reason=f"Failed to parse `{string}` as date object: {e!s}"
            )

    def __deserialize_datetime(self, string: str) -> datetime | str:
        """Deserialize string to datetime.

        Args:
            string: String to deserialize

        Returns:
            Datetime object or string if parsing fails

        Raises:
            ApiException: If datetime parsing fails

        """
        try:
            from dateutil.parser import parse
            return parse(string)
        except ImportError:
            return string
        except ValueError as e:
            raise ApiException(
                status=0,
                reason=f"Failed to parse `{string}` as datetime object: {e!s}"
            )

    def __deserialize_model(self, data: Any, klass: type[T]) -> T | Any:
        """Deserialize data into model instance.

        Args:
            data: The data to deserialize
            klass: The model class

        Returns:
            Model instance

        """
        if not klass.openapi_types:
            return data

        if not data:
            return None

        # If it's a Pydantic model
        if hasattr(klass, "model_validate"):
            return klass.model_validate(data)

        # Fall back to mapping fields manually
        kwargs: dict[str, Any] = {}

        if hasattr(klass, "openapi_types") and hasattr(klass, "attribute_map"):
            for attr, attr_type in klass.openapi_types.items():
                if klass.attribute_map[attr] in data:
                    value = data[klass.attribute_map[attr]]
                    kwargs[attr] = self.__deserialize(value, attr_type)

        return klass(**kwargs)

    def call_api(
        self,
        resource_path: str,
        method: str,
        path_params: dict[str, Any] | None = None,
        query_params: list[tuple[str, str]] | None = None,
        header_params: dict[str, str] | None = None,
        body: Any = None,
        post_params: list[tuple[str, str]] | None = None,
        files: dict[str, str] | None = None,
        response_type: str | type[T] | None = None,
        auth_settings: list[str] | None = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        collection_formats: dict[str, str] | None = None,
        _preload_content: bool = True,
        _request_timeout: float | tuple[float, float] | None = None,
        _host: str | None = None,
        _request_auth: dict[str, str] | None = None
    ) -> T | tuple[T, int, dict[str, str]] | httpx.Response:
        """Make the HTTP request and return deserialized data.

        Args:
            resource_path: Path to the resource
            method: HTTP method
            path_params: Path parameters
            query_params: Query parameters
            header_params: Header parameters
            body: Request body
            post_params: Form parameters
            files: Files to upload
            response_type: Response type
            auth_settings: Authentication settings
            async_req: Whether to execute asynchronously
            _return_http_data_only: Whether to return only data
            collection_formats: Collection formats
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _host: Host override
            _request_auth: Authentication override

        Returns:
            Deserialized data or response

        Raises:
            ApiException: If API call fails

        """
        # If async_req is set, execute async and return a future
        if async_req:
            loop = asyncio.get_event_loop()
            return loop.create_task(
                self.call_api_async(
                    resource_path, method, path_params, query_params, header_params,
                    body, post_params, files, response_type, auth_settings,
                    _return_http_data_only, collection_formats, _preload_content,
                    _request_timeout, _host, _request_auth
                )
            )

        # Execute synchronously
        return self._call_api_sync(
            resource_path, method, path_params, query_params, header_params,
            body, post_params, files, response_type, auth_settings,
            _return_http_data_only, collection_formats, _preload_content,
            _request_timeout, _host, _request_auth
        )

    async def call_api_async(
        self,
        resource_path: str,
        method: str,
        path_params: dict[str, Any] | None = None,
        query_params: list[tuple[str, str]] | None = None,
        header_params: dict[str, str] | None = None,
        body: Any = None,
        post_params: list[tuple[str, str]] | None = None,
        files: dict[str, str] | None = None,
        response_type: str | type[T] | None = None,
        auth_settings: list[str] | None = None,
        _return_http_data_only: bool = True,
        collection_formats: dict[str, str] | None = None,
        _preload_content: bool = True,
        _request_timeout: float | tuple[float, float] | None = None,
        _host: str | None = None,
        _request_auth: dict[str, str] | None = None
    ) -> T | tuple[T, int, dict[str, str]] | httpx.Response:
        """Make the HTTP request asynchronously.

        Args:
            resource_path: Path to the resource
            method: HTTP method
            path_params: Path parameters
            query_params: Query parameters
            header_params: Header parameters
            body: Request body
            post_params: Form parameters
            files: Files to upload
            response_type: Response type
            auth_settings: Authentication settings
            _return_http_data_only: Whether to return only data
            collection_formats: Collection formats
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _host: Host override
            _request_auth: Authentication override

        Returns:
            Deserialized data or response

        Raises:
            ApiException: If API call fails

        """
        try:
            return await self._call_api_async(
                resource_path, method, path_params, query_params, header_params,
                body, post_params, files, response_type, auth_settings,
                _return_http_data_only, collection_formats, _preload_content,
                _request_timeout, _host, _request_auth
            )
        except Exception as e:
            if isinstance(e, httpx.HTTPStatusError):
                handle_http_error(e)
            raise

    def _call_api_sync(
        self,
        resource_path: str,
        method: str,
        path_params: dict[str, Any] | None = None,
        query_params: list[tuple[str, str]] | None = None,
        header_params: dict[str, str] | None = None,
        body: Any = None,
        post_params: list[tuple[str, str]] | None = None,
        files: dict[str, str] | None = None,
        response_type: str | type[T] | None = None,
        auth_settings: list[str] | None = None,
        _return_http_data_only: bool = True,
        collection_formats: dict[str, str] | None = None,
        _preload_content: bool = True,
        _request_timeout: float | tuple[float, float] | None = None,
        _host: str | None = None,
        _request_auth: dict[str, str] | None = None
    ) -> T | tuple[T, int, dict[str, str]] | httpx.Response:
        """Make the HTTP request synchronously.

        Args:
            resource_path: Path to the resource
            method: HTTP method
            path_params: Path parameters
            query_params: Query parameters
            header_params: Header parameters
            body: Request body
            post_params: Form parameters
            files: Files to upload
            response_type: Response type
            auth_settings: Authentication settings
            _return_http_data_only: Whether to return only data
            collection_formats: Collection formats
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _host: Host override
            _request_auth: Authentication override

        Returns:
            Deserialized data or response

        Raises:
            ApiException: If API call fails

        """
        try:
            response_data = self._request_sync(
                method, resource_path, path_params, query_params, header_params,
                body, post_params, files, auth_settings, collection_formats,
                _preload_content, _request_timeout, _host, _request_auth
            )

            if not _preload_content:
                return response_data

            return_data = self.deserialize(response_data, response_type)

            if _return_http_data_only:
                return return_data

            return (return_data, response_data.status_code, dict(response_data.headers))
        except httpx.HTTPStatusError as e:
            handle_http_error(e)

    async def _call_api_async(
        self,
        resource_path: str,
        method: str,
        path_params: dict[str, Any] | None = None,
        query_params: list[tuple[str, str]] | None = None,
        header_params: dict[str, str] | None = None,
        body: Any = None,
        post_params: list[tuple[str, str]] | None = None,
        files: dict[str, str] | None = None,
        response_type: str | type[T] | None = None,
        auth_settings: list[str] | None = None,
        _return_http_data_only: bool = True,
        collection_formats: dict[str, str] | None = None,
        _preload_content: bool = True,
        _request_timeout: float | tuple[float, float] | None = None,
        _host: str | None = None,
        _request_auth: dict[str, str] | None = None
    ) -> T | tuple[T, int, dict[str, str]] | httpx.Response:
        """Make the HTTP request asynchronously.

        Args:
            resource_path: Path to the resource
            method: HTTP method
            path_params: Path parameters
            query_params: Query parameters
            header_params: Header parameters
            body: Request body
            post_params: Form parameters
            files: Files to upload
            response_type: Response type
            auth_settings: Authentication settings
            _return_http_data_only: Whether to return only data
            collection_formats: Collection formats
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _host: Host override
            _request_auth: Authentication override

        Returns:
            Deserialized data or response

        Raises:
            ApiException: If API call fails

        """
        response_data = await self._request_async(
            method, resource_path, path_params, query_params, header_params,
            body, post_params, files, auth_settings, collection_formats,
            _preload_content, _request_timeout, _host, _request_auth
        )

        if not _preload_content:
            return response_data

        return_data = self.deserialize(response_data, response_type)

        if _return_http_data_only:
            return return_data

        return (return_data, response_data.status_code, dict(response_data.headers))

    def _request_sync(
        self,
        method: str,
        url: str,
        path_params: dict[str, Any] | None = None,
        query_params: list[tuple[str, str]] | None = None,
        header_params: dict[str, str] | None = None,
        body: Any = None,
        post_params: list[tuple[str, str]] | None = None,
        files: dict[str, str] | None = None,
        auth_settings: list[str] | None = None,
        collection_formats: dict[str, str] | None = None,
        _preload_content: bool = True,
        _request_timeout: float | tuple[float, float] | None = None,
        _host: str | None = None,
        _request_auth: dict[str, str] | None = None
    ) -> httpx.Response:
        """Make a synchronous HTTP request.

        Args:
            method: HTTP method
            url: URL for the request
            path_params: Path parameters
            query_params: Query parameters
            header_params: Header parameters
            body: Request body
            post_params: Form parameters
            files: Files to upload
            auth_settings: Authentication settings
            collection_formats: Collection formats
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _host: Host override
            _request_auth: Authentication override

        Returns:
            HTTP response

        Raises:
            ApiException: If request fails

        """
        # Set request URL
        url = self._build_url(url, path_params, _host)

        # Prepare headers
        headers = self._prepare_headers(header_params)

        # Prepare request data
        data, files_data = self._prepare_request_data(post_params, files)

        # Prepare request body
        request_body = self._prepare_request_body(body, headers)

        # Apply authentication settings
        self._apply_auth_settings(headers, query_params, auth_settings, _request_auth)

        # Send the request
        try:
            return self._execute_request_sync(
                method, url, query_params, headers,
                data, files_data, request_body, _request_timeout
            )
        except httpx.RequestError as e:
            raise ApiException(
                status=0,
                reason=f"Connection error: {e!s}"
            ) from e

    async def _request_async(
        self,
        method: str,
        url: str,
        path_params: dict[str, Any] | None = None,
        query_params: list[tuple[str, str]] | None = None,
        header_params: dict[str, str] | None = None,
        body: Any = None,
        post_params: list[tuple[str, str]] | None = None,
        files: dict[str, str] | None = None,
        auth_settings: list[str] | None = None,
        collection_formats: dict[str, str] | None = None,
        _preload_content: bool = True,
        _request_timeout: float | tuple[float, float] | None = None,
        _host: str | None = None,
        _request_auth: dict[str, str] | None = None
    ) -> httpx.Response:
        """Make an asynchronous HTTP request.

        Args:
            method: HTTP method
            url: URL for the request
            path_params: Path parameters
            query_params: Query parameters
            header_params: Header parameters
            body: Request body
            post_params: Form parameters
            files: Files to upload
            auth_settings: Authentication settings
            collection_formats: Collection formats
            _preload_content: Whether to preload content
            _request_timeout: Request timeout
            _host: Host override
            _request_auth: Authentication override

        Returns:
            HTTP response

        Raises:
            ApiException: If request fails

        """
        # Set request URL
        url = self._build_url(url, path_params, _host)

        # Prepare headers
        headers = self._prepare_headers(header_params)

        # Prepare request data
        data, files_data = self._prepare_request_data(post_params, files)

        # Prepare request body
        request_body = self._prepare_request_body(body, headers)

        # Apply authentication settings
        self._apply_auth_settings(headers, query_params, auth_settings, _request_auth)

        # Send the request
        try:
            return await self._execute_request_async(
                method, url, query_params, headers,
                data, files_data, request_body, _request_timeout
            )
        except httpx.RequestError as e:
            raise ApiException(
                status=0,
                reason=f"Connection error: {e!s}"
            ) from e

    def _build_url(
        self,
        url: str,
        path_params: dict[str, Any] | None = None,
        _host: str | None = None
    ) -> str:
        """Build the URL for the request.

        Args:
            url: Base URL
            path_params: Path parameters
            _host: Host override

        Returns:
            Complete URL

        """
        # Apply path parameters if provided
        if path_params:
            for k, v in path_params.items():
                replacement = self._quote_path_param(v)
                url = url.replace(
                    f"{{{k}}}",
                    replacement
                )

        # Use host override if provided
        if _host:
            url = _host + url
        elif not url.startswith("http"):
            url = self.configuration.host + url

        return url

    def _quote_path_param(self, param: Any) -> str:
        """Quote a path parameter.

        Args:
            param: Parameter to quote

        Returns:
            Quoted parameter string

        """
        import urllib.parse
        if isinstance(param, (int, float, bool)):
            return str(param)
        return urllib.parse.quote(str(param), safe=self.configuration.safe_chars_for_path_param)

    def _prepare_headers(self, header_params: dict[str, str] | None = None) -> dict[str, str]:
        """Prepare request headers.

        Args:
            header_params: Additional headers

        Returns:
            Complete headers dictionary

        """
        headers = dict(self.default_headers)

        if header_params:
            headers.update(header_params)

        if self.cookie:
            headers["Cookie"] = self.cookie

        # Add custom User-Agent if not already set
        if "User-Agent" not in headers:
            headers["User-Agent"] = self.user_agent

        return headers

    def _prepare_request_data(
        self,
        post_params: list[tuple[str, str]] | None = None,
        files: dict[str, str] | None = None
    ) -> tuple[list[tuple[str, str]] | None, dict[str, tuple[str, bytes, str]] | None]:
        """Prepare request form data and files.

        Args:
            post_params: Form parameters
            files: Files to upload

        Returns:
            Tuple of form data and files dict

        """
        data = post_params if post_params else None
        files_data = None

        if files:
            files_data = {}
            for k, file_path in files.items():
                if not file_path:
                    continue

                with open(file_path, "rb") as f:
                    filename = os.path.basename(f.name)
                    filedata = f.read()
                    mimetype = (mimetypes.guess_type(filename)[0]
                               or "application/octet-stream")
                    files_data[k] = (filename, filedata, mimetype)

        return data, files_data

    def _prepare_request_body(self, body: Any, headers: dict[str, str]) -> bytes | str | None:
        """Prepare request body.

        Args:
            body: Request body
            headers: Request headers

        Returns:
            Serialized request body

        """
        if body is None:
            return None

        content_type = headers.get("Content-Type", "")

        # For JSON content type, serialize body
        if "application/json" in content_type.lower():
            return json.dumps(self.sanitize_for_serialization(body))

        # For string content type, return body as is
        if isinstance(body, (str, bytes)):
            return body

        # For other content types, default to JSON
        return json.dumps(self.sanitize_for_serialization(body))

    def _apply_auth_settings(
        self,
        headers: dict[str, str],
        query_params: list[tuple[str, str]] | None,
        auth_settings: list[str] | None = None,
        _request_auth: dict[str, str] | None = None
    ) -> None:
        """Apply authentication settings.

        Args:
            headers: Request headers
            query_params: Query parameters
            auth_settings: Authentication settings
            _request_auth: Authentication override

        """
        if not auth_settings:
            return

        query_params = query_params or []

        # Apply authentication override if provided
        if _request_auth:
            self._apply_auth(headers, query_params, _request_auth)
            return

        # Apply configured authentication settings
        for auth in auth_settings:
            auth_setting = self.configuration.auth_settings().get(auth)
            if auth_setting:
                self._apply_auth(headers, query_params, auth_setting)

    def _apply_auth(
        self,
        headers: dict[str, str],
        query_params: list[tuple[str, str]],
        auth_setting: dict[str, Any]
    ) -> None:
        """Apply authentication setting.

        Args:
            headers: Request headers
            query_params: Query parameters
            auth_setting: Authentication setting

        """
        if auth_setting["in"] == "cookie":
            headers["Cookie"] = auth_setting["value"]
        elif auth_setting["in"] == "header":
            headers[auth_setting["key"]] = auth_setting["value"]
        elif auth_setting["in"] == "query":
            query_params.append((auth_setting["key"], auth_setting["value"]))
        else:
            raise ApiValueError(
                "Authentication token must be in `query` or `header`"
            )

    def _execute_request_sync(
        self,
        method: str,
        url: str,
        query_params: list[tuple[str, str]] | None,
        headers: dict[str, str],
        data: list[tuple[str, str]] | None,
        files: dict[str, tuple[str, bytes, str]] | None,
        body: bytes | str | None,
        _request_timeout: float | tuple[float, float] | None
    ) -> httpx.Response:
        """Execute a synchronous HTTP request.

        Args:
            method: HTTP method
            url: URL for the request
            query_params: Query parameters
            headers: Request headers
            data: Form data
            files: Files to upload
            body: Request body
            _request_timeout: Request timeout

        Returns:
            HTTP response

        Raises:
            ApiException: If request fails

        """
        # Set query parameters
        params = []
        if query_params:
            params = query_params

        # Set timeout
        timeout = _request_timeout or self.configuration.settings.timeout

        # Execute the appropriate HTTP method
        if method == "GET":
            response = self.sync_client.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                follow_redirects=True
            )
            response.raise_for_status()
            return response

        if method == "HEAD":
            response = self.sync_client.head(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                follow_redirects=True
            )
            response.raise_for_status()
            return response

        if method == "OPTIONS":
            response = self.sync_client.options(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                follow_redirects=True
            )
            response.raise_for_status()
            return response

        if method == "POST":
            response = self.sync_client.post(
                url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                json=None if body is None else json.loads(body) if isinstance(body, str) else body,
                timeout=timeout,
                follow_redirects=True
            )
            response.raise_for_status()
            return response

        if method == "PUT":
            response = self.sync_client.put(
                url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                json=None
                if body is None
                else json.loads(body)
                if isinstance(body, str)
                else body,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "PATCH":
            response = self.sync_client.patch(
                url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                json=None
                if body is None
                else json.loads(body)
                if isinstance(body, str)
                else body,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "DELETE":
            response = self.sync_client.delete(
                url,
                params=params,
                headers=headers,
                data=data,
                json=None
                if body is None
                else json.loads(body)
                if isinstance(body, str)
                else body,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        raise ApiValueError(
            "HTTP method must be `GET`, `HEAD`, `OPTIONS`, "
            "`POST`, `PATCH`, `PUT` or `DELETE`."
        )

    async def _execute_request_async(
        self,
        method: str,
        url: str,
        query_params: list[tuple[str, str]] | None,
        headers: dict[str, str],
        data: list[tuple[str, str]] | None,
        files: dict[str, tuple[str, bytes, str]] | None,
        body: bytes | str | None,
        _request_timeout: float | tuple[float, float] | None,
    ) -> httpx.Response:
        """Execute an asynchronous HTTP request.

        Args:
            method: HTTP method
            url: URL for the request
            query_params: Query parameters
            headers: Request headers
            data: Form data
            files: Files to upload
            body: Request body
            _request_timeout: Request timeout

        Returns:
            HTTP response

        Raises:
            ApiException: If request fails

        """
        # Set query parameters
        params = []
        if query_params:
            params = query_params

        # Set timeout
        timeout = _request_timeout or self.configuration.settings.timeout

        # Execute the appropriate HTTP method
        if method == "GET":
            response = await self.async_client.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "HEAD":
            response = await self.async_client.head(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "OPTIONS":
            response = await self.async_client.options(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "POST":
            response = await self.async_client.post(
                url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                json=None
                if body is None
                else json.loads(body)
                if isinstance(body, str)
                else body,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "PUT":
            response = await self.async_client.put(
                url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                json=None
                if body is None
                else json.loads(body)
                if isinstance(body, str)
                else body,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "PATCH":
            response = await self.async_client.patch(
                url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                json=None
                if body is None
                else json.loads(body)
                if isinstance(body, str)
                else body,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        if method == "DELETE":
            response = await self.async_client.delete(
                url,
                params=params,
                headers=headers,
                data=data,
                json=None
                if body is None
                else json.loads(body)
                if isinstance(body, str)
                else body,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response

        raise ApiValueError(
            "HTTP method must be `GET`, `HEAD`, `OPTIONS`, "
            "`POST`, `PATCH`, `PUT` or `DELETE`."
        )

    def parameters_to_tuples(
        self,
        params: dict[str, Any] | list[tuple[str, Any]],
        collection_formats: dict[str, str] | None = None,
    ) -> list[tuple[str, str]]:
        """Convert parameters to list of tuples.

        Args:
            params: Parameters as dict or list of tuples
            collection_formats: Collection format information

        Returns:
            List of parameter tuples

        """
        collection_formats = collection_formats or {}
        new_params: list[tuple[str, str]] = []

        if isinstance(params, dict):
            for k, v in params.items():
                if k in collection_formats:
                    collection_format = collection_formats[k]
                    if collection_format == "multi":
                        new_params.extend((k, value) for value in v)
                    else:
                        if collection_format == "ssv":
                            delimiter = " "
                        elif collection_format == "tsv":
                            delimiter = "\t"
                        elif collection_format == "pipes":
                            delimiter = "|"
                        else:  # csv is the default
                            delimiter = ","
                        new_params.append(
                            (k, delimiter.join(str(value) for value in v))
                        )
                else:
                    new_params.append((k, v))
        else:
            # It's already a list of tuples
            new_params = params

        return new_params

    def select_header_accept(self, accepts: list[str] | None) -> str | None:
        """Return 'Accept' based on an array of accepts provided.

        Args:
            accepts: List of acceptable media types

        Returns:
            The Accept header value or None if no accepts

        """
        if not accepts:
            return None

        accepts = [x.lower() for x in accepts]

        if "application/json" in accepts:
            return "application/json"
        return ", ".join(accepts)

    def select_header_content_type(self, content_types: list[str] | None) -> str:
        """Return 'Content-Type' based on an array of content_types provided.

        Args:
            content_types: List of content types

        Returns:
            The Content-Type header value

        """
        if not content_types:
            return "application/json"

        content_types = [x.lower() for x in content_types]

        if "application/json" in content_types or "*/*" in content_types:
            return "application/json"
        return content_types[0]
