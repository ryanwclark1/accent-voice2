# resources/trunk_register/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class TrunkRegisterEvent(TenantEvent):
    """Base class for Trunk Register events."""

    service: ClassVar[str] = "confd"
    content: dict


class TrunkRegisterIAXAssociatedEvent(TrunkRegisterEvent):
    """Event for when an IAX register is associated with a trunk."""

    name: ClassVar[str] = "trunk_register_iax_associated"
    routing_key_fmt: ClassVar[str] = "config.trunks.registers.iax.updated"

    def __init__(self, trunk_id: int, register_id: int, **data):
        content = {"trunk_id": trunk_id, "register_id": register_id}
        super().__init__(content=content, **data)


class TrunkRegisterIAXDissociatedEvent(TrunkRegisterEvent):
    """Event for when an IAX register is dissociated from a trunk."""

    name: ClassVar[str] = "trunk_register_iax_dissociated"
    routing_key_fmt: ClassVar[str] = "config.trunks.registers.iax.deleted"

    def __init__(self, trunk_id: int, register_id: int, **data):
        content = {
            "trunk_id": trunk_id,
            "register_id": register_id,
        }
        super().__init__(content=content, **data)
