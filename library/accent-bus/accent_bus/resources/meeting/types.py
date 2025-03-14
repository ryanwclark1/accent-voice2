# accent_bus/resources/meeting/types.py
# Copyright 2025 Accent Communications

"""Meeting types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class MeetingDict(TypedDict, total=False):
    """Dictionary representing a meeting."""

    uuid: UUIDStr
    name: str
    owner_uuids: list[UUIDStr]
    ingress_http_uri: str
    guest_sip_authorization: str | None  # b64 encoded


class MeetingAuthorizationDict(TypedDict, total=False):
    """Dictionary representing a meeting authorization."""

    uuid: UUIDStr
    meeting_uuid: UUIDStr
    guest_uuid: UUIDStr
    guest_name: str
    status: str
    creation_time: str


class MeetingParticipantDict(TypedDict, total=False):
    """Dictionary representing a meeting participant."""

    id: str
    caller_id_name: str
    caller_id_number: str
    call_id: str
    user_uuid: UUIDStr | None
