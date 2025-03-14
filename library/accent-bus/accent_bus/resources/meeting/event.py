# resources/meeting/event.py
from typing import ClassVar

from pydantic import UUID4

from accent_bus.resources.common.event import (  # Import base classes
    TenantEvent,
    UserEvent,
)

from .types import MeetingAuthorizationDict, MeetingDict, MeetingParticipantDict


class MeetingEvent(TenantEvent):
    """Base class for meeting events
    Args:
        meeting_uuid (UUID4): The UUID of the meeting.
    """

    service: ClassVar[str] = "confd"
    content: dict
    meeting_uuid: str

    def __init__(
        self,
        content: dict,
        meeting_uuid: UUID4,
        *args,
        **kwargs,
    ):
        super().__init__(content, *args, **kwargs)
        if meeting_uuid is None:
            raise ValueError("meeting_uuid must have a value")
        self.meeting_uuid = str(meeting_uuid)


class MeetingCreatedEvent(MeetingEvent):
    """Event for when a meeting is created."""

    name: ClassVar[str] = "meeting_created"
    routing_key_fmt: ClassVar[str] = "config.meetings.created"

    def __init__(self, meeting: MeetingDict, **data):
        super().__init__(content=meeting, meeting_uuid=meeting["uuid"], **data)


class MeetingDeletedEvent(MeetingEvent):
    """Event for when a meeting is deleted."""

    name: ClassVar[str] = "meeting_deleted"
    routing_key_fmt: ClassVar[str] = "config.meetings.deleted"

    def __init__(self, meeting: MeetingDict, **data):
        super().__init__(content=meeting, meeting_uuid=meeting["uuid"], **data)


class MeetingEditedEvent(MeetingEvent):
    """Event for when a meeting is updated."""

    name: ClassVar[str] = "meeting_updated"
    routing_key_fmt: ClassVar[str] = "config.meetings.updated"

    def __init__(self, meeting: MeetingDict, **data):
        super().__init__(content=meeting, meeting_uuid=meeting["uuid"], **data)


class MeetingProgressEvent(MeetingEvent):
    """Event for when a meeting changes status."""

    name: ClassVar[str] = "meeting_progress"
    routing_key_fmt: ClassVar[str] = "config.meetings.progress"

    def __init__(
        self,
        meeting: MeetingDict,
        status: str,
        **data,
    ):
        content = dict(meeting)
        content["status"] = status
        super().__init__(content=content, meeting_uuid=meeting["uuid"], **data)


class MeetingUserProgressEvent(MeetingEvent, UserEvent):
    """Event for user meeting progress."""

    name: ClassVar[str] = "meeting_user_progress"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.meetings.progress"

    def __init__(
        self,
        meeting: MeetingDict,
        status: str,
        **data,
    ):
        content = dict(meeting)
        content["status"] = status
        content["user_uuid"] = str(data["user_uuid"])
        super().__init__(content=content, meeting_uuid=meeting["uuid"], **data)


class MeetingParticipantEvent(MeetingEvent):
    """Base class for participant events."""

    service: ClassVar[str] = "calld"


class MeetingParticipantJoinedEvent(MeetingParticipantEvent):
    """Event for when a participant joins a meeting."""

    name: ClassVar[str] = "meeting_participant_joined"
    routing_key_fmt: ClassVar[str] = "meetings.{meeting_uuid}.participants.joined"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUID4,
        **data,
    ):
        content = dict(participant, meeting_uuid=str(meeting_uuid))
        super().__init__(content=content, meeting_uuid=meeting_uuid, **data)


class MeetingParticipantLeftEvent(MeetingParticipantEvent):
    """Event for when a participant leaves a meeting."""

    name: ClassVar[str] = "meeting_participant_left"
    routing_key_fmt: ClassVar[str] = "meetings.{meeting_uuid}.participants.left"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUID4,
        **data,
    ):
        content = dict(participant, meeting_uuid=str(meeting_uuid))
        super().__init__(content=content, meeting_uuid=meeting_uuid, **data)


class MeetingUserParticipantEvent(MeetingEvent, UserEvent):
    service: ClassVar[str] = "calld"
    required_acl_fmt: ClassVar[str] = (
        "events.users.{user_uuid}.meetings.participants.{verb}"
    )
    # user_uuid is in base class


