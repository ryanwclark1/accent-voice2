# accent_bus/resources/call_logd/types.py
# Copyright 2025 Accent Communications

"""Call logd types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import DateTimeStr, UUIDStr


class CallLogExportDataDict(TypedDict, total=False):
    """Dictionary representing call log export data."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    user_uuid: UUIDStr
    requested_at: DateTimeStr
    filename: str
    status: str
