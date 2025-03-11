# Copyright 2025 Accent Communications

"""Data models for the Directory Service API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ContactModel(BaseModel):
    """A contact in the directory.

    Attributes:
        id: Unique identifier
        name: Contact's name
        number: Phone number
        email: Email address
        company: Company name
        source: Source identifier
        favorite: Whether the contact is favorited

    """

    id: str
    name: str
    number: str | None = None
    email: str | None = None
    company: str | None = None
    source: str | None = None
    favorite: bool = False


class SourceModel(BaseModel):
    """A source of contacts.

    Attributes:
        uuid: Unique identifier
        name: Source name
        backend: Backend type
        tenant_uuid: Associated tenant UUID
        config: Source configuration

    """

    uuid: str
    name: str
    backend: str
    tenant_uuid: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)


class ProfileModel(BaseModel):
    """A directory profile.

    Attributes:
        uuid: Unique identifier
        name: Profile name
        tenant_uuid: Associated tenant UUID
        services: Configured services
        display: Display configuration
        sources: List of source references

    """

    uuid: str
    name: str
    tenant_uuid: str | None = None
    services: dict[str, Any] = Field(default_factory=dict)
    display: dict[str, Any] | None = None
    sources: list[dict[str, str]] = Field(default_factory=list)


class DirectoryModel(BaseModel):
    """A directory configuration.

    Attributes:
        uuid: Unique identifier
        name: Directory name
        tenant_uuid: Associated tenant UUID
        profiles: List of associated profile UUIDs

    """

    uuid: str
    name: str
    tenant_uuid: str | None = None
    profiles: list[str] = Field(default_factory=list)


class PhonebookModel(BaseModel):
    """A phonebook configuration.

    Attributes:
        uuid: Unique identifier
        name: Phonebook name
        description: Description of the phonebook
        tenant_uuid: Associated tenant UUID

    """

    uuid: str
    name: str
    description: str | None = None
    tenant_uuid: str | None = None


class DisplayModel(BaseModel):
    """A display configuration.

    Attributes:
        uuid: Unique identifier
        name: Display name
        tenant_uuid: Associated tenant UUID
        columns: Column definitions

    """

    uuid: str
    name: str
    tenant_uuid: str | None = None
    columns: list[dict[str, Any]] = Field(default_factory=list)
