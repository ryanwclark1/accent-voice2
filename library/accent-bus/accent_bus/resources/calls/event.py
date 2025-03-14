# resources/calls/event.py
from typing import ClassVar

from resources.common.event import UserEvent

from .types import CallDict, RelocateDict, TransferDict


class CallEvent(UserEvent):
    """Base class for Call events."""

    service: ClassVar[str] = "calld"
    required_acl_fmt: ClassVar[str] = "events.calls.{user_uuid}"
    content: dict


class CallCreatedEvent(CallEvent):
    """Event for when a call is created."""

    name: ClassVar[str] = "call_created"
    routing_key_fmt: ClassVar[str] = "calls.call.created"

    # required_acl_fmt: ClassVar[str] = "events.calls.{user_uuid}" # Already defined
    def __init__(self, call: CallDict, **data):
        super().__init__(content=call, **data)


class CallEndedEvent(CallEvent):
    """Event for when a call ends."""

    name: ClassVar[str] = "call_ended"
    routing_key_fmt: ClassVar[str] = "calls.call.ended"

    def __init__(self, call: CallDict, **data):
        super().__init__(content=call, **data)


class CallUpdatedEvent(CallEvent):
    """Event for when a call is updated."""

    name: ClassVar[str] = "call_updated"
    routing_key_fmt: ClassVar[str] = "calls.call.updated"

    def __init__(self, call: CallDict, **data):
        super().__init__(content=call, **data)


class CallAnsweredEvent(CallEvent):
    """Event for when a call is answered."""

    name: ClassVar[str] = "call_answered"
    routing_key_fmt: ClassVar[str] = "calls.call.answered"

    def __init__(self, call: CallDict, **data):
        super().__init__(content=call, **data)


class CallDTMFEvent(CallEvent):
    """Event for when a DTMF digit is received on a call."""

    name: ClassVar[str] = "call_dtmf_created"
    routing_key_fmt: ClassVar[str] = "calls.dtmf.created"

    def __init__(self, call_id: str, digit_number: str, **data):
        content = {
            "call_id": call_id,
            "digit": digit_number,
            "user_uuid": str(data["user_uuid"]),
        }
        super().__init__(content=content, **data)


class CallHeldEvent(CallEvent):
    """Event for when a call is put on hold."""

    name: ClassVar[str] = "call_held"
    routing_key_fmt: ClassVar[str] = "calls.hold.created"

    def __init__(self, call_id: str, **data):
        content = {
            "call_id": call_id,
            "user_uuid": str(data["user_uuid"]),
        }
        super().__init__(content=content, **data)


class CallResumedEvent(CallEvent):
    """Event for when a call is resumed from hold."""

    name: ClassVar[str] = "call_resumed"
    routing_key_fmt: ClassVar[str] = "calls.hold.deleted"

    def __init__(self, call_id: str, **data):
        content = {
            "call_id": call_id,
            "user_uuid": str(data["user_uuid"]),
        }
        super().__init__(content=content, **data)


class MissedCallEvent(CallEvent):
    """Event for when a call is missed."""

    name: ClassVar[str] = "user_missed_call"
    routing_key_fmt: ClassVar[str] = "calls.missed"

    def __init__(self, call: CallDict, **data):
        super().__init__(content=call, **data)


class CallRelocateInitiatedEvent(CallEvent):
    """Event for when a call relocation is initiated."""

    name: ClassVar[str] = "relocate_initiated"
    routing_key_fmt: ClassVar[str] = "calls.relocate.created"
    required_acl_fmt: ClassVar[str] = (
        "events.relocates.{user_uuid}"  # Override, different prefix.
    )

    def __init__(self, relocate: RelocateDict, **data):
        super().__init__(content=relocate, **data)


class CallRelocateAnsweredEvent(CallEvent):
    """Event for when a relocated call is answered."""

    name: ClassVar[str] = "relocate_answered"
    routing_key_fmt: ClassVar[str] = "calls.relocate.edited"
    required_acl_fmt: ClassVar[str] = "events.relocates.{user_uuid}"

    def __init__(self, relocate: RelocateDict, **data):
        super().__init__(content=relocate, **data)


