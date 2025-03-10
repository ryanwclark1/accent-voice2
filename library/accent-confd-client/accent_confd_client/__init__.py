# Copyright 2025 Accent Communications

"""Accent Configuration Daemon client library.

This package provides a client for interacting with the Accent Configuration
Daemon API, with both synchronous and asynchronous interfaces.
"""

from accent_confd_client.client import ConfdClient

__all__ = [
    "ConfdClient",
]
