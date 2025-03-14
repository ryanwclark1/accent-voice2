# resources/func_key/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class FuncKeyEvent(TenantEvent):
    """Base class for Func Key events."""

    service: ClassVar[str] = "confd"
    content: dict


class FuncKeyTemplateCreatedEvent(FuncKeyEvent):
    """Event for when a func key template is created."""

    name: ClassVar[str] = "func_key_template_created"
    routing_key_fmt: ClassVar[str] = "config.funckey.template.created"

    def __init__(self, template_id: int, **data):
        content = {"id": template_id}
        super().__init__(content=content, **data)


class FuncKeyTemplateDeletedEvent(FuncKeyEvent):
    """Event for when a func key template is deleted."""

    name: ClassVar[str] = "func_key_template_deleted"
    routing_key_fmt: ClassVar[str] = "config.funckey.template.deleted"

    def __init__(self, template_id: int, **data):
        content = {"id": template_id}
        super().__init__(content=content, **data)


class FuncKeyTemplateEditedEvent(FuncKeyEvent):
    """Event for when a func key template is edited."""

    name: ClassVar[str] = "func_key_template_edited"
    routing_key_fmt: ClassVar[str] = "config.funckey.template.edited"

    def __init__(self, template_id: int, **data):
        content = {"id": template_id}
        super().__init__(content=content, **data)
