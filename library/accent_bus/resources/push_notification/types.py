# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict


class PushMobileDict(TypedDict, total=False):
    peer_caller_id_number: str
    peer_caller_id_name: str
    call_id: str
    video: bool
    ring_timeout: int
    sip_call_id: str
    mobile_wakeup_timestamp: str  # iso-formatted timestamp
