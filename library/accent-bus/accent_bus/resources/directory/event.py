# Copyright 2023 Accent Communications

from ..common.event import UserEvent
from ..common.types import UUIDStr


class FavoriteAddedEvent(UserEvent):
    service = 'dird'
    name = 'favorite_added'
    routing_key_fmt = 'directory.{user_uuid}.favorite.created'

    def __init__(
        self,
        source_name: str,
        entry_id: str,
        accent_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'accent_uuid': str(accent_uuid),
            'user_uuid': str(user_uuid),
            'source': source_name,
            'source_entry_id': entry_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class FavoriteDeletedEvent(UserEvent):
    service = 'dird'
    name = 'favorite_deleted'
    routing_key_fmt = 'directory.{user_uuid}.favorite.deleted'

    def __init__(
        self,
        source_name: str,
        entry_id: str,
        accent_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'accent_uuid': str(accent_uuid),
            'user_uuid': str(user_uuid),
            'source': source_name,
            'source_entry_id': entry_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
