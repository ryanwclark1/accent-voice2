# accent_auth/tenants/schemas.py

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from accent_auth.models import CustomBaseModel


class Domain(BaseModel):
    """Represents a domain."""

    name: str
    uuid: str

    model_config = {"from_attributes": True}


class Address(BaseModel):
    """Represents an address."""

    line_1: str | None = None
    line_2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None

    model_config = {"from_attributes": True}


class TenantBase(BaseModel):
    """Base schema for tenant-related operations."""

    name: str | None = Field(None, max_length=128)
    phone: str | None = None
    contact_uuid: str | None = None
    domain_names: List[str] = []
    address: Address | None = None  # Use the Address Pydantic model
    default_authentication_method: str = "native"


class TenantCreate(TenantBase):
    """Schema for creating a new tenant."""

    slug: str | None = None
    parent_uuid: str


class TenantUpdate(TenantBase):
    """Schema for updating a tenant.  All base fields are optional."""

    pass  # Inherits all fields, but all are optional


class TenantResult(TenantBase):
    """Schema for returning tenant details."""

    uuid: str
    slug: str
    parent_uuid: str

    model_config = {"from_attributes": True}


class TenantList(BaseModel):
    total: int
    filtered: int
    items: list[TenantResult]
