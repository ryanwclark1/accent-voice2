# accent_auth/users/schemas.py

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from accent_auth.models import CustomBaseModel


class Email(BaseModel):
    """Represents an email address."""

    address: str
    main: bool
    confirmed: bool | None = None  # Make confirmed optional, with None as default


class EmailUpdate(BaseModel):
    address: str
    main: bool
    confirmed: bool | None = None


class UserBase(BaseModel):
    """Base schema for user-related operations."""

    username: str | None = None  # Allow None for updates
    firstname: str | None = None
    lastname: str | None = None
    enabled: bool = True
    purpose: str = "user"
    authentication_method: str = "default"


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=1)  # Password is required on creation
    email_address: EmailStr = Field(
        ..., description="The user's primary email address"
    )  # email is required on creation
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "secure_password",
                "email_address": "john.doe@example.com",
                "firstname": "John",
                "lastname": "Doe",
                "purpose": "user",
                "authentication_method": "default",
            }
        }


class UserUpdate(UserBase):
    """Schema for updating an existing user.  All base fields are optional."""

    pass  # Inherits all fields, but all are optional


class UserResult(UserBase):
    """Schema for the user data returned by the API."""

    uuid: str
    emails: List[Email] = []
    tenant_uuid: str

    class Config:
        from_attributes = True  # Use ORM mode (Pydantic v2)


class UserList(BaseModel):
    total: int
    filtered: int
    items: list[UserResult]


class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=1)


class UserRegister(BaseModel):
    username: str = Field(..., min_length=1, max_length=256)
    password: str = Field(..., min_length=1)
    email_address: EmailStr
    firstname: str | None = None
    lastname: str | None = None
    purpose: str = "user"
    authentication_method: str = "default"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "secure_password",
                "email_address": "john.doe@example.com",
                "firstname": "John",
                "lastname": "Doe",
            }
        }


# Added for sessions
class UserSession(BaseModel):
    """Represents a user session."""

    uuid: str
    mobile: bool
    tenant_uuid: str
    # You might want to add more fields here, like creation date, last activity, etc.

    model_config = {"from_attributes": True}


class UserSessionList(BaseModel):
    """Response schema for listing user sessions."""

    total: int
    filtered: int
    items: list[UserSession]
