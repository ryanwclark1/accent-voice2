# resources/application/types.py

from pydantic import UUID4, BaseModel, Field


class ApplicationDict(BaseModel):
    """Represents the structure of an Application."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    destination: str | None = None
    destination_options: dict[str, str] = Field(default_factory=dict)
