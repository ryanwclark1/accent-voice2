# Copyright 2025 Accent Communications

"""Accent Deployd Client Library.

This package provides a client for interacting with the Accent Deployd service API,
supporting both synchronous and asynchronous operations with modern Python features.
"""

from accent_deployd_client.client import DeploydClient as Client
from accent_deployd_client.models import DeploydResponse

__all__ = [
    "Client",
    "DeploydResponse",
]
