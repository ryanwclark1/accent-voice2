# accent_bus/resources/conference/event.py
# Copyright 2025 Accent Communications

"""Conference events."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from accent_bus.resources.common.event import MultiUserEvent, TenantEvent, UserEvent

if TYPE_CHECKING:
    from collections.abc import Mapping

    from accent_bus.resources.common.types import UUIDStr

    from .types import ParticipantDict


class _ConferenceMixin:
    """Mixin for conference-related events."""

    def __init__(self, content: Mapping, conference_id: int, *args: Any) -> None:
        super().__init__(content, *args)  # type: ignore[call-arg]
        if not conference_id:
            msg = "conference_id must have a value"
            raise ValueError(msg)
        self.conference_id = conference_id


class ConferenceCreatedEvent(_ConferenceMixin, TenantEvent):
    """Event for when a conference is created."""

    service = "confd"
    name = "conference_created"
    routing_key_fmt = "config.conferences.created"

    def __init__(self, conference_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           conference_id: Conference ID
           tenant_uuid: tenant UUID

        """
        content = {"id": conference_id}
        super().__init__(content, conference_id, tenant_uuid)


class ConferenceDeletedEvent(_ConferenceMixin, TenantEvent):
    """Event for when a conference is deleted."""

    service = "confd"
    name = "conference_deleted"
    routing_key_fmt = "config.conferences.deleted"

    def __init__(self, conference_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            conference_id (int): The ID of the conference.
            tenant_uuid (UUIDStr): tenant UUID

        """
        content = {"id": conference_id}
        super().__init__(content, conference_id, tenant_uuid)


class ConferenceEditedEvent(_ConferenceMixin, TenantEvent):
    """Event for when a conference is edited."""

    service = "confd"
    name = "conference_edited"
    routing_key_fmt = "config.conferences.edited"

    def __init__(self, conference_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           conference_id: Conference ID
           tenant_uuid: tenant UUID

        """
        content = {"id": conference_id}
        super().__init__(content, conference_id, tenant_uuid)


class ConferenceRecordStartedEvent(_ConferenceMixin, TenantEvent):
    """Event for when conference recording starts."""

    service = "calld"
    name = "conference_record_started"
    routing_key_fmt = "conferences.{id}.record"

    def __init__(self, conference_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            conference_id (int): conference ID.
            tenant_uuid (UUIDStr):  tenant UUID

        """
        content = {"id": conference_id}
        super().__init__(content, conference_id, tenant_uuid)


class ConferenceRecordStoppedEvent(_ConferenceMixin, TenantEvent):
    """Event for when conference recording stops."""

    service = "calld"
    name = "conference_record_stopped"
    routing_key_fmt = "conferences.{id}.record"

    def __init__(self, conference_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           conference_id: Conference ID
           tenant_uuid: tenant UUID

        """
        content = {"id": conference_id}
        super().__init__(content, conference_id, tenant_uuid)


class ConferenceParticipantJoinedEvent(_ConferenceMixin, MultiUserEvent):
    """Event for when a participant joins a conference."""

    service = "calld"
    name = "conference_participant_joined"
    routing_key_fmt = "conferences.{conference_id}.participants.joined"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuids: list[str],
    ) -> None:
        """Initialize event.

        Args:
           conference_id: Conference ID
           participant: Participant
           tenant_uuid: tenant UUID
           user_uuids: List of User UUIDs

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuids)


class ConferenceParticipantLeftEvent(_ConferenceMixin, MultiUserEvent):
    """Event for when a participant leaves a conference."""

    service = "calld"
    name = "conference_participant_left"
    routing_key_fmt = "conferences.{conference_id}.participants.left"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuids: list[str],
    ) -> None:
        """Initialize event.

        Args:
           conference_id: Conference ID
           participant: Participant
           tenant_uuid: tenant UUID
           user_uuids: List of User UUID

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuids)


class ConferenceParticipantMutedEvent(_ConferenceMixin, TenantEvent):
    """Event for when a participant is muted in a conference."""

    service = "calld"
    name = "conference_participant_muted"
    routing_key_fmt = "conferences.{conference_id}.participants.mute"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            conference_id (int):  conference ID.
            participant (ParticipantDict): participant details.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid)


class ConferenceParticipantUnmutedEvent(_ConferenceMixin, TenantEvent):
    """Event for when a participant is unmuted in a conference."""

    service = "calld"
    name = "conference_participant_unmuted"
    routing_key_fmt = "conferences.{conference_id}.particpants.mute"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           conference_id: Conference ID
           participant: Participant
           tenant_uuid: tenant UUID

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid)


class ConferenceParticipantTalkStartedEvent(_ConferenceMixin, MultiUserEvent):
    """Event for when a participant starts talking in a conference."""

    service = "calld"
    name = "conference_participant_talk_started"
    routing_key_fmt = "conferences.{conference_id}.participants.talk"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuids: list[str],
    ) -> None:
        """Initialize Event.

        Args:
           conference_id: Conference ID
           participant: Participant
           tenant_uuid: tenant UUID
           user_uuids: list of user UUIDs

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuids)


class ConferenceParticipantTalkStoppedEvent(_ConferenceMixin, MultiUserEvent):
    """Event for when a participant stops talking in a conference."""

    service = "calld"
    name = "conference_participant_talk_stopped"
    routing_key_fmt = "conferences.{conference_id}.participants.talk"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuids: list[str],
    ) -> None:
        """Initialize event.

        Args:
          conference_id: Conference ID
          participant: Participant
          tenant_uuid: tenant UUID
          user_uuids: List of User UUID

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuids)


class ConferenceUserParticipantJoinedEvent(_ConferenceMixin, UserEvent):
    """Event for when a participant joins a user conference."""

    service = "calld"
    name = "conference_user_participant_joined"
    routing_key_fmt = "conferences.users.{user_uuid}.participants.joined"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          conference_id: Conference ID
          participant: Participant
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuid)


class ConferenceUserParticipantLeftEvent(_ConferenceMixin, UserEvent):
    """Event for when a participant leaves a user conference."""

    service = "calld"
    name = "conference_user_participant_left"
    routing_key_fmt = "conferences.users.{user_uuid}.participants.left"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            conference_id (int): conference ID.
            participant (ParticipantDict): participant.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuid)


class ConferenceUserParticipantTalkStartedEvent(_ConferenceMixin, UserEvent):
    """Event for when a participant starts talking in a user conference."""

    service = "calld"
    name = "conference_user_participant_talk_started"
    routing_key_fmt = "conferences.users.{user_uuid}.participants.talk"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           conference_id: Conference ID
           participant: Participant
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuid)


class ConferenceUserParticipantTalkStoppedEvent(_ConferenceMixin, UserEvent):
    """Event for when a participant stops talking in a user conference."""

    service = "calld"
    name = "conference_user_participant_talk_stopped"
    routing_key_fmt = "conferences.users.{user_uuid}.participants.talk"

    def __init__(
        self,
        conference_id: int,
        participant: ParticipantDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            conference_id (int): conference ID.
            participant (ParticipantDict): participant details.
            tenant_uuid (UUIDStr): tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = dict(participant, conference_id=conference_id)
        super().__init__(content, conference_id, tenant_uuid, user_uuid)
