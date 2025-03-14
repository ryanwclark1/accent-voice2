# resources/application/types.py
from typing import Dict, Optional

from pydantic import BaseModel, UUID4, Field


class ApplicationDict(BaseModel):
    """Represents the structure of an Application."""

    uuid: UUID4
    tenant_uuid: UUID4
    name: str
    destination: str | None = None
    destination_options: dict[str, str] = Field(default_factory=dict)
