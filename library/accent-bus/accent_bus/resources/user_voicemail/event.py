# accent_bus/resources/user_voicemail/event.py
# Copyright 2025 Accent Communications

"""User voicemail events."""

from accent_bus.resources.common.event import UserEvent
from accent_bus.resources.common.types import UUIDStr


class UserVoicemailAssociatedEvent(UserEvent):
    """Event for when a user voicemail is associated."""

    service = "confd"
    name = "user_voicemail_associated"
    routing_key_fmt = "config.users.{user_uuid}.voicemails.updated"

    def __init__(
        self,
        voicemail_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            voicemail_id (int):  voicemail ID.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        content = {
            "user_uuid": str(user_uuid),
            "voicemail_id": int(voicemail_id),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailDissociatedEvent(UserEvent):
    """Event for when a user voicemail is dissociated."""

    service = "confd"
    name = "user_voicemail_dissociated"
    routing_key_fmt = "config.users.{user_uuid}.voicemails.deleted"

    def __init__(
        self,
        voicemail_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           voicemail_id: Voicemail ID
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "user_uuid": user_uuid,
            "voicemail_id": int(voicemail_id),
        }
        super().__init__(content, tenant_uuid, user_uuid)
