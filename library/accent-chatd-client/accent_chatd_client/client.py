# Copyright 2025 Accent Communications

"""Client implementation for Accent Chat Daemon API."""

from __future__ import annotations

import logging
from typing import Any

from accent_lib_rest_client.client import BaseClient

logger = logging.getLogger(__name__)


class ChatdClient(BaseClient):
    """Client for interacting with the Chat Daemon API.

    This client provides methods for creating and managing chat rooms,
    sending messages, and tracking user presence.
    """

    namespace = "accent_chatd_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/chatd",
        version: str = "1.0",
        **kwargs: Any,
    ) -> None:
        """Initialize the Chat Daemon client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments passed to BaseClient

        """
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
