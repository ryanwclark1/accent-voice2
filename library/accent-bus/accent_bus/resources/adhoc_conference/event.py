# resources/adhoc_conference/event.py
from typing import ClassVar

from accent_bus.resources.common.event import UserEvent  # Import UserEvent


class AdhocConferenceEvent(UserEvent):  # Inherit from UserEvent
    """Base class for Adhoc Conference events."""

    service: ClassVar[str] = "calld"
    # tenant_uuid and user_uuid are already in UserEvent
    content: dict


class AdhocConferenceCreatedEvent(AdhocConferenceEvent):
    """Event for when an adhoc conference is created."""

    name: ClassVar[str] = "conference_adhoc_created"
    routing_key_fmt: ClassVar[str] = "conferences.users.{user_uuid}.adhoc.created"

    def __init__(self, conference_id: int, **data):
        content = {"conference_id": conference_id}
        super().__init__(content=content, **data)


class AdhocConferenceDeletedEvent(AdhocConferenceEvent):
    """Event for when an adhoc conference is deleted."""

    name: ClassVar[str] = "conference_adhoc_deleted"
    routing_key_fmt: ClassVar[str] = "conferences.users.{user_uuid}.adhoc.deleted"

    def __init__(self, conference_id: int, **data):
        content = {"conference_id": conference_id}
        super().__init__(content=content, **data)


class AdhocConferenceParticipantJoinedEvent(AdhocConferenceEvent):
    """Event for when a participant joins an adhoc conference."""

    name: ClassVar[str] = "conference_adhoc_participant_joined"
    routing_key_fmt: ClassVar[str] = (
        "conferences.users.{user_uuid}.adhoc.participants.joined"
    )

    def __init__(self, conference_id: int, call_id: str, **data):
        content = {"conference_id": conference_id, "call_id": call_id}
        super().__init__(content=content, **data)


class AdhocConferenceParticipantLeftEvent(AdhocConferenceEvent):
    """Event for when a participant leaves an adhoc conference."""

    name: ClassVar[str] = "conference_adhoc_participant_left"
    routing_key_fmt: ClassVar[str] = (
        "conferences.users.{user_uuid}.adhoc.participants.left"
    )

    def __init__(self, conference_id: int, call_id: str, **data):
        content = {"conference_id": conference_id, "call_id": call_id}
        super().__init__(content=content, **data)
