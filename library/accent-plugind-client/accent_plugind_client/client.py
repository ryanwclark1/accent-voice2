# Copyright 2025 Accent Communications

"""Accent Plugin Daemon client implementation.

This module provides the main client class for interacting with
the Accent Plugin Daemon API.
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from accent_lib_rest_client.client import BaseClient

# Configure logging
logger = logging.getLogger(__name__)


class PlugindClient(BaseClient):
    """Client for the Accent Plugin Daemon API.

    This client provides both synchronous and asynchronous interfaces
    for interacting with the Plugin Daemon API.
    """

    namespace: ClassVar[str] = "accent_plugind_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/plugind",
        version: str = "0.2",
        **kwargs: Any,
    ) -> None:
        """Initialize the Plugin Daemon client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments passed to the base client

        Raises:
            InvalidArgumentError: If required arguments are invalid

        """
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
        logger.debug(
            "Initialized PlugindClient for %s:%s%s/%s", host, port, prefix, version
        )
