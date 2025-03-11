# Copyright 2025 Accent Communications

"""Client implementation for the Accent Market API.

This module provides the main client class for interacting with
the Accent Market API.
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from accent_lib_rest_client.client import BaseClient

# Configure logging
logger = logging.getLogger(__name__)


class Client(BaseClient):
    """Client for interacting with the Accent Market API.

    This client extends the BaseClient to provide specific functionality
    for the Accent Market API.
    """

    namespace: ClassVar[str] = "accent_market_client.commands"

    def __init__(
        self,
        host: str = "apps.accentvoice.io",
        port: int | None = None,
        version: str = "v1",
        https: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a new Accent Market API client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server
            version: API version string
            https: Whether to use HTTPS
            **kwargs: Additional arguments to pass to the BaseClient

        """
        logger.debug(
            "Initializing Accent Market client for %s://%s",
            "https" if https else "http",
            host,
        )
        super().__init__(host=host, port=port, version=version, https=https, **kwargs)
