# accent_bus/resources/outcall_trunk/event.py
# Copyright 2025 Accent Communications

"""Outcall trunk events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class OutcallTrunksAssociatedEvent(TenantEvent):
    """Event for when trunks are associated with an outcall."""

    service = "confd"
    name = "outcall_trunks_associated"
    routing_key_fmt = "config.outcalls.trunks.updated"

    def __init__(
        self,
        outcall_id: int,
        trunk_ids: list[int],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            outcall_id (int): outcall ID.
            trunk_ids (list[int]): List of Trunk IDs.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {
            "outcall_id": outcall_id,
            "trunk_ids": trunk_ids,
        }
        super().__init__(content, tenant_uuid)
