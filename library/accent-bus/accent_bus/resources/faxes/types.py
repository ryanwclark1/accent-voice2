# accent_bus/resources/faxes/types.py
# Copyright 2025 Accent Communications

"""Fax types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class FaxDict(TypedDict, total=False):
    """Dictionary representing a fax."""

    id: str
    call_id: str
    extension: str
    context: str
    caller_id: str
    ivr_extension: str
    wait_time: int
    user_uuid: UUIDStr
    tenant_uuid: UUIDStr
