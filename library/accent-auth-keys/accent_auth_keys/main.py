# Copyright 2025 Accent Communications

"""Main entry point for the Accent Auth Keys application."""

import asyncio
import logging
import os
import sys
from typing import Any

from cliff.app import App
from cliff.commandmanager import CommandManager

from . import config
from .client import AsyncClient
from .file_manager import FileManager

# Configure logging
logger = logging.getLogger(__name__)


class AccentAuthKeys(App):
    """Main application class for Accent Auth Keys.

    This class manages the lifecycle of the application, handling configuration,
    command registration, and client initialization.
    """

    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self) -> None:
        """Initialize the AccentAuthKeys application."""
        super().__init__(
            description="A wrapper to accent-auth-cli to manage internal users",
            command_manager=CommandManager("accent_auth_keys.commands"),
            version="2.0.0",
        )
        self._token: str | None = None
        self._client: AsyncClient | None = None
        self._auth_config: dict[str, Any] = {}
        self.services: dict[str, Any] = {}
        self.file_manager: FileManager | None = None

    def build_option_parser(self, *args: Any, **kwargs: Any) -> Any:
        """Build the option parser for command-line arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The configured argument parser.

        """
        parser = super().build_option_parser(*args, **kwargs)
        parser.add_argument(
            "--accent-auth-cli-config",
            default=os.getenv(
                "ACCENT_AUTH_CLI_CONFIG", "/root/.config/accent-auth-cli"
            ),
            help="Extra configuration directory to override the accent-auth-cli configuration",
        )
        parser.add_argument(
            "--base-dir",
            default="/var/lib/accent-auth-keys",
            help="The base directory of the file keys",
        )
        parser.add_argument(
            "--config",
            default="/etc/accent-auth-keys",
            help="The accent-auth-keys configuration directory",
        )
        return parser

    @property
    def client(self) -> AsyncClient:
        """Get the async client instance.

        The client will be initialized with the authentication configuration
        and a token if available.

        Returns:
            The AsyncClient instance.

        """
        if not self._client:
            self._client = AsyncClient(**self._auth_config)

        if not self._token:
            # We need to create a token in a synchronous context
            loop = asyncio.new_event_loop()
            try:
                token_response = loop.run_until_complete(
                    self._client.token.new("accent_user", expiration=600)
                )
                self._token = token_response.token
            finally:
                loop.close()

        self._client.set_token(self._token)
        return self._client

    def initialize_app(self, argv: list[str]) -> None:
        """Initialize the application.

        This method sets up configuration, logging, and initializes the client
        and file manager.

        Args:
            argv: Command-line arguments.

        """
        self.LOG.debug("accent-auth-keys")
        self.LOG.debug("options=%s", self.options)

        conf = config.build(self.options)
        self.LOG.debug("Starting with config: %s", conf)

        self.LOG.debug("client args: %s", conf["auth"])
        self._auth_config = dict(conf["auth"])

        self.services = config.load_services(self.options)
        self.file_manager = FileManager(self, self.options.base_dir)


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the application.

    Args:
        argv: Command-line arguments. Defaults to sys.argv[1:].

    Returns:
        Exit code.

    """
    if argv is None:
        argv = sys.argv[1:]

    app = AccentAuthKeys()
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())
