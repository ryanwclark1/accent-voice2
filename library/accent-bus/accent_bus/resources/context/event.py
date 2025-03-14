# resources/context/event.py
from typing import ClassVar

from resources.common.event import TenantEvent

from .types import ContextDict


class ContextEvent(TenantEvent):
    """Base class for Context events."""

    service: ClassVar[str] = "confd"
    content: dict


class ContextCreatedEvent(ContextEvent):
    """Event for when a context is created."""

    name: ClassVar[str] = "context_created"
    routing_key_fmt: ClassVar[str] = "config.contexts.created"

    def __init__(self, context_data: ContextDict, **data):
        super().__init__(content=context_data, **data)


class ContextDeletedEvent(ContextEvent):
    """Event for when a context is deleted."""

    name: ClassVar[str] = "context_deleted"
    routing_key_fmt: ClassVar[str] = "config.contexts.deleted"

    def __init__(self, context_data: ContextDict, **data):
        super().__init__(content=context_data, **data)


class ContextEditedEvent(ContextEvent):
    """Event for when a context is edited."""

    name: ClassVar[str] = "context_edited"
    routing_key_fmt: ClassVar[str] = "config.contexts.edited"

    def __init__(self, context_data: ContextDict, **data):
        super().__init__(content=context_data, **data)
