# Copyright 2023 Accent Communications

import logging
from dataclasses import dataclass

from accent_call_logd.database.queries.tenant import TenantDAO

from ...sync_db import remove_tenant

logger = logging.getLogger(__name__)


@dataclass
class TenantEventHandler:
    tenant_dao: TenantDAO

    def subscribe(self, bus_consumer):
        bus_consumer.subscribe('auth_tenant_deleted', self._auth_tenant_deleted)

    def _auth_tenant_deleted(self, event):
        with self.tenant_dao.new_session() as session:
            remove_tenant(event['uuid'], session)
