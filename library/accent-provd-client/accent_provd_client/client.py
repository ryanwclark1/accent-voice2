# Copyright 2025 Accent Communications

"""Client for the Accent provisioning API."""

from __future__ import annotations

import logging
from typing import Any

from accent_lib_rest_client.client import BaseClient

logger = logging.getLogger(__name__)


class Client(BaseClient):
    """Client for interacting with the provisioning API.

    This class extends BaseClient to provide commands specific to
    the provisioning service.
    """

    namespace = "accent_provd_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/provd",
        version: str = "0.2",
        **kwargs: Any,
    ) -> None:
        """Initialize the provisioning client.

        Args:
            host: Server hostname or IP
            port: Server port
            prefix: URL prefix
            version: API version
            **kwargs: Additional keyword arguments for BaseClient

        """
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
