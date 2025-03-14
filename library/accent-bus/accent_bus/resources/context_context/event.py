# accent_bus/resources/context_context/event.py
# Copyright 2025 Accent Communications

"""Context context events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class ContextContextsAssociatedEvent(TenantEvent):
    """Event for when contexts are associated."""

    service = "confd"
    name = "contexts_associated"
    routing_key_fmt = "config.contexts.contexts.updated"

    def __init__(
        self,
        context_id: int,
        context_ids: list[int],
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          context_id: Context ID
          context_ids: List of Context IDs
          tenant_uuid: tenant UUID

        """
        content = {
            "context_id": context_id,
            "context_ids": context_ids,
        }
        super().__init__(content, tenant_uuid)
