# accent_bus/resources/func_key/event.py
# Copyright 2025 Accent Communications

"""Function key events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class FuncKeyTemplateCreatedEvent(TenantEvent):
    """Event for when a function key template is created."""

    service = "confd"
    name = "func_key_template_created"
    routing_key_fmt = "config.funckey.template.created"

    def __init__(self, template_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
          template_id: Template ID
          tenant_uuid: tenant UUID

        """
        content = {"id": template_id}
        super().__init__(content, tenant_uuid)


class FuncKeyTemplateDeletedEvent(TenantEvent):
    """Event for when a function key template is deleted."""

    service = "confd"
    name = "func_key_template_deleted"
    routing_key_fmt = "config.funckey.template.deleted"

    def __init__(self, template_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            template_id (int): template ID.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {"id": template_id}
        super().__init__(content, tenant_uuid)


class FuncKeyTemplateEditedEvent(TenantEvent):
    """Event for when a function key template is edited."""

    service = "confd"
    name = "func_key_template_edited"
    routing_key_fmt = "config.funckey.template.edited"

    def __init__(self, template_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            template_id (int): template ID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"id": template_id}
        super().__init__(content, tenant_uuid)
