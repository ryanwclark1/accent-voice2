# resources/faxes/types.py
from typing import TypedDict

from pydantic import UUID4


class FaxDict(TypedDict, total=False):
    """Represents fax information."""

    id: str
    call_id: str
    extension: str
    context: str
    caller_id: str
    ivr_extension: str
    wait_time: int
    user_uuid: UUID4
    tenant_uuid: UUID4
