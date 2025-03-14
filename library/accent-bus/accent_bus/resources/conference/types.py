# resources/conference/types.py
from typing import TypedDict

from pydantic import UUID4


class ParticipantDict(TypedDict, total=False):
    """Represents a participant in a conference."""

    id: str
    caller_id_name: str
    caller_id_number: str
    muted: bool
    join_time: int
    admin: bool
    language: str
    call_id: str
    user_uuid: UUID4 | None
