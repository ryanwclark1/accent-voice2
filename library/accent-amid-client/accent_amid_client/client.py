# Copyright 2025 Accent Communications

"""AMID API client implementation.

This module provides the main client class for interacting with the AMID API.
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from accent_lib_rest_client.client import BaseClient

logger = logging.getLogger(__name__)


class AmidClient(BaseClient):
    """Client for the AMID API.

    This client supports both synchronous and asynchronous operations.
    """

    namespace: ClassVar[str] = "accent_amid_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/amid",
        version: str = "1.0",
        **kwargs: Any,
    ) -> None:
        """Initialize a new AMID API client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments passed to BaseClient

        """
        logger.debug(
            "Initializing AMID client for %s:%s%s/%s", host, port, prefix, version
        )
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
