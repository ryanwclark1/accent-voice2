# accent_auth/auth/schemas.py

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator, model_validator
from accent_auth.services import saml


class TokenRequest(BaseModel):
    """Schema for creating a new token."""

    grant_type: (
        str  # We need to check in the route if authorization is Basic or Bearer.
    )
    username: str | None = None
    password: str | None = None
    refresh_token: str | None = None
    client_id: str | None = None
    saml_session_id: str | None = None
    expiration: int | None = Field(None, ge=1, le=315360000)  # Between 1s and 10 years
    access_type: str = "online"  # Default value
    domain_name: str | None = None
    tenant_id: str | None = None
    mobile: bool | None = None

    @model_validator(mode="after")
    def check_username_password_or_refresh_token(self) -> "TokenRequest":
        if self.grant_type == "password" and (
            self.username is None or self.password is None
        ):
            raise ValueError(
                "Username and password must be provided when not using a refresh token"
            )
        if self.grant_type == "refresh_token" and not self.refresh_token:
            raise ValueError("refresh_token is required for refresh_token grant type")

        if self.grant_type == "refresh_token" and not self.client_id:
            raise ValueError("client_id is required for refresh_token grant type")

        if self.grant_type == "client_credentials" and not self.client_id:
            raise ValueError("client_id is required for client_credentials grant_type")

        if self.access_type == "offline" and not self.client_id:
            raise ValueError(
                "Client_id must be provided when using access_type offline."
            )

        if self.saml_session_id and (
            self.refresh_token or self.username or self.password
        ):
            raise ValueError(
                "saml_session_id cannot be used with username/password or refresh_token"
            )

        return self


class TokenResponse(BaseModel):
    """Schema for the response when creating or retrieving a token."""

    token: str
    refresh_token: str | None = None  # Only present for offline access
    expires_at: str
    issued_at: str
    utc_expires_at: str
    utc_issued_at: str
    auth_id: str
    accent_user_uuid: str | None
    accent_uuid: str | None
    acl: list[str]
    metadata: dict
    session_uuid: str
    user_agent: str | None
    remote_addr: str | None
    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "string",
                "metadata": {},
            }
        }
    }


class TokenScopesCheckRequest(BaseModel):
    """Schema for the request to check token scopes."""

    scopes: list[str]
    tenant_uuid: str | None = None


class TokenScopesCheckResponse(BaseModel):
    """Schema for the response of the token scopes check."""

    scopes: dict[str, bool]


class RefreshTokenList(BaseModel):
    """Schema for the response to the refresh token list."""

    total: int
    filtered: int
    items: list[RefreshToken]


class SAMLLoginContext(BaseModel):
    """Schema for SAML SSO login context."""

    redirect_url: str
    domain: str


class SAMLSSOResponse(BaseModel):
    """Schema for the SAML SSO response, containing the redirect URL."""

    location: str
    saml_session_id: str


class SAMLIdpResponse(BaseModel):
    """Schema for the SAML IdP response."""

    SAMLResponse: str = Field(
        ..., description="Encoded SAML XML response"
    )  # Required field
    RelayState: str = Field(..., description="Relay state parameter")


class SAMLLogoutRequest(BaseModel):
    location: str


class ExternalAuthConfig(BaseModel):
    data: dict
    type_uuid: str
    tenant_uuid: str


class ExternalAuthUser(BaseModel):
    uuid: str


class ExternalAuthUserList(BaseModel):
    total: int
    filtered: int
    items: list[ExternalAuthUser]


class IDPList(BaseModel):
    types: list[str]


class LDAPConfigSchema(BaseModel):  # Moved from other location
    """Schema for the LDAP backend configuration."""

    tenant_uuid: str
    host: str
    port: int
    protocol_version: int
    protocol_security: str | None = None
    bind_dn: str | None = None
    user_base_dn: str
    user_login_attribute: str
    user_email_attribute: str
    search_filters: str | None = None
    model_config = {"from_attributes": True}


class LDAPConfigUpdateSchema(BaseModel):  # Moved from other location
    """Schema for updating the LDAP backend configuration."""

    host: str | None = None
    port: int | None = None
    protocol_version: int | None = None
    protocol_security: str | None = None
    bind_dn: str | None = None
    bind_password: str | None = None
    user_base_dn: str | None = None
    user_login_attribute: str | None = None
    user_email_attribute: str | None = None
    search_filters: str | None = None


class SAMLConfigSchema(BaseModel):  # Moved from other location
    """Schema for the SAML backend configuration."""

    tenant_uuid: str
    domain_uuid: str
    entity_id: str
    idp_metadata: str  # Store as a string.  We'll parse it when needed.
    acs_url: str
    model_config = {"from_attributes": True}


class SAMLAcsUrlTemplate(BaseModel):  # Moved from other location
    acs_url: str
