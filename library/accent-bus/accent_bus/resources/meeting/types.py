# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class MeetingDict(TypedDict, total=False):
    uuid: UUIDStr
    name: str
    owner_uuids: list[UUIDStr]
    ingress_http_uri: str
    guest_sip_authorization: str | None  # b64 encoded


class MeetingAuthorizationDict(TypedDict, total=False):
    uuid: UUIDStr
    meeting_uuid: UUIDStr
    guest_uuid: UUIDStr
    guest_name: str
    status: str
    creation_time: str


class MeetingParticipantDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str
    call_id: str
    user_uuid: UUIDStr | None
