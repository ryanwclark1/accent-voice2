from pathlib import PurePosixPath
from datetime import datetime

import validators
from pydantic import UUID4, BaseModel, Field, field_validator, ValidationInfo


class URLConfig(BaseModel):
    """Configuration for URL formatting."""

    scheme: str
    host: str
    port: int | None = None
    prefix: str = ""
    version: str = ""

    model_config = {"frozen": True}

    @field_validator("scheme")
    @classmethod
    def validate_scheme(cls, v: str) -> str:
        """Validate that the scheme is either http or https."""
        if v not in ("http", "https"):
            raise ValueError("Scheme must be either http or https")
        return v.lower()

    @staticmethod
    def _add_leading_slash(v: str) -> str:
        """Add a leading slash to a string if it doesn't already have one."""
        return v if v.startswith("/") else f"/{v}"

    @field_validator("prefix", "version")
    @classmethod
    def validate_path(cls, v: str) -> str:
        return cls._add_leading_slash(v)

    def build_base_url(self) -> str:
        """Build the base URL from configuration."""
        parts = [self.scheme, "://", self.host]
        if self.port:
            parts.append(f":{self.port}")
        parts.extend([self.prefix, self.version])
        url = "".join(parts)
        if not validators.url(url):
            raise ValueError(f"Invalid URL: {url}")
        return url

    def build_url(self, *fragments: str) -> str:
        """Build complete URL with optional path fragments using pathlib."""
        base = self.build_base_url()
        path = PurePosixPath(base, *fragments) if fragments else PurePosixPath(base)
        return str(path)


class RequestParameters(BaseModel):
    """Base model for request parameters."""

    tenant_uuid: UUID4 | None = None
    timeout: int | None = None
    verify_ssl: bool = True
    model_config = {"frozen": True}


class ErrorResponse(BaseModel):
    """Standard error response format."""

    message: str
    error_id: str | None = None
    details: str | None = None
    timestamp: datetime | None = None
    resource: str | None = None
    model_config = {"frozen": True}


class ClientConfig(URLConfig):
    """Client configuration with validation."""

    host: str
    https: bool = True
    port: int = Field(default=443, gt=0, lt=65536)
    prefix: str | None = ""
    tenant_uuid: UUID4 | None = None
    timeout: int = Field(default=10, gt=0)
    token: str | None = None
    user_agent: str = Field(default="")
    verify_certificate: bool = True
    version: str = ""
    tenant_uuid: UUID4 | None = None

    model_config = {"frozen": True}

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int, info: ValidationInfo) -> int:
        if info.data["scheme"] == "http" and v == 443:
            return 80
        elif info.data["scheme"] == "https" and v == 80:
            return 443
        return v


class TenantConfig(BaseModel):

    """Configuration for tenant management."""

    tenant_uuid: UUID4 | None = None
    tenant_enabled: bool = True
    model_config = {"frozen": True}


class TokenConfig(BaseModel):
    """Configuration for token management."""

    token: str
    token_type: str = "Bearer"
    expires_at: datetime | None = None
    model_config = {"frozen": True}
