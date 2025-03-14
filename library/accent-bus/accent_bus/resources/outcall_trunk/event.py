# resources/outcall_trunk/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class OutcallTrunkEvent(TenantEvent):
    """Base class for Outcall Trunk events."""

    service: ClassVar[str] = "confd"
    content: dict


class OutcallTrunksAssociatedEvent(OutcallTrunkEvent):
    """Event for when trunks are associated with an outcall."""

    name: ClassVar[str] = "outcall_trunks_associated"
    routing_key_fmt: ClassVar[str] = "config.outcalls.trunks.updated"

    def __init__(self, outcall_id: int, trunk_ids: list[int], **data):
        content = {
            "outcall_id": outcall_id,
            "trunk_ids": trunk_ids,
        }
        super().__init__(content=content, **data)
