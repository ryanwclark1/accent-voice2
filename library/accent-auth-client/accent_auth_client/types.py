# Copyright 2025 Accent Communications
from __future__ import annotations

from datetime import datetime
from typing import Any, TypeAlias

from pydantic import UUID4, BaseModel, ConfigDict, Field

# Type Aliases
JSON: TypeAlias = str | int | float | bool | None | list["JSON"] | dict[str, "JSON"]
ACSRedirectLocation: TypeAlias = str
LogoutRedirectLocation: TypeAlias = str
TokenDict: TypeAlias = dict[str, Any]
SSOResponseDict: TypeAlias = dict[str, str]


class TokenMetadata(BaseModel):
    """Base token metadata with required fields.

    Attributes:
        uuid: Unique identifier
        tenant_uuid: Tenant unique identifier
        auth_id: Authentication identifier
        pbx_user_uuid: PBX user identifier
        accent_uuid: Accent system identifier

    """

    uuid: UUID4
    tenant_uuid: UUID4
    auth_id: str
    pbx_user_uuid: UUID4
    accent_uuid: UUID4

    model_config = ConfigDict(frozen=True)


class TokenMetadataStack(TokenMetadata):
    """Extended token metadata with optional fields.

    Attributes:
        purpose: Token purpose
        admin: Admin information

    """

    purpose: str | None = None
    admin: str | None = None

    model_config = ConfigDict(frozen=True)


class Token(BaseModel):
    """Authentication token information.

    Attributes:
        token: The token string
        session_uuid: Session identifier
        metadata: Token metadata
        acl: Access control list
        auth_id: Authentication identifier
        accent_uuid: Accent system identifier
        expires_at: Expiration timestamp
        utc_expires_at: Expiration timestamp in UTC
        issued_at: Issuance timestamp
        utc_issued_at: Issuance timestamp in UTC
        user_agent: User agent string
        remote_addr: Remote address

    """

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
                    "accent_uuid": "123e4567-e89b-12d3-a456-426614174000",
                },
                "acl": ["read", "write"],
                "auth_id": "user123",
                "accent_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "expires_at": "2025-12-31T23:59:59Z",
                "utc_expires_at": "2025-12-31T23:59:59Z",
                "issued_at": "2025-01-01T00:00:00Z",
                "utc_issued_at": "2025-01-01T00:00:00Z",
                "user_agent": "Mozilla/5.0",
                "remote_addr": "192.168.1.1",
            }
        },
    )


class SSOResponse(BaseModel):
    """SSO response information.

    Attributes:
        location: The redirect location
        saml_session_id: SAML session identifier

    """

    location: str
    saml_session_id: str

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "example": {
                "location": "https://sso.example.com/auth",
                "saml_session_id": "session123",
            }
        },
    )


class ErrorDetail(BaseModel):
    """Model for detailed error information.

    Attributes:
        code: Error code
        message: Error message
        field: Optional field name for validation errors
        details: Optional additional error details

    """

    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] | None = None

    model_config = ConfigDict(frozen=True)


class ErrorResponse(BaseModel):
    """Model for API error responses.

    Attributes:
        message: Main error message
        errors: List of detailed errors
        status_code: HTTP status code
        timestamp: When the error occurred

    """

    message: str
    errors: list[ErrorDetail] = Field(default_factory=list)
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(frozen=True)
