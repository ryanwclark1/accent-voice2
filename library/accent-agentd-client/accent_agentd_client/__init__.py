# Copyright 2025 Accent Communications

"""Accent Agent Daemon client library for controlling agent states.

This package provides a client for interacting with the Accent Agent Daemon API,
supporting both synchronous and asynchronous operations.
"""

from accent_agentd_client.client import AgentdClient as Client
from accent_agentd_client.error import (
    ALREADY_IN_QUEUE,
    ALREADY_IN_USE,
    ALREADY_LOGGED,
    CONTEXT_DIFFERENT_TENANT,
    NO_SUCH_AGENT,
    NO_SUCH_EXTEN,
    NO_SUCH_LINE,
    NO_SUCH_QUEUE,
    NOT_IN_QUEUE,
    NOT_LOGGED,
    QUEUE_DIFFERENT_TENANT,
    UNAUTHORIZED,
    AgentdClientError,
)
from accent_agentd_client.models import AgentStatus

__all__ = [
    "ALREADY_IN_QUEUE",
    "ALREADY_IN_USE",
    "ALREADY_LOGGED",
    "CONTEXT_DIFFERENT_TENANT",
    "NOT_IN_QUEUE",
    "NOT_LOGGED",
    "NO_SUCH_AGENT",
    "NO_SUCH_EXTEN",
    "NO_SUCH_LINE",
    "NO_SUCH_QUEUE",
    "QUEUE_DIFFERENT_TENANT",
    "UNAUTHORIZED",
    "AgentStatus",
    "AgentdClientError",
    "Client",
]
