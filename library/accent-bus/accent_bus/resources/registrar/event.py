# accent_bus/resources/registrar/event.py
# Copyright 2025 Accent Communications

"""Registrar events."""

from accent_bus.resources.common.event import ServiceEvent

from .types import RegistrarDict


class RegistrarCreatedEvent(ServiceEvent):
    """Event for when a registrar is created."""

    service = "confd"
    name = "registrar_created"
    routing_key_fmt = "config.registrar.created"

    def __init__(self, registrar: RegistrarDict) -> None:
        """Initialize the event.

        Args:
          registrar (RegistrarDict): registrar

        """
        super().__init__(registrar)


class RegistrarDeletedEvent(ServiceEvent):
    """Event for when a registrar is deleted."""

    service = "confd"
    name = "registrar_deleted"
    routing_key_fmt = "config.registrar.deleted"

    def __init__(self, registrar: RegistrarDict) -> None:
        """Initialize the event.

        Args:
            registrar (RegistrarDict): The registrar details.

        """
        super().__init__(registrar)


class RegistrarEditedEvent(ServiceEvent):
    """Event for when a registrar is edited."""

    service = "confd"
    name = "registrar_edited"
    routing_key_fmt = "config.registrar.edited"

    def __init__(self, registrar: RegistrarDict) -> None:
        """Initialize event.

        Args:
            registrar (RegistrarDict): registrar details.

        """
        super().__init__(registrar)
