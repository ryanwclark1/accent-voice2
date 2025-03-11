# Copyright 2025 Accent Communications

"""Pydantic models for Webhookd client.

This module contains the pydantic models used to represent and validate
the data structures used in the Webhookd API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class WebhookdConfig(BaseModel):
    """Configuration model for Webhookd service.

    Attributes:
        enabled: Whether the service is enabled
        debug: Whether debug mode is enabled
        additional_fields: Any additional configuration fields

    """

    enabled: bool = True
    debug: bool = False
    additional_fields: dict[str, Any] = Field(default_factory=dict)

    # Using extra=allow to allow for additional fields
    model_config = {"extra": "allow"}


class NotificationModel(BaseModel):
    """Model for mobile notifications.

    Attributes:
        recipient: Recipient identifier
        message: Notification message content
        title: Optional notification title
        data: Optional additional data payload

    """

    recipient: str
    message: str
    title: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class StatusResponse(BaseModel):
    """Model for service status response.

    Attributes:
        status: Status string (e.g., "up", "down")
        version: Service version
        uptime: Service uptime in seconds
        timestamp: Response timestamp

    """

    status: str
    version: str
    uptime: float
    timestamp: datetime = Field(default_factory=datetime.now)


class ServiceInfo(BaseModel):
    """Model for service information.

    Attributes:
        name: Service name
        description: Service description
        events: Available event types

    """

    name: str
    description: str
    events: list[str]


class ServicesDict(BaseModel):
    """Model for services collection.

    Attributes:
        services: Dictionary of available services

    """

    services: dict[str, ServiceInfo]


class SubscriptionModel(BaseModel):
    """Model for subscription data.

    Attributes:
        uuid: Subscription UUID
        service: Service name
        events: List of subscribed events
        config: Subscription configuration
        metadata: Optional metadata
        owner_uuid: Owner's UUID
        created_at: Creation timestamp
        updated_at: Last update timestamp

    """

    uuid: UUID | None = None
    service: str
    events: list[str]
    config: dict[str, Any]
    metadata: dict[str, str] = Field(default_factory=dict)
    owner_uuid: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserSubscriptionModel(BaseModel):
    """Model for user subscription data.

    Attributes:
        uuid: Subscription UUID
        service: Service name
        events: List of subscribed events
        config: Subscription configuration
        metadata: Optional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp

    """

    uuid: UUID | None = None
    service: str
    events: list[str]
    config: dict[str, Any]
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SubscriptionLog(BaseModel):
    """Model for subscription log entry.

    Attributes:
        uuid: Log entry UUID
        subscription_uuid: Subscription UUID
        event_name: Event name
        status: Status of the event
        timestamp: Event timestamp
        data: Event data

    """

    uuid: UUID
    subscription_uuid: UUID
    event_name: str
    status: str
    timestamp: datetime
    data: dict[str, Any] = Field(default_factory=dict)


class PaginatedResponse(BaseModel):
    """Base model for paginated responses.

    Attributes:
        total: Total number of items
        items: List of items in current page

    """

    total: int
    items: list[Any]


class SubscriptionListResponse(PaginatedResponse):
    """Model for subscription list response.

    Attributes:
        items: List of subscriptions

    """

    items: list[SubscriptionModel]


class UserSubscriptionListResponse(PaginatedResponse):
    """Model for user subscription list response.

    Attributes:
        items: List of user subscriptions

    """

    items: list[UserSubscriptionModel]


class SubscriptionLogListResponse(PaginatedResponse):
    """Model for subscription log list response.

    Attributes:
        items: List of subscription logs

    """

    items: list[SubscriptionLog]
