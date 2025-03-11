# Copyright 2025 Accent Communications

"""Webhookd client module for API interactions.

This module provides the main client for interacting with the Webhookd API,
with support for both synchronous and asynchronous operations.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from accent_lib_rest_client.client import BaseClient

# For typing only
if TYPE_CHECKING:
    from accent_webhookd_client.commands.config import ConfigCommand
    from accent_webhookd_client.commands.mobile_notifications import (
        MobileNotificationCommand,
    )
    from accent_webhookd_client.commands.status import StatusCommand
    from accent_webhookd_client.commands.subscriptions import SubscriptionsCommand

# Configure logging
logger = logging.getLogger(__name__)


class WebhookdClient(BaseClient):
    """Client for the Webhookd API.

    This client extends the BaseClient to provide specialized commands
    for interacting with the Webhookd service.

    Attributes:
        config: Command for managing configuration
        mobile_notifications: Command for sending mobile notifications
        status: Command for checking service status
        subscriptions: Command for managing subscriptions

    """

    namespace = "accent_webhookd_client.commands"

    config: ConfigCommand
    mobile_notifications: MobileNotificationCommand
    status: StatusCommand
    subscriptions: SubscriptionsCommand

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str = "/api/webhookd",
        version: str = "1.0",
        **kwargs: Any,
    ) -> None:
        """Initialize a new Webhookd client.

        Args:
            host: Hostname or IP of the Webhookd server
            port: Port number for the server
            prefix: URL prefix path
            version: API version string
            **kwargs: Additional arguments to pass to the BaseClient

        """
        logger.debug("Initializing Webhookd client for %s:%s", host, port)
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
