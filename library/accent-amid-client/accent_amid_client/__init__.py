# Copyright 2025 Accent Communications

"""Accent AMID client for API interactions.

This package provides a client for interacting with the Accent AMID API,
supporting both synchronous and asynchronous operations.
"""

from accent_amid_client.client import AmidClient as Client
from accent_amid_client.models import AmidResponse

__all__ = [
    "Client",
    "AmidResponse",
]
