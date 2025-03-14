# resources/call_logs/types.py


from pydantic import UUID4, BaseModel, Field

from accent_bus.resources.common.types import DateTimeStr


class DestinationConferenceDict(BaseModel):
    """Represents conference destination details."""

    conference_id: int


class DestinationMeetingDict(BaseModel):
    """Represents meeting destination details."""

    meeting_uuid: UUID4
    meeting_name: str


class DestinationUserDict(BaseModel):
    """Represents user destination details."""

    user_uuid: UUID4
    user_name: str


class DestinationUnknownDict(BaseModel):
    """Represents unknown destination details."""


class DestinationDetailsDict(BaseModel):
    """Represents all possible destination details."""

    conference: DestinationConferenceDict | None = None
    meeting: DestinationMeetingDict | None = None
    user: DestinationUserDict | None = None
    unknown: DestinationUnknownDict | None = None


class RecordingDict(BaseModel):
    """Represents recording details."""

    uuid: UUID4
    start_time: str
    end_time: str
    deleted: bool
    filename: str


class CDRDataDict(BaseModel):
    """Represents CDR data (Call Detail Record)."""

    id: int
    tenant_uuid: UUID4
    start: DateTimeStr
    end: DateTimeStr
    answered: bool
    duration: float
    call_direction: str
    conversation_id: str
    destination_details: DestinationDetailsDict | None = None
    destination_extension: str
    destination_internal_context: str
    destination_internal_extension: str
    destination_line_id: int
    destination_name: str
    destination_user_uuid: UUID4 | None = None
    requested_name: str
    requested_context: str
    requested_extension: str
    requested_internal_context: str
    requested_internal_extension: str
    source_extension: str
    source_internal_context: str
    source_internal_name: str
    source_internal_extension: str
    source_line_id: int
    source_name: str
    source_user_uuid: UUID4 | None = None
    tags: list[str] = Field(default_factory=list)
    recordings: list[RecordingDict] = Field(default_factory=list)
