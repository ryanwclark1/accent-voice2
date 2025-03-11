# Copyright 2025 Accent Communications

"""Data models for the Accent Setup Daemon client."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SetupConfig(BaseModel):
    """Configuration model for setup operations.

    Attributes:
        tenant_id: The tenant identifier
        parameters: Configuration parameters for the setup

    """

    tenant_id: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class StatusResponse(BaseModel):
    """Model for status response data.

    Attributes:
        status: Current setup status
        progress: Setup progress percentage
        started_at: When the setup started
        completed_at: When the setup completed, if finished
        error: Error details, if any

    """

    status: str
    progress: float
    started_at: datetime
    completed_at: datetime | None = None
    error: dict[str, Any] | None = None


class ConfigResponse(BaseModel):
    """Model for configuration response data.

    Attributes:
        config: Current configuration settings
        version: Configuration version
        updated_at: When the configuration was last updated

    """

    config: dict[str, Any]
    version: str
    updated_at: datetime
