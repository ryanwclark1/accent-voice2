# Copyright 2025 Accent Communications

"""Pydantic models for the Accent Agent Daemon client."""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)


class AgentStatus(BaseModel):
    """Agent status information.

    Attributes:
        id: Agent identifier
        number: Agent number
        origin_uuid: Origin UUID
        logged: Whether agent is logged in
        paused: Whether agent is paused
        extension: Extension number
        context: Context
        state_interface: State interface
        tenant_uuid: Tenant UUID

    """

    id: str
    number: str
    origin_uuid: str
    logged: bool = False
    paused: bool | None = None
    extension: str | None = None
    context: str | None = None
    state_interface: str | None = None
    tenant_uuid: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentStatus:
        """Create an AgentStatus instance from a dictionary.

        Args:
            data: Dictionary containing agent status data

        Returns:
            New AgentStatus instance

        """
        return cls(
            id=data["id"],
            number=data["number"],
            origin_uuid=data["origin_uuid"],
            logged=data["logged"],
            paused=data["paused"],
            extension=data["extension"],
            context=data["context"],
            state_interface=data["state_interface"],
            tenant_uuid=data["tenant_uuid"],
        )


class QueueRequest(BaseModel):
    """Request model for queue operations.

    Attributes:
        queue_id: Queue identifier

    """

    queue_id: str


class LoginRequest(BaseModel):
    """Request model for agent login operations.

    Attributes:
        extension: Extension number
        context: Context

    """

    extension: str
    context: str


class UserAgentLoginRequest(BaseModel):
    """Request model for user agent login.

    Attributes:
        line_id: Line identifier

    """

    line_id: str
