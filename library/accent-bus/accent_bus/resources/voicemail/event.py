# resources/voicemail/event.py
from typing import ClassVar

from pydantic import BaseModel, UUID4, Field

from resources.common.event import TenantEvent, UserEvent
from .types import VoicemailMessageDict


class VoicemailEvent(TenantEvent):
    """Base class for Voicemail events."""

    service: ClassVar[str] = "confd"
    content: dict


class VoicemailCreatedEvent(VoicemailEvent):
    """Event for when a voicemail is created."""

    name: ClassVar[str] = "voicemail_created"
    routing_key_fmt: ClassVar[str] = "config.voicemail.created"

    def __init__(self, voicemail_id: int, **data):
        content = {"id": int(voicemail_id)}
        super().__init__(content=content, **data)


class VoicemailDeletedEvent(VoicemailEvent):
    """Event for when a voicemail is deleted."""

    name: ClassVar[str] = "voicemail_deleted"
    routing_key_fmt: ClassVar[str] = "config.voicemail.deleted"

    def __init__(self, voicemail_id: int, **data):
        content = {"id": int(voicemail_id)}
        super().__init__(content=content, **data)


class VoicemailEditedEvent(VoicemailEvent):
    """Event for when a voicemail is edited."""

    name: ClassVar[str] = "voicemail_edited"
    routing_key_fmt: ClassVar[str] = "config.voicemail.edited"

    def __init__(self, voicemail_id: int, **data):
        content = {"id": int(voicemail_id)}
        super().__init__(content=content, **data)


class UserVoicemailEvent(UserEvent):
    """Base class for user-specific Voicemail events."""

    service: ClassVar[str] = "confd"  # Or calld, depending on context
    content: dict


class UserVoicemailEditedEvent(UserVoicemailEvent):
    """Event for when a user's voicemail settings are edited."""

    name: ClassVar[str] = "user_voicemail_edited"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.voicemails.edited"

    def __init__(
        self,
        voicemail_id: int,
        **data,
    ):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "voicemail_id": voicemail_id,
        }
        super().__init__(content=content, **data)


class UserVoicemailMessageEvent(UserEvent):
    """Base class for user voicemail message events."""

    service: ClassVar[str] = "calld"
    required_acl_fmt: ClassVar[str] = "events.users.{user_uuid}.voicemails"
    content: dict


class UserVoicemailMessageCreatedEvent(UserVoicemailMessageEvent):
    """Event for when a new voicemail message is created for a user."""

    name: ClassVar[str] = "user_voicemail_message_created"
    routing_key_fmt: ClassVar[str] = "voicemails.messages.created"

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        **data,
    ):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "voicemail_id": voicemail_id,
            "message_id": message_id,
            "message": message,
        }

        super().__init__(content=content, **data)


class UserVoicemailMessageUpdatedEvent(UserVoicemailMessageEvent):
    """Event for when a voicemail message is updated for a user."""

    name: ClassVar[str] = "user_voicemail_message_updated"
    routing_key_fmt: ClassVar[str] = "voicemails.messages.updated"

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        **data,
    ):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "voicemail_id": voicemail_id,
            "message_id": message_id,
            "message": message,
        }

        super().__init__(content=content, **data)


class UserVoicemailMessageDeletedEvent(UserVoicemailMessageEvent):
    """Event for when a voicemail message is deleted for a user."""

    name: ClassVar[str] = "user_voicemail_message_deleted"
    routing_key_fmt: ClassVar[str] = "voicemails.messages.deleted"

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        **data,
    ):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "voicemail_id": voicemail_id,
            "message_id": message_id,
            "message": message,
        }

        super().__init__(content=content, **data)
