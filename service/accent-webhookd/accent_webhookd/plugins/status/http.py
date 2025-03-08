# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict, cast

from accent.auth_verifier import required_acl

from accent_webhookd import auth
from accent_webhookd.rest_api import AuthResource

if TYPE_CHECKING:
    from ...bus import BusConsumer
    from ...types import WebhookdConfigDict


class StatusDict(TypedDict):
    status: Literal['ok', 'fail']


class StatusResponse(TypedDict):
    bus_consumer: StatusDict
    master_tenant: StatusDict


class StatusResource(AuthResource):
    def __init__(self, bus_consumer: BusConsumer, config: WebhookdConfigDict) -> None:
        self._bus_consumer = bus_consumer
        self._config = config

    @required_acl('webhookd.status.read')
    def get(self) -> tuple[StatusResponse, int]:
        try:
            auth.get_master_tenant_uuid()
        except auth.MasterTenantNotInitializedException:
            master_tenant_status = 'fail'
        else:
            master_tenant_status = 'ok'

        result = {
            'bus_consumer': {
                'status': 'ok' if self._bus_consumer.consumer_connected() else 'fail'
            },
            'master_tenant': {'status': master_tenant_status},
        }
        return cast(StatusResponse, result), 200
