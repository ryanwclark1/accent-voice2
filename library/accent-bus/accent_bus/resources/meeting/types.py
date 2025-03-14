# resources/meeting/types.py
from typing import TypedDict, List

from pydantic import UUID4
from resources.common.types import DateTimeStr


class MeetingDict(TypedDict, total=False):
    """Represents meeting information."""

    uuid: UUID4
    name: str
    owner_uuids: list[UUID4]
    ingress_http_uri: str
    guest_sip_authorization: str | None  # b64 encoded


class MeetingAuthorizationDict(TypedDict, total=False):
    """Represents a meeting authorization."""

    uuid: UUID4
    meeting_uuid: UUID4
    guest_uuid: UUID4
    guest_name: str
    status: str
    creation_time: DateTimeStr


class MeetingParticipantDict(TypedDict, total=False):
    """Represents a participant in a meeting."""

    id: str
    caller_id_name: str
    caller_id_number: str
    call_id: str
    user_uuid: UUID4 | None
