# resources/calls/parking.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import ParkedCallDict, ParkedCallTimedOutDict, UnparkedCallDict


class CallParkingEvent(TenantEvent):
    """Base class for Call Parking events."""

    service: ClassVar[str] = "calld"
    required_acl_fmt: ClassVar[str] = "events.parkings.{parking_id}.calls.updated"
    content: dict


class CallParkedEvent(CallParkingEvent):
    """Event for when a call is parked."""

    name: ClassVar[str] = "call_parked"
    routing_key_fmt: ClassVar[str] = "parkings.{parking_id}.calls.updated"
    content: ParkedCallDict

    def __init__(self, parked_call: ParkedCallDict, **data):
        super().__init__(content=parked_call, **data)


class CallUnparkedEvent(CallParkingEvent):
    """Event for when a call is unparked."""

    name: ClassVar[str] = "call_unparked"
    routing_key_fmt: ClassVar[str] = "parkings.{parking_id}.calls.updated"
    content: UnparkedCallDict

    def __init__(self, unparked_call: UnparkedCallDict, **data):
        super().__init__(content=unparked_call, **data)


class ParkedCallHungupEvent(CallParkingEvent):
    """Event for when a parked call is hung up."""

    name: ClassVar[str] = "parked_call_hungup"
    routing_key_fmt: ClassVar[str] = "parkings.{parking_id}.calls.updated"
    content: ParkedCallDict

    def __init__(self, parked_call: ParkedCallDict, **data):
        super().__init__(content=parked_call, **data)


class ParkedCallTimedOutEvent(CallParkingEvent):
    """Event for when a parked call times out."""

    name: ClassVar[str] = "parked_call_timed_out"
    routing_key_fmt: ClassVar[str] = "parkings.{parking_id}.calls.updated"
    content: ParkedCallTimedOutDict

    def __init__(self, parked_call: ParkedCallTimedOutDict, **data):
        super().__init__(content=parked_call, **data)
