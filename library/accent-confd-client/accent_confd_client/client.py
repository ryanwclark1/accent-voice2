# Copyright 2025 Accent Communications

"""Configuration Daemon client module."""

from typing import Any

from accent_lib_rest_client.client import BaseClient

from accent_confd_client.session import ConfdSession


class ConfdClient(BaseClient):
    """Client for the Configuration Daemon API."""

    namespace = "accent_confd_client.commands"

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/confd",
        version: str = "1.1",
        **kwargs: Any,
    ) -> None:
        """Initialize the Configuration Daemon client.

        Args:
            host: Hostname or IP address of the server
            port: Port number for the server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments passed to BaseClient

        """
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)

    def session(self) -> ConfdSession:
        """Get a ConfdSession instance (compatibility method).

        Returns:
            ConfdSession instance

        """
        client = super().session()
        return ConfdSession(client, self.url())
