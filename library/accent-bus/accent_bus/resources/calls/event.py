# accent_bus/resources/calls/event.py
# Copyright 2025 Accent Communications

"""Call events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr

from .types import CallDict, RelocateDict, TransferDict


class CallCreatedEvent(UserEvent):
    """Event for when a call is created."""

    service = "calld"
    name = "call_created"
    routing_key_fmt = "calls.call.created"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call: CallDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           call: Call
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        super().__init__(call, tenant_uuid, user_uuid)


class CallEndedEvent(UserEvent):
    """Event for when a call ends."""

    service = "calld"
    name = "call_ended"
    routing_key_fmt = "calls.call.ended"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call: CallDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call: Call
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(call, tenant_uuid, user_uuid)


class CallUpdatedEvent(UserEvent):
    """Event for when a call is updated."""

    service = "calld"
    name = "call_updated"
    routing_key_fmt = "calls.call.updated"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call: CallDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call: Call
          tenant_uuid:  tenant UUID
          user_uuid: user UUID

        """
        super().__init__(call, tenant_uuid, user_uuid)


class CallAnsweredEvent(UserEvent):
    """Event for when a call is answered."""

    service = "calld"
    name = "call_answered"
    routing_key_fmt = "calls.call.answered"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call: CallDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call: Call
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(call, tenant_uuid, user_uuid)


class CallDTMFEvent(UserEvent):
    """Event for when a DTMF is received on a call."""

    service = "calld"
    name = "call_dtmf_created"
    routing_key_fmt = "calls.dtmf.created"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call_id: str,
        digit_number: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           call_id: Call ID
           digit_number: DTMF Digit
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "call_id": call_id,
            "digit": digit_number,
            "user_uuid": str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class CallHeldEvent(UserEvent):
    """Event for when a call is held."""

    service = "calld"
    name = "call_held"
    routing_key_fmt = "calls.hold.created"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call_id: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          call_id: Call ID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {
            "call_id": call_id,
            "user_uuid": str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class CallResumedEvent(UserEvent):
    """Event for when a call is resumed."""

    service = "calld"
    name = "call_resumed"
    routing_key_fmt = "calls.hold.deleted"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call_id: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call_id: Call ID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {
            "call_id": call_id,
            "user_uuid": str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class MissedCallEvent(UserEvent):
    """Event for when a call is missed."""

    service = "calld"
    name = "user_missed_call"
    routing_key_fmt = "calls.missed"
    required_acl_fmt = "events.calls.{user_uuid}"

    def __init__(
        self,
        call: CallDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          call: Call
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(call, tenant_uuid, user_uuid)


class CallRelocateInitiatedEvent(UserEvent):
    """Event for when a call relocation is initiated."""

    service = "calld"
    name = "relocate_initiated"
    routing_key_fmt = "calls.relocate.created"
    required_acl_fmt = "events.relocates.{user_uuid}"

    def __init__(
        self,
        relocate: RelocateDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           relocate: Relocate data
           tenant_uuid:  tenant UUID
           user_uuid: user UUID

        """
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallRelocateAnsweredEvent(UserEvent):
    """Event for when a call relocation is answered."""

    service = "calld"
    name = "relocate_answered"
    routing_key_fmt = "calls.relocate.edited"
    required_acl_fmt = "events.relocates.{user_uuid}"

    def __init__(
        self,
        relocate: RelocateDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           relocate: Relocate data
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallRelocateCompletedEvent(UserEvent):
    """Event for when a call relocation is completed."""

    service = "calld"
    name = "relocate_completed"
    routing_key_fmt = "calls.relocate.edited"
    required_acl_fmt = "events.relocates.{user_uuid}"

    def __init__(
        self,
        relocate: RelocateDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           relocate: Relocate data
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallRelocateEndedEvent(UserEvent):
    """Event for when a call relocation is ended."""

    service = "calld"
    name = "relocate_ended"
    routing_key_fmt = "calls.relocate.deleted"
    required_acl_fmt = "events.relocates.{user_uuid}"

    def __init__(
        self,
        relocate: RelocateDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          relocate: Relocate data
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallTransferCreatedEvent(UserEvent):
    """Event for when a call transfer is created."""

    service = "calld"
    name = "transfer_created"
    routing_key_fmt = "calls.transfer.created"
    required_acl_fmt = "events.transfers.{user_uuid}"

    def __init__(
        self,
        transfer: TransferDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          transfer: Transfer
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferUpdatedEvent(UserEvent):
    """Event for when a call transfer is updated."""

    service = "calld"
    name = "transfer_updated"
    routing_key_fmt = "calls.transfer.created"
    required_acl_fmt = "events.transfers.{user_uuid}"

    def __init__(
        self,
        transfer: TransferDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           transfer: Transfer
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferAnsweredEvent(UserEvent):
    """Event for when a call transfer is answered."""

    service = "calld"
    name = "transfer_answered"
    routing_key_fmt = "calls.transfer.edited"
    required_acl_fmt = "events.transfers.{user_uuid}"

    def __init__(
        self,
        transfer: TransferDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            transfer (TransferDict):  transfer details.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferCancelledEvent(UserEvent):
    """Event for when a call transfer is cancelled."""

    service = "calld"
    name = "transfer_cancelled"
    routing_key_fmt = "calls.transfer.edited"
    required_acl_fmt = "events.transfers.{user_uuid}"

    def __init__(
        self,
        transfer: TransferDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            transfer (TransferDict):  transfer details.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferCompletedEvent(UserEvent):
    """Event for when a call transfer is completed."""

    service = "calld"
    name = "transfer_completed"
    routing_key_fmt = "calls.transfer.edited"
    required_acl_fmt = "events.transfers.{user_uuid}"

    def __init__(
        self,
        transfer: TransferDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
           transfer: Transfer
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferAbandonedEvent(UserEvent):
    """Event for when a call transfer is abandoned."""

    service = "calld"
    name = "transfer_abandoned"
    routing_key_fmt = "calls.transfer.edited"
    required_acl_fmt = "events.transfers.{user_uuid}"

    def __init__(
        self,
        transfer: TransferDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           transfer: Transfer
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferEndedEvent(UserEvent):
    """Event for when a call transfer is ended."""

    service = "calld"
    name = "transfer_ended"
    routing_key_fmt = "calls.transfer.deleted"
    required_acl_fmt = "events.transfers.{user_uuid}"

    def __init__(
        self,
        transfer: TransferDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          transfer: Transfer
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(transfer, tenant_uuid, user_uuid)
