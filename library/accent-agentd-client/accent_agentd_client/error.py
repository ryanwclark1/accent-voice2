# Copyright 2025 Accent Communications

"""Error definitions for the Accent Agent Daemon client."""

from __future__ import annotations

import logging

# Configure logging
logger = logging.getLogger(__name__)

# Error constants
NO_SUCH_AGENT = "no such agent"
NO_SUCH_LINE = "no such line"
NO_SUCH_QUEUE = "no such queue"
ALREADY_LOGGED = "already logged"
NOT_LOGGED = "not logged in"
ALREADY_IN_USE = "extension and context already in use"
ALREADY_IN_QUEUE = "agent already in queue"
NOT_IN_QUEUE = "agent not in queue"
NO_SUCH_EXTEN = "no such extension and context"
CONTEXT_DIFFERENT_TENANT = "agent and context are not in the same tenant"
QUEUE_DIFFERENT_TENANT = "agent and queue are not in the same tenant"
UNAUTHORIZED = "invalid token or unauthorized"


class AgentdClientError(Exception):
    """Exception raised for Agentd client errors.

    Attributes:
        error: Error message

    """

    def __init__(self, error: str) -> None:
        """Initialize the exception.

        Args:
            error: Error message

        """
        super().__init__(error)
        self.error = error
        logger.error("AgentdClientError: %s", error)
