# Copyright 2025 Accent Communications

"""Calld API client implementation.

This module provides the main client for interacting with the Accent Calld API.
"""

from __future__ import annotations

import logging

from accent_lib_rest_client.client import BaseClient

logger = logging.getLogger(__name__)


class CalldClient(BaseClient):
    """Client for interacting with the Accent Calld API.

    This client supports both synchronous and asynchronous operations.
    """

    namespace = "accent_calld_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/calld",
        version: str = "1.0",
        **kwargs,
    ) -> None:
        """Initialize a new Calld API client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments passed to BaseClient

        """
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
