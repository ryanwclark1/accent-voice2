# Copyright 2025 Accent Communications

from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar, TypeVar, cast
from uuid import UUID

import httpx
from pydantic import BaseModel, ValidationError

from .client import BaseClient
from .exceptions import HTTPError, ResponseValidationError

T = TypeVar("T", bound=BaseModel)
ResponseType = TypeVar("ResponseType")


class HTTPCommand:
    """Base class for HTTP commands."""

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    @property
    def session(self) -> httpx.Client:
        return self._client.session()

    def validate_response(
        self, response: httpx.Response, model: type[T] | None = None
    ) -> Any:
        """Validate and parse response data.

        Args:
            response: HTTP response to validate
            model: Optional Pydantic model to validate against

        Returns:
            Validated response data

        Raises:
            HTTPError: For HTTP-level errors
            ResponseValidationError: For validation errors
        """
        try:
            response.raise_for_status()
            data = response.json()

            if model is not None:
                try:
                    return model.model_validate(data)
                except ValidationError as e:
                    raise ResponseValidationError(e) from e

            return data

        except httpx.HTTPStatusError as e:
            raise HTTPError(e.response) from e


class RESTCommand(HTTPCommand, metaclass=ABCMeta):
    """Base class for REST commands with validation."""

    _headers: ClassVar[dict[str, str]] = {"Accept": "application/json"}

    @property
    @abstractmethod
    def resource(self) -> str:
        """Resource endpoint for this command."""
        pass

    def __init__(self, client: BaseClient) -> None:
        super().__init__(client)
        self.base_url = self._client.url(self.resource)
        self.timeout = self._client.timeout

    def _get_headers(
        self, tenant_uuid: UUID | str | None = None, **kwargs: str
    ) -> dict[str, str]:
        """Build headers for the request.

        Args:
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional header values

        Returns:
            Complete headers dictionary
        """
        headers = dict(self._headers)

        if tenant_uuid:
            headers["Accent-Tenant"] = str(tenant_uuid)

        headers.update(kwargs)
        return headers

    def get(
        self, *path_segments: str, response_model: type[T] | None = None, **kwargs: Any
    ) -> Any:
        """Perform GET request.

        Args:
            *path_segments: URL path segments to append
            response_model: Optional response validation model
            **kwargs: Additional request parameters (e.g., headers, params)

        Returns:
            Validated response data
        """
        url = self._client.url(self.resource, *path_segments)
        return self.handle_request("GET", url, response_model, **kwargs)

    def post(
        self, *path_segments: str, response_model: type[T] | None = None, **kwargs: Any
    ) -> Any:
        """Perform POST request.

        Args:
            *path_segments: URL path segments to append
            response_model: Optional response validation model
            **kwargs: Additional request parameters (e.g., headers, json, data)

        Returns:
            Validated response data
        """
        url = self._client.url(self.resource, *path_segments)
        return self.handle_request("POST", url, response_model, **kwargs)

    def put(
        self, *path_segments: str, response_model: type[T] | None = None, **kwargs: Any
    ) -> Any:
        """Perform PUT request.

        Args:
            *path_segments: URL path segments to append
            response_model: Optional response validation model
            **kwargs: Additional request parameters (e.g., headers, data)

        Returns:
            Validated response data
        """
        url = self._client.url(self.resource, *path_segments)
        return self.handle_request("PUT", url, response_model, **kwargs)

    def delete(
        self, *path_segments: str, response_model: type[T] | None = None, **kwargs: Any
    ) -> Any:
        """Perform DELETE request.

        Args:
            *path_segments: URL path segments to append
            response_model: Optional response validation model
            **kwargs: Additional request parameters (e.g., headers)

        Returns:
            Validated response data
        """
        url = self._client.url(self.resource, *path_segments)
        return self.handle_request("DELETE", url, response_model, **kwargs)

    def handle_request(
        self,
        method: str,
        url: str,
        response_model: type[T] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Handle the HTTP request and response validation.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: Full URL for the request
            response_model: Optional Pydantic model for response validation
            **kwargs:  Additional keyword arguments passed to httpx.request

        Returns:
            Validated response data, or None if no response body

        Raises:
            HTTPError: If the HTTP request fails
            ResponseValidationError: If response validation fails.
        """
        headers = kwargs.pop("headers", {})  # Extract headers, default to empty dict
        merged_headers = self._get_headers(**headers)
        with self.session as client:
            response = client.request(method, url, headers=merged_headers, **kwargs)
            return self.validate_response(response, response_model)
