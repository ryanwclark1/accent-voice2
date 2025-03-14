# resources/registrar/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent

from .types import RegistrarDict


class RegistrarEvent(ServiceEvent):
    """Base class for Registrar events."""

    service: ClassVar[str] = "confd"
    content: RegistrarDict  # Use the Pydantic model


class RegistrarCreatedEvent(RegistrarEvent):
    """Event for when a registrar is created."""

    name: ClassVar[str] = "registrar_created"
    routing_key_fmt: ClassVar[str] = "config.registrar.created"

    def __init__(self, registrar: RegistrarDict, **data):
        super().__init__(content=registrar, **data)


class RegistrarDeletedEvent(RegistrarEvent):
    """Event for when a registrar is deleted."""

    name: ClassVar[str] = "registrar_deleted"
    routing_key_fmt: ClassVar[str] = "config.registrar.deleted"

    def __init__(self, registrar: RegistrarDict, **data):
        super().__init__(content=registrar, **data)


class RegistrarEditedEvent(RegistrarEvent):
    """Event for when a registrar is edited."""

    name: ClassVar[str] = "registrar_edited"
    routing_key_fmt: ClassVar[str] = "config.registrar.edited"

    def __init__(self, registrar: RegistrarDict, **data):
        super().__init__(content=registrar, **data)
