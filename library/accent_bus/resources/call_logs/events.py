# Copyright 2023 Accent Communications

from ..common.event import TenantEvent, UserEvent
from ..common.types import UUIDStr
from .types import CDRDataDict


class CallLogCreatedEvent(TenantEvent):
    service = 'call_logd'
    name = 'call_log_created'
    routing_key_fmt = 'call_log.created'

    def __init__(self, cdr_data: CDRDataDict, tenant_uuid: UUIDStr):
        super().__init__(cdr_data, tenant_uuid)


class CallLogUserCreatedEvent(UserEvent):
    service = 'call_logd'
    name = 'call_log_user_created'
    routing_key_fmt = 'call_log.user.{user_uuid}.created'

    def __init__(
        self,
        cdr_data: CDRDataDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(cdr_data, tenant_uuid, user_uuid)
