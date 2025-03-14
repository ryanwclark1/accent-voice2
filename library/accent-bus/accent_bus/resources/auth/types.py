# resources/auth/types.py

from pydantic import UUID4, BaseModel, Field


class TenantDict(BaseModel):
    """Represents a Tenant."""

    uuid: UUID4
    name: str
    slug: str
    domain_names: list[str] = Field(default_factory=list)
