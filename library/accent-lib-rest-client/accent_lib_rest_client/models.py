# Copyright 2025 Accent Communications

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ClientConfig(BaseModel):
    """Configuration model for API clients.

    Attributes:
        host: Hostname or IP of the server
        port: Port number for the server
        version: API version string
        token: Authentication token
        tenant_uuid: Tenant identifier
        https: Whether to use HTTPS
        timeout: Request timeout in seconds
        verify_certificate: Whether to verify SSL certificates
        prefix: URL prefix path
        user_agent: User agent string for requests
        max_retries: Maximum number of retries for requests
        retry_delay: Delay between retries in seconds

    """

    host: str
    port: int | None = None
    version: str = ""
    token: str | None = None
    tenant_uuid: str | None = None
    https: bool = True
    timeout: float = 10.0
    verify_certificate: bool | str = True
    prefix: str | None = None
    user_agent: str = ""
    max_retries: int = 3
    retry_delay: float = 1.0


class CommandResponse(BaseModel):
    """Standard response model for API command results.

    Attributes:
        content: Raw response content
        status_code: HTTP status code
        headers: Response headers
        response_time: Time taken for the request in seconds

    """

    content: bytes | str
    status_code: int
    headers: dict[str, str]
    response_time: float | None = None


class JSONResponse(BaseModel):
    """Model for JSON responses.

    Attributes:
        data: The parsed JSON data
        status_code: HTTP status code
        headers: Response headers
        response_time: Time taken for the request in seconds

    """

    data: Any
    status_code: int
    headers: dict[str, str]
    response_time: float | None = None


class PaginatedResponse(BaseModel):
    """Model for paginated responses.

    Attributes:
        items: List of items in the current page
        total: Total number of items
        page: Current page number
        per_page: Number of items per page
        pages: Total number of pages

    """

    items: list[Any]
    total: int
    page: int
    per_page: int
    pages: int


class ErrorDetail(BaseModel):
    """Model for detailed error information.

    Attributes:
        code: Error code
        message: Error message
        field: Optional field name for validation errors
        details: Optional additional error details

    """

    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """Model for API error responses.

    Attributes:
        message: Main error message
        errors: List of detailed errors
        status_code: HTTP status code
        timestamp: When the error occurred

    """

    message: str
    errors: list[ErrorDetail] = Field(default_factory=list)
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)
