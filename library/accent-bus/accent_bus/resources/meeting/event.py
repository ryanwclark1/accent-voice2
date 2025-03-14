# accent_bus/resources/meeting/event.py
# Copyright 2025 Accent Communications

"""Meeting events."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from accent_bus.resources.common.event import TenantEvent, UserEvent

if TYPE_CHECKING:
    from collections.abc import Mapping

    from accent_bus.resources.common.types import UUIDStr

    from .types import MeetingAuthorizationDict, MeetingDict, MeetingParticipantDict


class _MeetingMixin:
    """Mixin for meeting-related events."""

    def __init__(
        self,
        content: Mapping,
        meeting_uuid: UUIDStr,
        *args: Any,
    ) -> None:
        super().__init__(content, *args)  # type: ignore[call-arg]
        if meeting_uuid is None:
            msg = "meeting_uuid must have a value"
            raise ValueError(msg)
        self.meeting_uuid = str(meeting_uuid)


class MeetingCreatedEvent(_MeetingMixin, TenantEvent):
    """Event for when a meeting is created."""

    service = "confd"
    name = "meeting_created"
    routing_key_fmt = "config.meetings.created"

    def __init__(self, meeting: MeetingDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          meeting: Meeting
          tenant_uuid: tenant UUID

        """
        super().__init__(meeting, meeting["uuid"], tenant_uuid)