class MeetingUserParticipantJoinedEvent(MeetingUserParticipantEvent):
    """Event for when a user's participant joins a meeting."""

    name: ClassVar[str] = "meeting_user_participant_joined"
    routing_key_fmt: ClassVar[str] = "meetings.users.{user_uuid}.participants.joined"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUID4,
        **data,
    ):
        content = dict(participant, meeting_uuid=str(meeting_uuid))
        super().__init__(content=content, meeting_uuid=meeting_uuid, **data)


class MeetingUserParticipantLeftEvent(MeetingUserParticipantEvent):
    """Event for when a user's participant leaves a meeting."""

    name: ClassVar[str] = "meeting_user_participant_left"
    routing_key_fmt: ClassVar[str] = "meetings.users.{user_uuid}.participants.left"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUID4,
        **data,
    ):
        content = dict(participant, meeting_uuid=str(meeting_uuid))
        super().__init__(content=content, meeting_uuid=meeting_uuid, **data)


class MeetingAuthorizationEvent(MeetingEvent):
    """Base class for meeting authorization events."""

    service: ClassVar[str] = "confd"


class MeetingAuthorizationCreatedEvent(MeetingAuthorizationEvent):
    """Event for when a meeting guest authorization is created."""

    name: ClassVar[str] = "meeting_guest_authorization_created"
    routing_key_fmt: ClassVar[str] = "config.meeting_guest_authorizations.created"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUID4,
        **data,
    ):
        super().__init__(
            content=meeting_authorization, meeting_uuid=meeting_uuid, **data
        )


class MeetingAuthorizationDeletedEvent(MeetingAuthorizationEvent):
    """Event for when a meeting guest authorization is deleted."""

    name: ClassVar[str] = "meeting_guest_authorization_deleted"
    routing_key_fmt: ClassVar[str] = "config.meeting_guest_authorizations.deleted"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUID4,
        **data,
    ):
        super().__init__(
            content=meeting_authorization, meeting_uuid=meeting_uuid, **data
        )


class MeetingAuthorizationEditedEvent(MeetingAuthorizationEvent):
    """Event for when a meeting guest authorization is updated."""

    name: ClassVar[str] = "meeting_guest_authorization_updated"
    routing_key_fmt: ClassVar[str] = "config.meeting_guest_authorizations.updated"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUID4,
        **data,
    ):
        super().__init__(
            content=meeting_authorization, meeting_uuid=meeting_uuid, **data
        )


class MeetingUserAuthorizationEvent(MeetingEvent, UserEvent):
    """Base class for user meeting authorization events."""

    service: ClassVar[str] = "confd"
    required_acl_fmt: ClassVar[str] = (
        "events.users.{user_uuid}.meeting_guest_authorizations.{verb}"
    )


class MeetingUserAuthorizationCreatedEvent(MeetingUserAuthorizationEvent):
    """Event for user meeting authorization creation."""

    name: ClassVar[str] = "meeting_user_guest_authorization_created"
    routing_key_fmt: ClassVar[str] = (
        "config.users.{user_uuid}.meeting_guest_authorizations.created"
    )

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUID4,
        **data,
    ):
        content = dict(meeting_authorization, user_uuid=str(data["user_uuid"]))
        super().__init__(content=content, meeting_uuid=meeting_uuid, **data)


class MeetingUserAuthorizationDeletedEvent(MeetingUserAuthorizationEvent):
    """Event for user meeting authorization deletion."""

    name: ClassVar[str] = "meeting_user_guest_authorization_deleted"
    routing_key_fmt: ClassVar[str] = (
        "config.users.{user_uuid}.meeting_guest_authorizations.deleted"
    )

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUID4,
        **data,
    ):
        content = dict(meeting_authorization, user_uuid=str(data["user_uuid"]))
        super().__init__(content=content, meeting_uuid=meeting_uuid, **data)


class MeetingUserAuthorizationEditedEvent(MeetingUserAuthorizationEvent):
    """Event for user meeting authorization update."""

    name: ClassVar[str] = "meeting_user_guest_authorization_updated"
    routing_key_fmt: ClassVar[str] = (
        "config.users.{user_uuid}.meeting_guest_authorizations.updated"
    )

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUID4,
        **data,
    ):
        content = dict(meeting_authorization, user_uuid=str(data["user_uuid"]))
        super().__init__(content=content, meeting_uuid=meeting_uuid, **data)
