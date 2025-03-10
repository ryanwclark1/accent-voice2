# Copyright 2025 Accent Communications

"""Client module for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

from accent_lib_rest_client.client import BaseClient

logger = logging.getLogger(__name__)


class Client(BaseClient):
    """Client for interacting with the Call Log daemon API.

    Provides both synchronous and asynchronous interfaces for accessing
    call log services.
    """

    namespace = "accent_call_logd_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/call-logd",
        version: str = "1.0",
        **kwargs: Any,
    ) -> None:
        """Initialize a new Call Log daemon API client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server, defaults to 443
            prefix: URL prefix path, defaults to '/api/call-logd'
            version: API version string, defaults to '1.0'
            **kwargs: Additional arguments passed to BaseClient

        """
        logger.debug("Initializing Call Log daemon client for %s:%s", host, port)
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
