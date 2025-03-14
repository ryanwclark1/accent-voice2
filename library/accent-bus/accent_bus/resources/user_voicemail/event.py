# resources/user_voicemail/event.py
from typing import ClassVar

from accent_bus.resources.common.event import UserEvent  # Correct import


class UserVoicemailEvent(UserEvent):
    """Base class for User Voicemail events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserVoicemailAssociatedEvent(UserVoicemailEvent):
    """Event for when a voicemail is associated with a user."""

    name: ClassVar[str] = "user_voicemail_associated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.voicemails.updated"

    def __init__(self, voicemail_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "voicemail_id": int(voicemail_id),
        }
        super().__init__(content=content, **data)


class UserVoicemailDissociatedEvent(UserVoicemailEvent):
    """Event for when a voicemail is dissociated from a user."""

    name: ClassVar[str] = "user_voicemail_dissociated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.voicemails.deleted"

    def __init__(self, voicemail_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "voicemail_id": int(voicemail_id),
        }
        super().__init__(content=content, **data)
