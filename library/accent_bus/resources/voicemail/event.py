# Copyright 2023 Accent Communications

from ..common.event import TenantEvent, UserEvent
from ..common.types import UUIDStr
from .types import VoicemailMessageDict


class VoicemailCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'voicemail_created'
    routing_key_fmt = 'config.voicemail.created'

    def __init__(self, voicemail_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(voicemail_id)}
        super().__init__(content, tenant_uuid)


class VoicemailDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'voicemail_deleted'
    routing_key_fmt = 'config.voicemail.deleted'

    def __init__(self, voicemail_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(voicemail_id)}
        super().__init__(content, tenant_uuid)


class VoicemailEditedEvent(TenantEvent):
    service = 'confd'
    name = 'voicemail_edited'
    routing_key_fmt = 'config.voicemail.edited'

    def __init__(self, voicemail_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(voicemail_id)}
        super().__init__(content, tenant_uuid)


class UserVoicemailEditedEvent(UserEvent):
    service = 'confd'
    name = 'user_voicemail_edited'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.edited'

    def __init__(
        self,
        voicemail_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailMessageCreatedEvent(UserEvent):
    service = 'calld'
    name = 'user_voicemail_message_created'
    routing_key_fmt = 'voicemails.messages.created'
    required_acl_fmt = 'events.users.{user_uuid}.voicemails'

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
            'message_id': message_id,
            'message': message,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailMessageUpdatedEvent(UserEvent):
    service = 'calld'
    name = 'user_voicemail_message_updated'
    routing_key_fmt = 'voicemails.messages.updated'
    required_acl_fmt = 'events.users.{user_uuid}.voicemails'

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
            'message_id': message_id,
            'message': message,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailMessageDeletedEvent(UserEvent):
    service = 'calld'
    name = 'user_voicemail_message_deleted'
    routing_key_fmt = 'voicemails.messages.deleted'
    required_acl_fmt = 'events.users.{user_uuid}.voicemails'

    def __init__(
        self,
        message_id: str,
        voicemail_id: int,
        message: VoicemailMessageDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
            'message_id': message_id,
            'message': message,
        }
        super().__init__(content, tenant_uuid, user_uuid)
