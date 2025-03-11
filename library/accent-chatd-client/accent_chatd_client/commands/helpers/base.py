# Copyright 2025 Accent Communications

"""Base command class for Chat Daemon API."""

import logging

from accent_chatd_client.command import ChatdCommand

logger = logging.getLogger(__name__)


class BaseCommand(ChatdCommand):
    """Base command for all Chat Daemon API endpoints.

    This class serves as a common base for all command implementations
    in the Chat Daemon client.
    """

    pass  # noqa: PIE790
