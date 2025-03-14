# resources/call_logd/types.py
from typing import TypedDict

from resources.common.types import DateTimeStr, UUIDStr


class CallLogExportDataDict(TypedDict, total=False):
    """Represents the data for a call log export."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    user_uuid: UUIDStr
    requested_at: DateTimeStr
    filename: str
    status: str
