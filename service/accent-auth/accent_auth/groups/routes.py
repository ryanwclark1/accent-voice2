# accent_auth/groups/schemas.py

from typing import List, Optional

from pydantic import BaseModel, Field, validator

from accent_auth.models import CustomBaseModel
from accent_auth.users.schemas import UserResult  # Import to avoid circlular import
from accent_auth.policies.schemas import Policy  # Import to avoid circlular import


class GroupBase(BaseModel):
    name: str = Field(..., max_length=80)
    slug: str | None = None  # Slug is optional, can be autogenerated.


class GroupCreate(GroupBase):
    tenant_uuid: str  # Added, since it's not part of the base.
    system_managed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Group",
                "slug": "my-group",  # Optional
                "tenant_uuid": "some-tenant-uuid",
                "system_managed": False,
            }
        }


class GroupUpdate(GroupBase):
    name: str | None = None  # Allow partial updates


class Group(GroupBase):
    """For returning group information."""

    uuid: str
    tenant_uuid: str
    system_managed: bool
    read_only: bool  # Keep this, as per your existing logic

    model_config = {"from_attributes": True}


class GroupList(BaseModel):
    total: int
    filtered: int
    items: list[Group]


# Added schemas
class PolicyList(BaseModel):
    total: int
    filtered: int
    items: list[Policy]


class UserList(BaseModel):
    total: int
    filtered: int
    items: list[UserResult]
