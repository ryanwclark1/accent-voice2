# Copyright 2025 Accent Communications

"""Accent REST client library for API interactions.

This package provides a flexible, async-first HTTP client for interacting with
Accent Communications APIs. It includes both synchronous and asynchronous interfaces,
robust error handling, and customizable request options.
"""

from .command import HTTPCommand, RESTCommand
from .exceptions import (
    AccentAPIError,
    AuthenticationError,
    InvalidArgumentError,
    ResourceNotFoundError,
    ServerError,
)
from .models import ClientConfig, CommandResponse, JSONResponse, PaginatedResponse

__all__ = [
    "AccentAPIError",
    "AuthenticationError",
    "ClientConfig",
    "CommandResponse",
    "HTTPCommand",
    "InvalidArgumentError",
    "JSONResponse",
    "PaginatedResponse",
    "RESTCommand",
    "ResourceNotFoundError",
    "ServerError",
]
