# Copyright 2024 Accent Communications
from __future__ import annotations

from typing import TypeAlias

from pydantic import UUID4, BaseModel, ConfigDict, Field

# Type Aliases
JSON: TypeAlias = str | int | float | bool | None | list['JSON'] | dict[str, 'JSON']
ACSRedirectLocation: TypeAlias = str
LogoutRedirectLocation: TypeAlias = str

class TokenMetadata(BaseModel):
    """Base token metadata with required fields"""
    uuid: UUID4
    tenant_uuid: UUID4
    auth_id: str
    pbx_user_uuid: UUID4
    accent_uuid: UUID4

    model_config = ConfigDict(frozen=True)

class TokenMetadataStack(TokenMetadata):
    """Extended token metadata with optional fields"""
    purpose: str | None = None
    admin: str | None = None

    model_config = ConfigDict(frozen=True)

class Token(BaseModel):
    """Authentication token information"""
    token: str
    session_uuid: UUID4
    metadata: TokenMetadata | TokenMetadataStack
    acl: list[str] = Field(default_factory=list)
    auth_id: str
    accent_uuid: UUID4
    expires_at: str
    utc_expires_at: str
    issued_at: str
    utc_issued_at: str
    user_agent: str
    remote_addr: str

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "token": "abc123",
                "session_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "metadata": {
                    "uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "tenant_uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "auth_id": "user123",
                    "pbx_user_uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "accent_uuid": "123e4567-e89b-12d3-a456-426614174000"
                },
                "acl": ["read", "write"],
                "auth_id": "user123",
                "accent_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "expires_at": "2024-12-31T23:59:59Z",
                "utc_expires_at": "2024-12-31T23:59:59Z",
                "issued_at": "2024-01-01T00:00:00Z",
                "utc_issued_at": "2024-01-01T00:00:00Z",
                "user_agent": "Mozilla/5.0",
                "remote_addr": "192.168.1.1"
            }
        }
    )

class SSOResponse(BaseModel):
    """SSO response information"""
    location: str
    saml_session_id: str

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "location": "https://sso.example.com/auth",
                "saml_session_id": "session123"
            }
        }
    )

