# accent_bus/resources/adhoc_conference/event.py
# Copyright 2025 Accent Communications

"""Adhoc conference events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class AdhocConferenceCreatedEvent(UserEvent):
    """Event for when an adhoc conference is created."""

    name = "conference_adhoc_created"
    routing_key_fmt = "conferences.users.{user_uuid}.adhoc.created"
    service = "calld"

    def __init__(
        self,
        conference_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           conference_id (int): Conference ID
           tenant_uuid (UUIDStr): tenant UUID
           user_uuid (UUIDStr): user UUID

        """
        content = {"conference_id": conference_id}
        super().__init__(content, tenant_uuid, user_uuid)


class AdhocConferenceDeletedEvent(UserEvent):
    """Event for when an adhoc conference is deleted."""

    name = "conference_adhoc_deleted"
    routing_key_fmt = "conferences.users.{user_uuid}.adhoc.deleted"
    service = "calld"

    def __init__(
        self,
        conference_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            conference_id (int): Conference ID.
            tenant_uuid (UUIDStr): tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = {"conference_id": conference_id}
        super().__init__(content, tenant_uuid, user_uuid)


class AdhocConferenceParticipantJoinedEvent(UserEvent):
    """Event for when a participant joins an adhoc conference."""

    name = "conference_adhoc_participant_joined"
    routing_key_fmt = "conferences.users.{user_uuid}.adhoc.participants.joined"
    service = "calld"

    def __init__(
        self,
        conference_id: int,
        call_id: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            conference_id (int): The conference ID.
            call_id (str): call ID.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        content = {"conference_id": conference_id, "call_id": call_id}
        super().__init__(content, tenant_uuid, user_uuid)


class AdhocConferenceParticipantLeftEvent(UserEvent):
    """Event for when a participant leaves an adhoc conference."""

    name = "conference_adhoc_participant_left"
    routing_key_fmt = "conferences.users.{user_uuid}.adhoc.participants.left"
    service = "calld"

    def __init__(
        self,
        conference_id: int,
        call_id: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            conference_id: Conference ID
            call_id: Call ID
            tenant_uuid: Tenant UUID
            user_uuid: User UUID

        """
        content = {"conference_id": conference_id, "call_id": call_id}
        super().__init__(content, tenant_uuid, user_uuid)
