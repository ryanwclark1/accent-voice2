# Copyright 2025 Accent Communications

"""Data models for the Accent Auth Keys application."""

from pydantic import BaseModel


class Service(BaseModel):
    """Service model representing an internal user with access control.

    Attributes:
        acl: Access control list for the service.
        system_user: System user that owns the service files.

    """

    acl: list[str]
    system_user: str


class ServiceFile(BaseModel):
    """Service file model containing credentials.

    Attributes:
        service_id: The ID of the service.
        service_key: The authentication key for the service.

    """

    service_id: str
    service_key: str


class User(BaseModel):
    """User model representing an Accent Auth user.

    Attributes:
        uuid: Unique identifier for the user.
        username: Username of the user.
        purpose: Purpose of the user (e.g., 'internal').

    """

    uuid: str
    username: str
    purpose: str


class Policy(BaseModel):
    """Policy model representing an access policy.

    Attributes:
        uuid: Unique identifier for the policy.
        name: Name of the policy.
        acl: Access control list for the policy.

    """

    uuid: str
    name: str
    acl: list[str]


class TokenResponse(BaseModel):
    """Token response model.

    Attributes:
        token: Authentication token.

    """

    token: str


class ItemsResponse(BaseModel):
    """Generic response with items.

    Attributes:
        items: List of items in the response.

    """

    items: list[dict]
