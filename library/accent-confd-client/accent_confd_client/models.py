# Copyright 2025 Accent Communications

"""Data models for the Configuration Daemon API."""

import logging
from typing import Any

from pydantic import BaseModel, Field

# Configure standard logging
logger = logging.getLogger(__name__)


class LineDevice(BaseModel):
    """Line device association model."""

    line_id: str
    device_id: str


class DeviceInfo(BaseModel):
    """Device information model."""

    id: str
    vendor: str | None = None
    model: str | None = None
    version: str | None = None
    description: str | None = None
    mac: str | None = None
    template_id: str | None = None
    status: str | None = None
    options: dict[str, Any] = Field(default_factory=dict)
    links: list[dict[str, str]] = Field(default_factory=list)


class UserLine(BaseModel):
    """User line association model."""

    user_id: str
    line_id: str
    main_line: bool = False
    main_user: bool = False


class FuncKey(BaseModel):
    """Function key model."""

    type: str
    label: str | None = None
    destination: dict[str, Any] = Field(default_factory=dict)
    legacy: bool | None = None


class UserFuncKey(BaseModel):
    """User function key model."""

    user_id: str
    template_id: str | None = None
    position: str
    blf: bool = False
    func_key: FuncKey


class Fallback(BaseModel):
    """Fallback model."""

    destination: str
    enabled: bool = True


class Forward(BaseModel):
    """Forward model."""

    destination: str | None = None
    enabled: bool = False


class Service(BaseModel):
    """Service model."""

    enabled: bool = False


class EndpointSIP(BaseModel):
    """SIP endpoint model."""

    id: str
    name: str
    auth_username: str | None = None
    password: str | None = None
    type: str = "friend"
    host: str = "dynamic"
    options: dict[str, Any] = Field(default_factory=dict)
    links: list[dict[str, str]] = Field(default_factory=list)
