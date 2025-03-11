# Copyright 2025 Accent Communications

"""Accent Agent Daemon client implementation."""

from __future__ import annotations

import logging
from typing import Any

from accent_lib_rest_client.client import BaseClient

# Configure logging
logger = logging.getLogger(__name__)


class AgentdClient(BaseClient):
    """Client for the Accent Agent Daemon API.

    Provides methods to interact with the Agentd service for managing
    agent states and operations.
    """

    namespace = "accent_agentd_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/agentd",
        version: str = "1.0",
        **kwargs: Any,
    ) -> None:
        """Initialize the Agentd client.

        Args:
            host: Hostname or IP of the server
            port: Port number for the server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments passed to BaseClient

        """
        logger.info(
            "Initializing AgentdClient: %s:%s%s v%s", host, port, prefix, version
        )
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
