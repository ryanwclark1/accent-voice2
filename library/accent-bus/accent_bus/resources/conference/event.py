# resources/conference/event.py
from typing import ClassVar

from accent_bus.resources.common.event import (
    MultiUserEvent,
    TenantEvent,
    UserEvent,
)  # Import base classes

from .types import ParticipantDict


class ConferenceEvent(TenantEvent):
    """Base class for conference events.

    Args:
        content (dict): Event content.
        conference_id (int): Conference ID.

    """

    service: ClassVar[str] = "confd"
    content: dict
    conference_id: int  # All conference events have a conference id

    def __init__(self, content: dict, conference_id: int, *args, **kwargs):
        super().__init__(content, *args, **kwargs)
        if not conference_id:
            raise ValueError("conference_id must have a value")
        self.conference_id = conference_id


class ConferenceCreatedEvent(ConferenceEvent):
    """Event for when a conference is created."""

    name: ClassVar[str] = "conference_created"
    routing_key_fmt: ClassVar[str] = "config.conferences.created"

    def __init__(self, conference_id: int, **data):
        content = {"id": conference_id}
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceDeletedEvent(ConferenceEvent):
    """Event for when a conference is deleted."""

    name: ClassVar[str] = "conference_deleted"
    routing_key_fmt: ClassVar[str] = "config.conferences.deleted"

    def __init__(self, conference_id: int, **data):
        content = {"id": conference_id}
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceEditedEvent(ConferenceEvent):
    """Event for when a conference is edited."""

    name: ClassVar[str] = "conference_edited"
    routing_key_fmt: ClassVar[str] = "config.conferences.edited"

    def __init__(self, conference_id: int, **data):
        content = {"id": conference_id}
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceRecordEvent(ConferenceEvent):
    """Base class for recording events"""

    service: ClassVar[str] = "calld"

    def __init__(self, conference_id: int, **data):
        content = {"id": conference_id}
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceRecordStartedEvent(ConferenceRecordEvent):
    """Event for when conference recording starts."""

    name: ClassVar[str] = "conference_record_started"
    routing_key_fmt: ClassVar[str] = "conferences.{id}.record"


class ConferenceRecordStoppedEvent(ConferenceRecordEvent):
    """Event for when conference recording stops."""

    name: ClassVar[str] = "conference_record_stopped"
    routing_key_fmt: ClassVar[str] = "conferences.{id}.record"


class ConferenceParticipantEvent(MultiUserEvent):
    """Base class for conference participant events.

    Args:
        conference_id (int): The ID of the conference.
        participant (ParticipantDict): Information about participant.
        user_uuids (list[str]): List of users UUID.

    """

    service: ClassVar[str] = "calld"
    conference_id: int

    def __init__(self, content: dict, conference_id: int, *args, **kwargs):
        super().__init__(content, *args, **kwargs)
        if not conference_id:
            raise ValueError("conference_id must have a value")
        self.conference_id = conference_id


class ConferenceParticipantJoinedEvent(ConferenceParticipantEvent):
    """Event for when a participant joins a conference."""

    name: ClassVar[str] = "conference_participant_joined"
    routing_key_fmt: ClassVar[str] = "conferences.{conference_id}.participants.joined"

    def __init__(self, participant: ParticipantDict, conference_id: int, *args, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceParticipantLeftEvent(ConferenceParticipantEvent):
    """Event for when a participant leaves a conference."""

    name: ClassVar[str] = "conference_participant_left"
    routing_key_fmt: ClassVar[str] = "conferences.{conference_id}.participants.left"

    def __init__(self, participant: ParticipantDict, conference_id: int, *args, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceParticipantMutedEvent(ConferenceEvent):
    """Event for when a participant is muted in a conference."""

    service: ClassVar[str] = "calld"  # Overrides the base class
    name: ClassVar[str] = "conference_participant_muted"
    routing_key_fmt: ClassVar[str] = "conferences.{conference_id}.participants.mute"

    def __init__(self, participant: ParticipantDict, conference_id: int, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceParticipantUnmutedEvent(ConferenceEvent):
    """Event for when a participant is unmuted in a conference."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "conference_participant_unmuted"
    routing_key_fmt: ClassVar[str] = "conferences.{conference_id}.particpants.mute"

    def __init__(self, participant: ParticipantDict, conference_id: int, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceParticipantTalkEvent(ConferenceParticipantEvent):
    """Base class for talk events"""

    def __init__(self, participant: ParticipantDict, conference_id: int, *args, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceParticipantTalkStartedEvent(ConferenceParticipantTalkEvent):
    """Event for when a participant starts talking in a conference."""

    name: ClassVar[str] = "conference_participant_talk_started"
    routing_key_fmt: ClassVar[str] = "conferences.{conference_id}.participants.talk"


class ConferenceParticipantTalkStoppedEvent(ConferenceParticipantTalkEvent):
    """Event for when a participant stops talking in a conference."""

    name: ClassVar[str] = "conference_participant_talk_stopped"
    routing_key_fmt: ClassVar[str] = "conferences.{conference_id}.participants.talk"


class ConferenceUserParticipantEvent(UserEvent):
    """Base class for user-specific, conference related events"""

    service: ClassVar[str] = "calld"
    conference_id: int

    def __init__(self, content: dict, conference_id: int, *args, **data):
        super().__init__(content, *args, **data)
        if not conference_id:
            raise ValueError("conference_id must have a value")
        self.conference_id = conference_id


class ConferenceUserParticipantJoinedEvent(ConferenceUserParticipantEvent):
    """Event for user participant joins."""

    name: ClassVar[str] = "conference_user_participant_joined"
    routing_key_fmt: ClassVar[str] = "conferences.users.{user_uuid}.participants.joined"

    def __init__(self, participant: ParticipantDict, conference_id: int, *args, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceUserParticipantLeftEvent(ConferenceUserParticipantEvent):
    """Event for user participant leaves."""

    name: ClassVar[str] = "conference_user_participant_left"
    routing_key_fmt: ClassVar[str] = "conferences.users.{user_uuid}.participants.left"

    def __init__(self, participant: ParticipantDict, conference_id: int, *args, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceUserParticipantTalkEvent(ConferenceUserParticipantEvent):
    """Base class for user talk events."""

    def __init__(self, participant: ParticipantDict, conference_id: int, *args, **data):
        content = dict(participant, conference_id=conference_id)
        super().__init__(content=content, conference_id=conference_id, **data)


class ConferenceUserParticipantTalkStartedEvent(ConferenceUserParticipantTalkEvent):
    """Event for when a user starts talking in a conference."""

    name: ClassVar[str] = "conference_user_participant_talk_started"
    routing_key_fmt: ClassVar[str] = "conferences.users.{user_uuid}.participants.talk"


class ConferenceUserParticipantTalkStoppedEvent(ConferenceUserParticipantTalkEvent):
    """Event for when a user stops talking in a conference."""

    name: ClassVar[str] = "conference_user_participant_talk_stopped"
    routing_key_fmt: ClassVar[str] = "conferences.users.{user_uuid}.participants.talk"
