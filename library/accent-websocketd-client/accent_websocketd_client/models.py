# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class WebsocketMessage(BaseModel):
    """Base model for websocket messages."""

    op: str
    data: dict[str, Any] | None = None


class EventData(BaseModel):
    """Model for event data."""

    name: str
    payload: dict[str, Any] = Field(default_factory=dict)


class EventMessage(WebsocketMessage):
    """Model for event messages."""

    op: Literal["event"]
    data: EventData


class SubscriptionRequest(WebsocketMessage):
    """Model for subscription requests."""

    op: Literal["subscribe"]
    data: dict[str, str] = Field(...)


class TokenUpdate(WebsocketMessage):
    """Model for token updates."""

    op: Literal["token"]
    data: dict[str, str] = Field(...)


class PingRequest(WebsocketMessage):
    """Model for ping requests."""

    op: Literal["ping"]
    data: dict[str, str] = Field(...)


class StartRequest(WebsocketMessage):
    """Model for start requests."""

    op: Literal["start"]
