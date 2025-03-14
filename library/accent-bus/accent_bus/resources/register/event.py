# resources/register/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class RegisterEvent(ServiceEvent):
    """Base class for Register events."""

    service: ClassVar[str] = "confd"
    content: dict


class RegisterSIPCreated(RegisterEvent):
    """Event for when a SIP register is created."""

    name: ClassVar[str] = "register_sip_created"
    routing_key_fmt: ClassVar[str] = "config.register.sip.created"

    def __init__(self, register_id: int, **data):
        content = {"id": int(register_id)}
        super().__init__(content=content, **data)


class RegisterSIPDeleted(RegisterEvent):
    """Event for when a SIP register is deleted."""

    name: ClassVar[str] = "register_sip_deleted"
    routing_key_fmt: ClassVar[str] = "config.register.sip.deleted"

    def __init__(self, register_id: int, **data):
        content = {"id": int(register_id)}
        super().__init__(content=content, **data)


class RegisterSIPEditedEvent(RegisterEvent):
    """Event for when a SIP register is edited."""

    name: ClassVar[str] = "register_sip_edited"
    routing_key_fmt: ClassVar[str] = "config.register.sip.edited"

    def __init__(self, register_id: int, **data):
        content = {"id": int(register_id)}
        super().__init__(content=content, **data)


class RegisterIAXCreatedEvent(RegisterEvent):
    """Event for when an IAX register is created."""

    name: ClassVar[str] = "register_iax_created"
    routing_key_fmt: ClassVar[str] = "config.register.iax.created"

    def __init__(self, register_id: int, **data):
        content = {"id": int(register_id)}
        super().__init__(content=content, **data)


class RegisterIAXDeletedEvent(RegisterEvent):
    """Event for when an IAX register is deleted."""

    name: ClassVar[str] = "register_iax_deleted"
    routing_key_fmt: ClassVar[str] = "config.register.iax.deleted"

    def __init__(self, register_id: int, **data):
        content = {"id": int(register_id)}
        super().__init__(content=content, **data)


class RegisterIAXEditedEvent(RegisterEvent):
    """Event for when an IAX register is edited."""

    name: ClassVar[str] = "register_iax_edited"
    routing_key_fmt: ClassVar[str] = "config.register.iax.edited"

    def __init__(self, register_id: int, **data):
        content = {"id": int(register_id)}
        super().__init__(content=content, **data)