class MeetingDeletedEvent(_MeetingMixin, TenantEvent):
    """Event for when a meeting is deleted."""

    service = "confd"
    name = "meeting_deleted"
    routing_key_fmt = "config.meetings.deleted"

    def __init__(self, meeting: MeetingDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            meeting (MeetingDict): meeting.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(meeting, meeting["uuid"], tenant_uuid)


class MeetingEditedEvent(_MeetingMixin, TenantEvent):
    """Event for when a meeting is edited."""

    service = "confd"
    name = "meeting_updated"
    routing_key_fmt = "config.meetings.updated"

    def __init__(self, meeting: MeetingDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          meeting: Meeting
          tenant_uuid: tenant UUID

        """
        super().__init__(meeting, meeting["uuid"], tenant_uuid)


class MeetingProgressEvent(_MeetingMixin, TenantEvent):
    """Event for meeting progress."""

    service = "confd"
    name = "meeting_progress"
    routing_key_fmt = "config.meetings.progress"

    def __init__(
        self,
        meeting: MeetingDict,
        status: str,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           meeting: Meeting
           status: Status
           tenant_uuid: tenant UUID

        """
        content = dict(meeting)
        content["status"] = status
        super().__init__(content, meeting["uuid"], tenant_uuid)


class MeetingUserProgressEvent(_MeetingMixin, UserEvent):
    """Event for user meeting progress."""

    service = "confd"
    name = "meeting_user_progress"
    routing_key_fmt = "config.users.{user_uuid}.meetings.progress"

    def __init__(
        self,
        meeting: MeetingDict,
        status: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          meeting: Meeting
          status: Status
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = dict(meeting)
        content["status"] = status
        content["user_uuid"] = user_uuid
        super().__init__(content, meeting["uuid"], tenant_uuid, user_uuid)


class MeetingParticipantJoinedEvent(_MeetingMixin, TenantEvent):
    """Event for when a participant joins a meeting."""

    service = "calld"
    name = "meeting_participant_joined"
    routing_key_fmt = "meetings.{meeting_uuid}.participants.joined"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            participant (MeetingParticipantDict):  participant.
            meeting_uuid (UUIDStr):  meeting UUID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid)


class MeetingParticipantLeftEvent(_MeetingMixin, TenantEvent):
    """Event for when a participant leaves a meeting."""

    service = "calld"
    name = "meeting_participant_left"
    routing_key_fmt = "meetings.{meeting_uuid}.participants.left"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           participant: Participant
           meeting_uuid: Meeting UUID
           tenant_uuid: tenant UUID

        """
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid)


class MeetingUserParticipantJoinedEvent(_MeetingMixin, UserEvent):
    """Event for when a participant joins a user meeting."""

    service = "calld"
    name = "meeting_user_participant_joined"
    routing_key_fmt = "meetings.users.{user_uuid}.participants.joined"
    required_acl_fmt = "events.users.{user_uuid}.meetings.participants.joined"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            participant (MeetingParticipantDict): The participant details.
            meeting_uuid (UUIDStr): The meeting UUID.
            tenant_uuid (UUIDStr): The tenant UUID.
            user_uuid (UUIDStr): The user UUID.

        """
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingUserParticipantLeftEvent(_MeetingMixin, UserEvent):
    """Event for when a participant leaves a user meeting."""

    service = "calld"
    name = "meeting_user_participant_left"
    routing_key_fmt = "meetings.users.{user_uuid}.participants.left"
    required_acl_fmt = "events.users.{user_uuid}.meetings.participants.left"

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            participant (MeetingParticipantDict): The participant details.
            meeting_uuid (UUIDStr): meeting UUID.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingAuthorizationCreatedEvent(_MeetingMixin, TenantEvent):
    """Event for when a meeting authorization is created."""

    service = "confd"
    name = "meeting_guest_authorization_created"
    routing_key_fmt = "config.meeting_guest_authorizations.created"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           meeting_authorization: Meeting Authorization
           meeting_uuid: Meeting UUID
           tenant_uuid: tenant UUID

        """
        super().__init__(meeting_authorization, meeting_uuid, tenant_uuid)


class MeetingAuthorizationDeletedEvent(_MeetingMixin, TenantEvent):
    """Event for when a meeting authorization is deleted."""

    service = "confd"
    name = "meeting_guest_authorization_deleted"
    routing_key_fmt = "config.meeting_guest_authorizations.deleted"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            meeting_authorization (MeetingAuthorizationDict): The meeting authorization details.
            meeting_uuid (UUIDStr):  meeting UUID.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(meeting_authorization, meeting_uuid, tenant_uuid)


class MeetingAuthorizationEditedEvent(_MeetingMixin, TenantEvent):
    """Event for when a meeting authorization is edited."""

    service = "confd"
    name = "meeting_guest_authorization_updated"
    routing_key_fmt = "config.meeting_guest_authorizations.updated"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          meeting_authorization: Meeting Authorization
          meeting_uuid: Meeting UUID
          tenant_uuid: tenant UUID

        """
        super().__init__(meeting_authorization, meeting_uuid, tenant_uuid)


class MeetingUserAuthorizationCreatedEvent(_MeetingMixin, UserEvent):
    """Event for when a user meeting authorization is created."""

    service = "confd"
    name = "meeting_user_guest_authorization_created"
    routing_key_fmt = "config.users.{user_uuid}.meeting_guest_authorizations.created"
    required_acl_fmt = "events.users.{user_uuid}.meeting_guest_authorizations.created"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          meeting_authorization: Meeting Authorization
          meeting_uuid: Meeting UUID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingUserAuthorizationDeletedEvent(_MeetingMixin, UserEvent):
    """Event for when a user meeting authorization is deleted."""

    service = "confd"
    name = "meeting_user_guest_authorization_deleted"
    routing_key_fmt = "config.users.{user_uuid}.meeting_guest_authorizations.deleted"
    required_acl_fmt = "events.users.{user_uuid}.meeting_guest_authorizations.deleted"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           meeting_authorization: Meeting Authorization
           meeting_uuid: Meeting UUID
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingUserAuthorizationEditedEvent(_MeetingMixin, UserEvent):
    """Event for when a user meeting authorization is edited."""

    service = "confd"
    name = "meeting_user_guest_authorization_updated"
    routing_key_fmt = "config.users.{user_uuid}.meeting_guest_authorizations.updated"
    required_acl_fmt = "events.users.{user_uuid}.meeting_guest_authorizations.updated"

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            meeting_authorization (MeetingAuthorizationDict): meeting authorization details.
            meeting_uuid (UUIDStr): The meeting UUID.
            tenant_uuid (UUIDStr): tenant UUID.
            user_uuid (UUIDStr): The user UUID.

        """
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)
