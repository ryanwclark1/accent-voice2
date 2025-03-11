# Copyright 2025 Accent Communications
"""Accent applicationd client

Client library for interacting with the Accent applicationd API.

This version has been updated to use HTTPX for both synchronous and
asynchronous HTTP requests, with full type hinting and Pydantic models.
"""

from __future__ import annotations

__version__ = "1.0.0"

# Import APIs
from accent_applicationd_client.api.application_api import ApplicationApi
from accent_applicationd_client.api.status_api import StatusApi

# Import ApiClient
from accent_applicationd_client.api_client import ApiClient
from accent_applicationd_client.configuration import Configuration

# Import exceptions
from accent_applicationd_client.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    OpenApiException,
)

# Import models
from accent_applicationd_client.models.application import Application
from accent_applicationd_client.models.http_validation_error import HTTPValidationError
from accent_applicationd_client.models.node import Node
from accent_applicationd_client.models.status import Status
from accent_applicationd_client.models.validation_error import ValidationError

__all__ = [
    # APIs
    "ApplicationApi",
    "StatusApi",
    # Client and Configuration
    "ApiClient",
    "Configuration",
    # Exceptions
    "ApiAttributeError",
    "ApiException",
    "ApiKeyError",
    "ApiTypeError",
    "ApiValueError",
    "OpenApiException",
    # Models
    "Application",
    "HTTPValidationError",
    "Node",
    "Status",
    "ValidationError",
    # Version
    "__version__",
]
