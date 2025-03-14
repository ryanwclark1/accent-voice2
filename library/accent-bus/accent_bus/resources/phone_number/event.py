# accent_bus/resources/phone_number/event.py
# Copyright 2025 Accent Communications
from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import TenantEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr

    from .types import PhoneNumberDict


class PhoneNumberCreatedEvent(TenantEvent):
    """Event for creation of a phone number."""

    service = "confd"
    name = "phone_number_created"
    routing_key_fmt = "config.phone_number.created"

    def __init__(self, phone_number: PhoneNumberDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          phone_number: Phone Number
          tenant_uuid: tenant UUID

        """
        super().__init__(phone_number, tenant_uuid)


class PhoneNumberDeletedEvent(TenantEvent):
    """Event for deletion of a phone number."""

    service = "confd"
    name = "phone_number_deleted"
    routing_key_fmt = "config.phone_number.deleted"

    def __init__(self, phone_number: PhoneNumberDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            phone_number (PhoneNumberDict): phone number.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        super().__init__(phone_number, tenant_uuid)


class PhoneNumberEditedEvent(TenantEvent):
    """Event for when a phone number is edited."""

    service = "confd"
    name = "phone_number_edited"
    routing_key_fmt = "config.phone_number.edited"

    def __init__(self, phone_number: PhoneNumberDict, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
           phone_number: Phone Number
           tenant_uuid: tenant UUID

        """
        super().__init__(phone_number, tenant_uuid)


class PhoneNumberMainUpdatedEvent(TenantEvent):
    """Event for when a main phone number is updated."""

    service = "confd"
    name = "phone_number_main_updated"
    routing_key_fmt = "config.phone_number.main.updated"

    def __init__(
        self,
        current_main_uuid: str | None,
        new_main_uuid: str | None,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            current_main_uuid (str): Current main phone number UUID.
            new_main_uuid (str): New main phone number UUID.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(
            {"current_main_uuid": current_main_uuid, "new_main_uuid": new_main_uuid},
            tenant_uuid,
        )
