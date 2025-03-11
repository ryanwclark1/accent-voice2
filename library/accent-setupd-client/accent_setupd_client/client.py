# Copyright 2025 Accent Communications

"""Setupd client implementation."""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from accent_lib_rest_client.client import BaseClient

logger = logging.getLogger(__name__)


class SetupdClient(BaseClient):
    """Client for interacting with the Setup Daemon API.

    This client provides methods for configuring and managing setup operations.
    """

    namespace: ClassVar[str] = "accent_setupd_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/setupd",
        version: str = "1.0",
        **kwargs: Any,
    ) -> None:
        """Initialize a new Setup Daemon client.

        Args:
            host: Hostname or IP of the setupd server
            port: Port number for the setupd server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments passed to BaseClient

        """
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
        logger.debug(
            "Initialized SetupdClient for %s:%s%s/%s",
            host,
            port,
            prefix,
            version,
        )