class CallRelocateCompletedEvent(CallEvent):
    """Event for when a call relocation is completed."""

    name: ClassVar[str] = "relocate_completed"
    routing_key_fmt: ClassVar[str] = "calls.relocate.edited"
    required_acl_fmt: ClassVar[str] = "events.relocates.{user_uuid}"

    def __init__(self, relocate: RelocateDict, **data):
        super().__init__(content=relocate, **data)


class CallRelocateEndedEvent(CallEvent):
    """Event for when a call relocation ends."""

    name: ClassVar[str] = "relocate_ended"
    routing_key_fmt: ClassVar[str] = "calls.relocate.deleted"
    required_acl_fmt: ClassVar[str] = "events.relocates.{user_uuid}"

    def __init__(self, relocate: RelocateDict, **data):
        super().__init__(content=relocate, **data)


class CallTransferCreatedEvent(CallEvent):
    """Event for when a call transfer is created."""

    name: ClassVar[str] = "transfer_created"
    routing_key_fmt: ClassVar[str] = "calls.transfer.created"
    required_acl_fmt: ClassVar[str] = "events.transfers.{user_uuid}"

    def __init__(self, transfer: TransferDict, **data):
        super().__init__(content=transfer, **data)


class CallTransferUpdatedEvent(CallEvent):
    """Event for when a call transfer is updated."""

    name: ClassVar[str] = "transfer_updated"
    routing_key_fmt: ClassVar[str] = "calls.transfer.created"  # Same as created
    required_acl_fmt: ClassVar[str] = "events.transfers.{user_uuid}"

    def __init__(self, transfer: TransferDict, **data):
        super().__init__(content=transfer, **data)


class CallTransferAnsweredEvent(CallEvent):
    """Event for when a transferred call is answered."""

    name: ClassVar[str] = "transfer_answered"
    routing_key_fmt: ClassVar[str] = "calls.transfer.edited"
    required_acl_fmt: ClassVar[str] = "events.transfers.{user_uuid}"

    def __init__(self, transfer: TransferDict, **data):
        super().__init__(content=transfer, **data)


class CallTransferCancelledEvent(CallEvent):
    """Event for when a call transfer is cancelled."""

    name: ClassVar[str] = "transfer_cancelled"
    routing_key_fmt: ClassVar[str] = "calls.transfer.edited"  # Same as answered
    required_acl_fmt: ClassVar[str] = "events.transfers.{user_uuid}"

    def __init__(self, transfer: TransferDict, **data):
        super().__init__(content=transfer, **data)


class CallTransferCompletedEvent(CallEvent):
    """Event for when a call transfer is completed."""

    name: ClassVar[str] = "transfer_completed"
    routing_key_fmt: ClassVar[str] = "calls.transfer.edited"  # Same as answered
    required_acl_fmt: ClassVar[str] = "events.transfers.{user_uuid}"

    def __init__(self, transfer: TransferDict, **data):
        super().__init__(content=transfer, **data)


class CallTransferAbandonedEvent(CallEvent):
    """Event for when a call transfer is abandoned."""

    name: ClassVar[str] = "transfer_abandoned"
    routing_key_fmt: ClassVar[str] = "calls.transfer.edited"  # Same as answered
    required_acl_fmt: ClassVar[str] = "events.transfers.{user_uuid}"

    def __init__(self, transfer: TransferDict, **data):
        super().__init__(content=transfer, **data)


class CallTransferEndedEvent(CallEvent):
    """Event for when a call transfer ends."""

    name: ClassVar[str] = "transfer_ended"
    routing_key_fmt: ClassVar[str] = "calls.transfer.deleted"
    required_acl_fmt: ClassVar[str] = "events.transfers.{user_uuid}"

    def __init__(self, transfer: TransferDict, **data):
        super().__init__(content=transfer, **data)
