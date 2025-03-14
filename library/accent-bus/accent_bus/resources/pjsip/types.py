# resources/pjsip/types.py

from pydantic import BaseModel, UUID4, Field


class PJSIPTransportDict(BaseModel):
    """Represents a PJSIP transport."""

    uuid: UUID4
    name: str
    options: list[str] = Field(default_factory=list)
