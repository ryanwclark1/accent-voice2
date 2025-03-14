# accent_bus/resources/calls/parking.py
# Copyright 2025 Accent Communications

"""Call parking events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import TenantEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr

    from .types import ParkedCallDict, ParkedCallTimedOutDict, UnparkedCallDict


class CallParkedEvent(TenantEvent):
    """Event for when a call is parked."""

    service = "calld"
    name = "call_parked"
    routing_key_fmt = "parkings.{parking_id}.calls.updated"
    required_acl_fmt = "events.parkings.{parking_id}.calls.updated"

    def __init__(self, parked_call: ParkedCallDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            parked_call (ParkedCallDict): parked call.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(parked_call, tenant_uuid)


class CallUnparkedEvent(TenantEvent):
    """Event for when a call is unparked."""

    service = "calld"
    name = "call_unparked"
    routing_key_fmt = "parkings.{parking_id}.calls.updated"
    required_acl_fmt = "events.parkings.{parking_id}.calls.updated"

    def __init__(self, unparked_call: UnparkedCallDict, tenant_uuid: str) -> None:
        """Initialize the event.

        Args:
           unparked_call: Unparked Call
           tenant_uuid: tenant UUID

        """
        super().__init__(unparked_call, tenant_uuid)


class ParkedCallHungupEvent(TenantEvent):
    """Event for when a parked call is hung up."""

    service = "calld"
    name = "parked_call_hungup"
    routing_key_fmt = "parkings.{parking_id}.calls.updated"
    required_acl_fmt = "events.parkings.{parking_id}.calls.updated"

    def __init__(self, parked_call: ParkedCallDict, tenant_uuid: str) -> None:
        """Initialize event.

        Args:
            parked_call (ParkedCallDict): parked call
            tenant_uuid (str): tenant UUID

        """
        super().__init__(parked_call, tenant_uuid)


class ParkedCallTimedOutEvent(TenantEvent):
    """Event for when a parked call times out."""

    service = "calld"
    name = "parked_call_timed_out"
    routing_key_fmt = "parkings.{parking_id}.calls.updated"
    required_acl_fmt = "events.parkings.{parking_id}.calls.updated"

    def __init__(self, parked_call: ParkedCallTimedOutDict, tenant_uuid: str) -> None:
        """Initialize event.

        Args:
           parked_call: Parked Call
           tenant_uuid: tenant UUID

        """
        super().__init__(parked_call, tenant_uuid)
