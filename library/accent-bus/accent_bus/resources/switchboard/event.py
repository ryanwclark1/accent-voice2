# resources/switchboard/event.py
from typing import Any, ClassVar

from pydantic import UUID4
from resources.common.event import MultiUserEvent, TenantEvent

from .types import (
    HeldCallDict,
    QueuedCallDict,
    SwitchboardDict,
    SwitchboardFallbackDict,
)


class SwitchboardEvent(TenantEvent):
    """Base class for Switchboard events.

    Args:
        switchboard_uuid (UUID4): The UUID of the switchboard.

    """

    service: ClassVar[str] = "confd"
    content: dict
    switchboard_uuid: str
    required_acl_fmt: ClassVar[str] = "switchboards.{switchboard_uuid}.{verb}"

    def __init__(
        self,
        content: dict,
        switchboard_uuid: UUID4,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(content, *args, **kwargs)
        if switchboard_uuid is None:
            raise ValueError("switchboard_uuid must have a value")
        self.switchboard_uuid = str(switchboard_uuid)


class SwitchboardCreatedEvent(SwitchboardEvent):
    """Event for when a switchboard is created."""

    name: ClassVar[str] = "switchboard_created"
    routing_key_fmt: ClassVar[str] = "config.switchboards.{switchboard_uuid}.created"

    def __init__(self, switchboard: SwitchboardDict, **data):
        super().__init__(
            content=switchboard, switchboard_uuid=switchboard["uuid"], **data
        )


class SwitchboardDeletedEvent(SwitchboardEvent):
    """Event for when a switchboard is deleted."""

    name: ClassVar[str] = "switchboard_deleted"
    routing_key_fmt: ClassVar[str] = "config.switchboards.{switchboard_uuid}.deleted"

    def __init__(self, switchboard: SwitchboardDict, **data):
        super().__init__(
            content=switchboard, switchboard_uuid=switchboard["uuid"], **data
        )


class SwitchboardEditedEvent(SwitchboardEvent):
    """Event for when a switchboard is edited."""

    name: ClassVar[str] = "switchboard_edited"
    routing_key_fmt: ClassVar[str] = "config.switchboards.{switchboard_uuid}.edited"

    def __init__(self, switchboard: SwitchboardDict, **data):
        super().__init__(
            content=switchboard, switchboard_uuid=switchboard["uuid"], **data
        )


class SwitchboardFallbackEditedEvent(SwitchboardEvent):
    """Event for switchboard fallback is edited."""

    name: ClassVar[str] = "switchboard_fallback_edited"
    routing_key_fmt: ClassVar[str] = "config.switchboards.fallbacks.edited"
    required_acl_fmt: ClassVar[str] = (
        "switchboards.fallbacks.edited"  # No switchboard_uuid
    )

    def __init__(self, fallback: SwitchboardFallbackDict, **data):
        super().__init__(
            content=fallback, switchboard_uuid=data["switchboard_uuid"], **data
        )


class SwitchboardMemberUserAssociatedEvent(
    SwitchboardEvent, MultiUserEvent
):  # Multiple inheritance
    """Event for when a user is associated as a member of a switchboard."""

    name: ClassVar[str] = "switchboard_member_user_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.switchboards.{switchboard_uuid}.members.users.updated"
    )

    def __init__(
        self,
        switchboard_uuid: UUID4,
        user_uuids: list[str],
        **data,
    ):
        content = {
            "switchboard_uuid": str(switchboard_uuid),
            "users": [{"uuid": str(uuid)} for uuid in user_uuids],
        }
        super().__init__(
            content=content,
            switchboard_uuid=switchboard_uuid,
            user_uuids=user_uuids,
            **data,
        )


class SwitchboardQueuedCallsUpdatedEvent(SwitchboardEvent):
    """Event for when the queued calls on a switchboard are updated."""

    service: ClassVar[str] = "calld"  # Different service.
    name: ClassVar[str] = "switchboard_queued_calls_updated"
    routing_key_fmt: ClassVar[str] = (
        "switchboards.{switchboard_uuid}.calls.queued.updated"
    )
    required_acl_fmt: ClassVar[str] = (
        "events.switchboards.{switchboard_uuid}.calls.queued.updated"
    )

    def __init__(self, items: list[QueuedCallDict], **data):
        content = {
            "switchboard_uuid": str(data["switchboard_uuid"]),
            "items": items,
        }
        super().__init__(
            content=content, switchboard_uuid=data["switchboard_uuid"], **data
        )


class SwitchboardQueuedCallAnsweredEvent(SwitchboardEvent):
    """Event for when a queued call on a switchboard is answered."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "switchboard_queued_call_answered"
    routing_key_fmt: ClassVar[str] = (
        "switchboards.{switchboard_uuid}.calls.queued.{queued_call_id}.answer.updated"
    )
    required_acl_fmt: ClassVar[str] = (
        "events.switchboards.{switchboard_uuid}.calls.queued.{queued_call_id}.answer.updated"
    )

    def __init__(self, operator_call_id: str, queued_call_id: str, **data):
        content = {
            "switchboard_uuid": str(data["switchboard_uuid"]),
            "operator_call_id": operator_call_id,
            "queued_call_id": queued_call_id,
        }
        super().__init__(
            content=content, switchboard_uuid=data["switchboard_uuid"], **data
        )


class SwitchboardHeldCallsUpdatedEvent(SwitchboardEvent):
    """Event for when the held calls on a switchboard are updated."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "switchboard_held_calls_updated"
    routing_key_fmt: ClassVar[str] = (
        "switchboards.{switchboard_uuid}.calls.held.updated"
    )
    required_acl_fmt: ClassVar[str] = (
        "events.switchboards.{switchboard_uuid}.calls.held.updated"
    )

    def __init__(self, items: list[HeldCallDict], **data):
        content = {
            "switchboard_uuid": str(data["switchboard_uuid"]),
            "items": items,
        }
        super().__init__(
            content=content, switchboard_uuid=data["switchboard_uuid"], **data
        )


class SwitchboardHeldCallAnsweredEvent(SwitchboardEvent):
    """Event for when a held call on a switchboard is answered."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "switchboard_held_call_answered"
    routing_key_fmt: ClassVar[str] = (
        "switchboards.{switchboard_uuid}.calls.held.{held_call_id}.answer.updated"
    )
    required_acl_fmt: ClassVar[str] = (
        "events.switchboards.{switchboard_uuid}.calls.held.{held_call_id}.answer.updated"
    )

    def __init__(self, operator_call_id: str, held_call_id: str, **data):
        content = {
            "switchboard_uuid": str(data["switchboard_uuid"]),
            "operator_call_id": operator_call_id,
            "held_call_id": held_call_id,
        }
        super().__init__(
            content=content, switchboard_uuid=data["switchboard_uuid"], **data
        )
