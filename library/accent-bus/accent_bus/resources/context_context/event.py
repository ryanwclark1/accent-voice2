# resources/context_context/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class ContextContextEvent(TenantEvent):
    """Base class for Context-Context events."""

    service: ClassVar[str] = "confd"
    content: dict


class ContextContextsAssociatedEvent(ContextContextEvent):
    """Event for when contexts are associated."""

    name: ClassVar[str] = "contexts_associated"
    routing_key_fmt: ClassVar[str] = "config.contexts.contexts.updated"

    def __init__(self, context_id: int, context_ids: list[int], **data):
        content = {
            "context_id": context_id,
            "context_ids": context_ids,
        }
        super().__init__(content=content, **data)
