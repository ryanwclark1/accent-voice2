# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class PagingCallerUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_caller_users_associated'
    routing_key_fmt = 'config.pagings.callers.users.updated'

    def __init__(
        self,
        paging_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'paging_id': paging_id,
            'user_uuids': users,
        }
        super().__init__(content, tenant_uuid)


class PagingMemberUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_member_users_associated'
    routing_key_fmt = 'config.pagings.members.users.updated'

    def __init__(
        self,
        paging_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'paging_id': paging_id,
            'user_uuids': users,
        }
        super().__init__(content, tenant_uuid)
