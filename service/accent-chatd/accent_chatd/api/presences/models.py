# src/accent_chatd/api/presences/models.py
from typing import List, Optional
import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class LinePresence(BaseModel):
    id: int
    state: str = Field(..., description="The current state of the line.")


class UserPresence(BaseModel):
    uuid: str
    tenant_uuid: str
    state: str
    status: Optional[str] = None
    last_activity: Optional[datetime.datetime] = None
    line_state: Optional[str] = None
    mobile: bool
    do_not_disturb: bool
    connected: bool
    lines: List[LinePresence] = []
    model_config = ConfigDict(
        from_attributes=True
    )  # allows creating pydantic models from orm objects

    @field_validator("state")
    def validate_state(cls, value):
        valid_states = {"available", "unavailable", "invisible", "away"}
        if value not in valid_states:
            raise ValueError(
                f"Invalid state. Must be one of: {', '.join(valid_states)}"
            )
        return value


class PresenceList(BaseModel):
    items: List[UserPresence]
    filtered: int
    total: int


# Used for Request.
class PresenceUpdateRequest(BaseModel):
    state: str
    status: Optional[str] = None

    @field_validator("state")
    def validate_state(cls, value):
        valid_states = {"available", "unavailable", "invisible", "away"}
        if value not in valid_states:
            raise ValueError(
                f"Invalid state. Must be one of: {', '.join(valid_states)}"
            )
        return value
