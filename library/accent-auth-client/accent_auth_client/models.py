# Copyright 2025 Accent Communications

"""Data models for the Accent Auth Client.

This module contains Pydantic models used throughout the auth client.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AuthClientConfig(BaseModel):
    """Configuration model for the auth client.

    Attributes:
        username: Username for basic authentication
        password: Password for basic authentication
        token: Authentication token
        tenant_uuid: Current tenant UUID

    """

    username: str | None = None
    password: str | None = None
    token: str | None = None
    tenant_uuid: UUID | None = None

    model_config = ConfigDict(frozen=True)


class AuthResponse(BaseModel):
    """Authentication response model.

    Attributes:
        token: Authentication token
        expires_at: Token expiration timestamp
        user_uuid: UUID of the authenticated user

    """

    token: str
    expires_at: datetime
    user_uuid: UUID

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_at": "2025-01-31T23:59:59Z",
                "user_uuid": "123e4567-e89b-12d3-a456-426614174000",
            }
        },
    )


class EmailStatus(BaseModel):
    """Email status model.

    Attributes:
        uuid: Email UUID
        address: Email address
        confirmed: Whether the email is confirmed
        primary: Whether this is the primary email

    """

    uuid: UUID
    address: str
    confirmed: bool
    primary: bool

    model_config = ConfigDict(frozen=True)


class PolicyACL(BaseModel):
    """Policy access control list model.

    Attributes:
        name: ACL name
        description: ACL description
        allowed: Whether access is allowed

    """

    name: str
    description: str | None = None
    allowed: bool

    model_config = ConfigDict(frozen=True)


class User(BaseModel):
    """User model.

    Attributes:
        uuid: User UUID
        username: Username
        firstname: First name
        lastname: Last name
        emails: List of user emails
        enabled: Whether the user is enabled

    """

    uuid: UUID
    username: str
    firstname: str | None = None
    lastname: str | None = None
    emails: list[EmailStatus] = Field(default_factory=list)
    enabled: bool = True

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "username": "jdoe",
                "firstname": "John",
                "lastname": "Doe",
                "emails": [
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174001",
                        "address": "jdoe@example.com",
                        "confirmed": True,
                        "primary": True,
                    }
                ],
                "enabled": True,
            }
        },
    )
