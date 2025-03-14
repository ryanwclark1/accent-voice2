# resources/outcall/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class OutcallEvent(TenantEvent):
    """Base class for Outcall events."""

    service: ClassVar[str] = "confd"
    content: dict


class OutcallCreatedEvent(OutcallEvent):
    """Event for when an outcall is created."""

    name: ClassVar[str] = "outcall_created"
    routing_key_fmt: ClassVar[str] = "config.outcalls.created"

    def __init__(self, outcall_id: int, **data):  # noqa: ANN204
        """Initialize an Event instance with the given outcall ID and additional data.

        Args:
            outcall_id (int): The ID of the outcall.
            **data: Additional keyword arguments to be passed to the
                superclass initializer.

        """
        content = {"id": outcall_id}
        super().__init__(content=content, **data)


class OutcallDeletedEvent(OutcallEvent):
    """Event for when an outcall is deleted."""

    name: ClassVar[str] = "outcall_deleted"
    routing_key_fmt: ClassVar[str] = "config.outcalls.deleted"

    def __init__(self, outcall_id: int, **data):
        content = {"id": outcall_id}
        super().__init__(content=content, **data)


class OutcallEditedEvent(OutcallEvent):
    """Event for when an outcall is edited."""

    name: ClassVar[str] = "outcall_edited"
    routing_key_fmt: ClassVar[str] = "config.outcalls.edited"

    def __init__(self, outcall_id: int, **data):
        """Initialize an instance of class with given outcall ID and additional data.

        Args:
            outcall_id (int): The ID of the outcall.
            **data: Additional keyword arguments to be passed to the
                superclass initializer.

        """
        content = {"id": outcall_id}
        super().__init__(content=content, **data)
