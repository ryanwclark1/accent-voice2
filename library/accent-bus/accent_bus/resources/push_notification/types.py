# resources/push_notification/types.py

from pydantic import BaseModel


class PushMobileDict(BaseModel):
    """Represents mobile push notification data."""

    peer_caller_id_number: str
    peer_caller_id_name: str
    call_id: str
    video: bool
    ring_timeout: int
    sip_call_id: str
    mobile_wakeup_timestamp: str  # ISO-formatted timestamp
