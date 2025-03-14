# accent_bus/resources/register/event.py
# Copyright 2025 Accent Communications

"""Register events."""

from accent_bus.resources.common.event import ServiceEvent


class RegisterSIPCreated(ServiceEvent):
    """Event for when a SIP register is created."""

    service = "confd"
    name = "register_sip_created"
    routing_key_fmt = "config.register.sip.created"

    def __init__(self, register_id: int) -> None:
        """Initialize the event.

        Args:
            register_id (int): The ID of the register.

        """
        content = {"id": int(register_id)}
        super().__init__(content)


class RegisterSIPDeleted(ServiceEvent):
    """Event for when a SIP register is deleted."""

    service = "confd"
    name = "register_sip_deleted"
    routing_key_fmt = "config.register.sip.deleted"

    def __init__(self, register_id: int) -> None:
        """Initialize Event.

        Args:
          register_id: Register ID

        """
        content = {"id": int(register_id)}
        super().__init__(content)


class RegisterSIPEditedEvent(ServiceEvent):
    """Event for when a SIP register is edited."""

    service = "confd"
    name = "register_sip_edited"
    routing_key_fmt = "config.register.sip.edited"

    def __init__(self, register_id: int) -> None:
        """Initialize event.

        Args:
          register_id: Register ID

        """
        content = {"id": int(register_id)}
        super().__init__(content)


class RegisterIAXCreatedEvent(ServiceEvent):
    """Event for when an IAX register is created."""

    service = "confd"
    name = "register_iax_created"
    routing_key_fmt = "config.register.iax.created"

    def __init__(self, register_id: int) -> None:
        """Initialize event.

        Args:
           register_id: Register ID

        """
        content = {"id": int(register_id)}
        super().__init__(content)


class RegisterIAXDeletedEvent(ServiceEvent):
    """Event for when an IAX register is deleted."""

    service = "confd"
    name = "register_iax_deleted"
    routing_key_fmt = "config.register.iax.deleted"

    def __init__(self, register_id: int) -> None:
        """Initialize event.

        Args:
            register_id (int):  register ID.

        """
        content = {"id": int(register_id)}
        super().__init__(content)


class RegisterIAXEditedEvent(ServiceEvent):
    """Event for when an IAX register is edited."""

    service = "confd"
    name = "register_iax_edited"
    routing_key_fmt = "config.register.iax.edited"

    def __init__(self, register_id: int) -> None:
        """Initialize the event.

        Args:
            register_id (int):  register ID.

        """
        content = {"id": int(register_id)}
        super().__init__(content)
