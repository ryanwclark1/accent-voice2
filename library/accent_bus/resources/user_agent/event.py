# Copyright 2023 Accent Communications

from ..common.event import UserEvent
from ..common.types import UUIDStr


class UserAgentAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_agent_associated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.updated'

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserAgentDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_agent_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.deleted'

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
