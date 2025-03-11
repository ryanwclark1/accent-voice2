# Copyright 2025 Accent Communications

"""Data models for the Accent Deployd client.

This module contains Pydantic models that represent the various data structures
used in API requests and responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class DeploydResponse(BaseModel):
    """Standard response model for Deployd API results.

    Attributes:
        data: The response data
        status_code: HTTP status code
        headers: Response headers
        response_time: Time taken for the request in seconds

    """

    data: Any
    status_code: int
    headers: dict[str, str]
    response_time: float | None = None


class DeploydErrorDetail(BaseModel):
    """Model for Deployd error details.

    Attributes:
        error_id: Error identifier
        message: Error message
        details: Additional error details
        timestamp: When the error occurred
        resource: Optional affected resource

    """

    error_id: str
    message: str
    details: str
    timestamp: datetime
    resource: str | None = None


class Credential(BaseModel):
    """Model for credential data.

    Attributes:
        uuid: Unique identifier
        username: Username for the credential
        password: Password for the credential (masked in responses)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        additional_data: Any additional credential data

    """

    uuid: str
    username: str | None = None
    password: str | None = None
    created_at: datetime
    updated_at: datetime
    additional_data: dict[str, Any] = Field(default_factory=dict)


class CredentialData(BaseModel):
    """Model for credential input data.

    Attributes:
        username: Username for the credential
        password: Password for the credential
        additional_data: Any additional credential data

    """

    username: str | None = None
    password: str | None = None
    additional_data: dict[str, Any] = Field(default_factory=dict)


class InstanceBase(BaseModel):
    """Base model for instance data.

    Attributes:
        name: Instance name
        provider_id: Provider identifier
        config: Instance configuration

    """

    name: str
    provider_id: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)


class InstanceData(InstanceBase):
    """Model for instance input data.

    Attributes:
        name: Instance name
        provider_id: Provider identifier
        credentials: Credentials for the instance
        config: Instance configuration

    """

    credentials: CredentialData | None = None


class Instance(InstanceBase):
    """Model for instance response data.

    Attributes:
        uuid: Unique identifier
        name: Instance name
        provider_id: Provider identifier
        status: Current instance status
        created_at: Creation timestamp
        updated_at: Last update timestamp
        config: Instance configuration
        credentials: List of associated credentials

    """

    uuid: str
    status: str
    created_at: datetime
    updated_at: datetime
    credentials: list[Credential] = Field(default_factory=list)


class InstancesList(BaseModel):
    """Model for a list of instances.

    Attributes:
        instances: List of instance objects
        total: Total number of instances

    """

    instances: list[Instance]
    total: int


class ProviderBase(BaseModel):
    """Base model for provider data.

    Attributes:
        name: Provider name
        type: Provider type
        config: Provider configuration

    """

    name: str
    type: str
    config: dict[str, Any] = Field(default_factory=dict)


class ProviderData(ProviderBase):
    """Model for provider input data.

    Attributes:
        name: Provider name
        type: Provider type
        credentials: Provider credentials
        config: Provider configuration

    """

    credentials: CredentialData | None = None


class Provider(ProviderBase):
    """Model for provider response data.

    Attributes:
        uuid: Unique identifier
        name: Provider name
        type: Provider type
        status: Current provider status
        created_at: Creation timestamp
        updated_at: Last update timestamp
        config: Provider configuration
        credentials: Associated credentials

    """

    uuid: str
    status: str
    created_at: datetime
    updated_at: datetime
    credentials: Credential | None = None


class ProvidersList(BaseModel):
    """Model for a list of providers.

    Attributes:
        providers: List of provider objects
        total: Total number of providers

    """

    providers: list[Provider]
    total: int


class Image(BaseModel):
    """Model for provider image data.

    Attributes:
        id: Image identifier
        name: Image name
        description: Image description
        extra: Additional image information

    """

    id: str
    name: str
    description: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class Location(BaseModel):
    """Model for provider location data.

    Attributes:
        id: Location identifier
        name: Location name
        country: Country code
        extra: Additional location information

    """

    id: str
    name: str
    country: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class Network(BaseModel):
    """Model for provider network data.

    Attributes:
        id: Network identifier
        name: Network name
        cidr: Network CIDR
        extra: Additional network information

    """

    id: str
    name: str
    cidr: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class Size(BaseModel):
    """Model for provider instance size data.

    Attributes:
        id: Size identifier
        name: Size name
        ram: RAM in MB
        disk: Disk size in GB
        bandwidth: Bandwidth in Mbps
        vcpus: Number of virtual CPUs
        extra: Additional size information

    """

    id: str
    name: str
    ram: int | None = None
    disk: int | None = None
    bandwidth: int | None = None
    vcpus: int | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class ResourcesList(BaseModel):
    """Generic model for lists of provider resources.

    Attributes:
        items: List of resource objects
        total: Total number of resources

    """

    items: list[Any]
    total: int

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: list[Any], info: Any) -> list[Any]:
        """Validate and convert items based on the resource type.

        Args:
            v: List of items
            info: Validation context

        Returns:
            Validated and converted items

        """
        if not v:
            return v

        # Determine resource type if possible
        sample = v[0]
        if isinstance(sample, dict):
            if "ram" in sample and "vcpus" in sample:
                return [Size(**item) if isinstance(item, dict) else item for item in v]
            if "cidr" in sample:
                return [
                    Network(**item) if isinstance(item, dict) else item for item in v
                ]
            if "country" in sample:
                return [
                    Location(**item) if isinstance(item, dict) else item for item in v
                ]
            if "description" in sample:
                return [Image(**item) if isinstance(item, dict) else item for item in v]

        return v


class Config(BaseModel):
    """Model for Deployd configuration data.

    Attributes:
        version: API version
        services: Available services
        features: Enabled features
        settings: Global settings

    """

    version: str
    services: dict[str, Any] = Field(default_factory=dict)
    features: dict[str, bool] = Field(default_factory=dict)
    settings: dict[str, Any] = Field(default_factory=dict)
