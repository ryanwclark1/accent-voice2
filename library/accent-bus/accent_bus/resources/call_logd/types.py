# resources/call_logd/types.py
from pydantic import BaseModel

from accent_bus.resources.common.types import DateTimeStr, UUIDStr


class CallLogExportDataDict(BaseModel):
    """Represents the data for a call log export."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    user_uuid: UUIDStr
    requested_at: DateTimeStr
    filename: str
    status: str
