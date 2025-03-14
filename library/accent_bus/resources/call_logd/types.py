# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import DateTimeStr, UUIDStr


class CallLogExportDataDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    user_uuid: UUIDStr
    requested_at: DateTimeStr
    filename: str
    status: str
