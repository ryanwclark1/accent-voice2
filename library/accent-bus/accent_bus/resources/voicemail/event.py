# accent_bus/resources/voicemail/event.py
# Copyright 2025 Accent Communications

"""Voicemail events."""

from accent_bus.resources.common.event import TenantEvent, UserEvent
from accent_bus.resources.common.types import UUIDStr

from .types import VoicemailMessageDict


class VoicemailCreatedEvent(TenantEvent):
    """Event for when a voicemail is created."""

    service = "confd"
    name = "voicemail_created"
    routing_key_fmt = "config.voicemail.created"

    def __init__(self, voicemail_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            voicemail_id (int): The ID of the voicemail.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": int(voicemail_id)}
        super().__init__(content, tenant_uuid)


class VoicemailDeletedEvent(TenantEvent):
    """Event for when a voicemail is deleted."""

    service = "confd"
    name = "voicemail_deleted"
    routing_key_fmt = "config.voicemail.deleted"

    def __init__(self, voicemail_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           voicemail_id: Voicemail ID
           tenant_uuid: tenant UUID

        """
        content = {"id": int(voicemail_id)}
        super().__init__(content, tenant_uuid)


class VoicemailEditedEvent(TenantEvent):
    """Event for when a voicemail is edited."""

    service = "confd"
    name = "voicemail_edited"
    routing_key_fmt = "config.voicemail.edited"

    def __init__(self, voicemail_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            voicemail_id (int):  voicemail ID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"id": int(voicemail_id)}
        super().__init__(content, tenant_uuid)


class UserVoicemailEditedEvent(UserEvent):
    """Event for when a user voicemail is edited."""

    service = "confd"
    name = "user_voicemail_edited"
    routing_key_fmt = "config.users.{user_uuid}.voicemails.edited"

    def __init__(
        self,
        voicemail_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            voicemail_id (int):  voicemail ID.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = {
            "user_uuid": str(user_uuid),
            "voicemail_id": voicemail_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailMessageCreatedEvent(UserEvent):
    """Event for when a user voicemail message is created."""

    service = "calld"
    name = "user_voicemail_message_created"
    routing_key_fmt = "voicemails.messages.created"
    required_acl_fmt = "events.users.{user_uuid}.voicemails"

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            message_id (str): The ID of the message.
            voicemail_id (int):  voicemail ID.
            message (VoicemailMessageDict): message.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        content = {
            "user_uuid": str(user_uuid),
            "voicemail_id": voicemail_id,
            "message_id": message_id,
            "message": message,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailMessageUpdatedEvent(UserEvent):
    """Event for when a user voicemail message is updated."""

    service = "calld"
    name = "user_voicemail_message_updated"
    routing_key_fmt = "voicemails.messages.updated"
    required_acl_fmt = "events.users.{user_uuid}.voicemails"

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            message_id (str):  message ID.
            voicemail_id (int):  voicemail ID.
            message (VoicemailMessageDict): message.
            tenant_uuid (UUIDStr): tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        content = {
            "user_uuid": str(user_uuid),
            "voicemail_id": voicemail_id,
            "message_id": message_id,
            "message": message,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailMessageDeletedEvent(UserEvent):
    """Event for when a user voicemail message is deleted."""

    service = "calld"
    name = "user_voicemail_message_deleted"
    routing_key_fmt = "voicemails.messages.deleted"
    required_acl_fmt = "events.users.{user_uuid}.voicemails"

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           message_id: Message ID
           voicemail_id: Voicemail ID
           message: Message
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {
            "user_uuid": str(user_uuid),
            "voicemail_id": voicemail_id,
            "message_id": message_id,
            "message": message,
        }
        super().__init__(content, tenant_uuid, user_uuid)
