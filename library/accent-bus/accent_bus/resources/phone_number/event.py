# resources/phone_number/event.py
from typing import ClassVar

from pydantic import BaseModel

from accent_bus.resources.common.event import TenantEvent

from .types import PhoneNumberDict


class PhoneNumberEvent(TenantEvent):
    """Base class for Phone Number events."""

    service: ClassVar[str] = "confd"
    content: dict


class PhoneNumberCreatedEvent(PhoneNumberEvent):
    """Event for when a phone number is created."""

    name: ClassVar[str] = "phone_number_created"
    routing_key_fmt: ClassVar[str] = "config.phone_number.created"

    def __init__(self, phone_number: PhoneNumberDict, **data):
        super().__init__(content=phone_number, **data)


class PhoneNumberDeletedEvent(PhoneNumberEvent):
    """Event for when a phone number is deleted."""

    name: ClassVar[str] = "phone_number_deleted"
    routing_key_fmt: ClassVar[str] = "config.phone_number.deleted"

    def __init__(self, phone_number: PhoneNumberDict, **data):
        super().__init__(content=phone_number, **data)


class PhoneNumberEditedEvent(PhoneNumberEvent):
    """Event for when a phone number is edited."""

    name: ClassVar[str] = "phone_number_edited"
    routing_key_fmt: ClassVar[str] = "config.phone_number.edited"

    def __init__(self, phone_number: PhoneNumberDict, **data):
        super().__init__(content=phone_number, **data)


class PhoneNumberMainUpdatedContent(BaseModel):
    current_main_uuid: str | None = None
    new_main_uuid: str | None = None


class PhoneNumberMainUpdatedEvent(PhoneNumberEvent):
    """Event for when the main phone number is updated."""

    name: ClassVar[str] = "phone_number_main_updated"
    routing_key_fmt: ClassVar[str] = "config.phone_number.main.updated"
    content: PhoneNumberMainUpdatedContent

    def __init__(
        self, current_main_uuid: str | None, new_main_uuid: str | None, **data
    ):
        content = PhoneNumberMainUpdatedContent(
            current_main_uuid=current_main_uuid, new_main_uuid=new_main_uuid
        )
        super().__init__(content=content.model_dump(), **data)
